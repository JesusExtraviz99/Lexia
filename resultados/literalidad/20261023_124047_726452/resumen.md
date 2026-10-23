# Piloto de transcripción literal

Exploración: una pasada por motor. Cuatro muestras con revisión cualitativa, dos controles fluidos y uno sin habla según referencia del lector. Notas no son conteos por evento ni referencia exhaustiva. No se proporciona el cuento o las notas al reconocedor. Mismos arrays de entrada, modelos y backends/precisiones distintos; sin cambio del seguidor.

| Muestra | Nota de escucha del lector | Faster Whisper Small | CrisperWhisper Small · literal |
|---|---|---|---|
| inicio | Las trabadas de este audio son tal cual así: u un una tarde, lu lucia pa paseaba por el par parque |  Una tarde Lucía paseaba por el parque. | U- u- una tarde lu- lucia pa- paseaba por el par- parque. |
| medio_1 | Las trabadas en este audio son: Descu descubrió un pe pequeño barco rojo el el barco |  descubrió un pequeño barco rojo, el barco... | Descu- descubrió un pe- pequeño barco rojo, el el barco, el barco rojo. |
| medio_2 | Las trabadas de este audio son estas: para acercarlo a la ori o orilla su abuelo la la ayudó y y jun |  para acercarlo a la orilla.  Su abuelo la ayudó y junto... | Para acercarlo a la ori- o- orilla, su abuelo la la ayudó y y junto. |
| final | Lo que se oye en el audio es esto: pues regre re regresaron a casa y lo y lo colocaron sobre una estantería |  pues regresaron a casa y lo colocaron sobre una estantería. | Pues regres- regres- regresaron a casa y lo y lo colocaron sobre una estantería. |
| fluida_inicio | Lectura normal validada por el lector; ruido breve inicial comunicado. |  Una mañana Ana salió al jardín de su casa, cerca de un árbol encontró una mariposa azul. | Una mañana, Ana, salió al jardín de su casa. Cerca de un árbol, encontró una mariposa azul. |
| fluida_medio | Lectura normal validada por el lector; evaluar posibles fragmentos de borde como tales. |  La mariposa voló despacio y se posó sobre una flor.  Ana llamó a su hermano para que pudiera verla. | La mariposa voló despacio y se posó sobre una flor. Ana llamó a su hermano para que pudiera verla. Los dos. |
| sin_habla | Según el lector, tras 23–24 s hay silencio con ruidos ambientales leves, sin habla adicional. |  |  |

## Cómputo de esta implementación

| Motor | Backend / precisión | Carga (s) | Suma inferencias (s) | Pico RAM del proceso (MiB) |
|---|---|---:|---:|---:|
| baseline | ctranslate2 / int8 | 1.15 | 14.08 | 696.734375 |
| candidato | transformers / float32 | 18.33 | 50.37 | 4252.88671875 |

Las muestras suman 56 s, incluida una sin habla. Las dos implementaciones cambian modelo, backend y precisión; calidad exploratoria y coste observado no aíslan el efecto del entrenamiento ni predicen tablet. CPU/RAM/GPU completas en cada JSON. No se calculan tasas de detección o conteos exactos sin revisión por evento.

No se introdujo el cuento ni las notas humanas como prompt. Comprobar todo texto nuevo contra el audio antes de considerarlo una mejora. Los fragmentos al borde de una ventana pueden estar incompletos por el corte.
