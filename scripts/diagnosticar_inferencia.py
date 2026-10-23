"""Perfila cortes ASR guardados sin cambiar el reconocimiento habitual ni el seguidor."""
import argparse
from datetime import datetime
import hashlib
import importlib.metadata
import json
import random
from time import perf_counter
from pathlib import Path

from scripts.seguir import ROOT, audio_bounds


class MeasuredModel:
    """Interpone medidas en operaciones nativas; conserva argumentos y resultados."""
    def __init__(self, model):
        self.wrapped = model
        self.events = []
        self.tokenizer = None
        self.options = None

    def __getattr__(self, name):
        target = getattr(self.wrapped, name)
        if name not in ('encode', 'generate', 'align'):
            return target
        def measured(*args, **kwargs):
            tick = perf_counter()
            result = target(*args, **kwargs)
            event = {'operation': name, 'seconds': perf_counter()-tick}
            if name == 'generate':
                from faster_whisper.transcribe import get_compression_ratio
                first = result[0]
                ids = first.sequences_ids[0]
                text = self.tokenizer.decode(ids).strip()
                avg = first.scores[0] * len(ids)**self.options.length_penalty / (len(ids)+1)
                event.update(temperature=kwargs.get('sampling_temperature', 0),
                             tokens=len(ids), text=text, avg_logprob=avg,
                             compression_ratio=get_compression_ratio(text),
                             no_speech_prob=first.no_speech_prob,
                             log_prob_threshold=self.options.log_prob_threshold,
                             compression_ratio_threshold=self.options.compression_ratio_threshold)
            self.events.append(event)
            return result
        return measured


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('carpeta', type=Path)
    parser.add_argument('--repeticiones', type=int, default=3, choices=range(1, 6))
    parser.add_argument('--solo-corte', type=int, help='Limitar a este corte, por ejemplo 22.')
    parser.add_argument('--sin-fallback', action='store_true', help='Ablación experimental: solo temperatura 0.')
    args = parser.parse_args()
    from faster_whisper import WhisperModel
    from faster_whisper.audio import decode_audio

    class ProfiledWhisper(WhisperModel):
        def generate_with_fallback(self, encoder_output, prompt, tokenizer, options):
            self.model.tokenizer, self.model.options = tokenizer, options
            return super().generate_with_fallback(encoder_output, prompt, tokenizer, options)

    source = args.carpeta.resolve()
    manifest = json.loads((source / 'resumen.json').read_text(encoding='utf-8'))
    records = {}
    for run in manifest['runs']:
        if run['window_seconds'] in [4, 8] and run['repeat'] == 1:
            path = (source / run['record_file']).resolve()
            if path.parent != source:
                raise ValueError('Registro fuera de carpeta.')
            records[run['window_seconds']] = json.loads(path.read_text(encoding='utf-8'))
    if set(records) != {4, 8} or len({d['audio_file'] for d in records.values()}) != 1:
        raise ValueError('Se requieren ventanas 4/8 del mismo audio.')
    from scripts.catalogo import resolve_audio_path
    audio_path = resolve_audio_path(records[4]['audio_file'])
    audio = decode_audio(str(audio_path), sampling_rate=16000)
    tick = perf_counter()
    model = ProfiledWhisper(str(ROOT / 'modelos/faster-whisper-small'), device='cpu',
                            compute_type='int8', local_files_only=True)
    load_seconds = perf_counter()-tick
    model.model = MeasuredModel(model.model)
    options = dict(language='es', beam_size=5, word_timestamps=True, vad_filter=True,
                   condition_on_previous_text=False)
    if args.sin_fallback:
        options['temperature'] = 0
    cuts = [args.solo_corte] if args.solo_corte else [20, 22, 24]
    plan = []
    rng = random.Random(20261021)
    for repeat in range(1, args.repeticiones+1):
        pairs = [(w, c) for w in [4, 8] for c in cuts]
        rng.shuffle(pairs)
        plan.extend((repeat, w, c) for w, c in pairs)
    folder = ROOT / 'resultados/diagnostico_inferencia' / datetime.now().strftime('%Y%m%d_%H%M%S_%f')
    folder.mkdir(parents=True)
    report = {'notice': 'Nuevas inferencias instrumentadas sobre cortes aislados en orden aleatorio por ronda. '
              'Modelo cargado una vez; primera llamada puede incluir calentamiento. No modifica reglas ni registros originales. '
              'Ablación solo temperatura cero cuando se indica; no implica recomendación ni activación.',
              'source_folder': str(source), 'source_manifest_sha256': hashlib.sha256((source/'resumen.json').read_bytes()).hexdigest(),
              'audio_file': audio_path.name, 'audio_sha256': hashlib.sha256(audio_path.read_bytes()).hexdigest(),
              'script_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              'transcribe_source_sha256': hashlib.sha256((ROOT/'.venv/Lib/site-packages/faster_whisper/transcribe.py').read_bytes()).hexdigest(),
              'versions': {n: importlib.metadata.version(n) for n in ['faster-whisper', 'ctranslate2', 'av']},
              'options': options, 'model_load_seconds': load_seconds, 'runs': []}
    print(f'Diagnóstico en {folder}', flush=True)
    for repeat, window, cutoff in plan:
        begin, end = audio_bounds(round(cutoff*16000), window)
        if end > len(audio):
            raise ValueError('Corte fuera del audio.')
        model.model.events = []
        tick = perf_counter()
        segments, info = model.transcribe(audio[begin:end].copy(), **options)
        preprocess = perf_counter()-tick
        segments = list(segments)
        total = perf_counter()-tick
        entry = {'repeat': repeat, 'window_seconds': window, 'cut_seconds': cutoff,
                 'audio_start_seconds': begin/16000, 'audio_end_seconds': end/16000,
                 'total_seconds': total, 'transcribe_return_seconds': preprocess,
                 'vad_duration_seconds': info.duration_after_vad,
                 'native_events': model.model.events,
                 'segments': [{'start': s.start+begin/16000, 'end': s.end+begin/16000,
                               'text': s.text, 'temperature': s.temperature, 'avg_logprob': s.avg_logprob,
                               'words': [{'word': w.word, 'start': w.start+begin/16000, 'end': w.end+begin/16000}
                                         for w in s.words or []]} for s in segments]}
        report['runs'].append(entry)
        (folder/'resumen.json').write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
        events = entry['native_events']
        times = {op: sum(e['seconds'] for e in events if e['operation'] == op) for op in ['encode', 'generate', 'align']}
        attempts = [e['temperature'] for e in events if e['operation'] == 'generate']
        print(f"Ronda {repeat} | ventana {window} | corte {cutoff} | total {total:.2f}s | etapas {times} | temperaturas {attempts}", flush=True)
        print(' ASR: '+' '.join(s.text for s in segments), flush=True)
    print(f'Informe: {folder / "resumen.json"}', flush=True)


if __name__ == '__main__':
    main()
