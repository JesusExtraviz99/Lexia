"""Reproduce solo el VAD de las ventanas revisadas; no ejecuta reconocimiento."""
from dataclasses import asdict
import hashlib
import importlib.metadata
import json

from faster_whisper.audio import decode_audio
from faster_whisper.vad import VadOptions, get_speech_timestamps
from scripts.archivos import write_text_atomic
from scripts.catalogo import ROOT, resolve_audio_path


def main():
    annotation_path=ROOT/'datos/anotaciones/lectura_02_trabadas_revision_cualitativa.json'
    annotation=json.loads(annotation_path.read_text(encoding='utf-8'))
    audio_path=resolve_audio_path(annotation['audio_file'])
    assert hashlib.sha256(audio_path.read_bytes()).hexdigest()==annotation['audio_sha256']
    audio=decode_audio(str(audio_path), sampling_rate=16000)
    options=VadOptions()
    rows=[]
    for name, expected in annotation['source_sha256'].items():
        path=ROOT/annotation['source_folder']/name
        assert hashlib.sha256(path.read_bytes()).hexdigest()==expected
        source=json.loads(path.read_text(encoding='utf-8'))
        for update in source['updates']:
            end=update['audio_available_seconds']
            section=next((s for s in annotation['intervals'] if s['start']<end<=s['end']),None)
            if not section:
                continue
            start=update['audio_window_start_seconds']
            clip=audio[round(start*16000):round(end*16000)].copy()
            chunks=get_speech_timestamps(clip, options, sampling_rate=16000)
            kept=sum(c['end']-c['start'] for c in chunks)
            row=dict(fragment=section['id'], window_seconds=source['audio_window_seconds'],
                     audio_start_seconds=start,audio_end_seconds=end,
                     input_samples=len(clip),kept_samples=kept,removed_samples=len(clip)-kept,
                     retained_intervals_seconds=[dict(start=start+c['start']/16000,end=start+c['end']/16000) for c in chunks])
            rows.append(row)
            print(f"{row['fragment']} | ventana {row['window_seconds']} s | {start:g}-{end:g} s | retirado {(len(clip)-kept)/16000:.4f} s")
    result=dict(analysis='reproduccion_del_VAD_sin_inferencias_ASR',
                faster_whisper_version=importlib.metadata.version('faster-whisper'),
                vad_options=asdict(options),audio_sha256=annotation['audio_sha256'],
                annotation_sha256=hashlib.sha256(annotation_path.read_bytes()).hexdigest(),
                source_sha256=annotation['source_sha256'], windows=rows,
                notice='Reproduce el VAD predeterminado de la versión instalada sobre los mismos recortes. Sin tiempos humanos de cada evento no identifica qué trabada coincide con un eventual recorte. No mide reconocimiento ni tasa de detección. No modifica audio, ASR ni anotaciones.')
    folder=ROOT/annotation['source_folder']
    output=folder/'diagnostico_vad_trabadas.json'
    write_text_atomic(output,json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(f"Ventanas completas: {sum(r['removed_samples']==0 for r in rows)}/{len(rows)}. Informe: {output}")


if __name__=='__main__':
    main()
