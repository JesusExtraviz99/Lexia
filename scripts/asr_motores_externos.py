"""Adaptadores offline; se importan únicamente las dependencias del motor elegido."""
from dataclasses import asdict
from datetime import datetime, timezone
import json
from pathlib import Path, PurePosixPath
import shutil
import stat
import time
import urllib.request
import zipfile

SPECS = {
    'xlsr': dict(name='xlsr', folder='wav2vec2-xlsr-53-spanish', profile='transformers',
        repo='jonatasgrosman/wav2vec2-large-xlsr-53-spanish',
        revision='96d7e9b4e4a78af515a3c6d3cee7c0826045d276', license='Apache-2.0'),
    'parakeet': dict(name='parakeet', folder='parakeet-tdt-0.6b-v3', profile='transformers',
        repo='nvidia/parakeet-tdt-0.6b-v3', revision='541d1f99c6b0c3cd0b11a95167540bb8edefd82b', license='CC-BY-4.0'),
    'whisper': dict(name='whisper', folder='faster-whisper-small', profile='whisper',
        repo='Systran/faster-whisper-small', revision='536b0662742c02347bc0e980a01041f333bce120', license='MIT'),
    'crisper': dict(name='crisper', folder='crisperwhisper2-small', profile='crisper',
        repo='nyralabs/CrisperWhisper2.0_small', revision='bcaecf0a584a1f600d8897fe6032b9e2e56429a7',
        license='nyra-health-non-commercial-research'),
    'vosk': dict(name='vosk', folder='vosk-model-small-es-0.42', profile='vosk',
        url='https://alphacephei.com/vosk/models/vosk-model-small-es-0.42.zip',
        revision='small-es-0.42', license='Apache-2.0',
        archive_sha256='09b239888f633ef2f0b4e09736e3d9936acfd810bc65d53fad45261762c6511f'),
}
FILES = {
    'parakeet': ['README.md', 'config.json', 'generation_config.json', 'model.safetensors',
                 'processor_config.json', 'tokenizer.json', 'tokenizer_config.json'],
    'whisper': ['README.md', 'config.json', 'model.bin', 'tokenizer.json', 'vocabulary.txt'],
    'crisper': ['added_tokens.json', 'config.json', 'generation_config.json', 'LICENSE.md',
        'merges.txt', 'model.safetensors', 'normalizer.json', 'preprocessor_config.json', 'README.md',
        'special_tokens_map.json', 'tokenizer.json', 'tokenizer_config.json', 'vocab.json'],
}
PACKAGES = {
    'xlsr': ['torch', 'transformers', 'accelerate', 'librosa', 'huggingface-hub'],
    'parakeet': ['torch', 'transformers', 'accelerate', 'librosa', 'huggingface-hub'],
    'crisper': ['torch', 'transformers', 'crisperwhisper', 'huggingface-hub'],
    'whisper': ['faster-whisper', 'ctranslate2', 'av', 'huggingface-hub'],
    'vosk': ['vosk'],
}


def parameters(motor):
    common = dict(precision='float32', batch_size=1, vad=False, denoise=False, language='es')
    if motor == 'xlsr':
        return dict(**common, decoder='CTC greedy without external LM')
    if motor == 'parakeet':
        common['language'] = 'multilingual model, automatic'
        return dict(**common, decoder='Transformers TDT generate', max_new_tokens=512)
    if motor == 'whisper':
        return dict(**common, decoder='CTranslate2 Whisper', beam_size=5, temperature=0,
                    condition_on_previous_text=False, word_timestamps=True)
    if motor == 'crisper':
        return dict(**common, decoder='Crisper Transformers verbatim', mode='verbatim',
                    max_new_tokens=256, temperature_fallback=True, hallucination_mitigation=True,
                    word_timestamps=True, longform_strategy='continuation', chunk_duration=30.0,
                    stride=26.0, context_words=12, drop_words=2, timestamp_aware_drop=True,
                    early_eot_recovery=True)
    return dict(precision='native Kaldi; no user float32 claim', decoder='KaldiRecognizer native graph',
                batch_size=1, endpointing='native defaults', words=True,
                vad='native endpointing, no external trimming', denoise=False, language='es',
                pcm_conversion='float32 to clipped rounded signed PCM16', chunk_samples=4000)


def safe_member(name, root, folder):
    posix = PurePosixPath(name)
    if (posix.is_absolute() or not posix.parts or posix.parts[0] != folder or
            '..' in posix.parts or ':' in name or '\\' in name):
        raise ValueError('Ruta ZIP no permitida: '+name)
    target = root.joinpath(*posix.parts).resolve()
    if not target.is_relative_to(root.resolve()):
        raise ValueError('Ruta ZIP fuera del directorio de modelos.')
    return target


def download(folder, motor, sha, save):
    spec = SPECS[motor]
    folder = Path(folder).resolve()
    if motor == 'vosk':
        cache = folder.parent/'.descargas'
        cache.mkdir(parents=True, exist_ok=True)
        archive = cache/(spec['folder']+'.zip')
        if not archive.exists():
            part = archive.with_suffix('.part')
            with urllib.request.urlopen(spec['url'], timeout=90) as incoming, part.open('wb') as out:
                shutil.copyfileobj(incoming, out)
            part.replace(archive)
        if sha(archive) != spec['archive_sha256']:
            raise ValueError('Vosk ZIP difiere de la huella local fijada el 28/10/2026.')
        if folder.name != spec['folder']:
            raise ValueError('Vosk requiere el nombre de carpeta oficial.')
        with zipfile.ZipFile(archive) as z:
            if z.testzip() is not None:
                raise ValueError('CRC ZIP incorrecto.')
            for member in z.infolist():
                target = safe_member(member.filename, folder.parent, spec['folder'])
                if stat.S_ISLNK(member.external_attr >> 16):
                    raise ValueError('Enlace simbólico no permitido en ZIP.')
                if member.is_dir():
                    target.mkdir(parents=True, exist_ok=True)
                    continue
                target.parent.mkdir(parents=True, exist_ok=True)
                if target.exists():
                    if target.read_bytes() != z.read(member):
                        raise ValueError('Archivo Vosk local diferente; no se sobrescribe: '+str(target))
                else:
                    with z.open(member) as incoming, target.open('xb') as out:
                        shutil.copyfileobj(incoming, out)
        names = sorted(p.relative_to(folder).as_posix() for p in folder.rglob('*')
                       if p.is_file() and p.name != 'lexia_modelo.json')
        expected = {}
    else:
        from huggingface_hub import HfApi, snapshot_download
        info = HfApi().model_info(spec['repo'], revision=spec['revision'], files_metadata=True)
        if info.sha != spec['revision']:
            raise ValueError('Revisión no coincidente.')
        expected = {f.rfilename: f for f in info.siblings}
        names = FILES[motor]
        if not set(names) <= expected.keys():
            raise ValueError('Archivos no encontrados en la revisión fijada.')
        snapshot_download(spec['repo'], revision=spec['revision'], local_dir=folder,
                          allow_patterns=names, max_workers=3)
    files = []
    for name in names:
        path = folder/name
        digest = sha(path)
        lfs = getattr(expected.get(name), 'lfs', None)
        published = lfs.get('sha256') if isinstance(lfs, dict) else getattr(lfs, 'sha256', None)
        if published and published != digest:
            raise ValueError('Hash LFS no coincide: '+name)
        files.append(dict(file=name, sha256=digest, bytes=path.stat().st_size,
                          published_lfs_sha256=published))
    save(folder/'lexia_modelo.json', dict(**spec, files=files, downloaded_at_utc=datetime.now(timezone.utc).isoformat(),
        verification='LFS cuando existe; Vosk CRC y SHA fijada localmente, no checksum publicado independiente'))
    print('Modelo descargado y verificado:', motor, folder, flush=True)


def check(folder, motor, sha):
    manifest = json.loads((Path(folder)/'lexia_modelo.json').read_text(encoding='utf-8'))
    if any(manifest.get(k) != v for k, v in SPECS[motor].items()):
        raise ValueError('Modelo/revisión no coinciden con el motor solicitado.')
    if motor != 'vosk' and {f['file'] for f in manifest['files']} != set(FILES[motor]):
        raise ValueError('Lista de archivos del modelo no coincidente.')
    for f in manifest['files']:
        relative = PurePosixPath(f['file'])
        if relative.is_absolute() or '..' in relative.parts or ':' in f['file'] or '\\' in f['file']:
            raise ValueError('Ruta de manifiesto no válida.')
        if sha(Path(folder)/f['file']) != f['sha256']:
            raise ValueError('Modelo modificado: '+f['file'])
    return manifest


def load(motor, folder, gpu, threads):
    """Retorna callable y Torch solo si ese backend realmente lo utiliza."""
    if motor in ('parakeet', 'crisper'):
        import torch
        torch.set_num_threads(threads)
        torch.manual_seed(42)
        torch.backends.cudnn.benchmark = False
        if gpu is not None and (not torch.cuda.is_available() or torch.cuda.device_count() != 1):
            raise RuntimeError('Se exige una GPU visible; sin fallback automático a CPU.')
        device = 'cuda:0' if gpu is not None else 'cpu'
        def sync():
            if gpu is not None:
                torch.cuda.synchronize()
        if motor == 'parakeet':
            from transformers import AutoModelForTDT, AutoProcessor
            processor = AutoProcessor.from_pretrained(folder, local_files_only=True, trust_remote_code=False)
            model = AutoModelForTDT.from_pretrained(folder, local_files_only=True, trust_remote_code=False,
                dtype=torch.float32, weights_only=True).eval().to(device)
            def infer(signal):
                begin = time.perf_counter()
                inputs = processor(signal, sampling_rate=16000, return_tensors='pt').to(device)
                sync()
                prepare = time.perf_counter()-begin
                begin = time.perf_counter()
                with torch.inference_mode():
                    generated = model.generate(**inputs, max_new_tokens=512)
                sync()
                forward = time.perf_counter()-begin
                begin = time.perf_counter()
                ids = generated.sequences.cpu()
                text = processor.batch_decode(ids, skip_special_tokens=True)[0]
                decode = time.perf_counter()-begin
                return dict(hypothesis=text, token_ids=ids.tolist()[0], prepare_seconds=prepare,
                    forward_seconds=forward, decode_seconds=decode,
                    generation_cap_reached=ids.shape[-1] >= 512)
            infer.parameter_count = sum(p.numel() for p in model.parameters())
        else:
            from crisperwhisper import CrisperWhisperModel
            model = CrisperWhisperModel(str(folder), backend='transformers', compute_type='float32',
                                       device='cuda' if gpu is not None else 'cpu', device_index=0)
            def infer(signal):
                sync()
                begin = time.perf_counter()
                result = model.transcribe(signal, language='es', mode='verbatim', sr=16000,
                    word_timestamps=True, max_new_tokens=256, hallucination_mitigation=True,
                    temperature_fallback=True, longform_strategy='continuation', chunk_duration=30.0,
                    stride=26.0, context_words=12, drop_words=2, timestamp_aware_drop=True,
                    early_eot_recovery=True)
                sync()
                return dict(hypothesis=result.text, token_ids=None, native_result=asdict(result),
                    prepare_seconds=None, forward_seconds=None, decode_seconds=None,
                    native_transcribe_seconds=time.perf_counter()-begin)
        sync()
        return infer, torch
    if motor == 'whisper':
        from faster_whisper import WhisperModel
        model = WhisperModel(str(folder), device='cuda' if gpu is not None else 'cpu', device_index=0,
            compute_type='float32', cpu_threads=threads, num_workers=1, local_files_only=True)
        def infer(signal):
            begin = time.perf_counter()
            segments, info = model.transcribe(signal, language='es', beam_size=5, temperature=0,
                condition_on_previous_text=False, word_timestamps=True, vad_filter=False)
            # Consumir generador: cronometrar solo transcribe() no mide la inferencia.
            native = [asdict(segment) for segment in segments]
            text = ' '.join(s['text'].strip() for s in native).strip()
            return dict(hypothesis=text, token_ids=[s.get('tokens') for s in native],
                native_segments=native, language_probability=info.language_probability,
                prepare_seconds=None, forward_seconds=None, decode_seconds=None,
                native_transcribe_seconds=time.perf_counter()-begin)
        return infer, None
    if motor == 'vosk':
        if gpu is not None:
            raise ValueError('Este adaptador Vosk utiliza CPU.')
        import numpy as np
        from vosk import Model, KaldiRecognizer
        model = Model(str(folder))
        def infer(signal):
            begin = time.perf_counter()
            pcm = np.clip(np.rint(signal.astype(np.float64)*32768), -32768, 32767).astype('<i2').tobytes()
            prepare = time.perf_counter()-begin
            begin = time.perf_counter()
            recognizer = KaldiRecognizer(model, 16000)
            recognizer.SetWords(True)
            parts = []
            for offset in range(0, len(pcm), 8000):
                if recognizer.AcceptWaveform(pcm[offset:offset+8000]):
                    parts.append(json.loads(recognizer.Result()))
            parts.append(json.loads(recognizer.FinalResult()))
            return dict(hypothesis=' '.join(p.get('text', '') for p in parts).strip(), token_ids=None,
                native_results=parts, prepare_seconds=prepare, forward_seconds=None, decode_seconds=None,
                native_transcribe_seconds=time.perf_counter()-begin)
        return infer, None
    raise ValueError('Motor no soportado: '+motor)
