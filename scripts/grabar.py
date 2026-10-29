"""Grabación local iniciada explícitamente por el usuario."""
import argparse
from datetime import datetime
from pathlib import Path
import os
import sys
from threading import Event
import numpy as np
import sounddevice as sd
import soundfile as sf
try:
    from .catalogo import register_recording, resolve_audio_path
except ImportError:
    from catalogo import register_recording, resolve_audio_path

ROOT = Path(__file__).resolve().parents[1]


def enter_pressed():
    """Consultar Enter sin dejar un hilo de lectura pendiente al agotar el tiempo."""
    if os.name == 'nt':
        import msvcrt
        while msvcrt.kbhit():
            key = msvcrt.getwch()
            if key == '\x03':
                raise KeyboardInterrupt
            if key in ('\r', '\n'):
                return True
        return False
    import select
    if select.select([sys.stdin], [], [], 0)[0]:
        line = sys.stdin.readline()
        if not line:
            raise ValueError('Entrada de terminal cerrada; no se puede esperar Enter.')
        return True
    return False


def record_until_enter(seconds, rate, device, stop_requested=None):
    """Conservar solo muestras recibidas; Enter guarda, el límite sigue vigente."""
    stop_requested = stop_requested or enter_pressed
    audio = np.empty((seconds * rate, 1), dtype=np.float32)
    count = 0
    finished = Event()
    errors = []

    def callback(indata, frames, timing, status):
        nonlocal count
        if status:
            errors.append(str(status))
        used = min(len(indata), len(audio) - count)
        audio[count:count + used] = indata[:used]
        count += used
        if count == len(audio):
            raise sd.CallbackStop

    with sd.InputStream(samplerate=rate, channels=1, dtype='float32', device=device,
                        callback=callback, finished_callback=finished.set):
        while not finished.wait(0.02):
            if stop_requested():
                break
    if not count:
        raise ValueError('No se han recibido muestras; no se guarda un WAV vacío.')
    if errors:
        print('Avisos de captura:', '; '.join(dict.fromkeys(errors)), flush=True)
    return audio[:count].copy()

def main():
    parser = argparse.ArgumentParser(description="Graba una lectura en WAV local.")
    parser.add_argument("--segundos", type=int, default=40)
    parser.add_argument("--dispositivos", action="store_true")
    parser.add_argument("--dispositivo", type=int)
    parser.add_argument("--cuento", type=Path, default=ROOT / "datos/textos/lectura_01.txt",
                        help="Texto que se muestra antes de grabar.")
    parser.add_argument('--nombre', help='Nombre descriptivo; el catálogo añade fecha e ID estable.')
    parser.add_argument('--caso', default='sin_clasificar', choices=['sin_clasificar','normal','lenta','pausa','relectura','disfluencias','otro'])
    parser.add_argument('--lector', help='Identificador anónimo del lector, por ejemplo adulto_01.')
    parser.add_argument('--ambiente', help='Descripción de condiciones, por ejemplo lluvia de fondo.')
    parser.add_argument('--parar-con-enter', action='store_true', help='Enter termina y guarda; --segundos es el máximo.')
    args = parser.parse_args()
    if args.dispositivos:
        print(sd.query_devices())
        return
    if not 1 <= args.segundos <= 600:
        parser.error("La duración debe estar entre 1 y 600 segundos.")
    try:
        text = args.cuento.read_text(encoding="utf-8-sig").strip()
        if not text:
            raise ValueError("El cuento está vacío.")
    except (OSError, ValueError) as exc:
        parser.error(str(exc))
    device = sd.query_devices(args.dispositivo, "input")
    rate = int(device["default_samplerate"])
    print("Micrófono:", device["name"])
    print("Cuento:", args.cuento.resolve())
    print(text)
    input(f"Pulsa Enter para grabar {'hasta' if args.parar_con_enter else 'durante'} {args.segundos} segundos. ")
    if args.parar_con_enter:
        print('Grabando... Pulsa Enter al terminar para guardar esta toma.', flush=True)
        audio = record_until_enter(args.segundos, rate, args.dispositivo)
    else:
        print("Grabando... Lee el texto en voz alta.")
        audio = sd.rec(args.segundos * rate, samplerate=rate, channels=1,
                       dtype="float32", device=args.dispositivo)
        sd.wait()
    folder = ROOT / "datos/audio"
    folder.mkdir(parents=True, exist_ok=True)
    path = folder / f"lectura_{datetime.now():%Y%m%d_%H%M%S_%f}.wav"
    sf.write(path, audio, rate, subtype="PCM_16")
    print('Duración guardada:', round(len(audio) / rate, 3), 's')
    print("Nivel máximo:", round(float(abs(audio).max()), 4))
    try:
        identity = register_recording(path, args.cuento, args.nombre, args.caso, args.lector, args.ambiente)
        path = resolve_audio_path(path)
        print('Nombre:', identity['label'])
        print('Contenido pendiente de revisión por escucha.')
    except (OSError, ValueError) as exc:
        print(f'El WAV se ha guardado, pero no pudo añadirse al catálogo: {exc}')

    print("Guardado:", path)

if __name__ == "__main__":
    try:
        main()
    except (sd.PortAudioError, ValueError) as exc:
        raise SystemExit(f"No se pudo grabar: {exc}. Consulta --dispositivos.")
