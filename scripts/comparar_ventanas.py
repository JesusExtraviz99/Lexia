"""Compara ventanas acústicas configurables y repeticiones sobre los mismos WAV."""
import argparse
from datetime import datetime
import json
import math
import random
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


def experiment_plan(windows, repetitions, seed):
    rng = random.Random(seed)
    plan = []
    for repeat in range(1, repetitions+1):
        order = list(windows)
        rng.shuffle(order)
        plan.extend((repeat, window) for window in order)
    return plan


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("audio", nargs="?", type=Path)
    parser.add_argument("--todos", action="store_true", help="Procesar los dos WAV de prueba.")
    parser.add_argument("--ventanas", nargs="+", type=int, default=[0, 6, 10], help="Duraciones en segundos; 0 es prefijo (por defecto: 0 6 10).")
    parser.add_argument("--repeticiones", type=int, default=1, help="Rondas por configuración, entre 1 y 5.")
    parser.add_argument("--semilla", type=int, default=20261014, help="Semilla para reproducir el orden aleatorio.")
    args = parser.parse_args()
    if args.audio and args.todos:
        parser.error("Elige un audio o --todos.")
    if not 1 <= args.repeticiones <= 5:
        parser.error("Las repeticiones deben estar entre 1 y 5.")
    if len(set(args.ventanas)) != len(args.ventanas) or any(w != 0 and not 2 <= w <= 120 for w in args.ventanas):
        parser.error("Las ventanas deben ser únicas y valer 0 o entre 2 y 120 s.")
    files = sorted((ROOT / "datos/audio").glob("*.wav"))
    if args.audio:
        files = [args.audio.resolve()]
    elif not args.todos:
        files = files[-1:]
    if not files:
        parser.error("No hay grabaciones.")
    folder = ROOT / "resultados/comparaciones" / datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    folder.mkdir(parents=True)
    plan = experiment_plan(args.ventanas, args.repeticiones, args.semilla)
    result = {"block_seconds": 2, "windows_seconds": args.ventanas,
              "repetitions": args.repeticiones, "seed": args.semilla,
              "execution_plan": [{"repeat": r, "window_seconds": w} for r, w in plan],
              "notice": f"{args.repeticiones} ronda(s) por configuración, orden aleatorio reproducible por ronda. Ejecución secuencial para no competir por CPU. Tiempos orientativos, afectados por carga y calentamiento. No hay referencia humana de posición ni latencia visual. Comparar posiciones entre métodos no demuestra precisión.",
              "runs": []}
    try:
        for audio in files:
            for repeat, window in plan:
                label = "prefijo" if not window else f"ventana_{window}s"
                path = folder / f"{audio.stem}_{label}_r{repeat}.json"
                print(f"\nComparando {audio.name}: {label}, ronda {repeat}/{args.repeticiones}", flush=True)
                subprocess.run([sys.executable, "-u", str(ROOT / "scripts/seguir.py"), str(audio),
                                "--ventana", str(window), "--salida", str(path)], check=True, cwd=ROOT)
                data = json.loads(path.read_text(encoding="utf-8"))
                result["runs"].append({"audio": audio.name, "method": label, "window_seconds": window, "repeat": repeat,
                                       "record_file": path.name, **summarize(data)})
                (folder / "resumen.json").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    except subprocess.CalledProcessError as exc:
        raise SystemExit(f"La comparación se interrumpió ({exc.returncode}). Se conservan los registros en {folder}.")
    lines = ["# Comparación de reprocesamiento", "", result["notice"], "",
             "Mismo modelo, CPU int8, VAD, bloques de 2 s, cuento y seguidor. La carga del modelo se excluye de los tiempos de inferencia. Solapamiento = ventana menos 2 s; no aplica al prefijo. El silencio final puede reducir los totales de las ventanas.", "",
             "| Audio | Método | Ronda | Total inferencia (s) | Mediana (s) | P95 (s) | Inferencias >2 s | Cola máxima simulada (s) | Posición final | Retrocesos |",
             "|---|---|---:|---:|---:|---:|---:|---:|---:|---:|"]
    for r in result["runs"]:
        lines.append(f"| {r['audio']} | {r['method']} | {r['repeat']} | {r['processing_total_seconds']:.2f} | {r['processing_median_seconds']:.2f} | {r['processing_p95_seconds']:.2f} | {r['over_block_updates']} | {r['max_backlog_seconds_simulated']:.2f} | {r['final_position']} | {r['backward_moves']} |")
    lines += ["", "## Posiciones en cada actualización", "",
              "Comparación descriptiva con el prefijo, no referencia de precisión. El prefijo también puede equivocarse."]
    aggregates = []
    for audio in files:
        for repeat in range(1, args.repeticiones+1):
            runs = sorted([r for r in result["runs"] if r["audio"] == audio.name and r["repeat"] == repeat], key=lambda r:r["window_seconds"])
            histories = [json.loads((folder / r["record_file"]).read_text(encoding="utf-8"))["updates"] for r in runs]
            lines += ["", f"### {audio.name}, ronda {repeat}", "",
                      "| Audio disponible (s) | " + " | ".join(r["method"] for r in runs) + " |",
                      "|---:|" + "---:|" * len(runs)]
            for entries in zip(*histories):
                lines.append(f"| {entries[0]['audio_available_seconds']:.1f} | " + " | ".join(str(e["position"] or "—") for e in entries) + " |")
        for window in args.ventanas:
            group = [r for r in result["runs"] if r["audio"] == audio.name and r["window_seconds"] == window]
            totals = [r["processing_total_seconds"] for r in group]
            aggregates.append({"audio":audio.name, "window_seconds":window, "method":group[0]["method"],
                               "mean_total_seconds":statistics.mean(totals), "min_total_seconds":min(totals),
                               "max_total_seconds":max(totals), "mean_max_backlog_seconds":statistics.mean(r["max_backlog_seconds_simulated"] for r in group),
                               "over_block_updates_total":sum(r["over_block_updates"] for r in group),
                               "updates_total":sum(r["updates"] for r in group),
                               "final_positions":[r["final_position"] for r in group]})
    result["aggregates"] = aggregates
    (folder / "resumen.json").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    lines += ["", "## Resumen por configuración", "",
              "| Audio | Método | Total medio (s) | Rango de totales (s) | Cola máxima media (s) | Inferencias >2 s | Posiciones finales |",
              "|---|---|---:|---|---:|---|---|"]
    for r in aggregates:
        lines.append(f"| {r['audio']} | {r['method']} | {r['mean_total_seconds']:.2f} | {r['min_total_seconds']:.2f}–{r['max_total_seconds']:.2f} | {r['mean_max_backlog_seconds']:.2f} | {r['over_block_updates_total']}/{r['updates_total']} | {r['final_positions']} |")
    report = folder / "resumen.md"
    report.write_text("\n".join(lines)+"\n", encoding="utf-8")
    print("\nResumen (tiempos de inferencia, sin carga del modelo):", flush=True)
    for r in result["runs"]:
        print(f"{r['audio']} | {r['method']} | ronda {r['repeat']} | total {r['processing_total_seconds']:.2f}s | mediana {r['processing_median_seconds']:.2f}s | >2s: {r['over_block_updates']} | cola max. {r['max_backlog_seconds_simulated']:.2f}s | posicion final {r['final_position']}", flush=True)
    print("\nMedias por configuración:", flush=True)
    for r in aggregates:
        print(f"{r['method']} | total medio {r['mean_total_seconds']:.2f}s | rango {r['min_total_seconds']:.2f}-{r['max_total_seconds']:.2f}s | >2s: {r['over_block_updates_total']}/{r['updates_total']} | posiciones finales {r['final_positions']}", flush=True)
    print("\nComparación terminada. Informe:", report, flush=True)


if __name__ == "__main__":
    main()
