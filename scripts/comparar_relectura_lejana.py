"""Contrasta tres seguidores sobre una carpeta explícita de hipótesis guardadas."""
import argparse
from datetime import datetime
import hashlib
import json
from pathlib import Path

from scripts.anotar import ROOT
from scripts.comparar_seguidores import Tracker, CombinedTracker, replay
from scripts.comparar_recuperacion import ExactRecoveryTracker


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('carpeta', type=Path, help='Carpeta de comparar_ventanas con resumen.json.')
    args = parser.parse_args()
    source = args.carpeta.resolve()
    manifest = source / 'resumen.json'
    comparison = json.loads(manifest.read_text(encoding='utf-8'))
    classes = {'original': Tracker, 'combinada': CombinedTracker,
               'nueva': ExactRecoveryTracker}
    report = {'notice': 'Reproducción de hipótesis fijas, sin nuevas inferencias. '
              'Cortes de audio y salida lista simulada son distintos. Sin referencia humana temporal: '
              'no se calcula latencia respecto a la lectura ni precisión. Reglas sin modificar ni activar.',
              'source_manifest': str(manifest), 'source_manifest_sha256': digest(manifest),
              'code_sha256': {name: digest(ROOT / 'scripts' / name) for name in
                             ['seguir.py', 'comparar_seguidores.py', 'comparar_recuperacion.py',
                              'comparar_relectura_lejana.py']}, 'runs': []}
    lines = ['# Relectura lejana: comparación de seguidores', '', report['notice'], '',
             '| Ventana | Ronda | Final original / combinada / nueva | Cortes distintos combinada–nueva | Recuperación exacta (corte s) |',
             '|---:|---:|---|---|---|']
    print('RELECTURA LEJANA: mismos ASR y tiempos guardados; sin nuevas inferencias.')
    for run in comparison['runs']:
        path = (source / run['record_file']).resolve()
        if path.parent != source:
            raise ValueError('Registro fuera de la carpeta indicada.')
        data = json.loads(path.read_text(encoding='utf-8'))
        traces = {name: replay(data, cls) for name, cls in classes.items()}
        if [(u['position'], u['movement'], u['mode']) for u in data['updates']] != [
                (u['position'], u['movement'], u['mode']) for u in traces['original']['updates']]:
            raise ValueError(f'El original no se reproduce: {path}')
        rows = []
        for index, source_row in enumerate(data['updates']):
            rows.append({'audio_seconds': source_row['audio_available_seconds'],
                         'ready_seconds_simulated': source_row['sequential_ready_seconds_simulated'],
                         'asr_text': ' '.join(w['word'] for w in source_row['hypothesis']),
                         'variants': {name: {key: trace['updates'][index][key] for key in
                                           ['position', 'movement', 'mode', 'evidence']}
                                      for name, trace in traces.items()}})
        changed = [r['audio_seconds'] for r in rows if
                   r['variants']['combinada']['position'] != r['variants']['nueva']['position']]
        fast = [r['audio_seconds'] for r in rows if
                r['variants']['nueva']['mode'] == 'recuperacion_global_exacta']
        finals = {name: trace['updates'][-1]['position'] for name, trace in traces.items()}
        report['runs'].append({'source_file': str(path), 'source_sha256': digest(path),
                               'window_seconds': run['window_seconds'], 'repeat': run['repeat'],
                               'baseline_reproduces_original': True, 'final_positions': finals,
                               'changed_cuts': changed, 'fast_recovery_cuts': fast, 'updates': rows})
        label = f"Ventana {run['window_seconds']} s, ronda {run['repeat']}"
        print(f"\n{label}: finales {finals}; recuperación exacta {fast}")
        print('Corte | Original / Combinada / Nueva | Modo nuevo | ASR')
        for row in rows:
            if any(v['movement'] < 0 for v in row['variants'].values()) or row['audio_seconds'] in changed:
                positions = ' / '.join(str(v['position']) for v in row['variants'].values())
                print(f"{row['audio_seconds']:5.1f} | {positions} | {row['variants']['nueva']['mode']} | {row['asr_text']}")
        lines.append(f"| {run['window_seconds']} | {run['repeat']} | {' / '.join(str(p) for p in finals.values())} | {changed} | {fast} |")
    folder = ROOT / 'resultados/relectura_lejana' / datetime.now().strftime('%Y%m%d_%H%M%S_%f')
    folder.mkdir(parents=True)
    (folder / 'resumen.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    (folder / 'resumen.md').write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print(f'\nInformes: {folder}')
    print('Pendiente de revisión compartida y escucha. No se publica ni activa la variante.')


if __name__ == '__main__':
    main()
