"""Piloto VAD sí/no sobre cuatro fragmentos revisados, sin cambiar el seguidor."""
from dataclasses import asdict
from datetime import datetime
import hashlib
import importlib.metadata
import json
from time import perf_counter, process_time

from faster_whisper import WhisperModel
from faster_whisper.audio import decode_audio
from faster_whisper.vad import VadOptions
from scripts.alinear import tokens
from scripts.archivos import write_text_atomic
from scripts.catalogo import ROOT, resolve_audio_path
from scripts.recursos import ResourceMonitor


def main():
    reference_path=ROOT/'datos/anotaciones/lectura_02_trabadas_revision_cualitativa.json'
    reference=json.loads(reference_path.read_text(encoding='utf-8'))
    audio_path=resolve_audio_path(reference['audio_file'])
    digest=lambda path:hashlib.sha256(path.read_bytes()).hexdigest()
    assert digest(audio_path)==reference['audio_sha256']
    source_name=next(n for n in reference['source_sha256'] if 'ventana_8s' in n)
    source_path=ROOT/reference['source_folder']/source_name
    assert digest(source_path)==reference['source_sha256'][source_name]
    source=json.loads(source_path.read_text(encoding='utf-8'))
    audio=decode_audio(str(audio_path),sampling_rate=16000)
    folder=ROOT/'resultados/disfluencias'/datetime.now().strftime('%Y%m%d_%H%M%S_%f')
    folder.mkdir(parents=True)
    result=dict(experiment='piloto_vad_si_no_texto_bruto_y_palabras', audio_file=reference['audio_file'],
                audio_sha256=reference['audio_sha256'], reference_sha256=digest(reference_path),
                source_file=source_path.relative_to(ROOT).as_posix(),source_sha256=digest(source_path),
                script_sha256=digest(__import__('pathlib').Path(__file__)),
                model='faster-whisper-small',device='cpu',compute_type='int8',
                versions={name:importlib.metadata.version(name) for name in ['faster-whisper','ctranslate2','av']},
                parameters=dict(language='es',beam_size=5,word_timestamps=True,condition_on_previous_text=False,
                                initial_prompt=None,repetition_penalty=1,no_repeat_ngram_size=0),
                vad_options=asdict(VadOptions()),runs=[],
                notice='Cuatro fragmentos completos de 8 s. Una pasada por condición; orden alternado. Sin referencias exhaustivas ni tasas de eventos. Un solo modelo compartido; tiempos no comparables directamente con rondas históricas. No modifica el seguidor, sus registros ni anotaciones humanas.')
    print('Piloto:',folder,flush=True)
    monitor=ResourceMonitor()
    monitor.start()
    try:
        start=perf_counter()
        model=WhisperModel(str(ROOT/'modelos/faster-whisper-small'),device='cpu',compute_type='int8',local_files_only=True)
        result['model_load_seconds']=perf_counter()-start
        for i,section in enumerate(reference['intervals']):
            clip=audio[round(section['start']*16000):round(section['end']*16000)].copy()
            historical=next(u for u in source['updates'] if u['audio_available_seconds']==section['end'])
            for vad in ([True,False] if i%2==0 else [False,True]):
                start=perf_counter(); cpu=process_time()
                segments,info=model.transcribe(clip.copy(),**result['parameters'],vad_filter=vad)
                raw=[]; heard=[]
                for segment in segments:
                    words=[]
                    for word in segment.words or []:
                        words.append(dict(raw_word=word.word,start=word.start+section['start'],end=word.end+section['start'],probability=word.probability))
                        heard.extend(tokens(word.word))
                    raw.append(dict(text=segment.text,start=segment.start+section['start'],end=segment.end+section['start'],words=words))
                row=dict(fragment=section['id'],audio_start=section['start'],audio_end=section['end'],vad_filter=vad,
                         segments=raw,normalized_words=heard,processing_seconds=perf_counter()-start,
                         cpu_seconds=process_time()-cpu,duration_after_vad=info.duration_after_vad,
                         historical_words=[w['word'] for w in historical['hypothesis']])
                row['matches_historical_words']=row['normalized_words']==row['historical_words']
                result['runs'].append(row)
                write_text_atomic(folder/'piloto.json',json.dumps(result,ensure_ascii=False,indent=2)+'\n')
                print(section['id'],'VAD',vad,repr(' '.join(s['text'] for s in raw)),flush=True)
    finally:
        result['resources']=monitor.stop()
        result['resource_scope']='piloto_completo_con_modelo_compartido'
        write_text_atomic(folder/'piloto.json',json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    lines=['# Piloto de VAD y transcripción literal','',result['notice'],'',
           '| Fragmento | VAD | Texto bruto del modelo | Palabras guardadas |', '|---|---|---|---|']
    for row in result['runs']:
        raw=' '.join(s['text'] for s in row['segments']).replace('|','/').replace('\n',' ')
        lines.append(f"| {row['fragment']} | {row['vad_filter']} | {raw} | {' '.join(row['normalized_words'])} |")
    write_text_atomic(folder/'resumen.md','\n'.join(lines)+'\n')
    print('Resumen:',folder/'resumen.md',flush=True)


if __name__=='__main__':
    main()
