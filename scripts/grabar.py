"""Grabación local iniciada explícitamente por el usuario."""
import argparse
from datetime import datetime
from pathlib import Path
import sounddevice as sd
import soundfile as sf

ROOT = Path(__file__).resolve().parents[1]

def main():
    parser = argparse.ArgumentParser(description="Graba una lectura en WAV local.")
    parser.add_argument("--segundos", type=int, default=40)
    parser.add_argument("--dispositivos", action="store_true")
    parser.add_argument("--dispositivo", type=int)
    args = parser.parse_args()
    if args.dispositivos:
        print(sd.query_devices())
        return
    if not 1 <= args.segundos <= 300:
        parser.error("La duración debe estar entre 1 y 300 segundos.")
    device = sd.query_devices(args.dispositivo, "input")
    rate = int(device["default_samplerate"])
    print("Micrófono:", device["name"])
    print((ROOT / "datos/textos/lectura_01.txt").read_text(encoding="utf-8"))
    input(f"Pulsa Enter para grabar durante {args.segundos} segundos. ")
    print("Grabando... Lee el texto en voz alta.")
    audio = sd.rec(args.segundos * rate, samplerate=rate, channels=1,
                   dtype="float32", device=args.dispositivo)
    sd.wait()
    folder = ROOT / "datos/audio"
    folder.mkdir(parents=True, exist_ok=True)
    path = folder / f"lectura_{datetime.now():%Y%m%d_%H%M%S_%f}.wav"
    sf.write(path, audio, rate, subtype="PCM_16")
    print("Guardado:", path)
    print("Nivel máximo:", round(float(abs(audio).max()), 4))

if __name__ == "__main__":
    try:
        main()
    except (sd.PortAudioError, ValueError) as exc:
        raise SystemExit(f"No se pudo grabar: {exc}. Consulta --dispositivos.")
