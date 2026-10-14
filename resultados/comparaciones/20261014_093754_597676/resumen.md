# Comparación de reprocesamiento

2 ronda(s) por configuración, orden aleatorio reproducible por ronda. Ejecución secuencial para no competir por CPU. Tiempos orientativos, afectados por carga y calentamiento. No hay referencia humana de posición ni latencia visual. Comparar posiciones entre métodos no demuestra precisión.

Mismo modelo, CPU int8, VAD, bloques de 2 s, cuento y seguidor. La carga del modelo se excluye de los tiempos de inferencia. Solapamiento = ventana menos 2 s; no aplica al prefijo. El silencio final puede reducir los totales de las ventanas.

| Audio | Método | Ronda | Total inferencia (s) | Mediana (s) | P95 (s) | Inferencias >2 s | Cola máxima simulada (s) | Posición final | Retrocesos |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| lectura_20261014_082953_219058.wav | ventana_8s | 1 | 26.17 | 1.78 | 1.99 | 0 | 0.00 | 56 | 0 |
| lectura_20261014_082953_219058.wav | prefijo | 1 | 44.47 | 2.47 | 4.79 | 10 | 13.12 | 56 | 0 |
| lectura_20261014_082953_219058.wav | ventana_6s | 1 | 28.90 | 2.04 | 2.40 | 10 | 1.52 | 56 | 0 |
| lectura_20261014_082953_219058.wav | ventana_4s | 1 | 25.99 | 1.99 | 2.19 | 7 | 0.70 | 56 | 0 |
| lectura_20261014_082953_219058.wav | ventana_10s | 1 | 28.83 | 1.93 | 2.16 | 6 | 0.52 | 56 | 0 |
| lectura_20261014_082953_219058.wav | ventana_12s | 1 | 30.39 | 2.00 | 2.28 | 7 | 1.45 | 56 | 0 |
| lectura_20261014_082953_219058.wav | prefijo | 2 | 44.31 | 2.54 | 4.46 | 10 | 13.06 | 56 | 0 |
| lectura_20261014_082953_219058.wav | ventana_4s | 2 | 22.61 | 1.71 | 1.87 | 0 | 0.00 | 56 | 0 |
| lectura_20261014_082953_219058.wav | ventana_12s | 2 | 29.67 | 1.96 | 2.27 | 7 | 1.21 | 56 | 0 |
| lectura_20261014_082953_219058.wav | ventana_6s | 2 | 24.93 | 1.78 | 1.89 | 0 | 0.00 | 56 | 0 |
| lectura_20261014_082953_219058.wav | ventana_10s | 2 | 28.92 | 1.95 | 2.14 | 6 | 0.46 | 56 | 0 |
| lectura_20261014_082953_219058.wav | ventana_8s | 2 | 27.63 | 1.86 | 2.04 | 2 | 0.04 | 56 | 0 |

## Posiciones en cada actualización

Comparación descriptiva con el prefijo, no referencia de precisión. El prefijo también puede equivocarse.

### lectura_20261014_082953_219058.wav, ronda 1

| Audio disponible (s) | prefijo | ventana_4s | ventana_6s | ventana_8s | ventana_10s | ventana_12s |
|---:|---:|---:|---:|---:|---:|---:|
| 2.0 | — | — | — | — | — | — |
| 4.0 | 3 | 3 | 3 | 3 | 3 | 3 |
| 6.0 | 9 | 9 | 9 | 9 | 9 | 9 |
| 8.0 | 16 | 16 | 16 | 16 | 16 | 16 |
| 10.0 | 20 | 20 | 20 | 20 | 20 | 20 |
| 12.0 | 27 | 27 | 27 | 27 | 27 | 27 |
| 14.0 | 35 | 35 | 35 | 35 | 35 | 35 |
| 16.0 | 38 | 39 | 39 | 39 | 39 | 38 |
| 18.0 | 44 | 44 | 44 | 44 | 44 | 44 |
| 20.0 | 48 | 48 | 48 | 48 | 48 | 48 |
| 22.0 | 51 | 52 | 52 | 52 | 52 | 52 |
| 24.0 | 56 | 56 | 56 | 56 | 56 | 56 |
| 26.0 | 56 | 56 | 56 | 56 | 56 | 56 |
| 28.0 | 56 | 56 | 56 | 56 | 56 | 56 |
| 30.0 | 56 | 56 | 56 | 56 | 56 | 56 |

### lectura_20261014_082953_219058.wav, ronda 2

| Audio disponible (s) | prefijo | ventana_4s | ventana_6s | ventana_8s | ventana_10s | ventana_12s |
|---:|---:|---:|---:|---:|---:|---:|
| 2.0 | — | — | — | — | — | — |
| 4.0 | 3 | 3 | 3 | 3 | 3 | 3 |
| 6.0 | 9 | 9 | 9 | 9 | 9 | 9 |
| 8.0 | 16 | 16 | 16 | 16 | 16 | 16 |
| 10.0 | 20 | 20 | 20 | 20 | 20 | 20 |
| 12.0 | 27 | 27 | 27 | 27 | 27 | 27 |
| 14.0 | 35 | 35 | 35 | 35 | 35 | 35 |
| 16.0 | 38 | 39 | 39 | 39 | 39 | 38 |
| 18.0 | 44 | 44 | 44 | 44 | 44 | 44 |
| 20.0 | 48 | 48 | 48 | 48 | 48 | 48 |
| 22.0 | 51 | 52 | 52 | 52 | 52 | 52 |
| 24.0 | 56 | 56 | 56 | 56 | 56 | 56 |
| 26.0 | 56 | 56 | 56 | 56 | 56 | 56 |
| 28.0 | 56 | 56 | 56 | 56 | 56 | 56 |
| 30.0 | 56 | 56 | 56 | 56 | 56 | 56 |

## Resumen por configuración

| Audio | Método | Total medio (s) | Rango de totales (s) | Cola máxima media (s) | Inferencias >2 s | Posiciones finales |
|---|---|---:|---|---:|---|---|
| lectura_20261014_082953_219058.wav | prefijo | 44.39 | 44.31–44.47 | 13.09 | 20/30 | [56, 56] |
| lectura_20261014_082953_219058.wav | ventana_4s | 24.30 | 22.61–25.99 | 0.35 | 7/30 | [56, 56] |
| lectura_20261014_082953_219058.wav | ventana_6s | 26.92 | 24.93–28.90 | 0.76 | 10/30 | [56, 56] |
| lectura_20261014_082953_219058.wav | ventana_8s | 26.90 | 26.17–27.63 | 0.02 | 2/30 | [56, 56] |
| lectura_20261014_082953_219058.wav | ventana_10s | 28.88 | 28.83–28.92 | 0.49 | 12/30 | [56, 56] |
| lectura_20261014_082953_219058.wav | ventana_12s | 30.03 | 29.67–30.39 | 1.33 | 14/30 | [56, 56] |
