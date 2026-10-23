"""Grabación local iniciada explícitamente por el usuario."""
import argparse
from datetime import datetime
from pathlib import Path
import sounddevice as sd
import soundfile as sf
try:
    from .catalogo import register_recording, resolve_audio_path
except ImportError:
    from catalogo import register_recording, resolve_audio_path

ROOT = Path(__file__).resolve().parents[1]

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
    args = parser.parse_args()
    if args.dispositivos:
        print(sd.query_devices())
        return
    if not 1 <= args.segundos <= 300:
        parser.error("La duración debe estar entre 1 y 300 segundos.")
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
    input(f"Pulsa Enter para grabar durante {args.segundos} segundos. ")
    print("Grabando... Lee el texto en voz alta.")
    audio = sd.rec(args.segundos * rate, samplerate=rate, channels=1,
                   dtype="float32", device=args.dispositivo)
    sd.wait()
    folder = ROOT / "datos/audio"
    folder.mkdir(parents=True, exist_ok=True)
    path = folder / f"lectura_{datetime.now():%Y%m%d_%H%M%S_%f}.wav"
    sf.write(path, audio, rate, subtype="PCM_16")
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
