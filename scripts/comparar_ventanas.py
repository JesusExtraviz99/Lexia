"""Compara prefijos y ventanas de 6 y 10 s sobre los mismos WAV."""
import argparse
from datetime import datetime
import json
import math
from pathlib import Path
import statistics
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]


def summarize(data):
    updates = data["updates"]
    times = [r["processing_seconds"] for r in updates]
    p95 = sorted(times)[max(0, math.ceil(0.95*len(times))-1)]
    reached = next((r["audio_available_seconds"] for r in updates
                    if r["position"] == len(data["story_words"])), None)
    return {"updates": len(updates), "processing_total_seconds": sum(times),
            "processing_median_seconds": statistics.median(times), "processing_p95_seconds": p95,
            "audio_reprocessed_total_seconds": sum(r["audio_reprocessed_seconds"] for r in updates),
            "over_block_updates": sum(t > data["block_seconds"] for t in times),
            "max_backlog_seconds_simulated": max(r["backlog_seconds_simulated"] for r in updates),
            "final_ready_seconds_simulated": updates[-1]["sequential_ready_seconds_simulated"],
            "final_position": updates[-1]["position"], "first_final_position_audio_seconds": reached,
            "backward_moves": sum(r["movement"] < 0 for r in updates),
            "holds": sum(r["movement"] == 0 for r in updates)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("audio", nargs="?", type=Path)
    parser.add_argument("--todos", action="store_true", help="Procesar los dos WAV de prueba.")
    args = parser.parse_args()
    if args.audio and args.todos:
        parser.error("Elige un audio o --todos.")
    files = sorted((ROOT / "datos/audio").glob("*.wav"))
    if args.audio:
        files = [args.audio.resolve()]
    elif not args.todos:
        files = files[-1:]
    if not files:
        parser.error("No hay grabaciones.")
    folder = ROOT / "resultados/comparaciones" / datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    folder.mkdir(parents=True)
    result = {"block_seconds": 2, "windows_seconds": [0, 6, 10],
              "notice": "Una ejecución por configuración en orden fijo. Tiempos orientativos, afectados por carga y calentamiento. No hay referencia humana de posición ni latencia visual. Comparar posiciones entre métodos no demuestra precisión.",
              "runs": []}
    try:
        for audio in files:
            for window in (0, 6, 10):
                label = "prefijo" if not window else f"ventana_{window}s"
                path = folder / f"{audio.stem}_{label}.json"
                print(f"\nComparando {audio.name}: {label}", flush=True)
                subprocess.run([sys.executable, "-u", str(ROOT / "scripts/seguir.py"), str(audio),
                                "--ventana", str(window), "--salida", str(path)], check=True, cwd=ROOT)
                data = json.loads(path.read_text(encoding="utf-8"))
                result["runs"].append({"audio": audio.name, "method": label, "window_seconds": window,
                                       "record_file": path.name, **summarize(data)})
                (folder / "resumen.json").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    except subprocess.CalledProcessError as exc:
        raise SystemExit(f"La comparación se interrumpió ({exc.returncode}). Se conservan los registros en {folder}.")
    lines = ["# Comparación de reprocesamiento", "", result["notice"], "",
             "Mismo modelo, CPU int8, VAD, bloques de 2 s, cuento y seguidor. La carga del modelo se excluye de los tiempos de inferencia. El solapamiento es 4 s en la ventana de 6 s y 8 s en la de 10 s.", "",
             "| Audio | Método | Total inferencia (s) | Mediana (s) | P95 (s) | Inferencias >2 s | Cola máxima simulada (s) | Posición final | Retrocesos |",
             "|---|---|---:|---:|---:|---:|---:|---:|---:|"]
    for r in result["runs"]:
        lines.append(f"| {r['audio']} | {r['method']} | {r['processing_total_seconds']:.2f} | {r['processing_median_seconds']:.2f} | {r['processing_p95_seconds']:.2f} | {r['over_block_updates']} | {r['max_backlog_seconds_simulated']:.2f} | {r['final_position']} | {r['backward_moves']} |")
    lines += ["", "## Posiciones en cada actualización", "",
              "Comparación descriptiva con el prefijo, no referencia de precisión. El prefijo también puede equivocarse."]
    for audio in files:
        runs = [r for r in result["runs"] if r["audio"] == audio.name]
        histories = [json.loads((folder / r["record_file"]).read_text(encoding="utf-8"))["updates"] for r in runs]
        lines += ["", f"### {audio.name}", "", "| Audio disponible (s) | Prefijo | Ventana 6 s | Ventana 10 s |", "|---:|---:|---:|---:|"]
        for entries in zip(*histories):
            lines.append(f"| {entries[0]['audio_available_seconds']:.1f} | " + " | ".join(str(e["position"] or "—") for e in entries) + " |")
    report = folder / "resumen.md"
    report.write_text("\n".join(lines)+"\n", encoding="utf-8")
    print("\nResumen (tiempos de inferencia, sin carga del modelo):", flush=True)
    for r in result["runs"]:
        print(f"{r['audio']} | {r['method']} | total {r['processing_total_seconds']:.2f}s | mediana {r['processing_median_seconds']:.2f}s | >2s: {r['over_block_updates']} | cola max. {r['max_backlog_seconds_simulated']:.2f}s | posicion final {r['final_position']}", flush=True)
    print("\nComparación terminada. Informe:", report, flush=True)


if __name__ == "__main__":
    main()
