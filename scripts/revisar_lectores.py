"""Revisión humana de nuevos lectores; audio local original, sin ASR."""
import argparse
from copy import deepcopy
from datetime import datetime, timezone
import hashlib
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
import re
import secrets
import threading
import wave
from urllib.parse import urlsplit

from scripts.catalogo import ROOT, read_catalog
from scripts.archivos import write_text_atomic

FLAGS = ['trabadas', 'repeticiones', 'autocorrecciones', 'omisiones', 'sustituciones',
         'pausas', 'ruido', 'otras_voces', 'ayuda', 'aplausos', 'corte', 'duda']


def validate_review(payload, template):
    if not isinstance(payload, dict) or payload.get('audio_sha256') != template['audio_sha256']:
        raise ValueError('La revisión no corresponde a este audio.')
    result = deepcopy(template)
    for key, limit in [('transcript_literal', 30000), ('notes', 10000), ('events', 15000)]:
        value = payload.get(key, '')
        if not isinstance(value, str) or len(value) > limit:
            raise ValueError(f'Campo incorrecto: {key}')
        result[key] = value.strip()
    flags = payload.get('flags', [])
    if not isinstance(flags, list) or any(f not in FLAGS for f in flags) or len(set(flags)) != len(flags):
        raise ValueError('Marcas de escucha incorrectas.')
    result['flags'] = flags
    for key, choices in [('completion', ['', 'completa', 'incompleta', 'dudoso']),
                         ('quality', ['', 'revisable', 'dificil', 'no_revisable'])]:
        if payload.get(key, '') not in choices:
            raise ValueError(f'Valor incorrecto: {key}')
        result[key] = payload.get(key, '')
    for key in ['general_reviewed', 'literal_reviewed']:
        value = payload.get(key, False)
        if type(value) is not bool:
            raise ValueError('El estado de revisión debe ser explícito.')
        result[key] = value
    if result['general_reviewed'] and (not result['completion'] or not result['quality']):
        raise ValueError('Indica si se completó la lectura y si el audio se puede revisar.')
    if result['literal_reviewed'] and (not result['general_reviewed'] or not result['transcript_literal']):
        raise ValueError('Para completar la referencia literal, revisa la calidad y escribe lo que se oye.')
    result['saved_at_utc'] = datetime.now(timezone.utc).isoformat()
    return result


class Workspace:
    def __init__(self, root=ROOT):
        self.root, self.lock = root, threading.Lock()
        self.nonce = secrets.token_urlsafe(32)
        self.folder = root/'datos/anotaciones/revision_lectores'
        self.items, self.files, self.templates = [], {}, {}
        rows = read_catalog(root)['recordings']
        # Seleccionar por contenido disponible, nunca sustituir una toma ausente
        # por otra que reutilizó su nombre. No modificar el catálogo al revisar.
        for path in sorted((root/'datos/audio').glob('*.wav')):
            digest = hashlib.sha256(path.read_bytes()).hexdigest()
            relative = path.relative_to(root).as_posix()
            matches = [r for r in rows if r['audio_file'] == relative and r['audio_sha256'] == digest]
            if len(matches) != 1:
                raise ValueError(f'El WAV no tiene una identidad única por huella: {path.name}')
            row = matches[0]
            if row.get('speaker_id') in ('lector_01', 'adulto_01'):
                continue
            key = row['id']
            if not re.fullmatch(r'[A-Za-z0-9_-]+', key):
                raise ValueError('ID de grabación incorrecto.')
            with wave.open(str(path), 'rb') as wav:
                duration = wav.getnframes()/wav.getframerate()
                rate, channels = wav.getframerate(), wav.getnchannels()
            story_path = (root/row['story_file']).resolve()
            if not story_path.is_relative_to((root/'datos/textos').resolve()):
                raise ValueError('Texto fuera de la carpeta permitida.')
            if hashlib.sha256(story_path.read_bytes()).hexdigest() != row['story_sha256']:
                raise ValueError('El cuento cambió desde la grabación.')
            self.files[key] = path
            self.templates[key] = dict(schema_version=1, recording_id=key, audio_file=relative,
                audio_sha256=digest, story_file=row['story_file'], story_sha256=row['story_sha256'],
                speaker_id=row['speaker_id'], review_method='escucha_humana_sin_hipotesis_asr',
                reviewer='usuario_revisor', independent_second_review=False,
                completion='', quality='', flags=[], notes='', events='', transcript_literal='',
                general_reviewed=False, literal_reviewed=False,
                notice='Referencia manual en desarrollo. Tiempos de eventos aproximados, sin alineación palabra por palabra. No completar palabras inaudibles. Distinguir voces ajenas del lector.')
            self.items.append(dict(id=key, name=path.name, reader=row['speaker_id'],
                story=story_path.stem, story_text=story_path.read_text(encoding='utf-8-sig'),
                seconds=duration, sample_rate=rate, channels=channels, audio='/audio/'+key))
        if not self.items:
            raise ValueError('No hay audios de otros lectores disponibles.')

    def current(self, key):
        path = self.folder/(key+'.json')
        if not path.exists():
            return deepcopy(self.templates[key])
        saved = json.loads(path.read_text(encoding='utf-8'))
        result = validate_review(saved, self.templates[key])
        result['saved_at_utc'] = saved.get('saved_at_utc')
        return result

    def save(self, key, payload):
        with self.lock:
            if hashlib.sha256(self.files[key].read_bytes()).hexdigest() != self.templates[key]['audio_sha256']:
                raise ValueError('El audio cambió. Reinicia el visor para comprobarlo.')
            result = validate_review(payload, self.templates[key])
            self.folder.mkdir(parents=True, exist_ok=True)
            path = self.folder/(key+'.json')
            if path.exists():
                backup = self.root/'datos/anotaciones/copias'
                backup.mkdir(parents=True, exist_ok=True)
                (backup/f'{key}_revision_{datetime.now():%Y%m%d_%H%M%S_%f}.json').write_bytes(path.read_bytes())
            write_text_atomic(path, json.dumps(result, ensure_ascii=False, indent=2)+'\n')
            return result


def make_handler(workspace):
    class Handler(BaseHTTPRequestHandler):
        def log_message(self, *_):
            pass

        def allowed(self):
            return self.headers.get('Host') == f'127.0.0.1:{self.server.server_port}'

        def reply(self, body, mime='application/json; charset=utf-8', code=200, extra=None):
            self.send_response(code)
            self.send_header('Content-Type', mime)
            self.send_header('Content-Length', str(len(body)))
            self.send_header('Cache-Control', 'no-store')
            self.send_header('X-Content-Type-Options', 'nosniff')
            self.send_header('Content-Security-Policy', "default-src 'self'; media-src 'self'; object-src 'none'; frame-ancestors 'none'")
            for key, value in (extra or {}).items():
                self.send_header(key, value)
            self.end_headers()
            try:
                self.wfile.write(body)
            except (BrokenPipeError, ConnectionResetError, ConnectionAbortedError):
                pass

        def do_GET(self):
            if not self.allowed():
                self.send_error(403); return
            path = urlsplit(self.path).path
            if path == '/api/revision':
                data = dict(items=[dict(item, review=workspace.current(item['id'])) for item in workspace.items], nonce=workspace.nonce)
                self.reply(json.dumps(data, ensure_ascii=False).encode('utf-8'))
            elif path.startswith('/audio/') and path[7:] in workspace.files:
                audio = workspace.files[path[7:]]
                size = audio.stat().st_size
                start, end, code = 0, size-1, 200
                headers = {'Accept-Ranges': 'bytes'}
                requested = self.headers.get('Range')
                if requested:
                    match = re.fullmatch(r'bytes=(\d+)-(\d*)', requested)
                    if not match:
                        self.send_error(416); return
                    start = int(match[1]); end = min(int(match[2]) if match[2] else size-1, size-1)
                    if start > end:
                        self.send_error(416); return
                    code = 206; headers['Content-Range'] = f'bytes {start}-{end}/{size}'
                with audio.open('rb') as stream:
                    stream.seek(start); body = stream.read(end-start+1)
                self.reply(body, 'audio/wav', code, headers)
            elif path in ('/', '/app.js', '/style.css'):
                name, mime = {'/': ('index.html','text/html; charset=utf-8'), '/app.js': ('app.js','text/javascript; charset=utf-8'), '/style.css': ('style.css','text/css; charset=utf-8')}[path]
                assets = getattr(workspace, 'assets', workspace.root/'herramientas/revision_lectores')
                self.reply((assets/name).read_bytes(), mime)
            else:
                self.send_error(404)

        def do_POST(self):
            origin = f'http://127.0.0.1:{self.server.server_port}'
            if not self.allowed() or self.headers.get('Origin') != origin or self.headers.get('X-Revision-Token') != workspace.nonce:
                self.send_error(403); return
            key = urlsplit(self.path).path.removeprefix('/api/guardar/')
            if not self.path.startswith('/api/guardar/') or key not in workspace.files:
                self.send_error(404); return
            try:
                size = int(self.headers.get('Content-Length', '0'))
                if not 0 < size <= 250000:
                    raise ValueError('Tamaño de revisión incorrecto.')
                payload = json.loads(self.rfile.read(size))
                result = workspace.save(key, payload)
                self.reply(json.dumps(result, ensure_ascii=False).encode('utf-8'))
            except (ValueError, OSError) as exc:
                self.reply(json.dumps({'error': str(exc)}).encode('utf-8'), code=400)
    return Handler


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--puerto', type=int, default=8783)
    args = parser.parse_args()
    workspace = Workspace()
    server = ThreadingHTTPServer(('127.0.0.1', args.puerto), make_handler(workspace))
    print(f'Revisión de {len(workspace.items)} audios: http://127.0.0.1:{server.server_port}/', flush=True)
    print('Sin reconocimiento. Originales intactos; anotaciones locales guardables y reanudables.', flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == '__main__':
    main()
