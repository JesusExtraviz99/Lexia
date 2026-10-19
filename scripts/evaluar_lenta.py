"""Contrasta cuatro anclas de lectura lenta sin interpolar las palabras no anotadas."""
import argparse
import hashlib
import json
from pathlib import Path

from scripts.anotar import ROOT, EventWorkspace
from scripts.alinear import normalize, tokens


def position_bounds(anchors, t, length):
    """Última palabra terminada: solo se acota con las anclas temporales conocidas."""
    completed = [w['story_range'][0] for w in anchors if w['end'] <= t]
    pending = [w['story_range'][0] for w in anchors if w['end'] > t]
    return max(completed, default=0), min(pending, default=length + 1) - 1


def evaluate(data, annotation, story):
    if (data['audio_file'] != Path(annotation['audio_file']).name
            or abs(data['audio_seconds'] - annotation['duration_seconds']) > .01
            or [normalize(w) for w in data['story_words']] != [normalize(w) for w in story]):
        raise ValueError('Audio, duración o cuento distintos de la referencia.')
    anchors = annotation['words']
    if ([w['story_range'] for w in anchors] != [[46, 46], [53, 53], [55, 55], [56, 56]]
            or not all(w['reviewed'] for w in anchors)):
        raise ValueError('Se requieren las cuatro anclas revisadas de la lectura lenta.')
    rows = []
    for u in data['updates']:
        t = u['audio_available_seconds']
        if t < anchors[0]['end']:
            continue
        low, high = position_bounds(anchors, t, len(story))
        position = u['position'] or 0
        ready = [r for r in data['updates'] if r['sequential_ready_seconds_simulated'] <= t]
        rows.append({'audio_seconds': t, 'reference_min': low, 'reference_max': high,
                     'hypothesis_position': position,
                     'minimum_lag_words': max(0, low - position),
                     'minimum_lead_words': max(0, position - high),
                     'visible_position_simulated': (ready[-1]['position'] or 0) if ready else 0,
                     'hypothesis_text': ' '.join(w['word'] for w in u['hypothesis'])})
    final_end = anchors[-1]['end']
    final = next((u for u in data['updates'] if u['audio_available_seconds'] >= final_end and u['position'] == 56), None)
    return {'samples': rows, 'cuaderno_end_seconds': final_end,
            'first_final_word': None if final is None else {
                'audio_seconds': final['audio_available_seconds'],
                'ready_seconds_simulated': final['sequential_ready_seconds_simulated'],
                'delay_seconds_simulated': final['sequential_ready_seconds_simulated'] - final_end},
            'post_reading_positions': [u['position'] for u in data['updates'] if u['audio_available_seconds'] >= final_end],
            'final_position': data['updates'][-1]['position']}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('folder', type=Path)
    args = parser.parse_args()
    workspace = EventWorkspace('lenta')
    annotation = workspace.current()
    reference = json.loads((ROOT / 'datos/referencias/lectura_lenta.json').read_text(encoding='utf-8'))
    folder = args.folder.resolve()
    comparison = json.loads((folder / 'resumen.json').read_text(encoding='utf-8'))
    runs = []
    for run in comparison['runs']:
        path = folder / run['record_file']
        result = evaluate(json.loads(path.read_text(encoding='utf-8')), annotation, tokens(reference['transcript_literal']))
        runs.append({'file': path.name, 'sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
                     'window_seconds': run['window_seconds'], 'repeat': run['repeat'], **result})
    notice = ('Cuatro anclas manuales revisadas por el lector, cobertura parcial y sin revisión independiente. '
              'Referencia = última palabra terminada. Entre anclas se indica un rango posible, sin interpolar tiempos. '
              'Cuando las cotas coinciden se conoce una posición exacta; tras cuaderno es 56. Una hipótesis dentro de un rango amplio no demuestra posición correcta. '
              'Un adelanto respecto al final anotado puede corresponder a una palabra todavía en curso. '
              'No se calcula un error medio para todo el audio. La posición visible usa la última salida ya lista '
              'según cola secuencial simulada, sin carga del modelo ni latencia de pantalla. '
              'Se reutilizan seis registros existentes, sin nuevas inferencias ni cambios del seguidor.')
    payload = {'notice': notice, 'annotation_file': workspace.path.relative_to(ROOT).as_posix(),
               'annotation_sha256': hashlib.sha256(workspace.path.read_bytes()).hexdigest(), 'runs': runs}
    (folder / 'evaluacion_lenta.json').write_text(json.dumps(payload, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    lines = ['# Lectura lenta frente a cuatro anclas humanas', '', notice, '',
             '| Ventana | Ronda | Primer corte con 56 tras terminar (s) | Demora final simulada (s) | Posición final | Posiciones tras el fin humano |',
             '|---:|---:|---:|---:|---:|---|']
    for r in runs:
        final = r['first_final_word']
        cut = str(final['audio_seconds']) if final else 'No alcanzada'
        delay = f"{final['delay_seconds_simulated']:.2f}" if final else '—'
        lines.append(f"| {r['window_seconds']} | {r['repeat']} | {cut} | {delay} | {r['final_position']} | {r['post_reading_positions']} |")
    lines += ['', '## Cortes desde el final de Después', '', '| Ventana | Ronda | Audio (s) | Referencia posible | Hipótesis | Retraso mínimo (palabras) | Visible simulado | Texto ASR |', '|---:|---:|---:|---|---:|---:|---:|---|']
    for r in runs:
        for u in r['samples']:
            text = u['hypothesis_text'].replace('|', '/').replace('\n', ' ')
            lines.append(f"| {r['window_seconds']} | {r['repeat']} | {u['audio_seconds']} | {u['reference_min']}–{u['reference_max']} | {u['hypothesis_position']} | {u['minimum_lag_words']} | {u['visible_position_simulated']} | {text} |")
    (folder / 'evaluacion_lenta.md').write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print(folder / 'evaluacion_lenta.md')


if __name__ == '__main__':
    main()
