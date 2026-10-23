# Audio completo frente al recorte de 8 segundos

## Hallazgo en el tramo revisado

El lector confirmó que la última aparición de «el barco rojo» del recorte 16–24 s no se oye: inserción del ASR. Con la entrada completa, esa continuación añadida ya no figura en el texto: se escribe «el el barco el barco flotaba…». Se conserva una aparición legítima de «barco rojo» antes de ese tramo. Es una comparación de salidas, no una validación humana nueva de todos los intentos.

**Candidato, recorte 16–24 s:** Descu- descubrió un pe- pequeño barco rojo, el el barco, el barco rojo.

**Candidato, grabación completa:** U- u- una tarde lu- lucia pa- paseaba por el par- parque con su abuelo junto a una un- una fuente des- des- descu- descubrió un pe- pequeño barco rojo, el el barco el barco flotaba des- despacio en entre las hojas. Lu- Lucia buscó una r- rama para acercarlo a la ori- o- orilla. Su abuelo la la ayudó y y juntos sa- sacaron el barco del del agua. Des- después regres- regresaron a casa y lo y lo colocaron sobre una estantería.

El candidato mantiene formas parciales y repeticiones que el motor habitual simplifica, pero su fidelidad por evento sigue pendiente de escucha. No se calcula recuperación, precisión/F1 o número real de trabadas a partir del texto generado.

## Qué ha cambiado y qué no

Mismo WAV completo para ambos motores, sin cuento ni notas como prompt; una pasada offline. Se conservan modelo y ajustes del piloto corto. Para entradas mayores de 30 s el candidato activa su estrategia interna continuation (ventanas 30 s, paso 26 s y contexto generado). No escucha toda la grabación en una única ventana. Cambian duración y procesamiento interno: no se aísla una causa del error ni se mide seguimiento en directo. Comparar el tramo revisado, sin convertir diferencias de texto en métricas humanas.

Se comprueba igualdad exacta entre los arrays de los cuatro recortes previos y sus intervalos en la grabación completa. El cuento y las notas no se entregan al modelo. La inferencia larga usa 0–30, 26–56 y 52–60 s (registrados en native_result.chunks), con continuación generada y ensamblado. El tramo 16–24 está dentro del primer bloque de 30 s: ahora dispone de audio anterior y también de los segundos 24–30 que no tenía el recorte. No se atribuye el cambio únicamente al contexto anterior ni a la estrategia de continuación. Es una pasada por motor y configuración; no demuestra que la inserción desaparezca siempre.

## Recursos del audio completo (60 s de entrada)

| Motor | Inferencia (s) | CPU del tramo de inferencia (s) | RTF inferencia | Carga (s) | Pico RAM proceso (MiB) |
|---|---:|---:|---:|---:|---:|
| baseline | 5.23 | 21.11 | 0.087 | 1.00 | 696.68 |
| candidato | 15.50 | 62.83 | 0.258 | 7.44 | 4417.32 |

RTF = tiempo de inferencia / duración de entrada, sin carga. Incluye el silencio final; no es RTF sobre habla ni latencia en directo. CPU acumulada puede superar tiempo de pared por los cuatro hilos. Pico RAM del proceso completo, incluida carga. CPU/RAM y muestras de GPU global en los JSON; motores ejecutados en CPU, sin energía propia del ASR ni medición móvil. Backends/precisiones distintos; no atribuir todo el coste al modelo. No comparar directamente el tiempo de este audio de 60 s con la suma de siete recortes de 56 s como si fuesen el mismo trabajo.

Persisten avisos del cargador sobre encoder_blank_head y opciones de atención/generación. En esta ejecución larga también se notifican max_new_tokens frente a max_length y limpieza de tokenización BPE. Se conservan parámetros efectivos solicitados y versiones; no se han parcheado paquetes. Marcas automáticas de palabra sin validar: no se usan como prueba de que una sílaba esté o no en el audio.

## Revisión compartida

Abrir http://127.0.0.1:8776/. El selector contiene la grabación completa y los cuatro recortes anteriores, con sus textos originales. Escuchar especialmente 16–30 s del audio completo y compararlo con Intermedio 1; después comprobar intentos del inicio, intermedio y final. Las referencias humanas previas conservan su alcance de muestras. Los resultados completos se publican como exploratorios y pendientes de revisión literal exhaustiva, sin activar el motor en el seguidor.

Comandos de comprobación (sin inferencia):

```powershell
.\.venv\Scripts\python.exe -m scripts.verificar_piloto_literal resultados/literalidad/20261023_131712_130708
.\.venv\Scripts\python.exe -m scripts.informar_literalidad_completa resultados/literalidad/20261023_131712_130708
.\.venv\Scripts\python.exe -m scripts.ver_piloto_literal resultados/literalidad/20261023_131712_130708 --puerto 8776
```

Referencia puntual del lector: datos/anotaciones/lectura_02_piloto_literal_revision.json (SHA256 2f0826de2fd6e086489fecb151a5a8e82d838df0f6e56db0b4ad524d244b229d).
Entradas, modelo, salidas, código ejecutado y piloto previo: huellas en manifest.json e integridad.json.
