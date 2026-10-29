"""Ensayo offline de límite final por VAD; compara el mismo ASR literal."""
import argparse
from datetime import date,datetime,timezone
import json
from pathlib import Path

from scripts.archivos import write_text_atomic
from scripts.catalogo import ROOT
from scripts.comparar_literalidad import digest
from scripts.lote_literalidad import load_outputs

SELECTION=[1,4,5,6,9,11,16,17]


def prefix_samples(last_end,total,sample_rate=16000):
    """El VAD ya incluye margen; no añadir otro ni recortar el inicio."""
    if last_end is None or last_end<=0:
        raise ValueError('Sin voz detectada: revisión explícita, no entrada vacía al ASR.')
    count=round(last_end*sample_rate)
    if not 0<count<=total:
        raise ValueError('Final VAD fuera de la grabación.')
    return count


def selected_numbers(numbers,total):
    selected=list(SELECTION if numbers is None else numbers)
    if not selected or len(set(selected))!=len(selected) or any(not 1<=n<=total for n in selected):
        raise ValueError('Selección vacía, duplicada o fuera del lote original.')
    return selected


def prepare(source,day,numbers=None):
    import numpy as np
    import soundfile as sf
    date.fromisoformat(day)
    old,outputs=load_outputs(source)
    selection=selected_numbers(numbers,len(old['samples']))
    diagnosis=source/'diagnostico_vad_literal.json'
    vad=json.loads(diagnosis.read_text(encoding='utf-8'))
    assert vad['status']=='completo' and vad['source_manifest_sha256']==digest(source/'manifest.json')
    assert vad['source_outputs_sha256']['candidato']==digest(source/'candidato.json')
    worker=ROOT/'scripts/comparar_literalidad.py'
    assert digest(worker)==outputs['candidato']['script_sha256'],'El trabajador ASR cambió; revisar antes del contraste.'
    for file in old['candidate_model']['files']:
        assert digest(ROOT/'modelos/crisperwhisper2-small'/file['file'])==file['sha256']
    stamp=datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S_%f_cola_vad_UTC')
    folder=ROOT/'resultados/literalidad'/stamp;folder.mkdir(parents=True)
    cache=ROOT/'.descartados/literalidad'/stamp;cache.mkdir(parents=True)
    preserved=[dict(file=p.relative_to(ROOT).as_posix(),sha256=digest(p)) for p in sorted(source.rglob('*.json'))]
    result=dict(experiment='literal_control_final_vad',created_date=day,sample_rate_hz=16000,
        candidate_model=old['candidate_model'],record_per_audio_resources=True,
        source_batch=source.relative_to(ROOT).as_posix(),source_manifest_sha256=digest(source/'manifest.json'),
        source_candidate_sha256=digest(source/'candidato.json'),source_vad_sha256=digest(diagnosis),
        source_worker_sha256=digest(worker),source_parameters=outputs['candidato']['parameters'],
        source_versions=outputs['candidato']['versions'],preserved_sources=preserved,
        selection_original_numbers=selection,vad_options=vad['options'],samples=[],
        notice='Control offline de la cola: mismo candidato literal y parámetros; solo cambia la entrada hasta el último final VAD con margen ya incluido. Se conserva el prefijo completo, con pausas interiores e índice temporal desde cero. Originales intactos; una inferencia nueva por caso. Original literal reutilizado del lote previo: no es una nueva medición pareada de tiempo. Cambiar la duración puede cambiar la geometría/ruta corta-larga de bloques; no aísla una causa interna ni valida el VAD en todo el habla. Selección de números originales: '+str(selection)+'. Partición según el registro de catálogo de cada audio. Sin cambios del seguidor ni publicación automática.')
    for number in selection:
        sample=old['samples'][number-1]
        v=next(r for r in vad['rows'] if r['id']==sample['id'])
        assert v['source_sha256']==sample['source_sha256']
        assert digest(ROOT/sample['source_audio'])==sample['source_sha256']
        assert digest(ROOT/sample['array_file'])==sample['array_sha256']
        original=np.load(ROOT/sample['array_file'],allow_pickle=False)
        count=prefix_samples(v['last_vad_end_seconds'],len(original))
        audio=original[:count].copy()
        array=cache/(sample['id']+'.npy');np.save(array,audio,allow_pickle=False)
        listen=cache/(sample['id']+'.wav');sf.write(listen,audio,16000,subtype='PCM_16')
        result['samples'].append(dict(id=sample['id'],kind=sample['kind'],
            label=f"Audio {number} · {sample['label']}",original_number=number,
            role=('seleccion_explicita' if numbers is not None else 'control' if number in [9,16] else 'problema_senalado'),start=0,end=count/16000,
            original_seconds=sample['end'],removed_tail_seconds=sample['end']-count/16000,
            prefix_end_sample=count,source_audio=sample['source_audio'],source_sha256=sample['source_sha256'],
            original_array_file=sample['array_file'],original_array_sha256=sample['array_sha256'],
            original_listen_file=sample['listen_file'],original_listen_sha256=sample['listen_sha256'],
            array_file=array.relative_to(ROOT).as_posix(),array_sha256=digest(array),
            listen_file=listen.relative_to(ROOT).as_posix(),listen_sha256=digest(listen),
            human_note=sample['human_note'],catalog_record=sample['catalog_record'],
            human_anchor_count=len(v['human_anchors']),
            human_anchors_retained=all(a['fully_covered'] and a['end']<=count/16000 for a in v['human_anchors'])))
    write_text_atomic(folder/'manifest.json',json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    (folder/'fuente_ejecutada.txt').write_bytes(worker.read_bytes())
    (folder/'fuente_preparacion.txt').write_bytes(Path(__file__).read_bytes())
    print(folder,flush=True)
    return folder


def load_comparison(folder):
    manifest=json.loads((folder/'manifest.json').read_text(encoding='utf-8'))
    assert manifest['experiment']=='literal_control_final_vad'
    source=ROOT/manifest['source_batch']
    assert digest(source/'manifest.json')==manifest['source_manifest_sha256']
    assert digest(source/'candidato.json')==manifest['source_candidate_sha256']
    previous=json.loads((source/'candidato.json').read_text(encoding='utf-8'))
    current=json.loads((folder/'candidato.json').read_text(encoding='utf-8'))
    assert current['status']=='completo' and current['manifest_sha256']==digest(folder/'manifest.json')
    assert current['parameters']==manifest['source_parameters']==previous['parameters']
    assert current['versions']==manifest['source_versions']==previous['versions']
    assert current['script_sha256']==manifest['source_worker_sha256']==previous['script_sha256']
    assert [r['id'] for r in current['runs']]==[s['id'] for s in manifest['samples']]
    old_rows={r['id']:r for r in previous['runs']}
    return manifest,previous,current,old_rows


def summarize(folder):
    manifest,previous,current,old_rows=load_comparison(folder)
    lines=['# Control VAD del final: mismo reconocedor literal','',manifest['notice'],'',
        '| Audio original | Papel | Duración original / enviada (s) | Inferencia previa / nueva (s) | Texto idéntico |',
        '|---|---|---:|---:|---|']
    rows=[]
    for sample,new in zip(manifest['samples'],current['runs']):
        old=old_rows[sample['id']]
        same=old['raw_text']==new['raw_text']
        row=dict(original_number=sample['original_number'],id=sample['id'],label=sample['label'],role=sample['role'],
            original_seconds=sample['original_seconds'],sent_seconds=sample['end'],tail_excluded_seconds=sample['removed_tail_seconds'],
            previous_inference_seconds=old['processing_seconds'],new_inference_seconds=new['processing_seconds'],
            previous_cpu_seconds=old['cpu_seconds'],new_cpu_seconds=new['cpu_seconds'],
            previous_ram_sampled_bytes=old['resource_interval']['working_set_max_sampled_bytes'],
            new_ram_sampled_bytes=new['resource_interval']['working_set_max_sampled_bytes'],
            new_rtf_original_duration=new['processing_seconds']/sample['original_seconds'],new_rtf_sent_duration=new['rtf_full_audio'],
            same_raw_text=same,
            new_is_exact_prefix_of_previous=old['raw_text'].startswith(new['raw_text']),
            removed_terminal_text=old['raw_text'][len(new['raw_text']):].strip() if old['raw_text'].startswith(new['raw_text']) else None,
            previous_text=old['raw_text'],new_text=new['raw_text'])
        rows.append(row)
        lines.append(f"| {sample['label']} | {sample['role']} | {sample['original_seconds']:.3f} / {sample['end']:.3f} | {old['processing_seconds']:.2f} / {new['processing_seconds']:.2f} | {'sí' if same else 'no'} |")
    totals=dict(original_audio_seconds=sum(r['original_seconds'] for r in rows),sent_audio_seconds=sum(r['sent_seconds'] for r in rows),
        previous_inference_seconds=sum(r['previous_inference_seconds'] for r in rows),new_inference_seconds=sum(r['new_inference_seconds'] for r in rows),
        new_model_load_seconds=current['model_load_seconds'],new_process_peak_ram_bytes=current['resources']['final_memory'].get('process_lifetime_peak_working_set_bytes'),
        note=f"Previo reutilizado de {len(previous['runs'])} casos; variante medida en proceso nuevo de {len(rows)}. Orden/estado térmico/caché pueden influir. VAD previo medido aparte, no incluido en estas inferencias. RAM muestreada por caso y pico de proceso no son el mismo indicador; CPU incluye instrumentación y GPU es global.")
    lines+=['','## Coste y límites','',
        f"Entradas originales: {totals['original_audio_seconds']:.3f} s; enviadas a la variante: {totals['sent_audio_seconds']:.3f} s. Inferencia original reutilizada: {totals['previous_inference_seconds']:.2f} s; nueva: {totals['new_inference_seconds']:.2f} s; carga única nueva: {totals['new_model_load_seconds']:.2f} s.",'',totals['note'],'',
        'RTF original y RTF sobre entrada enviada se guardan separados en metricas.json; acortar una cola cambia el denominador. La carga y VAD se contabilizan aparte; no son latencia de tablet ni del seguidor. Las marcas ASR siguen sin validar. Sin nueva referencia humana de estos textos ni precisión/F1 global.','',
        '## Salidas intactas para revisión']
    for row in rows:
        lines+=['',f"### {row['label']}",'','**Literal original, lote previo:** '+row['previous_text'],'',
                '**Literal con control del final, inferencia nueva:** '+row['new_text']]
    lines+=['','Escuchar el original completo y, opcionalmente, solo el prefijo enviado en http://127.0.0.1:8778/. El texto del cuento no se entrega al ASR y no se corrigen automáticamente sus errores.']
    write_text_atomic(folder/'resumen.md','\n'.join(lines)+'\n')
    write_text_atomic(folder/'metricas.json',json.dumps(dict(rows=rows,totals=totals),ensure_ascii=False,indent=2)+'\n')
    (folder/'fuente_informe.txt').write_bytes(Path(__file__).read_bytes())
    print(folder/'resumen.md',flush=True)


def verify(folder):
    import numpy as np
    manifest,previous,current,_=load_comparison(folder)
    source=ROOT/manifest['source_batch']
    assert digest(source/'diagnostico_vad_literal.json')==manifest['source_vad_sha256']
    for entry in manifest['preserved_sources']:
        assert digest(ROOT/entry['file'])==entry['sha256'],entry['file']
    for sample in manifest['samples']:
        for pathkey,hashkey in [('source_audio','source_sha256'),('array_file','array_sha256'),('listen_file','listen_sha256'),('original_array_file','original_array_sha256'),('original_listen_file','original_listen_sha256')]:
            assert digest(ROOT/sample[pathkey])==sample[hashkey]
        original=np.load(ROOT/sample['original_array_file'],allow_pickle=False)
        sent=np.load(ROOT/sample['array_file'],allow_pickle=False)
        assert np.array_equal(sent,original[:sample['prefix_end_sample']])
        assert len(sent)/16000==sample['end'] and sample['human_anchors_retained']
    for item in manifest['candidate_model']['files']:
        assert digest(ROOT/'modelos/crisperwhisper2-small'/item['file'])==item['sha256']
    assert digest(folder/'fuente_ejecutada.txt')==current['script_sha256']
    result=dict(manifest_sha256=digest(folder/'manifest.json'),new_output_sha256=digest(folder/'candidato.json'),
        previous_output_sha256=manifest['source_candidate_sha256'],prefixes_verified=len(manifest['samples']),
        human_anchors_retained=sum(s['human_anchor_count'] for s in manifest['samples']),
        source_files_unchanged=len(manifest['preserved_sources']),same_parameters_versions_worker=True,
        note='No acredita fidelidad de las nuevas salidas ni cobertura de todos los intentos; conserva original y pausas interiores.')
    write_text_atomic(folder/'integridad.json',json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(result,ensure_ascii=False),flush=True)


def viewer(folder):
    manifest,previous,current,old_rows=load_comparison(folder)
    samples=[];clips={}
    for item,new in zip(manifest['samples'],current['runs']):
        for key,hashkey,suffix in [('original_listen_file','original_listen_sha256',''),('listen_file','listen_sha256','__prefix')]:
            path=(ROOT/item[key]).resolve()
            assert path.is_relative_to((ROOT/'.descartados/literalidad').resolve()) and digest(path)==item[hashkey]
            clips[item['id']+suffix]=path
        samples.append(dict(id=item['id'],label=item['label'],kind=item['kind'],start=0,end=item['original_seconds'],
            sent_seconds=item['end'],note=item['human_note'],clip='/clip/'+item['id'],processed_clip='/clip/'+item['id']+'__prefix',
            outputs=dict(baseline=old_rows[item['id']],candidato=new)))
    metrics=dict(baseline=dict(load=None,seconds=sum(old_rows[s['id']]['processing_seconds'] for s in manifest['samples']),ram_mib=None,reused=True),
        candidato=dict(load=current['model_load_seconds'],seconds=sum(r['processing_seconds'] for r in current['runs']),
            ram_mib=current['resources']['final_memory'].get('process_lifetime_peak_working_set_bytes',0)/1048576))
    return dict(samples=samples,metrics=metrics,notice=manifest['notice'],batch=True,comparison_complete=False,tail_comparison=True,
        input_seconds=sum(s['original_seconds'] for s in manifest['samples']),sent_seconds=sum(s['end'] for s in manifest['samples']),
        panel_labels=dict(baseline='Literal original · reutilizado',candidato='Literal con final VAD · nuevo'),
        panel_descriptions=dict(baseline='CrisperWhisper Small CPU float32 · WAV completo · medición previa',candidato='Mismo modelo y ajustes · prefijo hasta el último VAD con margen')),clips


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('mode',choices=['preparar','resumir','verificar'])
    parser.add_argument('folder',type=Path)
    parser.add_argument('--fecha')
    parser.add_argument('--audios',nargs='+',type=int,help='Números del manifiesto original; por defecto seis problemas y dos controles.')
    args=parser.parse_args()
    if args.mode=='preparar':
        if not args.fecha:
            parser.error('Indica --fecha local del experimento.')
        prepare(args.folder.resolve(),args.fecha,args.audios)
    elif args.mode=='resumir':
        summarize(args.folder.resolve())
    else:
        verify(args.folder.resolve())


if __name__=='__main__':
    main()
