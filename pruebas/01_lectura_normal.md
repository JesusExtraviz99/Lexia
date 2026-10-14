# Prueba 01: lectura adulta normal

Audio: `datos/audio/lectura_20261014_081816_009646.wav`.
Resultados: los JSON con ese prefijo en `resultados/`.

- El sistema graba y transcribe un archivo WAV real.
- La salida coincide con las palabras del texto esperado, salvo puntuación.
- Ejecución comunicada por el lector: 3,99 s de procesamiento y 0,87 s de carga.
- Referencia inicial: cuento y salida mostrada por el lector; no hay anotación temporal humana.
- Es una prueba adulta de depuración, no una validación de lectura infantil ni de seguimiento en directo.

Antes de esta ejecución se corrigió la incompatibilidad de apertura de WAV entre faster-whisper 1.2.1 y PyAV 19.0.1, fijando PyAV 16.0.1.
