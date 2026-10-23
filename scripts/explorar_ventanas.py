"""Explorador local de fragmentos acústicos y decisiones ASR ya guardadas."""
import argparse
from io import BytesIO
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
from pathlib import Path
import wave

from scripts.anotar import ROOT
from scripts.comparar_seguidores import Tracker, CombinedTracker, replay
from scripts.comparar_recuperacion import ExactRecoveryTracker
from scripts.seguir import locate
from scripts.catalogo import audio_identity, resolve_audio_path, report_stem

UI = ROOT / 'herramientas/explorador_ventanas'


def load_experiment(folder):
    from faster_whisper.audio import decode_audio
    import numpy as np
    manifest = json.loads((folder / 'resumen.json').read_text(encoding='utf-8'))
    runs, clips, audio_name, audio = [], {}, None, None
    for run in manifest['runs']:
        path = (folder / run['record_file']).resolve()
        if path.parent != folder:
            raise ValueError('Registro fuera de la carpeta.')
        data = json.loads(path.read_text(encoding='utf-8'))
        if audio_name is None:
            audio_name = data['audio_file']
            if Path(audio_name).name != audio_name:
                raise ValueError('Nombre de audio inválido.')
            audio = decode_audio(str(resolve_audio_path(audio_name)), sampling_rate=16000)
        if audio_name != data['audio_file'] or abs(len(audio)/16000-data['audio_seconds']) > .01:
            raise ValueError('Se requiere una sola grabación compatible.')
        traces = {name: replay(data, cls) for name, cls in
                  [('original', Tracker), ('combinada', CombinedTracker), ('nueva', ExactRecoveryTracker)]}
        if [(u['position'], u['mode']) for u in data['updates']] != [
                (u['position'], u['mode']) for u in traces['original']['updates']]:
            raise ValueError('No se reproduce el original.')
        rows = []
        for i, row in enumerate(data['updates']):
            start, end = row['audio_window_start_seconds'], row['audio_window_end_seconds']
            key = f"{run['window_seconds']}/{run['repeat']}/{i}"
            clips[key] = (round(start*16000), round(end*16000))
            heard = [w['word'] for w in row['hypothesis']]
            rows.append({'start': start, 'end': end, 'clip': '/clip/'+key,
                         'hypothesis': heard, 'processing': row['processing_seconds'],
                         'ready': row['sequential_ready_seconds_simulated'],
                         'global_candidate_diagnostic': locate(data['story_words'], heard,
                                                               row['previous_position'], global_search=True)['position'],
                         'variants': {name: {k: trace['updates'][i][k] for k in
                                            ['position', 'word', 'mode', 'movement', 'evidence']}
                                      for name, trace in traces.items()}})
        runs.append({'window': run['window_seconds'], 'repeat': run['repeat'], 'rows': rows})
    peaks = [float(np.max(np.abs(audio[i:i+800]))) for i in range(0, len(audio), 800)]
    return {'audio': audio_name, 'audio_label': audio_identity(audio_name)['label'], 'duration': len(audio)/16000, 'story': data['story_words'],
            'peaks': peaks, 'runs': runs}, audio, clips


def clip_wav(audio, begin, end):
    # El mismo remuestreo/mono de seguir.py. PCM16 solo para escucha en el navegador.
    import numpy as np
    output = BytesIO()
    with wave.open(output, 'wb') as wav:
        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(16000)
        wav.writeframes(np.clip(np.rint(audio[begin:end]*32768), -32768, 32767).astype('<i2').tobytes())
    return output.getvalue()


def make_handler(payload, audio, clips):
    class Handler(BaseHTTPRequestHandler):
        def log_message(self, *_):
            pass

        def do_GET(self):
            if self.headers.get('Host') != f'127.0.0.1:{self.server.server_port}':
                self.send_error(403)
                return
            if self.path == '/data':
                body, mime = json.dumps(payload, ensure_ascii=False).encode(), 'application/json'
            elif self.path.startswith('/clip/') and self.path[6:] in clips:
                body, mime = clip_wav(audio, *clips[self.path[6:]]), 'audio/wav'
            elif self.path in ['/', '/app.js', '/style.css']:
                filename, mime = {'/': ('index.html', 'text/html'), '/app.js': ('app.js', 'text/javascript'),
                                  '/style.css': ('style.css', 'text/css')}[self.path]
                body = (UI / filename).read_bytes()
            else:
                self.send_error(404)
                return
            self.send_response(200)
            self.send_header('Content-Type', mime + ('; charset=utf-8' if mime != 'audio/wav' else ''))
            self.send_header('Content-Length', str(len(body)))
            self.send_header('Cache-Control', 'no-store')
            self.send_header('X-Content-Type-Options', 'nosniff')
            self.send_header('Content-Security-Policy', "default-src 'self'; script-src 'self'; style-src 'self'; media-src 'self'; connect-src 'self'; object-src 'none'; frame-ancestors 'none'")
            self.end_headers()
            try:
                self.wfile.write(body)
            except (BrokenPipeError, ConnectionResetError, ConnectionAbortedError):
                pass
    return Handler


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('carpeta', type=Path)
    parser.add_argument('--puerto', type=int, default=8771)
    args = parser.parse_args()
    payload, audio, clips = load_experiment(args.carpeta.resolve())
    server = ThreadingHTTPServer(('127.0.0.1', args.puerto), make_handler(payload, audio, clips))
    print(f'Explorador listo: http://127.0.0.1:{server.server_port}/', flush=True)
    print('Solo lectura: audio local y resultados guardados. No ejecuta ASR ni modifica anotaciones.', flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == '__main__':
    main()
