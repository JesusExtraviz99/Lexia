"""Contrasta las trazas de relectura lejana con tres anclas humanas revisadas."""
import argparse
import json
from pathlib import Path

from scripts.anotar import EventWorkspace, ROOT
from scripts.comparar_relectura_lejana import digest


def evaluate(rows, variant, anchors):
    cuaderno, los, alas = anchors
    backward = next((r for r in rows if r['audio_seconds'] >= los['start']
                     and r['variants'][variant]['movement'] < 0
                     and 37 <= r['variants'][variant]['position'] <= 45), None)
    final = next((r for r in rows if r['audio_seconds'] >= alas['end']
                  and r['variants'][variant]['position'] == 45), None)
    first_end = next((r for r in rows if cuaderno['end'] <= r['audio_seconds'] < los['start']
                      and r['variants'][variant]['position'] == 56), None)
    return {'first_56_ready_delay_after_cuaderno_end_simulated':
            first_end['ready_seconds_simulated'] - cuaderno['end'] if first_end else None,
            'backward_cut_seconds': backward['audio_seconds'] if backward else None,
            'backward_ready_seconds_simulated': backward['ready_seconds_simulated'] if backward else None,
            'backward_ready_since_los_start_simulated':
            backward['ready_seconds_simulated'] - los['start'] if backward else None,
            'final_45_cut_seconds': final['audio_seconds'] if final else None,
            'final_45_ready_seconds_simulated': final['ready_seconds_simulated'] if final else None,
            'final_45_ready_delay_after_alas_end_simulated':
            final['ready_seconds_simulated'] - alas['end'] if final else None,
            'final_position': rows[-1]['variants'][variant]['position']}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('carpeta', type=Path, help='Carpeta del comparador de relectura lejana.')
    args = parser.parse_args()
    folder = args.carpeta.resolve()
    manifest = folder / 'resumen.json'
    comparison = json.loads(manifest.read_text(encoding='utf-8'))
    workspace = EventWorkspace('relectura_lejana')
    annotation = workspace.current()
    anchors = annotation['words']
    if ([w['story_range'] for w in anchors] != [[56, 56], [37, 37], [45, 45]]
            or [w['attempt'] for w in anchors] != [1, 2, 2]
            or not all(w['reviewed'] for w in anchors)):
        raise ValueError('Se requieren cuaderno, Los y alas revisados.')
    notice = ('Anclas del propio lector, sin revisión independiente ni tiempos interiores de la frase. '
              'Salidas listas según cola secuencial simulada: no latencia visual medida; '
              'se reutilizan tiempos ASR y no se añade el coste de las variantes. '
              'La demora hasta alas se cuenta desde su final humano; el primer retroceso se cuenta desde el inicio de Los. '
              'Sin nuevas inferencias ni cambios del seguidor.')
    report = {'notice': notice, 'annotation_file': workspace.path.relative_to(ROOT).as_posix(),
              'annotation_sha256': digest(workspace.path), 'comparison_sha256': digest(manifest),
              'evaluator_sha256': digest(Path(__file__)), 'anchors': anchors, 'runs': []}
    lines = ['# Relectura lejana: contraste temporal humano', '', notice, '',
             '| Ventana | Ronda | Variante | Corte del retroceso (s) | Retroceso listo (s) | Alas listo (s) | Demora tras final de alas (s) |',
             '|---:|---:|---|---:|---:|---:|---:|']
    print('ANCLAS HUMANAS: ' + '; '.join(f"{w['word']}: {w['start']:.2f}-{w['end']:.2f} s" for w in anchors))
    print('Ventana | Ronda | Variante | Retroceso listo | Alas listo | Demora tras alas (simulada)')
    for run in comparison['runs']:
        source = Path(run['source_file'])
        data = json.loads(source.read_text(encoding='utf-8'))
        if (digest(source) != run['source_sha256'] or data['audio_file'] != workspace.audio.name
                or abs(data['audio_seconds'] - annotation['duration_seconds']) > .01
                or len(data['updates']) != len(run['updates'])):
            raise ValueError('Fuentes modificadas o audio incompatible.')
        for variant in ['original', 'combinada', 'nueva']:
            result = evaluate(run['updates'], variant, anchors)
            report['runs'].append({'window_seconds': run['window_seconds'], 'repeat': run['repeat'],
                                   'variant': variant, **result})
            def fmt(key):
                return 'no detectado' if result[key] is None else f'{result[key]:.2f}'
            values = [fmt(k) for k in ['backward_cut_seconds', 'backward_ready_seconds_simulated',
                      'final_45_ready_seconds_simulated', 'final_45_ready_delay_after_alas_end_simulated']]
            print(f"{run['window_seconds']} | {run['repeat']} | {variant} | {' | '.join(values[1:])}")
            lines.append(f"| {run['window_seconds']} | {run['repeat']} | {variant} | {' | '.join(values)} |")
    (folder / 'evaluacion_humana.json').write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    (folder / 'evaluacion_humana.md').write_text('\n'.join(lines)+'\n', encoding='utf-8')
    print(notice)
    print(f'Informe: {folder / "evaluacion_humana.md"}')


if __name__ == '__main__':
    main()
