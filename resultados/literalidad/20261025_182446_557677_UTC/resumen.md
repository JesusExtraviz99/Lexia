# Reconocimiento completo de todos los audios propios

Lote de desarrollo, una pasada por motor y WAV completo; un proceso por motor y modelo reutilizado secuencialmente. No se entregan cuento ni notas al ASR. Mismos arrays mono 16 kHz, sin VAD ni limpieza de ruido. Small CT2 CPU int8 frente a CrisperWhisper2.0 Small Transformers CPU float32 literal; cuatro hilos. Candidato >30 s: continuation, bloques 30 s/paso 26 s con contexto generado. Duración incluye silencio; no latencia en directo ni rendimiento de tablet. El seguimiento no cambia. Nombres/consignas y diferencias de texto no validan fidelidad ni permiten calcular tasas humanas. El audio externo no está descargado en el proyecto y no forma parte de este lote.

17 WAV completos; 880.00 s (14.67 min) por motor. Una pasada por archivo, sin nuevas voces ni repetición estadística.

| Audio | Duración (s) | Actual inferencia (s) | Literal inferencia (s) | RTF actual / literal | RAM máxima muestreada actual / literal (MiB) |
|---|---:|---:|---:|---|---|
| Lectura normal - cuento 1 - 14-10-2026.wav | 40.00 | 5.05 | 57.75 | 0.126 / 1.444 | 538.6 / 4204.1 |
| Lectura con disfluencias (Ana repetida, sin despacio, mari-mariposa) - cuento 1 - 14-10-2026.wav | 30.00 | 4.78 | 8.11 | 0.159 / 0.270 | 540.1 / 4258.8 |
| Lectura con pausa (flor-Ana) - cuento 1 - 14-10-2026.wav | 60.00 | 7.69 | 24.88 | 0.128 / 0.415 | 546.7 / 4260.6 |
| Lectura lenta - cuento 1 - 16-10-2026.wav | 90.00 | 10.71 | 37.03 | 0.119 / 0.411 | 541.6 / 4300.3 |
| Lectura con relectura (Los dos se quedaron en silencio) - cuento 1 - 16-10-2026.wav | 60.00 | 8.67 | 22.39 | 0.144 / 0.373 | 553.5 / 4314.6 |
| Lectura con relectura lejana (Los dos-alas) - cuento 1 - 21-10-2026.wav | 60.00 | 10.72 | 62.40 | 0.179 / 1.040 | 549.9 / 4218.1 |
| Lectura normal con lluvia - cuento 1 - 21-10-2026.wav | 40.00 | 7.27 | 21.64 | 0.182 / 0.541 | 556.3 / 4229.5 |
| Lectura con relectura lejana (Cerca-azul) - cuento 1 - 21-10-2026.wav | 45.00 | 6.21 | 15.20 | 0.138 / 0.338 | 555.7 / 4354.7 |
| Lectura normal con lluvia - cuento 2 - 21-10-2026.wav | 40.00 | 15.15 | 13.88 | 0.379 / 0.347 | 973.1 / 4272.7 |
| Lectura con relectura lejana (Junto-rojo) - cuento 2 - 21-10-2026.wav | 45.00 | 5.80 | 13.45 | 0.129 / 0.299 | 560.0 / 4307.4 |
| Lectura lenta - cuento 2 - lectura_02 - 23-10-2026.wav | 90.00 | 12.48 | 61.24 | 0.139 / 0.680 | 893.8 / 4274.8 |
| Lectura rápida - cuento 2 - lectura_02 - 23-10-2026.wav | 30.00 | 3.58 | 8.73 | 0.119 / 0.291 | 547.6 / 4254.0 |
| Lectura pausa con relectura barco rojo - el barco - cuento 2 - lectura_02 - 23-10-2026.wav | 50.00 | 4.76 | 14.10 | 0.095 / 0.282 | 559.5 / 4289.9 |
| Lectura sustitución rojo por azul - cuento 2 - lectura_02 - 23-10-2026.wav | 50.00 | 5.58 | 12.84 | 0.112 / 0.257 | 562.0 / 4387.5 |
| Lectura con ruido de fondo - cuento 2 - lectura_02 - 23-10-2026.wav | 50.00 | 9.40 | 20.13 | 0.188 / 0.403 | 940.0 / 4398.5 |
| Lectura con muchas trabadas - cuento 2 - lectura_02 - 23-10-2026.wav | 60.00 | 7.22 | 20.21 | 0.120 / 0.337 | 536.8 / 4233.5 |
| Lectura omisión abuelo - cuento 2 - lectura_02 - 23-10-2026.wav | 40.00 | 6.43 | 12.58 | 0.161 / 0.315 | 565.9 / 4195.0 |

## Totales y alcance

| Motor | Inferencia total (s) | RTF ponderado por duración | Carga única (s) | Pico RAM de toda la vida del proceso (MiB) |
|---|---:|---:|---:|---:|
| baseline | 131.50 | 0.149 | 2.17 | 980.84 |
| candidato | 426.57 | 0.485 | 18.91 | 4466.64 |

Cada JSON contiene textos brutos, palabras automáticas, bloques nativos del candidato, CPU/RAM/GPU global, versiones y configuración. En cada audio se conserva el subintervalo de recursos del único muestreador. RAM por audio = máximo muestreado y extremos del intervalo, no pico independiente garantizado; el modelo se reutiliza y conserva memoria. Pico Windows = vida completa del proceso, incluida carga. CPU incluye instrumentación. GPU global no implica ejecución del ASR en GPU: ambos motores están en CPU. Energía propia del ASR/FLOPs/tablet no medidos.

RTF = inferencia / duración total, incluido silencio. No es retardo de captura/interfaz ni RTF sobre habla. Backends/precisiones distintos, orden fijo, una pasada: no hay comparación causal de entrenamiento, estabilidad térmica ni generalización. Los tiempos de palabra del candidato siguen sin validarse por las advertencias de compatibilidad conocidas.

## Transcripciones para revisión

Las notas son consignas y confirmaciones previas, no una referencia literal exhaustiva. Una palabra añadida respecto al otro motor puede ser recuperación real o inserción; decidir escuchando. No calcular WER literal, precisión/F1 ni intentos a partir del cuento pretendido o de transcripciones sin revisar. No sumar bloques internos como eventos separados.

### Lectura normal - cuento 1 - 14-10-2026.wav

Consigna/metadatos: Lectura normal · cuento 1 · 14/10/2026.  Estado de referencia: transcripcion_confirmada_por_usuario.

**Actual:**  Una mañana Ana salió al jardín de su casa. Cerca de un árbol encontró una mariposa azul.  La mariposa voló despacio y se posó sobre una flor. Ana llamó a su hermano para que pudiera  verla. Los dos se quedaron en silencio mirando sus alas. Después volvieron a casa y dibujaron  la mariposa en un cuaderno.

**Literal:** Una mañana, Ana, salió al jardín de su casa. Cerca de un árbol, encontró una mariposa azul. La mariposa voló despacio y se posó sobre una flor. Ana llamó a su hermano para que pudiera verla. Los dos se quedaron en silencio, mirando sus alas. Después volvieron a casa y dibujaron la mariposa en un cuaderno. Vas por el lado de las chicas, la mariposa, el cuaderno y la mariposa y los chicas, las mariposas, las mariposas, las mariposas, las mariposas.

### Lectura con disfluencias (Ana repetida, sin despacio, mari-mariposa) - cuento 1 - 14-10-2026.wav

Consigna/metadatos: Disfluencias: Ana repetida, omisión de despacio y mari… mariposa · cuento 1 · 14/10/2026. Repetición de Ana en posición 3. Omisión de despacio (21). Intento incompleto mari seguido de mariposa al final (53). Estado de referencia: transcripcion_confirmada_por_usuario. Ambiente: Pájaros intermitentes y ruidos de silla/mochila según escucha del usuario.

**Actual:**  Una mañana Ana, Ana salió al jardín de su casa, cerca de un árbol encontró una mariposa  azul. La mariposa voló y se posó sobre una flor. Ana llamó a su hermano para que pudiera  verla. Los dos se quedaron en cinesio mirando sus alas. Después volvieron a casa y dibujaron  la mariposa en un cuaderno.

**Literal:** Una mañana, Ana Ana salió al jardín de su casa, cerca de un árbol encontró una mariposa azul. La mariposa voló y se posó sobre una flor. Ana llamó a su hermano para que pudiera verla. Los dos se quedaron en cinesio mirando sus alas. Después volvieron a casa y dibujaron la mar- mariposa en un cuaderno.

### Lectura con pausa (flor-Ana) - cuento 1 - 14-10-2026.wav

Consigna/metadatos: Lectura con pausa entre flor y Ana · cuento 1 · 14/10/2026. Pausa entre flor (27) y Ana (28). Estado de referencia: transcripcion_confirmada_por_usuario. Ambiente: Pájaros al final descritos por el lector; no se atribuye causalidad.

**Actual:**  Una mañana, Ana salió al jardín de su casa. Cerca de un árbol encontró una mariposa azul.  La mariposa voló despacio y se posó sobre una flor.  Ana llamó su hermano para que pudiera verla. Los dos se quedaron en silencio mirando sus  salas. Después volvieron a caza y dibujaron la mariposa en un cuaderno.  ¡Suscríbete!

**Literal:** Una mañana Ana salió al jardín de su casa. Cerca de un árbol encontró una mariposa azul. La mariposa voló despacio y se posó sobre una flor. Ana llamó su hermano para que pudiera verla. Los dos se quedaron en silencio mirando sus alas. Después volvieron a casa y dibujaron la mariposa en un cuaderno. [throatclearing]

### Lectura lenta - cuento 1 - 16-10-2026.wav

Consigna/metadatos: Lectura lenta · cuento 1 · 16/10/2026. Lectura deliberadamente lenta, sin omisiones confirmadas. Estado de referencia: transcripcion_confirmada_por_usuario. Ambiente: Ruido de silla al principio y final según el lector.

**Actual:**  Una mañana Ana salió al jardín de su casa, cerca de un árbol encontró una mariposa azul.  La mariposa voló despacio y se posó sobre una flor.  Ana llamó a su hermano para que pudiera verla.  Los dos se quedaron en silencio, mirando sus alas.  Después volvieron a casa y dibujaron la mariposa en un cuaderno.

**Literal:** Una mañana Ana salió al jardín de su casa. Cerca de un árbol encontró una mariposa azul. La mariposa voló desváceo y se posó sobre una flor. Ana llamó a su hermano para que pudiera verla. Los dos se quedaron en silencio, mirando sus alas. Después volvieron a casa y dibujaron la mariposa en un jugador no. Ven.

### Lectura con relectura (Los dos se quedaron en silencio) - cuento 1 - 16-10-2026.wav

Consigna/metadatos: Relectura de Los dos se quedaron en silencio · cuento 1 · 16/10/2026. Dos apariciones del tramo 37–42; después continúa el cuento. Estado de referencia: transcripcion_confirmada_por_usuario. Ambiente: Usuario describe audio limpio salvo ruido leve al final.

**Actual:**  Una mañana Ana salió al jardín de su casa.  Cerca de un árbol encontró una mariposa azul.  La mariposa voló despacio y se posó sobre una flor.  Ana llamó a su hermano para que pudiera verla.  Los dos se quedaron en silencio.  Los dos se quedaron en silencio mirando sus alas.  Después volvieron a casa y dibujaron la mariposa en un cuaderno.  Bueno, nos vemos en el próximo vídeo, ¡hasta la próxima!

**Literal:** Una mañana Ana salió al jardín de su casa. Cerca de un árbol encontró una mariposa azul. La mariposa voló despacio y se posó sobre una flor. Ana llamó su hermano para que pudiera verla. Los dos se quedaron en silencio. Los dos se quedaron en silencio mirando sus alas. Después volvieron a casa y dibujaron la mariposa en un cuaderno. Ven.

### Lectura con relectura lejana (Los dos-alas) - cuento 1 - 21-10-2026.wav

Consigna/metadatos: Relectura lejana: vuelta a Los dos… hasta alas · cuento 1 · 21/10/2026. Cuento completo, después relectura lenta de 37–45; final alas (45). Estado de referencia: transcripcion_confirmada_por_usuario.

**Actual:**  Una mañana Ana salió al jardín de su casa.  Cerca de un árbol encontró una mariposa azul.  La mariposa voló despacio y se posó sobre una flor.  Ana llamó a su hermano para que pudiera verla.  Los dos se quedaron en silencio mirando sus alas.  Después volvieron a casa y dibujaron la mariposa en un cuaderno.  Los dos se quedaron en silencio mirando sus alas.  y

**Literal:** Una mañana Ana salió al jardín de su casa. Cerca de un árbol encontró una mariposa azul. La mariposa voló despacio y se posó sobre una flor. Ana llamó a su hermano para que pudiera verla. Los dos se quedaron en silencio mirando sus alas. Después volvieron a casa y dibujaron la mariposa en un cuaderno. Los dos se quedaron en silencio mirando sus alas. ¿Y por qué no se puede ver el maravilla?

### Lectura normal con lluvia - cuento 1 - 21-10-2026.wav

Consigna/metadatos: Lectura normal con lluvia · cuento 1 · 21/10/2026.  Estado de referencia: lectura_unica_confirmada_por_usuario_sin_referencia_literal_guardada. Ambiente: Lluvia comunicada por el usuario.

**Actual:**  Una mañana Ana salió al jardín de su casa.  Cerca de un árbol encontró una mariposa azul.  La mariposa voló despacio y se posó sobre una flor.  Ana llamó su hermano para que pudiera verla.  Los dos se quedaron en silencio, mirando sus salas.  Después volvieron a casa y dibujaron la mariposa en un cuaderno.

**Literal:** Una mañana Ana salió al jardín de su casa. Cerca de un árbol encontró una mariposa azul. La mariposa voló despacio y se posó sobre una flor. Ana llamó su hermano para que pudiera verla. Los dos se quedaron en silencio, mirando sus alas. Después, volvieron a casa y dibujaron la mariposa en un cuaderno.

### Lectura con relectura lejana (Cerca-azul) - cuento 1 - 21-10-2026.wav

Consigna/metadatos: Relectura lejana: Cerca de un árbol… hasta azul · cuento 1 · 21/10/2026. Cuento completo seguido de relectura lenta de 10–17; final azul (17). Estado de referencia: transcripcion_confirmada_por_usuario.

**Actual:**  Una mañana Ana salió al jardín de su casa. Cerca de un árbol encontró una mariposa azul.  La mariposa voló despacio y se posó sobre una flor. Ana llamó a su hermano para que pudiera  verla. Los dos se quedaron en silencio mirando sus alas. Después volvieron a casa y dibujaron  la mariposa en un cuaderno.  Cerca de un árbol  encontró una mariposa azul.

**Literal:** Una mañana Ana salió al jardín de su casa. Cerca de un árbol encontró una mariposa azul. La mariposa voló despacio y se posó sobre una flor. Ana llamó su hermano para que pudiera verla. Los dos se quedaron en silencio, mirando sus alas. Después volvieron a casa y dibujaron la mariposa en un cuaderno. Cerca de un árbol encontró una mariposa azul.

### Lectura normal con lluvia - cuento 2 - 21-10-2026.wav

Consigna/metadatos: Lectura normal con lluvia · cuento 2 · 21/10/2026.  Estado de referencia: lectura_unica_confirmada_por_usuario_sin_referencia_literal_guardada. Ambiente: El usuario confirma que sigue lloviendo.

**Actual:**  Una tarde, Lucía paseaba por el parque con su abuelo.  Junto a una fuente descubrió un pequeño barco rojo.  El barco flotaba despacio entre las hojas.  Lucía buscó una rama para acercarlo a la orilla.  Su abuelo la ayudó y juntos sacaron el barco del agua.  Después regresaron a casa y lo colocaron sobre una estantería.  ¡Suscríbete!

**Literal:** Una tarde, Lucía paseaba por el parque con su abuelo. Junto a una fuente descubrió un pequeño barco rojo. El barco flotaba despacio entre las hojas. Lucía buscó una rama para acercarlo a la orilla. Su abuelo la ayudó y juntos sacaron el barco del agua. Después regresaron a casa y lo colocaron sobre una estantería.

### Lectura con relectura lejana (Junto-rojo) - cuento 2 - 21-10-2026.wav

Consigna/metadatos: Relectura lejana: Junto a una fuente… hasta rojo · cuento 2 · 21/10/2026. Cuento completo seguido de relectura lenta de 11–19; final rojo (19). Estado de referencia: transcripcion_confirmada_por_usuario. Ambiente: Nota humana en rojo: ruido de fondo algo notable. No se presupone intensidad de lluvia.

**Actual:**  Una tarde Lucía paseaba por el parque con su abuelo. Junto a una fuente descubrió un pequeño  barco rojo. El barco flutaba despacio entre las hojas. Lucía buscó una rama para acercarlo  a la orilla. Su abuelo la ayudó y junto sacaron el barco del agua. Después regresaron a casa  y lo colocaron sobre una estantería.  Junto a una fuente descubrió un pequeño barco rojo.

**Literal:** Una tarde, Lucía paseaba por el parque con su abuelo. Junto a una fuente descubrió un pequeño barco rojo. El barco flotaba despacio entre las hojas. Lucía buscó una rama para acercarlo a la orilla. Su abuelo la ayudó y juntos sacaron el barco del agua. Después regresaron a casa y lo colocaron sobre una estantería. Junto a una fuente descubrió un pequeño barco rojo.

### Lectura lenta - cuento 2 - lectura_02 - 23-10-2026.wav

Consigna/metadatos: Lectura lenta - cuento 2 · 23/10/2026.  Estado de referencia: descripcion_de_eventos_confirmada_por_lector_transcripcion_literal_pendiente. Ambiente: El usuario no percibe ruido de fondo en esta grabación; no es una medición de SNR.

**Actual:**  Una tarde Lucía paseaba por el parque con su abuelo.  Junto a una fuente descubrió un pequeño barco rojo.  El barco flotaba despacio entre las hojas.  Lucia buscó una rama para acercarlo a la orilla.  Su abuelo la ayudó y junto sacaron el barco del agua.  Después regresaron a casa y lo colocaron sobre una estantería.

**Literal:** Una tarde, Lucía paseaba por el parque con su abuelo. Junto a una fuente descubrió un pequeño barco rojo. El barco flotaba despacio entre las hojas. Lucía buscó una rama para acercarlo a la orilla. Su abuelo la ayudó y juntos sacaron el barco del agua. Después regresaron a casa y lo colocaron sobre una estantería. A la vez de hoy, la familia está en su casa, y el joven se lo lleva.

### Lectura rápida - cuento 2 - lectura_02 - 23-10-2026.wav

Consigna/metadatos: Lectura rápida - cuento 2 · 23/10/2026.  Estado de referencia: descripcion_de_eventos_confirmada_por_lector_transcripcion_literal_pendiente. Ambiente: El usuario no percibe ruido de fondo en esta grabación; no es una medición de SNR.

**Actual:**  Una tarde, Lucía paseaba por el parque con su abuelo. Junto a una fuente descubrió un pequeño barco rojo.  El barco flotaba despacio entre las hojas. Lucía buscó una rama para acercarlo a la orilla.  Su abuelo la ayudó y junto sacaron el barco del agua.  Después regresaron a casa y lo colocaron sobre una estantería.

**Literal:** Una tarde, Lucia paseaba por el parque con su abuelo, junto a una fuente descubrió un pequeño barco rojo, el barco flotaba despacio entre las hojas, Lucia buscó una rama para acercarlo a la orilla, su abuelo la ayudó y junto sacaron el barco del agua, después regresaron a casa y lo colocaron sobre una estantería.

### Lectura pausa con relectura barco rojo - el barco - cuento 2 - lectura_02 - 23-10-2026.wav

Consigna/metadatos: Lectura pausa con relectura barco rojo / el barco - cuento 2 · 23/10/2026. Tras leer Junto a una fuente descubrió un pequeño barco rojo, pausa aproximada de 8 s y relectura de la misma frase; después continúa hasta terminar el cuento. Estado de referencia: descripcion_de_eventos_confirmada_por_lector_transcripcion_literal_pendiente. Ambiente: El usuario no percibe ruido de fondo en esta grabación; no es una medición de SNR.

**Actual:**  Una tarde Lucía paseaba por el parque con su abuelo. Junto a una fuente descubrió un pequeño barco rojo.  Junto a una fuente descubrió un pequeño barco rojo. El barco flotaba despacio entre las hojas.  Lucía buscó una rama para acercarlo a la orilla. Su abuelo la ayudó y juntos sacaron el barco del  agua. Después regresaron a casa y lo colocaron sobre una estantería.

**Literal:** Una tarde, Lucía paseaba por el parque con su abuelo, junto a una fuente descubrió un pequeño barco rojo. Junto a una fuente descubrió un pequeño barco rojo, el barco flotaba de espacio entre las hojas. Lucía buscó una rama para acercar a la orilla, su abuelo la ayudó y juntos sacaron el barco del agua, después regresaron a casa y lo colocaron sobre una estantería.

### Lectura sustitución rojo por azul - cuento 2 - lectura_02 - 23-10-2026.wav

Consigna/metadatos: Lectura sustitución rojo por azul - cuento 2 · 23/10/2026.  Estado de referencia: descripcion_de_eventos_confirmada_por_lector_transcripcion_literal_pendiente. Ambiente: El usuario no percibe ruido de fondo en esta grabación; no es una medición de SNR.

**Actual:**  Una tarde Lucía paseaba por el parque con su abuelo. Junto a una fuente descubrió un pequeño barco azul.  El barco flotaba despacio entre las hojas. Lucía buscó una rama para acercarlo a la orilla.  Su abuelo la ayudó y juntos sacaron el barco del agua. Después regresaron a casa y lo colocaron sobre una estantería.  ¡Suscríbete!

**Literal:** Una tarde, Lucía paseaba por el parque con su abuelo. Junto a una fuente descubrió un pequeño barco azul. El barco flotaba despacio entre las hojas. Lucía buscó una rama para acercarlo a la orilla. Su abuelo la ayudó y juntos sacaron el barco del agua. Después regresaron a casa y lo colocaron sobre una estantería.

### Lectura con ruido de fondo - cuento 2 - lectura_02 - 23-10-2026.wav

Consigna/metadatos: Lectura con ruido de fondo - cuento 2 · 23/10/2026.  Estado de referencia: descripcion_de_eventos_confirmada_por_lector_transcripcion_literal_pendiente. Ambiente: Sonido de calle reproducido desde un móvil, según el usuario.

**Actual:**  Una tarde Lucía paseaba por el parque con su abuelo. Junto a una fuente descubrió un pequeño barco rojo.  El barco lotaba despacio entre las hojas. Lucía buscó una rama para acercarlo a la orilla.  Su abuelo la ayudó y junto sacaron el barco del agua.  Después regresaron a casa y lo colocaron sobre una estantería.  ¡Suscríbete!

**Literal:** Una tarde, Lucía paseaba por el parque con su abuelo. Junto a una fuente descubrió un pequeño barco rojo. El barco flotaba despacio entre las hojas. Lucía buscó una rama para acercarlo a la orilla. Su abuelo la ayudó y juntos sacaron el barco del agua. Después, regresaron a casa y lo colocaron sobre una estantería.

### Lectura con muchas trabadas - cuento 2 - lectura_02 - 23-10-2026.wav

Consigna/metadatos: Lectura con muchas trabadas - cuento 2 · 23/10/2026. Fragmentos y repeticiones durante el cuento, por ejemplo Una ta ta tarde, Lu, Lucía; lista literal completa pendiente de anotación. Estado de referencia: descripcion_de_eventos_confirmada_por_lector_transcripcion_literal_pendiente. Ambiente: El usuario no percibe ruido de fondo en esta grabación; no es una medición de SNR.

**Actual:**  Una tarde Lucía paseaba por el parque con su abuelo. Junto a una fuente descubrió un pequeño barco rojo.  el barco flotaba despacio entre las hojas, Lucía buscó una drama para acercarlo a la orilla,  su abuelo la ayudó y juntos sacaron el barco del agua, después regresaron a casa y lo colocaron  sobre una estantería.

**Literal:** U- u- una tarde lu- lucia pa- paseaba por el par- parque con su abuelo junto a una un- una fuente des- des- descu- descubrió un pe- pequeño barco rojo, el el barco el barco flotaba des- despacio en entre las hojas. Lu- Lucia buscó una r- rama para acercarlo a la ori- o- orilla. Su abuelo la la ayudó y y juntos sa- sacaron el barco del del agua. Des- después regres- regresaron a casa y lo y lo colocaron sobre una estantería.

### Lectura omisión abuelo - cuento 2 - lectura_02 - 23-10-2026.wav

Consigna/metadatos: Lectura omisión abuelo - cuento 2 · 23/10/2026. Omisión de las dos apariciones de abuelo, en con su abuelo y Su abuelo la ayudó. Estado de referencia: descripcion_de_eventos_confirmada_por_lector_transcripcion_literal_pendiente. Ambiente: El usuario no percibe ruido de fondo en esta grabación; no es una medición de SNR.

**Actual:**  Una tarde, Lucía paseaba por el parque Konsu. Junto a una fuente descubrió un pequeño barco rojo.  El barco flotaba despacio entre las hojas. Lucía buscó una rama para acercarlo a la orilla.  Su, la ayudó y juntos sacaron el barco del agua. Después regresaron a casa y lo colocaron sobre  una estantería.

**Literal:** Una tarde, Lucía paseaba por el parque Consu, junto a una fuente descubrió un pequeño barco rojo. El barco flotaba despacio entre las hojas. Lucía buscó una rama para acercarlo a la orilla. Suu la ayudó y juntos sacaron el barco del agua. Después regresaron a casa y lo colocaron sobre una estantería.

Revisión compartida en el visor local de solo lectura. Sin activar el motor en el seguidor ni publicar automáticamente.
