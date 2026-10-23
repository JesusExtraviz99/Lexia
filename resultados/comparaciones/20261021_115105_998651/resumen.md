# Comparación de reprocesamiento

3 ronda(s) por configuración, orden aleatorio reproducible por ronda. Ejecución secuencial para no competir por CPU. Tiempos orientativos, afectados por carga y calentamiento. No hay referencia humana de posición ni latencia visual. Comparar posiciones entre métodos no demuestra precisión.

Mismo modelo, CPU int8, VAD, bloques de 2 s, cuento y seguidor. La carga del modelo se excluye de los tiempos de inferencia. Solapamiento = ventana menos 2 s; no aplica al prefijo. El silencio final puede reducir los totales de las ventanas.

| Audio | Método | Ronda | Total inferencia (s) | Mediana (s) | P95 (s) | Inferencias >2 s | Cola máxima simulada (s) | Posición final | Retrocesos |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| lectura_20261021_114202_408281.wav | ventana_8s | 1 | 37.98 | 1.66 | 1.81 | 0 | 0.52 | 19 | 1 |
| lectura_20261021_114202_408281.wav | ventana_4s | 1 | 36.06 | 1.61 | 1.76 | 1 | 1.66 | 56 | 0 |
| lectura_20261021_114202_408281.wav | ventana_8s | 2 | 40.10 | 1.71 | 1.93 | 0 | 0.57 | 19 | 1 |
| lectura_20261021_114202_408281.wav | ventana_4s | 2 | 35.46 | 1.67 | 1.76 | 1 | 0.51 | 56 | 0 |
| lectura_20261021_114202_408281.wav | ventana_4s | 3 | 37.52 | 1.67 | 1.79 | 1 | 2.39 | 56 | 0 |
| lectura_20261021_114202_408281.wav | ventana_8s | 3 | 41.90 | 1.83 | 2.18 | 2 | 1.28 | 19 | 1 |

## Posiciones en cada actualización

Comparación descriptiva con el prefijo, no referencia de precisión. El prefijo también puede equivocarse.

### lectura_20261021_114202_408281.wav, ronda 1

| Audio disponible (s) | ventana_4s | ventana_8s |
|---:|---:|---:|
| 2.0 | 2 | 2 |
| 4.0 | 7 | 7 |
| 6.0 | 12 | 12 |
| 8.0 | 17 | 17 |
| 10.0 | 21 | 19 |
| 12.0 | 25 | 25 |
| 14.0 | 26 | 26 |
| 16.0 | 26 | 31 |
| 18.0 | 37 | 37 |
| 20.0 | 43 | 43 |
| 22.0 | 47 | 47 |
| 24.0 | 51 | 52 |
| 26.0 | 56 | 56 |
| 28.0 | 56 | 56 |
| 30.0 | 56 | 56 |
| 32.0 | 56 | 56 |
| 34.0 | 56 | 56 |
| 36.0 | 56 | 56 |
| 38.0 | 56 | 56 |
| 40.0 | 56 | 56 |
| 42.0 | 56 | 19 |
| 44.0 | 56 | 19 |
| 45.0 | 56 | 19 |

### lectura_20261021_114202_408281.wav, ronda 2

| Audio disponible (s) | ventana_4s | ventana_8s |
|---:|---:|---:|
| 2.0 | 2 | 2 |
| 4.0 | 7 | 7 |
| 6.0 | 12 | 12 |
| 8.0 | 17 | 17 |
| 10.0 | 21 | 19 |
| 12.0 | 25 | 25 |
| 14.0 | 26 | 26 |
| 16.0 | 26 | 31 |
| 18.0 | 37 | 37 |
| 20.0 | 43 | 43 |
| 22.0 | 47 | 47 |
| 24.0 | 51 | 52 |
| 26.0 | 56 | 56 |
| 28.0 | 56 | 56 |
| 30.0 | 56 | 56 |
| 32.0 | 56 | 56 |
| 34.0 | 56 | 56 |
| 36.0 | 56 | 56 |
| 38.0 | 56 | 56 |
| 40.0 | 56 | 56 |
| 42.0 | 56 | 19 |
| 44.0 | 56 | 19 |
| 45.0 | 56 | 19 |

### lectura_20261021_114202_408281.wav, ronda 3

| Audio disponible (s) | ventana_4s | ventana_8s |
|---:|---:|---:|
| 2.0 | 2 | 2 |
| 4.0 | 7 | 7 |
| 6.0 | 12 | 12 |
| 8.0 | 17 | 17 |
| 10.0 | 21 | 19 |
| 12.0 | 25 | 25 |
| 14.0 | 26 | 26 |
| 16.0 | 26 | 31 |
| 18.0 | 37 | 37 |
| 20.0 | 43 | 43 |
| 22.0 | 47 | 47 |
| 24.0 | 51 | 52 |
| 26.0 | 56 | 56 |
| 28.0 | 56 | 56 |
| 30.0 | 56 | 56 |
| 32.0 | 56 | 56 |
| 34.0 | 56 | 56 |
| 36.0 | 56 | 56 |
| 38.0 | 56 | 56 |
| 40.0 | 56 | 56 |
| 42.0 | 56 | 19 |
| 44.0 | 56 | 19 |
| 45.0 | 56 | 19 |

## Resumen por configuración

| Audio | Método | Total medio (s) | Rango de totales (s) | Cola máxima media (s) | Inferencias >2 s | Posiciones finales |
|---|---|---:|---|---:|---|---|
| lectura_20261021_114202_408281.wav | ventana_4s | 36.35 | 35.46–37.52 | 1.52 | 3/69 | [56, 56, 56] |
| lectura_20261021_114202_408281.wav | ventana_8s | 40.00 | 37.98–41.90 | 0.79 | 2/69 | [19, 19, 19] |

<!-- recursos-computo-inicio -->
## Recursos y coste computacional

Datos de la ejecución original. «No medido» no significa cero. RTF = suma de inferencias / duración del audio completo (incluye silencio); no es latencia visual ni mide captura, escritura o muestreo. Las rondas de una grabación no son lecturas independientes.

| Registro | Dispositivo ASR | Precisión | GPU para ASR | RTF | Máx. inferencia (s) | CPU/RAM/GPU instrumentadas |
|---|---|---|---|---:|---:|---|
| lectura_20261021_114202_408281_ventana_8s_r1.json | cpu | int8 | no (CPU) | 0.844 | 1.810 | no_medido_en_la_ejecucion_original |
| lectura_20261021_114202_408281_ventana_4s_r1.json | cpu | int8 | no (CPU) | 0.801 | 3.659 | no_medido_en_la_ejecucion_original |
| lectura_20261021_114202_408281_ventana_8s_r2.json | cpu | int8 | no (CPU) | 0.891 | 1.957 | no_medido_en_la_ejecucion_original |
| lectura_20261021_114202_408281_ventana_4s_r2.json | cpu | int8 | no (CPU) | 0.788 | 2.513 | no_medido_en_la_ejecucion_original |
| lectura_20261021_114202_408281_ventana_4s_r3.json | cpu | int8 | no (CPU) | 0.834 | 4.395 | no_medido_en_la_ejecucion_original |
| lectura_20261021_114202_408281_ventana_8s_r3.json | cpu | int8 | no (CPU) | 0.931 | 2.283 | no_medido_en_la_ejecucion_original |

Para comparar tablets habrá que medir en el dispositivo de destino: RAM máxima, tiempo de respuesta sostenido y consumo/batería. Este ordenador no permite deducir esos valores. No se cambia CPU por GPU automáticamente.
<!-- recursos-computo-fin -->

<!-- identidad-audio-inicio -->
## Audio utilizado

- **Relectura lejana: Junto a una fuente… hasta rojo · cuento 2 · 21/10/2026** — Lectura con relectura lejana (Junto-rojo) - cuento 2 - 21-10-2026.wav
<!-- identidad-audio-fin -->
