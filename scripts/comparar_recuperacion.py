"""Prueba recuperación exacta global sobre la combinación, sin cambiar el seguidor habitual."""
from datetime import datetime
import hashlib
import json
import math

from scripts.alinear import normalize
from scripts.anotar import ROOT, Workspace, EventWorkspace
from scripts.comparar_seguidores import CASES, Tracker, CombinedTracker, replay
from scripts.comparar_combinacion import changes
from scripts.diagnosticar_recuperacion import STORY, PREFIX, timed, scenarios
from scripts.seguir import locate
from scripts.evaluar_seguimiento import evaluate as evaluate_normal
from scripts.evaluar_pausa import evaluate as evaluate_pause
from scripts.evaluar_lenta import evaluate as evaluate_slow
from scripts.evaluar_relectura import evaluate as evaluate_repeat


def unique_exact_tail(story, hypothesis):
    """Exige que toda la cola usada (3–8 palabras) sea exacta y tenga una sola aparición."""
    tail = hypothesis[-8:]
    if len(tail) < 3:
        return None
    heard = [normalize(w['word']) for w in tail]
    expected = [normalize(w) for w in story]
    starts = [i for i in range(len(expected) - len(heard) + 1) if expected[i:i + len(heard)] == heard]
    if len(starts) != 1:
        return None
    return {'position': starts[0] + len(heard), 'phrase': heard,
            'start_seconds': tail[0]['start'], 'end_seconds': tail[-1]['end'],
            'ordered_times': all(a['end'] <= b['start'] for a, b in zip(tail, tail[1:]))}


class ExactRecoveryTracker(CombinedTracker):
    """Recuperación anticipada solo hacia atrás, con frase inequívoca y tiempo posterior."""
    def update_timed(self, hypothesis):
        for w in hypothesis:
            if any(isinstance(w.get(k), bool) or not isinstance(w.get(k), (int, float))
                   or not math.isfinite(w[k]) for k in ['start', 'end']):
                raise ValueError('Se requieren timestamps ASR finitos.')
            if not 0 <= w['start'] <= w['end']:
                raise ValueError('Intervalo ASR inválido.')
        if self.position and self.latest_support_end is not None:
            local = locate(self.story, [w['word'] for w in hypothesis], self.position)
            if local['position'] is None:
                exact = unique_exact_tail(self.story, hypothesis)
                if (exact is not None and exact['position'] < self.position and exact['ordered_times']
                        and exact['start_seconds'] >= self.latest_support_end
                        and exact['end_seconds'] > self.latest_support_end):
                    old, previous_time = self.position, self.latest_support_end
                    self.position = exact['position']
                    self.latest_support_end = exact['end_seconds']
                    self.failures = 0
                    self.recovery_candidate = None
                    return {'previous_position': old, 'position': self.position,
                            'word': self.story[self.position - 1], 'movement': self.position - old,
                            'mode': 'recuperacion_global_exacta',
                            'evidence': {'reason': 'frase_exacta_unica_posterior',
                                         'position': self.position, 'phrase': exact['phrase'],
                                         'asr_phrase_start_seconds': exact['start_seconds'],
                                         'asr_phrase_end_seconds': exact['end_seconds'],
                                         'previous_support_end_seconds': previous_time}}
        return super().update_timed(hypothesis)


def synthetic_comparison():
    results = []
    controls = [*scenarios(),
                ('E. Frase exacta de audio antiguo', [timed('mirando sus alas', 0)]),
                ('F. Solo dos palabras', [timed('mirando sus', 20)]),
                ('G. Una palabra no coincide', [timed('mirando sus alax', 20)]),
                ('H. Frase que empieza antes del apoyo aceptado', [timed('mirando sus alas', 14)]),
                ('I. Texto antiguo seguido de igual texto con tiempos nuevos',
                 [timed('mirando sus alas', 0), timed('mirando sus alas', 20)])]
    for title, proposals in controls:
        data = {'story_words': STORY, 'updates': [{'hypothesis': h} for h in PREFIX + proposals]}
        old = replay(data, CombinedTracker)['updates'][-len(proposals):]
        new = replay(data, ExactRecoveryTracker)['updates'][-len(proposals):]
        results.append({'case': title, 'combined_positions': [u['position'] for u in old],
                        'new_positions': [u['position'] for u in new],
                        'new_modes': [u['mode'] for u in new],
                        'fast_recoveries': sum(u['mode'] == 'recuperacion_global_exacta' for u in new)})
    ambiguous_story = STORY + ['enlace'] * 24 + STORY[:3] + ['final'] * 20
    ambiguous = ExactRecoveryTracker(ambiguous_story)
    ambiguous.position, ambiguous.latest_support_end = len(ambiguous_story), 50
    previous_ambiguous = CombinedTracker(ambiguous_story)
    previous_ambiguous.position, previous_ambiguous.latest_support_end = len(ambiguous_story), 50
    previous_state = previous_ambiguous.update_timed(timed('mirando sus alas', 60))
    state = ambiguous.update_timed(timed('mirando sus alas', 60))
    results.append({'case': 'J. Frase con dos apariciones en el cuento (estado sintetico)',
                    'combined_positions': [previous_state['position']], 'new_positions': [state['position']],
                    'new_modes': [state['mode']],
                    'fast_recoveries': int(state['mode'] == 'recuperacion_global_exacta'),
                    'initial_position': len(ambiguous_story), 'expected_fast_recoveries': 0})
    return results


def main():
    folder = ROOT / 'resultados/recuperacion' / datetime.now().strftime('%Y%m%d_%H%M%S_%f')
    folder.mkdir(parents=True)
    annotations = {'normal': Workspace().current(),
                   **{case: EventWorkspace(case).current() for case in ['pausa', 'lenta', 'relectura']}}
    from scripts.alinear import tokens
    story = tokens((ROOT / 'datos/textos/lectura_01.txt').read_text(encoding='utf-8'))
    report = {'notice': 'Variante experimental sobre la combinación. Mismos ASR, cortes y tiempos guardados; sin nuevas inferencias, grabaciones ni medición real de latencia. Se usan anclas humanas solo para evaluar. Regla de al menos tres palabras elegida provisionalmente sobre datos de desarrollo. Seguidor habitual sin activar variantes.',
              'rule': 'Si falla la búsqueda local: cola completa de 3 a 8 palabras exactas consecutivas, aparición única en todo el cuento, destino anterior, tiempos ordenados y frase situada después del apoyo temporal aceptado. El resto conserva la combinación y la política de texto idéntico.',
              'code_sha256': {name: hashlib.sha256((ROOT / 'scripts' / name).read_bytes()).hexdigest()
                              for name in ['seguir.py', 'comparar_seguidores.py', 'comparar_recuperacion.py', 'diagnosticar_recuperacion.py']},
              'annotation_sha256': {case: hashlib.sha256((ROOT / 'datos/anotaciones' /
                                      ('lectura_normal.json' if case == 'normal' else f'lectura_{case}_fragmentos.json')).read_bytes()).hexdigest()
                                    for case in annotations},
              'synthetic_controls': synthetic_comparison(), 'runs': []}
    classes = {'original': Tracker, 'combinada': CombinedTracker, 'recuperacion_exacta': ExactRecoveryTracker}
    print('RECUPERACION GLOBAL EXACTA - comparacion experimental, sin nuevas inferencias')
    print('Caso | Ventana | Ronda | Final original / combinada / nueva | Cortes distintos combinada-nueva | Recuperacion nueva (corte s)')
    for case, source_folder, windows in CASES:
        source = ROOT / 'resultados/comparaciones' / source_folder
        comparison = json.loads((source / 'resumen.json').read_text(encoding='utf-8'))
        for run in comparison['runs']:
            if run['window_seconds'] not in windows:
                continue
            path = source / run['record_file']
            data = json.loads(path.read_text(encoding='utf-8'))
            traces = {name: replay(data, cls) for name, cls in classes.items()}
            if any((a['position'], a['movement'], a['mode']) != (b['position'], b['movement'], b['mode'])
                   for a, b in zip(data['updates'], traces['original']['updates'])):
                raise ValueError(f'Original no reproducido: {path}')
            filename = f"{case}_{run['window_seconds']}s_r{run['repeat']}.json"
            summary = {'case': case, 'window_seconds': run['window_seconds'], 'repeat': run['repeat'],
                       'source_file': path.relative_to(ROOT).as_posix(), 'source_sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
                       'trace_file': filename, 'baseline_reproduces_original': True,
                       'changes_from_combined': changes(traces['combinada'], traces['recuperacion_exacta']), 'variants': {}}
            compact = {'source_file': summary['source_file'], 'source_sha256': summary['source_sha256'], 'variants': {}}
            for name, trace in traces.items():
                evaluation = None
                if case == 'normal':
                    evaluation = evaluate_normal(trace, annotations[case])
                elif case in ['pausa', 'lenta', 'relectura']:
                    evaluator = {'pausa': evaluate_pause, 'lenta': evaluate_slow, 'relectura': evaluate_repeat}[case]
                    evaluation = evaluator(trace, annotations[case], story)
                summary['variants'][name] = {'final_position': trace['updates'][-1]['position'], 'evaluation': evaluation,
                    'tracker_update_seconds_measured': trace['replay']['tracker_update_seconds_measured'],
                    'fast_recovery_cuts': [u['audio_available_seconds'] for u in trace['updates'] if u['mode'] == 'recuperacion_global_exacta']}
                compact['variants'][name] = [{'audio_seconds': u['audio_available_seconds'], 'position': u['position'],
                                             'movement': u['movement'], 'mode': u['mode'], 'evidence': u['evidence']}
                                            for u in trace['updates']]
            (folder / filename).write_text(json.dumps(compact, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
            report['runs'].append(summary)
            finals = ' / '.join(str(summary['variants'][name]['final_position']) for name in classes)
            print(f"{case} | {run['window_seconds']} | {run['repeat']} | {finals} | {len(summary['changes_from_combined'])} | {summary['variants']['recuperacion_exacta']['fast_recovery_cuts']}")
    print('\nCONTROLES SINTETICOS: las listas son propuestas, no segundos de demora')
    for control in report['synthetic_controls']:
        print(f"{control['case']}: antes {control['combined_positions']} -> nueva {control['new_positions']}; recuperaciones nuevas {control['fast_recoveries']}")
    print('Control I: limite conservado; tras rechazar texto antiguo, igual texto con tiempos nuevos sigue sin procesarse.')
    print('Control J usa otro cuento construido, de 61 palabras; se comprueba que la frase ambigua no activa la regla nueva.')
    (folder / 'resumen.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    lines = ['# Recuperación global exacta', '', report['notice'], '', report['rule'], '',
             '| Caso | Ventana | Ronda | Cambios de posición respecto a combinación | Final combinación | Final nuevo |', '|---|---:|---:|---:|---:|---:|']
    for r in report['runs']:
        lines.append(f"| {r['case']} | {r['window_seconds']} | {r['repeat']} | {len(r['changes_from_combined'])} | {r['variants']['combinada']['final_position']} | {r['variants']['recuperacion_exacta']['final_position']} |")
    lines += ['', '## Controles sintéticos', '']
    for control in report['synthetic_controls']:
        lines.append(f"- {control['case']}: {control['combined_positions']} → {control['new_positions']}; recuperaciones nuevas {control['fast_recoveries']}.")
    lines += ['', 'No se cambia la política de texto idéntico. El control I conserva esa limitación. Exactitud y unicidad no prueban nueva habla: los tiempos ASR pueden fallar o el reconocedor inventar texto del cuento. No se mide generalización ni latencia real.']
    (folder / 'resumen.md').write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print(f'\nInformes: {folder}')
    print('No se activa en el seguidor habitual ni se publica. Pendiente de comprobacion compartida.')


if __name__ == '__main__':
    main()
