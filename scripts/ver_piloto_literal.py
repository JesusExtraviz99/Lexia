"""Visor de escucha del piloto literal, sin inferencias ni escritura de referencias."""
import argparse
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
from pathlib import Path

from scripts.catalogo import ROOT
from scripts.comparar_literalidad import digest

UI=ROOT/'herramientas/piloto_literal'


def load(folder):
    manifest_path=folder/'manifest.json'
    manifest=json.loads(manifest_path.read_text(encoding='utf-8'))
    outputs={e:json.loads((folder/(e+'.json')).read_text(encoding='utf-8')) for e in ['baseline','candidato']}
    if any(o.get('status')!='completo' or o['manifest_sha256']!=digest(manifest_path) for o in outputs.values()):
        raise ValueError('Resultados incompletos o manifiesto cambiado.')
    clips={};samples=[]
    for item in manifest['samples']:
        path=(ROOT/item['listen_file']).resolve()
        if not path.is_relative_to((ROOT/'.descartados/literalidad').resolve()) or digest(path)!=item['listen_sha256']:
            raise ValueError('Recorte no permitido o modificado.')
        clips[item['id']]=path
        samples.append(dict(id=item['id'],kind=item['kind'],start=item['start'],end=item['end'],note=item['human_note'],
                            clip='/clip/'+item['id'],outputs={e:next(r for r in o['runs'] if r['id']==item['id']) for e,o in outputs.items()}))
    metrics={e:dict(load=o['model_load_seconds'],seconds=sum(r['processing_seconds'] for r in o['runs']),
                    ram_mib=o['resources']['final_memory'].get('process_lifetime_peak_working_set_bytes',0)/1048576,
                    backend=o['backend'],precision=o['compute_type']) for e,o in outputs.items()}
    if manifest.get('source_pilot'):
        prior=(ROOT/manifest['source_pilot']).resolve()
        if not prior.is_relative_to((ROOT/'resultados/literalidad').resolve()):
            raise ValueError('Piloto previo fuera de la carpeta permitida.')
        if any(digest(prior/name)!=value for name,value in manifest['prior_hashes'].items()):
            raise ValueError('El piloto previo ha cambiado.')
        previous,previous_clips=load(prior)
        for sample in previous['samples']:
            if sample['kind']=='trabadas':
                samples.append(sample)
                clips[sample['id']]=previous_clips[sample['id']]
    duration=sum(s['end']-s['start'] for s in manifest['samples'])
    return dict(samples=samples,metrics=metrics,notice=manifest['notice'],input_seconds=duration,
                comparison_complete=bool(manifest.get('source_pilot'))),clips


def make_handler(payload,clips):
    class Handler(BaseHTTPRequestHandler):
        def log_message(self,*_):
            pass
        def do_GET(self):
            if self.headers.get('Host')!=f'127.0.0.1:{self.server.server_port}':
                self.send_error(403);return
            if self.path=='/data':
                body=json.dumps(payload,ensure_ascii=False).encode('utf-8');mime='application/json; charset=utf-8'
            elif self.path.startswith('/clip/') and self.path[6:] in clips:
                body=clips[self.path[6:]].read_bytes();mime='audio/wav'
            elif self.path in ['/', '/app.js','/style.css']:
                filename,mime={'/':('index.html','text/html; charset=utf-8'),'/app.js':('app.js','text/javascript; charset=utf-8'),'/style.css':('style.css','text/css; charset=utf-8')}[self.path]
                path=UI/filename if filename!='style.css' else ROOT/'herramientas/revision_trabadas/style.css'
                body=path.read_bytes()
            else:
                self.send_error(404);return
            self.send_response(200)
            self.send_header('Content-Type',mime);self.send_header('Content-Length',str(len(body)))
            self.send_header('Cache-Control','no-store');self.send_header('X-Content-Type-Options','nosniff')
            self.send_header('Content-Security-Policy',"default-src 'self'; script-src 'self'; style-src 'self'; media-src 'self'; connect-src 'self'; object-src 'none'; frame-ancestors 'none'")
            self.end_headers()
            try:self.wfile.write(body)
            except (BrokenPipeError,ConnectionResetError,ConnectionAbortedError):pass
    return Handler


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('folder',type=Path)
    parser.add_argument('--puerto',type=int,default=8775)
    args=parser.parse_args()
    payload,clips=load(args.folder.resolve())
    server=ThreadingHTTPServer(('127.0.0.1',args.puerto),make_handler(payload,clips))
    print(f'Piloto listo: http://127.0.0.1:{server.server_port}/',flush=True)
    try:server.serve_forever()
    except KeyboardInterrupt:pass
    finally:server.server_close()


if __name__=='__main__':main()
