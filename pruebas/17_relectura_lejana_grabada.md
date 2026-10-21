# Propuesta de contraste con una relectura lejana grabada

Protocolo: 19/10/2026. Actualización: 21/10/2026. Grabación y ejecución ASR recibidas; comparación experimental pendiente de revisión compartida y referencia humana.

## Pregunta

¿La recuperación exacta anticipada vuelve a localizar una frase anterior tras terminar el cuento, usando hipótesis producidas por ASR real y conservando la protección frente a revisiones de audio antiguo?

La comprobación del usuario de resultados/recuperacion/20261019_120351_062213 reproduce la mejora sintética y cero cambios frente a la combinación en los 36 registros existentes. La nueva vía no se activa en esos registros: por eso se requiere un caso positivo grabado, no otra repetición del mismo control sintético.

## Grabación por el usuario

```powershell
.\.venv\Scripts\python.exe scripts\grabar.py --segundos 60
```

El programa muestra el cuento y espera Enter antes de activar la grabación. Mantener micrófono y entorno actual. Leer el cuento completo a ritmo normal hasta cuaderno. Hacer una pausa aproximada de dos segundos y volver a leer solamente:

> Los dos se quedaron en silencio, mirando sus alas.

En esta segunda lectura pronunciar las palabras despacio, aproximadamente una palabra por segundo, sin necesidad de cronometrarlas. Terminar en alas y no continuar con Después. No añadir comentarios hablados para anunciar la vuelta atrás. Guardar silencio hasta que termine la grabación. La pausa aproximada es una instrucción de realización, no una anotación temporal exacta.

Tras la segunda lectura, la posición esperada del cuento es 45 (alas), no 56 (cuaderno). El salto vuelve a 37 desde una lectura que llegó a 56, alejándose del contexto local más que en la relectura corta anterior. El ritmo lento de la segunda lectura busca que la frase tenga tiempo de ocupar ventanas propias; no garantiza que el ASR produzca coincidencias exactas.

## Análisis previsto, después de recibir la ruta

1. Identificar el WAV concreto mediante la ruta Guardado; no seleccionar a ciegas el último audio. Revisar escucha y contenido literal antes de declarar referencia.
2. Obtener hipótesis con la configuración anterior, ventanas 4/8 s, bloques 2 s y tres rondas. Las rondas son repeticiones de cómputo sobre una sola grabación.
3. Reproducir las mismas hipótesis con original, combinación y recuperación exacta. No modificar los parámetros de la regla para obtener un resultado favorable antes de registrar la primera comparación.
4. Si hacen falta marcas humanas, revisar solo el cuaderno del primer final y el intervalo de la frase releída, conservando rango del cuento 37–45 e intento. No interpolar tiempos de las nueve palabras internas ni exigir anotación completa del cuento.
5. Registrar si la nueva vía se activa, el candidato, respaldo temporal, coincidencia exacta/unicidad, recuperación del tramo y posición tras terminar en alas. Distinguir corte de audio e instante de salida lista simulado.

Si la regla no se activa, distinguir ausencia de frase exacta en ASR, ambigüedad, tiempos no posteriores, acierto local o descarte por texto idéntico. No atribuir automáticamente el fallo al lector ni declararlo solucionado a partir de una posición final aislada. Si todas las versiones recuperan igual, el caso no demuestra una ventaja de la nueva regla.

El caso sigue siendo desarrollo con un adulto y el mismo cuento/entorno; no valida generalización ni sustituye otras voces o entornos posteriores. No se activa aún ninguna variante en el seguidor habitual y no se publica este trabajo sin petición del usuario.

## Primera ejecución y comprobación compartida

Audio: datos/audio/lectura_20261021_090304_259866.wav. El usuario comparte resultados/comparaciones/20261021_090720_432047. Para comparar los tres seguidores sin nuevas inferencias:

```powershell
.\.venv\Scripts\python.exe -m scripts.comparar_relectura_lejana resultados/comparaciones/20261021_090720_432047
```

La ejecución local resultados/relectura_lejana/20261021_091237_442232 reproduce los seis registros originales. En 4 s, original y combinación terminan en 56; la nueva regla vuelve a 43 en el corte 32 y llega a 45 en 34. En 8 s, las tres versiones terminan en 45, pero la nueva recupera en 34 frente a 38. Se repite en las tres rondas. Son cortes de audio, no tiempos humanos anotados ni latencia medida. No se han ajustado reglas. El usuario ejecuta el comparador: resultados/relectura_lejana/20261021_091515_954571. Sus seis registros coinciden íntegramente con los del asistente (posiciones, modos y evidencias). Pendiente de confirmar el contenido por escucha y revisar las anclas necesarias.

## Contraste con anclas humanas revisadas

El usuario confirma contenido y revisa tres anclas: cuaderno 24,65–25,48 s; Los de la relectura 29,16–29,43; alas final 32,17–32,73. No se anotan las palabras interiores. Comprobación para repetir:

```powershell
.\.venv\Scripts\python.exe -m scripts.evaluar_relectura_lejana resultados/relectura_lejana/20261021_091515_954571
```

Demora desde el final humano de alas hasta salida lista simulada: nueva 4 s, 2,87–2,92 s; nueva 8 s, 2,96–3,16 s; original/combinación 8 s, 6,82–6,90 s. Original/combinación 4 s sin recuperación. Tiempos ASR y cola reutilizados, sin pantalla ni coste adicional de las variantes. Evaluador ejecutado por asistente y usuario: las 18 filas y las demoras coinciden. Revisión compartida completada, sin activar variantes ni publicar.
