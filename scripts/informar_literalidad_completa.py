"""Contrasta la salida completa con el recorte humano revisado, sin inferencias."""
import argparse
import json
from pathlib import Path

from scripts.archivos import write_text_atomic
from scripts.catalogo import ROOT
from scripts.comparar_literalidad import digest


def report(folder):
    manifest=json.loads((folder/'manifest.json').read_text(encoding='utf-8'))
    prior=ROOT/manifest['source_pilot']
    if any(digest(prior/name)!=value for name,value in manifest['prior_hashes'].items()):
        raise ValueError('El piloto previo ha cambiado.')
    outputs={engine:json.loads((folder/(engine+'.json')).read_text(encoding='utf-8')) for engine in ['baseline','candidato']}
    for result in outputs.values():
        if result.get('status')!='completo' or result['manifest_sha256']!=digest(folder/'manifest.json'):
            raise ValueError('Ejecución incompleta o manifiesto cambiado.')
    previous=json.loads((prior/'candidato.json').read_text(encoding='utf-8'))
    old=next(row['raw_text'] for row in previous['runs'] if row['id']=='medio_1')
    new=outputs['candidato']['runs'][0]['raw_text']
    review=ROOT/'datos/anotaciones/lectura_02_piloto_literal_revision.json'
    human=json.loads(review.read_text(encoding='utf-8'))
    if human['candidate_output_sha256']!=digest(prior/'candidato.json'):
        raise ValueError('La revisión humana no corresponde a esa salida previa.')
    lines=['# Audio completo frente al recorte de 8 segundos','',
        '## Hallazgo en el tramo revisado','',
        'El lector confirmó que la última aparición de «el barco rojo» del recorte 16–24 s no se oye: inserción del ASR. Con la entrada completa, esa continuación añadida ya no figura en el texto: se escribe «el el barco el barco flotaba…». Se conserva una aparición legítima de «barco rojo» antes de ese tramo. Es una comparación de salidas, no una validación humana nueva de todos los intentos.','',
        '**Candidato, recorte 16–24 s:** '+old,'',
        '**Candidato, grabación completa:** '+new,'',
        'El candidato mantiene formas parciales y repeticiones que el motor habitual simplifica, pero su fidelidad por evento sigue pendiente de escucha. No se calcula recuperación, precisión/F1 o número real de trabadas a partir del texto generado.','',
        '## Qué ha cambiado y qué no','',manifest['notice'],'',
        'Se comprueba igualdad exacta entre los arrays de los cuatro recortes previos y sus intervalos en la grabación completa. El cuento y las notas no se entregan al modelo. La inferencia larga usa 0–30, 26–56 y 52–60 s (registrados en native_result.chunks), con continuación generada y ensamblado. El tramo 16–24 está dentro del primer bloque de 30 s: ahora dispone de audio anterior y también de los segundos 24–30 que no tenía el recorte. No se atribuye el cambio únicamente al contexto anterior ni a la estrategia de continuación. Es una pasada por motor y configuración; no demuestra que la inserción desaparezca siempre.','',
        '## Recursos del audio completo (60 s de entrada)','',
        '| Motor | Inferencia (s) | CPU del tramo de inferencia (s) | RTF inferencia | Carga (s) | Pico RAM proceso (MiB) |',
        '|---|---:|---:|---:|---:|---:|']
    duration=manifest['samples'][0]['end']
    for name,data in outputs.items():
        run=data['runs'][0]
        peak=data['resources']['final_memory']['process_lifetime_peak_working_set_bytes']/1048576
        lines.append(f"| {name} | {run['processing_seconds']:.2f} | {run['cpu_seconds']:.2f} | {run['processing_seconds']/duration:.3f} | {data['model_load_seconds']:.2f} | {peak:.2f} |")
    lines+=['',
        'RTF = tiempo de inferencia / duración de entrada, sin carga. Incluye el silencio final; no es RTF sobre habla ni latencia en directo. CPU acumulada puede superar tiempo de pared por los cuatro hilos. Pico RAM del proceso completo, incluida carga. CPU/RAM y muestras de GPU global en los JSON; motores ejecutados en CPU, sin energía propia del ASR ni medición móvil. Backends/precisiones distintos; no atribuir todo el coste al modelo. No comparar directamente el tiempo de este audio de 60 s con la suma de siete recortes de 56 s como si fuesen el mismo trabajo.','',
        'Persisten avisos del cargador sobre encoder_blank_head y opciones de atención/generación. En esta ejecución larga también se notifican max_new_tokens frente a max_length y limpieza de tokenización BPE. Se conservan parámetros efectivos solicitados y versiones; no se han parcheado paquetes. Marcas automáticas de palabra sin validar: no se usan como prueba de que una sílaba esté o no en el audio.','',
        '## Revisión compartida','',
        'Abrir http://127.0.0.1:8776/. El selector contiene la grabación completa y los cuatro recortes anteriores, con sus textos originales. Escuchar especialmente 16–30 s del audio completo y compararlo con Intermedio 1; después comprobar intentos del inicio, intermedio y final. Las referencias humanas previas conservan su alcance de muestras. Los resultados completos se publican como exploratorios y pendientes de revisión literal exhaustiva, sin activar el motor en el seguidor.','',
        'Comandos de comprobación (sin inferencia):','',
        '```powershell',
        f'.\\.venv\\Scripts\\python.exe -m scripts.verificar_piloto_literal {folder.relative_to(ROOT).as_posix()}',
        f'.\\.venv\\Scripts\\python.exe -m scripts.informar_literalidad_completa {folder.relative_to(ROOT).as_posix()}',
        f'.\\.venv\\Scripts\\python.exe -m scripts.ver_piloto_literal {folder.relative_to(ROOT).as_posix()} --puerto 8776',
        '```','',
        f'Referencia puntual del lector: {review.relative_to(ROOT).as_posix()} (SHA256 {digest(review)}).',
        'Entradas, modelo, salidas, código ejecutado y piloto previo: huellas en manifest.json e integridad.json.']
    complete_review=ROOT/'datos/anotaciones/lectura_02_literal_completa_revision.json'
    if complete_review.exists():
        reviewed=json.loads(complete_review.read_text(encoding='utf-8'))
        if reviewed['experiment_folder']==folder.relative_to(ROOT).as_posix():
            if (reviewed['candidate_output_sha256']!=digest(folder/'candidato.json')
                    or reviewed['manifest_sha256']!=digest(folder/'manifest.json')):
                raise ValueError('La revisión completa no corresponde a estas fuentes.')
            lines+=['','## Confirmación posterior del lector','',
                'Tras escuchar la grabación completa, el lector valora el resto como bastante fiel y señala una omisión: se oye «regres- re- regresaron», frente a «regres- regresaron» del candidato. Falta el intento parcial «re-». Es un episodio conservado parcialmente: tres intentos (dos parciales y palabra completa) frente a dos en la salida, sin perder la palabra pretendida.','',
                'Esta revisión cualitativa y la corrección puntual no son un inventario temporal exhaustivo ni una revisión independiente. No se calcula precisión/F1 o porcentaje global. La evaluación debe distinguir localizar un episodio de contar sus intentos. No se cambia el texto bruto del ASR ni se ejecuta una nueva inferencia.','',
                f'Referencia: {complete_review.relative_to(ROOT).as_posix()} (SHA256 {digest(complete_review)}).']
    write_text_atomic(folder/'comparacion_contexto.md','\n'.join(lines)+'\n')
    print(folder/'comparacion_contexto.md')


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('folder',type=Path)
    report(parser.parse_args().folder.resolve())


if __name__=='__main__':
    main()
