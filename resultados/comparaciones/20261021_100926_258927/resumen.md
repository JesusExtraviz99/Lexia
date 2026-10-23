# Comparación de reprocesamiento

3 ronda(s) por configuración, orden aleatorio reproducible por ronda. Ejecución secuencial para no competir por CPU. Tiempos orientativos, afectados por carga y calentamiento. No hay referencia humana de posición ni latencia visual. Comparar posiciones entre métodos no demuestra precisión.

Mismo modelo, CPU int8, VAD, bloques de 2 s, cuento y seguidor. La carga del modelo se excluye de los tiempos de inferencia. Solapamiento = ventana menos 2 s; no aplica al prefijo. El silencio final puede reducir los totales de las ventanas.

| Audio | Método | Ronda | Total inferencia (s) | Mediana (s) | P95 (s) | Inferencias >2 s | Cola máxima simulada (s) | Posición final | Retrocesos |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| lectura_20261021_100814_321948.wav | ventana_8s | 1 | 32.70 | 1.66 | 1.77 | 1 | 4.35 | 56 | 0 |
| lectura_20261021_100814_321948.wav | ventana_4s | 1 | 23.61 | 1.56 | 1.64 | 0 | 0.00 | 56 | 0 |
| lectura_20261021_100814_321948.wav | ventana_8s | 2 | 38.08 | 1.75 | 1.86 | 1 | 8.51 | 56 | 0 |
| lectura_20261021_100814_321948.wav | ventana_4s | 2 | 24.08 | 1.59 | 1.65 | 0 | 0.00 | 56 | 0 |
| lectura_20261021_100814_321948.wav | ventana_4s | 3 | 24.18 | 1.59 | 1.66 | 0 | 0.00 | 56 | 0 |
| lectura_20261021_100814_321948.wav | ventana_8s | 3 | 37.35 | 1.74 | 1.85 | 1 | 7.86 | 56 | 0 |

## Posiciones en cada actualización

Comparación descriptiva con el prefijo, no referencia de precisión. El prefijo también puede equivocarse.

### lectura_20261021_100814_321948.wav, ronda 1

| Audio disponible (s) | ventana_4s | ventana_8s |
|---:|---:|---:|
| 2.0 | 2 | 2 |
| 4.0 | 6 | 6 |
| 6.0 | 9 | 12 |
| 8.0 | 16 | 16 |
| 10.0 | 19 | 19 |
| 12.0 | 24 | 24 |
| 14.0 | 27 | 27 |
| 16.0 | 35 | 35 |
| 18.0 | 38 | 38 |
| 20.0 | 42 | 42 |
| 22.0 | 46 | 44 |
| 24.0 | 50 | 50 |
| 26.0 | 55 | 55 |
| 28.0 | 56 | 56 |
| 30.0 | 56 | 56 |
| 32.0 | 56 | 56 |
| 34.0 | 56 | 56 |
| 36.0 | 56 | 56 |
| 38.0 | 56 | 56 |
| 40.0 | 56 | 56 |

### lectura_20261021_100814_321948.wav, ronda 2

| Audio disponible (s) | ventana_4s | ventana_8s |
|---:|---:|---:|
| 2.0 | 2 | 2 |
| 4.0 | 6 | 6 |
| 6.0 | 9 | 12 |
| 8.0 | 16 | 16 |
| 10.0 | 19 | 19 |
| 12.0 | 24 | 24 |
| 14.0 | 27 | 27 |
| 16.0 | 35 | 35 |
| 18.0 | 38 | 38 |
| 20.0 | 42 | 42 |
| 22.0 | 46 | 45 |
| 24.0 | 50 | 50 |
| 26.0 | 55 | 55 |
| 28.0 | 56 | 56 |
| 30.0 | 56 | 56 |
| 32.0 | 56 | 56 |
| 34.0 | 56 | 56 |
| 36.0 | 56 | 56 |
| 38.0 | 56 | 56 |
| 40.0 | 56 | 56 |

### lectura_20261021_100814_321948.wav, ronda 3

| Audio disponible (s) | ventana_4s | ventana_8s |
|---:|---:|---:|
| 2.0 | 2 | 2 |
| 4.0 | 6 | 6 |
| 6.0 | 9 | 12 |
| 8.0 | 16 | 16 |
| 10.0 | 19 | 19 |
| 12.0 | 24 | 24 |
| 14.0 | 27 | 27 |
| 16.0 | 35 | 35 |
| 18.0 | 38 | 38 |
| 20.0 | 42 | 42 |
| 22.0 | 46 | 44 |
| 24.0 | 50 | 50 |
| 26.0 | 55 | 55 |
| 28.0 | 56 | 56 |
| 30.0 | 56 | 56 |
| 32.0 | 56 | 56 |
| 34.0 | 56 | 56 |
| 36.0 | 56 | 56 |
| 38.0 | 56 | 56 |
| 40.0 | 56 | 56 |

## Resumen por configuración

| Audio | Método | Total medio (s) | Rango de totales (s) | Cola máxima media (s) | Inferencias >2 s | Posiciones finales |
|---|---|---:|---|---:|---|---|
| lectura_20261021_100814_321948.wav | ventana_4s | 23.96 | 23.61–24.18 | 0.00 | 0/60 | [56, 56, 56] |
| lectura_20261021_100814_321948.wav | ventana_8s | 36.04 | 32.70–38.08 | 6.91 | 3/60 | [56, 56, 56] |

<!-- recursos-computo-inicio -->
## Recursos y coste computacional

Datos de la ejecución original. «No medido» no significa cero. RTF = suma de inferencias / duración del audio completo (incluye silencio); no es latencia visual ni mide captura, escritura o muestreo. Las rondas de una grabación no son lecturas independientes.

| Registro | Dispositivo ASR | Precisión | GPU para ASR | RTF | Máx. inferencia (s) | CPU/RAM/GPU instrumentadas |
|---|---|---|---|---:|---:|---|
| lectura_20261021_100814_321948_ventana_8s_r1.json | cpu | int8 | no (CPU) | 0.817 | 6.354 | no_medido_en_la_ejecucion_original |
| lectura_20261021_100814_321948_ventana_4s_r1.json | cpu | int8 | no (CPU) | 0.590 | 1.740 | no_medido_en_la_ejecucion_original |
| lectura_20261021_100814_321948_ventana_8s_r2.json | cpu | int8 | no (CPU) | 0.952 | 10.512 | no_medido_en_la_ejecucion_original |
| lectura_20261021_100814_321948_ventana_4s_r2.json | cpu | int8 | no (CPU) | 0.602 | 1.667 | no_medido_en_la_ejecucion_original |
| lectura_20261021_100814_321948_ventana_4s_r3.json | cpu | int8 | no (CPU) | 0.604 | 1.694 | no_medido_en_la_ejecucion_original |
| lectura_20261021_100814_321948_ventana_8s_r3.json | cpu | int8 | no (CPU) | 0.934 | 9.859 | no_medido_en_la_ejecucion_original |

Para comparar tablets habrá que medir en el dispositivo de destino: RAM máxima, tiempo de respuesta sostenido y consumo/batería. Este ordenador no permite deducir esos valores. No se cambia CPU por GPU automáticamente.
<!-- recursos-computo-fin -->

<!-- identidad-audio-inicio -->
## Audio utilizado

- **Lectura normal con lluvia · cuento 1 · 21/10/2026** — Lectura normal con lluvia - cuento 1 - 21-10-2026.wav
<!-- identidad-audio-fin -->
