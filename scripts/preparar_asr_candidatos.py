"""Descarga fijada y prueba técnica local de los nuevos candidatos ASR."""
import argparse
from dataclasses import asdict
from datetime import datetime, timezone
import importlib.metadata
import json
import os
from pathlib import Path, PurePosixPath
import shutil
import stat
from time import perf_counter
import urllib.request
import zipfile

from scripts.archivos import write_text_atomic
from scripts.catalogo import ROOT
from scripts.comparar_literalidad import digest
from scripts.recursos import ResourceMonitor

MODELS={
    'xlsr':dict(repo='jonatasgrosman/wav2vec2-large-xlsr-53-spanish',folder='wav2vec2-xlsr-53-spanish',license='Apache-2.0'),
    'vosk':dict(url='https://alphacephei.com/vosk/models/vosk-model-small-es-0.42.zip',folder='vosk-model-small-es-0.42',license='Apache-2.0'),
    'parakeet':dict(repo='nvidia/parakeet-tdt-0.6b-v3',folder='parakeet-tdt-0.6b-v3',license='CC-BY-4.0')}


def save(path,value):
    write_text_atomic(path,json.dumps(value,ensure_ascii=False,indent=2)+'\n')


def hf_download(spec):
    from huggingface_hub import HfApi, snapshot_download, hf_hub_download
    info=HfApi().model_info(spec['repo'],files_metadata=True)
    names={f.rfilename for f in info.siblings}
    allowed={'README.md','LICENSE','LICENSE.txt','config.json','generation_config.json',
             'preprocessor_config.json','processor_config.json','tokenizer_config.json',
             'tokenizer.json','special_tokens_map.json','added_tokens.json','vocab.json',
             'vocab.txt','merges.txt','tokenizer.model','sentencepiece.bpe.model'} & names
    if 'model.safetensors' in names:allowed.add('model.safetensors')
    elif 'model.safetensors.index.json' in names:
        index=hf_hub_download(spec['repo'],'model.safetensors.index.json',revision=info.sha)
        shards=set(json.loads(Path(index).read_text(encoding='utf-8'))['weight_map'].values())
        assert shards <= names
        allowed.update(shards);allowed.add('model.safetensors.index.json')
    elif 'pytorch_model.bin' in names:allowed.add('pytorch_model.bin')
    else:raise ValueError(f"Sin pesos Transformers reconocidos: {spec['repo']}; archivos: {sorted(names)}")
    target=ROOT/'modelos'/spec['folder']
    snapshot_download(spec['repo'],revision=info.sha,local_dir=target,allow_patterns=sorted(allowed),max_workers=3)
    records=[]
    for name in sorted(allowed):
        path=target/name
        sha=digest(path)
        remote=next(f for f in info.siblings if f.rfilename==name)
        lfs=getattr(remote,'lfs',None)
        expected=lfs.get('sha256') if isinstance(lfs,dict) else getattr(lfs,'sha256',None)
        if expected and sha!=expected:raise ValueError(f'Pesos no coincidentes con LFS: {name}')
        records.append(dict(file=name,bytes=path.stat().st_size,sha256=sha,published_lfs_sha256=expected))
    return dict(**spec,revision=info.sha,path=target.relative_to(ROOT).as_posix(),files=records,
                trust_remote_code=False,notice='Revisión fijada; pesos y configuración locales, sin ejecutar Python del repositorio. SHA256 LFS cotejado cuando está publicado.')


def zip_target(name,root,expected_folder):
    parts=PurePosixPath(name).parts
    if (not parts or PurePosixPath(name).is_absolute() or '..' in parts or ':' in name
            or '\\' in name or parts[0]!=expected_folder):
        raise ValueError(f'Ruta ZIP no permitida: {name}')
    target=root.joinpath(*parts).resolve()
    if not target.is_relative_to(root.resolve()):raise ValueError('Ruta fuera de modelos.')
    return target


def vosk_download(spec):
    cache=ROOT/'.tools/cache/vosk';cache.mkdir(parents=True,exist_ok=True)
    archive=cache/(spec['folder']+'.zip')
    if not archive.exists():
        part=archive.with_suffix('.part')
        with urllib.request.urlopen(spec['url'],timeout=90) as response,part.open('wb') as stream:
            shutil.copyfileobj(response,stream)
        part.rename(archive)
    root=ROOT/'modelos';target=root/spec['folder']
    if target.exists():raise FileExistsError(f'No sobrescribir carpeta Vosk existente: {target}')
    with zipfile.ZipFile(archive) as zipped:
        if zipped.testzip() is not None:raise ValueError('CRC ZIP incorrecto.')
        for item in zipped.infolist():
            destination=zip_target(item.filename,root,spec['folder'])
            if stat.S_ISLNK(item.external_attr>>16):raise ValueError('Enlace en ZIP no permitido.')
            if item.is_dir():destination.mkdir(parents=True,exist_ok=True);continue
            destination.parent.mkdir(parents=True,exist_ok=True)
            with zipped.open(item) as incoming,destination.open('xb') as outgoing:
                shutil.copyfileobj(incoming,outgoing)
    files=[dict(file=p.relative_to(target).as_posix(),bytes=p.stat().st_size,sha256=digest(p))
           for p in sorted(target.rglob('*')) if p.is_file()]
    return dict(**spec,path=target.relative_to(ROOT).as_posix(),files=files,
                archive_sha256=digest(archive),archive_bytes=archive.stat().st_size,zip_crc_verified=True,
                notice='Descarga del proveedor oficial; SHA256 local y CRC, sin checksum criptográfico publicado cotejado.')


def download(folder,key):
    os.environ['HF_HOME']=str(ROOT/'.tools/cache/hf-candidatos')
    folder.mkdir(parents=True,exist_ok=True)
    path=folder/(key+'_modelo.json')
    if path.exists():raise FileExistsError(path)
    print('Descargando',key,flush=True)
    record=vosk_download(MODELS[key]) if key=='vosk' else hf_download(MODELS[key])
    record.update(downloaded_date='2026-10-28',status='descargado_verificado',script_sha256=digest(Path(__file__)))
    save(path,record)
    print('Descarga verificada',key,record.get('revision'),sum(f['bytes'] for f in record['files']),flush=True)


def smoke(folder,key):
    import numpy as np
    os.environ['HF_HUB_OFFLINE']='1';os.environ['TOKENIZERS_PARALLELISM']='false'
    model_record=folder/(key+'_modelo.json')
    manifest=json.loads(model_record.read_text(encoding='utf-8'))
    path=ROOT/manifest['path']
    for item in manifest['files']:
        assert digest(path/item['file'])==item['sha256']
    output=dict(model=key,date='2026-10-28',source_model_sha256=digest(model_record),
        script_sha256=digest(Path(__file__)),
        device='cpu',signal='un segundo sintético de ceros mono 16 kHz',
        audio_source='generado_en_memoria_sin_microfono',sample_rate_hz=16000,
        versions={name:importlib.metadata.version(name) for name in ['numpy','torch','transformers','huggingface-hub','vosk','librosa','soundfile']},
        notice='Solo prueba técnica de carga/ejecución, no evaluación de calidad ni benchmark de rendimiento. No usa grabaciones propias o datasets. Recursos incluyen importación/carga y señal sintética.')
    signal=np.zeros(16000,dtype=np.float32)
    monitor=ResourceMonitor();monitor.start()
    try:
        start=perf_counter()
        if key=='vosk':
            from vosk import Model, KaldiRecognizer
            model=Model(str(path))
            output['model_load_seconds']=perf_counter()-start
            recognizer=KaldiRecognizer(model,16000)
            recognizer.AcceptWaveform(np.zeros(16000,dtype=np.int16).tobytes())
            output['synthetic_output']=json.loads(recognizer.FinalResult())
        else:
            import torch
            from transformers import (AutoProcessor,AutoModelForCTC,AutoModelForTDT,
                                      Wav2Vec2FeatureExtractor,Wav2Vec2CTCTokenizer,Wav2Vec2Processor)
            torch.set_num_threads(4)
            if key=='xlsr':
                processor=Wav2Vec2Processor(
                    feature_extractor=Wav2Vec2FeatureExtractor.from_pretrained(path,local_files_only=True),
                    tokenizer=Wav2Vec2CTCTokenizer.from_pretrained(path,local_files_only=True))
                output['decoder']='CTC greedy, sin modelo de lenguaje adicional'
            else:
                processor=AutoProcessor.from_pretrained(path,local_files_only=True,trust_remote_code=False)
            cls=AutoModelForCTC if key=='xlsr' else AutoModelForTDT
            model=cls.from_pretrained(path,local_files_only=True,trust_remote_code=False,dtype=torch.float32,weights_only=True).eval()
            output['model_load_seconds']=perf_counter()-start
            inputs=processor(signal,sampling_rate=16000,return_tensors='pt')
            with torch.inference_mode():
                if key=='xlsr':
                    logits=model(**inputs).logits
                    output['synthetic_output']=processor.batch_decode(logits.argmax(-1))
                    output['logits_shape']=list(logits.shape)
                else:
                    generated=model.generate(**inputs,max_new_tokens=32)
                    output['synthetic_output']=processor.batch_decode(generated.sequences,skip_special_tokens=True)
                    output['generated_sequences_shape']=list(generated.sequences.shape)
            output['cpu_threads']=4
        output['technical_total_seconds']=perf_counter()-start
        output['status']='carga_y_ejecucion_correctas'
    except BaseException as exc:
        output['status']='error';output['error']=repr(exc)
        raise
    finally:
        output['resources']=monitor.stop()
        save(folder/(key+'_prueba_tecnica.json'),output)
    print(key,output['status'],flush=True)


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('mode',choices=['descargar','prueba'])
    parser.add_argument('model',choices=MODELS)
    parser.add_argument('--salida',type=Path,required=True)
    args=parser.parse_args()
    if args.mode=='descargar':download(args.salida.resolve(),args.model)
    else:smoke(args.salida.resolve(),args.model)
