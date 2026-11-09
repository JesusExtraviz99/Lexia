"""Auditoría de los siete ASR nuevos y tabla conjunta con el dev previamente auditado."""
import argparse
from collections import Counter
import json
from pathlib import Path
from scripts import evaluar_asr_externo as e
from scripts.revisar_mls_completo import equal, read
from scripts.ampliacion_motores import KEYS


def audit(folder, baseline, dataset, archive):
    folder,baseline=Path(folder).resolve(),Path(baseline).resolve()
    out=folder/'revision_completa'
    if out.exists():raise ValueError('Revisión existente, no sobrescribir.')
    digest=e.sha(archive)
    equal(digest,Path(str(archive)+'.sha256').read_text().split()[0],'SHA256 transferencia')
    cohort=read(folder/'cohorte.json')
    equal(cohort['status'],'completed','cohorte')
    equal(sorted(j['motor'] for j in cohort['jobs']),sorted(KEYS),'siete motores')
    old=read(baseline/'revision_completa/verificacion.json')
    reference=read(baseline/'xlsr/ejecucion.json')['selection']['items']
    equal(len(reference),2408,'cobertura dev')
    for motor in old['motors']:
        for name in ['ejecucion.json','resumen.json']:
            relative=motor['motor']+'/'+name
            equal(e.sha(baseline/relative),old['source_files_preserved'][relative],'fuente de auditoría anterior '+relative)
    hashes={p.relative_to(folder).as_posix():e.sha(p) for p in folder.rglob('*') if p.is_file()}
    rows=[];texts={};all_caps={}
    for job in cohort['jobs']:
        key=job['motor'];base=folder/key
        equal(job['returncode'],0,key+' retorno')
        equal(job['status'],'completed',key+' estado')
        m=read(base/'ejecucion.json')
        config={k:v for k,v in m.items() if k not in ('created_at_utc','run_signature')}
        equal(e.signature(config),m['run_signature'],key+' firma')
        equal(m['selection']['items'],reference,key+' selección exacta')
        equal(m['gpu_physical_index'],job['gpu'],key+' GPU')
        equal({p.stem for p in (base/'audios').glob('*.json')},{i['id'] for i in reference},key+' cobertura')
        sessions=list((base/'sesiones').glob('*.json'));equal(len(sessions),1,key+' sesión única')
        session=read(sessions[0]);resources=session['resources']
        equal(session['status'],'completed',key+' sesión completa')
        equal(session['pid'],job['pid'],key+' PID')
        equal(session['run_signature'],m['run_signature'],key+' firma sesión')
        if resources.get('incremental_log_error'):raise ValueError(key+' error de telemetría')
        counts=Counter()
        with sessions[0].with_suffix('.jsonl').open(encoding='utf-8') as stream:
            for line in stream:counts[json.loads(line)['kind']]+=1
        equal(counts['process'],len(resources['samples']),key+' JSONL RAM')
        equal(counts['gpu'],len(resources['gpu_samples']),key+' JSONL GPU')
        compact=[];examples=[];caps=[]
        for item in reference:
            result=read(base/'audios'/(item['id']+'.json'))
            equal(result['status'],'ok',key+'/'+item['id'])
            equal(result['run_signature'],m['run_signature'],key+' firma audio')
            for k,v in item.items():equal(result[k],v,key+' identidad '+k)
            calculated=e.score(result['reference'],result['hypothesis'])
            for k,v in calculated.items():equal(result['accuracy'][k],v,key+'/'+item['id']+' '+k)
            compact.append(e.report_record(result))
            if result.get('native_output',{}).get('generation_cap_reached'):
                caps.append(dict(id=item['id'],token_count=len(result.get('token_ids',[])),
                                 last_token=(result.get('token_ids') or [None])[-1],wer=calculated['wer']))
            examples.append(dict(id=item['id'],reference=result['reference'],hypothesis=result['hypothesis'],wer=calculated['wer']))
        summary=e.aggregate(compact);saved=read(base/'resumen.json')
        for k,v in summary.items():equal(saved[k],v,key+' resumen '+k)
        gpu=resources['summary']['gpu']
        rows.append(dict(motor=key,group='nuevos',gpu=job['gpu'],**summary,
            ram_rss_max_observed_mib=resources['summary']['rss_bytes']['maximum']/1048576,
            vram_process_max_observed_mib=(gpu['process_vram_mib']['maximum'] if gpu['process_vram_mib'] else None),
            resource_summary=resources['summary'],model_import_and_load_seconds=session['model_import_and_load_seconds'],
            warmup_seconds=session['warmup']['wall_seconds'],session_wall_seconds=resources['wall_seconds'],
            parameter_count=session.get('parameter_count'),generation_cap_indicators=caps,
            source_matches_local=m['script_sha256']==e.sha(e.__file__),
            adapter_matches_local=m['adapter_sha256']==e.sha(Path(__file__).parent/'ampliacion_motores.py')))
        texts[key]=sorted(examples,key=lambda r:r['wer'],reverse=True)[:10]
        all_caps[key]=caps
        print(key,'auditado',len(compact),'WER',summary['corpus_wer'],'indicadores límite',len(caps),flush=True)
    for item in reference:equal(e.sha(Path(dataset)/item['file']),item['sha256'],'FLAC local '+item['id'])
    for name,digest_before in hashes.items():equal(e.sha(folder/name),digest_before,'original intacto '+name)
    old_rows=[dict(motor=r['motor'],group='anteriores',gpu=r['gpu'],corpus_wer=r['corpus_wer'],corpus_cer=r['corpus_cer'],
                   asr_total_seconds=r['asr_total_seconds'],corpus_asr_rtf=r['corpus_asr_rtf'],
                   ram_rss_max_observed_mib=r['ram_rss_max_observed_mib'],
                   vram_process_max_observed_mib=r['vram_process_max_observed_mib']) for r in old['motors']]
    all_rows=sorted(rows+old_rows,key=lambda r:r['corpus_wer'])
    payload=dict(created_at_utc=e.now(),status='audited_no_new_inference',new_records=2408*7,
        selected=2408,audio_seconds=sum(i['audio_seconds'] for i in reference),reference_words=rows[0]['totals']['reference_words'],
        checksum_verified=True,archive_sha256=e.sha(archive),same_inputs_as_previous=True,local_audio_hashes_checked=2408,
        source_files_preserved=hashes,new_models=rows,all_models_ranked=all_rows,top_error_examples=texts,
        previous_audit='mls_dev_completo_paralela_01/revision_completa/verificacion.json',
        previous_summary_manifest_hashes_rechecked=True,human_audio_review=False)
    e.save(out/'verificacion.json',payload)
    lines=['# MLS dev · comparación de todos los candidatos','',
        'Siete nuevos modelos: 16.856 resultados recalculados, 2.408 audios y unas diez horas por motor. Descarga, firmas, cobertura, referencias/huellas, resúmenes y conteos de telemetría verificados. Mismos 2.408 FLAC cotejados localmente. Los cinco resultados anteriores proceden de su auditoría previa; sus manifiestos y resúmenes siguen intactos. Sin inferencias nuevas o escucha independiente.', '',
        '| Modelo | WER % | CER % | ASR acumulado min | RTF | RAM RSS máx. MiB | VRAM PID máx. MiB |',
        '|---|---:|---:|---:|---:|---:|---:|']
    for r in all_rows:
        lines.append(f"| {r['motor']} | {100*r['corpus_wer']:.2f} | {100*r['corpus_cer']:.2f} | {r['asr_total_seconds']/60:.2f} | {r['corpus_asr_rtf']:.4f} | {r['ram_rss_max_observed_mib']:.1f} | {r['vram_process_max_observed_mib'] if r['vram_process_max_observed_mib'] is not None else 'CPU'} |")
    lines+=['','## Lectura de los resultados','',
        '- Menor WER/CER significa menor error frente a las referencias oficiales; no acredita seguimiento en directo, literalidad ni voz infantil.',
        '- Coste ASR con modelo cargado/calentado; excluye carga, lectura y escritura. RAM/VRAM son máximos observados de sesión, no picos garantizados. Ejecuciones concurrentes en fechas/asignaciones diferentes: no atribuir todas las diferencias de tiempo a la arquitectura.',
        '- Se conserva la precisión float32; Whisper Turbo utiliza Transformers, frente a CT2 en Whisper Small, y los nuevos no generan marcas de palabra. Esas diferencias forman parte de cada configuración.',
        '- Moonshine declara fuentes MLS/FLEURS/CommonVoice en entrenamiento. Auditar particiones/IDs antes de afirmar independencia del test o generalización; conocer el corpus de origen no prueba solapamiento de test.',
        '- La revisión humana anterior confirmó referencias incompletas/diferentes en cuatro casos seleccionados: discrepancia frente al texto no equivale siempre a invención. No se han corregido referencias ni eliminado clips.',
        '- No se descartan modelos solo por WER: para el seguidor interesan posición, demora, estabilidad y recuperación en directo, además de coste y viabilidad local.', '',
        '## Indicadores de límite de generación', '',
        'Son alertas del adaptador, no diagnóstico automático de truncamiento. Los tokens de inicio/fin y la regla de longitud requieren revisar cada caso; conservar las salidas y el protocolo antes de interpretar o modificar límites.', '']
    for r in rows:lines.append(f"- {r['motor']}: {len(r['generation_cap_indicators'])} alertas.")
    lines+=['','## Casos de mayor error para revisión','']
    for key,examples in texts.items():
        lines += [f'### {key}','']
        for r in examples[:5]:
            lines += [f"**{r['id']} · WER {100*r['wer']:.2f} %**",'', 'Referencia: '+r['reference'],'','ASR: '+r['hypothesis'],'']
    (out/'informe.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    print('Informe:',out/'informe.md',flush=True)


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--carpeta',type=Path,required=True);p.add_argument('--anteriores',type=Path,required=True)
    p.add_argument('--dataset',type=Path,required=True);p.add_argument('--archivo',type=Path,required=True)
    a=p.parse_args();audit(a.carpeta,a.anteriores,a.dataset,a.archivo)
