"""Revisión cualitativa de cuatro fragmentos; reutiliza ASR, sin nuevas inferencias."""
import argparse
from copy import deepcopy
from datetime import datetime, timezone
import hashlib
from http.server import ThreadingHTTPServer
import json
from pathlib import Path
import secrets
import threading

from scripts.archivos import write_text_atomic
from scripts.catalogo import ROOT
from scripts import explorar_ventanas as explorer

FOLDER = ROOT/'resultados/lotes/20261023_102114_072901/lectura_20261023_101522_832827'
PLAN = [('inicio', 'Inicio', 0, 8), ('medio_1', 'Primer tramo intermedio', 16, 24),
        ('medio_2', 'Segundo tramo intermedio', 34, 42), ('final', 'Final', 48, 56)]
FLAGS = ['fragmentos', 'silabas_repetidas', 'palabras_repetidas', 'reinicios', 'sin_trabadas', 'dudoso']
CHOICES = ['', 'conserva', 'simplifica', 'cambia', 'mixto', 'dudoso']


def validate_reviews(reviews):
    if not isinstance(reviews, list) or len(reviews) != len(PLAN):
        raise ValueError('Se requieren los cuatro fragmentos, aunque queden pendientes.')
    result = []
    for item, (key, *_rest) in zip(reviews, PLAN):
        if not isinstance(item, dict) or item.get('id') != key:
            raise ValueError('Fragmento incorrecto.')
        flags = item.get('heard', [])
        notes = item.get('notes', '')
        done = item.get('reviewed', False)
        if not isinstance(flags, list) or any(f not in FLAGS for f in flags) or len(set(flags)) != len(flags):
            raise ValueError('Descripción de lo escuchado incorrecta.')
        if 'sin_trabadas' in flags and len(flags) > 1:
            raise ValueError('No combines sin trabadas con otras descripciones.')
        if not isinstance(notes, str) or len(notes) > 4000 or type(done) is not bool:
            raise ValueError('Nota o estado incorrectos.')
        a, b = item.get('asr4', ''), item.get('asr8', '')
        if a not in CHOICES or b not in CHOICES:
            raise ValueError('Valoración ASR incorrecta.')
        if done and (not flags or not a or not b):
            raise ValueError('Para marcar revisado, describe lo escuchado y valora ambas ventanas; puedes elegir duda.')
        result.append(dict(id=key, heard=flags, notes=notes.strip(), reviewed=done, asr4=a, asr8=b))
    return result


class Review:
    def __init__(self, folder=FOLDER, root=ROOT):
        self.root, self.folder = root, folder
        self.nonce, self.lock = secrets.token_urlsafe(24), threading.Lock()
        raw, self.audio, self.clips = explorer.load_experiment(folder.resolve())
        manifest = json.loads((folder/'resumen.json').read_text(encoding='utf-8'))
        self.sources = {r['record_file']: hashlib.sha256((folder/r['record_file']).read_bytes()).hexdigest()
                        for r in manifest['runs'] if r['repeat']==1}
        source_wav = explorer.resolve_audio_path(raw['audio'], root)
        self.audio_sha = hashlib.sha256(source_wav.read_bytes()).hexdigest()
        self.path = root/'datos/anotaciones/lectura_02_trabadas_revision_cualitativa.json'
        sections = []
        for key, title, start, end in PLAN:
            self.clips['contexto/'+key] = (round(start*16000), round(end*16000))
            cuts = []
            for index, row in enumerate(next(r for r in raw['runs'] if r['window']==4 and r['repeat']==1)['rows']):
                if not start < row['end'] <= end:
                    continue
                windows = []
                for w in [4,8]:
                    entry = next(r for r in raw['runs'] if r['window']==w and r['repeat']==1)['rows'][index]
                    decision = entry['variants']['original']
                    windows.append(dict(seconds=w, start=entry['start'], end=entry['end'],
                                        clip=entry['clip'], text=' '.join(entry['hypothesis']),
                                        position=decision['position'], word=decision['word'],
                                        processing=entry['processing']))
                cuts.append(dict(end=row['end'], windows=windows))
            sections.append(dict(id=key, title=title, start=start, end=end,
                                 clip='/clip/contexto/'+key, cuts=cuts))
        self.payload = dict(audio_label=raw['audio_label'], audio_file=raw['audio'], sections=sections,
                            annotation_file=self.path.relative_to(root).as_posix(), round=1)

    def current(self):
        if self.path.exists():
            state = json.loads(self.path.read_text(encoding='utf-8'))
            if state['audio_sha256'] != self.audio_sha or state['source_sha256'] != self.sources:
                raise ValueError('La revisión guardada corresponde a otros archivos.')
            validate_reviews(state['reviews'])
            return state
        return dict(schema_version=1, review_type='cualitativa_fragmentos_seleccionados',
                    audio_file=self.payload['audio_file'], audio_sha256=self.audio_sha,
                    source_folder=self.folder.relative_to(self.root).as_posix(), source_sha256=self.sources,
                    round=1, intervals=[dict(id=k, start=s, end=e) for k,_,s,e in PLAN],
                    notice='Revisión del propio lector con acceso a ASR. No es transcripción literal, revisión independiente, cobertura total ni anotación de límites de palabras.',
                    reviews=[dict(id=k, heard=[], notes='', reviewed=False, asr4='', asr8='') for k,*_ in PLAN])

    def save(self, payload):
        if not isinstance(payload, dict):
            raise ValueError('Formato de revisión incorrecto.')
        reviews = validate_reviews(payload.get('reviews'))
        with self.lock:
            state = deepcopy(self.current())
            state.update(reviews=reviews, reviewed_by='usuario', updated_utc=datetime.now(timezone.utc).isoformat())
            if self.path.exists():
                backup = self.root/'datos/anotaciones/copias'/f'trabadas_{datetime.now():%Y%m%d_%H%M%S_%f}.json'
                backup.parent.mkdir(parents=True, exist_ok=True)
                write_text_atomic(backup, self.path.read_text(encoding='utf-8'))
            write_text_atomic(self.path, json.dumps(state, ensure_ascii=False, indent=2)+'\n')
            return state


def make_handler(review):
    explorer.UI = ROOT/'herramientas/revision_trabadas'
    parent = explorer.make_handler(review.payload, review.audio, review.clips)
    class Handler(parent):
        def reply(self, status, data):
            body = json.dumps(data, ensure_ascii=False).encode('utf-8')
            self.send_response(status)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.send_header('Content-Length', str(len(body)))
            self.send_header('Cache-Control', 'no-store')
            self.end_headers()
            self.wfile.write(body)

        def do_GET(self):
            if self.path == '/api/revision':
                if self.headers.get('Host') != f'127.0.0.1:{self.server.server_port}':
                    self.reply(403, {'error':'Host incorrecto.'})
                    return
                try:
                    self.reply(200, dict(**review.payload, annotation=review.current(), nonce=review.nonce))
                except ValueError as exc:
                    self.reply(409, {'error':str(exc)})
            else:
                super().do_GET()

        def do_POST(self):
            origin = f'http://127.0.0.1:{self.server.server_port}'
            if (self.path != '/api/guardar' or self.headers.get('Host') != origin[7:]
                    or self.headers.get('Origin') != origin or self.headers.get('X-Revision-Token') != review.nonce):
                self.reply(403, {'error':'Petición no permitida.'})
                return
            try:
                size = int(self.headers.get('Content-Length', '0'))
                if not 0 < size <= 100000:
                    raise ValueError('Tamaño incorrecto.')
                state = review.save(json.loads(self.rfile.read(size)))
                self.reply(200, {'annotation':state})
            except (ValueError, KeyError, TypeError) as exc:
                self.reply(400, {'error':str(exc)})

    return Handler


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--puerto', type=int, default=8774)
    args = parser.parse_args()
    review = Review()
    server = ThreadingHTTPServer(('127.0.0.1',args.puerto), make_handler(review))
    print(f'Revisión lista: http://127.0.0.1:{server.server_port}/', flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == '__main__':
    main()
