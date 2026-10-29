"""Guiar una tanda de lecturas; el usuario inicia cada grabación con Enter."""
import argparse
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
PLAN = ROOT / 'datos/textos/lectura_04_tomas.json'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--plan', type=Path, default=PLAN, help='Consignas de la tanda en JSON.')
    parser.add_argument('--listar', action='store_true', help='Mostrar consignas sin acceder al micrófono.')
    parser.add_argument('--desde', type=int, default=1)
    parser.add_argument('--hasta', type=int)
    parser.add_argument('--lector', default='adulto_01', help='Identificador anónimo del lector.')
    parser.add_argument('--ambiente', help='Condiciones reales de esta tanda, por ejemplo habitación tranquila.')
    parser.add_argument('--dispositivo', type=int, help='Índice del micrófono; por defecto el habitual.')
    args = parser.parse_args()
    plan = json.loads(args.plan.read_text(encoding='utf-8'))
    total = len(plan['takes'])
    if not total or [t['number'] for t in plan['takes']] != list(range(1,total+1)):
        parser.error('Las tomas del plan deben estar numeradas consecutivamente desde 1.')
    if args.hasta is None:
        args.hasta = total
    if not 1 <= args.desde <= args.hasta <= total:
        parser.error(f'El intervalo debe estar entre 1 y {total}, con --desde <= --hasta.')
    if any(not 1 <= t['seconds'] <= 600 for t in plan['takes']):
        parser.error('Cada toma debe durar entre 1 y 600 segundos.')
    story = ROOT / plan['story_file']
    text = story.read_text(encoding='utf-8').strip()
    print(f"{plan['title']} · {len(text.split())} palabras", flush=True)
    print('Enter inicia cada toma; otro Enter la termina y guarda. El tiempo indicado es el máximo.', flush=True)
    print('No digas títulos ni consignas. No uses Ctrl+C para terminar y guardar una toma.', flush=True)
    for take in plan['takes']:
        if not args.desde <= take['number'] <= args.hasta:
            continue
        print(f"\nTOMA {take['number']}/{total} · {take['label']} · {take['seconds']} s", flush=True)
        print(take['instructions'], flush=True)
        if args.listar:
            continue
        command = [sys.executable, '-u', '-m', 'scripts.grabar',
                   '--cuento', str(story), '--segundos', str(take['seconds']),
                   '--parar-con-enter',
                   '--nombre', take['label'], '--caso', take['case'], '--lector', args.lector]
        if args.ambiente:
            command += ['--ambiente', args.ambiente]
        if args.dispositivo is not None:
            command += ['--dispositivo', str(args.dispositivo)]
        result = subprocess.run(command, cwd=ROOT)
        if result.returncode:
            raise SystemExit(f"Tanda detenida en toma {take['number']}. Reanuda con el mismo --plan y --desde {take['number']}.")
    if not args.listar:
        print('\nTanda terminada. Comprueba las rutas Guardado; el contenido queda pendiente de escucha.', flush=True)
        print('No se ha ejecutado ningún reconocedor.', flush=True)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        raise SystemExit('\nTanda interrumpida. La toma en curso puede no haberse guardado; las anteriores se conservan.')
