# Diagnóstico de voz antes de nuevas transcripciones

Inferencia VAD nueva sobre los arrays originales del lote; no es ASR nuevo. Intervalos VAD con margen, no referencia humana ni detector perfecto. No se recorta, concatena, cambia la duración ni filtra ninguna salida. La cobertura de anclas solo comprueba límites ya anotados; no valida todas las sílabas/trabadas. Parámetros iniciales, no óptimos.

6 WAV; inferencia VAD total 1.26 s; carga 0.26 s. CPU, memoria y GPU global disponibles en el JSON; ASR no ejecutado.

Anclas humanas completamente cubiertas por intervalos VAD con margen: 0/0. Esto no equivale a sensibilidad global ni valida fragmentos sin tiempos humanos.

| Audio | Último final VAD con margen (s) | Último bloque del candidato | Solapamiento VAD en ese bloque (s) |
|---|---:|---|---:|
| 1 · Lectura normal - caja del sendero - lectura_04 - 26-10-2026.wav | 52.592 | 78.0–90.0 | 0.000 |
| 2 · Lectura repeticiones de palabras - caja del sendero - lectura_04 - 26-10-2026.wav | 65.84 | 78.0–100.0 | 0.000 |
| 3 · Lectura intentos parciales - caja del sendero - lectura_04 - 26-10-2026.wav | 70.32 | 104.0–120.0 | 0.000 |
| 4 · Lectura omisiones y sustituciones - caja del sendero - lectura_04 - 26-10-2026.wav | 59.984 | 78.0–90.0 | 0.000 |
| 5 · Lectura pausa larga y continuacion - caja del sendero - lectura_04 - 26-10-2026.wav | 72.112 | 104.0–120.0 | 0.000 |
| 6 · Lectura dificultades mixtas libres - caja del sendero - lectura_04 - 26-10-2026.wav | 98.16 | 130.0–150.0 | 0.000 |

No se han descartado esos bloques ni evaluado una transcripción corregida. Un resultado sin solapamiento VAD es una propuesta de zona sin voz; suprimirla puede perder habla débil o fragmentos. El siguiente ensayo debe conservar originales, márgenes y mapa temporal, y medir tanto texto añadido como habla omitida. Las pausas originales permanecen disponibles para las estadísticas.

Control inicial: threshold 0,5; no descartar segmentos detectados por duración mínima; separación tras 2 s y margen 400 ms. Modelo Silero v6 de faster-whisper ya instalado. No son umbrales ideales demostrados.
