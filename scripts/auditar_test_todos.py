"""Audita test sin ASR y compara con dev; originales y referencias permanecen intactos."""
import argparse
from bisect import bisect_left,bisect_right
from collections import Counter
import json
from pathlib import Path

from scripts import evaluar_asr_externo as e
from scripts.revisar_mls_completo import equal,read


def audit(folder,dataset,archive,dev,protocol_file,package_file):
    folder,dataset=Path(folder).resolve(),Path(dataset).resolve()
    out=folder/'revision_completa'
    if out.exists():raise ValueError('Revisión existente; no sobrescribir.')
    root=Path(__file__).resolve().parents[1]
    protocol=read(protocol_file);package=read(package_file)
    equal(e.sha(archive),Path(str(archive)+'.sha256').read_text().split()[0],'SHA256 transferencia')
    cohort=read(folder/'cohorte.json')
    equal(cohort['status'],'completed','estado cohorte');equal(cohort['partition'],'test','partición')
    equal(sorted(j['motor'] for j in cohort['jobs']),sorted(protocol['models']),'doce motores fijados')
    for name,digest in protocol['source_sha256'].items():equal(e.sha(root/name),digest,'fuente delegada '+name)
    reference=e.select_mls(dataset,'test',0,42)['items']
    equal(len(reference),2385,'test oficial completo')
    dev=read(dev)
    dev_rows={r['motor']:r for r in dev['all_models_ranked']}
    equal(set(dev_rows),set(protocol['models']),'dev común')
    originals={p.relative_to(folder).as_posix():e.sha(p) for p in folder.rglob('*') if p.is_file()}
    rows=[];texts={}
    for job in cohort['jobs']:
        key=job['motor'];base=folder/key
        equal(job['status'],'completed',key+' job');equal(job['returncode'],0,key+' retorno')
        m=read(base/'ejecucion.json');config={k:v for k,v in m.items() if k not in ('created_at_utc','run_signature')}
        equal(e.signature(config),m['run_signature'],key+' firma')
        equal(m['selection']['items'],reference,key+' selección oficial')
        equal(m['gpu_physical_index'],job['gpu'],key+' GPU')
        expected=protocol['models'][key]
        for field,value in expected.items():
            if field=='adapter_sha256' and not job.get('reused'):
                value=package['source_sha256']['scripts/motores_test_todos.py']
            equal(m.get(field),value,key+' protocolo '+field)
        equal({p.stem for p in (base/'audios').glob('*.json')},{i['id'] for i in reference},key+' IDs')
        sessions=list((base/'sesiones').glob('*.json'))
        equal(len(sessions),1,key+' sesión única')
        session=read(sessions[0]);resources=session['resources']
        equal(session['status'],'completed',key+' sesión')
        equal(session['pid'],job['pid'],key+' PID');equal(session['run_signature'],m['run_signature'],key+' firma sesión')
        if resources.get('incremental_log_error'):raise ValueError(key+' error de telemetría')
        counts=Counter()
        with sessions[0].with_suffix('.jsonl').open(encoding='utf-8') as stream:
            for line in stream:counts[json.loads(line)['kind']]+=1
        equal(counts['process'],len(resources['samples']),key+' JSONL RAM')
        equal(counts['gpu'],len(resources['gpu_samples']),key+' JSONL GPU')
        times=sorted(s['elapsed_seconds'] for s in resources['gpu_samples'])
        compact=[];examples=[];caps=[];bad_times=[];coverage=0
        for item in reference:
            r=read(base/'audios'/(item['id']+'.json'))
            equal(r['status'],'ok',key+'/'+item['id']);equal(r['run_signature'],m['run_signature'],key+' firma audio')
            for field,value in item.items():equal(r[field],value,key+' identidad '+field)
            calculated=e.score(r['reference'],r['hypothesis'])
            for field,value in calculated.items():equal(r['accuracy'][field],value,key+'/'+item['id']+' '+field)
            compact.append(e.report_record(r))
            coverage+=bisect_right(times,r['monitor_interval_end_seconds'])>bisect_left(times,r['monitor_interval_start_seconds'])
            native=r.get('native_output',{})
            if native.get('generation_cap_reached'):caps.append(item['id'])
            words=[]
            if key=='crisper':words=native.get('native_result',{}).get('words') or []
            elif key=='whisper':words=[w for s in native.get('native_segments',[]) for w in s.get('words') or []]
            elif key=='vosk':words=[w for s in native.get('native_results',[]) for w in s.get('result',[])]
            invalid=sum(not (0<=w.get('start',-1)<=w.get('end',-1)<=item['audio_seconds']+.1) for w in words)
            if invalid:bad_times.append(dict(id=item['id'],invalid_words=invalid))
            examples.append(dict(id=item['id'],reference=r['reference'],hypothesis=r['hypothesis'],
                wer=calculated['wer'],audio_seconds=item['audio_seconds'],
                counts={k:calculated[k] for k in ('substitutions','deletions','insertions')}))
        summary=e.aggregate(compact);saved=read(base/'resumen.json')
        for field,value in summary.items():equal(saved[field],value,key+' resumen '+field)
        equal(next(r['summary'] for r in cohort['results'] if r['motor']==key),saved,key+' resumen coordinador')
        rs=resources['summary'];gpu=rs['gpu']
        row=dict(motor=key,gpu=job['gpu'],reused=bool(job.get('reused')),**summary,
            dev_wer=dev_rows[key]['corpus_wer'],dev_cer=dev_rows[key]['corpus_cer'],
            wer_difference_percentage_points=100*(summary['corpus_wer']-dev_rows[key]['corpus_wer']),
            dev_asr_total_seconds=dev_rows[key]['asr_total_seconds'],
            ram_rss_max_observed_mib=rs['rss_bytes']['maximum']/1048576,
            vram_process_max_observed_mib=gpu['process_vram_mib']['maximum'] if gpu['process_vram_mib'] else None,
            resource_summary=rs,model_import_and_load_seconds=session['model_import_and_load_seconds'],
            warmup_seconds=session['warmup']['wall_seconds'],session_wall_seconds=resources['wall_seconds'],
            process_samples=counts['process'],gpu_samples=counts['gpu'],audios_with_gpu_samples=coverage,
            generation_cap_audio_ids=caps,native_time_out_of_range=bad_times)
        rows.append(row);texts[key]=sorted(examples,key=lambda r:r['wer'],reverse=True)[:10]
        print(key,'verificados',len(compact),'WER',summary['corpus_wer'],'CER',summary['corpus_cer'],flush=True)
    for name,digest in originals.items():equal(e.sha(folder/name),digest,'original intacto '+name)
    rows.sort(key=lambda r:r['corpus_wer'])
    payload=dict(created_at_utc=e.now(),status='audited_no_new_inference',selected=len(reference),
        results_recomputed=len(reference)*len(rows),audio_seconds=sum(i['audio_seconds'] for i in reference),
        checksum_verified=True,archive_sha256=e.sha(archive),same_inputs=True,
        official_local_selection_and_audio_hashes_checked=len(reference),configuration_matches_frozen_dev=True,
        source_files_preserved=originals,motors=rows,top_error_examples=texts,human_audio_review=False,
        reviewer_script_sha256=e.sha(__file__))
    e.save(out/'verificacion.json',payload)
    lines=['# MLS test · comparación de los doce candidatos','',
        f"Auditoría técnica: {len(rows)} motores, {len(reference)} audios ({payload['audio_seconds']/3600:.4f} h) por motor; {payload['results_recomputed']:,} resultados y alineamientos recalculados. Transferencia SHA256 cotejada, selección oficial local completa y huellas verificadas, configuración fijada desde dev, firmas/cobertura/resúmenes/telemetría comprobados. Originales y referencias conservados. Sin nuevas inferencias ni escucha humana independiente.",'',
        '## Precisión: dev frente a test','',
        '| Modelo | WER dev % | WER test % | Diferencia pp | CER test % | Audios exactos % | S / D / I test |',
        '|---|---:|---:|---:|---:|---:|---|']
    for r in rows:
        t=r['totals']
        lines.append(f"| {r['motor']} | {100*r['dev_wer']:.2f} | {100*r['corpus_wer']:.2f} | {r['wer_difference_percentage_points']:+.2f} | {100*r['corpus_cer']:.2f} | {100*r['exact_audio_fraction']:.2f} | {t['substitutions']} / {t['deletions']} / {t['insertions']} |")
    lines+=['','WER: sustituciones + omisiones + inserciones por palabra de referencia. No es porcentaje de audios erróneos ni tasa de acierto; puede superar el 100 %. CER por caracteres, incluidos espacios. Una diferencia negativa significa menos error en test; son conjuntos distintos, no una mejora de pesos o reglas. No se ha realizado contraste estadístico pareado entre modelos.','',
        '## Coste y recursos observados','',
        '| Modelo | ASR min | RTF | RAM RSS máx. MiB | VRAM PID máx. MiB | Carga s | Sesión min | Reutilizado |',
        '|---|---:|---:|---:|---:|---:|---:|---|']
    for r in rows:
        v=r['vram_process_max_observed_mib']
        lines.append(f"| {r['motor']} | {r['asr_total_seconds']/60:.2f} | {r['corpus_asr_rtf']:.4f} | {r['ram_rss_max_observed_mib']:.1f} | {v if v is not None else 'CPU'} | {r['model_import_and_load_seconds']:.2f} | {r['session_wall_seconds']/60:.2f} | {'sí' if r['reused'] else 'no'} |")
    lines+=['',
        'ASR excluye carga, calentamiento, E/S, puntuación y escritura. Sesión incluye más operaciones. Máximos RAM/VRAM muestreados, no picos garantizados. Configuraciones y backends diferentes; GPU dedicadas por tarea propia pero CPU/RAM/disco compartidos y concurrencia variable. Los reutilizados conservarían recursos de su ejecución original. No equivale a una medición aislada, latencia del seguidor, batería o rendimiento de tablet. Telemetría completa (CPU/RAM/E/S/GPU/potencia/energía cuando disponible) en los JSON originales y resource_summary del verificador.','',
        '## Alertas y revisión pendiente','',
        'Las alertas son diagnósticas: ausencia de un indicador no prueba ausencia de truncamiento. Muestras GPU ausentes durante una inferencia rápida no significan GPU inactiva. Marcas temporales con tolerancia de 100 ms al final del archivo.']
    for r in rows:
        other=r['resource_summary']['gpu'].get('other_compute_process_count')
        instrumented=r['motor'] in ('parakeet','moonshine_tiny_es','moonshine_small_es','granite_turboctc','canary_v2','qwen_asr_06b','qwen_asr_17b','whisper_turbo')
        lines.append(f"- {r['motor']}: {len(r['generation_cap_audio_ids'])} indicadores de límite{' (sin indicador equivalente instrumentado)' if not instrumented else ''}; marcas fuera de rango en {len(r['native_time_out_of_range'])} clips; muestras GPU en {r['audios_with_gpu_samples']}/{len(reference)} audios; máximo de otros procesos GPU observado {other['maximum'] if other else 'no disponible/CPU'}.")
    lines+=['',
        'La escucha de referencias problemáticas de dev no valida las de test. WER alto o discrepancias no prueban invención: revisar audio antes de clasificar fallos. Mantener métricas oficiales y anotaciones humanas separadas. Las fuentes de entrenamiento de Moonshine incluyen MLS/FLEURS/CommonVoice: falta auditoría de particiones/IDs antes de afirmar independencia. Este test no acredita literalidad/disfluencias, voz infantil o seguimiento en vivo; se estudiarán en el banco propio. No ajustar configuraciones a partir de test para presentar después este mismo test como evaluación independiente.','',
        '## Casos para escucha compartida','',
        'Cinco mayores WER por motor; selección dirigida a fallos, no estimación de su frecuencia. Diez ejemplos por modelo en verificacion.json y todos los resultados por audio en las carpetas originales.']
    for key,examples in texts.items():
        lines+=['',f'### {key}','']
        for r in examples[:5]:
            lines += [f"**{r['id']} · WER {100*r['wer']:.2f} % · {r['audio_seconds']:.2f} s**",'',
                'Referencia: '+r['reference'],'','ASR: '+r['hypothesis'],'']
    (out/'informe.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    print('Informe:',out/'informe.md',flush=True)
    return payload


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--carpeta',type=Path,required=True);p.add_argument('--dataset',type=Path,required=True)
    p.add_argument('--archivo',type=Path,required=True)
    p.add_argument('--dev',type=Path,default=Path('resultados/asr_externo/mls_dev_nuevos_completo_01/revision_completa/verificacion.json'))
    p.add_argument('--protocolo',type=Path,default=Path('entornos/test_todos/protocolo.json'))
    p.add_argument('--paquete',type=Path,default=Path('entornos/test_todos/verificacion_paquete.json'))
    a=p.parse_args();audit(a.carpeta,a.dataset,a.archivo,a.dev,a.protocolo,a.paquete)
