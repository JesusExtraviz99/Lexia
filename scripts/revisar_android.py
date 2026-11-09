"""Importación verificada de JSON Android y diagnóstico por reproducción, sin ASR."""
import argparse,hashlib,json,statistics
from datetime import datetime,timezone
from pathlib import Path
import shutil
from scripts.alinear import tokens
from scripts.seguir import Tracker
from scripts.comparar_margen_directo import MarginTracker
from scripts.diagnosticar_apoyos_android import SupportedTracker

ROOT=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def distribution(values):
    return dict(count=len(values),minimum=min(values),median=statistics.median(values),maximum=max(values)) if values else None

def review(files,out):
    out=Path(out)
    if out.exists():raise ValueError('Revisión existente; no sobrescribir.')
    dest=ROOT/'resultados/android/sesiones/20261109';dest.mkdir(parents=True,exist_ok=True)
    rows=[]
    for src in map(Path,files):
        source_digest=sha(src);data=json.loads(src.read_text(encoding='utf-8'))
        if not data['finished'] or data['runtime']['architecture'] not in (2,4):raise ValueError('Sesión inesperada.')
        if data['story'] not in {p.name for p in (ROOT/'datos/textos').glob('*.txt')}:raise ValueError('Texto desconocido.')
        story_path=ROOT/'datos/textos'/data['story'];story=story_path.read_text(encoding='utf-8-sig')
        assert hashlib.sha256(story.encode()).hexdigest()==data['story_sha256'],'Texto modificado'
        target=dest/src.name
        if target.exists():assert sha(target)==source_digest,'Destino distinto; no se sobrescribe'
        else:shutil.copyfile(src,target)
        assert sha(target)==source_digest
        offset=data.get('tracker_local_search_offset_words',12)
        policy=data.get('tracker_advance_policy','original')
        if offset not in (6,12) or policy not in ('original','terminal_and_recent'):raise ValueError('Perfil del seguidor desconocido')
        configured=offset!=12 or policy!='original'
        tracker=(SupportedTracker(tokens(story),offset,True) if policy=='terminal_and_recent' else MarginTracker(tokens(story),offset)) if configured else Tracker(tokens(story))
        previous=[];trace=[]
        for i,r in enumerate(data['updates']):
            heard=tokens(r['hypothesis'])
            if configured:
                old=tracker.position
                position=tracker.update_recent(r['hypothesis'],r['asr_current_line']) if policy=='terminal_and_recent' else tracker.update(heard)
                # Posición/movimiento se recalculan; los motivos detallados se conservan del exportador nativo.
                state=dict(position=position or None,movement=position-old,mode=r['tracker_mode'],
                           evidence=dict(reason=r['tracker_reason'],exact_matches=r['tracker_exact_matches'],
                                         edit_cost=r['tracker_edit_cost'],hypothesis_words=r['tracker_hypothesis_words']))
            elif heard==previous:
                state=dict(position=tracker.position or None,movement=0,mode='hipotesis_sin_cambios',evidence={})
            else:state=tracker.update(heard)
            assert (state['position'] or 0)==r['position'],f'Posición no reproducida {src.name}/{i}'
            assert state['movement']==r['movement'],f'Movimiento no reproducido {src.name}/{i}'
            previous=heard;trace.append(dict(**r,diagnosis=state))
        plateaus=[];i=0
        while i<len(trace):
            j=i+1
            while j<len(trace) and trace[j]['position']==trace[i]['position']:j+=1
            end=trace[j]['callback_elapsed_ms'] if j<len(trace) else data['wall_ms']
            elapsed=end-trace[i]['callback_elapsed_ms'];segment=trace[i:j]
            if 0<trace[i]['position']<len(tokens(story)) and elapsed>=1500:
                plateaus.append(dict(position=trace[i]['position'],start_ms=trace[i]['callback_elapsed_ms'],end_ms=end,
                    seconds=elapsed/1000,callbacks=len(segment),distinct_texts=len({r['hypothesis'] for r in segment}),
                    rejected_evidence=sum(r['diagnosis']['evidence'].get('reason')=='evidencia_incompatible' for r in segment),
                    examples=[dict(elapsed_ms=r['callback_elapsed_ms'],tail=' '.join(tokens(r['hypothesis'])[-12:]),
                        mode=r['diagnosis']['mode'],evidence=r['diagnosis']['evidence']) for r in segment[:1]+segment[-2:]]))
            i=j
        lines=[r['sdk_last_transcription_latency_ms'] for r in trace if 'sdk_last_transcription_latency_ms' in r]
        samples=data['resource_samples']
        row=dict(file=target.relative_to(ROOT).as_posix(),source_name=src.name,sha256=source_digest,
            model='Tiny' if data['runtime']['architecture']==2 else 'Small',device=data['device'],
            sdk=data['runtime']['sdk'],runtime=data['runtime'],seconds=data['wall_ms']/1000,
            cpu_seconds_app=data['cpu_ms_app']/1000,callbacks=len(trace),final=data['final_position'],
            backwards=sum(r['movement']<0 for r in trace),guide_words=data['guide_words'],
            historical_guide_policy=data.get('guide_policy','fixed_pairs' if data['guide_words']==2 else 'next_word'),
            sdk_complete_line_latency_ms=distribution(lines),pss_mib=distribution([r['pss_kib']/1024 for r in samples]),
            position_plateaus=plateaus,positions_reproduced=True,battery_start=data['battery_start'],battery_end=data['battery_end'],
            reference_words=len(tokens(story)),rejected_updates=sum(r['diagnosis']['evidence'].get('reason')=='evidencia_incompatible' for r in trace))
        row.update(app_version=data.get('app_version','0.1'),tracker_advance_policy=policy,local_search_offset=offset,
                   native_interval_requested=data.get('native_transcription_interval_requested_seconds'),
                   diagnostic_source='native_fields_positions_independently_replayed' if configured else 'python_reconstructed')
        rows.append(row)
    out.mkdir(parents=True)
    payload=dict(created_at_utc=datetime.now(timezone.utc).isoformat(),status='records_reviewed_no_new_inference',sessions=rows,
        all_positions_reproduced=True,no_independent_audio_review=True,
        notice='Mesetas de posición no son por sí solas bloqueos de cómputo o errores lectores. Sin audio/anclas humanas no se miden demoras por palabra ni se atribuyen discrepancias a invenciones. SDK nativo y PC son configuraciones distintas; los tiempos de sus métricas no son directamente equivalentes.')
    (out/'revision.json').write_text(json.dumps(payload,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    text=['# Lecturas Android · revisión técnica','',payload['notice'],'',
        '| Modelo | Intervalo solicitado s | Duración toma s | Callbacks | Final | Retrocesos | PSS máximo MiB | Latencia SDK línea completa mediana ms |',
        '|---|---:|---:|---:|---:|---:|---:|---:|']
    for r in rows:text.append(f"| {r['model']} | {r['native_interval_requested'] if r['native_interval_requested'] is not None else 'no explícito'} | {r['seconds']:.2f} | {r['callbacks']} | {r['final']}/{r['reference_words']} | {r['backwards']} | {r['pss_mib']['maximum']:.1f} | {r['sdk_complete_line_latency_ms']['median']:.1f} |")
    text+=['','Dispositivo exportado: Xiaomi 23090RA98G, Android 16/API36 y unos 11,12 GiB de RAM física visible al sistema (variante comercial de 12 GB). PSS corresponde a toda la app durante la lectura; no se compara como si fuera RSS Windows. CPU acumulada puede superar el tiempo de pared al usar varios hilos. Batería/temperatura son observaciones cortas de app+sistema, no consumo neto del ASR.','',
        'Llegar al final no acredita un seguimiento continuo correcto. Se enumeran posiciones que permanecen estables mientras llegan callbacks. Si cambia el texto pero el alineador rechaza evidencia, no es una congelación total de la interfaz. Si no hay callbacks, no se puede distinguir pausa del lector, segmentación/VAD, cálculo u otras causas solo con estos JSON.','',
        'La política visual se conserva por sesión en revision.json: fixed_pairs en las parejas de 0.1 y sliding_next_words en 0.2. Esta última desplaza las dos palabras guía con cada avance reconocido. Lecturas diferentes no permiten atribuir diferencias de rendimiento solo a esa presentación.','',
        'Las salidas contienen repeticiones y diferencias respecto al cuento; algunas pueden corresponder a intentos de relectura del usuario para desbloquear el marcador. No se puntúan como errores ni se cambia la referencia sin escucha o confirmación específica.','']
    for r in rows:
        text+=['## '+r['model'],'',f"Posiciones estables ≥1,5 s (excluidos inicio y final): {len(r['position_plateaus'])}. Actualizaciones con evidencia incompatible en la reproducción: {r['rejected_updates']}.",'']
        for p in sorted(r['position_plateaus'],key=lambda p:p['seconds'],reverse=True)[:5]:
            text+=[f"### Posición {p['position']} · {p['start_ms']/1000:.2f}–{p['end_ms']/1000:.2f} s · {p['seconds']:.2f} s",'',f"{p['callbacks']} callbacks, {p['distinct_texts']} textos distintos y {p['rejected_evidence']} rechazos de evidencia.",'']
            for e in p['examples']:text.append(f"- {e['elapsed_ms']/1000:.2f} s: {e['tail']} · {e['mode']} · {e['evidence']}")
            text.append('')
    (out/'informe.md').write_text('\n'.join(text)+'\n',encoding='utf-8')
    print('\n'.join(text[:10]));print('Informe:',out/'informe.md')

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('files',type=Path,nargs='+');p.add_argument('--salida',type=Path,required=True)
    a=p.parse_args();review(a.files,a.salida)
