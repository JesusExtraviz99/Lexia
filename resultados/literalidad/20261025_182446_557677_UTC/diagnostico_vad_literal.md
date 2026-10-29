# Diagnóstico de voz antes de nuevas transcripciones

Inferencia VAD nueva sobre los 17 arrays originales; no es ASR nuevo. Intervalos VAD con margen, no referencia humana ni detector perfecto. No se recorta, concatena, cambia la duración ni filtra ninguna salida. La cobertura de anclas solo comprueba límites ya anotados; no valida todas las sílabas/trabadas. Parámetros iniciales, no óptimos.

17 WAV; inferencia VAD total 1.68 s; carga 0.24 s. CPU, memoria y GPU global disponibles en el JSON; ASR no ejecutado.

Anclas humanas completamente cubiertas por intervalos VAD con margen: 75/75. Esto no equivale a sensibilidad global ni valida fragmentos sin tiempos humanos.

| Audio | Último final VAD con margen (s) | Último bloque del candidato | Solapamiento VAD en ese bloque (s) |
|---|---:|---|---:|
| 1 · Lectura normal - cuento 1 - 14-10-2026.wav | 23.312 | 26.0–40.0 | 0.000 |
| 2 · Lectura con disfluencias (Ana repetida, sin despacio, mari-mariposa) - cuento 1 - 14-10-2026.wav | 24.336 | 0–30.0 | 23.040 |
| 3 · Lectura con pausa (flor-Ana) - cuento 1 - 14-10-2026.wav | 31.376 | 52.0–60.0 | 0.000 |
| 4 · Lectura lenta - cuento 1 - 16-10-2026.wav | 77.68 | 78.0–90.0 | 0.000 |
| 5 · Lectura con relectura (Los dos se quedaron en silencio) - cuento 1 - 16-10-2026.wav | 29.68 | 52.0–60.0 | 0.000 |
| 6 · Lectura con relectura lejana (Los dos-alas) - cuento 1 - 21-10-2026.wav | 33.136 | 52.0–60.0 | 0.000 |
| 7 · Lectura normal con lluvia - cuento 1 - 21-10-2026.wav | 26.864 | 26.0–40.0 | 0.864 |
| 8 · Lectura con relectura lejana (Cerca-azul) - cuento 1 - 21-10-2026.wav | 34.672 | 26.0–45.0 | 8.672 |
| 9 · Lectura normal con lluvia - cuento 2 - 21-10-2026.wav | 26.352 | 26.0–40.0 | 0.352 |
| 10 · Lectura con relectura lejana (Junto-rojo) - cuento 2 - 21-10-2026.wav | 40.272 | 26.0–45.0 | 11.680 |
| 11 · Lectura lenta - cuento 2 - lectura_02 - 23-10-2026.wav | 66.8 | 78.0–90.0 | 0.000 |
| 12 · Lectura rápida - cuento 2 - lectura_02 - 23-10-2026.wav | 16.144 | 0–30.0 | 15.776 |
| 13 · Lectura pausa con relectura barco rojo - el barco - cuento 2 - lectura_02 - 23-10-2026.wav | 41.776 | 26.0–50.0 | 15.776 |
| 14 · Lectura sustitución rojo por azul - cuento 2 - lectura_02 - 23-10-2026.wav | 28.24 | 26.0–50.0 | 2.240 |
| 15 · Lectura con ruido de fondo - cuento 2 - lectura_02 - 23-10-2026.wav | 27.92 | 26.0–50.0 | 1.920 |
| 16 · Lectura con muchas trabadas - cuento 2 - lectura_02 - 23-10-2026.wav | 56.528 | 52.0–60.0 | 4.528 |
| 17 · Lectura omisión abuelo - cuento 2 - lectura_02 - 23-10-2026.wav | 27.632 | 26.0–40.0 | 1.632 |

No se han descartado esos bloques ni evaluado una transcripción corregida. Un resultado sin solapamiento VAD es una propuesta de zona sin voz; suprimirla puede perder habla débil o fragmentos. El siguiente ensayo debe conservar originales, márgenes y mapa temporal, y medir tanto texto añadido como habla omitida. Las pausas originales permanecen disponibles para las estadísticas.

Control inicial: threshold 0,5; no descartar segmentos detectados por duración mínima; separación tras 2 s y margen 400 ms. Modelo Silero v6 de faster-whisper ya instalado. No son umbrales ideales demostrados.
