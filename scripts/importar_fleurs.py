"""Copiar, extraer con rutas restringidas y verificar FLEURS español local."""
import argparse
import csv
from datetime import datetime, timezone
import gzip
import json
from pathlib import Path, PurePosixPath
import shutil
import tarfile

from scripts.archivos import write_text_atomic
from scripts.catalogo import ROOT
from scripts.comparar_literalidad import digest


def member_target(member, split, root):
    name=member.name
    parts=PurePosixPath(name).parts
    if (not parts or PurePosixPath(name).is_absolute() or '..' in parts
            or '\\' in name or ':' in name or parts[0]!=split):
        raise ValueError(f'Ruta de archivo no permitida: {name}')
    if not member.isdir() and not member.isfile():
        raise ValueError(f'Enlace/tipo no permitido: {name}')
    if member.isfile() and (len(parts)!=2 or not name.endswith('.wav') or member.size>100_000_000):
        raise ValueError(f'Miembro inesperado: {name}')
    target=root.joinpath(*parts).resolve()
    if not target.is_relative_to(root.resolve()):
        raise ValueError('La extracción saldría de su carpeta.')
    return target


def read_rows(path):
    rows=[];names=set()
    with path.open(encoding='utf-8-sig',newline='') as stream:
        for number,fields in enumerate(csv.reader(stream,delimiter='\t'),1):
            if len(fields)!=7:
                raise ValueError(f'{path.name}:{number}: se esperaban siete columnas.')
            filename=fields[1]
            if (not filename.endswith('.wav') or filename!=Path(filename).name
                    or '/' in filename or '\\' in filename or ':' in filename or filename in names):
                raise ValueError(f'Nombre duplicado/no válido: {filename}')
            samples=int(fields[5])
            if samples<=0 or not fields[2].strip() or not fields[3].strip():
                raise ValueError(f'Entrada vacía/no válida: {filename}')
            names.add(filename)
            rows.append(dict(sentence_id=fields[0],filename=filename,expected_samples=samples))
    if not rows:raise ValueError('Tabla sin registros.')
    return rows


def import_dataset(source):
    import numpy as np
    import soundfile as sf
    target=ROOT/'datos/externos/fleurs_es_419'
    if target.exists():
        raise FileExistsError(f'No se sobrescribe una importación existente: {target}')
    # Comprobar las seis entradas antes de escribir o extraer.
    expected=[f'{split}.{suffix}' for split in ['dev','test','train'] for suffix in ['tar.gz','tsv']]
    for name in expected:
        if not (source/name).is_file():raise FileNotFoundError(source/name)
    for split in ['dev','test','train']:read_rows(source/(split+'.tsv'))
    target.mkdir(parents=True)
    archives=target/'archivos';archives.mkdir()
    audio=target/'audio';audio.mkdir()
    (ROOT/'datos/externos/mls_es').mkdir(parents=True,exist_ok=True)
    report=dict(dataset='google/fleurs',subset='es_419',imported_date='2026-10-28',
        created_at_utc=datetime.now(timezone.utc).isoformat(),status='en_curso',
        source_url='https://huggingface.co/datasets/google/fleurs/tree/main/data/es_419',
        license='CC-BY-4.0',root=target.relative_to(ROOT).as_posix(),
        source_directory=str(source.resolve()),files=[],splits={},warnings=[],
        script_sha256=digest(Path(__file__)),asr_executed=False,
        notice='Comprobación técnica local completa; no certifica fidelidad literal de referencias, ausencia de solapamiento con entrenamiento ni calidad clínica. SHA256 locales, sin contrastar con hashes publicados por el proveedor. Se conservan particiones y originales comprimidos; no se selecciona ni reconoce una muestra.')
    (target/'fuente_importacion.txt').write_bytes(Path(__file__).read_bytes())
    status_file=target/'verificacion.json'
    try:
        for name in expected:
            src=source/name
            dst=archives/name if name.endswith('.tar.gz') else target/name
            shutil.copy2(src,dst)
            sha=digest(dst)
            if digest(src)!=sha:raise ValueError(f'Copia no idéntica: {name}')
            report['files'].append(dict(name=name,bytes=dst.stat().st_size,sha256=sha,file=dst.relative_to(ROOT).as_posix()))
            print('Copiado y verificado:',name,flush=True)
        index=[];sha_splits={};filename_splits={};id_splits={}
        for split in ['dev','test','train']:
            rows=read_rows(target/(split+'.tsv'))
            extracted=0;unpacked_bytes=0
            # gzip, además del tar, se consume hasta EOF para verificar su CRC/tráiler.
            with gzip.open(archives/(split+'.tar.gz'),'rb') as zipped:
                with tarfile.open(fileobj=zipped,mode='r|') as tar:
                    for member in tar:
                        dst=member_target(member,split,audio)
                        if member.isdir():dst.mkdir(parents=True,exist_ok=True);continue
                        unpacked_bytes+=member.size
                        if unpacked_bytes>20_000_000_000:raise ValueError('Tamaño inesperado de extracción.')
                        dst.parent.mkdir(parents=True,exist_ok=True)
                        with tar.extractfile(member) as incoming,dst.open('xb') as outgoing:
                            shutil.copyfileobj(incoming,outgoing)
                        if dst.stat().st_size!=member.size:raise ValueError(f'Extracción incompleta: {dst.name}')
                        extracted+=1
                while zipped.read(1024*1024):pass
            actual={p.name for p in (audio/split).iterdir() if p.is_file()}
            wanted={r['filename'] for r in rows}
            if actual!=wanted:
                raise ValueError(f'{split}: faltan {len(wanted-actual)} audios y sobran {len(actual-wanted)}.')
            print(split,'extraído; verificando',len(rows),'WAV completos',flush=True)
            seconds=0;subtypes=set();zero=[];peaks=[]
            for number,row in enumerate(rows,1):
                path=audio/split/row['filename']
                frames=0;peak=0.0;energy=0.0
                with sf.SoundFile(path) as wav:
                    if wav.samplerate!=16000 or wav.channels!=1 or wav.frames!=row['expected_samples']:
                        raise ValueError(f'Audio incompatible con TSV/16 kHz mono: {path.name}')
                    subtypes.add(wav.subtype)
                    for block in wav.blocks(blocksize=65536,dtype='float32'):
                        if not np.isfinite(block).all():raise ValueError(f'Muestras no finitas: {path.name}')
                        frames+=len(block);peak=max(peak,float(np.max(np.abs(block))))
                        energy+=float(np.sum(block.astype(np.float64)**2))
                    if frames!=wav.frames:raise ValueError(f'Decodificación incompleta: {path.name}')
                if peak==0:zero.append(row['filename'])
                sha=digest(path);sha_splits.setdefault(sha,set()).add(split)
                filename_splits.setdefault(row['filename'],set()).add(split)
                id_splits.setdefault(row['sentence_id'],set()).add(split)
                seconds+=frames/16000;peaks.append(peak)
                index.append(dict(split=split,**row,audio_file=path.relative_to(ROOT).as_posix(),
                                  sha256=sha,decoded_frames=frames,peak_abs=peak,rms=(energy/frames)**.5))
                if number%500==0:print(split,number,'/',len(rows),'verificados',flush=True)
            report['splits'][split]=dict(rows=len(rows),audio_files=extracted,audio_seconds=seconds,
                sample_rate_hz=16000,channels=1,subtypes=sorted(subtypes),
                gzip_crc_verified=True,all_audio_fully_decoded=True,
                missing_audio=0,extra_audio=0,silent_files=zero,max_peak_abs=max(peaks))
            if zero:report['warnings'].append(f'{split}: {len(zero)} archivos de amplitud nula.')
            print(split,'completo:',len(rows),'audios,',round(seconds/3600,3),'horas',flush=True)
            write_text_atomic(status_file,json.dumps(report,ensure_ascii=False,indent=2)+'\n')
        report['cross_split']=dict(identical_audio_sha256=sum(len(v)>1 for v in sha_splits.values()),
            shared_filenames=sum(len(v)>1 for v in filename_splits.values()),
            shared_sentence_ids=sum(len(v)>1 for v in id_splits.values()),
            notice='IDs de frase pueden repetirse entre lecturas; no equivalen a identidad de audio/hablante. Conservar particiones oficiales; no auditar independencia de entrenamiento a partir de esta comprobación.')
        if report['cross_split']['identical_audio_sha256']:
            report['warnings'].append('Hay audios idénticos entre particiones; revisar antes de evaluar.')
        write_text_atomic(target/'indice_audio.json',json.dumps(index,ensure_ascii=False,indent=2)+'\n')
        report['audio_index_sha256']=digest(target/'indice_audio.json')
        report['total_audio_files']=len(index)
        report['total_audio_seconds']=sum(s['audio_seconds'] for s in report['splits'].values())
        report['status']='completo'
    except BaseException as exc:
        report['status']='error';report['error']=str(exc)
        raise
    finally:
        write_text_atomic(status_file,json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    write_text_atomic(ROOT/'datos/externos/fleurs_es_419_verificacion.json',json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print('Importación verificada:',status_file,flush=True)


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--origen',type=Path,required=True)
    args=parser.parse_args();import_dataset(args.origen.resolve())
