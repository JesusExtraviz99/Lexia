"""Diagnóstico VAD de entradas literales: no recorta audio ni repite ASR."""
import argparse
from dataclasses import asdict
import importlib.metadata
import json
from pathlib import Path
from time import perf_counter,process_time

from scripts.archivos import write_text_atomic
from scripts.catalogo import ROOT
from scripts.comparar_literalidad import digest
from scripts.lote_literalidad import load_outputs
from scripts.recursos import ResourceMonitor


def covered_seconds(start,end,intervals):
    """Intersección con la unión de intervalos; no contar solapamientos dos veces."""
    if end<start:
        raise ValueError('Intervalo invertido.')
    clipped=sorted((max(start,a),min(end,b)) for a,b in intervals if min(end,b)>max(start,a))
    total=0.;last=None
    for a,b in clipped:
        if last is None:
            last=[a,b]
        elif a<=last[1]:
            last[1]=max(last[1],b)
        else:
            total+=last[1]-last[0];last=[a,b]
    return total+(last[1]-last[0] if last else 0.)


def diagnose(folder,day):
    import numpy as np
    from faster_whisper import vad
    from faster_whisper.utils import get_assets_path
    manifest,outputs=load_outputs(folder)
    target=folder/'diagnostico_vad_literal.json'
    if target.exists():
        raise FileExistsError('Este diagnóstico existe. Conservarlo antes de preparar otro contraste.')
    original_hashes={e:digest(folder/(e+'.json')) for e in outputs}
    options=vad.VadOptions(threshold=.5,min_speech_duration_ms=0,min_silence_duration_ms=2000,speech_pad_ms=400)
    model_file=Path(get_assets_path())/'silero_vad_v6.onnx'
    record=dict(date=day,kind='diagnostico_solo_VAD_sin_reconocimiento_de_texto',
        source_manifest_sha256=digest(folder/'manifest.json'),source_outputs_sha256=original_hashes,
        model_file=str(model_file.relative_to(ROOT)),model_sha256=digest(model_file),
        vad_source_sha256=digest(Path(vad.__file__)),script_sha256=digest(Path(__file__)),
        versions={name:importlib.metadata.version(name) for name in ['faster-whisper','onnxruntime','numpy']},
        device='cpu',vad_model_threads=1,options=asdict(options),rows=[],
        notice='Inferencia VAD nueva sobre los arrays originales del lote; no es ASR nuevo. Intervalos VAD con margen, no referencia humana ni detector perfecto. No se recorta, concatena, cambia la duración ni filtra ninguna salida. La cobertura de anclas solo comprueba límites ya anotados; no valida todas las sílabas/trabadas. Parámetros iniciales, no óptimos.')
    monitor=ResourceMonitor();monitor.start()
    try:
        start=perf_counter();vad.get_vad_model();record['model_load_seconds']=perf_counter()-start
        for number,sample in enumerate(manifest['samples'],1):
            array_file=ROOT/sample['array_file']
            if digest(array_file)!=sample['array_sha256'] or digest(ROOT/sample['source_audio'])!=sample['source_sha256']:
                raise ValueError('La entrada ha cambiado.')
            audio=np.load(array_file,allow_pickle=False)
            start=perf_counter();cpu=process_time()
            detected=vad.get_speech_timestamps(audio,vad_options=options,sampling_rate=16000)
            seconds=perf_counter()-start;cpu_seconds=process_time()-cpu
            intervals=[(s['start']/16000,s['end']/16000) for s in detected]
            candidate=next(r for r in outputs['candidato']['runs'] if r['id']==sample['id'])
            chunks=candidate['native_result']['chunks'] or [dict(chunk_idx=0,start_sec=0,end_sec=sample['end'],text=candidate['raw_text'],is_last=True)]
            checks=[]
            for chunk in chunks:
                covered=covered_seconds(chunk['start_sec'],chunk['end_sec'],intervals)
                checks.append(dict(index=chunk['chunk_idx'],start=chunk['start_sec'],end=chunk['end_sec'],
                    vad_positive_seconds_with_padding=covered,no_vad_overlap=covered==0,
                    candidate_text=chunk['text'],is_last=chunk['is_last']))
            row=dict(number=number,id=sample['id'],audio=sample['source_audio'],source_sha256=sample['source_sha256'],
                audio_seconds=sample['end'],processing_seconds=seconds,cpu_seconds=cpu_seconds,
                intervals_seconds=intervals,last_vad_end_seconds=max((b for a,b in intervals),default=None),
                candidate_input_blocks=checks,human_anchors=[])
            annotation_name=sample['catalog_record'].get('annotation_file')
            if annotation_name:
                path=ROOT/annotation_name
                data=json.loads(path.read_text(encoding='utf-8'))
                if data['audio_sha256']!=sample['source_sha256']:
                    raise ValueError('Anotación de otro audio.')
                row['annotation_file']=annotation_name;row['annotation_sha256']=digest(path)
                for word in data.get('words',[]):
                    if word.get('reviewed') and word.get('start') is not None and word.get('end') is not None:
                        a,b=word['start'],word['end'];covered=covered_seconds(a,b,intervals)
                        row['human_anchors'].append(dict(word=word['word'],start=a,end=b,
                            covered_seconds=covered,fully_covered=covered>=b-a-1e-6))
            record['rows'].append(row)
            print(number,sample['id'],'último VAD',row['last_vad_end_seconds'],flush=True)
        record['status']='completo'
    finally:
        record['resources']=monitor.stop()
    if any(digest(folder/(e+'.json'))!=h for e,h in original_hashes.items()):
        raise ValueError('Cambió una salida ASR durante el diagnóstico.')
    record['asr_outputs_unchanged']=True
    anchors=[a for r in record['rows'] for a in r['human_anchors']]
    record['human_anchors_count']=len(anchors)
    record['human_anchors_fully_covered']=sum(a['fully_covered'] for a in anchors)
    write_text_atomic(target,json.dumps(record,ensure_ascii=False,indent=2)+'\n')
    (folder/'fuente_diagnostico_vad.txt').write_bytes(Path(__file__).read_bytes())
    lines=['# Diagnóstico de voz antes de nuevas transcripciones','',record['notice'],'',
        f"{len(record['rows'])} WAV; inferencia VAD total {sum(r['processing_seconds'] for r in record['rows']):.2f} s; carga {record['model_load_seconds']:.2f} s. CPU, memoria y GPU global disponibles en el JSON; ASR no ejecutado.",'',
        f"Anclas humanas completamente cubiertas por intervalos VAD con margen: {record['human_anchors_fully_covered']}/{record['human_anchors_count']}. Esto no equivale a sensibilidad global ni valida fragmentos sin tiempos humanos.",'',
        '| Audio | Último final VAD con margen (s) | Último bloque del candidato | Solapamiento VAD en ese bloque (s) |',
        '|---|---:|---|---:|']
    for row in record['rows']:
        last=row['candidate_input_blocks'][-1]
        lines.append(f"| {row['number']} · {Path(row['audio']).name} | {row['last_vad_end_seconds']} | {last['start']}–{last['end']} | {last['vad_positive_seconds_with_padding']:.3f} |")
    lines+=['','No se han descartado esos bloques ni evaluado una transcripción corregida. Un resultado sin solapamiento VAD es una propuesta de zona sin voz; suprimirla puede perder habla débil o fragmentos. El siguiente ensayo debe conservar originales, márgenes y mapa temporal, y medir tanto texto añadido como habla omitida. Las pausas originales permanecen disponibles para las estadísticas.','',
        'Control inicial: threshold 0,5; no descartar segmentos detectados por duración mínima; separación tras 2 s y margen 400 ms. Modelo Silero v6 de faster-whisper ya instalado. No son umbrales ideales demostrados.']
    write_text_atomic(folder/'diagnostico_vad_literal.md','\n'.join(lines)+'\n')
    print('Anclas:',record['human_anchors_fully_covered'],'/',record['human_anchors_count'],flush=True)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('folder',type=Path)
    parser.add_argument('--fecha',required=True)
    args=parser.parse_args();diagnose(args.folder.resolve(),args.fecha)


if __name__=='__main__':
    main()
