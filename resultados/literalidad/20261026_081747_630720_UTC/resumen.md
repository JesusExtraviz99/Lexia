# Reconocimiento completo del lote de audios propios

Selección exclusiva de grabaciones del cuento datos/textos/lectura_04.txt. Lote de desarrollo, una pasada por motor y WAV completo; un proceso por motor y modelo reutilizado secuencialmente. No se entregan cuento ni notas al ASR. Mismos arrays mono 16 kHz, sin VAD ni limpieza de ruido. Small CT2 CPU int8 frente a CrisperWhisper2.0 Small Transformers CPU float32 literal; cuatro hilos. Candidato >30 s: continuation, bloques 30 s/paso 26 s con contexto generado. Duración incluye silencio; no latencia en directo ni rendimiento de tablet. El seguimiento no cambia. Nombres/consignas y diferencias de texto no validan fidelidad ni permiten calcular tasas humanas. El audio externo no está descargado en el proyecto y no forma parte de este lote.

6 WAV completos; 670.00 s (11.17 min) por motor. Una pasada por archivo, sin nuevas voces ni repetición estadística.

| Audio | Duración (s) | Actual inferencia (s) | Literal inferencia (s) | RTF actual / literal | RAM máxima muestreada actual / literal (MiB) |
|---|---:|---:|---:|---|---|
| Lectura normal - caja del sendero - lectura_04 - 26-10-2026.wav | 90.00 | 15.45 | 25.95 | 0.172 / 0.288 | 945.6 / 4358.8 |
| Lectura repeticiones de palabras - caja del sendero - lectura_04 - 26-10-2026.wav | 100.00 | 12.39 | 25.20 | 0.124 / 0.252 | 945.7 / 4378.4 |
| Lectura intentos parciales - caja del sendero - lectura_04 - 26-10-2026.wav | 120.00 | 22.30 | 32.48 | 0.186 / 0.271 | 970.0 / 4297.8 |
| Lectura omisiones y sustituciones - caja del sendero - lectura_04 - 26-10-2026.wav | 90.00 | 14.04 | 24.19 | 0.156 / 0.269 | 796.5 / 4203.4 |
| Lectura pausa larga y continuacion - caja del sendero - lectura_04 - 26-10-2026.wav | 120.00 | 15.16 | 53.00 | 0.126 / 0.442 | 599.9 / 4779.6 |
| Lectura dificultades mixtas libres - caja del sendero - lectura_04 - 26-10-2026.wav | 150.00 | 19.81 | 52.64 | 0.132 / 0.351 | 965.3 / 4283.7 |

## Totales y alcance

| Motor | Inferencia total (s) | RTF ponderado por duración | Carga única (s) | Pico RAM de toda la vida del proceso (MiB) |
|---|---:|---:|---:|---:|
| baseline | 99.14 | 0.148 | 1.25 | 970.42 |
| candidato | 213.46 | 0.319 | 15.80 | 5057.56 |

Cada JSON contiene textos brutos, palabras automáticas, bloques nativos del candidato, CPU/RAM/GPU global, versiones y configuración. En cada audio se conserva el subintervalo de recursos del único muestreador. RAM por audio = máximo muestreado y extremos del intervalo, no pico independiente garantizado; el modelo se reutiliza y conserva memoria. Pico Windows = vida completa del proceso, incluida carga. CPU incluye instrumentación. GPU global no implica ejecución del ASR en GPU: ambos motores están en CPU. Energía propia del ASR/FLOPs/tablet no medidos.

RTF = inferencia / duración total, incluido silencio. No es retardo de captura/interfaz ni RTF sobre habla. Backends/precisiones distintos, orden fijo, una pasada: no hay comparación causal de entrenamiento, estabilidad térmica ni generalización. Los tiempos de palabra del candidato siguen sin validarse por las advertencias de compatibilidad conocidas.

## Transcripciones para revisión

Las notas son consignas y confirmaciones previas, no una referencia literal exhaustiva. Una palabra añadida respecto al otro motor puede ser recuperación real o inserción; decidir escuchando. No calcular WER literal, precisión/F1 ni intentos a partir del cuento pretendido o de transcripciones sin revisar. No sumar bloques internos como eventos separados.

### Lectura normal - caja del sendero - lectura_04 - 26-10-2026.wav

Consigna/metadatos: Lectura normal - caja del sendero · 26/10/2026. El lector confirma haber seguido la consigna: Lee todo el cuento una sola vez a tu ritmo habitual, sin introducir errores deliberados. Estado de referencia: descripcion_confirmada_por_lector_pendiente_escucha_detallada.

**Actual:**  Una mañana Mateo salió a caminar con su hermana Clara, junto al puente encontraron una pequeña caja de madera, dentro había una llave, una pluma azul y un papel doblado.  Clara abrió el papel y leyó, busca donde termina el sendero. Los dos siguieron despacio hasta un viejo molino.  Allí descubrieron una puerta escondida entre las plantas. Mateo probó la llave pero no consiguió  abrirla. Entonces Clara levantó una piedra y encontró otra entrada. Detrás había un jardín  lleno de flores. Antes de regresar dejaron la caja junto al puente para que alguien más pudiera  descubrir el secreto.  Este es el canal de subtítulos en español de la Iglesia de Jesucristo de los Santos de los Últimos días.

**Literal:** Una mañana Mateo salió a caminar con su hermana Clara. Junto al puente encontraron una pequeña caja de madera. Dentro había una llave, una pluma azul y un papel doblado. Clara abrió el papel y leyó, busca donde termina el sendero. Los dos siguieron despacio hasta un viejo molino. Allí descubrieron una puerta escondida entre las plantas. Mateo probó la llave, pero no consiguió abrirla, entonces Clara levantó una piedra y encontró otra entrada. Detrás había un jardín lleno de flores. Antes de regresar, dejaron la caja junto al puente para que alguien más pudiera descubrir el secreto.

### Lectura repeticiones de palabras - caja del sendero - lectura_04 - 26-10-2026.wav

Consigna/metadatos: Lectura repeticiones de palabras - caja del sendero · 26/10/2026. El lector confirma haber seguido la consigna: Lee todo el cuento. Introduce cuatro repeticiones: una una pequeña caja; Clara Clara abrió; Mateo Mateo probó; junto junto al puente (en la última frase). El resto se lee normalmente. Estado de referencia: descripcion_confirmada_por_lector_pendiente_escucha_detallada.

**Actual:**  Una mañana Mateo salió a caminar con su hermana Clara, junto al puente encontraron una pequeña caja de madera, dentro había una llave, una pluma azul y un papel doblado.  Clara abrió el papel y leyó, busca donde termina el sendero.  Los dos siguieron despacio hasta un viejo molino. Allí descubrieron una puerta escondida entre las  plantas. Mateo, Mateo probó la llave, pero no consiguió abrirla. Entonces Clara levantó  una piedra y encontró otra entrada. Detrás había un jardín lleno de flores.  Antes de regresar dejaron la caja junto, junto al puente para que alguien más pudiera descubrir el secreto.

**Literal:** Una mañana Mateo salió a caminar con su hermana Clara. Junto al puente encontraron una una pequeña caja de madera. Dentro había una llave, una pluma azul y un papel doblado. Clara Clara abrió el papel y leyó, busca donde termina el sendero. Los dos siguieron despacio hasta un viejo molino, allí descubrieron una puerta escondida entre las plantas. Mateo Mateo probó la llave, pero no consiguió abrirla. Entonces Clara levantó una piedra y encontró otra entrada. Detrás había un jardín lleno de flores. Antes de regresar, dejaron la caja junto junto al puente para que alguien más pudiera descubrir el secreto. ¿Para qué?

### Lectura intentos parciales - caja del sendero - lectura_04 - 26-10-2026.wav

Consigna/metadatos: Lectura intentos parciales - caja del sendero · 26/10/2026. El lector confirma haber seguido la consigna: Lee todo el cuento. En pequeña di pe- pe- pequeña; en descubrieron di des- des- descubrieron; en regresar di regres- re- regresar. Los guiones indican cortar la palabra, no decir guion. Deja salir los intentos sin corregirlos después. El resto se lee normalmente. Estado de referencia: descripcion_confirmada_por_lector_pendiente_escucha_detallada.

**Actual:**  Una mañana Mateo salió a caminar con su hermana Clara.  Junto al puente encontraron una pe, pe, pequeña caja de madera.  Dentro había una llave, una pluma azul y un papel doblado.  Clara abrió el papel y leyó, busca donde termina el sendero. Los dos siguieron despacio hasta un  viejo molino. Allí des, des, descubrieron una puerta escondida entre las plantas. Mateo probó  la llave, pero no consiguió abrirla. Entonces Clara levantó una piedra y encontró otra  entrada. Detrás había un jardín lleno de flores. Antes de regresar, dejaron la caja  junto al puente para que alguien más pudiera descubrir el secreto.

**Literal:** Una mañana Mateo salió a caminar con su hermana Clara. Junto al puente encontraron una pe- pe- pequeña caja de madera. Dentro había una llave, una pluma azul y un papel doblado. Clara abrió el papel y leyó:"Busca donde termina el sendero". Los dos siguieron despacio hasta un viejo molino. Allí des des descubrieron una puerta escondida entre las plantas. Mateo probó la llave, pero no consiguió abrirla. Entonces Clara levantó una piedra y encontró otra entrada. Detrás había un jardín lleno de flores. Antes de regresar, dejaron la caja junto al puente para que alguien más pudiera descubrir el secreto. ¿Para qué?

### Lectura omisiones y sustituciones - caja del sendero - lectura_04 - 26-10-2026.wav

Consigna/metadatos: Lectura omisiones y sustituciones - caja del sendero · 26/10/2026. El lector confirma haber seguido la consigna: Lee todo el cuento omitiendo madera y viejo. Sustituye pluma azul por pluma roja y un jardín por un parque. No añadas después las palabras omitidas ni corrijas las sustituciones. Estado de referencia: descripcion_confirmada_por_lector_pendiente_escucha_detallada.

**Actual:**  Una mañana Mateo salió a caminar con su hermana Clara. Junto al puente encontraron una pequeña caja de...  Dentro había una llave, una pluma roja y un papel doblado.  Clara abrió el papel y leyó, busca donde termina el sendero.  Los dos siguieron despacio hasta un molino. Allí descubrieron una puerta escondida entre  las plantas. Mateo probó la llave, pero no consiguió abrirla. Entonces Clara levantó  una piedra y encontró otra entrada. Detrás había un parque lleno de flores. Antes de  dejaron la caja junto al puente para que alguien más pudiera descubrir el secreto.

**Literal:** Una mañana Mateo salió a caminar con su hermana Clara, junto al puente, encontraron una pequeña caja de dentro había una llave, una pluma roja y un papel doblado. Clara abrió el papel y leyó:"Busca donde termina el sendero". Los dos siguieron despacio hasta un molino. Allí descubrieron una puerta escondida entre las plantas. Mateo probó la llave, pero no consiguió abrirla. Entonces Clara levantó una piedra y encontró otra entrada. Detrás había un parque lleno de flores. Antes de regresar, dejaron la caja junto al puente para que alguien más pudiera descubrir el secreto.

### Lectura pausa larga y continuacion - caja del sendero - lectura_04 - 26-10-2026.wav

Consigna/metadatos: Lectura pausa larga y continuacion - caja del sendero · 26/10/2026. El lector confirma haber seguido la consigna: Lee hasta y un papel doblado. Haz una pausa aproximada de 8 segundos sin hablar, continúa por Clara abrió el papel y termina el cuento una sola vez. No repitas la frase anterior. Estado de referencia: descripcion_confirmada_por_lector_pendiente_escucha_detallada.

**Actual:**  Una mañana Mateo salió a caminar con su hermana Clara.  Junto al puente encontraron una pequeña caja de madera.  Dentro había una llave, una pluma azul y un papel doblado.  Clara abrió el papel y leyó, busca donde termina el sendero. Los dos siguieron despacio hasta un viejo molino.  Allí descubrieron una puerta escondida entre las plantas. Mateo probó la llave, pero no consiguió abrirla.  Entonces Clara levantó una piedra y encontró otra entrada.  Detrás había un jardín lleno de flores.  Antes de regresar dejaron la caja junto al puente  para que alguien más pudiera descubrir el secreto.

**Literal:** Una mañana Mateo salió a caminar con su hermana Clara. Junto al puente, encontraron una pequeña caja de madera. Dentro había una llave, una pluma azul y un papel doblado. Clara abrió el papel y leyó, busca donde termina el sendero. Los dos siguieron despacio hasta un viejo molino. Allí descubrieron una puerta escondida entre las plantas. Mateo probó la llave, pero no consiguió abrirla. Entonces Clara levantó una piedra y encontró otra entrada. Detrás había un jardín lleno de flores. Antes de regresar, dejaron la caja junto al puente para que alguien más pudiera descubrir el secreto. P- p. P- p.

### Lectura dificultades mixtas libres - caja del sendero - lectura_04 - 26-10-2026.wav

Consigna/metadatos: Lectura dificultades mixtas libres - caja del sendero · 26/10/2026. El lector describe confusiones/autocorrecciones, recuerda descubrieron y luego encontraron una caja..., otra autocorrección no recordada, repeticiones parciales y cambios lentos/rápidos. Secuencia literal completa pendiente de escucha. Estado de referencia: descripcion_confirmada_por_lector_pendiente_escucha_detallada.

**Actual:**  Una mañana ma mateo salió a caminar con su hermana clara.  Junto al puente descubrieron encontraron una pequeña caja de madera.  dentro había una llave, una pluma azul y un papel doblado. Clara abrió el papel y le  yo, buscan donde termina el sendero, los dos siguieron despacio hasta un viejo molino. Allí  y descubrí, descubrieron una puerta escondida entre las plantas.  Mateo probó la llave, pero no con...  Consiguió abrirla.  Entonces Clara levantó una piedra y encontró otra entrada.  Detrás había un jardín lleno de flores.  Antes de regresar dejaron la caja  junto al puente para que alguien más pudiera descubrir el secreto.  y  y

**Literal:** [yawn] Una mañana, ma- ma- Mateo salió a caminar con su her- her- hermana Clara. Junto al puente descubrieron encontraron una pequeña caja de madera. Dentro había una llave, una una pluma azul y un papel doblado. Clara abrió el papel y leyó, busca donde termina el sendero, los dos siguieron despacio hasta un viejo molino. Allí des- descubrí des- descubrí descubrieron una puerta escondida entre las plantas. Mateo probó la llave, pero no con consiguió abrirla. Entonces Clara Levam le- Levam levantó una piedra y encontró otra entrada detrás había un jardín lleno de flores, antes de regresar dejaron la ca- la casa la- la caja junto al puente para que alguien más pudiera descubrir el secreto. P- por favor, si te da la pena, por favor, si te da la pena, por favor, si te da la pena, ¿?

Revisión compartida en el visor local de solo lectura. Sin activar el motor en el seguidor ni publicar automáticamente.
