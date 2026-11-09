"""Preparar MLS español dev/test para el servidor, sin train ni inferencias."""
import hashlib
import io
import json
from pathlib import Path
import tarfile
from datetime import datetime, timezone

import soundfile as sf

ROOT = Path(__file__).resolve().parents[1]


def digest(path):
    h = hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(4*1024*1024), b''):
            h.update(block)
    return h.hexdigest()


def keyed_lines(path, columns):
    result = {}
    for line in path.read_text(encoding='utf-8').splitlines():
        fields = line.split('\t')
        if len(fields) != columns or not fields[0] or fields[0] in result:
            raise ValueError(f'Fila incorrecta o repetida en {path}')
        result[fields[0]] = fields[1:]
    return result


def main():
    source = ROOT/'datos/externos/mls_es'
    destination = ROOT/'datos/externos/paquetes'
    destination.mkdir(exist_ok=True)
    archive = destination/'mls_es_dev_test.tar'
    manifest_file = destination/'mls_es_dev_test_manifest.json'
    checksum_file = destination/'mls_es_dev_test.tar.sha256'
    if any(p.exists() for p in (archive, manifest_file, checksum_file)):
        raise FileExistsError('Ya existe una salida de este paquete; no se sobrescribe.')
    manifest = dict(dataset='Multilingual LibriSpeech Spanish', source_url='https://www.openslr.org/94/',
        created_at_utc=datetime.now(timezone.utc).isoformat(), splits={}, files=[],
        scope='dev y test completos; train excluido; sin cambios en audios o transcripciones',
        verification='IDs audio/transcripción/segmentos; cabeceras FLAC; SHA256 por archivo y cotejo de bytes dentro del TAR. No decodificación completa ni revisión humana.',
        selection='Usar dev para desarrollo/configuración y reservar test para evaluación con configuración fijada. Auditar entrenamiento previo de cada modelo.',
        packaging_script_sha256=digest(Path(__file__)))
    selected = [source/name for name in ('LICENSE', 'README', 'metainfo.txt')]
    for split in ('dev', 'test'):
        folder = source/split
        transcripts = keyed_lines(folder/'transcripts.txt', 2)
        segments = keyed_lines(folder/'segments.txt', 4)
        audio = sorted((folder/'audio').rglob('*.flac'))
        ids = [p.stem for p in audio]
        if not audio or len(ids) != len(set(ids)) or set(ids) != set(transcripts) or set(ids) != set(segments):
            raise ValueError(f'Faltan o sobran audios/referencias en {split}.')
        seconds = 0
        for path in audio:
            info = sf.info(path)
            if info.frames <= 0 or info.samplerate != 16000 or info.channels != 1:
                raise ValueError(f'Cabecera inesperada: {path}')
            seconds += info.frames/info.samplerate
        files = sorted(p for p in folder.rglob('*') if p.is_file())
        selected.extend(files)
        manifest['splits'][split] = dict(audio_files=len(audio), files=len(files), duration_seconds=seconds,
            bytes=sum(p.stat().st_size for p in files))
        print(f'{split}: {len(audio)} audios, {seconds/3600:.2f} horas. Referencias completas.', flush=True)
    for path in selected:
        if path.is_symlink() or not path.is_file():
            raise ValueError(f'Archivo ausente o enlace no permitido: {path}')
        relative = path.relative_to(source).as_posix()
        if relative.startswith('train/'):
            raise ValueError('train no debe formar parte del paquete.')
        manifest['files'].append(dict(file='mls_es/'+relative, bytes=path.stat().st_size, sha256=digest(path)))
    payload = (json.dumps(manifest, ensure_ascii=False, indent=2)+'\n').encode('utf-8')
    manifest_file.write_bytes(payload)
    print('Creando TAR sin compresión…', flush=True)
    with tarfile.open(archive, 'w') as tar:
        for path, item in zip(selected, manifest['files']):
            tar.add(path, arcname=item['file'], recursive=False)
        info = tarfile.TarInfo('mls_es/PAQUETE_DEV_TEST.json')
        info.size = len(payload)
        tar.addfile(info, io.BytesIO(payload))
    expected = {item['file']: item for item in manifest['files']}
    seen = set()
    with tarfile.open(archive, 'r:') as tar:
        for member in tar:
            if not member.isfile() or member.name in seen:
                raise ValueError('Contenido inesperado o duplicado en TAR.')
            seen.add(member.name)
            h = hashlib.sha256()
            with tar.extractfile(member) as stream:
                for block in iter(lambda: stream.read(4*1024*1024), b''):
                    h.update(block)
            wanted = hashlib.sha256(payload).hexdigest() if member.name == 'mls_es/PAQUETE_DEV_TEST.json' else expected[member.name]['sha256']
            if h.hexdigest() != wanted:
                raise ValueError(f'Bytes distintos dentro de TAR: {member.name}')
    if seen != set(expected)|{'mls_es/PAQUETE_DEV_TEST.json'}:
        raise ValueError('Paquete incompleto.')
    sha = digest(archive)
    with checksum_file.open('w', encoding='ascii', newline='\n') as stream:
        stream.write(f'{sha}  {archive.name}\n')
    report = dict(dataset=manifest['dataset'], created_at_utc=manifest['created_at_utc'],
        archive=archive.relative_to(ROOT).as_posix(), bytes=archive.stat().st_size,
        sha256=sha, manifest_sha256=hashlib.sha256(payload).hexdigest(), splits=manifest['splits'],
        archive_members=len(seen), train_included=False, verification=manifest['verification'],
        status='empaquetado_y_verificado_localmente', upload_status='pendiente')
    report_folder = ROOT/'resultados/preparacion_datasets'
    report_folder.mkdir(exist_ok=True)
    (report_folder/'mls_dev_test_paquete.json').write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    print(json.dumps(report, ensure_ascii=False, indent=2), flush=True)


if __name__ == '__main__':
    main()
