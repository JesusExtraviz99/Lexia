"""Revisa la relectura por intentos completos sin inventar tiempos de palabras interiores."""
import argparse
import hashlib
import json
from pathlib import Path

from scripts.anotar import ROOT, EventWorkspace
from scripts.alinear import normalize, tokens


def phase_at(anchors, t):
    first, second, following = anchors
    if first['start'] <= t < first['end']:
        return 'primer_intento'
    if first['end'] <= t < second['start']:
        return 'entre_intentos'
    if second['start'] <= t < second['end']:
        return 'segundo_intento'
    if second['end'] <= t < following['end']:
        return 'frase_repetida_terminada'
    if t >= following['end']:
        return 'mirando_terminada'
    return 'antes_de_la_frase'


def evaluate(data, annotation, story):
    if (data['audio_file'] != Path(annotation['audio_file']).name
            or abs(data['audio_seconds'] - annotation['duration_seconds']) > .01
            or [normalize(w) for w in data['story_words']] != [normalize(w) for w in story]):
        raise ValueError('Registro incompatible con audio, duración o cuento.')
    anchors = annotation['words']
    if ([w['story_range'] for w in anchors] != [[37, 42], [37, 42], [43, 43]]
            or [w['attempt'] for w in anchors] != [1, 2, 1]
            or not all(w['reviewed'] for w in anchors)):
        raise ValueError('Se requieren ambos intentos y mirando revisados.')
    rows = []
    for u in data['updates']:
        t = u['audio_available_seconds']
        if not anchors[0]['start'] <= t <= anchors[2]['end'] + data['block_seconds']:
            continue
        ready = [r for r in data['updates'] if r['sequential_ready_seconds_simulated'] <= t]
        rows.append({'audio_seconds': t, 'phase': phase_at(anchors, t),
                     'position': u['position'], 'movement': u['movement'],
                     'ready_seconds_simulated': u['sequential_ready_seconds_simulated'],
                     'visible_position_simulated': ready[-1]['position'] if ready else None,
                     'hypothesis_text': ' '.join(w['word'] for w in u['hypothesis'])})
    second = anchors[1]
    outputs = [u for u in data['updates'] if second['start'] <= u['sequential_ready_seconds_simulated'] < second['end']]
    return {'first_attempt_seconds': [anchors[0]['start'], anchors[0]['end']],
            'second_attempt_seconds': [second['start'], second['end']],
            'gap_seconds': second['start'] - anchors[0]['end'],
            'samples': rows,
            'second_attempt_cut_samples': sum(r['phase'] == 'segundo_intento' for r in rows),
            'backward_hypotheses_with_cut_in_second_attempt': sum(r['phase'] == 'segundo_intento' and r['movement'] < 0 for r in rows),
            'backward_outputs_ready_during_second_attempt_simulated': sum(u['movement'] < 0 for u in outputs),
            'final_position': data['updates'][-1]['position']}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('folder', type=Path)
    args = parser.parse_args()
    workspace = EventWorkspace('relectura')
    annotation = workspace.current()
    story = tokens((ROOT / 'datos/textos/lectura_01.txt').read_text(encoding='utf-8'))
    folder = args.folder.resolve()
    comparison = json.loads((folder / 'resumen.json').read_text(encoding='utf-8'))
    runs = []
    for run in comparison['runs']:
        path = folder / run['record_file']
        result = evaluate(json.loads(path.read_text(encoding='utf-8')), annotation, story)
        runs.append({'file': path.name, 'sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
                     'window_seconds': run['window_seconds'], 'repeat': run['repeat'], **result})
    notice = ('Dos intentos completos y una palabra revisados por el lector, sin revisión independiente. '
              'No hay tiempos humanos de las seis palabras interiores: no se calcula error exacto de posición dentro de la frase '
              'ni demora de detección de su primer Los. Un retroceso pequeño no acredita seguir la frase completa desde su inicio. '
              'Se distingue el corte del audio del instante de salida lista según cola secuencial simulada, '
              'sin carga del modelo ni pantalla. Se reutilizan seis registros existentes, sin nuevas inferencias.')
    payload = {'notice': notice, 'annotation_file': workspace.path.relative_to(ROOT).as_posix(),
               'annotation_sha256': hashlib.sha256(workspace.path.read_bytes()).hexdigest(), 'runs': runs}
    (folder / 'evaluacion_relectura.json').write_text(json.dumps(payload, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    lines = ['# Relectura contrastada con intentos humanos', '', notice, '',
             f"Primer intento: {annotation['words'][0]['start']:.2f}–{annotation['words'][0]['end']:.2f} s. Segundo: {annotation['words'][1]['start']:.2f}–{annotation['words'][1]['end']:.2f} s. Mirando: {annotation['words'][2]['start']:.2f}–{annotation['words'][2]['end']:.2f} s.", '',
             '| Ventana | Ronda | Cortes durante segundo intento | Retrocesos de hipótesis en esos cortes | Salidas con retroceso listas durante el segundo intento (simulado) |', '|---:|---:|---:|---:|---:|']
    for r in runs:
        lines.append(f"| {r['window_seconds']} | {r['repeat']} | {r['second_attempt_cut_samples']} | {r['backward_hypotheses_with_cut_in_second_attempt']} | {r['backward_outputs_ready_during_second_attempt_simulated']} |")
    lines += ['', '## Cortes próximos a la relectura', '', '| Ventana | Ronda | Audio (s) | Fase | Posición | Movimiento | Salida lista simulada (s) | Visible simulado en el corte | Texto ASR |', '|---:|---:|---:|---|---:|---:|---:|---:|---|']
    for r in runs:
        for u in r['samples']:
            text = u['hypothesis_text'].replace('|', '/').replace('\n', ' ')
            lines.append(f"| {r['window_seconds']} | {r['repeat']} | {u['audio_seconds']} | {u['phase']} | {u['position']} | {u['movement']} | {u['ready_seconds_simulated']:.2f} | {u['visible_position_simulated']} | {text} |")
    (folder / 'evaluacion_relectura.md').write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print(folder / 'evaluacion_relectura.md')


if __name__ == '__main__':
    main()
