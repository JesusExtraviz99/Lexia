# Evaluación temporal de la lectura normal

Pregunta: ¿qué desfase presenta el seguimiento de 4, 6 y 8 segundos frente a los tiempos revisados por el lector?

Referencia: datos/anotaciones/lectura_normal.json, 56 palabras revisadas, audio original de 40 segundos. Nueve notas advierten de límites difíciles de separar. Es una referencia de desarrollo asistida inicialmente por ASR y revisada por el propio lector; no constituye una anotación independiente.

Configuración: mismo modelo small, CPU int8, VAD activado, bloques de 2 segundos, sin cambiar el seguidor. Tres rondas secuenciales en orden aleatorio reproducible. Las rondas repiten el mismo audio: describen variación de cómputo, no diversidad de lectura.

```powershell
.\.venv\Scripts\python.exe -u scripts\comparar_ventanas.py datos\audio\lectura_20261014_081816_009646.wav --ventanas 4 6 8 --repeticiones 3
.\.venv\Scripts\python.exe -m scripts.evaluar_seguimiento resultados/comparaciones/CARPETA_GENERADA
```

Convenciones:

- Referencia en un instante: última palabra cuyo final anotado ya ha pasado. Durante una palabra aún incompleta se mantiene la anterior; antes de terminar la primera, posición cero.
- Error firmado: estimación menos referencia; negativo indica retraso y positivo adelanto respecto a esta convención.
- Hipótesis al corte: posición producida con el audio hasta ese corte, sin incluir el tiempo que tarda en obtenerse.
- Visible simulado en ese mismo corte: última salida cuyo procesamiento ya ha terminado según el modelo de cola secuencial. Antes de la primera salida la posición es cero. No se incluyen carga inicial del modelo, transferencia ni pantalla.
- Medias calculadas únicamente en cortes de 2 segundos dentro del intervalo entre inicio de la primera palabra y final de la última. Se conserva todo el seguimiento, pero el silencio final no reduce las medias de error.
- Demora final simulada: instante en que está lista la primera salida con posición 56 menos el final humano de cuaderno. Incluye la espera hasta el siguiente corte y la cola; no es tiempo de inferencia aislado ni latencia medida en una interfaz.

El informe conserva los cortes individuales, cobertura, medias de error absoluto y firmado, máximo absoluto, coincidencias exactas y muestras a una palabra de distancia. No exige coincidencia perfecta en fronteras ambiguas ni evalúa pronunciación. Esta primera versión no admite referencias parciales, intentos repetidos ni saltos del cuento: deberán representarse explícitamente antes de evaluar esos casos.

Próxima decisión: valorar conjuntamente desfase y coste de cómputo antes de elegir una configuración provisional. Posteriormente revisar fragmentos clave de pausa, lectura lenta y relectura; no modificar varias ayudas de audio simultáneamente.
