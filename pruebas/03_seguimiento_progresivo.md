# Prueba 03: seguimiento progresivo local

Estado: comprobaciones del desarrollador y prueba del usuario completadas. El usuario autoriza guardar esta versión en GitHub antes de comparar ventanas de reprocesamiento.

## Método

- Se decodifica el WAV local y se entrega al modelo un prefijo acumulado, recortado cada 2 s. El ASR no recibe audio posterior al corte.
- Whisper small, CPU int8, beam_size=5, detección de voz activa. Esta configuración no es idéntica a la primera transcripción sin VAD.
- Alineamiento de las últimas 8 palabras contra una ventana próxima a la posición anterior. Los umbrales son experimentales.
- Posición base 1: última palabra del cuento apoyada por coincidencia textual. No se estima aún la palabra pronunciada en cada instante.
- Se permiten retrocesos al cambiar la hipótesis. Una búsqueda global de recuperación requiere confirmación. El avance no implica lectura correcta.
- Registro de cada hipótesis, movimiento, evidencia, procesamiento y cola secuencial simulada. No se utiliza el JSON definitivo para fabricar las hipótesis intermedias.

## Segunda grabación: desviaciones deliberadas

Audio: `datos/audio/lectura_20261014_082953_219058.wav`.
Primer registro: `resultados/seguimiento/lectura_20261014_082953_219058_20261014_090237_718476_seguimiento.json`.

- 15 actualizaciones sobre 30 s de audio; llega al índice 56, cuaderno.
- Hasta 4 s: hipótesis Una mañana Ana Ana, posición 3.
- Hasta 12 s: posición 27, flor, tras la omisión de despacio.
- Hasta 18 s: posición 44, sus, tras la salida cinesio.
- Hasta 22 s: aparece provisionalmente Hola Madi; conserva la posición 51, dibujaron.
- Hasta 24 s: se revisa a la mariposa en un cuaderno y alcanza la posición 56.
- Se mantiene al final durante las últimas actualizaciones.

No se ha medido precisión temporal con anotaciones humanas. Llegar al final no demuestra que las posiciones intermedias sean correctas. La prueba no representa evaluación infantil.

## Coste observado

La primera grabación normal también se procesó completa (40 s, 20 actualizaciones): alcanza cuaderno al corte de 24 s y conserva la posición hasta el final. Su registro está en resultados/seguimiento con el prefijo lectura_20261014_081816_009646.

En esta ejecución, las inferencias sumaron aproximadamente 52,16 s para 30 s de audio. La disponibilidad final bajo procesamiento secuencial simulado sería aproximadamente 54,60 s desde el inicio del audio, excluyendo carga del modelo y otras etapas. Esta versión acumularía retraso en directo.

El reprocesamiento de prefijos crecientes es deliberadamente sencillo para estudiar revisiones del ASR. Antes del micrófono será necesario comparar ventanas acústicas limitadas con solapamiento, tamaños de bloque y modelos/configuraciones, conservando la continuidad del texto. No extrapolar estos tiempos a streaming nativo ni a un modelo sobre GPU.

## Comprobaciones

Diez pruebas automáticas en total: cinco del alineador posterior y cinco del seguidor. Incluyen omisiones, sustituciones, repeticiones, retrocesos, palabras iguales en varias posiciones y un ejemplo de habla ajena al cuento. Son comprobaciones de lógica, no una validación de robustez general.

El usuario ejecutó scripts/seguir.py y compartió el registro lectura_20261014_082953_219058_20261014_090803_312561_seguimiento. Confirma la revisión de Los dos secu a Los dos se quedaron entre los cortes de 16 y 18 s. El seguidor pasa de la posición 38 (dos) a 44 (sus), y termina en 56 (cuaderno). Se mantienen las hipótesis originales para estudiar esas revisiones.

Pendiente: comparar prefijos acumulados con ventanas acústicas limitadas y solapadas sobre los mismos audios. Los futuros cambios se probarán localmente y se subirán únicamente tras confirmación del usuario.
