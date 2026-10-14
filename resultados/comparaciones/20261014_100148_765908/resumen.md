# Comparación de reprocesamiento

3 ronda(s) por configuración, orden aleatorio reproducible por ronda. Ejecución secuencial para no competir por CPU. Tiempos orientativos, afectados por carga y calentamiento. No hay referencia humana de posición ni latencia visual. Comparar posiciones entre métodos no demuestra precisión.

Mismo modelo, CPU int8, VAD, bloques de 2 s, cuento y seguidor. La carga del modelo se excluye de los tiempos de inferencia. Solapamiento = ventana menos 2 s; no aplica al prefijo. El silencio final puede reducir los totales de las ventanas.

| Audio | Método | Ronda | Total inferencia (s) | Mediana (s) | P95 (s) | Inferencias >2 s | Cola máxima simulada (s) | Posición final | Retrocesos |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| lectura_20261014_082953_219058.wav | ventana_8s | 1 | 25.49 | 1.75 | 1.91 | 0 | 0.00 | 56 | 0 |
| lectura_20261014_082953_219058.wav | prefijo | 1 | 43.15 | 2.49 | 4.67 | 9 | 12.83 | 56 | 0 |
| lectura_20261014_082953_219058.wav | ventana_6s | 1 | 23.72 | 1.71 | 1.89 | 0 | 0.00 | 56 | 0 |
| lectura_20261014_082953_219058.wav | ventana_4s | 1 | 21.49 | 1.63 | 1.90 | 0 | 0.00 | 56 | 0 |
| lectura_20261014_082953_219058.wav | ventana_10s | 1 | 28.58 | 1.91 | 2.20 | 4 | 0.44 | 56 | 0 |
| lectura_20261014_082953_219058.wav | ventana_12s | 1 | 29.33 | 1.96 | 2.26 | 7 | 1.00 | 56 | 0 |
| lectura_20261014_082953_219058.wav | prefijo | 2 | 48.09 | 2.70 | 5.13 | 10 | 16.27 | 56 | 0 |
| lectura_20261014_082953_219058.wav | ventana_4s | 2 | 24.25 | 1.86 | 1.99 | 0 | 0.00 | 56 | 0 |
| lectura_20261014_082953_219058.wav | ventana_12s | 2 | 32.23 | 2.18 | 2.68 | 9 | 3.15 | 56 | 0 |
| lectura_20261014_082953_219058.wav | ventana_6s | 2 | 26.17 | 1.84 | 2.15 | 5 | 0.29 | 56 | 0 |
| lectura_20261014_082953_219058.wav | ventana_10s | 2 | 27.90 | 1.90 | 2.09 | 4 | 0.19 | 56 | 0 |
| lectura_20261014_082953_219058.wav | ventana_8s | 2 | 27.30 | 1.82 | 2.28 | 1 | 0.28 | 56 | 0 |
| lectura_20261014_082953_219058.wav | ventana_8s | 3 | 26.98 | 1.83 | 1.97 | 0 | 0.00 | 56 | 0 |
| lectura_20261014_082953_219058.wav | ventana_4s | 3 | 21.62 | 1.63 | 1.99 | 0 | 0.00 | 56 | 0 |
| lectura_20261014_082953_219058.wav | prefijo | 3 | 43.32 | 2.45 | 4.34 | 11 | 12.10 | 56 | 0 |
| lectura_20261014_082953_219058.wav | ventana_12s | 3 | 28.94 | 2.01 | 2.19 | 8 | 0.69 | 56 | 0 |
| lectura_20261014_082953_219058.wav | ventana_10s | 3 | 28.07 | 1.87 | 2.13 | 5 | 0.23 | 56 | 0 |
| lectura_20261014_082953_219058.wav | ventana_6s | 3 | 24.23 | 1.72 | 2.11 | 1 | 0.11 | 56 | 0 |

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

### lectura_20261014_082953_219058.wav, ronda 3

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
| lectura_20261014_082953_219058.wav | prefijo | 44.85 | 43.15–48.09 | 13.73 | 30/45 | [56, 56, 56] |
| lectura_20261014_082953_219058.wav | ventana_4s | 22.45 | 21.49–24.25 | 0.00 | 0/45 | [56, 56, 56] |
| lectura_20261014_082953_219058.wav | ventana_6s | 24.71 | 23.72–26.17 | 0.14 | 6/45 | [56, 56, 56] |
| lectura_20261014_082953_219058.wav | ventana_8s | 26.59 | 25.49–27.30 | 0.09 | 1/45 | [56, 56, 56] |
| lectura_20261014_082953_219058.wav | ventana_10s | 28.18 | 27.90–28.58 | 0.28 | 13/45 | [56, 56, 56] |
| lectura_20261014_082953_219058.wav | ventana_12s | 30.16 | 28.94–32.23 | 1.62 | 24/45 | [56, 56, 56] |
