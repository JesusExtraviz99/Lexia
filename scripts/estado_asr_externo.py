"""Consulta progreso guardado sin modelos ni reconocimiento; compatible con Python 3.8."""
import argparse
import json
import os
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('folder', type=Path)
    args = parser.parse_args()
    path = args.folder/'cohorte.json'
    if not path.is_file():
        preparation = args.folder.with_name(args.folder.name+'.preparacion.json')
        if preparation.is_file():
            value = json.loads(preparation.read_text(encoding='utf-8'))
            if os.name != 'posix':
                print('Estado guardado de preparación:', value['status'], '|', value['updated_at_utc'])
                print('Consulta el proceso en el servidor Linux; no se comprueban PID remotos en Windows.')
                return
            try:
                os.kill(int(value['pid']), 0)
                print('Preparación:', value['status'], '|', value['updated_at_utc'])
                print('Aún no hay inferencias iniciadas. Consulta también su .lanzador.log.')
            except (ProcessLookupError, ValueError):
                print('La preparación terminó o falló antes de crear cohorte.json. Consulta su .lanzador.log.')
            return
        raise SystemExit('El lanzador aún no ha creado cohorte.json. Consulta su .lanzador.log.')
    cohort = json.loads(path.read_text(encoding='utf-8'))
    print('Cohorte:', cohort['cohort'], '| Estado:', cohort['status'])
    print('Motor       Dispositivo  Completados       Fallos  Estado / última actualización UTC')
    for job in cohort['jobs']:
        source = args.folder/job['motor']/'progreso.json'
        value = json.loads(source.read_text(encoding='utf-8')) if source.exists() else {}
        device = 'CPU' if job['gpu'] is None else 'GPU '+str(job['gpu'])
        progress = str(value.get('completed', 0))+'/'+str(value.get('selected', '?'))
        status = value.get('status', 'preparando')
        if job.get('reused'):
            status += ' (reutilizado; recursos de ejecución original)'
        if job.get('status') in ('error', 'terminated_by_launcher'):
            status = job['status']
        print('{:<11} {:<12} {:<17} {:<7} {} {}'.format(
            job['motor'], device, progress, value.get('failures', 0), status, value.get('updated_at_utc', '')))
    print('Pendientes de plaza:', cohort.get('pending', []))
    if cohort.get('error'):
        print('Error:', cohort['error'])


if __name__ == '__main__':
    main()
