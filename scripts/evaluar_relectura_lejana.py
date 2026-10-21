"""Contrasta las trazas de relectura lejana con tres anclas humanas revisadas."""
import argparse
import json
from pathlib import Path

from scripts.anotar import EventWorkspace, ROOT
from scripts.comparar_relectura_lejana import digest


def evaluate(rows, variant, anchors, story_range=(37, 45)):
    cuaderno, los, alas = anchors
    first_position, target = story_range
    backward = next((r for r in rows if r['audio_seconds'] >= los['start']
                     and r['variants'][variant]['movement'] < 0
                     and first_position <= r['variants'][variant]['position'] <= target), None)
    final = next((r for r in rows if r['audio_seconds'] >= alas['end']
                  and r['variants'][variant]['position'] == target), None)
    first_target = next((r for r in rows if r['audio_seconds'] >= los['start']
                         and r['variants'][variant]['position'] == target), None)
    first_end = next((r for r in rows if cuaderno['end'] <= r['audio_seconds'] < los['start']
                      and r['variants'][variant]['position'] == 56), None)
    result = {'target_position': target,
            'first_target_cut_seconds': first_target['audio_seconds'] if first_target else None,
            'first_target_ready_seconds_simulated': first_target['ready_seconds_simulated'] if first_target else None,
            'first_target_ready_minus_human_end_simulated':
            first_target['ready_seconds_simulated']-alas['end'] if first_target else None,
            'first_target_cut_before_human_end':
            first_target['audio_seconds'] < alas['end'] if first_target else None,
            'first_56_ready_delay_after_cuaderno_end_simulated':
            first_end['ready_seconds_simulated'] - cuaderno['end'] if first_end else None,
            'backward_cut_seconds': backward['audio_seconds'] if backward else None,
            'backward_ready_seconds_simulated': backward['ready_seconds_simulated'] if backward else None,
            'backward_ready_since_phrase_start_simulated':
            backward['ready_seconds_simulated'] - los['start'] if backward else None,
            'post_end_target_cut_seconds': final['audio_seconds'] if final else None,
            'post_end_target_ready_seconds_simulated': final['ready_seconds_simulated'] if final else None,
            'post_end_target_ready_delay_simulated':
            final['ready_seconds_simulated'] - alas['end'] if final else None,
            'final_position': rows[-1]['variants'][variant]['position']}
    if story_range == (37, 45):
        # Mantener las claves de los informes de la primera relectura.
        result.update(backward_ready_since_los_start_simulated=result['backward_ready_since_phrase_start_simulated'],
                      final_45_cut_seconds=result['post_end_target_cut_seconds'],
                      final_45_ready_seconds_simulated=result['post_end_target_ready_seconds_simulated'],
                      final_45_ready_delay_after_alas_end_simulated=result['post_end_target_ready_delay_simulated'])
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('carpeta', type=Path, help='Carpeta del comparador de relectura lejana.')
    parser.add_argument('--caso', choices=['relectura_lejana', 'relectura_azul'], default='relectura_lejana')
    args = parser.parse_args()
    folder = args.carpeta.resolve()
    manifest = folder / 'resumen.json'
    comparison = json.loads(manifest.read_text(encoding='utf-8'))
    workspace = EventWorkspace(args.caso)
    annotation = workspace.current()
    anchors = annotation['words']
    start_position, target = (10, 17) if args.caso == 'relectura_azul' else (37, 45)
    label = 'azul' if args.caso == 'relectura_azul' else 'alas'
    if ([w['story_range'] for w in anchors] != [[56, 56], [start_position, start_position], [target, target]]
            or [w['attempt'] for w in anchors] != [1, 2, 2]
            or not all(w['reviewed'] for w in anchors)):
        raise ValueError('Se requieren las tres anclas del caso revisadas.')
    notice = ('Anclas del propio lector, sin revisión independiente ni tiempos interiores de la frase. '
              'Salidas listas según cola secuencial simulada: no latencia visual medida; '
              'se reutilizan tiempos ASR y no se añade el coste de las variantes. '
              f'La diferencia hasta {label} se cuenta desde su final humano; el primer retroceso desde el inicio de la frase. '
              'Se distingue la primera hipótesis del destino (puede usar palabra incompleta) de la primera con corte posterior a su final humano. '
              'Un valor negativo significa anticipación, no una demora nula. '
              'Sin nuevas inferencias ni cambios del seguidor.')
    report = {'notice': notice, 'case': args.caso, 'annotation_file': workspace.path.relative_to(ROOT).as_posix(),
              'annotation_sha256': digest(workspace.path), 'comparison_sha256': digest(manifest),
              'evaluator_sha256': digest(Path(__file__)), 'anchors': anchors, 'runs': []}
    lines = ['# Relectura lejana: contraste temporal humano', '', notice, '',
             f'| Ventana | Ronda | Variante | Retroceso listo (s) | Primer {label} listo (s) | Diferencia respecto al final humano (s) | Corte antes del final humano | Destino listo con corte posterior al final humano (s) |',
             '|---:|---:|---|---:|---:|---:|---|---:|']
    print('ANCLAS HUMANAS: ' + '; '.join(f"{w['word']}: {w['start']:.2f}-{w['end']:.2f} s" for w in anchors))
    print(f'Ventana | Ronda | Variante | Retroceso listo | Primer {label} listo | Diferencia tras final humano (simulada) | Corte antes de terminar palabra | Destino listo con corte posterior al final humano')
    for run in comparison['runs']:
        source = Path(run['source_file'])
        data = json.loads(source.read_text(encoding='utf-8'))
        if (digest(source) != run['source_sha256'] or data['audio_file'] != workspace.audio.name
                or abs(data['audio_seconds'] - annotation['duration_seconds']) > .01
                or len(data['updates']) != len(run['updates'])):
            raise ValueError('Fuentes modificadas o audio incompatible.')
        for variant in ['original', 'combinada', 'nueva']:
            result = evaluate(run['updates'], variant, anchors, (start_position, target))
            report['runs'].append({'window_seconds': run['window_seconds'], 'repeat': run['repeat'],
                                   'variant': variant, **result})
            def fmt(key):
                return 'no detectado' if result[key] is None else f'{result[key]:.2f}'
            early = result['first_target_cut_before_human_end']
            values = [fmt(k) for k in ['backward_ready_seconds_simulated', 'first_target_ready_seconds_simulated',
                      'first_target_ready_minus_human_end_simulated']]
            values += ['no detectado' if early is None else ('sí' if early else 'no'), fmt('post_end_target_ready_seconds_simulated')]
            print(f"{run['window_seconds']} | {run['repeat']} | {variant} | {' | '.join(values)}")
            lines.append(f"| {run['window_seconds']} | {run['repeat']} | {variant} | {' | '.join(values)} |")
    (folder / 'evaluacion_humana.json').write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    (folder / 'evaluacion_humana.md').write_text('\n'.join(lines)+'\n', encoding='utf-8')
    print(notice)
    print(f'Informe: {folder / "evaluacion_humana.md"}')


if __name__ == '__main__':
    main()
