"""Fija y descarga nuevos checkpoints oficiales; sin ejecutar modelos ni código de sus repositorios."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = {
    'moonshine_tiny_es': ('moonshine-ai/moonshine-streaming-tiny-es', 'asr'),
    'moonshine_small_es': ('moonshine-ai/moonshine-streaming-small-es', 'asr'),
    'granite_turboctc': ('ibm-granite/granite-speech-5.0-470m-turboctc', 'asr'),
    'qwen_asr_06b': ('Qwen/Qwen3-ASR-0.6B-hf', 'asr'),
    'qwen_asr_17b': ('Qwen/Qwen3-ASR-1.7B-hf', 'asr'),
    'canary_v2': ('nvidia/canary-1b-v2', 'asr'),
    'whisper_turbo': ('openai/whisper-large-v3-turbo', 'asr'),
    'crisper_medium': ('nyralabs/CrisperWhisper2.0_medium', 'literal_download_only'),
    'crisper_turbo': ('nyralabs/CrisperWhisper2.0_turbo', 'literal_download_only'),
    'crisper_large': ('nyralabs/CrisperWhisper2.0_large', 'literal_download_only'),
}
FOLDER = ROOT/'resultados/instalacion_asr/ampliacion_20261106'
PLAN = FOLDER/'checkpoints_fijados.json'


def sha(path):
    result = hashlib.sha256()
    with Path(path).open('rb') as stream:
        for block in iter(lambda: stream.read(1024*1024), b''):
            result.update(block)
    return result.hexdigest()


def save(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix('.json.tmp')
    tmp.write_bytes((json.dumps(data, ensure_ascii=False, indent=2)+'\n').encode('utf-8'))
    tmp.replace(path)


def plan():
    from huggingface_hub import HfApi
    previous = json.loads(PLAN.read_text(encoding='utf-8')) if PLAN.exists() else {'models': {}}
    api = HfApi()
    records = {}
    for key, (repo, purpose) in REGISTRY.items():
        if previous.get('data_schema') == 2 and previous['models'].get(key,{}).get('repo') == repo:
            records[key] = previous['models'][key]
            continue
        old = previous['models'].get(key,{})
        info = api.model_info(repo, revision=old.get('revision') if old.get('repo') == repo else None, files_metadata=True)
        files = []
        for item in info.siblings:
            name = item.rfilename
            relative = PurePosixPath(name)
            if len(relative.parts) != 1:
                continue
            # Solo pesos seguros y datos; no descargar/ejecutar Python ni pickles BIN.
            if relative.suffix not in ('.json','.txt','.md','.safetensors','.model','.spm','.jinja') and name not in ('LICENSE','NOTICE'):
                continue
            if not any(x.rfilename.endswith('.safetensors') and '/' not in x.rfilename for x in info.siblings):
                raise ValueError('Sin pesos safetensors raíz: '+repo)
            lfs = getattr(item,'lfs',None)
            expected = lfs.get('sha256') if isinstance(lfs,dict) else getattr(lfs,'sha256',None)
            files.append(dict(file=name,bytes=item.size,published_lfs_sha256=expected))
        record=dict(key=key,repo=repo,purpose=purpose,revision=info.sha,
                    license=(getattr(info.card_data,'license',None) if info.card_data else None),
                    license_name=(getattr(info.card_data,'license_name',None) if info.card_data else None),
                    folder='modelos/ampliacion_20261106/'+key,files=files)
        records[key]=record
        print('Fijado',key,info.sha,'bytes',sum(x['bytes'] or 0 for x in files),flush=True)
    for record in records.values():
        research = record['repo'].startswith('nyralabs/') and record.get('license_name') == 'nyra-health-non-commercial-research'
        if record['license'] not in ('apache-2.0','mit','cc-by-4.0','nyra-health-non-commercial-research') and not research:
            raise ValueError('Licencia no admitida: '+record['repo'])
    data=dict(data_schema=2,created_at_utc=datetime.now(timezone.utc).isoformat(), models=records,
              excluded=['Scribe','Speechmatics'],
              notice='Uso actual gratuito; Crisper permitido solo para investigación/no comercial con su licencia. Servicios descartados. No se ejecutan modelos literales.')
    save(PLAN,data)
    return data


def download(keys):
    os.environ['HF_HOME']=str(ROOT/'.tools/cache/hf-ampliacion-20261106')
    from huggingface_hub import snapshot_download
    data=plan()
    for key in keys:
        record=data['models'][key]
        destination=ROOT/record['folder']
        manifest=destination/'lexia_modelo_ampliacion.json'
        if manifest.exists():
            existing=json.loads(manifest.read_text(encoding='utf-8'))
            if existing['revision']!=record['revision']:
                raise ValueError('No sobrescribir checkpoint diferente')
            for item in existing['files']:
                if sha(destination/item['file'])!=item['sha256']:
                    raise ValueError('Archivo local modificado: '+item['file'])
            if {x['file'] for x in existing['files']} == {x['file'] for x in record['files']}:
                print('Ya verificado',key,flush=True)
                continue
        print('Descargando',key,flush=True)
        snapshot_download(record['repo'],revision=record['revision'],local_dir=destination,
                          allow_patterns=[x['file'] for x in record['files']],max_workers=2)
        checked=[]
        for item in record['files']:
            path=destination/item['file']; digest=sha(path)
            if item['bytes'] is not None and path.stat().st_size!=item['bytes']:
                raise ValueError('Tamaño distinto: '+str(path))
            if item['published_lfs_sha256'] and digest!=item['published_lfs_sha256']:
                raise ValueError('SHA256 LFS distinto: '+str(path))
            checked.append(dict(**item,sha256=digest))
        save(manifest,dict(**{k:v for k,v in record.items() if k!='files'},files=checked,
                           downloaded_at_utc=datetime.now(timezone.utc).isoformat(),status='downloaded_verified_not_executed'))
        save(FOLDER/(key+'_descarga.json'),json.loads(manifest.read_text(encoding='utf-8')))
        print('Descarga verificada',key,flush=True)


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('action',choices=['plan','descargar'])
    p.add_argument('--modelos',choices=list(REGISTRY),nargs='+',default=list(REGISTRY))
    a=p.parse_args()
    if a.action=='plan': plan()
    else: download(a.modelos)
