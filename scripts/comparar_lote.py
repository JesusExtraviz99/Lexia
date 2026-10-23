"""Comparación secuencial de grabaciones catalogadas de una fecha y un cuento."""
import argparse
from datetime import datetime
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

from scripts.archivos import write_text_atomic
from scripts.catalogo import ROOT, read_catalog


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--fecha', required=True, help='Fecha de grabación AAAA-MM-DD.')
    parser.add_argument('--cuento', type=Path, required=True)
    parser.add_argument('--ventanas', type=int, nargs='+', default=[4, 8])
    parser.add_argument('--repeticiones', type=int, default=3)
    args = parser.parse_args()
    story = args.cuento.resolve()
    story_hash = digest(story)
    if not 1 <= args.repeticiones <= 5 or len(set(args.ventanas)) != len(args.ventanas) or any(w != 0 and not 2 <= w <= 120 for w in args.ventanas):
        parser.error('Revisa ventanas y repeticiones.')
    selected, unavailable = [], []
    for row in read_catalog()['recordings']:
        if row.get('recorded_date') != args.fecha or row.get('story_sha256') != story_hash:
            continue
        path = ROOT/row['audio_file']
        if not path.is_file() or digest(path) != row['audio_sha256']:
            unavailable.append(row['id'])
            continue
        selected.append(row)
    if not selected:
        parser.error('No hay WAV coincidentes con fecha, cuento y huella.')
    folder = ROOT/'resultados/lotes'/datetime.now().strftime('%Y%m%d_%H%M%S_%f')
    folder.mkdir(parents=True)
    manifest = {'status': 'en_curso', 'story_file': str(story), 'story_sha256': story_hash,
                'date_selection': args.fecha, 'windows': args.ventanas, 'repetitions': args.repeticiones,
                'unavailable_catalog_ids': unavailable,
                'notice': 'Comparación exploratoria. Nombres describen consignas; contenido pendiente de revisión. Tres rondas son cómputo del mismo audio. Sin referencia humana no mide precisión. No activa reglas experimentales.',
                'recordings': [{**r, 'comparison_folder': r['id'], 'status': 'pendiente'} for r in selected]}
    def save():
        write_text_atomic(folder/'lote.json', json.dumps(manifest, ensure_ascii=False, indent=2)+'\n')
    save()
    print('LOTE:', folder, flush=True)
    print(f'{len(selected)} WAV; {len(selected)*len(args.ventanas)*args.repeticiones} ejecuciones secuenciales.', flush=True)
    for index, row in enumerate(manifest['recordings'], 1):
        audio = ROOT/row['audio_file']
        if digest(audio) != row['audio_sha256'] or digest(story) != story_hash:
            raise ValueError('Audio o cuento cambiaron durante el lote.')
        print(f"[{index}/{len(selected)}] {audio.name}", flush=True)
        row['status'] = 'en_curso'
        save()
        command = [sys.executable, '-u', '-m', 'scripts.comparar_ventanas', str(audio),
                   '--cuento', str(story), '--ventanas', *map(str,args.ventanas),
                   '--repeticiones', str(args.repeticiones), '--carpeta-salida', str(folder/row['comparison_folder'])]
        with (folder/f"{row['id']}.log").open('w', encoding='utf-8') as log:
            process = subprocess.run(command, cwd=ROOT, stdout=log, stderr=subprocess.STDOUT,
                                     env={**os.environ, 'PYTHONIOENCODING': 'utf-8'})
        row['exit_code'] = process.returncode
        row['status'] = 'completo' if process.returncode == 0 else 'error'
        save()
        print(f"  {row['status']}: {row['comparison_folder']}", flush=True)
    manifest['status'] = 'completo' if all(r['status']=='completo' for r in manifest['recordings']) else 'con_errores'
    lines = ['# Comparación de grabaciones del segundo cuento', '', manifest['notice'], '',
             '| Audio | Ventana | Finales | Total medio ASR (s) | Cortes >2 s | Cola máxima (s) | Retrocesos por ronda |',
             '|---|---:|---|---:|---|---:|---|']
    for row in manifest['recordings']:
        if row['status'] != 'completo':
            lines.append(f"\nComparación incompleta: {row['audio_file']}; consultar su log.\n")
            continue
        result = json.loads((folder/row['comparison_folder']/'resumen.json').read_text(encoding='utf-8'))
        row['aggregates'] = result['aggregates']
        for a in result['aggregates']:
            runs = [r for r in result['runs'] if r['window_seconds']==a['window_seconds']]
            lines.append(f"| {Path(row['audio_file']).name} | {a['window_seconds']} | {a['final_positions']} | {a['mean_total_seconds']:.2f} | {a['over_block_updates_total']}/{a['updates_total']} | {max(r['max_backlog_seconds_simulated'] for r in runs):.2f} | {[r['backward_moves'] for r in runs]} |")
    lines += ['', 'Los informes de CPU/RAM/GPU y los textos ASR por corte están dentro de cada comparación. ASR en CPU int8; GPU global muestreada no equivale a uso de GPU por ASR.', '',
              'Para cada audio, abrir su carpeta y consultar resumen.md; el registro completo de terminal está en el .log correspondiente.']
    save()
    write_text_atomic(folder/'resumen.md', '\n'.join(lines)+'\n')
    print('RESUMEN:', folder/'resumen.md', flush=True)
    if manifest['status'] != 'completo':
        raise SystemExit(1)


if __name__ == '__main__':
    main()
