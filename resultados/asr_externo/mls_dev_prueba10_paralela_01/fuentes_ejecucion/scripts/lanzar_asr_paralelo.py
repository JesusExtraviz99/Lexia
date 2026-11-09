"""Lanza una prueba corta por motor en GPU explícitas; Vosk en CPU. Sin sudo/SSH.

Usar después de preparar entornos y pesos. Mantener esta terminal abierta.
No mata procesos ajenos ni elige tarjetas fuera de --gpus.
"""
import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import signal
import subprocess
import sys
import time

try:
    from . import asr_motores_externos as motors
except ImportError:
    import asr_motores_externos as motors

ROOT = Path(__file__).resolve().parents[1]


def write(path, value):
    temp = path.with_suffix('.tmp')
    temp.write_text(json.dumps(value, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    temp.replace(path)


def timestamp():
    return datetime.now(timezone.utc).isoformat()


def is_free(gpu):
    result = subprocess.run(['nvidia-smi', '-i', str(gpu), '--query-compute-apps=pid',
        '--format=csv,noheader,nounits'], text=True, capture_output=True, timeout=5)
    if result.returncode:
        raise RuntimeError(f'No se puede comprobar GPU {gpu}: {result.stderr.strip()}')
    return not any(line.strip().isdigit() for line in result.stdout.splitlines())


def job_command(motor, gpu, dataset, folder, cohort, limit, threads):
    executable = ROOT/'.venvs'/('servidor-'+motors.SPECS[motor]['profile'])/'bin/python'
    args = [str(executable), '-u', str(ROOT/'scripts/evaluar_asr_externo.py'), 'evaluar',
        '--motor', motor, '--dataset', str(dataset), '--particion', 'dev', '--limite', str(limit),
        '--semilla', '42', '--hilos', str(threads), '--modo-ejecucion', 'concurrente',
        '--cohorte', cohort, '--salida', str(folder/motor)]
    if gpu is not None:
        args += ['--gpu', str(gpu)]
    return args


def environment(motor, gpu, threads):
    env = os.environ.copy()
    env.update(CUDA_VISIBLE_DEVICES=str(gpu) if gpu is not None else '', PYTHONHASHSEED='42',
               TOKENIZERS_PARALLELISM='false', HF_HUB_OFFLINE='1')
    for key in ['OMP_NUM_THREADS', 'MKL_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'NUMEXPR_NUM_THREADS']:
        env[key] = str(threads)
    if motor == 'whisper':
        executable = ROOT/'.venvs/servidor-whisper/bin/python'
        query = ('from pathlib import Path; import nvidia.cublas,nvidia.cudnn; '
                 'print(":".join(str(Path(p.__path__[0])/"lib") for p in (nvidia.cublas,nvidia.cudnn)))')
        libs = subprocess.check_output([str(executable), '-c', query], env=env, text=True).strip()
        env['LD_LIBRARY_PATH'] = libs+(':'+env['LD_LIBRARY_PATH'] if env.get('LD_LIBRARY_PATH') else '')
    return env


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--dataset', type=Path, required=True)
    parser.add_argument('--gpus', type=int, nargs='+', required=True, help='Solo GPU que os han permitido usar.')
    parser.add_argument('--motores', choices=list(motors.SPECS), nargs='+', default=list(motors.SPECS))
    parser.add_argument('--limite', type=int, default=10)
    parser.add_argument('--hilos', type=int, default=4)
    parser.add_argument('--espera-maxima', type=int, default=1800, help='Segundos máximos esperando plazas ocupadas por otros.')
    parser.add_argument('--salida', type=Path, required=True, help='Carpeta nueva, un subdirectorio por motor.')
    parser.add_argument('--plan', action='store_true', help='Mostrar plan sin ejecutar ni consultar GPU.')
    args = parser.parse_args()
    if (len(set(args.gpus)) != len(args.gpus) or min(args.gpus) < 0 or
            len(set(args.motores)) != len(args.motores) or not 1 <= args.limite <= 100 or args.hilos < 1):
        parser.error('GPU y motores únicos; GPU no negativas; límite de prueba 1–100; hilos positivos.')
    folder = args.salida.resolve()
    dataset = args.dataset.resolve()
    cohort = folder.name
    if args.plan:
        print(json.dumps(dict(gpus=args.gpus, motors=args.motores, audio_count=args.limite,
                              selection_seed=42, dataset=str(dataset), output=str(folder),
                              notice='Un proceso por GPU disponible de la lista; Vosk CPU. Mismos IDs; no inicia tareas.'), indent=2))
        return
    if sys.platform != 'linux':
        raise RuntimeError('Lanzador preparado para los entornos Linux del servidor.')
    if folder.exists():
        raise FileExistsError('Usar carpeta nueva; no sobrescribir ni mezclar una cohorte anterior.')
    for motor in args.motores:
        executable = ROOT/'.venvs'/('servidor-'+motors.SPECS[motor]['profile'])/'bin/python'
        model = ROOT/'modelos'/motors.SPECS[motor]['folder']/'lexia_modelo.json'
        if not executable.is_file() or not model.is_file():
            raise FileNotFoundError(f'Falta entorno/modelo: {motor}; preparar antes de lanzar.')
    # Validar todos los índices explícitos antes de crear la cohorte.
    for gpu in args.gpus:
        is_free(gpu)
    folder.mkdir(parents=True)
    state = dict(started_at_utc=timestamp(), mode='concurrente', dataset=str(dataset),
        cohort=cohort, gpu_indices_authorized=args.gpus, limit=args.limite, seed=42,
        status='running', jobs=[],
        notice='Comparación concurrente: CPU/RAM/disco compartidos; no equivale a tiempos aislados. No se reservan GPU atómicamente frente a otros usuarios.')
    pending = list(args.motores)
    running = []
    last_progress = time.monotonic()
    waiting_since = time.monotonic()
    def start(motor, gpu):
        command = job_command(motor, gpu, dataset, folder, cohort, args.limite, args.hilos)
        env = environment(motor, gpu, args.hilos)
        log = (folder/(motor+'.log')).open('xb')
        try:
            process = subprocess.Popen(command, cwd=ROOT, env=env, stdout=log, stderr=subprocess.STDOUT,
                                       start_new_session=True)
        except BaseException:
            log.close()
            raise
        record = dict(motor=motor, gpu=gpu, pid=process.pid, command=command,
                      started_at_utc=timestamp(), status='running', log=motor+'.log')
        state['jobs'].append(record)
        running.append((process, log, record))
        print(f'Iniciado {motor}: GPU {gpu}' if gpu is not None else f'Iniciado {motor}: CPU', flush=True)
    try:
        while pending or running:
            for item in running[:]:
                process, log, record = item
                code = process.poll()
                if code is not None:
                    record.update(returncode=code, finished_at_utc=timestamp(),
                                  status='completed' if code == 0 else 'error')
                    log.close()
                    running.remove(item)
                    print(f"Terminado {record['motor']}: código {code}", flush=True)
                    waiting_since = time.monotonic()
            if 'vosk' in pending:
                start('vosk', None)
                pending.remove('vosk')
            used = {record['gpu'] for _, _, record in running if record['gpu'] is not None}
            for gpu in args.gpus:
                if pending and gpu not in used and is_free(gpu):
                    motor = pending[0]
                    start(motor, gpu)
                    pending.remove(motor)
                    waiting_since = time.monotonic()
            state['pending'] = pending[:]
            write(folder/'cohorte.json', state)
            if pending and not running and time.monotonic()-waiting_since > args.espera_maxima:
                raise TimeoutError('GPU solicitadas ocupadas; se conserva la cohorte sin ejecutar esos pendientes.')
            if time.monotonic()-last_progress > 30:
                print(f'Activos: {[r[2]["motor"] for r in running]}; pendientes: {pending}', flush=True)
                last_progress = time.monotonic()
            if pending or running:
                time.sleep(1)
        # Verificar igualdad de selección y reportar resultados sin inventar métricas ausentes.
        selected = None
        results = []
        for job in state['jobs']:
            manifest_path = folder/job['motor']/'ejecucion.json'
            summary_path = folder/job['motor']/'resumen.json'
            if manifest_path.exists():
                manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
                identity = [(r['id'], r['sha256'], r['reference']) for r in manifest['selection']['items']]
                if selected is None:
                    selected = identity
                elif identity != selected:
                    raise ValueError('Las selecciones de audio/referencia difieren entre motores.')
            results.append(dict(motor=job['motor'], gpu=job['gpu'], status=job['status'],
                summary=json.loads(summary_path.read_text(encoding='utf-8')) if summary_path.exists() else None))
        save_status = 'completed' if all(j['status'] == 'completed' for j in state['jobs']) else 'error'
        state.update(status=save_status, finished_at_utc=timestamp(), selection_equal=selected is not None,
                     results=results)
        write(folder/'cohorte.json', state)
        print('Resultados y registros:', folder, flush=True)
        if save_status != 'completed':
            raise RuntimeError('Algún motor falló; revisar sus .log. No hay sustitución automática de GPU/CPU.')
    except BaseException as exc:
        state.update(status='interrupted' if isinstance(exc, KeyboardInterrupt) else 'error',
                     error=f'{type(exc).__name__}: {exc}', finished_at_utc=timestamp())
        # Únicamente procesos hijos creados por este lanzamiento; nunca trabajos ajenos.
        for process, log, record in running:
            if process.poll() is None:
                # Dar al evaluador ocasión de guardar su finally antes de terminarlo.
                process.send_signal(signal.SIGINT)
                try:
                    process.wait(timeout=20)
                except subprocess.TimeoutExpired:
                    process.terminate()
                    try:
                        process.wait(timeout=10)
                    except subprocess.TimeoutExpired:
                        process.kill()
                        process.wait()
                record.update(status='terminated_by_launcher', returncode=process.returncode,
                              finished_at_utc=timestamp())
            log.close()
        write(folder/'cohorte.json', state)
        raise


if __name__ == '__main__':
    main()
