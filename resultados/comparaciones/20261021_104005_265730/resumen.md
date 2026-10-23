# Comparación de reprocesamiento

3 ronda(s) por configuración, orden aleatorio reproducible por ronda. Ejecución secuencial para no competir por CPU. Tiempos orientativos, afectados por carga y calentamiento. No hay referencia humana de posición ni latencia visual. Comparar posiciones entre métodos no demuestra precisión.

Mismo modelo, CPU int8, VAD, bloques de 2 s, cuento y seguidor. La carga del modelo se excluye de los tiempos de inferencia. Solapamiento = ventana menos 2 s; no aplica al prefijo. El silencio final puede reducir los totales de las ventanas.

| Audio | Método | Ronda | Total inferencia (s) | Mediana (s) | P95 (s) | Inferencias >2 s | Cola máxima simulada (s) | Posición final | Retrocesos |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| lectura_20261021_103917_243241.wav | ventana_8s | 1 | 34.94 | 1.61 | 1.86 | 0 | 0.00 | 17 | 1 |
| lectura_20261021_103917_243241.wav | ventana_4s | 1 | 30.50 | 1.60 | 1.69 | 0 | 0.00 | 56 | 0 |
| lectura_20261021_103917_243241.wav | ventana_8s | 2 | 36.54 | 1.69 | 1.95 | 0 | 0.00 | 17 | 1 |
| lectura_20261021_103917_243241.wav | ventana_4s | 2 | 30.77 | 1.58 | 1.75 | 0 | 0.00 | 56 | 0 |
| lectura_20261021_103917_243241.wav | ventana_4s | 3 | 30.78 | 1.61 | 1.70 | 0 | 0.00 | 56 | 0 |
| lectura_20261021_103917_243241.wav | ventana_8s | 3 | 36.67 | 1.78 | 1.90 | 0 | 0.00 | 17 | 1 |

## Posiciones en cada actualización

Comparación descriptiva con el prefijo, no referencia de precisión. El prefijo también puede equivocarse.

### lectura_20261021_103917_243241.wav, ronda 1

| Audio disponible (s) | ventana_4s | ventana_8s |
|---:|---:|---:|
| 2.0 | 2 | 2 |
| 4.0 | 9 | 9 |
| 6.0 | 15 | 15 |
| 8.0 | 17 | 17 |
| 10.0 | 24 | 24 |
| 12.0 | 27 | 27 |
| 14.0 | 35 | 35 |
| 16.0 | 40 | 40 |
| 18.0 | 45 | 45 |
| 20.0 | 49 | 49 |
| 22.0 | 55 | 53 |
| 24.0 | 56 | 56 |
| 26.0 | 56 | 56 |
| 28.0 | 56 | 56 |
| 30.0 | 56 | 56 |
| 32.0 | 56 | 56 |
| 34.0 | 56 | 56 |
| 36.0 | 56 | 17 |
| 38.0 | 56 | 17 |
| 40.0 | 56 | 17 |
| 42.0 | 56 | 17 |
| 44.0 | 56 | 17 |
| 45.0 | 56 | 17 |

### lectura_20261021_103917_243241.wav, ronda 2

| Audio disponible (s) | ventana_4s | ventana_8s |
|---:|---:|---:|
| 2.0 | 2 | 2 |
| 4.0 | 9 | 9 |
| 6.0 | 15 | 15 |
| 8.0 | 17 | 17 |
| 10.0 | 24 | 24 |
| 12.0 | 27 | 27 |
| 14.0 | 35 | 35 |
| 16.0 | 40 | 40 |
| 18.0 | 45 | 45 |
| 20.0 | 49 | 49 |
| 22.0 | 55 | 53 |
| 24.0 | 56 | 56 |
| 26.0 | 56 | 56 |
| 28.0 | 56 | 56 |
| 30.0 | 56 | 56 |
| 32.0 | 56 | 56 |
| 34.0 | 56 | 56 |
| 36.0 | 56 | 17 |
| 38.0 | 56 | 17 |
| 40.0 | 56 | 17 |
| 42.0 | 56 | 17 |
| 44.0 | 56 | 17 |
| 45.0 | 56 | 17 |

### lectura_20261021_103917_243241.wav, ronda 3

| Audio disponible (s) | ventana_4s | ventana_8s |
|---:|---:|---:|
| 2.0 | 2 | 2 |
| 4.0 | 9 | 9 |
| 6.0 | 15 | 15 |
| 8.0 | 17 | 17 |
| 10.0 | 24 | 24 |
| 12.0 | 27 | 27 |
| 14.0 | 35 | 35 |
| 16.0 | 40 | 40 |
| 18.0 | 45 | 45 |
| 20.0 | 49 | 49 |
| 22.0 | 55 | 53 |
| 24.0 | 56 | 56 |
| 26.0 | 56 | 56 |
| 28.0 | 56 | 56 |
| 30.0 | 56 | 56 |
| 32.0 | 56 | 56 |
| 34.0 | 56 | 56 |
| 36.0 | 56 | 17 |
| 38.0 | 56 | 17 |
| 40.0 | 56 | 17 |
| 42.0 | 56 | 17 |
| 44.0 | 56 | 17 |
| 45.0 | 56 | 17 |

## Resumen por configuración

| Audio | Método | Total medio (s) | Rango de totales (s) | Cola máxima media (s) | Inferencias >2 s | Posiciones finales |
|---|---|---:|---|---:|---|---|
| lectura_20261021_103917_243241.wav | ventana_4s | 30.68 | 30.50–30.78 | 0.00 | 0/69 | [56, 56, 56] |
| lectura_20261021_103917_243241.wav | ventana_8s | 36.05 | 34.94–36.67 | 0.00 | 0/69 | [17, 17, 17] |

<!-- recursos-computo-inicio -->
## Recursos y coste computacional

Datos de la ejecución original. «No medido» no significa cero. RTF = suma de inferencias / duración del audio completo (incluye silencio); no es latencia visual ni mide captura, escritura o muestreo. Las rondas de una grabación no son lecturas independientes.

| Registro | Dispositivo ASR | Precisión | GPU para ASR | RTF | Máx. inferencia (s) | CPU/RAM/GPU instrumentadas |
|---|---|---|---|---:|---:|---|
| lectura_20261021_103917_243241_ventana_8s_r1.json | cpu | int8 | no (CPU) | 0.776 | 1.878 | no_medido_en_la_ejecucion_original |
| lectura_20261021_103917_243241_ventana_4s_r1.json | cpu | int8 | no (CPU) | 0.678 | 1.701 | no_medido_en_la_ejecucion_original |
| lectura_20261021_103917_243241_ventana_8s_r2.json | cpu | int8 | no (CPU) | 0.812 | 1.947 | no_medido_en_la_ejecucion_original |
| lectura_20261021_103917_243241_ventana_4s_r2.json | cpu | int8 | no (CPU) | 0.684 | 1.861 | no_medido_en_la_ejecucion_original |
| lectura_20261021_103917_243241_ventana_4s_r3.json | cpu | int8 | no (CPU) | 0.684 | 1.834 | no_medido_en_la_ejecucion_original |
| lectura_20261021_103917_243241_ventana_8s_r3.json | cpu | int8 | no (CPU) | 0.815 | 1.904 | no_medido_en_la_ejecucion_original |

Para comparar tablets habrá que medir en el dispositivo de destino: RAM máxima, tiempo de respuesta sostenido y consumo/batería. Este ordenador no permite deducir esos valores. No se cambia CPU por GPU automáticamente.
<!-- recursos-computo-fin -->

<!-- identidad-audio-inicio -->
## Audio utilizado

- **Relectura lejana: Cerca de un árbol… hasta azul · cuento 1 · 21/10/2026** — Lectura con relectura lejana (Cerca-azul) - cuento 1 - 21-10-2026.wav
<!-- identidad-audio-fin -->
