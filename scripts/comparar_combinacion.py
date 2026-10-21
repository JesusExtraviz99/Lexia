"""Compara original, palabra aislada, protección temporal y ambas sobre el mismo ASR."""
from datetime import datetime
import hashlib
import json

from scripts.alinear import tokens
from scripts.anotar import ROOT, Workspace, EventWorkspace
from scripts.comparar_seguidores import CASES, Tracker, SingleWordTracker, TemporalBacktrackTracker, CombinedTracker, replay
from scripts.evaluar_seguimiento import evaluate as evaluate_normal
from scripts.evaluar_pausa import evaluate as evaluate_pause
from scripts.evaluar_lenta import evaluate as evaluate_slow
from scripts.evaluar_relectura import evaluate as evaluate_repeat


VARIANTS = {'original': Tracker, 'palabra_aislada': SingleWordTracker,
            'temporal': TemporalBacktrackTracker, 'combinada': CombinedTracker}


def changes(first, second):
    return [{'audio_seconds': a['audio_available_seconds'], 'first': a['position'], 'second': b['position']}
            for a, b in zip(first['updates'], second['updates']) if a['position'] != b['position']]


def interaction_changes(original, single, temporal, combined):
    """Cuenta posiciones combinadas no observadas en ninguna variante aislada.

    Es una comprobación descriptiva de interacción, no prueba estadística.
    """
    return [{'audio_seconds': o['audio_available_seconds'], 'original': o['position'],
             'palabra_aislada': s['position'], 'temporal': t['position'], 'combinada': c['position']}
            for o, s, t, c in zip(original['updates'], single['updates'], temporal['updates'], combined['updates'])
            if c['position'] not in {o['position'], s['position'], t['position']}]


def far_rereading_check():
    """Caso sintético para mostrar el límite de la búsqueda local tras conservar avance."""
    def timed(text, start):
        return [{'word': w, 'start': start + i, 'end': start + i + 1}
                for i, w in enumerate(tokens(text))]
    data = {'story_words': tokens('mirando sus alas después volvieron a casa y dibujaron la mariposa en un cuaderno'),
            'updates': [{'hypothesis': h} for h in [timed('mirando sus alas', 0), timed('Después', 3),
                        timed('y dibujaron la mariposa en un cuaderno', 8),
                        timed('en un jugaderno', 12), timed('mirando sus alas', 20)]]}
    return {'notice': 'Caso sintético, no grabación adicional. La relectura apunta a 3. Al conservar 14, la búsqueda local empieza en 3 y solo contiene una de las tres palabras, insuficiente para aceptar el salto en esta actualización. El original en 13 todavía incluye sus y alas y acepta 3. No se prueba aquí la recuperación global posterior.',
            'expected_rereading_position': 3,
            'positions_after_rereading': {name: replay(data, tracker)['updates'][-1]['position']
                                         for name, tracker in VARIANTS.items()}}


def main():
    folder = ROOT / 'resultados/combinacion' / datetime.now().strftime('%Y%m%d_%H%M%S_%f')
    folder.mkdir(parents=True)
    annotations = {'normal': Workspace().current(),
                   **{case: EventWorkspace(case).current() for case in ['pausa', 'lenta', 'relectura']}}
    story = tokens((ROOT / 'datos/textos/lectura_01.txt').read_text(encoding='utf-8'))
    report = {'notice': 'Comparación de cuatro seguidores sobre las mismas hipótesis guardadas. No hay nuevas inferencias ni nuevas grabaciones. Tiempos ASR/cola reutilizados, no mediciones nuevas de latencia total. Parámetros de ambas reglas sin cambios. Datos de desarrollo usados para diseñarlas; no demuestra generalización. Seguidor habitual sin activar variantes.',
              'variants': list(VARIANTS), 'synthetic_far_rereading': far_rereading_check(),
              'code_sha256': {name: hashlib.sha256((ROOT / 'scripts' / name).read_bytes()).hexdigest()
                              for name in ['seguir.py', 'comparar_seguidores.py', 'comparar_combinacion.py']},
              'annotation_sha256': {case: hashlib.sha256((ROOT / 'datos/anotaciones' /
                                      ('lectura_normal.json' if case == 'normal' else f'lectura_{case}_fragmentos.json')).read_bytes()).hexdigest()
                                    for case in annotations}, 'runs': []}
    for case, source_folder, windows in CASES:
        source = ROOT / 'resultados/comparaciones' / source_folder
        comparison = json.loads((source / 'resumen.json').read_text(encoding='utf-8'))
        for run in comparison['runs']:
            if run['window_seconds'] not in windows:
                continue
            path = source / run['record_file']
            data = json.loads(path.read_text(encoding='utf-8'))
            traces = {name: replay(data, tracker) for name, tracker in VARIANTS.items()}
            original = traces['original']
            if any((a['position'], a['movement'], a['mode']) != (b['position'], b['movement'], b['mode'])
                   for a, b in zip(data['updates'], original['updates'])):
                raise ValueError(f'No se reproduce el original: {path}')
            filename = f"{case}_{run['window_seconds']}s_r{run['repeat']}.json"
            summary = {'case': case, 'window_seconds': run['window_seconds'], 'repeat': run['repeat'],
                       'source_file': path.relative_to(ROOT).as_posix(),
                       'source_sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
                       'baseline_reproduces_original': True, 'trace_file': filename,
                       'interaction_positions': interaction_changes(*[traces[name] for name in VARIANTS]),
                       'variants': {}}
            compact = {'source_file': summary['source_file'], 'source_sha256': summary['source_sha256'],
                       'notice': 'Hipótesis y tiempos ASR completos en la fuente original, identificada por huella. No se duplican aquí.', 'variants': {}}
            for name, trace in traces.items():
                evaluation = None
                if case == 'normal':
                    evaluation = evaluate_normal(trace, annotations[case])
                elif case in ['pausa', 'lenta', 'relectura']:
                    evaluator = {'pausa': evaluate_pause, 'lenta': evaluate_slow, 'relectura': evaluate_repeat}[case]
                    evaluation = evaluator(trace, annotations[case], story)
                summary['variants'][name] = {'final_position': trace['updates'][-1]['position'],
                    'changes_from_original': changes(original, trace), 'evaluation': evaluation,
                    'single_word_updates': [u['audio_available_seconds'] for u in trace['updates'] if u['mode'] == 'palabra_aislada_consecutiva'],
                    'blocked_backward_updates': [u['audio_available_seconds'] for u in trace['updates'] if u['mode'] == 'retroceso_sin_tiempo_nuevo'],
                    'tracker_update_seconds_measured': trace['replay']['tracker_update_seconds_measured']}
                compact['variants'][name] = [{'audio_seconds': u['audio_available_seconds'], 'position': u['position'],
                                             'movement': u['movement'], 'mode': u['mode'], 'evidence': u['evidence']}
                                            for u in trace['updates']]
            (folder / filename).write_text(json.dumps(compact, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
            report['runs'].append(summary)
    (folder / 'resumen.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    lines = ['# Comparación de cuatro seguidores', '', report['notice'], '',
             '| Caso | Ventana | Ronda | Final original | Solo palabra | Solo temporal | Ambas | Cortes distintos original/ambas | Posiciones nuevas por interacción |',
             '|---|---:|---:|---:|---:|---:|---:|---:|---:|']
    print('COMPARACION DE CUATRO VERSIONES - solo reproduccion, sin nuevas inferencias')
    print('Caso | Ventana | Ronda | Final original / palabra / temporal / ambas | Cortes distintos original-ambas | Posiciones nuevas por interaccion')
    for r in report['runs']:
        finals = [r['variants'][name]['final_position'] for name in VARIANTS]
        different = len(r['variants']['combinada']['changes_from_original'])
        novel = len(r['interaction_positions'])
        lines.append(f"| {r['case']} | {r['window_seconds']} | {r['repeat']} | " + ' | '.join(map(str, finals)) + f' | {different} | {novel} |')
        print(f"{r['case']} | {r['window_seconds']} | {r['repeat']} | {' / '.join(map(str, finals))} | {different} | {novel}")
    lines += ['', '## Cambios de posición con ambas reglas', '']
    print('\nDETALLE DE LAS MEJORAS Y CAMBIOS CON AMBAS REGLAS')
    for r in report['runs']:
        combined = r['variants']['combinada']
        if combined['changes_from_original']:
            text = f"{r['case']}, ventana {r['window_seconds']}, ronda {r['repeat']}: palabra aislada {combined['single_word_updates']}; retrocesos rechazados {combined['blocked_backward_updates']}; cambios {combined['changes_from_original']}"
            lines.append(text)
            print(text)
    lines += ['', 'No observar posiciones nuevas por interacción no demuestra independencia de las reglas ni ausencia universal de regresiones. Ver evaluaciones humanas por variante en resumen.json.']
    check = report['synthetic_far_rereading']
    lines += ['', '## Límite observado en una relectura sintética lejana', '', check['notice'], '', str(check['positions_after_rereading'])]
    (folder / 'resumen.md').write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print(f'\nInformes guardados en: {folder}')
    print('\nCONTROL ADICIONAL: RELECTURA SINTETICA LEJANA (objetivo: posicion 3)')
    print(check['positions_after_rereading'])
    print('Limite: conservar una posicion adelantada desplaza la zona de busqueda. Una relectura lejana puede necesitar recuperacion adicional. No se ha corregido en este experimento.')
    print('Las reglas siguen siendo experimentales: el seguidor habitual no cambia. Pendiente de revision compartida.')


if __name__ == '__main__':
    main()
