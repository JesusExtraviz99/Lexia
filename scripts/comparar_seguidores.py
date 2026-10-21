"""Reproduce hipótesis guardadas para aislar una variante experimental del seguidor."""
from copy import deepcopy
import argparse
from datetime import datetime
import hashlib
import json
import math
from pathlib import Path
from time import perf_counter

from scripts.alinear import normalize, tokens
from scripts.anotar import ROOT, Workspace, EventWorkspace
from scripts.seguir import Tracker, locate
from scripts.evaluar_seguimiento import evaluate as evaluate_normal
from scripts.evaluar_pausa import evaluate as evaluate_pause
from scripts.evaluar_lenta import evaluate as evaluate_slow
from scripts.evaluar_relectura import evaluate as evaluate_repeat


class SingleWordTracker(Tracker):
    """Solo acepta una palabra aislada larga, exacta, única localmente y consecutiva.

    Variante de desarrollo: no sustituye el Tracker que se usa al transcribir.
    No usa tiempos humanos, etiquetas del caso ni palabras específicas del cuento.
    """
    def update(self, hypothesis):
        if len(hypothesis) == 1 and 0 < self.position < len(self.story):
            heard = normalize(hypothesis[0])
            start, stop = max(0, self.position - 12), min(len(self.story), self.position + 24)
            matches = [i + 1 for i in range(start, stop) if normalize(self.story[i]) == heard]
            if len(heard) >= 5 and matches == [self.position + 1]:
                old = self.position
                self.position += 1
                self.failures = 0
                self.recovery_candidate = None
                return {'previous_position': old, 'position': self.position,
                        'word': self.story[self.position - 1], 'movement': 1,
                        'mode': 'palabra_aislada_consecutiva',
                        'evidence': {'exact_matches': 1, 'hypothesis_words': 1,
                                     'reason': 'larga_exacta_unica_local_y_consecutiva'}}
        return super().update(hypothesis)


class TemporalBacktrackTracker(Tracker):
    """Rechaza retrocesos cuya coincidencia exacta no aporta un tiempo ASR posterior.

    No usa referencias humanas. La marca temporal es una estimación del ASR,
    no una prueba de nueva habla. No combina la regla de palabra aislada.
    """
    def __init__(self, story):
        super().__init__(story)
        self.latest_support_end = None

    def update_timed(self, hypothesis):
        for w in hypothesis:
            if any(not isinstance(w.get(k), (int, float)) or not math.isfinite(w[k]) for k in ['start', 'end']):
                raise ValueError('La variante temporal necesita tiempos ASR finitos.')
            if not 0 <= w['start'] <= w['end']:
                raise ValueError('Intervalo ASR inválido.')
        old = (self.position, self.failures, self.recovery_candidate)
        heard = [w['word'] for w in hypothesis]
        state = super().update(heard)
        if state['mode'] == 'palabra_aislada_consecutiva':
            matched = {'position': state['position'], 'matched_hypothesis_index': 0}
        elif state['evidence'].get('position') is None:
            return state
        else:
            matched = locate(self.story, heard, old[0], global_search=state['mode'] == 'recuperacion', include_match_index=True)
        index = matched.get('matched_hypothesis_index')
        if matched['position'] != state['position'] or index is None:
            raise ValueError('No se pudo reproducir la coincidencia temporal del candidato.')
        candidate_end = hypothesis[index]['end']
        state['evidence'] = {**state['evidence'], 'matched_asr_end_seconds': candidate_end,
                             'previous_support_end_seconds': self.latest_support_end}
        if state['movement'] < 0 and self.latest_support_end is not None and candidate_end <= self.latest_support_end:
            self.position, self.failures, self.recovery_candidate = old
            state.update(position=self.position, word=self.story[self.position-1], movement=0,
                         mode='retroceso_sin_tiempo_nuevo')
            state['evidence']['rejected_position'] = matched['position']
        else:
            self.latest_support_end = max(candidate_end, self.latest_support_end or 0)
        return state


class CombinedTracker(TemporalBacktrackTracker, SingleWordTracker):
    """Combina ambas reglas sin alterar sus parámetros; no se activa en seguir.py.

    La envoltura temporal llama a la regla de palabra aislada y conserva también
    el respaldo temporal de los avances aceptados por esa regla.
    """


def replay(data, tracker_class=Tracker):
    """Misma política de hipótesis sin cambios que seguir.py; tiempos ASR reutilizados."""
    output = deepcopy(data)
    tracker = tracker_class(data['story_words'])
    previous_words = []
    elapsed = 0.0
    for row in output['updates']:
        heard = [w['word'] for w in row['hypothesis']]
        tick = perf_counter()
        state = ((tracker.update_timed(row['hypothesis']) if isinstance(tracker, TemporalBacktrackTracker) else tracker.update(heard)) if heard != previous_words else
                 {'previous_position': tracker.position, 'position': tracker.position or None,
                  'word': tracker.story[tracker.position - 1] if tracker.position else None,
                  'movement': 0, 'mode': 'hipotesis_sin_cambios', 'evidence': {}})
        elapsed += perf_counter() - tick
        row.update(state)
        previous_words = heard
    output['replay'] = {'tracker': tracker_class.__name__, 'tracker_update_seconds_measured': elapsed,
                        'notice': 'Hipótesis y tiempos ASR/cola reutilizados. No son medidas nuevas de inferencia ni de latencia total. No se usan anclas humanas para decidir movimientos.'}
    return output


CASES = [
    ('normal', '20261019_084114_510023', {4, 6, 8}),
    ('desviaciones', '20261014_100148_765908', {4, 6, 8}),
    ('pausa', '20261014_111548_094194', {4, 8}),
    ('lenta', '20261016_095252_869489', {4, 8}),
    ('relectura', '20261016_104206_415649', {4, 8}),
]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--variante', choices=['palabra_aislada', 'temporal'], default='palabra_aislada')
    args = parser.parse_args()
    variant_class = TemporalBacktrackTracker if args.variante == 'temporal' else SingleWordTracker
    variant_label = args.variante
    annotations = {'normal': Workspace().current(),
                   **{case: EventWorkspace(case).current() for case in ['pausa', 'lenta', 'relectura']}}
    story = tokens((ROOT / 'datos/textos/lectura_01.txt').read_text(encoding='utf-8'))
    folder = ROOT / ('resultados/retrocesos' if args.variante == 'temporal' else 'resultados/seguidores') / datetime.now().strftime('%Y%m%d_%H%M%S_%f')
    folder.mkdir(parents=True)
    report = {'notice': 'Experimento de desarrollo sobre hipótesis ASR fijas. Cambia solo el seguidor. ASR, ventanas, cortes y tiempos de inferencia permanecen reutilizados. Las métricas de salida visible son una comparación bajo esos tiempos, no latencia nueva medida. Una mejora en estos audios usados para diseñar la regla no prueba generalización. Variante no activada en seguir.py.',
              'rule': 'Una sola palabra ASR, al menos cinco caracteres normalizados, coincidencia exacta única en la ventana local y exactamente la siguiente palabra del cuento, con posición previa distinta de cero. El resto conserva el comportamiento original.',
              'code_sha256': {name: hashlib.sha256((ROOT / 'scripts' / name).read_bytes()).hexdigest()
                              for name in ['seguir.py', 'comparar_seguidores.py']},
              'annotations': {case: {'audio_sha256': annotation['audio_sha256'],
                                      'annotation_sha256': hashlib.sha256((ROOT / 'datos/anotaciones' /
                                          ('lectura_normal.json' if case == 'normal' else f'lectura_{case}_fragmentos.json')).read_bytes()).hexdigest(),
                                      'reviewed_intervals': annotation.get('reviewed_intervals'),
                                      'reviewed_words': annotation.get('reviewed_words')}
                              for case, annotation in annotations.items()},
              'runs': []}
    if args.variante == 'temporal':
        report['rule'] = 'Solo para retrocesos: el final ASR de la última coincidencia exacta debe ser posterior a la marca de apoyo temporal ya aceptada. No se combina la regla de palabra aislada ni se usan tiempos humanos. Umbral sin tolerancia, provisional y sensible a errores de timestamps. Conserva la política original de no actualizar ante texto idéntico.'
    for case, source_folder, windows in CASES:
        source = ROOT / 'resultados/comparaciones' / source_folder
        comparison = json.loads((source / 'resumen.json').read_text(encoding='utf-8'))
        for run in comparison['runs']:
            if run['window_seconds'] not in windows:
                continue
            path = source / run['record_file']
            original = json.loads(path.read_text(encoding='utf-8'))
            baseline = replay(original)
            if any((a['position'], a['movement'], a['mode']) != (b['position'], b['movement'], b['mode'])
                   for a, b in zip(original['updates'], baseline['updates'])):
                raise ValueError(f'La reproducción del original no coincide: {path}')
            variant = replay(original, variant_class)
            summary = {'case': case, 'window_seconds': run['window_seconds'], 'repeat': run['repeat'],
                       'source_file': path.relative_to(ROOT).as_posix(),
                       'source_sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
                       'baseline_reproduces_original': True, 'variants': {},
                       'position_changes': [{'audio_seconds': a['audio_available_seconds'],
                                             'baseline': a['position'], 'variant': b['position']}
                                            for a, b in zip(baseline['updates'], variant['updates']) if a['position'] != b['position']]}
            for label, data in [('original', baseline), (variant_label, variant)]:
                filename = f"{case}_{run['window_seconds']}s_r{run['repeat']}_{label}.json"
                (folder / filename).write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
                evaluation = None
                if case == 'normal':
                    evaluation = evaluate_normal(data, annotations[case])
                elif case in ['pausa', 'lenta', 'relectura']:
                    evaluator = {'pausa': evaluate_pause, 'lenta': evaluate_slow, 'relectura': evaluate_repeat}[case]
                    evaluation = evaluator(data, annotations[case], story)
                summary['variants'][label] = {'file': filename, 'evaluation': evaluation,
                    'tracker_update_seconds_measured': data['replay']['tracker_update_seconds_measured'],
                    'single_word_updates': [u['audio_available_seconds'] for u in data['updates'] if u['mode'] == 'palabra_aislada_consecutiva'],
                    'blocked_backward_updates': [u['audio_available_seconds'] for u in data['updates'] if u['mode'] == 'retroceso_sin_tiempo_nuevo'],
                    'final_position': data['updates'][-1]['position']}
            report['runs'].append(summary)
    (folder / 'resumen.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    lines = [f'# Comparación del seguidor: {variant_label}', '', report['notice'], '', report['rule'], '',
             '| Caso | Ventana | Ronda | Cortes con posición distinta | Aplicación de regla (audio s) | Final original | Final variante |', '|---|---:|---:|---:|---|---:|---:|']
    for r in report['runs']:
        a, b = r['variants']['original'], r['variants'][variant_label]
        rule_updates = b['blocked_backward_updates'] if args.variante == 'temporal' else b['single_word_updates']
        lines.append(f"| {r['case']} | {r['window_seconds']} | {r['repeat']} | {len(r['position_changes'])} | {rule_updates} | {a['final_position']} | {b['final_position']} |")
    lines += ['', 'Los JSON de resumen conservan las métricas humanas por variante y los cortes modificados. En desviaciones solo se compara el comportamiento; no se inventa una referencia temporal. Los registros originales permanecen intactos.']
    (folder / 'resumen.md').write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print(folder)
    if args.variante == 'temporal':
        print('\nCOMPARACION TEMPORAL: mismos textos ASR; sin nuevas inferencias.')
        print('Caso | Ventana | Ronda | Cortes distintos | Final original -> variante | Retrocesos rechazados (corte s)')
        for r in report['runs']:
            a, b = r['variants']['original'], r['variants'][variant_label]
            print(f"{r['case']} | {r['window_seconds']} | {r['repeat']} | {len(r['position_changes'])} | {a['final_position']} -> {b['final_position']} | {b['blocked_backward_updates']}")
        print('\nDETALLE DE LAS POSICIONES QUE CAMBIAN')
        for r in report['runs']:
            if r['position_changes']:
                print(f"{r['case']}, ventana {r['window_seconds']}, ronda {r['repeat']}: {r['position_changes']}")
        print('\nLa regla NO esta activada en el seguidor habitual. Tiempos de ASR/cola reutilizados; no son latencia nueva medida.')


if __name__ == '__main__':
    main()
