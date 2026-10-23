"""Descarga un modelo público fijando revisión y huellas, fuera del entorno principal."""
import hashlib
import json
from pathlib import Path
from huggingface_hub import HfApi, snapshot_download

ROOT=Path(__file__).resolve().parents[1]


def main():
    repo='nyralabs/CrisperWhisper2.0_small'
    info=HfApi(token=False).model_info(repo)
    folder=ROOT/'modelos/crisperwhisper2-small'
    print('Repositorio:',repo,'Revisión:',info.sha,flush=True)
    snapshot_download(repo,revision=info.sha,token=False,local_dir=folder,
                      cache_dir=ROOT/'.tools/cache/hf-literal',max_workers=3,
                      allow_patterns=['*.json','*.txt','*.safetensors','LICENSE.md','README.md'])
    files=[]
    for path in sorted(folder.iterdir()):
        if not path.is_file():
            continue
        digest=hashlib.sha256()
        with path.open('rb') as stream:
            for chunk in iter(lambda:stream.read(1024*1024),b''):
                digest.update(chunk)
        files.append(dict(file=path.name,bytes=path.stat().st_size,sha256=digest.hexdigest()))
    config=json.loads((folder/'generation_config.json').read_text(encoding='utf-8'))
    languages=config.get('lang_to_id',{})
    print('Token español en configuración:', '<|es|>' in languages,flush=True)
    metadata=dict(repo=repo,revision=info.sha,files=files,spanish_language_token='<|es|>' in languages,
                  total_bytes=sum(f['bytes'] for f in files),license_source=str(folder/'LICENSE.md'))
    (ROOT/'.tools/modelo_literal_procedencia.json').write_text(json.dumps(metadata,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print('Modelo guardado:',folder,flush=True)


if __name__=='__main__':
    main()
