"""Contrasta contextos del alineador sobre JSON guardados; no ejecuta ASR."""
import argparse
import hashlib
import json
from pathlib import Path
from scripts.alinear import tokens
from scripts.seguir import locate

ROOT = Path(__file__).resolve().parents[1]


class MarginTracker:
    def __init__(self, story, before=12, allow_global=True):
        self.story, self.before, self.allow_global = story, before, allow_global
        self.position = self.failures = 0
        self.pending = None
        self.previous = []

    def update(self, heard):
        if heard == self.previous:
            return self.position
        self.previous = heard[:]
        evidence = locate(self.story, heard, self.position, before=self.before)
        candidate = evidence['position']
        if candidate is None:
            self.failures += 1
            if self.allow_global and self.failures >= 2:
                recovery = locate(self.story, heard, self.position, global_search=True)['position']
                if recovery is not None:
                    if recovery == self.pending:
                        candidate = recovery
                    self.pending = recovery
                else:
                    self.pending = None
        else:
            self.failures, self.pending = 0, None
        if candidate is not None:
            self.position = candidate
        return self.position


# locate usa índices de inicio base cero y posición base uno: offset 6
# incluye la palabra actual y cinco palabras anteriores (no solo cuatro).
CONFIGS = {'original': (12, True), 'local5_global': (6, True), 'local5_sin_global': (6, False)}


def replay(story, hypotheses, initial=0):
    traces = {}
    for name, config in CONFIGS.items():
        tracker = MarginTracker(story, *config)
        tracker.position = initial
        traces[name] = [tracker.update(tokens(text)) for text in hypotheses]
    return traces


def compare(files, output):
    output = Path(output)
    if output.exists():
        raise ValueError('La salida ya existe; no se sobrescribe.')
    rows = []
    for file in map(Path, files):
        data = json.loads(file.read_text(encoding='utf-8'))
        story_name = data['story']
        if isinstance(story_name, dict):
            story_name = story_name.get('file', story_name.get('path'))
        story_file = ROOT / 'datos/textos' / Path(story_name).name
        story = tokens(story_file.read_text(encoding='utf-8-sig'))
        hypotheses = [r['hypothesis'] for r in data['updates']]
        traces = replay(story, hypotheses)
        recorded = [r['position'] or 0 for r in data['updates']]
        assert traces['original'] == recorded, f'No reproduce original: {file}'
        variants = {}
        for name, positions in traces.items():
            changes = [dict(index=i, original=recorded[i], variant=p,
                            hypothesis=hypotheses[i]) for i, p in enumerate(positions) if p != recorded[i]]
            movements = [p-q for q, p in zip([0]+positions, positions)]
            variants[name] = dict(final=positions[-1], backwards=sum(x<0 for x in movements),
                                  forward_jumps_gt1=sum(x>1 for x in movements), changes=changes)
        rows.append(dict(file=str(file), sha256=hashlib.sha256(file.read_bytes()).hexdigest(),
                         model=data.get('model', data.get('runtime', {}).get('architecture')),
                         updates=len(hypotheses), variants=variants))
    # Una frase exacta fuera de cinco palabras y con texto cambiante:
    # aquí sí existe referencia de destino construida, no una etiqueta inferida del audio.
    synthetic_story = tokens('uno dos tres cuatro cinco seis siete ocho nueve diez once doce trece catorce quince dieciseis diecisiete dieciocho diecinueve veinte')
    controls = []
    for label, initial, phrases, expected in [
        ('avance normal', 10, ['nueve diez once', 'diez once doce'], 12),
        ('relectura corta', 12, ['ocho nueve diez', 'nueve diez once'], 11),
        ('relectura lejana', 20, ['uno dos tres', 'uno dos dos tres', 'uno uno dos tres'], 3),
        ('ocho palabras antiguas sin avance', 12, ['cinco seis siete ocho nueve diez once doce'], 12),
    ]:
        controls.append(dict(case=label, initial=initial, hypotheses=phrases,
                             expected_final=expected, traces=replay(synthetic_story, phrases, initial)))
    payload = dict(status='replay_only_no_new_inference', configs=CONFIGS, sessions=rows, controls=controls,
                   notice='Cambios de posición no equivalen a mejoras sin referencia humana. Mismos textos ASR: no mide aceleración del modelo ni nueva latencia. El cuento no se introduce en el ASR.')
    output.mkdir(parents=True)
    (output/'comparacion.json').write_text(json.dumps(payload, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    md = ['# Margen de cinco palabras · reproducción', '', payload['notice'], '',
          'Se aísla buscar desde cinco palabras anteriores a la posición aceptada (offset before=6: incluye también la posición actual), en lugar del offset original before=12. Por separado se desactiva la recuperación global. Se mantienen 24 palabras por delante, hipótesis de ocho palabras y umbrales originales.', '',
          '| Sesión | Versión | Final | Retrocesos | Avances >1 | Cortes distintos |',
          '|---|---|---:|---:|---:|---:|']
    for r in rows:
        for name, v in r['variants'].items():
            md.append(f"| {Path(r['file']).name} | {name} | {v['final']} | {v['backwards']} | {v['forward_jumps_gt1']} | {len(v['changes'])} |")
    md += ['', '## Controles construidos', '', 'Son propuestas textuales, no grabaciones ni segundos de demora.']
    for c in controls:
        md += ['', f"- {c['case']}: destino construido {c['expected_final']}; {c['traces']}."]
    md += ['', '## Interpretación', '', 'Un margen de cinco palabras no prohíbe retroceder dentro de ese margen ni garantiza eliminar oscilaciones. Quitar la recuperación global sí impide resolver ciertos regresos lejanos; el resaltado no demuestra que nunca ocurrirán. Acortar el cuento buscado no acelera por sí mismo la inferencia acústica. Un avance de varias palabras puede ser la llegada de una frase reconocida; no demuestra omisión lectora ni pérdida de todas esas palabras.', '', 'Ninguna de estas variantes queda activada en la app.']
    (output/'informe.md').write_text('\n'.join(md)+'\n', encoding='utf-8')
    print('\n'.join(md[:8]))
    for r in rows:
        print(Path(r['file']).name, {n:dict(final=v['final'],backs=v['backwards'],changes=len(v['changes'])) for n,v in r['variants'].items()})
    print('Controles:', controls)
    print('Informe:', output/'informe.md')


if __name__ == '__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('files', nargs='+', type=Path)
    p.add_argument('--salida', required=True, type=Path)
    a=p.parse_args()
    compare(a.files, a.salida)
