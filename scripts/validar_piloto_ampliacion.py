"""Comprueba el piloto guardado antes de autorizar dev completo; sin ASR ni cambios de archivos."""
import argparse
import hashlib
import json
from pathlib import Path

from scripts.ampliacion_motores import KEYS


def read(path):
    return json.loads(path.read_text(encoding='utf-8'))


def validate(folder):
    folder=Path(folder)
    cohort=read(folder/'cohorte.json')
    jobs=cohort['jobs']
    if cohort['status']!='completed' or {j['motor'] for j in jobs}!=set(KEYS) or len(jobs)!=len(KEYS):
        raise ValueError('El piloto no contiene los siete motores completos; revisar estados/logs.')
    identity=None
    caps=[]
    for job in jobs:
        key=job['motor'];base=folder/key
        if job['status']!='completed' or job['returncode']!=0:
            raise ValueError('Motor no completado: '+key)
        manifest=read(base/'ejecucion.json')
        config={k:v for k,v in manifest.items() if k not in ('created_at_utc','run_signature')}
        signature=hashlib.sha256(json.dumps(config,sort_keys=True,ensure_ascii=False).encode()).hexdigest()
        if signature!=manifest['run_signature']:
            raise ValueError('Firma incoherente: '+key)
        for name,field in [('ampliacion_motores.py','adapter_sha256'),('evaluar_asr_externo.py','script_sha256')]:
            current=hashlib.sha256((Path(__file__).parent/name).read_bytes()).hexdigest()
            if manifest[field]!=current:
                raise ValueError('Fuentes distintas de las del piloto: '+name)
        items=manifest['selection']['items']
        if len(items)!=10 or manifest['selection']['split']!='dev':
            raise ValueError('Piloto distinto de diez dev: '+key)
        if identity is None:identity=items
        elif identity!=items:raise ValueError('Audios/referencias distintos entre motores.')
        summary=read(base/'resumen.json')
        if summary['completed']!=10 or summary['failures']!=0:
            raise ValueError('Cobertura/fallos incorrectos: '+key)
        if {p.stem for p in (base/'audios').glob('*.json')}!={i['id'] for i in items}:
            raise ValueError('Faltan resultados por audio: '+key)
        for item in items:
            result=read(base/'audios'/(item['id']+'.json'))
            if result['status']!='ok' or result['run_signature']!=signature or any(result[k]!=v for k,v in item.items()):
                raise ValueError('Resultado/identidad incoherente: '+key+'/'+item['id'])
            if result.get('native_output',{}).get('generation_cap_reached'):
                caps.append(key+'/'+item['id'])
    if caps:
        raise ValueError('Indicador de límite de generación activado; revisar antes de ampliar: '+', '.join(caps))
    return dict(status='pilot_structure_verified',motors=len(jobs),selected=10,
                notice='Verificación estructural, no auditoría de métricas ni escucha; fuentes y resultados conservados.')


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('folder',type=Path)
    print(json.dumps(validate(parser.parse_args().folder),ensure_ascii=False,indent=2))
