# Comparación de reprocesamiento

3 ronda(s) por configuración, orden aleatorio reproducible por ronda. Ejecución secuencial para no competir por CPU. Tiempos orientativos, afectados por carga y calentamiento. No hay referencia humana de posición ni latencia visual. Comparar posiciones entre métodos no demuestra precisión.

Mismo modelo, CPU int8, VAD, bloques de 2 s, cuento y seguidor. La carga del modelo se excluye de los tiempos de inferencia. Solapamiento = ventana menos 2 s; no aplica al prefijo. El silencio final puede reducir los totales de las ventanas.

| Audio | Método | Ronda | Total inferencia (s) | Mediana (s) | P95 (s) | Inferencias >2 s | Cola máxima simulada (s) | Posición final | Retrocesos |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| lectura_20261016_095108_269618.wav | ventana_8s | 1 | 98.30 | 1.75 | 1.87 | 2 | 24.21 | 55 | 1 |
| lectura_20261016_095108_269618.wav | ventana_4s | 1 | 71.14 | 1.64 | 2.22 | 3 | 2.27 | 53 | 0 |
| lectura_20261016_095108_269618.wav | ventana_8s | 2 | 93.79 | 1.62 | 1.70 | 1 | 25.03 | 55 | 1 |
| lectura_20261016_095108_269618.wav | ventana_4s | 2 | 67.18 | 1.55 | 2.04 | 3 | 1.91 | 53 | 0 |
| lectura_20261016_095108_269618.wav | ventana_4s | 3 | 67.89 | 1.56 | 2.04 | 3 | 1.91 | 53 | 0 |
| lectura_20261016_095108_269618.wav | ventana_8s | 3 | 87.79 | 1.63 | 1.70 | 1 | 18.90 | 55 | 1 |

## Posiciones en cada actualización

Comparación descriptiva con el prefijo, no referencia de precisión. El prefijo también puede equivocarse.

### lectura_20261016_095108_269618.wav, ronda 1

| Audio disponible (s) | ventana_4s | ventana_8s |
|---:|---:|---:|
| 2.0 | — | — |
| 4.0 | 2 | 2 |
| 6.0 | 2 | 3 |
| 8.0 | 4 | 3 |
| 10.0 | 7 | 3 |
| 12.0 | 9 | 9 |
| 14.0 | 10 | 10 |
| 16.0 | 13 | 13 |
| 18.0 | 13 | 13 |
| 20.0 | 15 | 15 |
| 22.0 | 16 | 16 |
| 24.0 | 17 | 17 |
| 26.0 | 19 | 19 |
| 28.0 | 20 | 20 |
| 30.0 | 21 | 21 |
| 32.0 | 24 | 24 |
| 34.0 | 26 | 26 |
| 36.0 | 27 | 27 |
| 38.0 | 28 | 29 |
| 40.0 | 32 | 31 |
| 42.0 | 32 | 34 |
| 44.0 | 34 | 34 |
| 46.0 | 35 | 35 |
| 48.0 | 35 | 36 |
| 50.0 | 38 | 38 |
| 52.0 | 40 | 40 |
| 54.0 | 42 | 42 |
| 56.0 | 42 | 42 |
| 58.0 | 44 | 44 |
| 60.0 | 45 | 45 |
| 62.0 | 45 | 46 |
| 64.0 | 45 | 47 |
| 66.0 | 49 | 49 |
| 68.0 | 50 | 50 |
| 70.0 | 52 | 52 |
| 72.0 | 53 | 53 |
| 74.0 | 53 | 54 |
| 76.0 | 53 | 55 |
| 78.0 | 53 | 56 |
| 80.0 | 53 | 55 |
| 82.0 | 53 | 55 |
| 84.0 | 53 | 55 |
| 86.0 | 53 | 55 |
| 88.0 | 53 | 55 |
| 90.0 | 53 | 55 |

### lectura_20261016_095108_269618.wav, ronda 2

| Audio disponible (s) | ventana_4s | ventana_8s |
|---:|---:|---:|
| 2.0 | — | — |
| 4.0 | 2 | 2 |
| 6.0 | 2 | 3 |
| 8.0 | 4 | 3 |
| 10.0 | 7 | 3 |
| 12.0 | 9 | 9 |
| 14.0 | 10 | 10 |
| 16.0 | 13 | 13 |
| 18.0 | 13 | 13 |
| 20.0 | 15 | 15 |
| 22.0 | 16 | 16 |
| 24.0 | 17 | 17 |
| 26.0 | 19 | 19 |
| 28.0 | 20 | 20 |
| 30.0 | 21 | 21 |
| 32.0 | 24 | 24 |
| 34.0 | 26 | 26 |
| 36.0 | 27 | 27 |
| 38.0 | 28 | 29 |
| 40.0 | 32 | 31 |
| 42.0 | 32 | 34 |
| 44.0 | 34 | 34 |
| 46.0 | 35 | 35 |
| 48.0 | 35 | 36 |
| 50.0 | 38 | 38 |
| 52.0 | 40 | 40 |
| 54.0 | 42 | 42 |
| 56.0 | 42 | 42 |
| 58.0 | 44 | 44 |
| 60.0 | 45 | 45 |
| 62.0 | 45 | 46 |
| 64.0 | 45 | 47 |
| 66.0 | 49 | 49 |
| 68.0 | 50 | 50 |
| 70.0 | 52 | 52 |
| 72.0 | 53 | 53 |
| 74.0 | 53 | 54 |
| 76.0 | 53 | 55 |
| 78.0 | 53 | 56 |
| 80.0 | 53 | 55 |
| 82.0 | 53 | 55 |
| 84.0 | 53 | 55 |
| 86.0 | 53 | 55 |
| 88.0 | 53 | 55 |
| 90.0 | 53 | 55 |

### lectura_20261016_095108_269618.wav, ronda 3

| Audio disponible (s) | ventana_4s | ventana_8s |
|---:|---:|---:|
| 2.0 | — | — |
| 4.0 | 2 | 2 |
| 6.0 | 2 | 3 |
| 8.0 | 4 | 3 |
| 10.0 | 7 | 3 |
| 12.0 | 9 | 9 |
| 14.0 | 10 | 10 |
| 16.0 | 13 | 13 |
| 18.0 | 13 | 13 |
| 20.0 | 15 | 15 |
| 22.0 | 16 | 16 |
| 24.0 | 17 | 17 |
| 26.0 | 19 | 19 |
| 28.0 | 20 | 20 |
| 30.0 | 21 | 21 |
| 32.0 | 24 | 24 |
| 34.0 | 26 | 26 |
| 36.0 | 27 | 27 |
| 38.0 | 28 | 29 |
| 40.0 | 32 | 31 |
| 42.0 | 32 | 34 |
| 44.0 | 34 | 34 |
| 46.0 | 35 | 35 |
| 48.0 | 35 | 36 |
| 50.0 | 38 | 38 |
| 52.0 | 40 | 40 |
| 54.0 | 42 | 42 |
| 56.0 | 42 | 42 |
| 58.0 | 44 | 44 |
| 60.0 | 45 | 45 |
| 62.0 | 45 | 46 |
| 64.0 | 45 | 47 |
| 66.0 | 49 | 49 |
| 68.0 | 50 | 50 |
| 70.0 | 52 | 52 |
| 72.0 | 53 | 53 |
| 74.0 | 53 | 54 |
| 76.0 | 53 | 55 |
| 78.0 | 53 | 56 |
| 80.0 | 53 | 55 |
| 82.0 | 53 | 55 |
| 84.0 | 53 | 55 |
| 86.0 | 53 | 55 |
| 88.0 | 53 | 55 |
| 90.0 | 53 | 55 |

## Resumen por configuración

| Audio | Método | Total medio (s) | Rango de totales (s) | Cola máxima media (s) | Inferencias >2 s | Posiciones finales |
|---|---|---:|---|---:|---|---|
| lectura_20261016_095108_269618.wav | ventana_4s | 68.74 | 67.18–71.14 | 2.03 | 9/135 | [53, 53, 53] |
| lectura_20261016_095108_269618.wav | ventana_8s | 93.29 | 87.79–98.30 | 22.72 | 4/135 | [55, 55, 55] |

<!-- recursos-computo-inicio -->
## Recursos y coste computacional

Datos de la ejecución original. «No medido» no significa cero. RTF = suma de inferencias / duración del audio completo (incluye silencio); no es latencia visual ni mide captura, escritura o muestreo. Las rondas de una grabación no son lecturas independientes.

| Registro | Dispositivo ASR | Precisión | GPU para ASR | RTF | Máx. inferencia (s) | CPU/RAM/GPU instrumentadas |
|---|---|---|---|---:|---:|---|
| lectura_20261016_095108_269618_ventana_8s_r1.json | cpu | int8 | no (CPU) | 1.092 | 26.214 | no_medido_en_la_ejecucion_original |
| lectura_20261016_095108_269618_ventana_4s_r1.json | cpu | int8 | no (CPU) | 0.790 | 4.271 | no_medido_en_la_ejecucion_original |
| lectura_20261016_095108_269618_ventana_8s_r2.json | cpu | int8 | no (CPU) | 1.042 | 27.030 | no_medido_en_la_ejecucion_original |
| lectura_20261016_095108_269618_ventana_4s_r2.json | cpu | int8 | no (CPU) | 0.746 | 3.913 | no_medido_en_la_ejecucion_original |
| lectura_20261016_095108_269618_ventana_4s_r3.json | cpu | int8 | no (CPU) | 0.754 | 3.910 | no_medido_en_la_ejecucion_original |
| lectura_20261016_095108_269618_ventana_8s_r3.json | cpu | int8 | no (CPU) | 0.975 | 20.903 | no_medido_en_la_ejecucion_original |

Para comparar tablets habrá que medir en el dispositivo de destino: RAM máxima, tiempo de respuesta sostenido y consumo/batería. Este ordenador no permite deducir esos valores. No se cambia CPU por GPU automáticamente.
<!-- recursos-computo-fin -->

<!-- identidad-audio-inicio -->
## Audio utilizado

- **Lectura lenta · cuento 1 · 16/10/2026** — Lectura lenta - cuento 1 - 16-10-2026.wav
<!-- identidad-audio-fin -->
