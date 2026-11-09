"""Un clip público dev por ASR, secuencial CPU; literales expresamente excluidos."""
import argparse
import json
import os
from pathlib import Path
import subprocess
import sys

from scripts.ampliacion_motores import KEYS
from scripts.preparar_ampliacion_asr import FOLDER, ROOT, save


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--modelos',choices=KEYS,nargs='+',default=KEYS)
    parser.add_argument('--ronda',type=int,default=1)
    args=parser.parse_args()
    report=[]
    for key in args.modelos:
        output=FOLDER/('prueba_local_'+str(args.ronda))/key
        summary=output/'resumen.json'
        if summary.exists():
            result=json.loads(summary.read_text(encoding='utf-8'))
            report.append(dict(motor=key,status='completed' if result['completed']==1 and result['failures']==0 else 'error',summary=result))
            continue
        if output.exists():
            report.append(dict(motor=key,status='error_output_exists_review_required'))
            continue
        if not (ROOT/'modelos/ampliacion_20261106'/key/'lexia_modelo_ampliacion.json').exists():
            report.append(dict(motor=key,status='pending_download'))
            continue
        log=FOLDER/(key+'_prueba_local_r'+str(args.ronda)+'.log')
        command=[sys.executable,'-u','-m','scripts.evaluar_ampliacion_asr','evaluar','--motor',key,
            '--dataset',str(ROOT/'datos/externos/mls_es'),'--limite','1','--salida',str(output),
            '--modo-ejecucion','aislada','--hilos','4']
        env=os.environ.copy();env.update(HF_HUB_OFFLINE='1',CUDA_VISIBLE_DEVICES='',TOKENIZERS_PARALLELISM='false')
        print('Probando CPU, un clip público:',key,flush=True)
        try:
            with log.open('wb') as stream:
                result=subprocess.run(command,cwd=ROOT,env=env,stdout=stream,stderr=subprocess.STDOUT,timeout=600)
            row=dict(motor=key,status='completed' if result.returncode==0 else 'error',returncode=result.returncode,log=log.relative_to(ROOT).as_posix())
            if summary.exists():row['summary']=json.loads(summary.read_text(encoding='utf-8'))
        except subprocess.TimeoutExpired:
            row=dict(motor=key,status='timeout_600s',log=log.relative_to(ROOT).as_posix())
        report.append(row)
        save(FOLDER/('pruebas_locales_estado_r'+str(args.ronda)+'.json'),dict(models=report,notice='CPU: 1 clip dev por ASR. No mide generalización/GPU/tablet; literales sin ejecutar.'))
        print(key,row['status'],flush=True)
        if row['status']!='completed':
            print(log.read_text(encoding='utf-8',errors='replace')[-4000:],flush=True)
    save(FOLDER/('pruebas_locales_estado_r'+str(args.ronda)+'.json'),dict(models=report,notice='CPU: 1 clip dev por ASR. No mide generalización/GPU/tablet; literales sin ejecutar.'))


if __name__=='__main__':main()
