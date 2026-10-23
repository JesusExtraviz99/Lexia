"""Transcribe un archivo local, sin enviar audio a un servicio remoto."""
import argparse
from datetime import datetime
import importlib.metadata
import json
from pathlib import Path
from time import perf_counter
from faster_whisper import WhisperModel
try:
    from .catalogo import audio_identity, resolve_audio_path, report_stem
except ImportError:
    from catalogo import audio_identity, resolve_audio_path, report_stem

ROOT = Path(__file__).resolve().parents[1]

def main():
    parser = argparse.ArgumentParser(description="Transcribe una grabación con el modelo local.")
    parser.add_argument("audio", nargs="?", type=Path)
    args = parser.parse_args()
    audio = args.audio
    if audio is None:
        recordings = sorted((ROOT / "datos/audio").glob("*.wav"), key=lambda p: p.stat().st_mtime_ns)
        if not recordings:
            parser.error("No hay grabaciones. Ejecuta primero scripts/grabar.py.")
        audio = recordings[-1]
    audio = resolve_audio_path(audio).resolve()
    if not audio.is_file():
        parser.error(f"No existe el audio: {audio}")
    print('Audio:', audio_identity(audio)['label'], '|', audio.name)
    model_path = ROOT / "modelos/faster-whisper-small"
    if not (model_path / "model.bin").is_file():
        parser.error("Falta el modelo. Ejecuta scripts/preparar_modelo.py.")
    load_start = perf_counter()
    model = WhisperModel(str(model_path), device="cpu", compute_type="int8", local_files_only=True)
    load_seconds = perf_counter() - load_start
    start = perf_counter()
    segments, info = model.transcribe(str(audio), language="es", beam_size=5,
                                      word_timestamps=True, vad_filter=False,
                                      condition_on_previous_text=False)
    items = []
    for segment in segments:
        print(f"[{segment.start:.2f}–{segment.end:.2f}] {segment.text}")
        items.append({"start": segment.start, "end": segment.end, "text": segment.text,
                      "words": [{"word": w.word, "start": w.start, "end": w.end,
                                 "probability": w.probability} for w in (segment.words or [])]})
    seconds = perf_counter() - start
    data = {"audio": str(audio), "model": "Systran/faster-whisper-small",
            "device": "cpu", "compute_type": "int8", "language": "es",
            "beam_size": 5, "vad_filter": False, "condition_on_previous_text": False,
            "faster_whisper_version": importlib.metadata.version("faster-whisper"),
            "audio_seconds": info.duration, "model_load_seconds": load_seconds,
            "processing_seconds": seconds, "segments": items,
            "notice": "Transcripción posterior; no mide latencia visible ni exactitud del cursor."}
    folder = ROOT / "resultados"
    folder.mkdir(parents=True, exist_ok=True)
    output = folder / f"{report_stem(audio)}_{datetime.now():%Y%m%d_%H%M%S_%f}.json"
    output.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Procesamiento: {seconds:.2f} s. Carga del modelo: {load_seconds:.2f} s.")
    print("Resultado:", output)

if __name__ == "__main__":
    main()
