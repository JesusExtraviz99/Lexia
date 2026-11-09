"""Resume sesiones de micrófono ya guardadas; no ejecuta ASR ni cambia reglas."""
import argparse
from datetime import datetime,timezone
import hashlib
import json
from pathlib import Path
import statistics


def analyze(files,out,single_reading_confirmed=False):
    out=Path(out)
    if out.exists():raise ValueError('No sobrescribir una revisión anterior.')
    rows=[];hashes={}
    for path in map(Path,files):
        raw=path.read_bytes();s=json.loads(raw)
        if s['source']!='microfono_navegador' or not s['finished']:raise ValueError('Se requiere una sesión de micrófono terminada.')
        hashes[str(path)]=hashlib.sha256(raw).hexdigest()
        updates=s['updates']
        if not updates:raise ValueError('Sesión sin actualizaciones.')
        backwards=[]
        for i,r in enumerate(updates):
            if r['movement']<0:
                backwards.append(dict(index=i,cut=r['audio_end_seconds'],previous=r['previous_position'],
                    position=r['position'],movement=r['movement'],mode=r['mode'],
                    context=[dict(cut=x['audio_end_seconds'],position=x['position'],hypothesis=x['hypothesis']) for x in updates[max(0,i-1):i+2]]))
        render=[r['browser']['estimated_cut_age_at_render_ms'] for r in updates if 'browser' in r]
        rows.append(dict(id=s['id'],model=s['model'],story=s['story'],story_sha256=s['story_sha256'],
            window=s['window_seconds'],step=s['requested_step_seconds'],threads=s['cpu_threads'],
            client_profile=s.get('client_profile'),updates=len(updates),audio_seconds=updates[-1]['audio_end_seconds'],
            final_position=updates[-1]['position'],story_words=len(s['words']),backtracks=backwards,
            asr_median_seconds=statistics.median(r['asr_wall_seconds'] for r in updates),
            cut_age_estimated_median_ms=statistics.median(render) if render else None,
            measured_cut_step_median_seconds=statistics.median(b['audio_end_seconds']-a['audio_end_seconds'] for a,b in zip(updates,updates[1:]))))
    out.mkdir(parents=True)
    payload=dict(created_at_utc=datetime.now(timezone.utc).isoformat(),rows=rows,source_sha256=hashes,
        user_confirms_single_reading_without_deliberate_rereading=single_reading_confirmed,
        notice='Tomas diferentes, no mismo audio ni ritmo controlado. Sin nueva inferencia, escucha independiente o referencia temporal humana. Antigüedad estimada del corte no equivale a demora por palabra. No evalúa uso infantil o tablet. Reglas y registros originales intactos.')
    (out/'diagnostico.json').write_text(json.dumps(payload,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    lines=['# Tres pruebas locales de seguimiento · 09/11/2026','',payload['notice'],'',
        'El usuario confirma una sola lectura por toma, sin relecturas deliberadas.' if single_reading_confirmed else 'Intención de relecturas no confirmada por el usuario.','',
        '| Modelo | Ventana / paso s | Hilos | Actualizaciones | ASR mediana s | Antigüedad estimada del corte mediana ms | Retrocesos | Posición final |',
        '|---|---:|---:|---:|---:|---:|---:|---:|']
    for r in rows:
        lines.append(f"| {r['model']} | {r['window']} / {r['step']} | {r['threads']} | {r['updates']} | {r['asr_median_seconds']:.3f} | {r['cut_age_estimated_median_ms']:.1f} | {len(r['backtracks'])} | {r['final_position']}/{r['story_words']} |")
    lines+=['','## Diagnóstico','',
        'Granite presenta revisiones de hipótesis en el borde de las ventanas: elimina una palabra antes reconocida o fusiona/cambia la palabra final. El alineador textual acepta una coincidencia anterior y la guía de la siguiente palabra también retrocede. Los extremos de audio avanzan; eso no acredita que la palabra antigua se haya pronunciado de nuevo, porque las ventanas se solapan y no hay tiempos ASR por palabra.', '',
        'El último caso cuaderno→quaderno deja como última coincidencia exacta «un»: Granite termina en posición 55 en vez de 56. Es el mismo tipo de revisión de reconocimiento que motivó la protección temporal previa, pero esa variante exige marcas ASR por palabra que estos adaptadores no proporcionan. No se inventan tiempos ni se activa un bloqueo general de retrocesos que impediría relecturas auténticas.', '',
        'En estas tomas, Moonshine Small y Tiny completan la posición 56 sin retrocesos y calculan más rápido. Favorece continuar pruebas con ellos, pero no demuestra superioridad general: se han leído audios distintos a velocidades distintas. Un WER mejor en MLS no garantiza mejor comportamiento con micrófono y ventanas cortas en CPU.', '',
        'Se propone mantener Small como referencia provisional de equilibrio y contrastar Tiny cuando prime respuesta/memoria, especialmente con pausas, errores y relecturas reales. Granite se conserva como candidato de comparación. Cualquier nueva protección se debería contrastar mediante reproducción de registros y controles de relectura antes de activarla. No se cambia ningún reconocedor ni regla con este informe.','',
        '## Retrocesos observados','']
    for r in rows:
        for case in r['backtracks']:
            lines += [f"### {r['model']} · corte {case['cut']:.3f} s · {case['previous']} → {case['position']}",'']
            for x in case['context']:lines.append(f"- {x['cut']:.3f} s · posición {x['position']}: {x['hypothesis']}")
            lines.append('')
    (out/'informe.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    for path,digest in hashes.items():
        if hashlib.sha256(Path(path).read_bytes()).hexdigest()!=digest:raise ValueError('Registro modificado durante revisión.')
    print('\n'.join(lines[:13]));print('Informe:',out/'informe.md')


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('files',type=Path,nargs='+')
    p.add_argument('--salida',type=Path,required=True);p.add_argument('--lectura-sin-relecturas-confirmada',action='store_true')
    a=p.parse_args();analyze(a.files,a.salida,a.lectura_sin_relecturas_confirmada)
