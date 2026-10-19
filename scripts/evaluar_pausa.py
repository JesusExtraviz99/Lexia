"""Revisa una pausa con tres anclas humanas sin extrapolar tiempos al resto del cuento."""
import argparse
import hashlib
import json
from pathlib import Path

from scripts.anotar import EventWorkspace, ROOT
from scripts.alinear import tokens, normalize


def evaluate(data, annotation, story):
    if data['audio_file'] != Path(annotation['audio_file']).name:
        raise ValueError('Audio distinto del anotado.')
    if abs(data['audio_seconds'] - annotation['duration_seconds']) > .01:
        raise ValueError('Duración distinta del audio anotado.')
    if [normalize(w) for w in data['story_words']] != [normalize(w) for w in story]:
        raise ValueError('Cuento distinto del anotado.')
    anchors = annotation['words']
    if ([w['story_range'] for w in anchors] != [[27, 27], [28, 28], [56, 56]]
            or not all(w['reviewed'] for w in anchors)):
        raise ValueError('Se requieren las tres anclas de pausa revisadas.')
    pause_start, pause_end = anchors[0]['end'], anchors[1]['start']
    resume_word_end, reading_end = anchors[1]['end'], anchors[2]['end']
    updates = data['updates']
    rows = []
    for u in updates:
        t = u['audio_available_seconds']
        if pause_start <= t < pause_end:
            ready = [r for r in updates if r['sequential_ready_seconds_simulated'] <= t]
            visible = (ready[-1]['position'] or 0) if ready else 0
            rows.append({'audio_seconds': t, 'reference_position': 27,
                         'hypothesis_position': u['position'] or 0,
                         'visible_position_simulated': visible,
                         'hypothesis_text': ' '.join(w['word'] for w in u['hypothesis'])})
    # Un salto a una posición posterior acredita avance del seguidor, no reconocimiento de Ana.
    resumed = next((u for u in updates if u['audio_available_seconds'] >= resume_word_end
                    and (u['position'] or 0) >= 28), None)
    final = next((u for u in updates if u['audio_available_seconds'] >= reading_end
                  and u['position'] == 56), None)
    after = [u for u in updates if u['audio_available_seconds'] >= reading_end]
    return {'pause_start_seconds': pause_start, 'pause_end_seconds': pause_end,
            'pause_duration_seconds': pause_end - pause_start, 'pause_samples': rows,
            'hypothesis_exact_27_samples': sum(r['hypothesis_position'] == 27 for r in rows),
            'visible_exact_27_samples': sum(r['visible_position_simulated'] == 27 for r in rows),
            'first_advance_after_resume': None if resumed is None else {
                'audio_seconds': resumed['audio_available_seconds'], 'position': resumed['position'],
                'delay_from_ana_end_seconds_simulated': resumed['sequential_ready_seconds_simulated'] - resume_word_end},
            'first_final_word': None if final is None else {
                'audio_seconds': final['audio_available_seconds'],
                'delay_from_cuaderno_end_seconds_simulated': final['sequential_ready_seconds_simulated'] - reading_end},
            'post_reading_samples': len(after),
            'post_reading_positions': [u['position'] for u in after]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('folder', type=Path)
    args = parser.parse_args()
    workspace = EventWorkspace('pausa')
    annotation = workspace.current()
    reference = json.loads((ROOT / 'datos/referencias/lectura_pausa.json').read_text(encoding='utf-8'))
    folder = args.folder.resolve()
    comparison = json.loads((folder / 'resumen.json').read_text(encoding='utf-8'))
    results = []
    for run in comparison['runs']:
        path = folder / run['record_file']
        result = evaluate(json.loads(path.read_text(encoding='utf-8')), annotation, tokens(reference['transcript_literal']))
        results.append({'file': path.name, 'sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
                        'window_seconds': run['window_seconds'], 'repeat': run['repeat'], **result})
    notice = ('Tres anclas manuales revisadas por el lector; cobertura parcial, sin revisión independiente. '
              'La pausa se mide desde el final de flor hasta el inicio de Ana: intervalo sin lectura, no silencio acústico absoluto. '
              'Solo se conoce posición de referencia 27 dentro de ese intervalo. '
              'Las hipótesis de ventanas solapadas pueden contener habla anterior a la pausa. '
              'Una hipótesis no vacía no demuestra alucinación ni habla durante la pausa. '
              'La posición visible usa la última salida ya terminada en cada corte, según cola secuencial simulada, '
              'sin carga inicial del modelo ni latencia de pantalla. No se asignan tiempos a palabras no anotadas. '
              'El primer avance >=28 no mide reconocimiento exacto ni tiempo de detección de Ana. '
              'Se reutilizan registros existentes: no se han ejecutado nuevas inferencias.')
    payload = {'notice': notice, 'annotation_file': workspace.path.relative_to(ROOT).as_posix(),
               'annotation_sha256': hashlib.sha256(workspace.path.read_bytes()).hexdigest(), 'runs': results}
    (folder / 'evaluacion_pausa.json').write_text(json.dumps(payload, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    lines = ['# Evaluación de la pausa con anclas humanas', '', notice, '',
             f"Pausa anotada: {results[0]['pause_start_seconds']:.2f}–{results[0]['pause_end_seconds']:.2f} s; duración {results[0]['pause_duration_seconds']:.2f} s.", '',
             '| Ventana | Ronda | Hipótesis en 27 durante pausa | Visible en 27 durante pausa | Primer avance tras retomar (audio s / posición) | Demora de avance simulada desde fin de Ana (s) | Demora final simulada (s) |',
             '|---:|---:|---:|---:|---|---:|---:|']
    for r in results:
        resume, final = r['first_advance_after_resume'], r['first_final_word']
        first = f"{resume['audio_seconds']:.2f} / {resume['position']}" if resume else 'Sin avance'
        delay = f"{resume['delay_from_ana_end_seconds_simulated']:.2f}" if resume else '—'
        ending = f"{final['delay_from_cuaderno_end_seconds_simulated']:.2f}" if final else 'No alcanzada'
        n = len(r['pause_samples'])
        lines.append(f"| {r['window_seconds']} | {r['repeat']} | {r['hypothesis_exact_27_samples']}/{n} | {r['visible_exact_27_samples']}/{n} | {first} | {delay} | {ending} |")
    lines += ['', '## Cortes dentro de la pausa', '', '| Ventana | Ronda | Audio (s) | Referencia | Hipótesis | Visible simulado | Texto ASR |', '|---:|---:|---:|---:|---:|---:|---|']
    for r in results:
        for row in r['pause_samples']:
            text = row['hypothesis_text'].replace('|', '/').replace('\n', ' ')
            lines.append(f"| {r['window_seconds']} | {r['repeat']} | {row['audio_seconds']} | 27 | {row['hypothesis_position']} | {row['visible_position_simulated']} | {text} |")
    (folder / 'evaluacion_pausa.md').write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print(folder / 'evaluacion_pausa.md')


if __name__ == '__main__':
    main()
