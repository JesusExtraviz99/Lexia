# Control VAD del final: mismo reconocedor literal

Control offline de la cola: mismo candidato literal y parámetros; solo cambia la entrada hasta el último final VAD con margen ya incluido. Se conserva el prefijo completo, con pausas interiores e índice temporal desde cero. Originales intactos; una inferencia nueva por caso. Original literal reutilizado del lote previo: no es una nueva medición pareada de tiempo. Cambiar la duración puede cambiar la geometría/ruta corta-larga de bloques; no aísla una causa interna ni valida el VAD en todo el habla. Casos 1,4,5,6,11,17 y controles 9/16; todos de desarrollo. Sin cambios del seguidor ni publicación automática.

| Audio original | Papel | Duración original / enviada (s) | Inferencia previa / nueva (s) | Texto idéntico |
|---|---|---:|---:|---|
| Audio 1 · Lectura normal - cuento 1 - 14-10-2026.wav | problema_senalado | 40.000 / 23.312 | 57.75 / 7.53 | no |
| Audio 4 · Lectura lenta - cuento 1 - 16-10-2026.wav | problema_senalado | 90.000 / 77.680 | 37.03 / 16.05 | no |
| Audio 5 · Lectura con relectura (Los dos se quedaron en silencio) - cuento 1 - 16-10-2026.wav | problema_senalado | 60.000 / 29.680 | 22.39 / 7.25 | no |
| Audio 6 · Lectura con relectura lejana (Los dos-alas) - cuento 1 - 21-10-2026.wav | problema_senalado | 60.000 / 33.136 | 62.40 / 11.58 | no |
| Audio 9 · Lectura normal con lluvia - cuento 2 - 21-10-2026.wav | control | 40.000 / 26.352 | 13.88 / 7.06 | sí |
| Audio 11 · Lectura lenta - cuento 2 - lectura_02 - 23-10-2026.wav | problema_senalado | 90.000 / 66.800 | 61.24 / 15.06 | no |
| Audio 16 · Lectura con muchas trabadas - cuento 2 - lectura_02 - 23-10-2026.wav | control | 60.000 / 56.528 | 20.21 / 16.66 | sí |
| Audio 17 · Lectura omisión abuelo - cuento 2 - lectura_02 - 23-10-2026.wav | problema_senalado | 40.000 / 27.632 | 12.58 / 6.77 | sí |

## Coste y límites

Entradas originales: 480.000 s; enviadas a la variante: 341.120 s. Inferencia original reutilizada: 287.48 s; nueva: 87.95 s; carga única nueva: 11.62 s.

Previo reutilizado de 17 casos; variante medida en proceso nuevo de 8. Orden/estado térmico/caché pueden influir. VAD previo medido aparte, no incluido en estas inferencias. RAM muestreada por caso y pico de proceso no son el mismo indicador; CPU incluye instrumentación y GPU es global.

RTF original y RTF sobre entrada enviada se guardan separados en metricas.json; acortar una cola cambia el denominador. La carga y VAD se contabilizan aparte; no son latencia de tablet ni del seguidor. Las marcas ASR siguen sin validar. Sin nueva referencia humana de estos textos ni precisión/F1 global.

## Salidas intactas para revisión

### Audio 1 · Lectura normal - cuento 1 - 14-10-2026.wav

**Literal original, lote previo:** Una mañana, Ana, salió al jardín de su casa. Cerca de un árbol, encontró una mariposa azul. La mariposa voló despacio y se posó sobre una flor. Ana llamó a su hermano para que pudiera verla. Los dos se quedaron en silencio, mirando sus alas. Después volvieron a casa y dibujaron la mariposa en un cuaderno. Vas por el lado de las chicas, la mariposa, el cuaderno y la mariposa y los chicas, las mariposas, las mariposas, las mariposas, las mariposas.

**Literal con control del final, inferencia nueva:** Una mañana, Ana, salió al jardín de su casa. Cerca de un árbol, encontró una mariposa azul. La mariposa voló despacio y se posó sobre una flor. Ana llamó a su hermano para que pudiera verla. Los dos se quedaron en silencio, mirando sus alas. Después volvieron a casa y dibujaron la mariposa en un cuaderno.

### Audio 4 · Lectura lenta - cuento 1 - 16-10-2026.wav

**Literal original, lote previo:** Una mañana Ana salió al jardín de su casa. Cerca de un árbol encontró una mariposa azul. La mariposa voló desváceo y se posó sobre una flor. Ana llamó a su hermano para que pudiera verla. Los dos se quedaron en silencio, mirando sus alas. Después volvieron a casa y dibujaron la mariposa en un jugador no. Ven.

**Literal con control del final, inferencia nueva:** Una mañana Ana salió al jardín de su casa. Cerca de un árbol encontró una mariposa azul. La mariposa voló desváceo y se posó sobre una flor. Ana llamó a su hermano para que pudiera verla. Los dos se quedaron en silencio, mirando sus alas. Después volvieron a casa y dibujaron la mariposa en un jugador no.

### Audio 5 · Lectura con relectura (Los dos se quedaron en silencio) - cuento 1 - 16-10-2026.wav

**Literal original, lote previo:** Una mañana Ana salió al jardín de su casa. Cerca de un árbol encontró una mariposa azul. La mariposa voló despacio y se posó sobre una flor. Ana llamó su hermano para que pudiera verla. Los dos se quedaron en silencio. Los dos se quedaron en silencio mirando sus alas. Después volvieron a casa y dibujaron la mariposa en un cuaderno. Ven.

**Literal con control del final, inferencia nueva:** Una mañana Ana salió al jardín de su casa. Cerca de un árbol encontró una mariposa azul. La mariposa voló despacio y se posó sobre una flor. Ana llamó su hermano para que pudiera verla. Los dos se quedaron en silencio. Los dos se quedaron en silencio mirando sus alas. Después volvieron a casa y dibujaron la mariposa en un cuaderno.

### Audio 6 · Lectura con relectura lejana (Los dos-alas) - cuento 1 - 21-10-2026.wav

**Literal original, lote previo:** Una mañana Ana salió al jardín de su casa. Cerca de un árbol encontró una mariposa azul. La mariposa voló despacio y se posó sobre una flor. Ana llamó a su hermano para que pudiera verla. Los dos se quedaron en silencio mirando sus alas. Después volvieron a casa y dibujaron la mariposa en un cuaderno. Los dos se quedaron en silencio mirando sus alas. ¿Y por qué no se puede ver el maravilla?

**Literal con control del final, inferencia nueva:** Una mañana Ana salió al jardín de su casa. Cerca de un árbol encontró una mariposa azul. La mariposa voló despacio y se posó sobre una flor. Ana llamó a su hermano para que pudiera verla. Los dos se quedaron en silencio mirando sus alas. Después volvieron a casa y dibujaron la mariposa en un cuaderno. Los dos se quedaron en silencio mirando sus alas.

### Audio 9 · Lectura normal con lluvia - cuento 2 - 21-10-2026.wav

**Literal original, lote previo:** Una tarde, Lucía paseaba por el parque con su abuelo. Junto a una fuente descubrió un pequeño barco rojo. El barco flotaba despacio entre las hojas. Lucía buscó una rama para acercarlo a la orilla. Su abuelo la ayudó y juntos sacaron el barco del agua. Después regresaron a casa y lo colocaron sobre una estantería.

**Literal con control del final, inferencia nueva:** Una tarde, Lucía paseaba por el parque con su abuelo. Junto a una fuente descubrió un pequeño barco rojo. El barco flotaba despacio entre las hojas. Lucía buscó una rama para acercarlo a la orilla. Su abuelo la ayudó y juntos sacaron el barco del agua. Después regresaron a casa y lo colocaron sobre una estantería.

### Audio 11 · Lectura lenta - cuento 2 - lectura_02 - 23-10-2026.wav

**Literal original, lote previo:** Una tarde, Lucía paseaba por el parque con su abuelo. Junto a una fuente descubrió un pequeño barco rojo. El barco flotaba despacio entre las hojas. Lucía buscó una rama para acercarlo a la orilla. Su abuelo la ayudó y juntos sacaron el barco del agua. Después regresaron a casa y lo colocaron sobre una estantería. A la vez de hoy, la familia está en su casa, y el joven se lo lleva.

**Literal con control del final, inferencia nueva:** Una tarde, Lucía paseaba por el parque con su abuelo. Junto a una fuente descubrió un pequeño barco rojo. El barco flotaba despacio entre las hojas. Lucía buscó una rama para acercarlo a la orilla. Su abuelo la ayudó y juntos sacaron el barco del agua. Después regresaron a casa y lo colocaron sobre una estantería.

### Audio 16 · Lectura con muchas trabadas - cuento 2 - lectura_02 - 23-10-2026.wav

**Literal original, lote previo:** U- u- una tarde lu- lucia pa- paseaba por el par- parque con su abuelo junto a una un- una fuente des- des- descu- descubrió un pe- pequeño barco rojo, el el barco el barco flotaba des- despacio en entre las hojas. Lu- Lucia buscó una r- rama para acercarlo a la ori- o- orilla. Su abuelo la la ayudó y y juntos sa- sacaron el barco del del agua. Des- después regres- regresaron a casa y lo y lo colocaron sobre una estantería.

**Literal con control del final, inferencia nueva:** U- u- una tarde lu- lucia pa- paseaba por el par- parque con su abuelo junto a una un- una fuente des- des- descu- descubrió un pe- pequeño barco rojo, el el barco el barco flotaba des- despacio en entre las hojas. Lu- Lucia buscó una r- rama para acercarlo a la ori- o- orilla. Su abuelo la la ayudó y y juntos sa- sacaron el barco del del agua. Des- después regres- regresaron a casa y lo y lo colocaron sobre una estantería.

### Audio 17 · Lectura omisión abuelo - cuento 2 - lectura_02 - 23-10-2026.wav

**Literal original, lote previo:** Una tarde, Lucía paseaba por el parque Consu, junto a una fuente descubrió un pequeño barco rojo. El barco flotaba despacio entre las hojas. Lucía buscó una rama para acercarlo a la orilla. Suu la ayudó y juntos sacaron el barco del agua. Después regresaron a casa y lo colocaron sobre una estantería.

**Literal con control del final, inferencia nueva:** Una tarde, Lucía paseaba por el parque Consu, junto a una fuente descubrió un pequeño barco rojo. El barco flotaba despacio entre las hojas. Lucía buscó una rama para acercarlo a la orilla. Suu la ayudó y juntos sacaron el barco del agua. Después regresaron a casa y lo colocaron sobre una estantería.

Escuchar el original completo y, opcionalmente, solo el prefijo enviado en http://127.0.0.1:8778/. El texto del cuento no se entrega al ASR y no se corrigen automáticamente sus errores.
