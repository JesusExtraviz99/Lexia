from scripts.catalogo import same_audio
"""Evalúa registros de lectura normal contra anotación humana completa, sin nuevas inferencias."""
import argparse
from bisect import bisect_right
import hashlib
import json
from pathlib import Path
import statistics

from scripts.anotar import Workspace
from scripts.alinear import normalize

ROOT = Path(__file__).resolve().parents[1]


def position_at(words, seconds):
    """Última palabra terminada; se mantiene en pausas. Índices desde 1, cero antes."""
    return bisect_right([w['end'] for w in words], seconds)


def metrics(rows, key):
    values = [r[key] for r in rows]
    return {'samples': len(values),
            'mean_signed_words': statistics.mean(values) if values else None,
            'mean_absolute_words': statistics.mean(abs(v) for v in values) if values else None,
            'max_absolute_words': max(map(abs, values)) if values else None,
            'exact_samples': sum(v == 0 for v in values),
            'within_one_word_samples': sum(abs(v) <= 1 for v in values)}


def evaluate(data, annotation):
    words = annotation['words']
    if not same_audio(data['audio_file'], annotation['audio_file']):
        raise ValueError('El registro corresponde a otro audio.')
    if [normalize(w) for w in data['story_words']] != [normalize(w['word']) for w in words]:
        raise ValueError('El cuento del registro no coincide con la anotación.')
    if abs(data['audio_seconds'] - annotation['duration_seconds']) > .01:
        raise ValueError('Duración del registro incorrecta.')
    if not all(w['reviewed'] for w in words):
        raise ValueError('Este evaluador requiere revisión completa de la lectura normal.')
    updates = data['updates']
    first, last = words[0]['start'], words[-1]['end']
    cut_rows, display_rows = [], []
    for update in updates:
        cutoff = update['audio_available_seconds']
        predicted = update['position'] or 0
        if first <= cutoff <= last:
            expected = position_at(words, cutoff)
            # Lo que estaría visible en ese instante: última inferencia ya terminada.
            available = [u for u in updates if u['sequential_ready_seconds_simulated'] <= cutoff]
            visible = (available[-1]['position'] or 0) if available else 0
            cut_rows.append({'audio_seconds': cutoff, 'reference_position': expected,
                             'hypothesis_position': predicted, 'error_words': predicted - expected})
            display_rows.append({'audio_seconds': cutoff, 'reference_position': expected,
                                 'visible_position_simulated': visible, 'error_words': visible - expected})
    final = next((u for u in updates if u['position'] == len(words)), None)
    return {'window_seconds': data['audio_window_seconds'],
            'annotation_coverage_words': len(words),
            'hypothesis_at_audio_cutoff': metrics(cut_rows, 'error_words'),
            'visible_at_audio_cutoff_simulated': metrics(display_rows, 'error_words'),
            'cutoff_samples': cut_rows, 'display_samples': display_rows,
            'first_final_word_audio_seconds': final['audio_available_seconds'] if final else None,
            'first_final_word_ready_seconds_simulated': final['sequential_ready_seconds_simulated'] if final else None,
            'final_word_delay_seconds_simulated': final['sequential_ready_seconds_simulated'] - last if final else None,
            'final_position': updates[-1]['position']}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('folder', type=Path, help='Carpeta de una comparación de lectura normal.')
    args = parser.parse_args()
    annotation = Workspace().current()
    folder = args.folder.resolve()
    comparison = json.loads((folder / 'resumen.json').read_text(encoding='utf-8'))
    results = []
    for run in comparison['runs']:
        path = folder / run['record_file']
        result = evaluate(json.loads(path.read_text(encoding='utf-8')), annotation)
        results.append({'file': path.name, 'sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
                        'repeat': run['repeat'], **result})
    notice = ('Referencia de desarrollo revisada por el lector, no independiente. '
              'Posición de referencia = última palabra terminada (fin <= instante). '
              'Error firmado = posición estimada menos referencia: negativo es retraso. '
              'Muestras cada 2 s dentro de la lectura, desde la primera palabra hasta el fin de la última; '
              'se excluye el silencio final de las medias. La hipótesis al corte ignora coste de cómputo; '
              'la posición visible simulada conserva la última salida ya lista en ese mismo instante, '
              'incluyendo cola secuencial y sin carga de modelo ni latencia de pantalla. '
              'Límites ambiguos y muestreo de 2 s limitan la interpretación. '
              'Tres rondas del mismo audio no son tres lectores ni validación en otros entornos.')
    payload = {'notice': notice, 'annotation_file': 'datos/anotaciones/lectura_normal.json',
               'annotation_sha256': hashlib.sha256((ROOT / 'datos/anotaciones/lectura_normal.json').read_bytes()).hexdigest(),
               'runs': results}
    (folder / 'evaluacion_humana.json').write_text(json.dumps(payload, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    lines = ['# Seguimiento frente a marcas humanas', '', notice, '',
             '| Ventana | Ronda | Cortes | Error absoluto medio hipótesis (palabras) | Error absoluto medio visible simulado (palabras) | Demora final simulada (s) |',
             '|---:|---:|---:|---:|---:|---:|']
    for r in results:
        h, v = r['hypothesis_at_audio_cutoff'], r['visible_at_audio_cutoff_simulated']
        delay = r['final_word_delay_seconds_simulated']
        delay_label = f'{delay:.2f}' if delay is not None else 'No alcanzada'
        lines.append(f"| {r['window_seconds']} | {r['repeat']} | {h['samples']} | {h['mean_absolute_words']:.2f} | {v['mean_absolute_words']:.2f} | {delay_label} |")
    lines += ['', '## Posición por corte', '', '| Ventana | Ronda | Audio (s) | Referencia | Hipótesis | Visible simulado |', '|---:|---:|---:|---:|---:|---:|']
    for r in results:
        for h, v in zip(r['cutoff_samples'], r['display_samples']):
            lines.append(f"| {r['window_seconds']} | {r['repeat']} | {h['audio_seconds']} | {h['reference_position']} | {h['hypothesis_position']} | {v['visible_position_simulated']} |")
    (folder / 'evaluacion_humana.md').write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print(folder / 'evaluacion_humana.md')


if __name__ == '__main__':
    main()
