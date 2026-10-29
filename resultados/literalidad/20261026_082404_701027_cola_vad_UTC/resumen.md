# Control VAD del final: mismo reconocedor literal

Control offline de la cola: mismo candidato literal y parámetros; solo cambia la entrada hasta el último final VAD con margen ya incluido. Se conserva el prefijo completo, con pausas interiores e índice temporal desde cero. Originales intactos; una inferencia nueva por caso. Original literal reutilizado del lote previo: no es una nueva medición pareada de tiempo. Cambiar la duración puede cambiar la geometría/ruta corta-larga de bloques; no aísla una causa interna ni valida el VAD en todo el habla. Selección de números originales: [1, 2, 3, 4, 5, 6]. Partición según el registro de catálogo de cada audio. Sin cambios del seguidor ni publicación automática.

| Audio original | Papel | Duración original / enviada (s) | Inferencia previa / nueva (s) | Texto idéntico |
|---|---|---:|---:|---|
| Audio 1 · Lectura normal - caja del sendero - lectura_04 - 26-10-2026.wav | seleccion_explicita | 90.000 / 52.592 | 25.95 / 12.00 | sí |
| Audio 2 · Lectura repeticiones de palabras - caja del sendero - lectura_04 - 26-10-2026.wav | seleccion_explicita | 100.000 / 65.840 | 25.20 / 20.94 | no |
| Audio 3 · Lectura intentos parciales - caja del sendero - lectura_04 - 26-10-2026.wav | seleccion_explicita | 120.000 / 70.320 | 32.48 / 22.61 | no |
| Audio 4 · Lectura omisiones y sustituciones - caja del sendero - lectura_04 - 26-10-2026.wav | seleccion_explicita | 90.000 / 59.984 | 24.19 / 19.25 | sí |
| Audio 5 · Lectura pausa larga y continuacion - caja del sendero - lectura_04 - 26-10-2026.wav | seleccion_explicita | 120.000 / 72.112 | 53.00 / 19.30 | no |
| Audio 6 · Lectura dificultades mixtas libres - caja del sendero - lectura_04 - 26-10-2026.wav | seleccion_explicita | 150.000 / 98.160 | 52.64 / 24.76 | no |

## Coste y límites

Entradas originales: 670.000 s; enviadas a la variante: 419.008 s. Inferencia original reutilizada: 213.46 s; nueva: 118.86 s; carga única nueva: 7.60 s.

Previo reutilizado de 6 casos; variante medida en proceso nuevo de 6. Orden/estado térmico/caché pueden influir. VAD previo medido aparte, no incluido en estas inferencias. RAM muestreada por caso y pico de proceso no son el mismo indicador; CPU incluye instrumentación y GPU es global.

RTF original y RTF sobre entrada enviada se guardan separados en metricas.json; acortar una cola cambia el denominador. La carga y VAD se contabilizan aparte; no son latencia de tablet ni del seguidor. Las marcas ASR siguen sin validar. Sin nueva referencia humana de estos textos ni precisión/F1 global.

## Salidas intactas para revisión

### Audio 1 · Lectura normal - caja del sendero - lectura_04 - 26-10-2026.wav

**Literal original, lote previo:** Una mañana Mateo salió a caminar con su hermana Clara. Junto al puente encontraron una pequeña caja de madera. Dentro había una llave, una pluma azul y un papel doblado. Clara abrió el papel y leyó, busca donde termina el sendero. Los dos siguieron despacio hasta un viejo molino. Allí descubrieron una puerta escondida entre las plantas. Mateo probó la llave, pero no consiguió abrirla, entonces Clara levantó una piedra y encontró otra entrada. Detrás había un jardín lleno de flores. Antes de regresar, dejaron la caja junto al puente para que alguien más pudiera descubrir el secreto.

**Literal con control del final, inferencia nueva:** Una mañana Mateo salió a caminar con su hermana Clara. Junto al puente encontraron una pequeña caja de madera. Dentro había una llave, una pluma azul y un papel doblado. Clara abrió el papel y leyó, busca donde termina el sendero. Los dos siguieron despacio hasta un viejo molino. Allí descubrieron una puerta escondida entre las plantas. Mateo probó la llave, pero no consiguió abrirla, entonces Clara levantó una piedra y encontró otra entrada. Detrás había un jardín lleno de flores. Antes de regresar, dejaron la caja junto al puente para que alguien más pudiera descubrir el secreto.

### Audio 2 · Lectura repeticiones de palabras - caja del sendero - lectura_04 - 26-10-2026.wav

**Literal original, lote previo:** Una mañana Mateo salió a caminar con su hermana Clara. Junto al puente encontraron una una pequeña caja de madera. Dentro había una llave, una pluma azul y un papel doblado. Clara Clara abrió el papel y leyó, busca donde termina el sendero. Los dos siguieron despacio hasta un viejo molino, allí descubrieron una puerta escondida entre las plantas. Mateo Mateo probó la llave, pero no consiguió abrirla. Entonces Clara levantó una piedra y encontró otra entrada. Detrás había un jardín lleno de flores. Antes de regresar, dejaron la caja junto junto al puente para que alguien más pudiera descubrir el secreto. ¿Para qué?

**Literal con control del final, inferencia nueva:** Una mañana Mateo salió a caminar con su hermana Clara. Junto al puente encontraron una una pequeña caja de madera. Dentro había una llave, una pluma azul y un papel doblado. Clara Clara abrió el papel y leyó, busca donde termina el sendero. Los dos siguieron despacio hasta un viejo molino, allí descubrieron una puerta escondida entre las plantas. Mateo Mateo probó la llave, pero no consiguió abrirla. Entonces Clara levantó una piedra y encontró otra entrada. Detrás había un jardín lleno de flores. Antes de regresar, dejaron la caja junto junto al puente para que alguien más pudiera descubrir el secreto.

### Audio 3 · Lectura intentos parciales - caja del sendero - lectura_04 - 26-10-2026.wav

**Literal original, lote previo:** Una mañana Mateo salió a caminar con su hermana Clara. Junto al puente encontraron una pe- pe- pequeña caja de madera. Dentro había una llave, una pluma azul y un papel doblado. Clara abrió el papel y leyó:"Busca donde termina el sendero". Los dos siguieron despacio hasta un viejo molino. Allí des des descubrieron una puerta escondida entre las plantas. Mateo probó la llave, pero no consiguió abrirla. Entonces Clara levantó una piedra y encontró otra entrada. Detrás había un jardín lleno de flores. Antes de regresar, dejaron la caja junto al puente para que alguien más pudiera descubrir el secreto. ¿Para qué?

**Literal con control del final, inferencia nueva:** Una mañana Mateo salió a caminar con su hermana Clara. Junto al puente encontraron una pe- pe- pequeña caja de madera. Dentro había una llave, una pluma azul y un papel doblado. Clara abrió el papel y leyó:"Busca donde termina el sendero". Los dos siguieron despacio hasta un viejo molino. Allí des des descubrieron una puerta escondida entre las plantas. Mateo probó la llave, pero no consiguió abrirla. Entonces Clara levantó una piedra y encontró otra entrada. Detrás había un jardín lleno de flores. Antes de regresar, dejaron la caja junto al puente para que alguien más pudiera descubrir el secreto.

### Audio 4 · Lectura omisiones y sustituciones - caja del sendero - lectura_04 - 26-10-2026.wav

**Literal original, lote previo:** Una mañana Mateo salió a caminar con su hermana Clara, junto al puente, encontraron una pequeña caja de dentro había una llave, una pluma roja y un papel doblado. Clara abrió el papel y leyó:"Busca donde termina el sendero". Los dos siguieron despacio hasta un molino. Allí descubrieron una puerta escondida entre las plantas. Mateo probó la llave, pero no consiguió abrirla. Entonces Clara levantó una piedra y encontró otra entrada. Detrás había un parque lleno de flores. Antes de regresar, dejaron la caja junto al puente para que alguien más pudiera descubrir el secreto.

**Literal con control del final, inferencia nueva:** Una mañana Mateo salió a caminar con su hermana Clara, junto al puente, encontraron una pequeña caja de dentro había una llave, una pluma roja y un papel doblado. Clara abrió el papel y leyó:"Busca donde termina el sendero". Los dos siguieron despacio hasta un molino. Allí descubrieron una puerta escondida entre las plantas. Mateo probó la llave, pero no consiguió abrirla. Entonces Clara levantó una piedra y encontró otra entrada. Detrás había un parque lleno de flores. Antes de regresar, dejaron la caja junto al puente para que alguien más pudiera descubrir el secreto.

### Audio 5 · Lectura pausa larga y continuacion - caja del sendero - lectura_04 - 26-10-2026.wav

**Literal original, lote previo:** Una mañana Mateo salió a caminar con su hermana Clara. Junto al puente, encontraron una pequeña caja de madera. Dentro había una llave, una pluma azul y un papel doblado. Clara abrió el papel y leyó, busca donde termina el sendero. Los dos siguieron despacio hasta un viejo molino. Allí descubrieron una puerta escondida entre las plantas. Mateo probó la llave, pero no consiguió abrirla. Entonces Clara levantó una piedra y encontró otra entrada. Detrás había un jardín lleno de flores. Antes de regresar, dejaron la caja junto al puente para que alguien más pudiera descubrir el secreto. P- p. P- p.

**Literal con control del final, inferencia nueva:** Una mañana Mateo salió a caminar con su hermana Clara. Junto al puente, encontraron una pequeña caja de madera. Dentro había una llave, una pluma azul y un papel doblado. Clara abrió el papel y leyó, busca donde termina el sendero. Los dos siguieron despacio hasta un viejo molino. Allí descubrieron una puerta escondida entre las plantas. Mateo probó la llave, pero no consiguió abrirla. Entonces Clara levantó una piedra y encontró otra entrada. Detrás había un jardín lleno de flores. Antes de regresar, dejaron la caja junto al puente para que alguien más pudiera descubrir el secreto.

### Audio 6 · Lectura dificultades mixtas libres - caja del sendero - lectura_04 - 26-10-2026.wav

**Literal original, lote previo:** [yawn] Una mañana, ma- ma- Mateo salió a caminar con su her- her- hermana Clara. Junto al puente descubrieron encontraron una pequeña caja de madera. Dentro había una llave, una una pluma azul y un papel doblado. Clara abrió el papel y leyó, busca donde termina el sendero, los dos siguieron despacio hasta un viejo molino. Allí des- descubrí des- descubrí descubrieron una puerta escondida entre las plantas. Mateo probó la llave, pero no con consiguió abrirla. Entonces Clara Levam le- Levam levantó una piedra y encontró otra entrada detrás había un jardín lleno de flores, antes de regresar dejaron la ca- la casa la- la caja junto al puente para que alguien más pudiera descubrir el secreto. P- por favor, si te da la pena, por favor, si te da la pena, por favor, si te da la pena, ¿?

**Literal con control del final, inferencia nueva:** [yawn] Una mañana, ma- ma- Mateo salió a caminar con su her- her- hermana Clara. Junto al puente descubrieron encontraron una pequeña caja de madera. Dentro había una llave, una una pluma azul y un papel doblado. Clara abrió el papel y leyó, busca donde termina el sendero, los dos siguieron despacio hasta un viejo molino. Allí des- descubrí des- descubrí descubrieron una puerta escondida entre las plantas. Mateo probó la llave, pero no con consiguió abrirla. Entonces Clara Levam le- Levam levantó una piedra y encontró otra entrada detrás había un jardín lleno de flores, antes de regresar dejaron la ca- la casa la- la caja junto al puente para que alguien más pudiera descubrir el secreto.

Escuchar el original completo y, opcionalmente, solo el prefijo enviado en http://127.0.0.1:8778/. El texto del cuento no se entrega al ASR y no se corrigen automáticamente sus errores.
