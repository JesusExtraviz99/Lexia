"""Ablaciones de un ajuste sobre tomas 2/3 y diagnóstico separado de contexto."""
import argparse
from dataclasses import asdict
from datetime import datetime, timezone
import importlib.metadata
import json
import os
from pathlib import Path
import shutil
from time import perf_counter, process_time

from scripts.archivos import write_text_atomic
from scripts.catalogo import ROOT
from scripts.comparar_literalidad import digest, resource_interval
from scripts.recursos import ResourceMonitor, memory_snapshot

SOURCE = ROOT/'resultados/literalidad/20261026_082404_701027_cola_vad_UTC'
CHANGES = {'sin_reparacion': {'hallucination_mitigation': False},
           'sin_temperaturas_alternativas': {'temperature_fallback': False},
           'sin_recuperacion_cierre': {'early_eot_recovery': False}}


def save(path, value):
    write_text_atomic(path, json.dumps(value, ensure_ascii=False, indent=2)+'\n')


def prepare():
    import numpy as np
    import soundfile as sf
    old=json.loads((SOURCE/'manifest.json').read_text(encoding='utf-8'))
    result=json.loads((SOURCE/'candidato.json').read_text(encoding='utf-8'))
    assert result['status']=='completo' and result['manifest_sha256']==digest(SOURCE/'manifest.json')
    stamp=datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S_%f_intentos_UTC')
    folder=ROOT/'resultados/literalidad'/stamp;folder.mkdir()
    cache=ROOT/'.descartados/literalidad'/stamp;cache.mkdir()
    samples=[]
    for number in [3,2]:
        s=old['samples'][number-1]
        assert digest(ROOT/s['array_file'])==s['array_sha256']
        assert digest(ROOT/s['source_audio'])==s['source_sha256']
        samples.append(dict(**s,experiment_id=f'toma_{number}',take=number,
                            input_scope='prefijo_VAD_completo',absolute_start=0))
    target=samples[0]
    ref=next(r for r in result['runs'] if r['id']==target['id'])
    # Borde interno real del último bloque; no marca humana ni corte fonético.
    last=ref['native_result']['chunks'][-1]
    start=last['start_sec'];end=target['end']
    array=np.load(ROOT/target['array_file'],allow_pickle=False)
    crop=array[round(start*16000):round(end*16000)].copy()
    path=cache/'ultimo_bloque.npy';np.save(path,crop,allow_pickle=False)
    wav=cache/'ultimo_bloque.wav';sf.write(wav,crop,16000,subtype='PCM_16')
    samples.append(dict(**{k:v for k,v in target.items() if k not in ['array_file','array_sha256','listen_file','listen_sha256','experiment_id','input_scope','absolute_start','end']},
                        experiment_id='toma_3_ultimo_bloque',input_scope='recorte_diagnostico_sin_contexto_previo',
                        absolute_start=start,end=end-start,array_file=path.relative_to(ROOT).as_posix(),
                        array_sha256=digest(path),listen_file=wav.relative_to(ROOT).as_posix(),listen_sha256=digest(wav)))
    jobs=[dict(sample=s['experiment_id'],variant=variant,changes=changes)
          for variant,changes in CHANGES.items() for s in samples[:2]]
    jobs.append(dict(sample=samples[2]['experiment_id'],variant='recorte_ajustes_originales',changes={}))
    manifest=dict(created_date='2026-10-26',experiment='ablaciones_intentos_literal',
        source_batch=SOURCE.relative_to(ROOT).as_posix(),
        source_hashes={name:digest(SOURCE/name) for name in ['manifest.json','candidato.json','integridad.json']},
        candidate_model=old['candidate_model'],parameters=result['parameters'],versions=result['versions'],
        samples=samples,jobs=jobs,cache=cache.relative_to(ROOT).as_posix(),
        notice='Exploración de desarrollo sobre tomas 2/3; 5/6 reservadas intactas. Mismo prefijo VAD para cada ablación, un solo parámetro distinto. Referencia original reutilizada, no benchmark pareado. El recorte del último bloque cambia entrada y contexto: contraste separado, no aislación causal de un parámetro. Marcas automáticas no son tiempos humanos. No se suministra cuento, palabra objetivo o transcripción como prompt. Sin cambios del seguidor.')
    save(folder/'manifest.json',manifest)
    (folder/'fuente_experimento.txt').write_bytes(Path(__file__).read_bytes())
    print(folder,flush=True)


def run(folder):
    import numpy as np
    import torch
    from crisperwhisper import CrisperWhisperModel
    if (folder/'resultados.json').exists():
        raise FileExistsError('Conservar salida anterior; prepara otro experimento.')
    m=json.loads((folder/'manifest.json').read_text(encoding='utf-8'))
    source=ROOT/m['source_batch']
    for name,sha in m['source_hashes'].items():
        assert digest(source/name)==sha
    for item in m['candidate_model']['files']:
        assert digest(ROOT/'modelos/crisperwhisper2-small'/item['file'])==item['sha256']
    versions={name:importlib.metadata.version(name) for name in m['versions']}
    assert versions==m['versions']
    os.environ['HF_HUB_OFFLINE']='1';os.environ['TOKENIZERS_PARALLELISM']='false'
    torch.set_num_threads(4)
    output=dict(manifest_sha256=digest(folder/'manifest.json'),script_sha256=digest(Path(__file__)),
                versions=versions,device='cpu',compute_type='float32',cpu_threads=4,runs=[],status='en_curso')
    monitor=ResourceMonitor();monitor.start()
    try:
        start=perf_counter()
        model=CrisperWhisperModel(str(ROOT/'modelos/crisperwhisper2-small'),backend='transformers',compute_type='float32',device='cpu')
        output['model_load_seconds']=perf_counter()-start
        for job in m['jobs']:
            sample=next(s for s in m['samples'] if s['experiment_id']==job['sample'])
            assert digest(ROOT/sample['array_file'])==sample['array_sha256']
            audio=np.load(ROOT/sample['array_file'],allow_pickle=False)
            params={**m['parameters'],**job['changes']}
            differences={key:value for key,value in params.items() if m['parameters'].get(key)!=value}
            assert differences==job['changes']
            if job['sample']!='toma_3_ultimo_bloque':
                assert len(differences)==1
            before=memory_snapshot();start=perf_counter();cpu=process_time()
            native=model.transcribe(audio.copy(),**params)
            elapsed=perf_counter()-start;cpu_elapsed=process_time()-cpu
            output['runs'].append(dict(**job,parameters=params,raw_text=native.text,
                words=[asdict(w) for w in native.words or []],native_result=asdict(native),
                processing_seconds=elapsed,cpu_seconds=cpu_elapsed,audio_seconds=len(audio)/16000,
                absolute_start=sample['absolute_start'],
                resource_interval=resource_interval(monitor,start-monitor.wall_start,start-monitor.wall_start+elapsed,
                                                   cpu_elapsed,before,memory_snapshot())))
            save(folder/'resultados.json',output)
            print(job['sample'],job['variant'],repr(native.text),flush=True)
        output['status']='completo'
    except BaseException as exc:
        output['status']='error';output['error']=str(exc)
        raise
    finally:
        output['resources']=monitor.stop()
        save(folder/'resultados.json',output)


def summarize(folder):
    m=json.loads((folder/'manifest.json').read_text(encoding='utf-8'))
    r=json.loads((folder/'resultados.json').read_text(encoding='utf-8'))
    assert r['status']=='completo' and len(r['runs'])==len(m['jobs'])
    assert r['manifest_sha256']==digest(folder/'manifest.json')
    assert r['script_sha256']==digest(folder/'fuente_experimento.txt')
    source=ROOT/m['source_batch']
    for name,sha in m['source_hashes'].items():
        assert digest(source/name)==sha
    prior=json.loads((source/'candidato.json').read_text(encoding='utf-8'))
    rows=[];clips=[]
    lines=['# Intentos parciales: ablaciones del literal','',m['notice'],'']
    viewer=ROOT/m['cache']/'visor';viewer.mkdir(exist_ok=True)
    for s in m['samples']:
        assert digest(ROOT/s['array_file'])==s['array_sha256']
        assert digest(ROOT/s['listen_file'])==s['listen_sha256']
        assert digest(ROOT/s['source_audio'])==s['source_sha256']
        wavname=s['experiment_id']+'.wav';shutil.copyfile(ROOT/s['listen_file'],viewer/wavname)
        clips.append(dict(id=s['experiment_id'],audio=wavname,start=s['absolute_start'],end=s['absolute_start']+s['end']))
        lines+=['',f"## {s['experiment_id']} · audio {s['absolute_start']:.2f}–{s['absolute_start']+s['end']:.2f} s",'']
        ref=next(v for v in prior['runs'] if v['id']==s['id'])
        if s['input_scope']=='prefijo_VAD_completo':
            rows.append(dict(sample=s['experiment_id'],variant='Referencia original · reutilizada',text=ref['raw_text'],seconds=None))
            lines+=['**Referencia reutilizada:** '+ref['raw_text'],'']
        for result in [v for v in r['runs'] if v['sample']==s['experiment_id']]:
            rows.append(dict(sample=s['experiment_id'],variant=result['variant'],text=result['raw_text'],seconds=result['processing_seconds']))
            lines += [f"**{result['variant']}** ({result['processing_seconds']:.2f} s): "+result['raw_text'],'']
    lines+=['','Las salidas no se corrigen ni convierten automáticamente en eventos. El objetivo humano confirmado es regres- re- regresar; no se entrega al modelo. Recorte a partir de 52 s según bloque automático, no límite humano de palabra. Las variantes pueden no ejecutar internamente una ruta desactivada: igualdad de salida no prueba que esa ruta causase o no el error. CPU/RAM/GPU global en resultados.json; inferencia excluye carga y VAD previo. Sin rendimiento móvil ni precisión global.']
    write_text_atomic(folder/'resumen.md','\n'.join(lines)+'\n')
    save(viewer/'data.json',dict(notice=m['notice'],clips=clips,rows=rows))
    ui=ROOT/'herramientas/analisis_intentos'
    for name in ['index.html','app.js','style.css']:
        shutil.copyfile(ui/name,viewer/name)
    save(folder/'integridad.json',dict(manifest_sha256=digest(folder/'manifest.json'),output_sha256=digest(folder/'resultados.json'),
        jobs_verified=len(r['runs']),source_hashes_unchanged=True,input_hashes_verified=True,
        notice='Integridad técnica, no validación humana de calidad.'))
    print(folder/'resumen.md',flush=True)
    print('Visor:',viewer,flush=True)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('mode',choices=['preparar','ejecutar','resumir'])
    parser.add_argument('folder',nargs='?',type=Path)
    args=parser.parse_args()
    if args.mode=='preparar':prepare()
    elif args.folder is None:parser.error('Indica carpeta.')
    elif args.mode=='ejecutar':run(args.folder.resolve())
    else:summarize(args.folder.resolve())


if __name__=='__main__':main()
