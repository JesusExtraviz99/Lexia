# Comparación de reprocesamiento

Una ejecución por configuración en orden fijo. Tiempos orientativos, afectados por carga y calentamiento. No hay referencia humana de posición ni latencia visual. Comparar posiciones entre métodos no demuestra precisión.

Mismo modelo, CPU int8, VAD, bloques de 2 s, cuento y seguidor. La carga del modelo se excluye de los tiempos de inferencia. El solapamiento es 4 s en la ventana de 6 s y 8 s en la de 10 s.

| Audio | Método | Total inferencia (s) | Mediana (s) | P95 (s) | Inferencias >2 s | Cola máxima simulada (s) | Posición final | Retrocesos |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| lectura_20261014_081816_009646.wav | prefijo | 50.51 | 2.59 | 3.21 | 14 | 10.18 | 56 | 0 |
| lectura_20261014_081816_009646.wav | ventana_6s | 25.93 | 1.79 | 2.05 | 2 | 0.13 | 56 | 0 |
| lectura_20261014_081816_009646.wav | ventana_10s | 30.35 | 1.83 | 2.08 | 6 | 0.44 | 56 | 0 |
| lectura_20261014_082953_219058.wav | prefijo | 44.74 | 2.52 | 4.67 | 10 | 13.39 | 56 | 0 |
| lectura_20261014_082953_219058.wav | ventana_6s | 24.58 | 1.78 | 1.86 | 0 | 0.00 | 56 | 0 |
| lectura_20261014_082953_219058.wav | ventana_10s | 29.01 | 1.91 | 2.26 | 6 | 0.66 | 56 | 0 |

## Posiciones en cada actualización

Comparación descriptiva con el prefijo, no referencia de precisión. El prefijo también puede equivocarse.

### lectura_20261014_081816_009646.wav

| Audio disponible (s) | Prefijo | Ventana 6 s | Ventana 10 s |
|---:|---:|---:|---:|
| 2.0 | — | — | — |
| 4.0 | 5 | 5 | 5 |
| 6.0 | 12 | 12 | 12 |
| 8.0 | 17 | 17 | 17 |
| 10.0 | 20 | 20 | 20 |
| 12.0 | 27 | 27 | 27 |
| 14.0 | 34 | 34 | 34 |
| 16.0 | 38 | 38 | 38 |
| 18.0 | 43 | 43 | 43 |
| 20.0 | 46 | 46 | 48 |
| 22.0 | 51 | 53 | 53 |
| 24.0 | 56 | 56 | 56 |
| 26.0 | 56 | 56 | 56 |
| 28.0 | 56 | 56 | 56 |
| 30.0 | 56 | 56 | 56 |
| 32.0 | 56 | 56 | 56 |
| 34.0 | 56 | 56 | 56 |
| 36.0 | 56 | 56 | 56 |
| 38.0 | 56 | 56 | 56 |
| 40.0 | 56 | 56 | 56 |

### lectura_20261014_082953_219058.wav

| Audio disponible (s) | Prefijo | Ventana 6 s | Ventana 10 s |
|---:|---:|---:|---:|
| 2.0 | — | — | — |
| 4.0 | 3 | 3 | 3 |
| 6.0 | 9 | 9 | 9 |
| 8.0 | 16 | 16 | 16 |
| 10.0 | 20 | 20 | 20 |
| 12.0 | 27 | 27 | 27 |
| 14.0 | 35 | 35 | 35 |
| 16.0 | 38 | 39 | 39 |
| 18.0 | 44 | 44 | 44 |
| 20.0 | 48 | 48 | 48 |
| 22.0 | 51 | 52 | 52 |
| 24.0 | 56 | 56 | 56 |
| 26.0 | 56 | 56 | 56 |
| 28.0 | 56 | 56 | 56 |
| 30.0 | 56 | 56 | 56 |
