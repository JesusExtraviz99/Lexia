# Comparación de reprocesamiento

3 ronda(s) por configuración, orden aleatorio reproducible por ronda. Ejecución secuencial para no competir por CPU. Tiempos orientativos, afectados por carga y calentamiento. No hay referencia humana de posición ni latencia visual. Comparar posiciones entre métodos no demuestra precisión.

Mismo modelo, CPU int8, VAD, bloques de 2 s, cuento y seguidor. La carga del modelo se excluye de los tiempos de inferencia. Solapamiento = ventana menos 2 s; no aplica al prefijo. El silencio final puede reducir los totales de las ventanas.

| Audio | Método | Ronda | Total inferencia (s) | Mediana (s) | P95 (s) | Inferencias >2 s | Cola máxima simulada (s) | Posición final | Retrocesos |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| lectura_20261014_111454_984161.wav | ventana_8s | 1 | 38.72 | 1.68 | 2.35 | 9 | 1.64 | 56 | 0 |
| lectura_20261014_111454_984161.wav | ventana_4s | 1 | 32.12 | 1.64 | 2.10 | 4 | 0.19 | 56 | 0 |
| lectura_20261014_111454_984161.wav | ventana_8s | 2 | 39.66 | 1.87 | 2.32 | 9 | 0.88 | 56 | 0 |
| lectura_20261014_111454_984161.wav | ventana_4s | 2 | 31.37 | 1.71 | 2.05 | 2 | 0.06 | 56 | 0 |
| lectura_20261014_111454_984161.wav | ventana_4s | 3 | 32.54 | 1.68 | 2.08 | 6 | 0.19 | 56 | 0 |
| lectura_20261014_111454_984161.wav | ventana_8s | 3 | 40.44 | 1.87 | 2.34 | 12 | 1.51 | 56 | 0 |

## Posiciones en cada actualización

Comparación descriptiva con el prefijo, no referencia de precisión. El prefijo también puede equivocarse.

### lectura_20261014_111454_984161.wav, ronda 1

| Audio disponible (s) | ventana_4s | ventana_8s |
|---:|---:|---:|
| 2.0 | — | — |
| 4.0 | 6 | 6 |
| 6.0 | 13 | 13 |
| 8.0 | 17 | 17 |
| 10.0 | 21 | 20 |
| 12.0 | 27 | 27 |
| 14.0 | 27 | 27 |
| 16.0 | 27 | 27 |
| 18.0 | 27 | 27 |
| 20.0 | 27 | 27 |
| 22.0 | 27 | 27 |
| 24.0 | 36 | 36 |
| 26.0 | 42 | 42 |
| 28.0 | 46 | 46 |
| 30.0 | 53 | 53 |
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

### lectura_20261014_111454_984161.wav, ronda 2

| Audio disponible (s) | ventana_4s | ventana_8s |
|---:|---:|---:|
| 2.0 | — | — |
| 4.0 | 6 | 6 |
| 6.0 | 13 | 13 |
| 8.0 | 17 | 17 |
| 10.0 | 21 | 20 |
| 12.0 | 27 | 27 |
| 14.0 | 27 | 27 |
| 16.0 | 27 | 27 |
| 18.0 | 27 | 27 |
| 20.0 | 27 | 27 |
| 22.0 | 27 | 27 |
| 24.0 | 36 | 36 |
| 26.0 | 42 | 42 |
| 28.0 | 46 | 46 |
| 30.0 | 53 | 53 |
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

### lectura_20261014_111454_984161.wav, ronda 3

| Audio disponible (s) | ventana_4s | ventana_8s |
|---:|---:|---:|
| 2.0 | — | — |
| 4.0 | 6 | 6 |
| 6.0 | 13 | 13 |
| 8.0 | 17 | 17 |
| 10.0 | 21 | 20 |
| 12.0 | 27 | 27 |
| 14.0 | 27 | 27 |
| 16.0 | 27 | 27 |
| 18.0 | 27 | 27 |
| 20.0 | 27 | 27 |
| 22.0 | 27 | 27 |
| 24.0 | 36 | 36 |
| 26.0 | 42 | 42 |
| 28.0 | 46 | 46 |
| 30.0 | 53 | 53 |
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
| lectura_20261014_111454_984161.wav | ventana_4s | 32.01 | 31.37–32.54 | 0.15 | 12/90 | [56, 56, 56] |
| lectura_20261014_111454_984161.wav | ventana_8s | 39.60 | 38.72–40.44 | 1.34 | 30/90 | [56, 56, 56] |

<!-- recursos-computo-inicio -->
## Recursos y coste computacional

Datos de la ejecución original. «No medido» no significa cero. RTF = suma de inferencias / duración del audio completo (incluye silencio); no es latencia visual ni mide captura, escritura o muestreo. Las rondas de una grabación no son lecturas independientes.

| Registro | Dispositivo ASR | Precisión | GPU para ASR | RTF | Máx. inferencia (s) | CPU/RAM/GPU instrumentadas |
|---|---|---|---|---:|---:|---|
| lectura_20261014_111454_984161_ventana_8s_r1.json | cpu | int8 | no (CPU) | 0.645 | 2.387 | no_medido_en_la_ejecucion_original |
| lectura_20261014_111454_984161_ventana_4s_r1.json | cpu | int8 | no (CPU) | 0.535 | 2.176 | no_medido_en_la_ejecucion_original |
| lectura_20261014_111454_984161_ventana_8s_r2.json | cpu | int8 | no (CPU) | 0.661 | 2.338 | no_medido_en_la_ejecucion_original |
| lectura_20261014_111454_984161_ventana_4s_r2.json | cpu | int8 | no (CPU) | 0.523 | 2.058 | no_medido_en_la_ejecucion_original |
| lectura_20261014_111454_984161_ventana_4s_r3.json | cpu | int8 | no (CPU) | 0.542 | 2.110 | no_medido_en_la_ejecucion_original |
| lectura_20261014_111454_984161_ventana_8s_r3.json | cpu | int8 | no (CPU) | 0.674 | 2.381 | no_medido_en_la_ejecucion_original |

Para comparar tablets habrá que medir en el dispositivo de destino: RAM máxima, tiempo de respuesta sostenido y consumo/batería. Este ordenador no permite deducir esos valores. No se cambia CPU por GPU automáticamente.
<!-- recursos-computo-fin -->

<!-- identidad-audio-inicio -->
## Audio utilizado

- **Lectura con pausa entre flor y Ana · cuento 1 · 14/10/2026** — Lectura con pausa (flor-Ana) - cuento 1 - 14-10-2026.wav
<!-- identidad-audio-fin -->
