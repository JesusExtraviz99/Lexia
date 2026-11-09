"""Prototipo de micrófono en localhost: ASR CPU offline, sin servidor remoto."""
import argparse
from datetime import datetime,timezone
import gc
import hashlib
from http.server import BaseHTTPRequestHandler,ThreadingHTTPServer
import json
import math
from pathlib import Path
import secrets
import threading
import time
from urllib.parse import urlsplit,parse_qs

from scripts.alinear import TOKEN,tokens
from scripts.seguir import Tracker
from scripts.archivos import write_text_atomic

ROOT=Path(__file__).resolve().parents[1]
MODELS={'granite_turboctc':'Granite TurboCTC','moonshine_small_es':'Moonshine Small español',
        'moonshine_tiny_es':'Moonshine Tiny español','parakeet':'Parakeet TDT','canary_v2':'Canary v2'}


def pcm_window(raw,rate,end,window=8):
    import numpy as np
    from scipy.signal import resample_poly
    if rate not in (16000,22050,24000,32000,44100,48000,96000):raise ValueError('Frecuencia no admitida.')
    if len(raw)%4 or not raw or len(raw)>rate*window*4:raise ValueError('Ventana PCM incorrecta.')
    samples=np.frombuffer(raw,dtype='<f4').copy()
    if not np.isfinite(samples).all() or np.abs(samples).max()>1.01:raise ValueError('PCM inválido.')
    if not math.isfinite(end) or end<len(samples)/rate or end>600:raise ValueError('Tiempo de captura inválido.')
    start=end-len(samples)/rate
    if rate!=16000:
        factor=math.gcd(rate,16000)
        samples=resample_poly(samples,16000//factor,rate//factor).astype('float32')
    return samples,start


class LocalEngine:
    def __init__(self,root=ROOT,infer=None,threads=4):
        self.root=Path(root);self.lock=threading.Lock();self.infer=infer
        self.threads=threads
        self.model='prueba' if infer else None;self.state='ready' if infer else 'empty'
        self.error=None;self.sessions={};self.load_seconds=0;self.max_rss=0
        self.process=None
        self.stories={p.name:p.read_text(encoding='utf-8-sig') for p in (self.root/'datos/textos').glob('lectura_*.txt')}

    def status(self):
        return dict(state=self.state,model=self.model,error=self.error,load_seconds=self.load_seconds,
                    rss_mib=(self.process.memory_info().rss/1048576 if self.process else None),
                    device='CPU del ordenador',external_audio_services=False)

    def prepare(self,key):
        if key not in MODELS:raise ValueError('Modelo no admitido.')
        if not self.lock.acquire(blocking=False):raise ValueError('El motor está ocupado.')
        if any(not s['finished'] for s in self.sessions.values()):
            self.lock.release();raise ValueError('Finaliza la lectura antes de cambiar de modelo.')
        self.state='loading';self.error=None
        def load():
            try:
                import os
                os.environ.update(HF_HUB_OFFLINE='1',TRANSFORMERS_OFFLINE='1',CUDA_VISIBLE_DEVICES='',TOKENIZERS_PARALLELISM='false')
                import psutil
                from scripts import ampliacion_motores,asr_motores_externos
                adapter=asr_motores_externos if key=='parakeet' else ampliacion_motores
                self.infer=None;gc.collect()
                folder=self.root/'modelos'/adapter.SPECS[key]['folder']
                def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
                started=time.perf_counter()
                identity=adapter.check(folder,key,sha)
                self.infer,self.torch=adapter.load(key,folder,None,self.threads)
                self.identity=identity;self.parameters=adapter.parameters(key);self.load_seconds=time.perf_counter()-started
                self.process=psutil.Process();self.model=key;self.state='ready'
            except Exception as exc:
                self.infer=None;self.state='error';self.error=str(exc)
            finally:self.lock.release()
        threading.Thread(target=load,daemon=True).start()

    def start(self,story,source='microfono_navegador',window=8,step=2,client_profile=1,guide_words=1):
        with self.lock:
            if source not in ('microfono_navegador','diagnostico_archivo_publico'):raise ValueError('Origen no admitido.')
            if type(window) not in (int,float) or window not in (4,6,8):raise ValueError('Ventana no admitida.')
            if type(step) not in (int,float) or step not in (.125,.25,.5,1,2):raise ValueError('Paso no admitido.')
            if type(client_profile)!=int or client_profile not in (1,2):raise ValueError('Cliente no admitido.')
            if type(guide_words)!=int or guide_words not in (1,2):raise ValueError('Guía visual no admitida.')
            if self.state!='ready':raise ValueError('Espera a que el modelo esté preparado.')
            if story not in self.stories:raise ValueError('Texto no admitido.')
            if any(not s['finished'] for s in self.sessions.values()):raise ValueError('Ya hay una lectura abierta; finalízala antes de iniciar otra.')
            ident=secrets.token_hex(12);text=self.stories[story]
            s=dict(id=ident,created_at_utc=datetime.now(timezone.utc).isoformat(),model=self.model,
                story=story,story_sha256=hashlib.sha256(text.encode()).hexdigest(),
                words=tokens(text),tracker=Tracker(tokens(text)),last_words=[],last_end=0,updates=[],finished=False,
                runtime=self.status(),model_identity=getattr(self,'identity',None),
                asr_parameters=getattr(self,'parameters',None),cpu_threads=self.threads,
                client_profile=client_profile,capture_block_samples=512 if client_profile==2 else 2048,
                visual_guide=dict(group_size=guide_words,policy='sliding_next_words' if guide_words==2 else 'next_word'),
                render_reporting='piggyback' if client_profile==2 else 'separate_post',
                capture_settings=None,source=source,audio_saved_by_server=False,
                rule='Tracker original textual compartido. Sin marcas temporales de palabra inventadas.',
                window_seconds=window,requested_step_seconds=step,
                notice='Actualización real por ventanas; sin streaming nativo. No mide error de posición sin referencia humana. Antigüedad del corte estimada por reloj del navegador; no latencia acústica física.')
            self.sessions[ident]=s;self.save(s)
            return dict(id=ident,words=s['words'],window_seconds=window,requested_step_seconds=step,guide_words=guide_words)

    def save(self,s):
        folder=self.root/'resultados/directo_local';folder.mkdir(parents=True,exist_ok=True)
        serial={k:v for k,v in s.items() if k!='tracker'}
        write_text_atomic(folder/(s['id']+'.json'),json.dumps(serial,ensure_ascii=False,indent=2)+'\n')

    def update(self,ident,raw,rate,end,render=None):
        if not self.lock.acquire(blocking=False):raise ValueError('Motor ocupado: no se acumulan ventanas.')
        try:
            if ident not in self.sessions:raise ValueError('Sesión desconocida.')
            s=self.sessions[ident]
            if s['finished'] or end<=s['last_end']:raise ValueError('Corte antiguo o sesión cerrada.')
            if self.state!='ready' or s['model']!=self.model:raise ValueError('Modelo no disponible.')
            signal,start=pcm_window(raw,rate,end,s['window_seconds'])
            if render is not None:self.apply_render(s,render)
            began=time.perf_counter();cpu=time.process_time()
            native=self.infer(signal)
            seconds=time.perf_counter()-began;cpu_seconds=time.process_time()-cpu
            alignment_start=time.perf_counter()
            heard=tokens(native['hypothesis'])
            if heard==s['last_words']:
                position=s['tracker'].position
                found=dict(previous_position=position,position=position or None,
                    word=s['words'][position-1] if position else None,movement=0,
                    mode='hipotesis_sin_cambios',evidence={})
            else:found=s['tracker'].update(heard)
            s['last_words']=heard
            record=dict(index=len(s['updates']),audio_start_seconds=start,audio_end_seconds=end,
                unprocessed_audio_gap_seconds=max(0,start-s['last_end']),
                native_sample_rate=rate,hypothesis=native['hypothesis'],**found,
                asr_wall_seconds=seconds,asr_cpu_seconds=cpu_seconds,
                align_seconds=time.perf_counter()-alignment_start,
                generation_cap_reached=native.get('generation_cap_reached'),
                rms=float((signal.astype('float64')**2).mean()**.5),
                rss_after_inference_mib=(self.process.memory_info().rss/1048576 if self.process else None))
            s['updates'].append(record);s['last_end']=end;self.save(s)
            return record
        finally:self.lock.release()

    @staticmethod
    def apply_render(s,p):
        if not isinstance(p,dict) or p.get('id')!=s['id'] or p.get('kind')!='render':raise ValueError('Informe de navegador inválido.')
        idx=p.get('index')
        if type(idx)!=int or not 0<=idx<len(s['updates']):raise ValueError('Actualización desconocida.')
        values={}
        for key in ('request_roundtrip_ms','estimated_cut_age_at_render_ms'):
            value=p.get(key)
            if type(value) not in (float,int) or not math.isfinite(value) or abs(value)>900000:raise ValueError('Tiempo inválido.')
            values[key]=value
        s['updates'][idx]['browser']=values

    def event(self,p):
        with self.lock:
            s=self.sessions.get(p.get('id'))
            if s is None:raise ValueError('Sesión desconocida.')
            if p['kind']=='render':
                self.apply_render(s,p)
            elif p['kind']=='capture':
                settings=p.get('settings',{})
                s['capture_settings']={k:settings.get(k) for k in ('sampleRate','channelCount','echoCancellation','noiseSuppression','autoGainControl')}
            elif p['kind']=='finish':
                if p.get('render') is not None:self.apply_render(s,p['render'])
                s['finished']=True;s['finished_at_utc']=datetime.now(timezone.utc).isoformat()
            else:raise ValueError('Evento no admitido.')
            self.save(s);return dict(ok=True,file='resultados/directo_local/'+s['id']+'.json')


def make_handler(engine,port,token):
    assets=ROOT/'herramientas/directo_local'
    hosts={'127.0.0.1:'+str(port),'localhost:'+str(port)}
    class Handler(BaseHTTPRequestHandler):
        def log_message(self,*args):pass
        def reply(self,data,status=200,mime='application/json; charset=utf-8'):
            if not isinstance(data,bytes):data=json.dumps(data,ensure_ascii=False).encode()
            self.send_response(status);self.send_header('Content-Type',mime)
            self.send_header('Content-Length',str(len(data)));self.send_header('Cache-Control','no-store')
            self.send_header('X-Content-Type-Options','nosniff')
            self.send_header('Content-Security-Policy',"default-src 'self'; connect-src 'self'; script-src 'self'; style-src 'self'; media-src 'self' blob:; object-src 'none'; frame-ancestors 'none'")
            self.end_headers();self.wfile.write(data)
        def valid_host(self):return self.headers.get('Host') in hosts
        def do_GET(self):
            if not self.valid_host():return self.reply({'error':'Host no permitido'},403)
            path=urlsplit(self.path).path
            if path=='/api/config':return self.reply(dict(token=token,models=MODELS,stories=[dict(id=k,text=v) for k,v in engine.stories.items()],runtime=engine.status()))
            if path=='/api/status':return self.reply(engine.status())
            file={'/':'index.html','/app.js':'app.js','/style.css':'style.css','/capture.js':'capture.js'}.get(path)
            if not file:return self.reply({'error':'No encontrado'},404)
            mime='text/html; charset=utf-8' if file.endswith('.html') else 'text/css' if file.endswith('.css') else 'application/javascript'
            self.reply((assets/file).read_bytes(),mime=mime)
        def do_POST(self):
            if not self.valid_host() or self.headers.get('X-Lexia-Token')!=token:return self.reply({'error':'Petición no autorizada'},403)
            origin=self.headers.get('Origin')
            if origin and origin not in {'http://'+h for h in hosts}:return self.reply({'error':'Origen no permitido'},403)
            try:
                length=int(self.headers.get('Content-Length','0'))
                if not 0<length<=4_000_000:raise ValueError('Tamaño no permitido.')
                data=self.rfile.read(length);parsed=urlsplit(self.path)
                if parsed.path=='/api/audio':
                    q=parse_qs(parsed.query)
                    header=self.headers.get('X-Lexia-Render')
                    if header and len(header)>1000:raise ValueError('Informe de navegador demasiado grande.')
                    render=json.loads(header) if header else None
                    result=engine.update(q['id'][0],data,int(q['rate'][0]),float(q['end'][0]),render=render)
                else:
                    p=json.loads(data)
                    if parsed.path=='/api/prepare':engine.prepare(p['model']);result={'ok':True}
                    elif parsed.path=='/api/start':result=engine.start(p['story'],p.get('source','microfono_navegador'),p.get('window',8),p.get('step',2),p.get('client_profile',1),p.get('guide_words',1))
                    elif parsed.path=='/api/event':result=engine.event(p)
                    else:return self.reply({'error':'No encontrado'},404)
                self.reply(result)
            except (ValueError,KeyError,TypeError) as exc:self.reply({'error':str(exc)},400)
            except Exception as exc:self.reply({'error':str(exc)},500)
    return Handler


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--puerto',type=int,default=8790)
    p.add_argument('--hilos',type=int,choices=[1,2,4,8],default=4)
    p.add_argument('--modelo',choices=MODELS,default='granite_turboctc');a=p.parse_args()
    if not 1024<=a.puerto<=65535:p.error('Puerto fuera de rango.')
    engine=LocalEngine(threads=a.hilos);server=ThreadingHTTPServer(('127.0.0.1',a.puerto),make_handler(engine,a.puerto,secrets.token_urlsafe(32)))
    engine.prepare(a.modelo)
    print(f'Lexia local: http://127.0.0.1:{a.puerto}/ | CPU, sin servicios remotos. Ctrl+C detiene la web.',flush=True)
    try:server.serve_forever()
    except KeyboardInterrupt:pass
    finally:server.server_close()


if __name__=='__main__':main()
