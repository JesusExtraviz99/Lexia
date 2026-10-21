"""Reproductor de anotación temporal, servido solo en 127.0.0.1."""
import argparse
from copy import deepcopy
from datetime import datetime, timezone
import hashlib
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
import math
from pathlib import Path
import re
import secrets
import shutil
import threading
import wave

try:
    from .alinear import tokens, normalize
except ImportError:
    from alinear import tokens, normalize

ROOT = Path(__file__).resolve().parents[1]
UI = ROOT / "herramientas/anotador"


def validate_annotation(payload, template):
    """Solo tiempos/estados del caso fijado; nunca modifica la referencia literal."""
    if not isinstance(payload, dict) or not isinstance(payload.get("words"), list):
        raise ValueError("Formato de anotación incorrecto.")
    if len(payload["words"]) != len(template["words"]):
        raise ValueError("Debe conservarse el número de palabras.")
    result = deepcopy(template)
    previous_end = 0.0
    for original, supplied in zip(result["words"], payload["words"]):
        if not isinstance(supplied, dict) or supplied.get("index") != original["index"] or supplied.get("word") != original["word"]:
            raise ValueError("No se pueden cambiar las palabras ni sus índices.")
        start, end = supplied.get("start"), supplied.get("end")
        reviewed = supplied.get("reviewed")
        if not isinstance(reviewed, bool):
            raise ValueError("El estado de revisión debe ser explícito.")
        if (start is None) != (end is None):
            raise ValueError("Indica inicio y fin, o deja ambos vacíos.")
        if start is not None:
            if any(isinstance(v, bool) or not isinstance(v, (int, float)) or not math.isfinite(v) for v in (start, end)):
                raise ValueError("Los tiempos deben ser números finitos.")
            if not 0 <= start < end <= result["duration_seconds"]:
                raise ValueError("El intervalo debe estar dentro del audio y tener duración positiva.")
            if start < previous_end - 0.001:
                raise ValueError(f"La palabra {original['index']} se solapa con la anterior. Ajusta el límite compartido.")
            previous_end = end
        elif reviewed:
            raise ValueError("Una palabra sin tiempos no puede marcarse revisada.")
        note = supplied.get("note", "")
        if not isinstance(note, str) or len(note) > 1000:
            raise ValueError("Nota demasiado larga o incorrecta.")
        origin = supplied.get("timing_origin", "manual")
        if origin not in ("sin_marcar", "manual", "borrador_asr", "asr_ajustado"):
            raise ValueError("Procedencia de tiempos incorrecta.")
        original.update(start=start, end=end, reviewed=reviewed, note=note, timing_origin=origin)
    result["reviewed_words"] = sum(w["reviewed"] for w in result["words"])
    result["timing_status"] = "revision_usuario_completa" if result["reviewed_words"] == len(result["words"]) else "borrador_parcial"
    result["reviewer"] = "usuario_lector" if result["reviewed_words"] else None
    if result.get('annotation_kind') == 'selected_intervals':
        result['reviewed_intervals'] = result.pop('reviewed_words')
        result['timing_status'] = ('revision_intervalos_seleccionados_completa'
                                   if result['reviewed_intervals'] == len(result['words']) else 'borrador_parcial')
    result["saved_at_utc"] = datetime.now(timezone.utc).isoformat()
    return result


class Workspace:
    def __init__(self, root=ROOT):
        self.root = root
        self.lock = threading.Lock()
        self.nonce = secrets.token_urlsafe(24)
        reference_path = root / "datos/referencias/lectura_normal.json"
        reference = json.loads(reference_path.read_text(encoding="utf-8"))
        if reference["status"] != "transcripcion_validada_tiempos_pendientes":
            raise ValueError("La transcripción normal debe estar validada antes de anotar.")
        self.audio = root / reference["audio_file"]
        digest = hashlib.sha256(self.audio.read_bytes()).hexdigest()
        if digest != reference["audio_sha256"]:
            raise ValueError("El audio no coincide con la referencia validada.")
        with wave.open(str(self.audio), "rb") as wav:
            duration = wav.getnframes() / wav.getframerate()
        expected = tokens(reference["transcript_literal"])
        self.template = {"schema_version": 1, "recording_id": "lectura_normal", "audio_file": reference["audio_file"],
                         "audio_sha256": digest, "duration_seconds": duration,
                         "transcript_sha256": hashlib.sha256(reference["transcript_literal"].encode("utf-8")).hexdigest(),
                         "boundary_convention": "inicio y fin audibles de cada palabra pronunciada, incluidos sonidos finales; conservar huecos de silencio",
                         "timing_status": "borrador_parcial", "reviewed_words": 0,
                         "notice": "Anotación de desarrollo por el lector, no revisión independiente. No transferir automáticamente a referencia temporal ni afirmar precisión de milisegundos.",
                         "words": [{"index": i+1, "word": w, "start": None, "end": None,
                                    "reviewed": False, "timing_origin": "sin_marcar", "note": ""} for i, w in enumerate(expected)]}
        self.path = root / "datos/anotaciones/lectura_normal.json"
        self.draft = self.make_asr_draft(expected)

    def make_asr_draft(self, expected):
        files = sorted((self.root / "resultados").glob("lectura_20261014_081816_009646_*.json"))
        for path in reversed(files):
            data = json.loads(path.read_text(encoding="utf-8"))
            words = [w for s in data.get("segments", []) for w in s.get("words", [])]
            normalized = [normalize(t) for w in words for t in tokens(w["word"])]
            if normalized != [normalize(w) for w in expected] or len(words) != len(expected):
                continue
            candidate = deepcopy(self.template)
            for dest, source in zip(candidate["words"], words):
                dest.update(start=source["start"], end=source["end"], timing_origin="borrador_asr")
            try:
                candidate = validate_annotation(candidate, self.template)
            except ValueError:
                continue
            candidate["asr_source_file"] = path.relative_to(self.root).as_posix()
            return candidate
        return None

    def current(self):
        if not self.path.exists():
            return deepcopy(self.template)
        data = json.loads(self.path.read_text(encoding="utf-8"))
        if data.get("audio_sha256") != self.template["audio_sha256"] or data.get("transcript_sha256") != self.template["transcript_sha256"]:
            raise ValueError("La anotación guardada pertenece a otro audio o texto.")
        # Validamos tiempos e identidad; la fecha se conserva hasta guardar de nuevo.
        validated = validate_annotation(data, self.template)
        validated["saved_at_utc"] = data.get("saved_at_utc")
        return validated

    def save(self, payload):
        with self.lock:
            result = validate_annotation(payload, self.template)
            self.path.parent.mkdir(parents=True, exist_ok=True)
            if self.path.exists():
                backups = self.path.parent / "copias"
                backups.mkdir(exist_ok=True)
                stamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
                shutil.copy2(self.path, backups / f"{self.path.stem}_{stamp}.json")
            temporary = self.path.with_suffix(".tmp")
            temporary.write_text(json.dumps(result, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
            temporary.replace(self.path)
            return result


EVENT_CASES = {
    'relectura_azul': ('lectura_relectura_azul', 'Segunda vuelta atrás: Cerca de un árbol',
                       'Marca cuaderno al terminar el cuento completo, Cerca al empezar la relectura y azul al terminarla. Cerca y azul pertenecen a la segunda lectura del tramo. No marques las palabras interiores.',
                       [('cuaderno · final de la lectura completa', [56, 56], 1, [18, 25]),
                        ('Cerca · inicio de la relectura', [10, 10], 2, [24, 30]),
                        ('azul · final de la relectura', [17, 17], 2, [30, 37])]),
    'relectura_lejana': ('lectura_relectura_lejana', 'Vuelta atrás después del final del cuento',
                        'Marca solo tres palabras: cuaderno al terminar el cuento, Los al empezar la relectura y alas al terminarla. Los y alas son de la segunda lectura de ese tramo. Sus límites permiten delimitar la frase sin anotar cada palabra interna.',
                        [('cuaderno · final de la lectura completa', [56, 56], 1, [22, 28]),
                         ('Los · inicio de la relectura', [37, 37], 2, [26, 32]),
                         ('alas · final de la relectura', [45, 45], 2, [30, 36])]),
    'pausa': ('lectura_pausa', 'Pausa entre flor y Ana',
              'Marca flor antes de la pausa, Ana al retomar la lectura y cuaderno al final. Solo estas tres palabras.',
              [('flor · antes de la pausa', [27, 27], 1, [6, 14]),
               ('Ana · al retomar', [28, 28], 1, [18, 26]),
               ('cuaderno · final', [56, 56], 1, [26, 34])]),
    'lenta': ('lectura_lenta', 'Lectura lenta: puntos de pérdida y final',
              'Marca únicamente Después, mariposa de la última frase, un y cuaderno. No anotes el resto del cuento.',
              [('Después', [46, 46], 1, [56, 68]),
               ('mariposa · última frase', [53, 53], 1, [66, 78]),
               ('un · antes de cuaderno', [55, 55], 1, [70, 82]),
               ('cuaderno · final', [56, 56], 1, [70, 82])]),
    'relectura': ('lectura_relectura', 'Dos intentos de la misma frase',
                 'Marca la frase entera Los dos se quedaron en silencio en su primer y segundo intento. Después marca mirando. Cada intento conserva el mismo tramo del cuento.',
                 [('Los dos se quedaron en silencio · primer intento', [37, 42], 1, [12, 22]),
                  ('Los dos se quedaron en silencio · segundo intento', [37, 42], 2, [16, 26]),
                  ('mirando · después del segundo intento', [43, 43], 1, [20, 28])]),
}


class EventWorkspace(Workspace):
    """Intervalos seleccionados; no representan una anotación de todas las palabras."""
    def __init__(self, case, root=ROOT):
        recording, title, instructions, targets = EVENT_CASES[case]
        self.root, self.lock, self.nonce = root, threading.Lock(), secrets.token_urlsafe(24)
        reference = json.loads((root / f'datos/referencias/{recording}.json').read_text(encoding='utf-8'))
        self.audio = root / reference['audio_file']
        digest = hashlib.sha256(self.audio.read_bytes()).hexdigest()
        if digest != reference['audio_sha256']:
            raise ValueError('El audio no coincide con la referencia validada.')
        with wave.open(str(self.audio), 'rb') as wav:
            duration = wav.getnframes() / wav.getframerate()
        self.template = {'schema_version': 1, 'annotation_kind': 'selected_intervals',
                         'recording_id': recording, 'title': title, 'instructions': instructions,
                         'audio_file': reference['audio_file'], 'audio_sha256': digest,
                         'transcript_sha256': hashlib.sha256(reference['transcript_literal'].encode('utf-8')).hexdigest(),
                         'duration_seconds': duration, 'timing_status': 'borrador_parcial',
                         'reviewed_intervals': 0,
                         'coverage_notice': 'Solo intervalos seleccionados. Completar esta lista no significa anotar todo el audio. Las ventanas de orientación no son marcas humanas ni propuestas de inicio/fin.',
                         'boundary_convention': 'Inicio audible y final audible de la palabra o frase completa de cada intento, en orden cronológico.',
                         'words': [{'index': i + 1, 'word': label, 'story_range': indices, 'attempt': attempt,
                                    'navigation_seconds': navigation, 'start': None, 'end': None,
                                    'reviewed': False, 'note': '', 'timing_origin': 'sin_marcar'}
                                   for i, (label, indices, attempt, navigation) in enumerate(targets)]}
        self.path = root / f'datos/anotaciones/{recording}_fragmentos.json'
        self.draft = None


def make_handler(workspace):
    class Handler(BaseHTTPRequestHandler):
        def log_message(self, *_args):
            pass

        def allowed_host(self):
            return self.headers.get("Host") == f"127.0.0.1:{self.server.server_port}"

        def reply(self, status, value):
            body = json.dumps(value, ensure_ascii=False).encode("utf-8")
            self.send_response(status)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Cache-Control", "no-store")
            self.send_header("X-Content-Type-Options", "nosniff")
            self.end_headers()
            self.wfile.write(body)

        def do_GET(self):
            if not self.allowed_host():
                self.reply(403, {"error": "Host no permitido."})
                return
            if self.path == "/api/caso":
                try:
                    self.reply(200, {"annotation": workspace.current(), "asr_draft": workspace.draft, "nonce": workspace.nonce})
                except ValueError as exc:
                    self.reply(409, {"error": str(exc)})
                return
            if self.path == "/audio":
                size = workspace.audio.stat().st_size
                start, end = 0, size-1
                partial = self.headers.get("Range")
                if partial:
                    match = re.fullmatch(r"bytes=(\d+)-(\d*)", partial)
                    if not match:
                        self.send_error(416)
                        return
                    start = int(match[1])
                    end = min(int(match[2]) if match[2] else end, size-1)
                    if start > end:
                        self.send_error(416)
                        return
                self.send_response(206 if partial else 200)
                self.send_header("Content-Type", "audio/wav")
                self.send_header("Accept-Ranges", "bytes")
                self.send_header("Content-Length", str(end-start+1))
                if partial:
                    self.send_header("Content-Range", f"bytes {start}-{end}/{size}")
                self.end_headers()
                try:
                    with workspace.audio.open("rb") as stream:
                        stream.seek(start)
                        remaining = end-start+1
                        while remaining:
                            chunk = stream.read(min(65536, remaining))
                            if not chunk:
                                break
                            self.wfile.write(chunk)
                            remaining -= len(chunk)
                except (ConnectionAbortedError, ConnectionResetError, BrokenPipeError):
                    pass
                return
            files = {"/": ("index.html", "text/html"), "/app.js": ("app.js", "text/javascript"), "/style.css": ("style.css", "text/css")}
            if self.path not in files:
                self.send_error(404)
                return
            name, content_type = files[self.path]
            body = (UI / name).read_bytes()
            self.send_response(200)
            self.send_header("Content-Type", content_type+"; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Cache-Control", "no-store")
            self.send_header("Content-Security-Policy", "default-src 'self'; script-src 'self'; style-src 'self'; media-src 'self'; connect-src 'self'; object-src 'none'; frame-ancestors 'none'")
            self.end_headers()
            self.wfile.write(body)

        def do_POST(self):
            expected_origin = f"http://127.0.0.1:{self.server.server_port}"
            if (not self.allowed_host() or self.path != "/api/guardar" or
                    self.headers.get("Origin") != expected_origin or
                    self.headers.get("X-Anotador-Token") != workspace.nonce):
                self.reply(403, {"error": "Petición no permitida."})
                return
            try:
                size = int(self.headers.get("Content-Length", "0"))
                if not 0 < size <= 200000:
                    raise ValueError("Tamaño de petición incorrecto.")
                payload = json.loads(self.rfile.read(size))
                result = workspace.save(payload)
                self.reply(200, {"annotation": result, "file": workspace.path.relative_to(workspace.root).as_posix()})
            except (ValueError, KeyError, TypeError) as exc:
                self.reply(400, {"error": str(exc)})

    return Handler


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--puerto", type=int, default=8765)
    parser.add_argument('--caso', choices=['normal', *EVENT_CASES], default='normal')
    args = parser.parse_args()
    if not 0 <= args.puerto <= 65535:
        parser.error("Puerto incorrecto.")
    try:
        workspace = Workspace() if args.caso == 'normal' else EventWorkspace(args.caso)
        server = ThreadingHTTPServer(("127.0.0.1", args.puerto), make_handler(workspace))
    except (OSError, ValueError) as exc:
        parser.error(str(exc))
    print(f"Abre http://127.0.0.1:{server.server_port}", flush=True)
    print(f"Caso {args.caso}. Guardado local en datos/anotaciones. Ctrl+C para cerrar.", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
