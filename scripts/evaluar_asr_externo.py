"""Evaluación offline MLS con cinco motores y telemetría por proceso/sistema.

No graba, no sube audio y no cambia los datos. Descarga de pesos explícita y separada.
Ejecutable directamente, sin importar otros módulos del proyecto.
"""
import argparse
import csv
from datetime import datetime, timezone
import hashlib
import importlib.metadata
import io
import json
import math
import os
from pathlib import Path
import platform
import random
import re
import subprocess
import sys
import threading
import time
import unicodedata

try:
    from . import asr_motores_externos as motors
except ImportError:
    import asr_motores_externos as motors

ROOT = Path(__file__).resolve().parents[1]
SPEC = dict(name='xlsr', repo='jonatasgrosman/wav2vec2-large-xlsr-53-spanish',
            revision='96d7e9b4e4a78af515a3c6d3cee7c0826045d276', license='Apache-2.0')
MODEL_FILES = ['README.md', 'config.json', 'preprocessor_config.json',
               'pytorch_model.bin', 'vocab.json', 'special_tokens_map.json']
NORMALIZATION = 'NFC; minúsculas; puntuación Unicode sustituida por espacios; espacios colapsados; conserva tildes, ñ y números. CER incluye espacios.'


def now():
    return datetime.now(timezone.utc).isoformat()


def sha(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as stream:
        for block in iter(lambda: stream.read(1024*1024), b''):
            h.update(block)
    return h.hexdigest()


def signature(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, ensure_ascii=False).encode()).hexdigest()


def save(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix+'.tmp')
    with tmp.open('w', encoding='utf-8', newline='\n') as stream:
        json.dump(value, stream, ensure_ascii=False, indent=2, allow_nan=False)
        stream.write('\n')
    os.replace(tmp, path)


def normalized(text):
    text = unicodedata.normalize('NFC', text).lower()
    return ' '.join(''.join(' ' if unicodedata.category(c).startswith('P') else c
                            for c in text).split())


def score(reference, hypothesis):
    import jiwer
    ref, hyp = normalized(reference), normalized(hypothesis)
    words = jiwer.process_words(ref, hyp)
    chars = jiwer.process_characters(ref, hyp)
    raw_words = jiwer.process_words(reference, hypothesis)
    raw_chars = jiwer.process_characters(reference, hypothesis)
    alignment = [dict(type=c.type, ref_start=c.ref_start_idx, ref_end=c.ref_end_idx,
                      hyp_start=c.hyp_start_idx, hyp_end=c.hyp_end_idx)
                 for sentence in words.alignments for c in sentence]
    return dict(reference_normalized=ref, hypothesis_normalized=hyp,
                reference_words=len(ref.split()), hypothesis_words=len(hyp.split()),
                reference_characters=len(ref), hypothesis_characters=len(hyp),
                hits=words.hits, substitutions=words.substitutions,
                deletions=words.deletions, insertions=words.insertions,
                wer=words.wer, cer=chars.cer, mer=words.mer, wil=words.wil, wip=words.wip,
                character_hits=chars.hits, character_substitutions=chars.substitutions,
                character_deletions=chars.deletions, character_insertions=chars.insertions,
                raw_wer=raw_words.wer, raw_cer=raw_chars.cer,
                exact_normalized=ref == hyp, empty_hypothesis=not hyp, alignment=alignment)


def select_mls(dataset, split, limit, seed):
    """IDs oficiales y orden pseudoaleatorio fijo; todos los modelos reutilizarán el manifiesto."""
    import soundfile as sf
    dataset = Path(dataset).resolve()
    partition = dataset/split
    refs = partition/'transcripts.txt'
    rows = {}
    for line in refs.read_text(encoding='utf-8').splitlines():
        key, text = line.split('\t', 1)
        if not re.fullmatch(r'\d+_\d+_\d+', key) or not text.strip() or key in rows:
            raise ValueError(f'ID o referencia MLS inválida/duplicada: {key}')
        rows[key] = text
    audio = {p.stem: p for p in (partition/'audio').rglob('*.flac')}
    actual_count = sum(1 for _ in (partition/'audio').rglob('*.flac'))
    if len(audio) != actual_count or audio.keys() != rows.keys():
        raise ValueError('Los IDs de FLAC y transcripciones no coinciden exactamente.')
    ids = sorted(rows)
    random.Random(seed).shuffle(ids)
    if limit:
        ids = ids[:limit]
    selected = []
    for key in ids:
        path = audio[key]
        info = sf.info(path)
        if info.samplerate != 16000 or info.channels != 1 or info.frames <= 0:
            raise ValueError(f'Se exige mono 16 kHz no vacío: {path}')
        selected.append(dict(id=key, speaker_id=key.split('_')[0], book_id=key.split('_')[1],
                             file=path.relative_to(dataset).as_posix(), sha256=sha(path),
                             file_bytes=path.stat().st_size, frames=info.frames,
                             sample_rate=info.samplerate, audio_seconds=info.duration,
                             reference=rows[key]))
    return dict(schema_version=1, dataset='MLS español', split=split, seed=seed, limit=limit,
                selection='sorted IDs then Python random.Random(seed).shuffle; first limit, 0=all',
                transcripts_sha256=sha(refs), total_partition_audio=len(rows), items=selected)


def download_model(folder, motor='xlsr'):
    if motor != 'xlsr':
        return motors.download(folder, motor, sha, save)
    from huggingface_hub import HfApi, snapshot_download
    folder = Path(folder).resolve()
    info = HfApi().model_info(SPEC['repo'], revision=SPEC['revision'], files_metadata=True)
    if info.sha != SPEC['revision']:
        raise ValueError('La revisión descargable no coincide con la fijada.')
    names = {f.rfilename: f for f in info.siblings}
    for name in MODEL_FILES:
        if name not in names:
            raise ValueError(f'Falta archivo en la revisión fijada: {name}')
    snapshot_download(SPEC['repo'], revision=SPEC['revision'], local_dir=folder,
                      allow_patterns=MODEL_FILES, max_workers=3)
    records = []
    for name in MODEL_FILES:
        path = folder/name
        digest = sha(path)
        lfs = getattr(names[name], 'lfs', None)
        expected = lfs.get('sha256') if isinstance(lfs, dict) else getattr(lfs, 'sha256', None)
        if expected and expected != digest:
            raise ValueError(f'Hash LFS no coincide: {name}')
        records.append(dict(file=name, sha256=digest, bytes=path.stat().st_size,
                            published_lfs_sha256=expected))
    manifest = dict(**SPEC, downloaded_at_utc=now(), files=records,
                    source='Hugging Face, revisión fijada, LFS cotejado cuando está publicado')
    save(folder/'lexia_modelo.json', manifest)
    print('Modelo descargado y verificado:', folder, flush=True)


def check_model(folder, motor='xlsr'):
    if motor != 'xlsr':
        return motors.check(folder, motor, sha)
    folder = Path(folder)
    manifest = json.loads((folder/'lexia_modelo.json').read_text(encoding='utf-8'))
    if any(manifest.get(k) != v for k, v in SPEC.items()):
        raise ValueError('El manifiesto no corresponde al XLSR fijado.')
    if {f['file'] for f in manifest['files']} != set(MODEL_FILES):
        raise ValueError('Lista de archivos del modelo no válida.')
    for f in manifest['files']:
        if sha(folder/f['file']) != f['sha256']:
            raise ValueError('Modelo modificado: '+f['file'])
    return manifest


GPU_FIELDS = ['memory.used', 'utilization.gpu', 'utilization.memory', 'power.draw',
              'temperature.gpu', 'clocks.sm', 'clocks.mem']
GPU_KEYS = ['memory_used_mib', 'utilization_percent', 'memory_utilization_percent',
            'power_watts', 'temperature_celsius', 'sm_clock_mhz', 'memory_clock_mhz']


def gpu_sample(gpu):
    if gpu is None:
        return dict(status='no_solicitada')
    try:
        result = subprocess.run(['nvidia-smi', '-i', str(gpu), '--query-gpu='+','.join(GPU_FIELDS),
                                 '--format=csv,noheader,nounits'], text=True, capture_output=True, timeout=3)
        if result.returncode:
            return dict(status='no_disponible', error=result.stderr.strip())
        values = next(csv.reader(io.StringIO(result.stdout), skipinitialspace=True))
        if len(values) != len(GPU_KEYS):
            return dict(status='no_disponible', error='Formato NVIDIA inesperado')
        def number(v):
            try:
                n = float(v)
                return n if math.isfinite(n) else None
            except ValueError:
                return None
        value = dict(status='medido', **dict(zip(GPU_KEYS, map(number, values))))
        # Solo se conservan memoria de nuestro PID y número de otros procesos, no sus comandos.
        processes = subprocess.run(['nvidia-smi', '-i', str(gpu),
            '--query-compute-apps=pid,used_gpu_memory', '--format=csv,noheader,nounits'],
            text=True, capture_output=True, timeout=3)
        if processes.returncode == 0:
            rows = list(csv.reader(io.StringIO(processes.stdout), skipinitialspace=True))
            rows = [r for r in rows if len(r) == 2 and r[0].strip().isdigit()]
            own = [number(r[1]) for r in rows if int(r[0]) == os.getpid()]
            value.update(process_vram_mib=own[0] if own else None,
                         other_compute_process_count=sum(int(r[0]) != os.getpid() for r in rows),
                         process_vram_status='medido' if own and own[0] is not None else 'sin_dato_del_PID')
        else:
            value.update(process_vram_mib=None, process_vram_status='consulta_no_disponible')
        return value
    except (OSError, subprocess.TimeoutExpired) as exc:
        return dict(status='no_disponible', error=str(exc))


def distribution(values):
    import numpy as np
    values = [v for v in values if v is not None and math.isfinite(v)]
    if not values:
        return None
    return dict(count=len(values), minimum=min(values), mean=float(np.mean(values)),
                median=float(np.median(values)), std_population=float(np.std(values)),
                p90=float(np.percentile(values, 90)), p95=float(np.percentile(values, 95)),
                p99=float(np.percentile(values, 99)), maximum=max(values))


def resource_summary(samples, gpu_samples):
    energy = 0.0
    coverage = 0.0
    # No extrapolar a tramos sin muestras; no atribuir energía del dispositivo al proceso.
    for first, second in zip(gpu_samples, gpu_samples[1:]):
        p, q = first.get('power_watts'), second.get('power_watts')
        dt = second['elapsed_seconds']-first['elapsed_seconds']
        if p is not None and q is not None and 0 < dt <= 5:
            energy += .5*(p+q)*dt
            coverage += dt
    return dict(rss_bytes=distribution([s['rss_bytes'] for s in samples]),
                cpu_percent_one_core=distribution([s.get('cpu_percent_one_core') for s in samples]),
                gpu={k: distribution([s.get(k) for s in gpu_samples]) for k in GPU_KEYS+['process_vram_mib', 'other_compute_process_count']},
                gpu_energy_sampled_interval_joules=energy if coverage else None,
                gpu_energy_coverage_seconds=coverage,
                notice='RAM/CPU del proceso incluido muestreo; máximos observados. GPU, potencia y energía de la GPU física completa, no exclusivas del ASR. Sin extrapolación fuera del intervalo muestreado ni sustracción de reposo.')


def process_snapshot():
    import psutil
    p = psutil.Process()
    result = dict(rss_bytes=p.memory_info().rss, vms_bytes=p.memory_info().vms,
                  threads=p.num_threads(), cpu_times=p.cpu_times()._asdict())
    for field, getter in [('memory_full', p.memory_full_info), ('io_counters', p.io_counters),
                           ('context_switches', p.num_ctx_switches)]:
        try:
            result[field] = getter()._asdict()
        except (psutil.Error, AttributeError, NotImplementedError) as exc:
            result[field] = dict(status='no_disponible', reason=type(exc).__name__)
    try:
        result['cpu_affinity'] = p.cpu_affinity()
    except (psutil.Error, AttributeError, NotImplementedError):
        result['cpu_affinity'] = None
    # ru_maxrss de Linux es KiB; es un máximo de toda la vida, no por audio.
    if sys.platform.startswith('linux'):
        import resource
        result['lifetime_peak_rss_bytes'] = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*1024
    return result


def system_snapshot(path):
    import psutil
    result = dict(cpu_percent_machine=psutil.cpu_percent(None),
                  logical_cpus=psutil.cpu_count(), physical_cores=psutil.cpu_count(logical=False),
                  virtual_memory=psutil.virtual_memory()._asdict(), swap=psutil.swap_memory()._asdict(),
                  disk_usage=psutil.disk_usage(str(path))._asdict(),
                  load_average=list(os.getloadavg()) if hasattr(os, 'getloadavg') else None)
    try:
        freq = psutil.cpu_freq()
        result['cpu_frequency_mhz'] = freq._asdict() if freq else None
    except (OSError, NotImplementedError):
        result['cpu_frequency_mhz'] = None
    try:
        result['disk_io_global'] = psutil.disk_io_counters()._asdict()
    except (OSError, AttributeError, NotImplementedError):
        result['disk_io_global'] = None
    try:
        result['temperatures_reported'] = {k: [v._asdict() for v in values]
            for k, values in psutil.sensors_temperatures().items()}
    except (OSError, AttributeError, NotImplementedError):
        result['temperatures_reported'] = None
    return result


def gpu_details(gpu):
    if gpu is None:
        return None
    try:
        value = subprocess.run(['nvidia-smi', '-i', str(gpu), '-q', '-d',
            'PERFORMANCE,TEMPERATURE,POWER,CLOCK,MEMORY,UTILIZATION'],
            capture_output=True, text=True, timeout=5)
        return dict(returncode=value.returncode, output=value.stdout, error=value.stderr,
                    scope='GPU completa: estado de rendimiento, límites y motivos informados por el controlador.')
    except (OSError, subprocess.TimeoutExpired) as exc:
        return dict(status='no_disponible', error=str(exc))


def environment_size():
    total = 0
    try:
        for path in Path(sys.prefix).rglob('*'):
            if path.is_file() and not path.is_symlink():
                total += path.stat().st_size
        return dict(logical_regular_file_bytes=total,
                    scope='Suma lógica de tamaños; enlaces duros compartidos pueden contarse en más de un entorno; no espacio físico exclusivo.')
    except OSError as exc:
        return dict(status='no_disponible', error=str(exc))


def cpu_model():
    if sys.platform.startswith('linux'):
        try:
            for line in Path('/proc/cpuinfo').read_text(encoding='utf-8').splitlines():
                if line.startswith('model name') and ':' in line:
                    return line.split(':', 1)[1].strip()
        except OSError:
            pass
    return platform.processor()


class Monitor:
    def __init__(self, gpu, interval=.25, stream_path=None):
        import psutil
        self.process = psutil.Process()
        self.gpu, self.interval = gpu, interval
        self.samples, self.gpu_samples = [], []
        self.event = threading.Event()
        self.stream_path, self.stream, self.stream_error = stream_path, None, None

    def stream_sample(self, kind, value):
        if self.stream is not None and self.stream_error is None:
            try:
                self.stream.write(json.dumps(dict(kind=kind, data=value), ensure_ascii=False, allow_nan=False)+'\n')
                self.stream.flush()
            except (OSError, ValueError) as exc:
                self.stream_error = str(exc)

    def start(self):
        self.begin = time.perf_counter()
        self.started_at_utc = now()
        if self.stream_path is not None:
            self.stream_path.parent.mkdir(parents=True, exist_ok=True)
            self.stream = self.stream_path.open('x', encoding='utf-8', newline='\n')
            self.stream_sample('start', dict(started_at_utc=self.started_at_utc, pid=os.getpid()))
        self.process.cpu_percent(None)
        self.thread = threading.Thread(target=self.loop, daemon=True)
        self.thread.start()

    def loop(self):
        import psutil
        next_gpu = 0
        while not self.event.is_set():
            elapsed = time.perf_counter()-self.begin
            try:
                cpu = self.process.cpu_times()
                memory = self.process.memory_info()
                self.samples.append(dict(elapsed_seconds=elapsed, rss_bytes=memory.rss,
                    vms_bytes=memory.vms, cpu_user_seconds=cpu.user, cpu_system_seconds=cpu.system,
                    cpu_percent_one_core=self.process.cpu_percent(None) if self.samples else None,
                    threads=self.process.num_threads(), system_ram_available_bytes=psutil.virtual_memory().available,
                    system_cpu_percent_machine=psutil.cpu_percent(None),
                    system_ram_used_bytes=psutil.virtual_memory().used,
                    system_swap_used_bytes=psutil.swap_memory().used,
                    load_average=list(os.getloadavg()) if hasattr(os, 'getloadavg') else None))
                self.stream_sample('process', self.samples[-1])
            except psutil.Error:
                pass
            if self.gpu is not None and elapsed >= next_gpu:
                # Tiempo central de consulta; intervalo real conservado, consulta puede tardar.
                first = time.perf_counter()
                value = gpu_sample(self.gpu)
                last = time.perf_counter()
                self.gpu_samples.append(dict(elapsed_seconds=(first+last)/2-self.begin,
                                             query_seconds=last-first, **value))
                self.stream_sample('gpu', self.gpu_samples[-1])
                next_gpu = last-self.begin+1
            self.event.wait(self.interval)

    def stop(self):
        self.event.set()
        self.thread.join()
        if self.stream is not None:
            self.stream.close()
        return dict(wall_seconds=time.perf_counter()-self.begin, ram_requested_interval_seconds=self.interval,
                    started_at_utc=self.started_at_utc, finished_at_utc=now(),
                    incremental_log=self.stream_path.name if self.stream_path else None,
                    incremental_log_error=self.stream_error,
                    gpu_requested_interval_seconds=1, samples=self.samples, gpu_samples=self.gpu_samples,
                    summary=resource_summary(self.samples, self.gpu_samples))


def load_xlsr(folder, gpu, threads):
    import torch
    from transformers import (AutoModelForCTC, Wav2Vec2FeatureExtractor,
                              Wav2Vec2CTCTokenizer, Wav2Vec2Processor)
    torch.set_num_threads(threads)
    torch.manual_seed(42)
    torch.backends.cudnn.benchmark = False
    device = 'cuda:0' if gpu is not None else 'cpu'
    if gpu is not None and (not torch.cuda.is_available() or torch.cuda.device_count() != 1):
        raise RuntimeError('Se exige exactamente una GPU visible; no se cambia a CPU.')
    processor = Wav2Vec2Processor(
        feature_extractor=Wav2Vec2FeatureExtractor.from_pretrained(folder, local_files_only=True),
        tokenizer=Wav2Vec2CTCTokenizer.from_pretrained(folder, local_files_only=True))
    model = AutoModelForCTC.from_pretrained(folder, local_files_only=True, trust_remote_code=False,
                                           dtype=torch.float32, weights_only=True).eval().to(device)
    def synchronize():
        if gpu is not None:
            torch.cuda.synchronize()
    def infer(signal):
        start = time.perf_counter()
        inputs = processor(signal, sampling_rate=16000, return_tensors='pt').to(device)
        synchronize()
        prepare = time.perf_counter()-start
        start = time.perf_counter()
        with torch.inference_mode():
            ids = model(**inputs).logits.argmax(dim=-1)
        synchronize()
        forward = time.perf_counter()-start
        start = time.perf_counter()
        text = processor.batch_decode(ids.cpu())[0]
        decode = time.perf_counter()-start
        return dict(hypothesis=text, prepare_seconds=prepare, forward_seconds=forward,
                    decode_seconds=decode, token_ids=ids.cpu().tolist()[0])
    synchronize()
    infer.parameter_count = sum(p.numel() for p in model.parameters())
    return infer, torch


def audio_metrics(signal):
    import numpy as np
    if not np.isfinite(signal).all():
        raise ValueError('Muestras no finitas.')
    peak = float(np.max(np.abs(signal)))
    rms = float(np.sqrt(np.mean(signal.astype(np.float64)**2)))
    return dict(peak_amplitude=peak, rms_amplitude=rms,
                rms_dbfs=20*math.log10(rms) if rms else None,
                samples_abs_ge_0999_fraction=float(np.mean(np.abs(signal) >= .999)),
                all_zero=peak == 0, vad=None, snr=None,
                notice='Indicador de amplitud próxima al límite, no diagnóstico de saturación. Sin VAD ni SNR medidos.')


def aggregate(records):
    good = [r for r in records if r['status'] == 'ok']
    names = ['hits', 'substitutions', 'deletions', 'insertions', 'reference_words',
             'character_substitutions', 'character_deletions', 'character_insertions', 'reference_characters']
    totals = {k: sum(r['accuracy'][k] for r in good) for k in names}
    n, c = totals['reference_words'], totals['reference_characters']
    audio = sum(r['audio_seconds'] for r in good)
    seconds = sum(r['timing']['asr_seconds'] for r in good)
    return dict(attempted=len(records), completed=len(good), failures=len(records)-len(good), totals=totals,
        corpus_wer=(totals['substitutions']+totals['deletions']+totals['insertions'])/n if n else None,
        corpus_cer=(totals['character_substitutions']+totals['character_deletions']+totals['character_insertions'])/c if c else None,
        exact_audio_fraction=sum(r['accuracy']['exact_normalized'] for r in good)/len(good) if good else None,
        empty_hypotheses=sum(r['accuracy']['empty_hypothesis'] for r in good),
        completed_audio_seconds=audio, asr_total_seconds=seconds,
        corpus_asr_rtf=seconds/audio if audio else None,
        audio_hours_per_asr_hour=audio/seconds if seconds else None,
        per_audio_wer=distribution([r['accuracy']['wer'] for r in good]),
        per_audio_cer=distribution([r['accuracy']['cer'] for r in good]),
        per_audio_asr_seconds=distribution([r['timing']['asr_seconds'] for r in good]),
        per_audio_rtf=distribution([r['timing']['asr_rtf'] for r in good]))


def report_record(record):
    """Resumen en memoria sin tokens/segmentos/alineamientos voluminosos."""
    result = {k: record[k] for k in ['id', 'status', 'audio_seconds', 'run_signature', 'error'] if k in record}
    result['accuracy'] = {k: v for k, v in record.get('accuracy', {}).items() if isinstance(v, (float, int, bool))}
    result['timing'] = {k: v for k, v in record.get('timing', {}).items() if isinstance(v, (float, int))}
    return result


def write_reports(folder, manifest, records=None):
    if records is None:
        records = []
        for item in manifest['selection']['items']:
            path = folder/'audios'/f"{item['id']}.json"
            if path.exists():
                record = json.loads(path.read_text(encoding='utf-8'))
                if record['run_signature'] != manifest['run_signature']:
                    raise ValueError('Resultado de otra configuración en la salida.')
                records.append(report_record(record))
    summary = dict(created_at_utc=now(), run_signature=manifest['run_signature'],
                   selected=len(manifest['selection']['items']), **aggregate(records))
    save(folder/'resumen.json', summary)
    columns = ['id', 'status', 'audio_seconds', 'wer', 'cer', 'substitutions', 'deletions',
               'insertions', 'asr_seconds', 'asr_rtf', 'error']
    with (folder/'audios.csv').open('w', encoding='utf-8-sig', newline='') as stream:
        writer = csv.DictWriter(stream, fieldnames=columns)
        writer.writeheader()
        for r in records:
            merged = {**r, **r.get('accuracy', {}), **r.get('timing', {})}
            writer.writerow({k: merged.get(k) for k in columns})
    lines = [f"# MLS · {manifest.get('motor', 'xlsr')} · prueba offline", '',
        f"Partición: {manifest['selection']['split']}. Seleccionados: {summary['selected']}; completados: {summary['completed']}; fallos: {summary['failures']}.",
        '', f"WER global: {summary['corpus_wer']}; CER global: {summary['corpus_cer']}; RTF ASR: {summary['corpus_asr_rtf']}.",
        '', '| Audio | Estado | Duración s | WER | CER | ASR s | RTF |', '|---|---|---:|---:|---:|---:|---:|']
    for r in records:
        a, t = r.get('accuracy', {}), r.get('timing', {})
        def fmt(v):
            return '—' if v is None else f'{v:.4f}'
        lines.append(f"| {r['id']} | {r['status']} | {fmt(r.get('audio_seconds'))} | {fmt(a.get('wer'))} | {fmt(a.get('cer'))} | {fmt(t.get('asr_seconds'))} | {fmt(t.get('asr_rtf'))} |")
    lines += ['', 'Normalización: '+NORMALIZATION, '',
        'Configuración exacta del motor en ejecucion.json. Una pasada por audio, batch 1. Sin VAD externo, remuestreo o reducción de ruido. Endpointing/segmentación internos dependen del motor. Calentamiento excluido y conservado por sesión.',
        'RTF ASR incluye preparación de entradas, transferencia, forward y decodificación; excluye lectura, métricas, escritura y carga del modelo. CUDA sincronizada al medir.',
        'Los fallos no reciben WER cero: se excluyen del cálculo y quedan contados. Reanudar no reintenta resultados fallidos.',
        'Recursos por sesión en sesiones/*.json, con muestras y alcance. La primera ejecución se conserva separada; cachés de disco no controladas. No es latencia visual, prueba de literalidad ni medida de tablet.',
        'Revisar cobertura, avisos y comparabilidad; ejecución concurrente y medición de rendimiento aislado son condiciones diferentes.']
    (folder/'resumen.md').write_text('\n'.join(lines)+'\n', encoding='utf-8')
    return summary


def run(args):
    import numpy as np
    import psutil
    import soundfile as sf
    motor = getattr(args, 'motor', 'xlsr')
    args.dataset = args.dataset.resolve()
    args.modelo = args.modelo.resolve()
    folder = args.salida.resolve()
    if args.particion == 'test' and not args.confirmar_test:
        raise ValueError('Test reservado: requiere --confirmar-test con configuración ya fijada.')
    selection = select_mls(args.dataset, args.particion, args.limite, args.semilla)
    if motor == 'vosk' and args.gpu is not None:
        raise ValueError('Vosk se ejecuta en CPU en este protocolo.')
    model = check_model(args.modelo, motor)
    versions = {}
    for package in ['numpy', 'soundfile', 'psutil', 'jiwer']+motors.PACKAGES[motor]:
        versions[package] = importlib.metadata.version(package)
    gpu_info = None
    if args.gpu is not None:
        gpu_info = subprocess.check_output(['nvidia-smi', '-i', str(args.gpu),
            '--query-gpu=uuid,name,driver_version,memory.total', '--format=csv,noheader'], text=True).strip()
    config = dict(motor=motor, model={k: model[k] for k in ['name', 'repo', 'url', 'revision', 'files'] if k in model},
        selection=selection, normalization=NORMALIZATION, script_sha256=sha(__file__),
        adapter_sha256=sha(motors.__file__), versions=versions, gpu_physical_index=args.gpu, gpu_info=gpu_info,
        parameters=motors.parameters(motor), batch_size=1, cpu_threads_requested=args.hilos,
        thread_notice='OMP/MKL/OpenBLAS environment limits recorded; Torch explicit threads; Vosk native threads not guaranteed.',
        mode=getattr(args, 'modo_ejecucion', 'sin_clasificar'), cohort=getattr(args, 'cohorte', None),
        runtime=dict(python=sys.version, platform=platform.platform(), cpu=cpu_model(),
                     logical_cpus=os.cpu_count()), warmup='first selected audio once per session, excluded',
        external_vad=False, denoise=False, resample=False, external_chunking=False,
        report_every=getattr(args, 'informar_cada', 50), progress_every_audio=True)
    run_signature = signature(config)
    manifest = dict(created_at_utc=now(), run_signature=run_signature, **config)
    manifest_path = folder/'ejecucion.json'
    if manifest_path.exists():
        previous = json.loads(manifest_path.read_text(encoding='utf-8'))
        if not args.reanudar or previous['run_signature'] != run_signature:
            raise ValueError('Salida existente: usar --reanudar con exactamente los mismos datos/configuración.')
        manifest = previous
    else:
        if folder.exists() and any(folder.iterdir()):
            raise ValueError('La carpeta de salida debe estar vacía para una ejecución nueva.')
        save(manifest_path, manifest)
    pending, report_rows = [], []
    for item in selection['items']:
        path = folder/'audios'/f"{item['id']}.json"
        if not path.exists():
            pending.append(item)
            continue
        saved = json.loads(path.read_text(encoding='utf-8'))
        if saved.get('run_signature') != run_signature or saved.get('id') != item['id']:
            raise ValueError('Resultado previo de otra ejecución/configuración.')
        if saved.get('status') == 'interrupted':
            # Conservar el intento incompleto y repetir únicamente ese audio al reanudar.
            save(folder/'intentos'/(item['id']+'_'+datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S_%f')+'.json'), saved)
            pending.append(item)
        elif saved.get('status') in ('ok', 'error'):
            report_rows.append(report_record(saved))
        else:
            raise ValueError('Estado de resultado previo no reconocido.')
    if not pending:
        summary = write_reports(folder, manifest, report_rows)
        print('Sin audios pendientes.', summary, flush=True)
        if summary['failures']:
            raise RuntimeError('Hay fallos guardados; revisar antes de iniciar otra ejecución.')
        return
    os.environ['CUDA_VISIBLE_DEVICES'] = str(args.gpu) if args.gpu is not None else ''
    os.environ['HF_HUB_OFFLINE'] = '1'
    os.environ['TOKENIZERS_PARALLELISM'] = 'false'
    session = dict(created_at_utc=now(), run_signature=run_signature, status='running',
                   pid=os.getpid(), hostname=platform.node(),
                   rss_before_load_bytes=psutil.Process().memory_info().rss,
                   process_before_load=process_snapshot(), system_before_load=system_snapshot(args.dataset),
                   gpu_details_before_load=gpu_details(args.gpu), environment_size=environment_size(),
                   environment_packages=sorted(f'{d.metadata["Name"]}=={d.version}' for d in importlib.metadata.distributions()),
                   thread_environment={k: os.environ.get(k) for k in ['OMP_NUM_THREADS','MKL_NUM_THREADS','OPENBLAS_NUM_THREADS','NUMEXPR_NUM_THREADS','PYTHONHASHSEED']},
                   process_cpu_start_seconds=time.process_time(),
                   model_disk_bytes=sum(f['bytes'] for f in model['files']),
                   unavailable=dict(vad=None, snr=None, cpu_energy=None, tablet=None, flops=None))
    session_id = datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S_%f')
    monitor = Monitor(args.gpu, stream_path=folder/'sesiones'/(session_id+'.jsonl'))
    monitor.start()
    progress_path = folder/'progreso.json'
    def progress(status, last=None):
        save(progress_path, dict(updated_at_utc=now(), status=status, motor=motor, pid=os.getpid(),
            selected=len(selection['items']), completed=sum(r['status'] == 'ok' for r in report_rows),
            failures=sum(r['status'] == 'error' for r in report_rows),
            interrupted=sum(r['status'] == 'interrupted' for r in report_rows),
            recorded=len(report_rows), last_audio=last,
            completed_audio_seconds=sum(r['audio_seconds'] for r in report_rows if r['status'] == 'ok'),
            elapsed_session_seconds=time.perf_counter()-monitor.begin,
            summary_notice='progreso.json se actualiza cada audio; resumen.md/csv cada bloque y al finalizar.'))
    progress('loading')
    try:
        start = time.perf_counter()
        infer, torch = (load_xlsr(args.modelo, args.gpu, args.hilos) if motor == 'xlsr'
                        else motors.load(motor, args.modelo, args.gpu, args.hilos))
        session.update(model_import_and_load_seconds=time.perf_counter()-start,
                       torch_cuda_build=torch.version.cuda if torch is not None else None,
                       gpu_name=torch.cuda.get_device_name(0) if torch is not None and args.gpu is not None else gpu_info,
                       parameter_count=getattr(infer, 'parameter_count', None),
                       process_after_load=process_snapshot())
        first = selection['items'][0]
        signal, _ = sf.read(args.dataset/first['file'], dtype='float32')
        start = time.perf_counter()
        session['warmup'] = dict(audio_id=first['id'], **infer(signal))
        session['warmup']['wall_seconds'] = time.perf_counter()-start
        progress('running')
        for i, item in enumerate(pending, 1):
            print(f"[{i}/{len(pending)}] {item['id']} ({item['audio_seconds']:.2f} s)", flush=True)
            record = dict(**item, created_at_utc=now(), run_signature=run_signature, status='error')
            record['monitor_interval_start_seconds'] = time.perf_counter()-monitor.begin
            record['rss_before_bytes'] = psutil.Process().memory_info().rss
            record['process_before'] = process_snapshot()
            cpu_start = time.process_time()
            begin = time.perf_counter()
            try:
                path = args.dataset/item['file']
                if sha(path) != item['sha256']:
                    raise ValueError('El audio cambió desde la selección.')
                start = time.perf_counter()
                signal, sr = sf.read(path, dtype='float32')
                read_seconds = time.perf_counter()-start
                if sr != 16000 or signal.ndim != 1 or len(signal) != item['frames']:
                    raise ValueError('El audio decodificado no coincide con el manifiesto.')
                record['input_metrics'] = audio_metrics(signal)
                if args.gpu is not None and torch is not None:
                    torch.cuda.reset_peak_memory_stats()
                start = time.perf_counter()
                result = infer(signal)
                asr_seconds = time.perf_counter()-start
                record.update(hypothesis=result.pop('hypothesis'), token_ids=result.pop('token_ids'))
                record['native_output'] = {k: result.pop(k) for k in list(result) if not k.endswith('_seconds')}
                if args.gpu is not None and torch is not None:
                    record['torch_memory'] = dict(peak_allocated_bytes=torch.cuda.max_memory_allocated(),
                        peak_reserved_bytes=torch.cuda.max_memory_reserved(),
                        scope='Allocator Torch; incluye modelo residente, no toda VRAM del proceso/dispositivo.')
                start = time.perf_counter()
                record['accuracy'] = score(item['reference'], record['hypothesis'])
                score_seconds = time.perf_counter()-start
                record['timing'] = dict(read_audio_seconds=read_seconds, **result,
                    asr_seconds=asr_seconds, asr_rtf=asr_seconds/item['audio_seconds'],
                    score_seconds=score_seconds, through_scoring_seconds=time.perf_counter()-begin,
                    process_cpu_seconds_through_scoring=time.process_time()-cpu_start)
                record['status'] = 'ok'
                print(f"  WER {record['accuracy']['wer']:.3f}; ASR {asr_seconds:.2f} s; {record['hypothesis']}", flush=True)
            except KeyboardInterrupt as exc:
                record.update(status='interrupted', error='KeyboardInterrupt', failed_after_seconds=time.perf_counter()-begin)
                raise
            except Exception as exc:
                record.update(error=f'{type(exc).__name__}: {exc}', failed_after_seconds=time.perf_counter()-begin)
                raise
            finally:
                record['monitor_interval_end_seconds'] = time.perf_counter()-monitor.begin
                record['rss_after_bytes'] = psutil.Process().memory_info().rss
                record['process_after'] = process_snapshot()
                record['resource_sampled_interval'] = resource_summary(
                    [s for s in list(monitor.samples) if record['monitor_interval_start_seconds'] <= s['elapsed_seconds'] <= record['monitor_interval_end_seconds']],
                    [s for s in list(monitor.gpu_samples) if record['monitor_interval_start_seconds'] <= s['elapsed_seconds'] <= record['monitor_interval_end_seconds']])
                save(folder/'audios'/f"{item['id']}.json", record)
                report_rows.append(report_record(record))
                progress('running', item['id'])
                if i % getattr(args, 'informar_cada', 50) == 0:
                    write_reports(folder, manifest, report_rows)
        session['status'] = 'completed'
    except BaseException as exc:
        session.update(status='interrupted' if isinstance(exc, KeyboardInterrupt) else 'error', error=f'{type(exc).__name__}: {exc}')
        raise
    finally:
        session['resources'] = monitor.stop()
        session['process_at_end'] = process_snapshot()
        session['system_at_end'] = system_snapshot(args.dataset)
        session['gpu_details_at_end'] = gpu_details(args.gpu)
        session['finished_at_utc'] = now()
        session['process_cpu_seconds'] = time.process_time()-session.pop('process_cpu_start_seconds')
        save(folder/'sesiones'/(session_id+'.json'), session)
        summary = write_reports(folder, manifest, report_rows)
        progress(session['status'])
        print('Informe:', folder/'resumen.md', flush=True)
        print(f"Completados {summary['completed']}/{summary['selected']}; fallos {summary['failures']}.", flush=True)
    if summary['failures']:
        raise RuntimeError('La salida contiene fallos; no es una evaluación completa válida.')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='action', required=True)
    download = sub.add_parser('descargar', help='Solo pesos fijados; sin audio/inferencia.')
    download.add_argument('--motor', choices=motors.SPECS, default='xlsr')
    download.add_argument('--modelo', type=Path)
    evaluation = sub.add_parser('evaluar')
    evaluation.add_argument('--dataset', type=Path, required=True)
    evaluation.add_argument('--motor', choices=motors.SPECS, default='xlsr')
    evaluation.add_argument('--modelo', type=Path)
    evaluation.add_argument('--salida', type=Path, required=True)
    evaluation.add_argument('--particion', choices=['dev', 'test'], default='dev')
    evaluation.add_argument('--limite', type=int, default=10, help='0=todos; primera prueba 10.')
    evaluation.add_argument('--semilla', type=int, default=42)
    evaluation.add_argument('--hilos', type=int, default=4)
    evaluation.add_argument('--gpu', type=int, help='Índice físico asignado; sin opción usa CPU explícitamente.')
    evaluation.add_argument('--reanudar', action='store_true')
    evaluation.add_argument('--confirmar-test', action='store_true')
    evaluation.add_argument('--modo-ejecucion', choices=['aislada', 'concurrente', 'sin_clasificar'], default='sin_clasificar')
    evaluation.add_argument('--cohorte', help='Identificador del lanzamiento compartido.')
    evaluation.add_argument('--informar-cada', type=int, default=50,
                            help='Regenerar informes cada N audios; cada resultado/progreso se guarda siempre.')
    args = parser.parse_args()
    for key in ['OMP_NUM_THREADS', 'MKL_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'NUMEXPR_NUM_THREADS']:
        os.environ[key] = str(getattr(args, 'hilos', 4))
    args.modelo = args.modelo or ROOT/'modelos'/motors.SPECS[args.motor]['folder']
    if args.action == 'descargar':
        download_model(args.modelo, args.motor)
    else:
        if args.limite < 0 or args.hilos < 1 or args.informar_cada < 1 or (args.gpu is not None and args.gpu < 0):
            parser.error('Límite/GPU no negativos e hilos positivos.')
        run(args)


if __name__ == '__main__':
    main()
