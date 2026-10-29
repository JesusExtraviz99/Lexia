"""Elegir texto y lector y guardar una única grabación; sin ejecutar ASR."""
import argparse
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
TYPES = [
    ('Lectura normal', 'normal'),
    ('Lectura lenta', 'lenta'),
    ('Lectura rápida', 'otro'),
    ('Lectura con pausas', 'pausa'),
    ('Lectura con relecturas', 'relectura'),
    ('Lectura con disfluencias', 'disfluencias'),
    ('Otro tipo (describir)', 'otro'),
]


def choose(prompt, count):
    while True:
        value = input(prompt).strip()
        if value.isdecimal() and 1 <= int(value) <= count:
            return int(value) - 1
        print(f'Escribe un número entre 1 y {count}.')


def required(prompt, reader=False):
    while True:
        value = input(prompt).strip()
        if reader and not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_-]{0,31}', value):
            print('Usa un ID de hasta 32 letras sin tildes, números, guiones o guion bajo; por ejemplo lector_02.')
        elif value and not any(c in value for c in '<>:"/\\|?*'):
            return value
        else:
            print('Introduce una descripción sin caracteres de rutas de archivo.')


def build_command(story, label, case, reader, environment, device=None):
    command = [sys.executable, '-u', '-m', 'scripts.grabar',
               '--cuento', str(story), '--nombre', label, '--caso', case,
               '--lector', reader, '--segundos', '600', '--parar-con-enter']
    if environment:
        command += ['--ambiente', environment]
    if device is not None:
        command += ['--dispositivo', str(device)]
    return command


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--listar', action='store_true', help='Mostrar los textos sin activar el micrófono.')
    parser.add_argument('--dispositivo', type=int, help='Índice del micrófono; por defecto el habitual.')
    args = parser.parse_args()
    stories = sorted((ROOT / 'datos/textos').glob('lectura_*.txt'))
    if not stories:
        parser.error('No se encuentran textos en datos/textos.')
    print('TEXTOS DISPONIBLES', flush=True)
    for number, story in enumerate(stories, 1):
        text = story.read_text(encoding='utf-8-sig').strip()
        print(f'{number}. {story.stem} · {len(text.split())} palabras · {text[:85]}…')
    if args.listar:
        return
    print('\nSe hará UNA grabación. Ctrl+C cancela; Enter durante la captura termina y guarda.')
    story = stories[choose('Número del texto: ', len(stories))]
    reader = required('ID del lector (ej. lector_02; reutiliza el mismo ID para esa persona): ', reader=True)
    print('\nTIPO DE LECTURA')
    for number, (label, _) in enumerate(TYPES, 1):
        print(f'{number}. {label}')
    label, case = TYPES[choose('Número del tipo de lectura: ', len(TYPES))]
    if label.startswith('Otro tipo'):
        label = required('Describe el tipo de lectura: ')[:70]
    environment = input('Ambiente o ruido de fondo (opcional, Enter para omitir): ').strip()
    print(f'\nTexto: {story.stem} | Lector: {reader} | Tipo: {label}', flush=True)
    print('El texto completo aparecerá a continuación. Límite de seguridad: 10 minutos.', flush=True)
    result = subprocess.run(build_command(story, label, case, reader, environment, args.dispositivo), cwd=ROOT)
    if result.returncode:
        raise SystemExit(result.returncode)
    print('\nGrabación finalizada. No se ejecuta ningún reconocedor ni se inicia otra toma.', flush=True)


if __name__ == '__main__':
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        raise SystemExit('\nGrabación cancelada. Comprueba si llegó a mostrarse una ruta Guardado.')
