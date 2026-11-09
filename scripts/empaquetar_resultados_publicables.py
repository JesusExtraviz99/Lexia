"""Respalda resultados textuales completos por cohorte y verifica cada miembro del TAR."""
import gzip
import hashlib
import io
import json
from pathlib import Path
import tarfile

ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'resultados/asr_externo'
OUTPUT=BASE/'archivos'
ALLOWED={'.json','.jsonl','.csv','.md','.txt','.log','.tsv','.sha256','.py'}


def digest(path):
    sha=hashlib.sha256()
    with path.open('rb') as source:
        for block in iter(lambda:source.read(1024*1024),b''):sha.update(block)
    return sha.hexdigest()


def main():
    OUTPUT.mkdir(exist_ok=True)
    rows=[]
    for folder in sorted(BASE.glob('mls_*')):
        if not folder.is_dir():continue
        files=sorted(p for p in folder.rglob('*') if p.is_file())
        if any(p.is_symlink() or p.suffix.lower() not in ALLOWED for p in files):
            raise ValueError('Miembro inesperado; revisar antes de publicar: '+str(folder))
        archive=OUTPUT/(folder.name+'.tar.gz')
        members={p.relative_to(folder).as_posix():dict(bytes=p.stat().st_size,sha256=digest(p)) for p in files}
        index=json.dumps(dict(cohort=folder.name,files=members),ensure_ascii=False,indent=2).encode('utf-8')
        # Reanudar solo comprobando íntegramente el paquete existente; nunca sobrescribirlo.
        if not archive.exists():
            with archive.open('wb') as dest,gzip.GzipFile(fileobj=dest,mode='wb',filename='',mtime=0,compresslevel=5) as compressed:
                with tarfile.open(fileobj=compressed,mode='w') as package:
                    for file in files:package.add(file,arcname=folder.name+'/'+file.relative_to(folder).as_posix(),recursive=False)
                    info=tarfile.TarInfo(folder.name+'/PUBLICACION_SHA256.json');info.size=len(index)
                    package.addfile(info,io.BytesIO(index))
        checked=0
        with tarfile.open(archive,'r:gz') as package:
            for member in package:
                if not member.isfile():raise ValueError('Miembro que no es archivo')
                relative=Path(member.name).relative_to(folder.name).as_posix()
                with package.extractfile(member) as source:
                    sha=hashlib.sha256();size=0
                    for block in iter(lambda:source.read(1024*1024),b''):sha.update(block);size+=len(block)
                if relative=='PUBLICACION_SHA256.json':
                    assert sha.hexdigest()==hashlib.sha256(index).hexdigest()
                else:
                    assert members[relative]==dict(bytes=size,sha256=sha.hexdigest()),relative
                    checked+=1
        assert checked==len(files)
        if archive.stat().st_size>=95*1024*1024:raise ValueError('Paquete demasiado grande para este plan de publicación')
        row=dict(cohort=folder.name,archive=archive.name,sha256=digest(archive),files=checked,
                 bytes_uncompressed=sum(v['bytes'] for v in members.values()),bytes_compressed=archive.stat().st_size,
                 all_members_verified=True,audio_included=False)
        rows.append(row)
        Path(str(archive)+'.sha256').write_text(row['sha256']+'  '+archive.name+'\n',encoding='utf-8',newline='\n')
        print(folder.name,checked,round(row['bytes_compressed']/1024**2,2),'MiB',flush=True)
    (OUTPUT/'indice.json').write_text(json.dumps(dict(packages=rows,scope='Resultados textuales; sin voces, modelos ni datasets de audio'),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')


if __name__=='__main__':main()
