"""Métricas de cómputo: distinguir medición, configuración y datos no disponibles."""
import csv
from datetime import datetime, timezone
import json
import math
import os
from pathlib import Path
import platform
import shutil
import statistics
import subprocess
import threading
from time import perf_counter, process_time


def memory_snapshot():
    if os.name != 'nt':
        return {'status': 'no_disponible', 'reason': 'Medidor de memoria implementado para Windows.'}
    import ctypes
    from ctypes import wintypes
    class Counters(ctypes.Structure):
        _fields_ = [('cb', wintypes.DWORD), ('PageFaultCount', wintypes.DWORD)] + [
            (n, ctypes.c_size_t) for n in ['PeakWorkingSetSize', 'WorkingSetSize',
            'QuotaPeakPagedPoolUsage', 'QuotaPagedPoolUsage', 'QuotaPeakNonPagedPoolUsage',
            'QuotaNonPagedPoolUsage', 'PagefileUsage', 'PeakPagefileUsage', 'PrivateUsage']]
    class MemoryStatus(ctypes.Structure):
        _fields_ = [('dwLength', wintypes.DWORD), ('dwMemoryLoad', wintypes.DWORD)] + [
            (n, ctypes.c_ulonglong) for n in ['total_phys', 'available_phys', 'total_pagefile',
            'available_pagefile', 'total_virtual', 'available_virtual', 'available_extended_virtual']]
    kernel = ctypes.WinDLL('kernel32', use_last_error=True)
    kernel.GetCurrentProcess.restype = wintypes.HANDLE
    kernel.K32GetProcessMemoryInfo.argtypes = [wintypes.HANDLE, ctypes.POINTER(Counters), wintypes.DWORD]
    counters = Counters()
    counters.cb = ctypes.sizeof(counters)
    status = MemoryStatus()
    status.dwLength = ctypes.sizeof(status)
    if not kernel.K32GetProcessMemoryInfo(kernel.GetCurrentProcess(), ctypes.byref(counters), counters.cb):
        return {'status': 'no_disponible', 'reason': 'Windows no devuelve memoria del proceso.'}
    system_ok = kernel.GlobalMemoryStatusEx(ctypes.byref(status))
    return {'status': 'medido', 'working_set_bytes': counters.WorkingSetSize,
            'private_commit_bytes': counters.PrivateUsage,
            'process_lifetime_peak_working_set_bytes': counters.PeakWorkingSetSize,
            'system_ram_total_bytes': status.total_phys if system_ok else None,
            'system_ram_available_bytes': status.available_phys if system_ok else None}


def gpu_snapshot():
    executable = shutil.which('nvidia-smi')
    if not executable:
        return {'status': 'no_disponible', 'reason': 'nvidia-smi no disponible; no significa ausencia de GPU.'}
    try:
        result = subprocess.run([executable, '--query-gpu=name,driver_version,memory.total,memory.used,utilization.gpu,power.draw,temperature.gpu',
                                 '--format=csv,noheader,nounits'], capture_output=True, text=True, timeout=2,
                                creationflags=getattr(subprocess, 'CREATE_NO_WINDOW', 0))
        if result.returncode:
            return {'status': 'no_disponible', 'reason': 'La consulta NVIDIA falló.'}
        gpus = []
        def number(value):
            try:
                value = float(value)
                return value if math.isfinite(value) else None
            except ValueError:
                return None
        for row in csv.reader(result.stdout.splitlines(), skipinitialspace=True):
            if len(row) != 7:
                continue
            gpus.append(dict(zip(['name', 'driver', 'vram_total_mib', 'vram_used_mib',
                                  'utilization_percent', 'power_watts', 'temperature_celsius'],
                                 [row[0], row[1], *[number(v) for v in row[2:]]])))
        return {'status': 'medido' if gpus else 'no_disponible', 'gpus': gpus,
                'scope': 'GPU completa del equipo; no atribuible exclusivamente al ASR ni a su proceso.'}
    except (OSError, subprocess.TimeoutExpired):
        return {'status': 'no_disponible', 'reason': 'Consulta NVIDIA no completada.'}


def hardware_snapshot():
    cpu = platform.processor() or None
    if os.name == 'nt':
        try:
            import winreg
            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r'HARDWARE\DESCRIPTION\System\CentralProcessor\0') as key:
                cpu = winreg.QueryValueEx(key, 'ProcessorNameString')[0].strip()
        except OSError:
            pass
    return {'captured_at_utc': datetime.now(timezone.utc).isoformat(), 'os': platform.platform(),
            'architecture': platform.machine(), 'python': platform.python_version(),
            'cpu_model': cpu, 'logical_cpus': os.cpu_count(), 'memory': memory_snapshot(), 'gpu': gpu_snapshot()}


class ResourceMonitor:
    """RAM/CPU cada 0,25 s y GPU global aproximadamente cada segundo.

    El proceso medido incluye el muestreo y el programa, no solo inferencia.
    La frecuencia real queda registrada; los máximos muestreados no son picos garantizados.
    """
    def __init__(self):
        self.samples = []
        self.gpu_samples = []
        self.stop_event = threading.Event()

    def start(self):
        self.hardware = hardware_snapshot()
        self.wall_start, self.cpu_start = perf_counter(), process_time()
        self.thread = threading.Thread(target=self._sample, daemon=True)
        self.thread.start()

    def _sample(self):
        next_gpu = 0
        while not self.stop_event.is_set():
            elapsed = perf_counter()-self.wall_start
            self.samples.append({'elapsed_seconds': elapsed, 'cpu_seconds': process_time()-self.cpu_start,
                                 'memory': memory_snapshot()})
            if elapsed >= next_gpu:
                gpu = gpu_snapshot()
                self.gpu_samples.append({'elapsed_seconds': elapsed, **gpu})
                next_gpu = perf_counter()-self.wall_start+1
            self.stop_event.wait(.25)

    def stop(self):
        self.stop_event.set()
        self.thread.join()
        elapsed, cpu = perf_counter()-self.wall_start, process_time()-self.cpu_start
        return {'hardware': self.hardware, 'wall_seconds': elapsed, 'process_cpu_seconds': cpu,
                'cpu_average_percent_one_logical_core': 100*cpu/elapsed if elapsed else None,
                'cpu_average_percent_machine_capacity': 100*cpu/elapsed/(os.cpu_count() or 1) if elapsed else None,
                'samples': self.samples, 'gpu_samples': self.gpu_samples,
                'final_memory': memory_snapshot(),
                'unavailable': {'asr_energy_joules': None, 'cpu_temperature_celsius': None,
                                'asr_flops': None, 'tablet_memory_and_battery': None},
                'notice': 'CPU y RAM del proceso completo, incluido muestreo. CPU 100% equivale a un procesador lógico; puede superar 100%. GPU/VRAM/potencia/temperatura son del equipo completo, no del ASR. No se mide energía específica, FLOPs ni rendimiento de tablet. Intervalos reales registrados, máximos muestreados no garantizan pico. Muestreo separado de inferencia; puede influir en la carga.'}


def compute_summary(data):
    updates = data.get('updates', [])
    times = [u['processing_seconds'] for u in updates if 'processing_seconds' in u]
    duration = data.get('audio_seconds')
    resources = data.get('resources')
    device = data.get('device')
    summary = {'model': data.get('model'), 'device': device, 'precision': data.get('compute_type'),
               'model_disk_bytes': data.get('model_disk_bytes'), 'input_audio_metrics': data.get('input_audio_metrics'),
               'gpu_used_for_asr': False if device == 'cpu' else True if device == 'cuda' else None,
               'resources_status': 'medido' if resources else 'no_medido_en_la_ejecucion_original',
               'audio_seconds': duration, 'model_load_seconds': data.get('model_load_seconds'),
               'asr_cpu_seconds': sum(u['asr_cpu_seconds'] for u in updates) if updates and all('asr_cpu_seconds' in u for u in updates) else None}
    if times:
        summary.update(inference_total_seconds=sum(times), inference_median_seconds=statistics.median(times),
                       inference_p95_seconds=sorted(times)[max(0, math.ceil(.95*len(times))-1)],
                       inference_max_seconds=max(times), real_time_factor_full_audio=sum(times)/duration if duration else None,
                       inference_seconds_per_update=sum(times)/len(times),
                       audio_seconds_per_inference_second=duration/sum(times) if duration and sum(times)>0 else None,
                       over_block_updates=sum(t>data.get('block_seconds', float('inf')) for t in times),
                       max_backlog_seconds_simulated=max(u.get('backlog_seconds_simulated', 0) for u in updates),
                       audio_reprocessed_seconds=sum(u.get('audio_reprocessed_seconds',0) for u in updates),
                       real_time_factor_nonempty_hypotheses=None)
        active = [u for u in updates if u.get('hypothesis')]
        # No se inventa duración de habla: para separar silencio se necesitan anclas/VAD explícitos.
        summary['nonempty_hypothesis_updates'] = len(active)
    if resources:
        summary['resources'] = resources
        memory_samples = [s['memory']['working_set_bytes'] for s in resources.get('samples', [])
                          if s['memory'].get('working_set_bytes') is not None]
        summary['ram_working_set_max_sampled_bytes'] = max(memory_samples) if memory_samples else None
        grouped = {}
        for sample in resources.get('gpu_samples', []):
            for index, gpu in enumerate(sample.get('gpus', [])):
                grouped.setdefault((index, gpu['name']), []).append(gpu)
        summary['gpu_global_sampled_statistics'] = []
        for (index, name), samples in grouped.items():
            stats = {'index': index, 'name': name, 'sample_count': len(samples),
                     'scope': 'GPU global del equipo, no atribuible al ASR; media aritmética de muestras.'}
            for field in ['vram_used_mib', 'utilization_percent', 'power_watts', 'temperature_celsius']:
                values = [s[field] for s in samples if s.get(field) is not None]
                stats[field] = {'minimum': min(values), 'mean': statistics.mean(values), 'maximum': max(values)} if values else None
            summary['gpu_global_sampled_statistics'].append(stats)
    return summary


def compute_markdown(entries):
    lines = ['## Recursos y coste computacional', '',
             'Datos de la ejecución original. «No medido» no significa cero. RTF = suma de inferencias / duración del audio completo (incluye silencio); no es latencia visual ni mide captura, escritura o muestreo. Las rondas de una grabación no son lecturas independientes.', '',
             '| Registro | Dispositivo ASR | Precisión | GPU para ASR | RTF | Máx. inferencia (s) | CPU/RAM/GPU instrumentadas |',
             '|---|---|---|---|---:|---:|---|']
    def fmt(value):
        return 'no medido' if value is None else f'{value:.3f}'
    for label, data in entries:
        s = compute_summary(data)
        gpu = 'no (CPU)' if s['gpu_used_for_asr'] is False else 'sí (CUDA)' if s['gpu_used_for_asr'] else 'no consta'
        lines.append(f"| {label} | {s['device'] or 'no consta'} | {s['precision'] or 'no consta'} | {gpu} | {fmt(s.get('real_time_factor_full_audio'))} | {fmt(s.get('inference_max_seconds'))} | {s['resources_status']} |")
        if s.get('resources'):
            r = s['resources']
            h = r['hardware']
            peak = r.get('final_memory',{}).get('process_lifetime_peak_working_set_bytes')
            lines += ['', f"**{label}:** CPU {h.get('cpu_model')}; {h.get('logical_cpus')} procesadores lógicos; {h.get('os')}. CPU media del proceso: {fmt(r.get('cpu_average_percent_machine_capacity'))}% de capacidad lógica del equipo. Pico de RAM del proceso durante su vida: {fmt(peak/1024**2 if peak is not None else None)} MiB. Carga del modelo: {fmt(s.get('model_load_seconds'))} s.", '', r['notice'], '',
                      'Las muestras completas de RAM, uso de GPU, VRAM, potencia y temperatura disponibles están en el JSON de recursos. La potencia GPU global en vatios no equivale al consumo energético del ASR.']
            lines += ['', '| GPU global | Muestras | Uso medio / máx. (%) | VRAM máx. (MiB) | Potencia media / máx. (W) | Temperatura máx. (°C) |',
                      '|---|---:|---|---:|---|---:|']
            for gpu in s['gpu_global_sampled_statistics']:
                def value(field, stat):
                    return fmt(gpu[field][stat] if gpu[field] else None)
                lines.append(f"| {gpu['name']} | {gpu['sample_count']} | {value('utilization_percent','mean')} / {value('utilization_percent','maximum')} | {value('vram_used_mib','maximum')} | {value('power_watts','mean')} / {value('power_watts','maximum')} | {value('temperature_celsius','maximum')} |")
            if not s['gpu_global_sampled_statistics']:
                lines.append('| No disponible mediante NVIDIA | 0 | no medido | no medido | no medido | no medido |')
    lines += ['', 'Para comparar tablets habrá que medir en el dispositivo de destino: RAM máxima, tiempo de respuesta sostenido y consumo/batería. Este ordenador no permite deducir esos valores. No se cambia CPU por GPU automáticamente.']
    return '\n'.join(lines)+'\n'


def write_resource_report(folder, root):
    """Informe complementario: no modifica JSON originales ni sus huellas."""
    folder, root = Path(folder), Path(root)
    manifest = json.loads((folder/'resumen.json').read_text(encoding='utf-8'))
    entries = []
    for run in manifest.get('runs', []):
        if run.get('record_file'):
            source = folder/run['record_file']
        elif run.get('source_file'):
            source = Path(run['source_file'])
            if not source.is_absolute():
                source = root/source
        else:
            continue
        if source.is_file():
            data = json.loads(source.read_text(encoding='utf-8'))
            if 'device' in data:
                entries.append((source.name, data))
    if not entries:
        return 0
    try:
        from .archivos import write_text_atomic
    except ImportError:
        from archivos import write_text_atomic
    payload = {'notice': 'Complemento derivado de registros originales. No añade mediciones retrospectivas. GPU/CPU/RAM no instrumentadas se conservan como no medidas.',
               'records': [{'file': name, **compute_summary(data)} for name, data in entries]}
    write_text_atomic(folder/'recursos_computo.json', json.dumps(payload,ensure_ascii=False,indent=2)+'\n')
    section = compute_markdown(entries)
    write_text_atomic(folder/'recursos_computo.md', section)
    begin, end = '<!-- recursos-computo-inicio -->', '<!-- recursos-computo-fin -->'
    for name in ['resumen.md', 'evaluacion_humana.md']:
        path = folder/name
        if path.exists():
            text = path.read_text(encoding='utf-8')
            if begin in text:
                head, rest = text.split(begin,1)
                _, tail = rest.split(end,1)
                text = head.rstrip()+'\n\n'+begin+'\n'+section+end+tail
            else:
                text = text.rstrip()+'\n\n'+begin+'\n'+section+end+'\n'
            write_text_atomic(path,text)
    return len(entries)
