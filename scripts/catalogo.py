"""Identidad estable y nombres legibles para las grabaciones de Lexia."""
import argparse
import hashlib
import json
import re
from pathlib import Path
import wave

try:
    from .archivos import write_text_atomic
except ImportError:
    from archivos import write_text_atomic

ROOT = Path(__file__).resolve().parents[1]


def catalog_path(root=ROOT):
    private = root/'datos/referencias/catalogo_local.json'
    return private if private.exists() else root/'datos/referencias/catalogo.json'


def read_catalog(root=ROOT):
    path = catalog_path(root)
    return json.loads(path.read_text(encoding='utf-8')) if path.exists() else {'schema_version': 2, 'recordings': []}


def audio_identity(audio, root=ROOT):
    name = Path(audio).name
    matches = [r for r in read_catalog(root)['recordings'] if name in audio_names(r)]
    if len(matches) > 1:
        matches = [r for r in matches if (root/r['audio_file']).is_file()
                   and hashlib.sha256((root/r['audio_file']).read_bytes()).hexdigest() == r.get('audio_sha256')]
    if len(matches) != 1:
        return {'id': None, 'label': f'Sin clasificar · {name}'}
    row = matches[0]
    return {key: row.get(key) for key in ['id', 'label', 'case', 'recorded_date', 'story_file', 'speaker_id', 'partition']}


def audio_names(row):
    return {Path(p).name for p in [row['audio_file'], *row.get('legacy_audio_files', [])]}


def resolve_audio_path(audio, root=ROOT):
    """Resolver referencias históricas sin reescribir los resultados originales."""
    audio = Path(audio)
    matches = [r for r in read_catalog(root)['recordings'] if audio.name in audio_names(r)]
    if len(matches) > 1:
        matches = [r for r in matches if (root/r['audio_file']).is_file()
                   and hashlib.sha256((root/r['audio_file']).read_bytes()).hexdigest() == r.get('audio_sha256')]
    if len(matches) == 1:
        target = root / matches[0]['audio_file']
        expected = matches[0].get('audio_sha256')
        if target.is_file() and expected and hashlib.sha256(target.read_bytes()).hexdigest() != expected:
            raise ValueError(f'El contenido del WAV no coincide con la referencia: {audio}')
        return target
    return audio if audio.is_absolute() else root / audio


def same_audio(first, second, root=ROOT):
    if Path(first).name == Path(second).name:
        return True
    return resolve_audio_path(first, root).resolve() == resolve_audio_path(second, root).resolve()


def report_stem(audio, root=ROOT):
    # Los nombres descriptivos largos no deben superar MAX_PATH en los informes.
    return audio_identity(audio, root).get('id') or Path(audio).stem[:70]


def descriptive_name(label, date, speaker=None):
    clean = re.sub(r'[<>:"/\\|?*\x00-\x1f]', '-', label).strip(' .')[:105]
    reader = re.sub(r'[<>:"/\\|?*\x00-\x1f]', '-', speaker or '').strip(' .')[:32]
    suffix = f' - {reader}' if reader else ''
    return f'{clean or "Lectura sin clasificar"} - {date[8:10]}-{date[5:7]}-{date[:4]}{suffix}.wav'


def register_recording(audio, story, label=None, case='sin_clasificar', speaker=None, environment=None, root=ROOT):
    """Registrar la consigna/metadatos; nunca dar por validado lo que se leyó."""
    reader_match = re.fullmatch(r'(?:lector|adulto)_(\d+)', speaker or '')
    if reader_match:
        speaker = f'lector_{int(reader_match[1]):02d}'
    catalog = read_catalog(root)
    relative = audio.resolve().relative_to(root.resolve()).as_posix()
    if any(audio.name in audio_names(r) for r in catalog['recordings']):
        return audio_identity(audio, root)
    stamp = audio.stem.split('_')[1]
    date = f'{stamp[:4]}-{stamp[4:6]}-{stamp[6:8]}'
    day = f'{stamp[6:8]}/{stamp[4:6]}/{stamp[:4]}'
    with wave.open(str(audio), 'rb') as wav:
        row = {'id': audio.stem, 'audio_file': relative,
               'audio_sha256': hashlib.sha256(audio.read_bytes()).hexdigest(),
               'label': f'{label or "Lectura sin clasificar"} · {day}' + (f' · {speaker}' if speaker else ''), 'case': case,
               'recorded_date': date, 'story_file': story.resolve().relative_to(root.resolve()).as_posix(),
               'story_sha256': hashlib.sha256(story.read_bytes()).hexdigest(),
               'speaker_id': speaker, 'partition': 'sin_asignar',
               'reference_status': 'pendiente_revision_usuario', 'reference_file': None,
               'reading_events': [], 'environment_notes': environment,
               'sample_rate_hz': wav.getframerate(), 'channels': wav.getnchannels(),
               'sample_width_bytes': wav.getsampwidth(), 'frames': wav.getnframes(),
               'duration_seconds': wav.getnframes()/wav.getframerate(),
               'notice': 'Nombre/caso describen la consigna, no validan contenido ni eventos. No es conjunto de prueba reservado por defecto.'}
    description = label or {'normal': 'Lectura normal', 'lenta': 'Lectura lenta',
                            'pausa': 'Lectura con pausa', 'relectura': 'Lectura con relectura',
                            'disfluencias': 'Lectura con disfluencias'}.get(case, 'Lectura sin clasificar')
    target = audio.with_name(descriptive_name(f'{description} - {story.stem}', date, speaker))
    if target.exists():
        target = target.with_name(f'{target.stem} - {audio.stem.split("_", 2)[-1]}.wav')
    if target.exists():
        raise FileExistsError(target)
    row['legacy_audio_files'] = [relative]
    row['audio_file'] = target.resolve().relative_to(root.resolve()).as_posix()
    catalog['recordings'].append(row)
    audio.rename(target)
    try:
        write_text_atomic(catalog_path(root), json.dumps(catalog,ensure_ascii=False,indent=2)+'\n')
    except OSError:
        target.rename(audio)
        raise
    return audio_identity(audio, root)


def label_reports(root=ROOT, folder=None):
    """Añadir nombres solo a Markdown; los JSON históricos conservan sus hashes."""
    rows = read_catalog(root)['recordings']
    changed = 0
    begin, end = '<!-- identidad-audio-inicio -->', '<!-- identidad-audio-fin -->'
    for path in (Path(folder) if folder else root/'resultados').rglob('*.md'):
        context = path.with_suffix('.json')
        if not context.exists():
            context = path.parent/'resumen.json'
        if not context.exists():
            continue
        source = context.read_text(encoding='utf-8')
        matches = [r for r in rows if any(Path(name).stem in source for name in audio_names(r)) or f'"{r["id"]}"' in source]
        if not matches:
            continue
        section = '\n'.join(['## Audio utilizado', '',
                              *[f"- **{r['label']}** — {Path(r['audio_file']).name}" for r in matches]])+'\n'
        text = path.read_text(encoding='utf-8')
        if begin in text:
            head, tail = text.split(begin,1)
            _, tail = tail.split(end,1)
            result = head.rstrip()+'\n\n'+begin+'\n'+section+end+tail
        else:
            result = text.rstrip()+'\n\n'+begin+'\n'+section+end+'\n'
        if result != text:
            write_text_atomic(path,result)
            changed += 1
    return changed


def verify_audio_catalog(rows, root=ROOT):
    """No confundir una entrada histórica explícita con otro WAV disponible."""
    available=[]
    for row in rows:
        path=root/row['audio_file']
        matches=path.is_file() and hashlib.sha256(path.read_bytes()).hexdigest()==row['audio_sha256']
        if matches:
            available.append(row)
        elif row.get('availability_status')!='historico_sin_wav_coincidente':
            raise ValueError(f'El WAV no coincide con su huella o no existe: {path}')
    return available


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--verificar', action='store_true', help='Comprobar WAV y SHA256, sin reconocimiento.')
    parser.add_argument('--actualizar-informes', action='store_true', help='Añadir nombres a Markdown, sin modificar JSON originales.')
    args = parser.parse_args()
    rows = read_catalog()['recordings']
    available=verify_audio_catalog(rows) if args.verificar else rows
    print(f'{len(rows)} entradas de catálogo; {len(available)} grabaciones'+(' verificadas' if args.verificar else ' registradas')+f'; {sum(r["duration_seconds"] for r in available)/60:.2f} minutos.')
    for row in rows:
        path = ROOT/row['audio_file']
        if args.verificar and row not in available:
            print(f'\n{row["id"]}: entrada histórica sin WAV coincidente; no se cuenta ni se sustituye su huella.')
            continue
        print(f"\n{row.get('label',row['id'])}\n  {row['audio_file']} | {row['duration_seconds']:.0f} s | {row['partition']}")
    if args.actualizar_informes:
        print(f'Informes etiquetados: {label_reports()}')
    if args.verificar:
        print('Todas las huellas de los WAV disponibles coinciden; históricos sin contenido local identificados aparte. No se ejecutó ASR.')


if __name__ == '__main__':
    main()
