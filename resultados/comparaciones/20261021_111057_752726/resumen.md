# Comparación de reprocesamiento

3 ronda(s) por configuración, orden aleatorio reproducible por ronda. Ejecución secuencial para no competir por CPU. Tiempos orientativos, afectados por carga y calentamiento. No hay referencia humana de posición ni latencia visual. Comparar posiciones entre métodos no demuestra precisión.

Mismo modelo, CPU int8, VAD, bloques de 2 s, cuento y seguidor. La carga del modelo se excluye de los tiempos de inferencia. Solapamiento = ventana menos 2 s; no aplica al prefijo. El silencio final puede reducir los totales de las ventanas.

| Audio | Método | Ronda | Total inferencia (s) | Mediana (s) | P95 (s) | Inferencias >2 s | Cola máxima simulada (s) | Posición final | Retrocesos |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| lectura_20261021_110858_556291.wav | ventana_8s | 1 | 27.01 | 1.67 | 1.79 | 0 | 0.00 | 56 | 0 |
| lectura_20261021_110858_556291.wav | ventana_4s | 1 | 22.41 | 1.57 | 1.63 | 0 | 0.00 | 56 | 0 |
| lectura_20261021_110858_556291.wav | ventana_8s | 2 | 28.39 | 1.74 | 1.89 | 0 | 0.00 | 56 | 0 |
| lectura_20261021_110858_556291.wav | ventana_4s | 2 | 29.22 | 1.86 | 2.50 | 6 | 2.07 | 56 | 0 |
| lectura_20261021_110858_556291.wav | ventana_4s | 3 | 29.03 | 2.05 | 2.22 | 12 | 1.03 | 56 | 0 |
| lectura_20261021_110858_556291.wav | ventana_8s | 3 | 33.62 | 2.08 | 2.33 | 11 | 2.27 | 56 | 0 |

## Posiciones en cada actualización

Comparación descriptiva con el prefijo, no referencia de precisión. El prefijo también puede equivocarse.

### lectura_20261021_110858_556291.wav, ronda 1

| Audio disponible (s) | ventana_4s | ventana_8s |
|---:|---:|---:|
| 2.0 | 2 | 2 |
| 4.0 | 6 | 6 |
| 6.0 | 10 | 10 |
| 8.0 | 16 | 16 |
| 10.0 | 19 | 19 |
| 12.0 | 23 | 23 |
| 14.0 | 27 | 26 |
| 16.0 | 31 | 31 |
| 18.0 | 37 | 37 |
| 20.0 | 41 | 41 |
| 22.0 | 46 | 46 |
| 24.0 | 51 | 50 |
| 26.0 | 56 | 56 |
| 28.0 | 56 | 56 |
| 30.0 | 56 | 56 |
| 32.0 | 56 | 56 |
| 34.0 | 56 | 56 |
| 36.0 | 56 | 56 |
| 38.0 | 56 | 56 |
| 40.0 | 56 | 56 |

### lectura_20261021_110858_556291.wav, ronda 2

| Audio disponible (s) | ventana_4s | ventana_8s |
|---:|---:|---:|
| 2.0 | 2 | 2 |
| 4.0 | 6 | 6 |
| 6.0 | 10 | 10 |
| 8.0 | 16 | 16 |
| 10.0 | 19 | 19 |
| 12.0 | 23 | 23 |
| 14.0 | 27 | 26 |
| 16.0 | 31 | 31 |
| 18.0 | 37 | 37 |
| 20.0 | 41 | 41 |
| 22.0 | 46 | 46 |
| 24.0 | 51 | 50 |
| 26.0 | 56 | 56 |
| 28.0 | 56 | 56 |
| 30.0 | 56 | 56 |
| 32.0 | 56 | 56 |
| 34.0 | 56 | 56 |
| 36.0 | 56 | 56 |
| 38.0 | 56 | 56 |
| 40.0 | 56 | 56 |

### lectura_20261021_110858_556291.wav, ronda 3

| Audio disponible (s) | ventana_4s | ventana_8s |
|---:|---:|---:|
| 2.0 | 2 | 2 |
| 4.0 | 6 | 6 |
| 6.0 | 10 | 10 |
| 8.0 | 16 | 16 |
| 10.0 | 19 | 19 |
| 12.0 | 23 | 23 |
| 14.0 | 27 | 26 |
| 16.0 | 31 | 31 |
| 18.0 | 37 | 37 |
| 20.0 | 41 | 41 |
| 22.0 | 46 | 46 |
| 24.0 | 51 | 50 |
| 26.0 | 56 | 56 |
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
| lectura_20261021_110858_556291.wav | ventana_4s | 26.89 | 22.41–29.22 | 1.03 | 18/60 | [56, 56, 56] |
| lectura_20261021_110858_556291.wav | ventana_8s | 29.67 | 27.01–33.62 | 0.76 | 11/60 | [56, 56, 56] |

<!-- recursos-computo-inicio -->
## Recursos y coste computacional

Datos de la ejecución original. «No medido» no significa cero. RTF = suma de inferencias / duración del audio completo (incluye silencio); no es latencia visual ni mide captura, escritura o muestreo. Las rondas de una grabación no son lecturas independientes.

| Registro | Dispositivo ASR | Precisión | GPU para ASR | RTF | Máx. inferencia (s) | CPU/RAM/GPU instrumentadas |
|---|---|---|---|---:|---:|---|
| lectura_20261021_110858_556291_ventana_8s_r1.json | cpu | int8 | no (CPU) | 0.675 | 1.789 | no_medido_en_la_ejecucion_original |
| lectura_20261021_110858_556291_ventana_4s_r1.json | cpu | int8 | no (CPU) | 0.560 | 1.658 | no_medido_en_la_ejecucion_original |
| lectura_20261021_110858_556291_ventana_8s_r2.json | cpu | int8 | no (CPU) | 0.710 | 1.917 | no_medido_en_la_ejecucion_original |
| lectura_20261021_110858_556291_ventana_4s_r2.json | cpu | int8 | no (CPU) | 0.731 | 2.569 | no_medido_en_la_ejecucion_original |
| lectura_20261021_110858_556291_ventana_4s_r3.json | cpu | int8 | no (CPU) | 0.726 | 2.244 | no_medido_en_la_ejecucion_original |
| lectura_20261021_110858_556291_ventana_8s_r3.json | cpu | int8 | no (CPU) | 0.840 | 2.342 | no_medido_en_la_ejecucion_original |

Para comparar tablets habrá que medir en el dispositivo de destino: RAM máxima, tiempo de respuesta sostenido y consumo/batería. Este ordenador no permite deducir esos valores. No se cambia CPU por GPU automáticamente.
<!-- recursos-computo-fin -->

<!-- identidad-audio-inicio -->
## Audio utilizado

- **Lectura normal con lluvia · cuento 2 · 21/10/2026** — Lectura normal con lluvia - cuento 2 - 21-10-2026.wav
<!-- identidad-audio-fin -->
