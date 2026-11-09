"""Escucha compartida de casos problemáticos MLS; originales y métricas intactos."""
import argparse
from copy import deepcopy
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import secrets
import threading
from http.server import ThreadingHTTPServer

from scripts.archivos import write_text_atomic
from scripts.revisar_lectores import make_handler

ROOT = Path(__file__).resolve().parents[1]
MOTORS = ['xlsr', 'parakeet', 'whisper', 'crisper', 'vosk']
REFERENCES = ['', 'coincide', 'incompleta', 'diferente', 'dudosa']


def read(path):
    return json.loads(path.read_text(encoding='utf-8'))


def validate(payload, template):
    if not isinstance(payload, dict) or payload.get('audio_sha256') != template['audio_sha256']:
        raise ValueError('Identidad del audio incorrecta.')
    result = deepcopy(template)
    for key, limit in [('notes', 15000), ('heard_transcript', 15000)]:
        value = payload.get(key, '')
        if not isinstance(value, str) or len(value) > limit:
            raise ValueError('Campo incorrecto: '+key)
        result[key] = value.strip()
    for key in ['listened', 'completed']:
        if type(payload.get(key, False)) is not bool:
            raise ValueError('Estado de escucha incorrecto.')
        result[key] = payload.get(key, False)
    result['reference_assessment'] = payload.get('reference_assessment', '')
    if result['reference_assessment'] not in REFERENCES:
        raise ValueError('Valoración de referencia incorrecta.')
    affected = payload.get('asr_errors', [])
    if not isinstance(affected, list) or len(set(affected)) != len(affected) or any(x not in MOTORS for x in affected):
        raise ValueError('Selección de motores incorrecta.')
    result['asr_errors'] = affected
    if result['completed'] and not (result['listened'] and result['reference_assessment'] and result['notes']):
        raise ValueError('Para terminar, confirma escucha, valora la referencia y escribe una nota.')
    result['saved_at_utc'] = datetime.now(timezone.utc).isoformat()
    return result


class Workspace:
    def __init__(self, root=ROOT):
        import soundfile as sf
        self.root, self.lock = root, threading.Lock()
        self.assets = root/'herramientas/revision_mls'
        self.nonce = secrets.token_urlsafe(32)
        self.base = root/'resultados/asr_externo/mls_dev_completo_paralela_01'
        self.folder = self.base/'revision_completa/escucha_humana'
        self.files, self.templates, self.items = {}, {}, []
        source = read(self.base/'revision_completa/transcripciones_comparadas.json')
        manifests = read(self.base/'xlsr/ejecucion.json')['selection']['items']
        by_id = {r['id']: r for r in manifests}
        results = {m: {r['id']: r for r in rows} for m, rows in source.items()}
        cases = {}
        def add(key, reason):
            cases.setdefault(key, []).append(reason)
        add('6671_9310_000053', 'Prioridad 1: repetición extensa en Crisper; comparar con lo realmente audible.')
        add('3678_1378_000014', 'Prioridad 2: varios ASR añaden presentación y capítulos; comprobar si la referencia omite voz real.')
        add('11670_10604_000122', 'Prioridad 3: cierre/crédito añadido; comprobar si existe en el audio.')
        audit = read(self.base/'revision_completa/verificacion.json')
        for motor in audit['motors']:
            for item in motor['native_time_out_of_range']:
                add(item['id'], f"Marca temporal de {motor['motor']} fuera de rango: escuchar el final. No confundir con error textual.")
        for motor in MOTORS:
            for item in sorted(source[motor], key=lambda r: r['wer'], reverse=True)[:3]:
                add(item['id'], 'Entre los tres WER más altos de '+motor+'; selección de diagnóstico, no representativa.')
        cache = root/'.descartados/revision_mls/audio'
        cache.mkdir(parents=True, exist_ok=True)
        for key, reasons in cases.items():
            item = by_id[key]
            original = (root/'datos/externos/mls_es'/item['file']).resolve()
            if not original.is_relative_to((root/'datos/externos/mls_es').resolve()):
                raise ValueError('Ruta de corpus incorrecta.')
            digest = hashlib.sha256(original.read_bytes()).hexdigest()
            if digest != item['sha256']:
                raise ValueError('FLAC diferente al evaluado: '+key)
            # Copia WAV PCM16 para reproducción compatible; sin recorte, filtros o ASR.
            wav = cache/(key+'_'+digest[:12]+'.wav')
            signal, sr = sf.read(original, dtype='int16')
            if not wav.exists():
                sf.write(wav, signal, sr, subtype='PCM_16')
            decoded, wav_sr = sf.read(wav, dtype='int16')
            if wav_sr != sr or decoded.shape != signal.shape or not (decoded == signal).all():
                raise ValueError('Copia de escucha no idéntica en muestras: '+key)
            self.files[key] = wav
            self.templates[key] = dict(schema_version=1, id=key, audio_sha256=digest,
                original_audio_file=original.relative_to(root).as_posix(),
                cohort='mls_dev_completo_paralela_01', reviewer='usuario', independent_second_review=False,
                listened=False, completed=False, reference_assessment='', asr_errors=[], notes='', heard_transcript='',
                notice='Escucha de diagnóstico. No modifica referencias, métricas o salidas originales.')
            hypotheses = []
            for motor in MOTORS:
                native = read(self.base/motor/'audios'/(key+'.json'))
                words = []
                output = native.get('native_output', {})
                if motor == 'crisper':
                    words = output.get('native_result', {}).get('words') or []
                elif motor == 'whisper':
                    words = [w for seg in output.get('native_segments', []) for w in seg.get('words') or []]
                elif motor == 'vosk':
                    words = [w for seg in output.get('native_results', []) for w in seg.get('result', [])]
                hypotheses.append(dict(motor=motor, **results[motor][key], last_words=words[-8:]))
            self.items.append(dict(id=key, name=key, seconds=item['audio_seconds'], reasons=reasons,
                reference=item['reference'], hypotheses=hypotheses, audio='/audio/'+key,
                original=item['file']))

    def current(self, key):
        path = self.folder/(key+'.json')
        if not path.exists():
            return deepcopy(self.templates[key])
        saved = read(path)
        result = validate(saved, self.templates[key])
        result['saved_at_utc'] = saved.get('saved_at_utc')
        return result

    def save(self, key, payload):
        with self.lock:
            result = validate(payload, self.templates[key])
            self.folder.mkdir(parents=True, exist_ok=True)
            path = self.folder/(key+'.json')
            if path.exists():
                backup = self.root/'.descartados/revision_mls/copias'
                backup.mkdir(parents=True, exist_ok=True)
                (backup/f'{key}_{datetime.now():%Y%m%d_%H%M%S_%f}.json').write_bytes(path.read_bytes())
            write_text_atomic(path, json.dumps(result, ensure_ascii=False, indent=2)+'\n')
            return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--puerto', type=int, default=8850)
    args = parser.parse_args()
    workspace = Workspace()
    server = ThreadingHTTPServer(('127.0.0.1', args.puerto), make_handler(workspace))
    print(f'Revisión MLS: {len(workspace.items)} casos · http://127.0.0.1:{server.server_port}/', flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == '__main__':
    main()
