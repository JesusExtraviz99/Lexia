"""Adaptadores de la segunda ronda, aislados del protocolo anterior. Literales excluidos."""
import json
from pathlib import Path
import time

from scripts.preparar_ampliacion_asr import REGISTRY, FOLDER

KEYS = [key for key, (_, purpose) in REGISTRY.items() if purpose == 'asr']
SPECS = {key: dict(name=key, folder='ampliacion_20261106/'+key, profile='ampliacion',
                   repo=REGISTRY[key][0], manifest='lexia_modelo_ampliacion.json') for key in KEYS}
PACKAGES = {key: ['torch','torchaudio','transformers','accelerate','librosa','huggingface-hub'] for key in KEYS}


def parameters(motor):
    return dict(precision='float32', batch_size=1, vad=False, denoise=False, language='es',
                decoder=('CTC greedy' if motor=='granite_turboctc' else 'Transformers generate'),
                beams=5 if motor=='whisper_turbo' else 1,
                max_new_tokens=('duration*6.5+2' if motor.startswith('moonshine') else 444 if motor=='whisper_turbo' else None if motor=='granite_turboctc' else 512),
                word_timestamps=False, source_language_conditioning=motor in ('qwen_asr_06b','qwen_asr_17b','canary_v2','whisper_turbo'),
                notice='Offline por clip completo, sin reglas del seguidor. Whisper usa Transformers y no CT2; tiempos de backend no equivalentes.')


def check(folder, motor, sha):
    if motor not in SPECS:
        raise ValueError('Solo nuevos ASR, sin modelos literales.')
    manifest=json.loads((Path(folder)/'lexia_modelo_ampliacion.json').read_text(encoding='utf-8'))
    fixed=json.loads((FOLDER/'checkpoints_fijados.json').read_text(encoding='utf-8'))['models'][motor]
    if any(manifest[k]!=fixed[k] for k in ('repo','revision','purpose')) or manifest['purpose']!='asr':
        raise ValueError('Modelo/revisión distintos del protocolo nuevo.')
    if {x['file'] for x in manifest['files']} != {x['file'] for x in fixed['files']}:
        raise ValueError('Lista de archivos incompleta o diferente del checkpoint fijado.')
    for item in manifest['files']:
        file=Path(folder)/item['file']
        if file.parent.resolve()!=Path(folder).resolve() or sha(file)!=item['sha256']:
            raise ValueError('Archivo de modelo modificado.')
    return dict(name=motor,repo=manifest['repo'],revision=manifest['revision'],files=manifest['files'])


def load(motor, folder, gpu, threads):
    import torch
    from transformers import AutoProcessor, AutoModelForSpeechSeq2Seq, AutoModelForCTC, Qwen3ASRForConditionalGeneration
    if motor not in SPECS:
        raise ValueError('No se permiten pruebas de literales.')
    torch.set_num_threads(threads)
    torch.manual_seed(42)
    torch.backends.cudnn.benchmark=False
    if gpu is not None and (not torch.cuda.is_available() or torch.cuda.device_count()!=1):
        raise RuntimeError('Se requiere una única GPU visible, sin fallback.')
    device='cuda:0' if gpu is not None else 'cpu'
    processor=AutoProcessor.from_pretrained(folder,local_files_only=True,trust_remote_code=False)
    cls=AutoModelForCTC if motor=='granite_turboctc' else Qwen3ASRForConditionalGeneration if motor.startswith('qwen_') else AutoModelForSpeechSeq2Seq
    model, loading=cls.from_pretrained(folder,local_files_only=True,trust_remote_code=False,
                 dtype=torch.float32,weights_only=True,attn_implementation='eager',output_loading_info=True)
    if loading.get('missing_keys') or loading.get('mismatched_keys') or loading.get('unexpected_keys'):
        raise RuntimeError('Checkpoint no coincide con la implementación: '+str(loading)[:4000])
    model=model.eval().to(device)
    def sync():
        if gpu is not None:
            torch.cuda.synchronize()
    def infer(signal):
        begin=time.perf_counter()
        if motor.startswith('qwen_'):
            inputs=processor.apply_transcription_request(signal,language='Spanish',sampling_rate=16000,return_tensors='pt')
        elif motor=='canary_v2':
            inputs=processor.apply_transcription_request(signal,source_language='es',target_language='es',sampling_rate=16000,return_tensors='pt')
        else:
            inputs=processor(signal,sampling_rate=16000,return_tensors='pt',return_attention_mask=True)
        inputs=inputs.to(device)
        sync(); prepare=time.perf_counter()-begin
        options={}
        cap=None
        if motor!='granite_turboctc':
            cap=int(len(signal)/16000*6.5)+2 if motor.startswith('moonshine') else 444 if motor=='whisper_turbo' else 512
            options=dict(max_new_tokens=cap,num_beams=5 if motor=='whisper_turbo' else 1,do_sample=False)
        if motor=='whisper_turbo':
            options.update(language='es',task='transcribe')
        begin=time.perf_counter()
        with torch.inference_mode():
            generated=model.generate(**inputs,**options)
        sync(); forward=time.perf_counter()-begin
        begin=time.perf_counter()
        ids=generated.sequences if hasattr(generated,'sequences') else generated
        prompt=inputs['input_ids'].shape[-1] if motor.startswith('qwen_') else 0
        output=ids[:,prompt:]
        if motor.startswith('qwen_'):
            hypothesis=processor.decode(output[0].cpu(),return_format='transcription_only')
        else:
            hypothesis=processor.batch_decode(output.cpu(),skip_special_tokens=True)[0]
        tokens=output[0].cpu().tolist()
        generated_count=len(tokens)-(4 if motor=='whisper_turbo' else 0)
        return dict(hypothesis=hypothesis,token_ids=tokens,
                    generation_cap_reached=(generated_count>=cap if cap is not None else None),
                    prepare_seconds=prepare,forward_seconds=forward,decode_seconds=time.perf_counter()-begin)
    infer.parameter_count=sum(p.numel() for p in model.parameters())
    return infer,torch
