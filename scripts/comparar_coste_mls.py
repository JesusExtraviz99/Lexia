"""Audita 100 MLS secuenciales y compara exclusivamente sus mismos IDs con el lote concurrente."""
import argparse
from collections import Counter
import json
from pathlib import Path

from scripts import evaluar_asr_externo as e
from scripts.revisar_mls_completo import equal, read


def compare(sequential, parallel, archive, dataset):
    sequential, parallel = Path(sequential).resolve(), Path(parallel).resolve()
    out = sequential/'revision_compartida'
    if out.exists():
        raise ValueError('La revisión ya existe, no se sobrescribe.')
    archive = Path(archive)
    digest = e.sha(archive)
    equal(digest, archive.with_name(archive.name+'.sha256').read_text().split()[0], 'SHA256 servidor')
    source_paths = list(p for p in sequential.rglob('*') if p.is_file())
    cohort, original = read(sequential/'cohorte.json'), read(parallel/'cohorte.json')
    equal(cohort['status'], 'completed', 'estado cohorte')
    equal([j['motor'] for j in cohort['jobs']], ['xlsr','parakeet','whisper','vosk'], 'motores/orden')
    equal(cohort['gpu_indices_authorized'], [0], 'única GPU autorizada')
    # Todos los procesos propios deben finalizar antes del comienzo del siguiente.
    for first, second in zip(cohort['jobs'], cohort['jobs'][1:]):
        if first['finished_at_utc'] > second['started_at_utc']:
            raise ValueError('Solapamiento de motores propios.')
    originals_by_motor = {j['motor']: j for j in original['jobs']}
    rows, selected, pending_hashes = [], None, {}
    # Registrar fuentes usadas antes de crear cualquier archivo derivado.
    for job in cohort['jobs']:
        base = parallel/job['motor']
        source_paths += [base/'ejecucion.json', base/'resumen.json', *list((base/'sesiones').glob('*'))]
        ids = read(sequential/job['motor']/'ejecucion.json')['selection']['items']
        source_paths += [base/'audios'/(r['id']+'.json') for r in ids]
    before = {str(p): e.sha(p) for p in source_paths}
    for job in cohort['jobs']:
        motor = job['motor']
        pair, resources = [], []
        seq_items = read(sequential/motor/'ejecucion.json')['selection']['items']
        if selected is None:
            selected = seq_items
        else:
            equal(seq_items, selected, motor+' selección entre motores')
        equal(len(seq_items), 100, motor+' total')
        equal(job['returncode'], 0, motor+' retorno')
        equal(job['status'], 'completed', motor+' estado')
        equal(job['gpu'], None if motor == 'vosk' else 0, motor+' GPU')
        for folder, items, full in [(sequential, seq_items, False), (parallel, seq_items, True)]:
            base = folder/motor
            manifest = read(base/'ejecucion.json')
            config = {k:v for k,v in manifest.items() if k not in ('created_at_utc','run_signature')}
            equal(e.signature(config), manifest['run_signature'], motor+' firma configuración')
            equal(manifest['selection']['items'][:100], items, motor+' mismos 100 audios')
            if not full:
                equal({p.stem for p in (base/'audios').glob('*.json')}, {r['id'] for r in items}, motor+' cobertura')
                seq_manifest = manifest
            else:
                for key in ['model','normalization','script_sha256','adapter_sha256','versions','parameters',
                            'batch_size','cpu_threads_requested','external_vad','denoise','resample','external_chunking']:
                    equal(manifest[key], seq_manifest[key], motor+' configuración conservada '+key)
            sessions = list((base/'sesiones').glob('*.json'))
            equal(len(sessions), 1, motor+' sesión única')
            session = read(sessions[0]); rs = session['resources']
            equal(session['status'], 'completed', motor+' sesión completa')
            equal(session['pid'], (originals_by_motor[motor] if full else job)['pid'], motor+' PID')
            if rs.get('incremental_log_error'):
                raise ValueError('Error de escritura de muestras')
            counts = Counter()
            with sessions[0].with_suffix('.jsonl').open(encoding='utf-8') as stream:
                for line in stream:
                    counts[json.loads(line)['kind']] += 1
            equal(counts['process'], len(rs['samples']), motor+' JSONL RAM')
            equal(counts['gpu'], len(rs['gpu_samples']), motor+' JSONL GPU')
            records, texts, intervals = [], {}, []
            for item in items:
                result = read(base/'audios'/(item['id']+'.json'))
                equal(result['status'], 'ok', motor+'/'+item['id'])
                equal(result['run_signature'], manifest['run_signature'], motor+' firma resultado')
                for key,value in item.items():
                    equal(result[key], value, motor+' identidad audio '+key)
                calculated = e.score(result['reference'], result['hypothesis'])
                for key,value in calculated.items():
                    equal(result['accuracy'][key], value, motor+' métrica '+key)
                records.append(e.report_record(result))
                texts[item['id']] = dict(hypothesis=result['hypothesis'], accuracy=result['accuracy'], timing=result['timing'])
                intervals.append((result['monitor_interval_start_seconds'],result['monitor_interval_end_seconds']))
                pending_hashes[item['id']] = item
            summary = e.aggregate(records)
            if not full:
                saved = read(base/'resumen.json')
                for key,value in summary.items():
                    equal(saved[key], value, motor+' resumen guardado '+key)
            start, end = min(i[0] for i in intervals), max(i[1] for i in intervals)
            block = e.resource_summary([s for s in rs['samples'] if start <= s['elapsed_seconds'] <= end],
                                       [s for s in rs['gpu_samples'] if start <= s['elapsed_seconds'] <= end])
            resources.append(dict(block_100=block, block_elapsed_seconds=end-start,
                session_wall_seconds=rs['wall_seconds'], model_import_and_load_seconds=session['model_import_and_load_seconds'],
                warmup_seconds=session['warmup']['wall_seconds'], gpu_info=manifest['gpu_info']))
            pair.append(dict(summary=summary, texts=texts))
        seq, par = pair
        changes = []
        for item in seq_items:
            key = item['id']
            a,b = seq['texts'][key],par['texts'][key]
            if a['hypothesis'] != b['hypothesis']:
                changes.append(dict(id=key, reference=item['reference'], sequential=a['hypothesis'], parallel=b['hypothesis'],
                                    normalized_changed=e.normalized(a['hypothesis']) != e.normalized(b['hypothesis'])))
        rows.append(dict(motor=motor, sequential=seq['summary'], parallel_same_100=par['summary'],
                         asr_time_change_percent=100*(seq['summary']['asr_total_seconds']/par['summary']['asr_total_seconds']-1),
                         transcript_changes=changes, sequential_resources=resources[0], parallel_resources_same_100=resources[1]))
        print(motor, 'auditado; cambios de texto', len(changes), 'ASR secuencial/concurrente',
              seq['summary']['asr_total_seconds'],par['summary']['asr_total_seconds'], flush=True)
    for item in pending_hashes.values():
        equal(e.sha(Path(dataset)/item['file']), item['sha256'], 'FLAC local '+item['id'])
    for path,digest_before in before.items():
        equal(e.sha(path), digest_before, 'original intacto '+path)
    payload = dict(created_at_utc=e.now(), status='audited_no_new_inference', archive_sha256=digest,
        checksum_verified=True, selected=100, local_audio_hashes_checked=len(pending_hashes),
        audio_seconds=sum(r['audio_seconds'] for r in selected), sequential_no_own_overlap=True,
        original_files_sha256=before, rows=rows, human_audio_review=False,
        notice='Una pasada por condición, sin inferir causalidad o significación; GPU física y carga ajena pueden diferir.')
    e.save(out/'comparacion.json', payload)
    lines = ['# MLS dev · coste secuencial frente a concurrente', '',
        f"Revisión del 06/11/2026. Cuatro motores, mismos 100 IDs/FLAC/referencias: {payload['audio_seconds']:.2f} s de audio. Crisper excluido. Los 400 resultados nuevos y los 400 originales correspondientes se recalculan desde las transcripciones. SHA256 de descarga, firmas, modelos/parámetros/versiones, cobertura y conteos JSONL verificados; 100 huellas locales cotejadas. Originales conservados. Sin ASR nuevo ni escucha humana independiente.", '',
        '## Reconocimiento: mismos 100 audios', '',
        '| Motor | ASR concurrente s | ASR secuencial s | Cambio % | WER concurrente % | WER secuencial % | Textos distintos (normalizados) |',
        '|---|---:|---:|---:|---:|---:|---:|']
    for r in rows:
        a,b=r['parallel_same_100'],r['sequential']
        lines.append(f"| {r['motor']} | {a['asr_total_seconds']:.2f} | {b['asr_total_seconds']:.2f} | {r['asr_time_change_percent']:+.2f} | {100*a['corpus_wer']:.2f} | {100*b['corpus_wer']:.2f} | {len(r['transcript_changes'])} ({sum(c['normalized_changed'] for c in r['transcript_changes'])}) |")
    lines += ['', 'Un cambio negativo de tiempo indica menor tiempo secuencial. WER es error de palabras: menor es mejor. No se compara el tiempo de 100 audios con el de 2.408 ni con el WER del corpus completo. Las diferencias de texto y sus referencias se conservan en comparacion.json.', '',
        '## Recursos durante el tramo de los 100 audios', '',
        '| Motor | RAM RSS máx. concurrente / secuencial MiB | VRAM PID máx. concurrente / secuencial MiB | Potencia GPU media concurrente / secuencial W |',
        '|---|---:|---:|---:|']
    def metric(block, key, gpu=False, scale=1):
        d=block['gpu'].get(key) if gpu else block.get(key)
        return 'n/d' if not d else f"{d['maximum' if key != 'power_watts' else 'mean']/scale:.1f}"
    for r in rows:
        a=r['parallel_resources_same_100']['block_100']; b=r['sequential_resources']['block_100']
        lines.append(f"| {r['motor']} | {metric(a,'rss_bytes',scale=1048576)} / {metric(b,'rss_bytes',scale=1048576)} | {metric(a,'process_vram_mib',True)} / {metric(b,'process_vram_mib',True)} | {metric(a,'power_watts',True)} / {metric(b,'power_watts',True)} |")
    lines += ['', 'Tramo desde el inicio del primer audio hasta el final del último, con los huecos de puntuación/escritura entre ambos. Excluye carga y calentamiento; los pesos residentes siguen contando. Máximos muestreados, no picos garantizados. Potencia media aritmética de muestras de la GPU física, no consumo exclusivo o neto del ASR; Vosk no usa GPU.', '',
        '## Inicialización y sesión secuencial', '',
        '| Motor | Carga/importación s | Calentamiento s | Sesión instrumentada s | RTF ASR |',
        '|---|---:|---:|---:|---:|']
    for r in rows:
        s=r['sequential_resources']
        lines.append(f"| {r['motor']} | {s['model_import_and_load_seconds']:.2f} | {s['warmup_seconds']:.2f} | {s['session_wall_seconds']:.2f} | {r['sequential']['corpus_asr_rtf']:.4f} |")
    lines += ['', '## Interpretación', '',
        '- La secuencia temporal confirma que no se solapan nuestros cuatro procesos. El servidor continúa compartido: otros usuarios pueden usar CPU/RAM/disco. La etiqueta aislada describe esta cohorte, no exclusividad del servidor.',
        '- Una sola pasada por condición. No atribuir todas las diferencias a eliminar concurrencia: cambian fecha, cachés, estado del sistema y GPU física (Parakeet pasa de 1 a 0; Whisper de 2 a 0). Revisar GPU/hardware y muestras, sin prometer significación estadística.',
        '- La calidad no debería asumirse idéntica: comprobar textos distintos. Decodificación numérica y empates pueden variar; no se establece una causa de cambios sin pruebas adicionales.',
        '- Los tiempos de carga/calentamiento y escritura son distintos de ASR. Estos costes siguen guardados; diferencias en la duración de sesión no son necesariamente mejoras del reconocedor.',
        '- Esta prueba mide reconocimiento offline, no el seguidor, latencia visual o rendimiento de tablet. Test permanece reservado.', '',
        '## Cambios de transcripción', '']
    for r in rows:
        lines += [f"### {r['motor']}", '']
        if not r['transcript_changes']:
            lines += ['Ningún texto distinto.', '']
        for c in r['transcript_changes']:
            lines += [f"**{c['id']}**", '', 'Referencia: '+c['reference'], '',
                      'Concurrente: '+c['parallel'], '', 'Secuencial: '+c['sequential'], '']
    (out/'informe.md').write_text('\n'.join(lines)+'\n', encoding='utf-8')
    print('Informe:',out/'informe.md', flush=True)


if __name__ == '__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--secuencial',type=Path,required=True)
    p.add_argument('--paralela',type=Path,required=True)
    p.add_argument('--archivo',type=Path,required=True)
    p.add_argument('--dataset',type=Path,required=True)
    a=p.parse_args()
    compare(a.secuencial,a.paralela,a.archivo,a.dataset)
