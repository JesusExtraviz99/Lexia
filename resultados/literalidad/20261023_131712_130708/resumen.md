# Piloto de transcripción literal

Mismo WAV completo para ambos motores, sin cuento ni notas como prompt; una pasada offline. Se conservan modelo y ajustes del piloto corto. Para entradas mayores de 30 s el candidato activa su estrategia interna continuation (ventanas 30 s, paso 26 s y contexto generado). No escucha toda la grabación en una única ventana. Cambian duración y procesamiento interno: no se aísla una causa del error ni se mide seguimiento en directo. Comparar el tramo revisado, sin convertir diferencias de texto en métricas humanas.

| Muestra | Nota de escucha del lector | Faster Whisper Small | CrisperWhisper Small · literal |
|---|---|---|---|
| completa | Lectura completa con trabadas variables, según el lector. No es una referencia literal exhaustiva. Comparar con las notas y el error confirmado del recorte 16–24 s. |  Una tarde Lucía paseaba por el parque con su abuelo. Junto a una fuente descubrió un pequeño barco rojo.  el barco flotaba despacio entre las hojas, Lucía buscó una drama para acercarlo a la orilla,  su abuelo la ayudó y juntos sacaron el barco del agua, después regresaron a casa y lo colocaron  sobre una estantería. | U- u- una tarde lu- lucia pa- paseaba por el par- parque con su abuelo junto a una un- una fuente des- des- descu- descubrió un pe- pequeño barco rojo, el el barco el barco flotaba des- despacio en entre las hojas. Lu- Lucia buscó una r- rama para acercarlo a la ori- o- orilla. Su abuelo la la ayudó y y juntos sa- sacaron el barco del del agua. Des- después regres- regresaron a casa y lo y lo colocaron sobre una estantería. |

## Cómputo de esta implementación

| Motor | Backend / precisión | Carga (s) | Suma inferencias (s) | Pico RAM del proceso (MiB) |
|---|---|---:|---:|---:|
| baseline | ctranslate2 / int8 | 1.00 | 5.23 | 696.67578125 |
| candidato | transformers / float32 | 7.44 | 15.50 | 4417.31640625 |

Las entradas suman 60.00 s por motor. Las dos implementaciones cambian modelo, backend y precisión; calidad exploratoria y coste observado no aíslan el efecto del entrenamiento ni predicen tablet. CPU/RAM/GPU completas en cada JSON. No se calculan tasas de detección o conteos exactos sin revisión por evento.

No se introdujo el cuento ni las notas humanas como prompt. Comprobar todo texto nuevo contra el audio antes de considerarlo una mejora. Los fragmentos al borde de una ventana pueden estar incompletos por el corte.
