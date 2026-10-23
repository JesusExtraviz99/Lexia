"""Piloto de literalidad separado del seguidor, con entradas fijadas y controles."""
import argparse
from dataclasses import asdict
from datetime import datetime
import hashlib
import importlib.metadata
import json
import os
from pathlib import Path
from time import perf_counter, process_time

from scripts.archivos import write_text_atomic
from scripts.catalogo import ROOT, resolve_audio_path
from scripts.recursos import ResourceMonitor


def digest(path):
    value=hashlib.sha256()
    with Path(path).open('rb') as stream:
        for chunk in iter(lambda:stream.read(1024*1024),b''):
            value.update(chunk)
    return value.hexdigest()


def prepare():
    import numpy as np
    import soundfile as sf
    from faster_whisper.audio import decode_audio
    reference=ROOT/'datos/anotaciones/lectura_02_trabadas_revision_cualitativa.json'
    human=json.loads(reference.read_text(encoding='utf-8'))
    control_reference=ROOT/'datos/referencias/lectura_normal.json'
    control=json.loads(control_reference.read_text(encoding='utf-8'))
    normal=resolve_audio_path(control['audio_file'])
    trabadas=resolve_audio_path(human['audio_file'])
    assert digest(normal)==control['audio_sha256'] and digest(trabadas)==human['audio_sha256']
    stamp=datetime.now().strftime('%Y%m%d_%H%M%S_%f')
    folder=ROOT/'resultados/literalidad'/stamp
    cache=ROOT/'.descartados/literalidad'/stamp
    folder.mkdir(parents=True);cache.mkdir(parents=True)
    metadata=json.loads((ROOT/'.tools/modelo_literal_procedencia.json').read_text(encoding='utf-8'))
    result=dict(experiment='baseline_y_crisper_small_literal',created_date='2026-10-23',
                candidate_model=metadata,reference_file=reference.relative_to(ROOT).as_posix(),
                reference_sha256=digest(reference),control_reference_sha256=digest(control_reference),
                sample_rate_hz=16000,samples=[],
                notice='Exploración: una pasada por motor. Cuatro muestras con revisión cualitativa, dos controles fluidos y uno sin habla según referencia del lector. Notas no son conteos por evento ni referencia exhaustiva. No se proporciona el cuento o las notas al reconocedor. Mismos arrays de entrada, modelos y backends/precisiones distintos; sin cambio del seguidor.')
    specs=[dict(id=s['id'],kind='trabadas',start=s['start'],end=s['end'],source=trabadas,
                human_note=next(r['notes'] for r in human['reviews'] if r['id']==s['id'])) for s in human['intervals']]
    specs += [dict(id='fluida_inicio',kind='control_fluido',start=0,end=8,source=normal,human_note='Lectura normal validada por el lector; ruido breve inicial comunicado.'),
              dict(id='fluida_medio',kind='control_fluido',start=8,end=16,source=normal,human_note='Lectura normal validada por el lector; evaluar posibles fragmentos de borde como tales.'),
              dict(id='sin_habla',kind='control_sin_habla',start=30,end=38,source=normal,human_note='Según el lector, tras 23–24 s hay silencio con ruidos ambientales leves, sin habla adicional.')]
    decoded={}
    for item in specs:
        source=item.pop('source')
        if source not in decoded:
            decoded[source]=decode_audio(str(source),sampling_rate=16000)
        clip=decoded[source][round(item['start']*16000):round(item['end']*16000)].copy()
        assert len(clip)==8*16000
        array_path=cache/(item['id']+'.npy'); np.save(array_path,clip,allow_pickle=False)
        audio_path=cache/(item['id']+'.wav');sf.write(audio_path,clip,16000,subtype='PCM_16')
        result['samples'].append(dict(**item,source_audio=source.relative_to(ROOT).as_posix(),source_sha256=digest(source),
                                     array_file=array_path.relative_to(ROOT).as_posix(),array_sha256=digest(array_path),
                                     listen_file=audio_path.relative_to(ROOT).as_posix(),listen_sha256=digest(audio_path)))
    write_text_atomic(folder/'manifest.json',json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(folder,flush=True)
    return folder


def prepare_complete(pilot):
    """Fija el WAV entero y enlaza el piloto anterior sin alterar sus resultados."""
    import numpy as np
    import soundfile as sf
    from faster_whisper.audio import decode_audio
    prior=json.loads((pilot/'manifest.json').read_text(encoding='utf-8'))
    sample=next(s for s in prior['samples'] if s['id']=='medio_1')
    source=ROOT/sample['source_audio']
    if digest(source)!=sample['source_sha256']:
        raise ValueError('El audio original ha cambiado.')
    audio=decode_audio(str(source),sampling_rate=16000)
    previous=np.load(ROOT/sample['array_file'],allow_pickle=False)
    if digest(ROOT/sample['array_file'])!=sample['array_sha256'] or not np.array_equal(previous,audio[16*16000:24*16000]):
        raise ValueError('El recorte previo no coincide exactamente con el audio completo.')
    stamp=datetime.now().strftime('%Y%m%d_%H%M%S_%f')
    folder=ROOT/'resultados/literalidad'/stamp
    cache=ROOT/'.descartados/literalidad'/stamp
    folder.mkdir(parents=True);cache.mkdir(parents=True)
    array=cache/'completa.npy';np.save(array,audio,allow_pickle=False)
    listen=cache/'completa.wav';sf.write(listen,audio,16000,subtype='PCM_16')
    result=dict(experiment='literalidad_audio_completo_frente_recortes',created_date=datetime.now().date().isoformat(),
        candidate_model=prior['candidate_model'],sample_rate_hz=16000,
        source_pilot=pilot.relative_to(ROOT).as_posix(),
        prior_hashes={name:digest(pilot/name) for name in ['manifest.json','baseline.json','candidato.json']},
        samples=[dict(id='completa',kind='trabadas',start=0,end=len(audio)/16000,
            human_note='Lectura completa con trabadas variables, según el lector. No es una referencia literal exhaustiva. Comparar con las notas y el error confirmado del recorte 16–24 s.',
            source_audio=sample['source_audio'],source_sha256=sample['source_sha256'],
            array_file=array.relative_to(ROOT).as_posix(),array_sha256=digest(array),
            listen_file=listen.relative_to(ROOT).as_posix(),listen_sha256=digest(listen))],
        notice='Mismo WAV completo para ambos motores, sin cuento ni notas como prompt; una pasada offline. Se conservan modelo y ajustes del piloto corto. Para entradas mayores de 30 s el candidato activa su estrategia interna continuation (ventanas 30 s, paso 26 s y contexto generado). No escucha toda la grabación en una única ventana. Cambian duración y procesamiento interno: no se aísla una causa del error ni se mide seguimiento en directo. Comparar el tramo revisado, sin convertir diferencias de texto en métricas humanas.')
    write_text_atomic(folder/'manifest.json',json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(folder,flush=True)
    return folder


def run(folder,engine):
    import numpy as np
    if (folder/(engine+'.json')).exists():
        raise FileExistsError('Ese resultado ya existe. Usa preparar para crear otro piloto y conservar el anterior.')
    os.environ['HF_HUB_OFFLINE']='1'
    os.environ['HF_HOME']=str(ROOT/'.tools/cache/hf-literal')
    os.environ['TOKENIZERS_PARALLELISM']='false'
    manifest=json.loads((folder/'manifest.json').read_text(encoding='utf-8'))
    for sample in manifest['samples']:
        if digest(ROOT/sample['array_file'])!=sample['array_sha256'] or digest(ROOT/sample['source_audio'])!=sample['source_sha256']:
            raise ValueError('La entrada ha cambiado respecto al manifiesto.')
    names=['numpy']+(['faster-whisper','ctranslate2','av'] if engine=='baseline' else ['crisperwhisper','torch','transformers','tokenizers'])
    output=dict(engine=engine,device='cpu',cpu_threads=4,compute_type='int8' if engine=='baseline' else 'float32',
                backend='ctranslate2' if engine=='baseline' else 'transformers',
                versions={name:importlib.metadata.version(name) for name in names},
                script_sha256=digest(Path(__file__)),manifest_sha256=digest(folder/'manifest.json'),runs=[],
                notice='Un proceso y modelo compartido por motor. Recursos del proceso completo, incluida carga y muestreo. Sin VAD para conservar entrada; GPU global no implica uso por ASR. No mide latencia del seguidor ni rendimiento de tablet.')
    monitor=ResourceMonitor();monitor.start()
    try:
        start=perf_counter()
        if engine=='baseline':
            from faster_whisper import WhisperModel
            model=WhisperModel(str(ROOT/'modelos/faster-whisper-small'),device='cpu',compute_type='int8',cpu_threads=4,local_files_only=True)
            params=dict(language='es',beam_size=5,word_timestamps=True,vad_filter=False,condition_on_previous_text=False)
        else:
            import torch
            from crisperwhisper import CrisperWhisperModel
            torch.set_num_threads(4)
            model=CrisperWhisperModel(str(ROOT/'modelos/crisperwhisper2-small'),backend='transformers',compute_type='float32',device='cpu')
            params=dict(language='es',mode='verbatim',sr=16000,word_timestamps=True,max_new_tokens=256,
                        hallucination_mitigation=True,temperature_fallback=True)
            if any(s['end']-s['start']>30 for s in manifest['samples']):
                params.update(longform_strategy='continuation',chunk_duration=30.0,stride=26.0,
                              context_words=12,drop_words=2,timestamp_aware_drop=True,early_eot_recovery=True)
        output['model_load_seconds']=perf_counter()-start
        output['parameters']=params
        for sample in manifest['samples']:
            clip=np.load(ROOT/sample['array_file'],allow_pickle=False)
            start=perf_counter();cpu=process_time()
            if engine=='baseline':
                segments,_=model.transcribe(clip.copy(),**params)
                raw=[];words=[]
                for segment in segments:
                    raw.append(segment.text)
                    words.extend(dict(word=w.word,start=w.start,end=w.end,probability=w.probability) for w in segment.words or [])
                text=' '.join(raw)
                native=None
            else:
                native=model.transcribe(clip.copy(),**params)
                text=native.text
                words=[asdict(w) for w in native.words or []]
            row=dict(id=sample['id'],kind=sample['kind'],raw_text=text,words=words,
                     processing_seconds=perf_counter()-start,cpu_seconds=process_time()-cpu,
                     word_time_convention='tiempos relativos al recorte; no son marcas humanas')
            if native is not None:
                row['native_result']=asdict(native)
            output['runs'].append(row)
            write_text_atomic(folder/(engine+'.json'),json.dumps(output,ensure_ascii=False,indent=2)+'\n')
            print(engine,sample['id'],repr(text),flush=True)
        output['status']='completo'
    except BaseException as exc:
        output['status']='error';output['error']=str(exc)
        raise
    finally:
        output['resources']=monitor.stop()
        output['environment_packages']=sorted(f'{d.metadata["Name"]}=={d.version}' for d in importlib.metadata.distributions())
        write_text_atomic(folder/(engine+'.json'),json.dumps(output,ensure_ascii=False,indent=2)+'\n')


def summarize(folder):
    manifest=json.loads((folder/'manifest.json').read_text(encoding='utf-8'))
    outputs={name:json.loads((folder/(name+'.json')).read_text(encoding='utf-8')) for name in ['baseline','candidato']}
    if any(o.get('status')!='completo' or len(o['runs'])!=len(manifest['samples']) or {r['id'] for r in o['runs']}!={s['id'] for s in manifest['samples']} for o in outputs.values()):
        raise ValueError('Faltan ejecuciones completas.')
    lines=['# Piloto de transcripción literal', '',manifest['notice'],'',
           '| Muestra | Nota de escucha del lector | Faster Whisper Small | CrisperWhisper Small · literal |',
           '|---|---|---|---|']
    for sample in manifest['samples']:
        texts=[next(r['raw_text'] for r in outputs[e]['runs'] if r['id']==sample['id']) for e in ['baseline','candidato']]
        fields=[sample['id'],sample['human_note'],*texts]
        lines.append('| '+' | '.join(f.replace('|','/').replace('\n',' ') for f in fields)+' |')
    lines+=['','## Cómputo de esta implementación','',
            '| Motor | Backend / precisión | Carga (s) | Suma inferencias (s) | Pico RAM del proceso (MiB) |',
            '|---|---|---:|---:|---:|']
    for name,data in outputs.items():
        memory=data['resources'].get('final_memory',{})
        peak=memory.get('process_lifetime_peak_working_set_bytes')
        lines.append(f"| {name} | {data['backend']} / {data['compute_type']} | {data['model_load_seconds']:.2f} | {sum(r['processing_seconds'] for r in data['runs']):.2f} | {peak/1048576 if peak else 'no medido'} |")
    duration=sum(s['end']-s['start'] for s in manifest['samples'])
    lines+=['',f'Las entradas suman {duration:.2f} s por motor. Las dos implementaciones cambian modelo, backend y precisión; calidad exploratoria y coste observado no aíslan el efecto del entrenamiento ni predicen tablet. CPU/RAM/GPU completas en cada JSON. No se calculan tasas de detección o conteos exactos sin revisión por evento.','',
            'No se introdujo el cuento ni las notas humanas como prompt. Comprobar todo texto nuevo contra el audio antes de considerarlo una mejora. Los fragmentos al borde de una ventana pueden estar incompletos por el corte.']
    write_text_atomic(folder/'resumen.md','\n'.join(lines)+'\n')
    print(folder/'resumen.md',flush=True)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('mode',choices=['preparar','preparar_completo','baseline','candidato','resumir'])
    parser.add_argument('folder',nargs='?',type=Path)
    args=parser.parse_args()
    if args.mode=='preparar':
        prepare()
    elif args.mode=='preparar_completo':
        if args.folder is None:
            parser.error('Indica la carpeta del piloto previo.')
        prepare_complete(args.folder.resolve())
    elif args.folder is None:
        parser.error('Falta la carpeta del manifiesto.')
    elif args.mode=='resumir':
        summarize(args.folder.resolve())
    else:
        run(args.folder.resolve(),args.mode)


if __name__=='__main__':
    main()
