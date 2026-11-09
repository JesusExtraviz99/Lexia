"""Test conjunto con cola GPU y reutilización explícita de test anterior completo e idéntico."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
from datetime import datetime,timezone

if __package__ in (None,''):
    sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from scripts import lanzar_asr_paralelo as launcher
from scripts import evaluar_asr_externo as e
from scripts import motores_test_todos as motors
from scripts import ampliacion_motores as new


def read(path):return json.loads(path.read_text(encoding='utf-8'))


def is_alive(pid):
    if os.name != 'posix':return False
    try:os.kill(int(pid),0);return True
    except (ProcessLookupError,ValueError,TypeError):return False
    except PermissionError:return True


def reuse_legacy(motor,folder,legacy,selection,protocol):
    if motor in new.SPECS or not legacy.exists():return None
    base=legacy/motor
    progress=read(base/'progreso.json') if (base/'progreso.json').exists() else {}
    old=read(legacy/'cohorte.json') if (legacy/'cohorte.json').exists() else {}
    pidfile=legacy.with_name(legacy.name+'.pid')
    parent_alive=pidfile.exists() and is_alive(pidfile.read_text().strip())
    if progress.get('status')!='completed':
        if (progress.get('pid') and is_alive(progress['pid'])) or (old.get('status')=='running' and parent_alive):
            return 'wait'
        return None  # Intento anterior incompleto y detenido; la nueva ejecución se conserva aparte.
    manifest=read(base/'ejecucion.json');summary=read(base/'resumen.json')
    expected=protocol['models'][motor]
    for key,value in expected.items():
        if manifest.get(key)!=value:raise ValueError('Test previo con configuración distinta: '+motor+'/'+key)
    if manifest['selection']['items']!=selection or summary['completed']!=len(selection) or summary['failures']!=0:
        raise ValueError('Test previo sin la cobertura oficial completa: '+motor)
    config={k:v for k,v in manifest.items() if k not in ('created_at_utc','run_signature')}
    if e.signature(config)!=manifest['run_signature']:raise ValueError('Firma previa incoherente: '+motor)
    if {p.stem for p in (base/'audios').glob('*.json')}!={i['id'] for i in selection}:
        raise ValueError('Faltan resultados previos: '+motor)
    for item in selection:
        r=read(base/'audios'/(item['id']+'.json'))
        if r['status']!='ok' or r['run_signature']!=manifest['run_signature'] or any(r[k]!=v for k,v in item.items()):
            raise ValueError('Identidad/estado previo incoherente: '+motor+'/'+item['id'])
    shutil.copytree(base,folder/motor)
    return dict(motor=motor,gpu=manifest['gpu_physical_index'],pid=progress.get('pid'),status='completed',
                returncode=0,reused=True,reused_from=str(base),run_signature=manifest['run_signature'],
                notice='Resultados y recursos medidos en su ejecución original, no nueva inferencia de esta cohorte.')


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--gpus',type=int,nargs='+',required=True)
    parser.add_argument('--root-anteriores',type=Path,required=True)
    parser.add_argument('--root-nuevos',type=Path,required=True)
    parser.add_argument('--dataset',type=Path,required=True)
    parser.add_argument('--salida',type=Path,required=True)
    parser.add_argument('--plan',action='store_true')
    args=parser.parse_args()
    if not args.plan and sys.platform != 'linux':
        raise SystemExit('La ejecución se realiza en el servidor Linux; fuera de él solo se admite --plan.')
    root=Path(__file__).resolve().parents[1]
    order=['crisper','qwen_asr_17b','qwen_asr_06b','whisper_turbo','canary_v2','moonshine_small_es',
           'moonshine_tiny_es','granite_turboctc','parakeet','xlsr','whisper','vosk']
    roots={key:(args.root_nuevos if key in new.SPECS else args.root_anteriores).resolve() for key in order}
    for key in order:
        spec=motors.SPECS[key]
        spec['executable']=str(roots[key]/'.venvs'/('servidor-'+spec['profile'])/'bin/python')
        spec['folder']=str(roots[key]/'modelos'/spec['folder'])
    protocol=read(root/'entornos/test_todos/protocolo.json')
    # Comprobar que las fuentes delegadas son las mismas que las de dev.
    for name,digest in protocol['source_sha256'].items():
        if hashlib.sha256((root/name).read_bytes()).hexdigest()!=digest:
            raise ValueError('Fuente cambiada desde el protocolo: '+name)
    for key in order:
        if motors.parameters(key)!=protocol['models'][key]['parameters']:
            raise ValueError('Parámetros distintos de dev: '+key)
    if not args.plan:
        preparation=Path(str(args.salida.resolve())+'.preparacion.json')
        preparation.parent.mkdir(parents=True,exist_ok=True)
        def phase(value):
            launcher.write(preparation,dict(status=value,pid=os.getpid(),updated_at_utc=datetime.now(timezone.utc).isoformat()))
        phase('validando_entornos')
        version_cache={}
        for key in order:
            executable=motors.SPECS[key]['executable']
            expected=protocol['models'][key]['versions']
            cache_key=(executable,tuple(sorted(expected)))
            if cache_key not in version_cache:
                code='import json,sys,importlib.metadata; print(json.dumps({p:importlib.metadata.version(p) for p in json.loads(sys.argv[1])}))'
                version_cache[cache_key]=json.loads(subprocess.check_output(
                    [executable,'-c',code,json.dumps(sorted(expected))],env={**os.environ,'CUDA_VISIBLE_DEVICES':''},text=True))
            if version_cache[cache_key]!=expected:
                raise ValueError('Versiones distintas de dev: '+key)
        print('Configuraciones y dependencias fijadas comprobadas; verificando MLS test.',flush=True)
        phase('verificando_2385_audios_test')
        selection=e.select_mls(args.dataset.resolve(),'test',0,42)['items']
        if len(selection)!=2385:raise ValueError('Se esperaban 2385 audios test.')
        legacy=args.root_anteriores/'resultados/asr_externo/mls_test_completo_paralela_01'
        launcher.reuse_result=lambda motor,folder:reuse_legacy(motor,folder,legacy,selection,protocol)
        phase('preparando_cola_gpu')
    def command(motor,gpu,dataset,folder,cohort,limit,threads):
        cmd=[motors.SPECS[motor]['executable'],'-u',str(root/'scripts/evaluar_test_todos.py'),'evaluar',
             '--motor',motor,'--dataset',str(dataset),'--modelo',motors.SPECS[motor]['folder'],
             '--particion','test','--limite','0','--semilla','42','--hilos',str(threads),
             '--modo-ejecucion','concurrente','--cohorte',cohort,'--salida',str(folder/motor)]
        if gpu is not None:cmd+=['--gpu',str(gpu)]
        return cmd
    def environment(motor,gpu,threads):
        env=os.environ.copy();env.update(CUDA_VISIBLE_DEVICES=str(gpu) if gpu is not None else '',
            PYTHONHASHSEED='42',TOKENIZERS_PARALLELISM='false',HF_HUB_OFFLINE='1')
        for key in ['OMP_NUM_THREADS','MKL_NUM_THREADS','OPENBLAS_NUM_THREADS','NUMEXPR_NUM_THREADS']:env[key]=str(threads)
        if motor=='whisper':
            code='from pathlib import Path; import nvidia.cublas,nvidia.cudnn; print(":".join(str(Path(p.__path__[0])/"lib") for p in (nvidia.cublas,nvidia.cudnn)))'
            libs=subprocess.check_output([motors.SPECS[motor]['executable'],'-c',code],env=env,text=True).strip()
            env['LD_LIBRARY_PATH']=libs+(':'+env['LD_LIBRARY_PATH'] if env.get('LD_LIBRARY_PATH') else '')
        return env
    launcher.ROOT=root;launcher.motors=motors;launcher.job_command=command;launcher.environment=environment
    sys.argv=['test_todos','--dataset',str(args.dataset),'--salida',str(args.salida),'--gpus',*[str(n) for n in args.gpus],
              '--motores',*order,'--particion','test','--confirmar-test','--limite','0','--completo','--espera-maxima','43200']
    if args.plan:sys.argv.append('--plan')
    launcher.main()


if __name__=='__main__':main()
