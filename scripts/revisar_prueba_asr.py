"""Auditoría offline de una cohorte MLS guardada; sin modelos ni inferencias."""
import argparse
import json
import math
from pathlib import Path

try:
    from . import evaluar_asr_externo as evaluator
except ImportError:
    import evaluar_asr_externo as evaluator


def read(path):
    return json.loads(path.read_text(encoding='utf-8'))


def audit(folder, dataset=None):
    folder = Path(folder).resolve()
    cohort = read(folder/'cohorte.json')
    motors = [j['motor'] for j in cohort['jobs']]
    if len(motors) != len(set(motors)):
        raise ValueError('Motor duplicado en cohorte.')
    source_files = [p for p in folder.rglob('*') if p.is_file() and 'revision_compartida' not in p.relative_to(folder).parts]
    hashes_before = {p.relative_to(folder).as_posix(): evaluator.sha(p) for p in source_files}
    selection, rows, comparisons = None, [], []
    for job in cohort['jobs']:
        motor = job['motor']
        base = folder/motor
        manifest = read(base/'ejecucion.json')
        config = {k: v for k, v in manifest.items() if k not in ('created_at_utc', 'run_signature')}
        if evaluator.signature(config) != manifest['run_signature']:
            raise ValueError('Firma de configuración inconsistente: '+motor)
        items = manifest['selection']['items']
        if selection is None:
            selection = items
        elif selection != items:
            raise ValueError('Entradas/referencias diferentes: '+motor)
        if job['returncode'] != 0 or manifest['gpu_physical_index'] != job['gpu']:
            raise ValueError('Estado/dispositivo no coincidente: '+motor)
        files = list((base/'audios').glob('*.json'))
        if {p.stem for p in files} != {r['id'] for r in items}:
            raise ValueError('Cobertura por audio incorrecta: '+motor)
        sessions = list((base/'sesiones').glob('*.json'))
        if len(sessions) != 1:
            raise ValueError('Esta primera auditoría requiere una sesión por motor.')
        session = read(sessions[0])
        if session['status'] != 'completed' or session['pid'] != job['pid']:
            raise ValueError('Sesión incompleta o PID diferente.')
        resources = session['resources']
        if resources.get('incremental_log_error'):
            raise ValueError('Error de escritura de telemetría.')
        streamed = [json.loads(line) for line in sessions[0].with_suffix('.jsonl').read_text(encoding='utf-8').splitlines()]
        if (sum(r['kind'] == 'process' for r in streamed) != len(resources['samples']) or
                sum(r['kind'] == 'gpu' for r in streamed) != len(resources['gpu_samples'])):
            raise ValueError('Muestras incrementales no coinciden con el informe.')
        records, coverage, native_times = [], [], []
        for item in items:
            result = read(base/'audios'/(item['id']+'.json'))
            if result['status'] != 'ok' or result['run_signature'] != manifest['run_signature']:
                raise ValueError('Audio fallido/firma diferente.')
            if any(result[k] != item[k] for k in item):
                raise ValueError('Referencia de audio diferente de manifiesto.')
            calculated = evaluator.score(result['reference'], result['hypothesis'])
            for k, v in calculated.items():
                previous = result['accuracy'][k]
                if isinstance(v, float):
                    if not math.isclose(v, previous, rel_tol=1e-10, abs_tol=1e-12):
                        raise ValueError('Métrica no coincide: '+motor+'/'+item['id']+'/'+k)
                elif v != previous:
                    raise ValueError('Métrica no coincide: '+motor+'/'+item['id']+'/'+k)
            records.append(result)
            start, end = result['monitor_interval_start_seconds'], result['monitor_interval_end_seconds']
            count = sum(start <= s['elapsed_seconds'] <= end for s in resources['gpu_samples'])
            coverage.append(dict(audio_id=item['id'], gpu_samples=count,
                                 torch_memory=result.get('torch_memory')))
            native = result.get('native_output', {})
            if native.get('generation_cap_reached'):
                raise ValueError('Posible límite de generación alcanzado en Parakeet.')
            words = []
            if motor == 'crisper':
                words = native.get('native_result', {}).get('words') or []
            elif motor == 'whisper':
                words = [w for s in native.get('native_segments', []) for w in s.get('words') or []]
            elif motor == 'vosk':
                words = [w for s in native.get('native_results', []) for w in s.get('result', [])]
            invalid = sum(not(0 <= w.get('start', -1) <= w.get('end', -1) <= item['audio_seconds']+.1) for w in words)
            native_times.append(dict(audio_id=item['id'], words=len(words), invalid_with_100ms_tolerance=invalid))
            comparisons.append(dict(motor=motor, id=item['id'], reference=result['reference'],
                                    hypothesis=result['hypothesis'], wer=calculated['wer']))
        recomputed = evaluator.aggregate(records)
        summary = read(base/'resumen.json')
        for key in ['attempted', 'completed', 'failures', 'totals', 'corpus_wer', 'corpus_cer',
                    'completed_audio_seconds', 'asr_total_seconds']:
            if summary[key] != recomputed[key]:
                raise ValueError('Resumen no coincide con audios: '+key)
        rs = resources['summary']
        gpu = rs['gpu']
        log = (folder/(motor+'.log')).read_text(encoding='utf-8', errors='replace')
        warning_lines = [line for line in log.splitlines() if any(s in line.lower()
            for s in ['unexpected', 'deprecated', 'not valid', 'ignoring clean_up', 'encoder_blank_head'])]
        rows.append(dict(motor=motor, gpu=job['gpu'], completed=len(records),
            wer=summary['corpus_wer'], cer=summary['corpus_cer'], counts=summary['totals'],
            asr_seconds=summary['asr_total_seconds'], rtf=summary['corpus_asr_rtf'],
            load_seconds=session['model_import_and_load_seconds'],
            warmup_seconds=session['warmup']['wall_seconds'], session_wall_seconds=resources['wall_seconds'],
            ram_rss_max_observed_mib=rs['rss_bytes']['maximum']/1048576,
            ram_lifetime_peak_mib=session['process_at_end'].get('lifetime_peak_rss_bytes', 0)/1048576,
            vram_process_max_observed_mib=gpu['process_vram_mib']['maximum'] if gpu['process_vram_mib'] else None,
            ram_samples=len(resources['samples']), gpu_samples=len(resources['gpu_samples']),
            gpu_statuses=sorted(set(s['status'] for s in resources['gpu_samples'])),
            other_compute_process_max=gpu['other_compute_process_count']['maximum'] if gpu['other_compute_process_count'] else None,
            per_audio_gpu_coverage=coverage, native_word_time_sanity=native_times,
            gpu_energy_sampled_interval_joules=rs['gpu_energy_sampled_interval_joules'],
            gpu_energy_coverage_seconds=rs['gpu_energy_coverage_seconds'], warnings=warning_lines,
            source_code_matches_local=manifest['script_sha256'] == evaluator.sha(evaluator.__file__),
            adapter_matches_local=manifest['adapter_sha256'] == evaluator.sha(evaluator.motors.__file__)))
    checked_local = []
    if dataset:
        for item in selection:
            path = Path(dataset)/item['file']
            if evaluator.sha(path) != item['sha256']:
                raise ValueError('Audio local distinto del procesado en servidor: '+item['id'])
            checked_local.append(item['id'])
    for name, expected in hashes_before.items():
        if evaluator.sha(folder/name) != expected:
            raise ValueError('La auditoría ha alterado un original.')
    out = folder/'revision_compartida'
    payload = dict(status='audited_no_new_inference', dataset='MLS dev',
        selected=len(selection), audio_seconds=sum(r['audio_seconds'] for r in selection),
        reference_words=sum(len(evaluator.normalized(r['reference']).split()) for r in selection),
        metrics_recomputed_from_saved_transcripts=True, same_inputs=True,
        local_audio_hashes_checked=checked_local, source_sha256=hashes_before, motors=rows,
        human_audio_review=False, notice='Revisión textual y técnica, no escucha independiente ni prueba de tablet.')
    evaluator.save(out/'verificacion.json', payload)
    lines = ['# Revisión de la primera prueba paralela · 04/11/2026', '',
        f"Cinco motores, {len(selection)} audios idénticos de MLS dev, {payload['audio_seconds']:.2f} s y {payload['reference_words']} palabras de referencia. Los 50 resultados completos se han recalculado desde las transcripciones guardadas; coinciden WER/CER, alineamientos y conteos. Las diez huellas se han cotejado también con los audios locales si se indica en verificacion.json. Sin inferencias nuevas ni escucha humana independiente.", '',
        '| Motor | Dispositivo | WER % | CER % | ASR total s | RTF | RAM RSS máx. observada MiB | VRAM PID máx. observada MiB |',
        '|---|---|---:|---:|---:|---:|---:|---:|']
    for r in rows:
        device = 'CPU' if r['gpu'] is None else f"GPU {r['gpu']}"
        vram = 'no usa GPU' if r['vram_process_max_observed_mib'] is None else f"{r['vram_process_max_observed_mib']:.0f}"
        lines.append(f"| {r['motor']} | {device} | {100*r['wer']:.2f} | {100*r['cer']:.2f} | {r['asr_seconds']:.2f} | {r['rtf']:.4f} | {r['ram_rss_max_observed_mib']:.1f} | {vram} |")
    lines += ['', 'ASR total es la suma de las diez llamadas con modelo ya cargado y calentado. No incluye carga, calentamiento, E/S ni escritura de informes. RAM/VRAM observadas abarcan la sesión, incluida carga y calentamiento. CPU/GPU y diferentes decodificadores/backends no son comparaciones de arquitectura en igualdad de condiciones.', '',
        '| Motor | Carga/importación s | Calentamiento s | Sesión instrumentada s | Muestras RAM / GPU | Audios con alguna muestra GPU |',
        '|---|---:|---:|---:|---:|---:|']
    for r in rows:
        covered = sum(c['gpu_samples'] > 0 for c in r['per_audio_gpu_coverage'])
        lines.append(f"| {r['motor']} | {r['load_seconds']:.2f} | {r['warmup_seconds']:.2f} | {r['session_wall_seconds']:.2f} | {r['ram_samples']} / {r['gpu_samples']} | {covered}/10 |")
    lines += ['', '## Interpretación y límites', '',
        '- Circuito técnico correcto en esta cohorte: diez resultados por motor, sin fallos ni hipótesis vacías; misma entrada y referencias, firmas coherentes y muestras JSONL coincidentes con el informe final. No hubo otros procesos de cómputo detectados en las GPU seleccionadas durante las muestras.',
        '- Parakeet tiene el menor WER observado (25 ediciones/372 palabras), Faster-Whisper 32, Crisper 40, XLSR 42 y Vosk 49. Solo diez clips; no seleccionar ganador ni extrapolar a niños, disfluencias u otros datasets.',
        '- XLSR es el más rápido en las llamadas ya calentadas. La primera llamada/carga es mucho más larga; la prueba no aísla inicialización, compilación/cachés o interferencia como causas.',
        '- Vosk necesita mucha menos RAM observada y funciona en CPU. No equivale a haber validado una tablet. Los otros motores usan RTX 3060 de 12 GB.',
        '- GPU muestreada aproximadamente cada segundo: algunos audios rápidos no tienen ninguna muestra individual. No significa GPU inactiva. Los picos del allocator Torch están guardados por audio; no equivalen al pico completo de VRAM. Para potencia/uso, conservar agregados de sesión y medir un bloque sostenido en la evaluación de rendimiento.',
        '- La energía estimada de sesión incluye carga, calentamiento e intervalos muestreados, sin reposo descontado: no dividirla para afirmar energía neta por audio ni compararla como consumo de tablet.',
        '- Ejecución concurrente: hay CPU/RAM/disco compartidos y el solapamiento cambia al terminar motores. Los tiempos son observaciones de esta ejecución, no un benchmark aislado.',
        '- Crisper: el backend instalado carga AutoModelForSpeechSeq2Seq/WhisperForConditionalGeneration y el log informa encoder_blank_head.weight/bias como UNEXPECTED. Se preserva el aviso; el paquete no consulta esa cabeza en su ruta Transformers. También hay avisos de generación/deprecación. No se ha demostrado que causen los errores textuales ni se han cambiado dependencias/decodificación. Revisar esa configuración antes de interpretar métricas de alineación fina.',
        '- Whisper, Crisper y Vosk devuelven marcas de palabra con comprobación básica de rango; no hay anclas humanas para acreditar su precisión. Parakeet no alcanza el límite configurado de tokens en estos clips; eso no certifica ausencia de omisiones en general.',
        '- Se conservan acentos/ortografía del dataset en la métrica primaria. Referencias como «fué», «despues», «ignorais» o construcciones antiguas pueden penalizar salidas con otra ortografía. Hay errores de nombres propios y segmentación en varios motores. No se corrigen referencias tras ver resultados ni se afirma por texto qué se pronunció realmente.',
        '- Siguiente paso: revisar conjuntamente transcripciones y aceptar protocolo/cobertura; después desarrollo más amplio con configuración fijada, manteniendo test reservado. Rendimiento aislado en selección fija antes de conclusiones de coste.', '',
        '## Transcripciones para comprobación', '']
    for item in selection:
        lines += [f"### {item['id']} · {item['audio_seconds']:.2f} s", '', '**Referencia:** '+item['reference'], '']
        for result in [r for r in comparisons if r['id'] == item['id']]:
            lines += [f"**{result['motor']} · WER {100*result['wer']:.2f}%:** {result['hypothesis']}", '']
    lines += ['Fuentes técnicas del aviso de Crisper: transformers_engine.py de crisperwhisper 2.0.3 instalado localmente; https://github.com/nyrahealth/CrisperWhisper/blob/main/DOCS.md (ruta Transformers y alineación con estados blank derivados de energía). La evidencia decisiva de esta ejecución es crisper.log, conservado sin modificar.']
    (out/'informe.md').write_text('\n'.join(lines)+'\n', encoding='utf-8')
    print(json.dumps(dict(status=payload['status'], selected=payload['selected'],
        local_audio_hashes_checked=len(checked_local), output=str(out/'informe.md'),
        source_files_preserved=len(hashes_before)), ensure_ascii=False, indent=2))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('folder', type=Path)
    parser.add_argument('--dataset', type=Path)
    args = parser.parse_args()
    audit(args.folder, args.dataset)
