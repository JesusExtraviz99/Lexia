"""Alineamiento textual posterior. No atribuye diferencias al lector."""
import argparse
from collections import Counter
import json
from pathlib import Path
import re
import unicodedata

ROOT = Path(__file__).resolve().parents[1]
TOKEN = re.compile(r"[^\W_]+(?:['’][^\W_]+)*", re.UNICODE)


def tokens(text):
    return TOKEN.findall(unicodedata.normalize("NFC", text))


def normalize(word):
    # Ignora caja y puntuación; conserva tildes y ñ.
    return unicodedata.normalize("NFC", word).casefold()


def align(expected, observed):
    """Distancia de edición global con costes unitarios y recorrido determinista.

    Cada palabra conserva su índice original (base 1). En empates se prioriza
    coincidencia/sustitución, luego omisión, luego inserción. No resuelve todas
    las ambigüedades de textos repetidos ni modela retrocesos en directo.
    """
    n, m = len(expected), len(observed)
    a = [normalize(w) for w in expected]
    b = [normalize(w["word"]) for w in observed]
    costs = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(n + 1):
        costs[i][0] = i
    for j in range(m + 1):
        costs[0][j] = j
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            costs[i][j] = min(costs[i-1][j-1] + (a[i-1] != b[j-1]),
                              costs[i-1][j] + 1, costs[i][j-1] + 1)
    rows = []
    i, j = n, m
    while i or j:
        if i and j and costs[i][j] == costs[i-1][j-1] + (a[i-1] != b[j-1]):
            kind = "coincidencia" if a[i-1] == b[j-1] else "sustitucion_candidata"
            ei, oi = i-1, j-1
            i, j = i-1, j-1
        elif i and costs[i][j] == costs[i-1][j] + 1:
            kind, ei, oi = "omision_candidata", i-1, None
            i -= 1
        else:
            kind, ei, oi = "insercion_candidata", None, j-1
            j -= 1
        item = observed[oi] if oi is not None else {}
        rows.append({"type": kind, "story_index": ei+1 if ei is not None else None,
                     "story_word": expected[ei] if ei is not None else None,
                     "asr_index": oi+1 if oi is not None else None,
                     "asr_word": item.get("word"), "start": item.get("start"),
                     "end": item.get("end"), "asr_probability": item.get("probability")})
    rows.reverse()
    # Una inserción que duplica el fragmento inmediatamente anterior o siguiente
    # es una repetición candidata. No cuenta doble la operación de edición.
    k = 0
    while k < len(rows):
        if rows[k]["type"] != "insercion_candidata":
            k += 1
            continue
        end = k
        while end < len(rows) and rows[end]["type"] == "insercion_candidata":
            end += 1
        run = rows[k:end]
        spoken = [normalize(r["asr_word"]) for r in run]
        before = next((r["story_index"] for r in reversed(rows[:k]) if r["story_index"]), 0)
        after = next((r["story_index"] for r in rows[end:] if r["story_index"]), n+1)
        refs = None
        if before >= len(run) and a[before-len(run):before] == spoken:
            refs = list(range(before-len(run)+1, before+1))
        elif after-1+len(run) <= n and a[after-1:after-1+len(run)] == spoken:
            refs = list(range(after, after+len(run)))
        for offset, row in enumerate(run):
            row["between_story_indices"] = [before or None, after if after <= n else None]
            if refs:
                row["type"] = "repeticion_candidata"
                row["repeated_story_index"] = refs[offset]
        k = end
    return rows, costs[n][m]


def observed_words(data):
    words = []
    for segment in data["segments"]:
        if segment.get("text", "").strip() and not segment.get("words"):
            raise ValueError("Faltan palabras con tiempos. Usa una transcripción con word_timestamps=True.")
        for entry in segment.get("words", []):
            parts = tokens(entry["word"])
            for part in parts:
                word = {**entry, "word": part}
                # Si una entrada contiene varios tokens, comparten el intervalo
                # estimado de origen: no inventamos tiempos individuales.
                words.append(word)
    return words


def report(data, source, story):
    rows = data["alignment"]
    lines = ["# Alineamiento textual de lectura", "", f"Transcripción: `{source.name}`.",
             f"Cuento: `{story.name}`.", "",
             "Comparación posterior entre cuento y ASR. Las diferencias son candidatas, no errores lectores confirmados.",
             "Los tiempos proceden del ASR; las omisiones no tienen un intervalo de audio asignado.", "",
             f"Palabras del cuento: {data['story_word_count']}. Palabras ASR: {data['asr_word_count']}.",
             f"Distancia de edición: {data['edit_distance']}.", "",
             "| Tipo | Palabras |", "|---|---:|"]
    for kind, count in sorted(data["counts"].items()):
        lines.append(f"| {kind} | {count} |")
    lines += ["", "## Diferencias candidatas", "",
              "| Tipo | Índice del cuento (base 1) | Esperado | ASR | Intervalo ASR (s) |",
              "|---|---|---|---|---|"]
    differences = [r for r in rows if r["type"] != "coincidencia"]
    for row in differences:
        pos = row["story_index"] or row.get("repeated_story_index")
        if pos is None:
            left, right = row.get("between_story_indices", [None, None])
            pos = f"entre {left or 'inicio'} y {right or 'fin'}"
        timing = "sin tiempo" if row["start"] is None else f"{row['start']:.2f}–{row['end']:.2f}"
        lines.append(f"| {row['type']} | {pos} | {row['story_word'] or '—'} | {row['asr_word'] or '—'} | {timing} |")
    if not differences:
        lines += ["", "No se encontraron diferencias tras normalizar caja y puntuación."]
    lines += ["", "## Límites", "",
              "Una coincidencia solo indica igualdad textual. No certifica pronunciación correcta.",
              "Un intento incompleto eliminado por el ASR no se puede recuperar con este alineamiento.",
              "El alineamiento global usa la transcripción completa y puede ser ambiguo con palabras repetidas; no demuestra seguimiento en directo.",
              "", "## Recorrido completo", "",
              "| Tipo | Índice cuento | Cuento | Índice ASR | ASR | Inicio | Fin |",
              "|---|---:|---|---:|---|---:|---:|"]
    for r in rows:
        start = "—" if r["start"] is None else f"{r['start']:.2f}"
        end = "—" if r["end"] is None else f"{r['end']:.2f}"
        lines.append(f"| {r['type']} | {r['story_index'] or '—'} | {r['story_word'] or '—'} | {r['asr_index'] or '—'} | {r['asr_word'] or '—'} | {start} | {end} |")
    return "\n".join(lines) + "\n"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("transcripcion", nargs="?", type=Path, help="JSON ASR; por defecto, el último de resultados.")
    parser.add_argument("--cuento", type=Path, default=ROOT / "datos/textos/lectura_01.txt")
    args = parser.parse_args()
    source = args.transcripcion
    if source is None:
        files = sorted((ROOT / "resultados").glob("lectura_*.json"))
        if not files:
            parser.error("No hay transcripciones. Ejecuta primero scripts/transcribir.py.")
        source = files[-1]
    try:
        raw = json.loads(source.read_text(encoding="utf-8-sig"))
        expected = tokens(args.cuento.read_text(encoding="utf-8-sig"))
        if not expected:
            raise ValueError("El cuento está vacío.")
        observed = observed_words(raw)
        if len(expected) * len(observed) > 4_000_000:
            raise ValueError("Texto demasiado grande para este alineador global; divide la prueba en fragmentos.")
        rows, distance = align(expected, observed)
    except (OSError, ValueError, KeyError, TypeError) as exc:
        parser.error(f"No se pudo alinear: {exc}")
    data = {"schema_version": 1, "method": "global_edit_distance_unit_cost",
            "transcription_file": source.name, "story_file": args.cuento.name,
            "normalization": "NFC, sin puntuación, casefold; conserva tildes y ñ",
            "story_word_count": len(expected), "asr_word_count": len(observed),
            "edit_distance": distance, "counts": dict(Counter(r["type"] for r in rows)),
            "notice": "Diferencias candidatas; no diagnóstico lector ni seguimiento en directo.",
            "alignment": rows}
    output = ROOT / "resultados/alineamientos"
    output.mkdir(parents=True, exist_ok=True)
    json_path = output / f"{source.stem}_alineado.json"
    md_path = output / f"{source.stem}_alineado.md"
    json_path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    md_path.write_text(report(data, source, args.cuento), encoding="utf-8")
    print(f"Cuento: {len(expected)} palabras. ASR: {len(observed)} palabras.")
    print("Resumen:", data["counts"])
    for row in rows:
        if row["type"] != "coincidencia":
            print(f"  {row['type']}: {row['story_word'] or '(sin palabra)'} -> {row['asr_word'] or '(sin palabra)'}")
    print("Informe:", md_path)
    print("JSON:", json_path)


if __name__ == "__main__":
    main()
