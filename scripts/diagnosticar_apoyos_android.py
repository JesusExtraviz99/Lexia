"""Ensayo de apoyo final y recuperación por sufijo exacto; solo JSON, sin ASR."""
import argparse
import hashlib
import json
from pathlib import Path
from scripts.alinear import tokens, normalize
from scripts.comparar_margen_directo import MarginTracker

ROOT=Path(__file__).resolve().parents[1]


class SupportedTracker(MarginTracker):
    def __init__(self, story, before=12, suffix_recovery=False):
        super().__init__(story,before,True)
        self.suffix_recovery=suffix_recovery
        self.normalized=[normalize(w) for w in story]
        self.event=None

    def update_recent(self, hypothesis, current_line):
        heard=tokens(hypothesis)
        self.event=None
        if heard==self.previous:
            return self.position
        old=self.position
        failures,pending=self.failures,self.pending
        candidate=super().update(heard)
        normalized=[normalize(w) for w in heard]
        if candidate>old:
            endpoint_matches=bool(normalized) and normalized[-1]==self.normalized[candidate-1]
            pair_matches=(len(normalized)>=2 and candidate>=2 and
                          normalized[-2:]==self.normalized[candidate-2:candidate])
            if not endpoint_matches or (candidate-old>1 and not pair_matches):
                self.position=old
                self.failures,self.pending=failures,pending
                self.event=dict(kind='advance_rejected_missing_terminal_support',candidate=candidate)
        if self.suffix_recovery and self.position==old:
            recent=[normalize(w) for w in tokens(current_line)]
            for size in range(min(8,len(recent)),2,-1):
                suffix=recent[-size:]
                if not any(len(word)>=5 for word in suffix):
                    continue
                endpoints=[start+size for start in range(len(self.normalized)-size+1)
                           if self.normalized[start:start+size]==suffix]
                if len(endpoints)==1 and old<endpoints[0]<=old+24:
                    self.position=endpoints[0]
                    self.failures,self.pending=0,None
                    self.event=dict(kind='recent_exact_unique_suffix',words=suffix,candidate=self.position)
                    break
        return self.position


def evaluate(files,output):
    output=Path(output)
    if output.exists():raise ValueError('La salida existe; no se sobrescribe.')
    rows=[]
    for file in map(Path,files):
        data=json.loads(file.read_text(encoding='utf-8'))
        story=tokens((ROOT/'datos/textos'/data['story']).read_text(encoding='utf-8-sig'))
        offset=data.get('tracker_local_search_offset_words',12)
        if offset not in (6,12):raise ValueError('Perfil desconocido')
        baseline=MarginTracker(story,offset)
        strict=SupportedTracker(story,offset)
        recent=SupportedTracker(story,offset,True)
        trace=[]
        for i,r in enumerate(data['updates']):
            old_baseline=baseline.position
            expected=baseline.update(tokens(r['hypothesis']))
            assert expected==r['position'] and expected-old_baseline==r['movement'],(file,i)
            current=r.get('asr_current_line',r['hypothesis'])
            a=strict.update_recent(r['hypothesis'],current)
            b=recent.update_recent(r['hypothesis'],current)
            trace.append(dict(index=i,callback_seconds=r['callback_elapsed_ms']/1000,
                              original=expected,terminal_support=a,terminal_and_recent=b,
                              terminal_event=strict.event,recent_event=recent.event,
                              current_line=current,hypothesis_tail=tokens(r['hypothesis'])[-8:]))
        variants={}
        for name in ('original','terminal_support','terminal_and_recent'):
            positions=[r[name] for r in trace]
            variants[name]=dict(final=positions[-1],backwards=sum(p<q for q,p in zip([0]+positions,positions)),
                                changes=sum(r[name]!=r['original'] for r in trace),
                                first_final_callback_seconds=next((r['callback_seconds'] for r in trace if r[name]==len(story)),None))
        rows.append(dict(file=file.name,sha256=hashlib.sha256(file.read_bytes()).hexdigest(),
                         app_version=data.get('app_version','0.1'),architecture=data['runtime']['architecture'],
                         native_interval=data.get('native_transcription_interval_requested_seconds','not_explicit'),
                         guide=data.get('guide_policy','fixed_pairs'),variants=variants,trace=trace))
    output.mkdir(parents=True)
    notice='Reproducción de las mismas hipótesis. No corrige el ASR, no prueba que una frase se pronunciara ni mide latencia acústica nueva. Las reglas no modifican las tomas guardadas; se ofrecen como opción experimental, desactivada por defecto, en APK0.4. Un sufijo inventado que coincida con el cuento todavía puede engañarlas.'
    (output/'comparacion.json').write_text(json.dumps(dict(notice=notice,sessions=rows),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    text=['# Apoyo de avances y texto reciente · experimento', '', notice,'',
          'Se conserva el ASR y el margen de cada sesión. Variante1: para avanzar, la última palabra propuesta debe coincidir con el destino; un avance de más de una posición requiere además las dos últimas palabras consecutivas exactas. Variante2 añade una salida del atasco: sufijo reciente de al menos tres palabras consecutivas exactas, una de al menos cinco caracteres, aparición única en el cuento y destino dentro de las 24 posiciones siguientes. No cambia retrocesos, ni acepta una palabra aislada, ni limita artificialmente todo avance a una posición.', '',
          '| Registro | Versión del seguidor | Final | Retrocesos | Callbacks distintos | Primer callback en final (s) |',
          '|---|---|---:|---:|---:|---:|']
    for row in rows:
        for name,v in row['variants'].items():
            text.append(f"| {row['file']} | {name} | {v['final']} | {v['backwards']} | {v['changes']} | {v['first_final_callback_seconds']} |")
    text+=['','## Límites y decisión','','El apoyo terminal evita ciertos saltos basados en coincidencias interiores antiguas. Puede retrasar avances correctos cuando el ASR añade una terminación errónea. La recuperación exacta por texto reciente puede superar contaminación anterior, pero es más permisiva que el alineamiento completo y requiere controles negativos. Las dos variantes están diseñadas a partir de estos mismos registros: son desarrollo, no validación independiente. No se elige por llegar al final antes.','',
           'Mantener 0,125 y 0,25 s como rango de futuras lecturas. La nueva toma usa Small, 0,125 s y contexto original, no el margen de cinco. Su diferencia respecto a otras tomas no prueba que la cadencia cause los errores: cambian lectura, segmentación y condiciones. No hay aquí escucha independiente ni referencia humana por palabra.']
    (output/'informe.md').write_text('\n'.join(text)+'\n',encoding='utf-8')
    for row in rows:print(row['file'],row['variants'])
    print('Informe:',output/'informe.md')


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('files',nargs='+',type=Path)
    p.add_argument('--salida',required=True,type=Path)
    args=p.parse_args();evaluate(args.files,args.salida)
