# Control VAD del final: mismo reconocedor literal

Control offline de la cola: mismo candidato literal y parámetros; solo cambia la entrada hasta el último final VAD con margen ya incluido. Se conserva el prefijo completo, con pausas interiores e índice temporal desde cero. Originales intactos; una inferencia nueva por caso. Original literal reutilizado del lote previo: no es una nueva medición pareada de tiempo. Cambiar la duración puede cambiar la geometría/ruta corta-larga de bloques; no aísla una causa interna ni valida el VAD en todo el habla. Selección de números originales: [3, 13]. Todos de desarrollo. Sin cambios del seguidor ni publicación automática.

| Audio original | Papel | Duración original / enviada (s) | Inferencia previa / nueva (s) | Texto idéntico |
|---|---|---:|---:|---|
| Audio 3 · Lectura con pausa (flor-Ana) - cuento 1 - 14-10-2026.wav | control_pausa_larga | 60.000 / 31.376 | 24.88 / 10.12 | no |
| Audio 13 · Lectura pausa con relectura barco rojo - el barco - cuento 2 - lectura_02 - 23-10-2026.wav | control_pausa_larga | 50.000 / 41.776 | 14.10 / 11.08 | sí |

## Coste y límites

Entradas originales: 110.000 s; enviadas a la variante: 73.152 s. Inferencia original reutilizada: 38.98 s; nueva: 21.21 s; carga única nueva: 7.91 s.

Previo reutilizado de 17 casos; variante medida en proceso nuevo de 2. Orden/estado térmico/caché pueden influir. VAD previo medido aparte, no incluido en estas inferencias. RAM muestreada por caso y pico de proceso no son el mismo indicador; CPU incluye instrumentación y GPU es global.

RTF original y RTF sobre entrada enviada se guardan separados en metricas.json; acortar una cola cambia el denominador. La carga y VAD se contabilizan aparte; no son latencia de tablet ni del seguidor. Las marcas ASR siguen sin validar. Sin nueva referencia humana de estos textos ni precisión/F1 global.

## Salidas intactas para revisión

### Audio 3 · Lectura con pausa (flor-Ana) - cuento 1 - 14-10-2026.wav

**Literal original, lote previo:** Una mañana Ana salió al jardín de su casa. Cerca de un árbol encontró una mariposa azul. La mariposa voló despacio y se posó sobre una flor. Ana llamó su hermano para que pudiera verla. Los dos se quedaron en silencio mirando sus alas. Después volvieron a casa y dibujaron la mariposa en un cuaderno. [throatclearing]

**Literal con control del final, inferencia nueva:** Una mañana Ana salió al jardín de su casa. Cerca de un árbol encontró una mariposa azul. La mariposa voló despacio y se posó sobre una flor. Ana llamó su hermano para que pudiera verla. Los dos se quedaron en silencio mirando sus alas. Después volvieron a casa y dibujaron la mariposa en un cuaderno.

### Audio 13 · Lectura pausa con relectura barco rojo - el barco - cuento 2 - lectura_02 - 23-10-2026.wav

**Literal original, lote previo:** Una tarde, Lucía paseaba por el parque con su abuelo, junto a una fuente descubrió un pequeño barco rojo. Junto a una fuente descubrió un pequeño barco rojo, el barco flotaba de espacio entre las hojas. Lucía buscó una rama para acercar a la orilla, su abuelo la ayudó y juntos sacaron el barco del agua, después regresaron a casa y lo colocaron sobre una estantería.

**Literal con control del final, inferencia nueva:** Una tarde, Lucía paseaba por el parque con su abuelo, junto a una fuente descubrió un pequeño barco rojo. Junto a una fuente descubrió un pequeño barco rojo, el barco flotaba de espacio entre las hojas. Lucía buscó una rama para acercar a la orilla, su abuelo la ayudó y juntos sacaron el barco del agua, después regresaron a casa y lo colocaron sobre una estantería.

Escuchar el original completo y, opcionalmente, solo el prefijo enviado en http://127.0.0.1:8778/. El texto del cuento no se entrega al ASR y no se corrigen automáticamente sus errores.
