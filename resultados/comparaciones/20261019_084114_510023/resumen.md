# Comparación de reprocesamiento

3 ronda(s) por configuración, orden aleatorio reproducible por ronda. Ejecución secuencial para no competir por CPU. Tiempos orientativos, afectados por carga y calentamiento. No hay referencia humana de posición ni latencia visual. Comparar posiciones entre métodos no demuestra precisión.

Mismo modelo, CPU int8, VAD, bloques de 2 s, cuento y seguidor. La carga del modelo se excluye de los tiempos de inferencia. Solapamiento = ventana menos 2 s; no aplica al prefijo. El silencio final puede reducir los totales de las ventanas.

| Audio | Método | Ronda | Total inferencia (s) | Mediana (s) | P95 (s) | Inferencias >2 s | Cola máxima simulada (s) | Posición final | Retrocesos |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| lectura_20261014_081816_009646.wav | ventana_6s | 1 | 27.91 | 1.84 | 2.25 | 8 | 1.30 | 56 | 0 |
| lectura_20261014_081816_009646.wav | ventana_4s | 1 | 26.59 | 1.76 | 2.33 | 8 | 1.64 | 56 | 0 |
| lectura_20261014_081816_009646.wav | ventana_8s | 1 | 34.29 | 2.21 | 2.47 | 13 | 4.66 | 56 | 0 |
| lectura_20261014_081816_009646.wav | ventana_6s | 2 | 27.18 | 1.79 | 2.26 | 5 | 0.87 | 56 | 0 |
| lectura_20261014_081816_009646.wav | ventana_4s | 2 | 22.66 | 1.70 | 1.84 | 0 | 0.00 | 56 | 0 |
| lectura_20261014_081816_009646.wav | ventana_8s | 2 | 28.02 | 1.81 | 2.06 | 2 | 0.10 | 56 | 0 |
| lectura_20261014_081816_009646.wav | ventana_4s | 3 | 22.24 | 1.66 | 1.81 | 0 | 0.00 | 56 | 0 |
| lectura_20261014_081816_009646.wav | ventana_8s | 3 | 27.46 | 1.79 | 1.94 | 0 | 0.00 | 56 | 0 |
| lectura_20261014_081816_009646.wav | ventana_6s | 3 | 24.79 | 1.71 | 1.88 | 0 | 0.00 | 56 | 0 |

## Posiciones en cada actualización

Comparación descriptiva con el prefijo, no referencia de precisión. El prefijo también puede equivocarse.

### lectura_20261014_081816_009646.wav, ronda 1

| Audio disponible (s) | ventana_4s | ventana_6s | ventana_8s |
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
| 20.0 | 47 | 46 | 46 |
| 22.0 | 53 | 53 | 53 |
| 24.0 | 56 | 56 | 56 |
| 26.0 | 56 | 56 | 56 |
| 28.0 | 56 | 56 | 56 |
| 30.0 | 56 | 56 | 56 |
| 32.0 | 56 | 56 | 56 |
| 34.0 | 56 | 56 | 56 |
| 36.0 | 56 | 56 | 56 |
| 38.0 | 56 | 56 | 56 |
| 40.0 | 56 | 56 | 56 |

### lectura_20261014_081816_009646.wav, ronda 2

| Audio disponible (s) | ventana_4s | ventana_6s | ventana_8s |
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
| 20.0 | 47 | 46 | 46 |
| 22.0 | 53 | 53 | 53 |
| 24.0 | 56 | 56 | 56 |
| 26.0 | 56 | 56 | 56 |
| 28.0 | 56 | 56 | 56 |
| 30.0 | 56 | 56 | 56 |
| 32.0 | 56 | 56 | 56 |
| 34.0 | 56 | 56 | 56 |
| 36.0 | 56 | 56 | 56 |
| 38.0 | 56 | 56 | 56 |
| 40.0 | 56 | 56 | 56 |

### lectura_20261014_081816_009646.wav, ronda 3

| Audio disponible (s) | ventana_4s | ventana_6s | ventana_8s |
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
| 20.0 | 47 | 46 | 46 |
| 22.0 | 53 | 53 | 53 |
| 24.0 | 56 | 56 | 56 |
| 26.0 | 56 | 56 | 56 |
| 28.0 | 56 | 56 | 56 |
| 30.0 | 56 | 56 | 56 |
| 32.0 | 56 | 56 | 56 |
| 34.0 | 56 | 56 | 56 |
| 36.0 | 56 | 56 | 56 |
| 38.0 | 56 | 56 | 56 |
| 40.0 | 56 | 56 | 56 |

## Resumen por configuración

| Audio | Método | Total medio (s) | Rango de totales (s) | Cola máxima media (s) | Inferencias >2 s | Posiciones finales |
|---|---|---:|---|---:|---|---|
| lectura_20261014_081816_009646.wav | ventana_4s | 23.83 | 22.24–26.59 | 0.55 | 8/60 | [56, 56, 56] |
| lectura_20261014_081816_009646.wav | ventana_6s | 26.63 | 24.79–27.91 | 0.72 | 13/60 | [56, 56, 56] |
| lectura_20261014_081816_009646.wav | ventana_8s | 29.92 | 27.46–34.29 | 1.59 | 15/60 | [56, 56, 56] |

<!-- recursos-computo-inicio -->
## Recursos y coste computacional

Datos de la ejecución original. «No medido» no significa cero. RTF = suma de inferencias / duración del audio completo (incluye silencio); no es latencia visual ni mide captura, escritura o muestreo. Las rondas de una grabación no son lecturas independientes.

| Registro | Dispositivo ASR | Precisión | GPU para ASR | RTF | Máx. inferencia (s) | CPU/RAM/GPU instrumentadas |
|---|---|---|---|---:|---:|---|
| lectura_20261014_081816_009646_ventana_6s_r1.json | cpu | int8 | no (CPU) | 0.698 | 2.586 | no_medido_en_la_ejecucion_original |
| lectura_20261014_081816_009646_ventana_4s_r1.json | cpu | int8 | no (CPU) | 0.665 | 2.333 | no_medido_en_la_ejecucion_original |
| lectura_20261014_081816_009646_ventana_8s_r1.json | cpu | int8 | no (CPU) | 0.857 | 2.620 | no_medido_en_la_ejecucion_original |
| lectura_20261014_081816_009646_ventana_6s_r2.json | cpu | int8 | no (CPU) | 0.680 | 2.260 | no_medido_en_la_ejecucion_original |
| lectura_20261014_081816_009646_ventana_4s_r2.json | cpu | int8 | no (CPU) | 0.567 | 1.901 | no_medido_en_la_ejecucion_original |
| lectura_20261014_081816_009646_ventana_8s_r2.json | cpu | int8 | no (CPU) | 0.701 | 2.102 | no_medido_en_la_ejecucion_original |
| lectura_20261014_081816_009646_ventana_4s_r3.json | cpu | int8 | no (CPU) | 0.556 | 1.826 | no_medido_en_la_ejecucion_original |
| lectura_20261014_081816_009646_ventana_8s_r3.json | cpu | int8 | no (CPU) | 0.686 | 1.967 | no_medido_en_la_ejecucion_original |
| lectura_20261014_081816_009646_ventana_6s_r3.json | cpu | int8 | no (CPU) | 0.620 | 1.920 | no_medido_en_la_ejecucion_original |

Para comparar tablets habrá que medir en el dispositivo de destino: RAM máxima, tiempo de respuesta sostenido y consumo/batería. Este ordenador no permite deducir esos valores. No se cambia CPU por GPU automáticamente.
<!-- recursos-computo-fin -->

<!-- identidad-audio-inicio -->
## Audio utilizado

- **Lectura normal · cuento 1 · 14/10/2026** — Lectura normal - cuento 1 - 14-10-2026.wav
<!-- identidad-audio-fin -->
