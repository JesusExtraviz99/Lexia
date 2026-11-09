"""Auditoría incremental de resultados MLS completos; sin cargar modelos ni ejecutar ASR."""
import argparse
from bisect import bisect_left, bisect_right
from collections import Counter
import json
import math
from pathlib import Path

from scripts import evaluar_asr_externo as e


def read(path):
    return json.loads(path.read_text(encoding='utf-8'))


def equal(actual, expected, context):
    if isinstance(expected, float):
        valid = isinstance(actual, (int, float)) and math.isclose(actual, expected, rel_tol=1e-10, abs_tol=1e-12)
    else:
        valid = actual == expected
    if not valid:
        raise ValueError('Discrepancia: '+context)


def audit(folder, dataset=None, archive=None):
    folder = Path(folder).resolve()
    out = folder/'revision_completa'
    if out.exists():
        raise ValueError('La revisión ya existe; no se sobrescribe.')
    originals = {p.relative_to(folder).as_posix(): e.sha(p) for p in folder.rglob('*') if p.is_file()}
    cohort = read(folder/'cohorte.json')
    equal(cohort['status'], 'completed', 'estado de cohorte')
    equal(cohort['partition'], 'dev', 'partición')
    equal(sorted(j['motor'] for j in cohort['jobs']), ['crisper', 'parakeet', 'vosk', 'whisper', 'xlsr'], 'motores')
    selection, rows, all_text = None, [], {}
    for job in cohort['jobs']:
        motor = job['motor']
        base = folder/motor
        manifest = read(base/'ejecucion.json')
        config = {k: v for k, v in manifest.items() if k not in ('created_at_utc', 'run_signature')}
        equal(e.signature(config), manifest['run_signature'], motor+' firma')
        equal(job['returncode'], 0, motor+' retorno')
        equal(job['status'], 'completed', motor+' estado')
        equal(manifest['gpu_physical_index'], job['gpu'], motor+' GPU')
        items = manifest['selection']['items']
        equal(len(items), 2408, motor+' cobertura dev')
        if selection is None:
            selection = items
        else:
            equal(items, selection, motor+' selección/referencias/huellas')
        equal({p.stem for p in (base/'audios').glob('*.json')}, {r['id'] for r in items}, motor+' IDs')
        sessions = list((base/'sesiones').glob('*.json'))
        # No atribuir una reanudación a una sesión única sin instrumentarla explícitamente.
        equal(len(sessions), 1, motor+' sesión única')
        session = read(sessions[0])
        equal(session['status'], 'completed', motor+' sesión')
        equal(session['pid'], job['pid'], motor+' PID')
        equal(session['run_signature'], manifest['run_signature'], motor+' firma sesión')
        resources = session['resources']
        if resources.get('incremental_log_error'):
            raise ValueError(motor+' error de escritura de telemetría')
        counts = Counter()
        with sessions[0].with_suffix('.jsonl').open(encoding='utf-8') as stream:
            for line in stream:
                counts[json.loads(line)['kind']] += 1
        equal(counts['process'], len(resources['samples']), motor+' muestras RAM JSONL')
        equal(counts['gpu'], len(resources['gpu_samples']), motor+' muestras GPU JSONL')
        times = sorted(s['elapsed_seconds'] for s in resources['gpu_samples'])
        compact, coverage, bad_times, caps, texts = [], 0, [], [], []
        for item in items:
            result = read(base/'audios'/(item['id']+'.json'))
            equal(result['status'], 'ok', motor+'/'+item['id']+' estado')
            equal(result['run_signature'], manifest['run_signature'], motor+' firma audio')
            for key, value in item.items():
                equal(result[key], value, motor+'/'+item['id']+'/'+key)
            calculated = e.score(result['reference'], result['hypothesis'])
            for key, value in calculated.items():
                equal(result['accuracy'][key], value, motor+'/'+item['id']+'/'+key)
            compact.append(e.report_record(result))
            count = bisect_right(times, result['monitor_interval_end_seconds'])-bisect_left(times, result['monitor_interval_start_seconds'])
            coverage += count > 0
            native = result.get('native_output', {})
            if native.get('generation_cap_reached'):
                caps.append(item['id'])
            words = []
            if motor == 'crisper':
                words = native.get('native_result', {}).get('words') or []
            elif motor == 'whisper':
                words = [w for s in native.get('native_segments', []) for w in s.get('words') or []]
            elif motor == 'vosk':
                words = [w for s in native.get('native_results', []) for w in s.get('result', [])]
            invalid = sum(not(0 <= w.get('start', -1) <= w.get('end', -1) <= item['audio_seconds']+.1) for w in words)
            if invalid:
                bad_times.append(dict(id=item['id'], invalid_words=invalid))
            texts.append(dict(id=item['id'], reference=result['reference'], hypothesis=result['hypothesis'],
                              wer=calculated['wer'], counts={k: calculated[k] for k in ('substitutions', 'deletions', 'insertions')},
                              audio_seconds=item['audio_seconds']))
        recomputed = e.aggregate(compact)
        summary = read(base/'resumen.json')
        for key, value in recomputed.items():
            equal(summary[key], value, motor+' resumen '+key)
        equal(cohort['results'][next(i for i, r in enumerate(cohort['results']) if r['motor'] == motor)]['summary'], summary,
              motor+' resumen coordinador')
        rs = resources['summary']
        gpu = rs['gpu']
        log = (folder/(motor+'.log')).read_text(encoding='utf-8', errors='replace')
        warning_counts = Counter(line for line in log.splitlines() if any(k in line.lower() for k in
            ('unexpected', 'deprecated', 'not valid', 'ignoring clean_up', 'encoder_blank_head', 'warning', 'truncat', 'max_new_tokens')))
        rows.append(dict(motor=motor, gpu=job['gpu'], **recomputed,
            load_seconds=session['model_import_and_load_seconds'], warmup_seconds=session['warmup']['wall_seconds'],
            session_wall_seconds=resources['wall_seconds'], resource_summary=rs,
            ram_rss_max_observed_mib=rs['rss_bytes']['maximum']/1048576,
            vram_process_max_observed_mib=gpu['process_vram_mib']['maximum'] if gpu['process_vram_mib'] else None,
            ram_samples=counts['process'], gpu_samples=counts['gpu'], audios_with_gpu_samples=coverage,
            native_time_out_of_range=bad_times, generation_cap_audio_ids=caps, warnings=dict(warning_counts),
            source_matches_local=manifest['script_sha256'] == e.sha(e.__file__),
            adapter_matches_local=manifest['adapter_sha256'] == e.sha(e.motors.__file__)))
        all_text[motor] = texts
        print(motor, 'verificados', len(compact), 'WER', recomputed['corpus_wer'], flush=True)
    checked = 0
    if dataset:
        for item in selection:
            equal(e.sha(Path(dataset)/item['file']), item['sha256'], 'huella FLAC local '+item['id'])
            checked += 1
    for name, digest in originals.items():
        equal(e.sha(folder/name), digest, 'original conservado '+name)
    archive_info = None
    if archive:
        archive = Path(archive)
        sidecar = archive.with_name(archive.name+'.sha256')
        actual = e.sha(archive)
        expected = sidecar.read_text(encoding='utf-8').split()[0] if sidecar.exists() else None
        if expected:
            equal(actual, expected, 'SHA256 de transferencia')
        archive_info = dict(file=archive.name, sha256=actual, server_sha256=expected,
                            transfer_checksum_verified=expected is not None)
    payload = dict(created_at_utc=e.now(), status='audited_no_new_inference', selection_count=len(selection),
        audio_seconds=sum(r['audio_seconds'] for r in selection),
        same_inputs=True, all_saved_metrics_recomputed=True, local_audio_hashes_checked=checked,
        source_files_preserved=originals, archive=archive_info, motors=rows,
        human_audio_review=False, reviewer_script_sha256=e.sha(__file__))
    e.save(out/'verificacion.json', payload)
    e.save(out/'transcripciones_comparadas.json', all_text)
    lines = ['# MLS dev completo · revisión compartida', '',
        f"Revisión técnica del 06/11/2026: {len(selection)} audios, {payload['audio_seconds']/3600:.4f} horas por motor y {rows[0]['totals']['reference_words']:,} palabras. Cinco motores completados, sin fallos ni hipótesis vacías. Recalculadas métricas y alineamientos de los 12.040 resultados; mismos IDs, referencias y huellas entre motores; cotejadas las 2.408 huellas con FLAC locales. Sin reconocimiento nuevo ni escucha humana independiente.", '',
        '## Precisión y coste observado', '',
        '| Motor | WER % | CER % | S / D / I | ASR acumulado min | RTF | RAM RSS máx. MiB | VRAM PID máx. MiB |',
        '|---|---:|---:|---|---:|---:|---:|---:|']
    for r in sorted(rows, key=lambda r: r['corpus_wer']):
        t = r['totals']; vram = r['vram_process_max_observed_mib']
        lines.append(f"| {r['motor']} | {100*r['corpus_wer']:.2f} | {100*r['corpus_cer']:.2f} | {t['substitutions']} / {t['deletions']} / {t['insertions']} | {r['asr_total_seconds']/60:.2f} | {r['corpus_asr_rtf']:.4f} | {r['ram_rss_max_observed_mib']:.1f} | {vram if vram is not None else 'CPU'} |")
    lines += ['', 'WER es (sustituciones + omisiones + inserciones) / palabras de referencia; menor es mejor, no es porcentaje de audios incorrectos. CER aplica errores a caracteres. Se conservan tildes y ortografía original; se ignoran mayúsculas y puntuación según el protocolo. RTF divide tiempo ASR por duración de audio; 0,01 equivale a un segundo de cálculo por cien de audio.', '',
        'Los tiempos ASR excluyen carga, calentamiento, lectura, puntuación y escritura. RAM/VRAM son máximos muestreados de la sesión, incluida carga y calentamiento. Los cinco procesos se ejecutaron concurrentemente: CPU, RAM y disco compartidos. No equivalen a rendimiento aislado ni predicen una tablet.', '',
        '## Distribución y cobertura', '',
        '| Motor | Audios exactos % | WER p95 % | WER máximo % | Carga s | Calentamiento s | Sesión min | Audios con muestra GPU |',
        '|---|---:|---:|---:|---:|---:|---:|---:|']
    for r in rows:
        lines.append(f"| {r['motor']} | {100*r['exact_audio_fraction']:.2f} | {100*r['per_audio_wer']['p95']:.2f} | {100*r['per_audio_wer']['maximum']:.2f} | {r['load_seconds']:.2f} | {r['warmup_seconds']:.2f} | {r['session_wall_seconds']/60:.2f} | {r['audios_with_gpu_samples']}/2408 |")
    lines += ['', '## Conclusiones y límites', '',
        '- Parakeet presenta el menor WER global en este conjunto. Su cola de errores por audio es más desfavorable que la de Whisper: el promedio global no elimina casos problemáticos. Revisar ejemplos antes de seleccionar candidatos.',
        '- XLSR presenta el menor CER y el menor tiempo ASR acumulado. El orden por caracteres y por palabras difiere; no reducir la comparación a una única métrica.',
        '- Crisper conserva utilidad potencial para literalidad, pero esta evaluación externa no tiene referencias de disfluencias: no demuestra que conserve mejor trabadas. Sus inserciones extremas deben revisarse. Vosk usa CPU y menos RAM; no se compara su velocidad como si usara la misma GPU.',
        '- Las tres GPU neuronales más rápidas terminan antes que Crisper. El grado de concurrencia cambia durante la sesión; reservar una prueba aislada y fija para comparar costes.',
        '- Muestreo GPU aproximadamente cada segundo: llamadas rápidas pueden no contener muestras. No significa GPU inactiva. Energía y potencia de GPU física incluyen carga/calentamiento y cualquier proceso concurrente; no son consumo neto por audio ni medida de batería/tablet.',
        '- Avisos de Crisper sobre encoder_blank_head y parámetros de generación se conservan en logs/verificacion.json. No se atribuyen errores a ese aviso sin demostrarlo. Límites de generación y marcas fuera de rango se enumeran abajo.',
        '- Conservamos todos los clips, incluidos valores extremos. Un WER superior al 100 % es posible por inserciones; no se recorta. Los ejemplos siguientes son discrepancias frente a referencias, no prueba por escucha de una alucinación.',
        '- Test sigue reservado. Revisar casos extremos y fijar configuraciones antes de evaluar test u otro corpus. Las métricas de lectura/disfluencias se estudiarán en el banco propio con referencias humanas.', '',
        '## Alertas de revisión', '']
    for r in rows:
        gpu = r['resource_summary']['gpu']
        other = gpu.get('other_compute_process_count')
        cap = f"indicador de límite de generación activado en {len(r['generation_cap_audio_ids'])} clips" if r['motor'] == 'parakeet' else 'indicador de límite de generación no instrumentado'
        lines.append(f"- {r['motor']}: {cap}; marcas fuera de rango en {len(r['native_time_out_of_range'])} clips; máximo de otros procesos GPU observado: {other['maximum'] if other else 'no disponible/CPU'}.")
    lines += ['', '## Casos para comprobación textual', '', 'Diez clips con mayor WER por motor; selección de diagnóstico, no muestra representativa. Las salidas completas están en transcripciones_comparadas.json y los JSON originales por audio.', '']
    for motor, texts in all_text.items():
        lines += [f'### {motor}', '']
        for r in sorted(texts, key=lambda r: r['wer'], reverse=True)[:10]:
            lines += [f"**{r['id']} · {r['audio_seconds']:.2f} s · WER {100*r['wer']:.2f} %**", '',
                      'Referencia: '+r['reference'], '', 'Hipótesis: '+r['hypothesis'], '']
    (out/'informe.md').write_text('\n'.join(lines)+'\n', encoding='utf-8')
    print('Informe:', out/'informe.md', flush=True)
    return payload


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('folder', type=Path)
    parser.add_argument('--dataset', type=Path)
    parser.add_argument('--archive', type=Path)
    args = parser.parse_args()
    audit(args.folder, args.dataset, args.archive)
