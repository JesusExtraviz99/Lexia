# Comparación de reprocesamiento

3 ronda(s) por configuración, orden aleatorio reproducible por ronda. Ejecución secuencial para no competir por CPU. Tiempos orientativos, afectados por carga y calentamiento. No hay referencia humana de posición ni latencia visual. Comparar posiciones entre métodos no demuestra precisión.

Mismo modelo, CPU int8, VAD, bloques de 2 s, cuento y seguidor. La carga del modelo se excluye de los tiempos de inferencia. Solapamiento = ventana menos 2 s; no aplica al prefijo. El silencio final puede reducir los totales de las ventanas.

| Audio | Método | Ronda | Total inferencia (s) | Mediana (s) | P95 (s) | Inferencias >2 s | Cola máxima simulada (s) | Posición final | Retrocesos |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| lectura_20261016_104151_933317.wav | ventana_8s | 1 | 30.89 | 1.59 | 1.78 | 0 | 0.00 | 56 | 0 |
| lectura_20261016_104151_933317.wav | ventana_4s | 1 | 26.09 | 1.50 | 1.67 | 0 | 0.00 | 56 | 1 |
| lectura_20261016_104151_933317.wav | ventana_8s | 2 | 31.77 | 1.63 | 1.93 | 0 | 0.00 | 56 | 0 |
| lectura_20261016_104151_933317.wav | ventana_4s | 2 | 26.46 | 1.54 | 1.70 | 0 | 0.00 | 56 | 1 |
| lectura_20261016_104151_933317.wav | ventana_4s | 3 | 26.09 | 1.48 | 1.69 | 0 | 0.00 | 56 | 1 |
| lectura_20261016_104151_933317.wav | ventana_8s | 3 | 31.80 | 1.63 | 1.88 | 0 | 0.00 | 56 | 0 |

## Posiciones en cada actualización

Comparación descriptiva con el prefijo, no referencia de precisión. El prefijo también puede equivocarse.

### lectura_20261016_104151_933317.wav, ronda 1

| Audio disponible (s) | ventana_4s | ventana_8s |
|---:|---:|---:|
| 2.0 | — | — |
| 4.0 | 7 | 7 |
| 6.0 | 11 | 11 |
| 8.0 | 16 | 16 |
| 10.0 | 19 | 19 |
| 12.0 | 24 | 24 |
| 14.0 | 27 | 27 |
| 16.0 | 34 | 34 |
| 18.0 | 36 | 38 |
| 20.0 | 42 | 42 |
| 22.0 | 41 | 42 |
| 24.0 | 45 | 45 |
| 26.0 | 47 | 47 |
| 28.0 | 52 | 52 |
| 30.0 | 56 | 56 |
| 32.0 | 56 | 56 |
| 34.0 | 56 | 56 |
| 36.0 | 56 | 56 |
| 38.0 | 56 | 56 |
| 40.0 | 56 | 56 |
| 42.0 | 56 | 56 |
| 44.0 | 56 | 56 |
| 46.0 | 56 | 56 |
| 48.0 | 56 | 56 |
| 50.0 | 56 | 56 |
| 52.0 | 56 | 56 |
| 54.0 | 56 | 56 |
| 56.0 | 56 | 56 |
| 58.0 | 56 | 56 |
| 60.0 | 56 | 56 |

### lectura_20261016_104151_933317.wav, ronda 2

| Audio disponible (s) | ventana_4s | ventana_8s |
|---:|---:|---:|
| 2.0 | — | — |
| 4.0 | 7 | 7 |
| 6.0 | 11 | 11 |
| 8.0 | 16 | 16 |
| 10.0 | 19 | 19 |
| 12.0 | 24 | 24 |
| 14.0 | 27 | 27 |
| 16.0 | 34 | 34 |
| 18.0 | 36 | 38 |
| 20.0 | 42 | 42 |
| 22.0 | 41 | 42 |
| 24.0 | 45 | 45 |
| 26.0 | 47 | 47 |
| 28.0 | 52 | 52 |
| 30.0 | 56 | 56 |
| 32.0 | 56 | 56 |
| 34.0 | 56 | 56 |
| 36.0 | 56 | 56 |
| 38.0 | 56 | 56 |
| 40.0 | 56 | 56 |
| 42.0 | 56 | 56 |
| 44.0 | 56 | 56 |
| 46.0 | 56 | 56 |
| 48.0 | 56 | 56 |
| 50.0 | 56 | 56 |
| 52.0 | 56 | 56 |
| 54.0 | 56 | 56 |
| 56.0 | 56 | 56 |
| 58.0 | 56 | 56 |
| 60.0 | 56 | 56 |

### lectura_20261016_104151_933317.wav, ronda 3

| Audio disponible (s) | ventana_4s | ventana_8s |
|---:|---:|---:|
| 2.0 | — | — |
| 4.0 | 7 | 7 |
| 6.0 | 11 | 11 |
| 8.0 | 16 | 16 |
| 10.0 | 19 | 19 |
| 12.0 | 24 | 24 |
| 14.0 | 27 | 27 |
| 16.0 | 34 | 34 |
| 18.0 | 36 | 38 |
| 20.0 | 42 | 42 |
| 22.0 | 41 | 42 |
| 24.0 | 45 | 45 |
| 26.0 | 47 | 47 |
| 28.0 | 52 | 52 |
| 30.0 | 56 | 56 |
| 32.0 | 56 | 56 |
| 34.0 | 56 | 56 |
| 36.0 | 56 | 56 |
| 38.0 | 56 | 56 |
| 40.0 | 56 | 56 |
| 42.0 | 56 | 56 |
| 44.0 | 56 | 56 |
| 46.0 | 56 | 56 |
| 48.0 | 56 | 56 |
| 50.0 | 56 | 56 |
| 52.0 | 56 | 56 |
| 54.0 | 56 | 56 |
| 56.0 | 56 | 56 |
| 58.0 | 56 | 56 |
| 60.0 | 56 | 56 |

## Resumen por configuración

| Audio | Método | Total medio (s) | Rango de totales (s) | Cola máxima media (s) | Inferencias >2 s | Posiciones finales |
|---|---|---:|---|---:|---|---|
| lectura_20261016_104151_933317.wav | ventana_4s | 26.21 | 26.09–26.46 | 0.00 | 0/90 | [56, 56, 56] |
| lectura_20261016_104151_933317.wav | ventana_8s | 31.49 | 30.89–31.80 | 0.00 | 0/90 | [56, 56, 56] |
