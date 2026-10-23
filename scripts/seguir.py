"""Simulación por prefijos de audio; guarda hipótesis y posiciones provisionales."""
import argparse
from datetime import datetime
import json
import importlib.metadata
import math
from pathlib import Path
from time import perf_counter, process_time

try:
    from .alinear import normalize, tokens
    from .archivos import write_text_atomic
    from .recursos import ResourceMonitor, compute_markdown
    from .catalogo import audio_identity, resolve_audio_path, report_stem
except ImportError:
    from alinear import normalize, tokens
    from archivos import write_text_atomic
    from recursos import ResourceMonitor, compute_markdown
    from catalogo import audio_identity, resolve_audio_path, report_stem

ROOT = Path(__file__).resolve().parents[1]


def audio_bounds(end, window_seconds, sample_rate=16000):
    """Intervalo [inicio, fin) sin audio futuro; 0 significa prefijo completo."""
    return (max(0, end-round(window_seconds*sample_rate)) if window_seconds else 0, end)


def locate(story, hypothesis, previous=0, before=12, after=24, global_search=False, include_match_index=False):
    """Alinea las últimas 8 palabras ASR contra un fragmento del cuento.

    Se permiten extremos libres del cuento y ediciones unitarias. Requiere
    dos coincidencias y al menos 60% de coincidencias respecto a la hipótesis.
    Los índices devueltos son base 1; no puntúa lectura ni pronunciación.
    """
    heard = [normalize(w) for w in hypothesis[-8:]]
    if len(heard) < 2:
        return {"position": None, "reason": "evidencia_insuficiente"}
    start = 0 if global_search else max(0, previous-before)
    stop = len(story) if global_search else min(len(story), previous+after)
    expected = [normalize(w) for w in story[start:stop]]
    n, m = len(heard), len(expected)
    dp = [[0] * (m+1) for _ in range(n+1)]
    for i in range(1, n+1):
        dp[i][0] = i
        for j in range(1, m+1):
            dp[i][j] = min(dp[i-1][j-1] + (heard[i-1] != expected[j-1]),
                           dp[i-1][j]+1, dp[i][j-1]+1)
    if not m:
        return {"position": None, "reason": "ventana_vacia"}
    endpoint = min(range(1, m+1), key=lambda j: (dp[n][j], abs(start+j-previous), j))
    i, j = n, endpoint
    matches = 0
    position = None
    matched_hypothesis_index = None
    while i:
        if j and dp[i][j] == dp[i-1][j-1] + (heard[i-1] != expected[j-1]):
            equal = heard[i-1] == expected[j-1]
            matches += int(equal)
            if equal and position is None:
                position = start+j
                matched_hypothesis_index = max(0, len(hypothesis)-8)+i-1
            i, j = i-1, j-1
        elif dp[i][j] == dp[i-1][j]+1:
            i -= 1
        else:
            j -= 1
    accepted = matches >= 2 and matches/n >= 0.6 and dp[n][endpoint]/n <= 0.4
    result = {"position": position if accepted else None,
            "reason": "coincidencia_local" if accepted else "evidencia_incompatible",
            "window_indices": [start+1, stop], "exact_matches": matches,
            "hypothesis_words": len(heard), "edit_cost": dp[n][endpoint]}
    if include_match_index:
        result['matched_hypothesis_index'] = matched_hypothesis_index if accepted else None
    return result


class Tracker:
    def __init__(self, story):
        self.story = story
        self.position = 0
        self.failures = 0
        self.recovery_candidate = None

    def update(self, hypothesis):
        old = self.position
        evidence = locate(self.story, hypothesis, self.position)
        mode = "local"
        candidate = evidence["position"]
        if candidate is None:
            self.failures += 1
            if self.failures >= 2:
                recovery = locate(self.story, hypothesis, self.position, global_search=True)
                if recovery["position"] is not None:
                    mode = "recuperacion_pendiente"
                    if recovery["position"] == self.recovery_candidate:
                        candidate, evidence = recovery["position"], recovery
                        mode = "recuperacion"
                    self.recovery_candidate = recovery["position"]
                else:
                    self.recovery_candidate = None
        else:
            self.failures = 0
            self.recovery_candidate = None
        if candidate is not None:
            self.position = candidate
        return {"previous_position": old, "position": self.position or None,
                "word": self.story[self.position-1] if self.position else None,
                "movement": self.position-old, "mode": mode, "evidence": evidence}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("audio", nargs="?", type=Path)
    parser.add_argument("--bloque", type=float, default=2.0, help="Segundos entre actualizaciones (por defecto 2).")
    parser.add_argument("--cuento", type=Path, default=ROOT / "datos/textos/lectura_01.txt")
    parser.add_argument("--ventana", type=float, default=0, help="Audio a reprocesar en segundos; 0 conserva los prefijos completos.")
    parser.add_argument("--salida", type=Path, help="Ruta del registro JSON, usada en comparaciones.")
    parser.add_argument('--sin-recursos', action='store_true', help='Desactivar muestreo de recursos para contrastar su sobrecoste.')
    args = parser.parse_args()
    if not math.isfinite(args.bloque) or not 0.5 <= args.bloque <= 10:
        parser.error("El bloque debe estar entre 0.5 y 10 segundos.")
    if not math.isfinite(args.ventana) or (args.ventana != 0 and not args.bloque <= args.ventana <= 120):
        parser.error("La ventana debe ser 0 o estar entre la duración del bloque y 120 segundos.")
    if args.audio is None:
        files = sorted((ROOT / "datos/audio").glob("*.wav"), key=lambda p: p.stat().st_mtime_ns)
        if not files:
            parser.error("No hay grabaciones.")
        args.audio = files[-1]
    args.audio = resolve_audio_path(args.audio)
    monitor = None
    try:
        story = tokens(args.cuento.read_text(encoding="utf-8-sig"))
        if not story:
            raise ValueError("El cuento está vacío.")
        # decode_audio remuestrea y convierte a mono; no entregamos el audio
        # futuro al modelo: cada llamada recibe únicamente audio[:end].
        from faster_whisper.audio import decode_audio
        from faster_whisper import WhisperModel
        audio = decode_audio(str(args.audio), sampling_rate=16000)
        if not len(audio):
            raise ValueError("El audio está vacío.")
        if len(audio) > 120*16000:
            raise ValueError("Esta primera prueba admite hasta 120 segundos.")
        if not args.sin_recursos:
            monitor = ResourceMonitor()
            monitor.start()
        load_start = perf_counter()
        model = WhisperModel(str(ROOT / "modelos/faster-whisper-small"), device="cpu",
                             compute_type="int8", local_files_only=True)
        load_seconds = perf_counter()-load_start
    except (OSError, ValueError) as exc:
        if monitor is not None:
            monitor.stop()
        parser.error(str(exc))
    tracker = Tracker(story)
    records = []
    step = round(args.bloque*16000)
    ends = list(range(step, len(audio), step)) + [len(audio)]
    ready = 0.0
    folder = ROOT / "resultados/seguimiento"
    folder.mkdir(parents=True, exist_ok=True)
    path = args.salida or folder / f"{report_stem(args.audio)}_{datetime.now():%Y%m%d_%H%M%S_%f}_seguimiento.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    data = {"schema_version": 1, "audio_file": args.audio.name, "story_file": args.cuento.name,
            "story_words": story, "audio_seconds": len(audio)/16000, "block_seconds": args.bloque,
            "audio_window_seconds": args.ventana, "overlap_seconds": max(0, args.ventana-args.bloque) if args.ventana else None,
            "model": "Systran/faster-whisper-small", "device": "cpu", "compute_type": "int8",
            "versions": {name: importlib.metadata.version(name) for name in ("faster-whisper", "av", "ctranslate2")},
            "model_load_seconds": load_seconds,
            "model_disk_bytes": sum(p.stat().st_size for p in (ROOT / 'modelos/faster-whisper-small').rglob('*') if p.is_file()),
            "resource_measurement": "desactivada" if args.sin_recursos else "CPU/RAM del proceso y GPU global muestreadas durante carga e inferencias; recursos completos al finalizar. No son métricas de tablet.",
            "position_convention": "última palabra del cuento apoyada por coincidencia textual en la hipótesis",
            "recognition": "ventana acústica limitada" if args.ventana else "prefijos acumulativos",
            "asr_parameters": {"language": "es", "beam_size": 5, "vad_filter": True, "condition_on_previous_text": False},
            "notice": "Simulación posterior, no streaming nativo ni medida de latencia visual. Tiempos ASR estimados. Posiciones provisionales, sin valoración lectora.",
            "updates": records}
    data['audio_identity'] = audio_identity(args.audio)
    print('Audio:', data['audio_identity']['label'], '|', args.audio.name)
    print("Simulación sin audio futuro. Actualización cada", args.bloque, "s. Ventana:", args.ventana or "prefijo completo")
    print("La posición indica la última palabra apoyada por la hipótesis, no la palabra actual en directo.")
    previous_words = []
    for end in ends:
        cutoff = end/16000
        begin, end = audio_bounds(end, args.ventana)
        offset = begin/16000
        tick = perf_counter()
        cpu_tick = process_time()
        segments, _ = model.transcribe(audio[begin:end].copy(), language="es", beam_size=5,
                                      word_timestamps=True, vad_filter=True,
                                      condition_on_previous_text=False)
        hypotheses = []
        for seg in segments:
            for w in seg.words or []:
                for word in tokens(w.word):
                    hypotheses.append({"word": word, "start": w.start+offset, "end": w.end+offset,
                                       "probability": w.probability})
        processing = perf_counter()-tick
        cpu_processing = process_time()-cpu_tick
        heard = [w["word"] for w in hypotheses]
        unchanged = heard == previous_words
        # No confirmamos recuperación con la misma hipótesis reiterada en silencio.
        state = (tracker.update(heard) if not unchanged else
                 {"previous_position": tracker.position, "position": tracker.position or None,
                  "word": story[tracker.position-1] if tracker.position else None,
                  "movement": 0, "mode": "hipotesis_sin_cambios", "evidence": {}})
        previous_words = heard
        start_simulated = max(cutoff, ready)
        ready = start_simulated+processing
        records.append({"audio_available_seconds": cutoff, "processing_seconds": processing,
                        "asr_cpu_seconds": cpu_processing,
                        "audio_window_start_seconds": offset, "audio_window_end_seconds": cutoff,
                        "audio_reprocessed_seconds": cutoff-offset,
                        "sequential_ready_seconds_simulated": ready,
                        "backlog_seconds_simulated": start_simulated-cutoff,
                        "hypothesis": hypotheses, **state})
        # Guardamos cada actualización para conservar progreso si se interrumpe.
        write_text_atomic(path, json.dumps(data, ensure_ascii=False, indent=2))
        print(f"Audio {offset:4.1f}-{cutoff:4.1f}s | posición {state['position'] or '-'}: {state['word'] or '-'} | {processing:.2f}s | {state['mode']}")
        print("  ASR:", " ".join(heard[-12:]))
    data['resources'] = monitor.stop() if monitor is not None else None
    rms = math.sqrt(float((audio.astype('float64')**2).mean()))
    data['input_audio_metrics'] = {'sample_rate_hz': 16000, 'channels': 1,
                                   'peak_amplitude': float(abs(audio).max()),
                                   'rms_dbfs_full_audio': 20*math.log10(rms) if rms else None,
                                   'notice': 'Señal remuestreada completa, incluida habla, ruido y silencio. No es SNR ni estimación de ruido aislado.'}
    write_text_atomic(path, json.dumps(data, ensure_ascii=False, indent=2))
    md_path = path.with_suffix(".md")
    lines = ["# Seguimiento progresivo simulado", "", data["notice"], "",
             f"Audio: {data['audio_identity']['label']} · {args.audio.name}", "",
             "Convención: última palabra apoyada por coincidencia textual; no se califica pronunciación.", "",
             f"Audio por inferencia: {'últimos ' + str(args.ventana) + ' segundos' if args.ventana else 'prefijo completo'}. Bloque: {args.bloque} s. Sin audio futuro.",
             "Las hipótesis de ventanas solapadas se alinean de forma independiente manteniendo el estado del seguidor. No se concatenan como una transcripción definitiva ni se cuentan intentos repetidos por el solapamiento.",
             "La cola secuencial simulada supone el modelo ya cargado y no mide transferencia ni pantalla.", "",
             "| Audio disponible (s) | Posición | Palabra | Movimiento | Procesamiento (s) | Cola simulada (s) | Modo |",
             "|---:|---:|---|---:|---:|---:|---|"]
    for r in records:
        lines.append(f"| {r['audio_available_seconds']:.1f} | {r['position'] or '—'} | {r['word'] or '—'} | {r['movement']} | {r['processing_seconds']:.2f} | {r['backlog_seconds_simulated']:.2f} | {r['mode']} |")
    lines += ["", "## Hipótesis disponibles", ""]
    for r in records:
        lines.append(f"- Hasta {r['audio_available_seconds']:.1f} s: " + " ".join(w["word"] for w in r["hypothesis"]))
    lines += ['', compute_markdown([(path.name, data)])]
    write_text_atomic(md_path, "\n".join(lines)+"\n")
    print("Informe:", md_path)
    print("Registro:", path)


if __name__ == "__main__":
    main()
