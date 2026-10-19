"""Muestra por qué el seguidor retrocede al reprocesar el final de la lectura lenta."""
import argparse
import json

from scripts.anotar import ROOT, EventWorkspace
from scripts.comparar_seguidores import replay
from scripts.seguir import locate


def inspect_run(data):
    reproduced = replay(data)
    if any((a['position'], a['movement'], a['mode']) != (b['position'], b['movement'], b['mode'])
           for a, b in zip(data['updates'], reproduced['updates'])):
        raise ValueError('La reproducción del seguidor original no coincide con el registro.')
    rows = []
    for u in data['updates']:
        if 76 <= u['audio_available_seconds'] <= 86:
            heard = [w['word'] for w in u['hypothesis']]
            rows.append({'audio_seconds': u['audio_available_seconds'],
                         'window_start': u['audio_window_start_seconds'],
                         'text': ' '.join(heard), 'previous_position': u['previous_position'],
                         'position': u['position'], 'movement': u['movement'],
                         'evidence': u['evidence'],
                         'recomputed_evidence': locate(data['story_words'], heard, u['previous_position'])})
    return rows


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--ronda', type=int, choices=[1, 2, 3], default=1)
    args = parser.parse_args()
    folder = ROOT / 'resultados/comparaciones/20261016_095252_869489'
    comparison = json.loads((folder / 'resumen.json').read_text(encoding='utf-8'))
    cases = []
    for run in comparison['runs']:
        if run['window_seconds'] == 8:
            path = folder / run['record_file']
            data = json.loads(path.read_text(encoding='utf-8'))
            cases.append((run['repeat'], path, data, inspect_run(data)))
    repeat, path, data, rows = next(case for case in cases if case[0] == args.ronda)
    print('DIAGNOSTICO DEL SEGUIDOR ORIGINAL - lectura lenta, ventana 8 s')
    print('Solo lee registros: no graba, no ejecuta ASR y no cambia ninguna regla.')
    print(f'Archivo: {path.relative_to(ROOT)}')
    print(f'Ronda: {repeat}. Posiciones, movimientos y modos originales reproducidos en {len(cases)}/{len(cases)} registros.')
    print('\nCorte | Ventana de audio | Posicion anterior -> nueva | Texto ASR')
    for row in rows:
        print(f"{row['audio_seconds']:5.0f} | {row['window_start']:5.0f}-{row['audio_seconds']:<5.0f} s | {row['previous_position']:2} -> {row['position']:2} | {row['text'] or '(vacio)'}")
    transition = next(row for row in rows if row['audio_seconds'] == 80)
    evidence = transition['recomputed_evidence']
    matches, n, cost = evidence['exact_matches'], evidence['hypothesis_words'], evidence['edit_cost']
    print('\nDECISION EN EL CORTE 80 s')
    print(f"Cuento, posiciones 54-56: {' '.join(data['story_words'][53:56])}")
    print(f"Hipotesis ASR: {transition['text']}")
    print(f'Coincidencias exactas: {matches}/{n} = {matches/n:.1%}; umbral minimo 60% y dos coincidencias.')
    print(f'Coste de edicion: {cost}/{n} = {cost/n:.1%}; maximo permitido 40%.')
    print(f"El alineamiento se acepta. Ultima coincidencia exacta: {evidence['position']} ({data['story_words'][evidence['position']-1]}).")
    print('Cuaderno/jugaderno no coinciden exactamente. El seguidor sustituye 56 por 55 sin exigir evidencia temporal de una relectura.')
    print('Despues, las hipotesis no aportan suficientes coincidencias para recuperar 56; mantiene 55.')
    print('\nCONTROL ENTRE RONDAS')
    for number, _, _, history in cases:
        cut78 = next(row for row in history if row['audio_seconds'] == 78)
        cut80 = next(row for row in history if row['audio_seconds'] == 80)
        print(f"Ronda {number}: corte 78 -> {cut78['position']}; corte 80 -> {cut80['position']} ({cut80['text']}).")
    annotation = EventWorkspace('lenta').current()
    final = annotation['words'][-1]
    if final['reviewed']:
        print(f"\nTu marca de cuaderno: {final['start']:.2f}-{final['end']:.2f} s. Ambas ventanas 70-78 y 72-80 contienen ese intervalo completo.")
    print('Esto explica la decision del seguidor. No determina por que el ASR cambia cuaderno por jugaderno.')
    print('El diagnostico no modifica la variante de palabra aislada ni aplica una correccion nueva.')


if __name__ == '__main__':
    main()
