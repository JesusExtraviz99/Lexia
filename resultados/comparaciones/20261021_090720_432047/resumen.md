# Comparación de reprocesamiento

3 ronda(s) por configuración, orden aleatorio reproducible por ronda. Ejecución secuencial para no competir por CPU. Tiempos orientativos, afectados por carga y calentamiento. No hay referencia humana de posición ni latencia visual. Comparar posiciones entre métodos no demuestra precisión.

Mismo modelo, CPU int8, VAD, bloques de 2 s, cuento y seguidor. La carga del modelo se excluye de los tiempos de inferencia. Solapamiento = ventana menos 2 s; no aplica al prefijo. El silencio final puede reducir los totales de las ventanas.

| Audio | Método | Ronda | Total inferencia (s) | Mediana (s) | P95 (s) | Inferencias >2 s | Cola máxima simulada (s) | Posición final | Retrocesos |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| lectura_20261021_090304_259866.wav | ventana_8s | 1 | 36.52 | 1.62 | 2.87 | 2 | 1.36 | 45 | 1 |
| lectura_20261021_090304_259866.wav | ventana_4s | 1 | 30.03 | 1.60 | 1.76 | 0 | 0.00 | 56 | 0 |
| lectura_20261021_090304_259866.wav | ventana_8s | 2 | 37.02 | 1.66 | 2.07 | 3 | 1.37 | 45 | 1 |
| lectura_20261021_090304_259866.wav | ventana_4s | 2 | 29.17 | 1.54 | 1.71 | 0 | 0.00 | 56 | 0 |
| lectura_20261021_090304_259866.wav | ventana_4s | 3 | 28.94 | 1.55 | 1.66 | 0 | 0.00 | 56 | 0 |
| lectura_20261021_090304_259866.wav | ventana_8s | 3 | 36.17 | 1.66 | 1.83 | 1 | 1.26 | 45 | 1 |

## Posiciones en cada actualización

Comparación descriptiva con el prefijo, no referencia de precisión. El prefijo también puede equivocarse.

### lectura_20261021_090304_259866.wav, ronda 1

| Audio disponible (s) | ventana_4s | ventana_8s |
|---:|---:|---:|
| 2.0 | 2 | 2 |
| 4.0 | 8 | 8 |
| 6.0 | 11 | 11 |
| 8.0 | 16 | 16 |
| 10.0 | 20 | 20 |
| 12.0 | 25 | 25 |
| 14.0 | 28 | 28 |
| 16.0 | 35 | 35 |
| 18.0 | 38 | 38 |
| 20.0 | 43 | 43 |
| 22.0 | 46 | 46 |
| 24.0 | 52 | 52 |
| 26.0 | 56 | 56 |
| 28.0 | 56 | 56 |
| 30.0 | 56 | 56 |
| 32.0 | 56 | 56 |
| 34.0 | 56 | 56 |
| 36.0 | 56 | 56 |
| 38.0 | 56 | 45 |
| 40.0 | 56 | 45 |
| 42.0 | 56 | 45 |
| 44.0 | 56 | 45 |
| 46.0 | 56 | 45 |
| 48.0 | 56 | 45 |
| 50.0 | 56 | 45 |
| 52.0 | 56 | 45 |
| 54.0 | 56 | 45 |
| 56.0 | 56 | 45 |
| 58.0 | 56 | 45 |
| 60.0 | 56 | 45 |

### lectura_20261021_090304_259866.wav, ronda 2

| Audio disponible (s) | ventana_4s | ventana_8s |
|---:|---:|---:|
| 2.0 | 2 | 2 |
| 4.0 | 8 | 8 |
| 6.0 | 11 | 11 |
| 8.0 | 16 | 16 |
| 10.0 | 20 | 20 |
| 12.0 | 25 | 25 |
| 14.0 | 28 | 28 |
| 16.0 | 35 | 35 |
| 18.0 | 38 | 38 |
| 20.0 | 43 | 43 |
| 22.0 | 46 | 46 |
| 24.0 | 52 | 52 |
| 26.0 | 56 | 56 |
| 28.0 | 56 | 56 |
| 30.0 | 56 | 56 |
| 32.0 | 56 | 56 |
| 34.0 | 56 | 56 |
| 36.0 | 56 | 56 |
| 38.0 | 56 | 45 |
| 40.0 | 56 | 45 |
| 42.0 | 56 | 45 |
| 44.0 | 56 | 45 |
| 46.0 | 56 | 45 |
| 48.0 | 56 | 45 |
| 50.0 | 56 | 45 |
| 52.0 | 56 | 45 |
| 54.0 | 56 | 45 |
| 56.0 | 56 | 45 |
| 58.0 | 56 | 45 |
| 60.0 | 56 | 45 |

### lectura_20261021_090304_259866.wav, ronda 3

| Audio disponible (s) | ventana_4s | ventana_8s |
|---:|---:|---:|
| 2.0 | 2 | 2 |
| 4.0 | 8 | 8 |
| 6.0 | 11 | 11 |
| 8.0 | 16 | 16 |
| 10.0 | 20 | 20 |
| 12.0 | 25 | 25 |
| 14.0 | 28 | 28 |
| 16.0 | 35 | 35 |
| 18.0 | 38 | 38 |
| 20.0 | 43 | 43 |
| 22.0 | 46 | 46 |
| 24.0 | 52 | 52 |
| 26.0 | 56 | 56 |
| 28.0 | 56 | 56 |
| 30.0 | 56 | 56 |
| 32.0 | 56 | 56 |
| 34.0 | 56 | 56 |
| 36.0 | 56 | 56 |
| 38.0 | 56 | 45 |
| 40.0 | 56 | 45 |
| 42.0 | 56 | 45 |
| 44.0 | 56 | 45 |
| 46.0 | 56 | 45 |
| 48.0 | 56 | 45 |
| 50.0 | 56 | 45 |
| 52.0 | 56 | 45 |
| 54.0 | 56 | 45 |
| 56.0 | 56 | 45 |
| 58.0 | 56 | 45 |
| 60.0 | 56 | 45 |

## Resumen por configuración

| Audio | Método | Total medio (s) | Rango de totales (s) | Cola máxima media (s) | Inferencias >2 s | Posiciones finales |
|---|---|---:|---|---:|---|---|
| lectura_20261021_090304_259866.wav | ventana_4s | 29.38 | 28.94–30.03 | 0.00 | 0/90 | [56, 56, 56] |
| lectura_20261021_090304_259866.wav | ventana_8s | 36.57 | 36.17–37.02 | 1.33 | 6/90 | [45, 45, 45] |
