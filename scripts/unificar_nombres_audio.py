"""Unificar nombres reales de WAV con respaldo de catálogo y aliases históricos."""
import argparse
from copy import deepcopy
from datetime import datetime
import hashlib
import json
from pathlib import Path
import re

from scripts.archivos import write_text_atomic
from scripts.catalogo import ROOT, read_catalog, descriptive_name, catalog_path


def reader_id(value):
    match = re.fullmatch(r'(?:adulto|lector)_(\d+)', value or '')
    if not match:
        raise ValueError(f'Identificador de lector no reconocido: {value!r}')
    return f'lector_{int(match[1]):02d}'


def description(row):
    # Partir del nombre existente conserva las consignas particulares.
    value = Path(row['audio_file']).stem
    value = re.sub(r' - \d{2}-\d{2}-\d{4}(?: - .*)?$', '', value)
    value = re.sub(r'^(?:Biblioteca|Tren|Limite) \d+ - ', '', value, flags=re.I)
    value = re.sub(r' - lectura_\d+$', '', value)
    value = re.sub(r' - (?:cuento [12]|caja del sendero)$', '', value, flags=re.I)
    value = re.sub(r' - cuento [12]$', '', value, flags=re.I)
    return value[0].upper() + value[1:]


def plan_names(root=ROOT):
    original = read_catalog(root)
    updated = deepcopy(original)
    rows = updated['recordings']
    hashes = {p.resolve(): hashlib.sha256(p.read_bytes()).hexdigest()
              for p in (root/'datos/audio').glob('*.wav')}
    matched = set()
    changes = []
    targets = set()
    for row in rows:
        source = (root/row['audio_file']).resolve()
        if hashes.get(source) != row['audio_sha256']:
            if row.get('availability_status') == 'historico_sin_wav_coincidente':
                continue
            # Otra toma con ese nombre no sustituye la grabación histórica.
            if source in hashes and any(other['audio_sha256'] == hashes[source]
                    and (root/other['audio_file']).resolve() == source for other in rows):
                row['availability_status'] = 'historico_sin_wav_coincidente'
                continue
            raise ValueError(f'Audio ausente o alterado sin otra toma identificada: {source}')
        if source in matched:
            raise ValueError(f'Dos entradas identifican el mismo WAV: {source}')
        matched.add(source)
        speaker = reader_id(row['speaker_id'])
        label = description(row)
        title = f'{label} - {Path(row["story_file"]).stem}'
        target = source.with_name(descriptive_name(title, row['recorded_date'], speaker))
        if target in targets or (target.exists() and target != source):
            stamp = row['id'].removeprefix('lectura_')
            target = target.with_name(f'{target.stem} - {stamp}.wav')
        if target in targets or (target.exists() and target != source):
            raise ValueError(f'Nombre de destino ocupado: {target}')
        if target.parent != (root/'datos/audio').resolve():
            raise ValueError('Destino fuera de datos/audio.')
        targets.add(target)
        if source != target:
            previous = row['audio_file']
            row['legacy_audio_files'] = list(dict.fromkeys([*row.get('legacy_audio_files', []), previous]))
            row['audio_file'] = target.relative_to(root.resolve()).as_posix()
        if speaker != row['speaker_id']:
            row['legacy_speaker_ids'] = list(dict.fromkeys([*row.get('legacy_speaker_ids', []), row['speaker_id']]))
            row['speaker_id'] = speaker
        row['label'] = f'{title} - {row["recorded_date"][8:10]}-{row["recorded_date"][5:7]}-{row["recorded_date"][:4]} - {speaker}'
        changes.append((source, target, row['audio_sha256']))
    if set(hashes) != matched:
        raise ValueError(f'WAV sin catalogar: {set(hashes)-matched}')
    return original, updated, changes


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--aplicar', action='store_true')
    args = parser.parse_args()
    original, updated, changes = plan_names()
    for source, target, _ in changes:
        if source != target:
            print(source.name + '\n  -> ' + target.name)
    print(f'{len(changes)} WAV identificados; {sum(a != b for a,b,_ in changes)} cambios de nombre.')
    if not args.aplicar:
        print('Vista previa. Usa --aplicar para renombrar.')
        return
    backup = ROOT/'.descartados'/f'nombres_audio_{datetime.now():%Y%m%d_%H%M%S_%f}'
    backup.mkdir(parents=True)
    catalog_file = catalog_path()
    (backup/'catalogo_anterior.json').write_bytes(catalog_file.read_bytes())
    (backup/'cambios.json').write_text(json.dumps([
        {'antes': str(a), 'despues': str(b), 'sha256': h} for a,b,h in changes], ensure_ascii=False, indent=2), encoding='utf-8')
    moved = []
    try:
        for source, target, expected in changes:
            if hashlib.sha256(source.read_bytes()).hexdigest() != expected:
                raise ValueError(f'El WAV cambió desde la comprobación: {source}')
            if source != target:
                if target.exists():
                    raise FileExistsError(target)
                source.rename(target)
                moved.append((source,target))
        write_text_atomic(catalog_file, json.dumps(updated, ensure_ascii=False, indent=2)+'\n')
    except Exception:
        for source,target in reversed(moved):
            target.rename(source)
        raise
    for _,target,expected in changes:
        if hashlib.sha256(target.read_bytes()).hexdigest() != expected:
            raise ValueError(f'Fallo de integridad tras renombrar: {target}')
    print('Catálogo actualizado; contenido de todos los WAV idéntico. Respaldo:', backup)


if __name__ == '__main__':
    main()
