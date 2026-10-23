"""Añade fichas de cómputo a informes sin reescribir los JSON originales."""
import argparse
from datetime import datetime
import json
from pathlib import Path

from scripts.seguir import ROOT
from scripts.archivos import write_text_atomic
from scripts.recursos import hardware_snapshot, write_resource_report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('carpeta', nargs='?', type=Path)
    parser.add_argument('--todos', action='store_true', help='Informes con registros de ASR identificables.')
    parser.add_argument('--inventario', action='store_true', help='Medir el equipo ahora, separado de las pruebas históricas.')
    args = parser.parse_args()
    if args.todos and args.carpeta:
        parser.error('Elige una carpeta o --todos.')
    if not (args.todos or args.carpeta or args.inventario):
        parser.error('Indica carpeta, --todos o --inventario.')
    if args.inventario:
        folder = ROOT/'resultados/recursos_equipo'/datetime.now().strftime('%Y%m%d_%H%M%S_%f')
        folder.mkdir(parents=True)
        snapshot = hardware_snapshot()
        snapshot['notice'] = 'Inventario actual, no medición de ejecuciones anteriores ni consumo específico del ASR. No representa una tablet.'
        write_text_atomic(folder/'equipo.json', json.dumps(snapshot,ensure_ascii=False,indent=2)+'\n')
        print(f'Inventario actual: {folder / "equipo.json"}')
    folders = [p.parent for p in (ROOT/'resultados').glob('*/*/resumen.json')] if args.todos else [args.carpeta.resolve()] if args.carpeta else []
    total = 0
    for folder in folders:
        count = write_resource_report(folder, ROOT)
        if count:
            print(f'{folder.relative_to(ROOT)}: {count} registros, recursos_computo.md/json')
            total += 1
    print(f'Informes complementados: {total}. No se ejecuta ASR ni se modifica ningún JSON original.')


if __name__ == '__main__':
    main()
