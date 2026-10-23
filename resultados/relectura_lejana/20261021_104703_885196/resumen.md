# Relectura lejana: comparación de seguidores

Reproducción de hipótesis fijas, sin nuevas inferencias. Cortes de audio y salida lista simulada son distintos. Sin referencia humana temporal: no se calcula latencia respecto a la lectura ni precisión. Reglas sin modificar ni activar.

| Ventana | Ronda | Final original / combinada / nueva | Cortes distintos combinada–nueva | Recuperación exacta (corte s) |
|---:|---:|---|---|---|
| 8 | 1 | 17 / 17 / 17 | [34.0] | [34.0] |
| 4 | 1 | 56 / 56 / 17 | [28.0, 30.0, 32.0, 34.0, 36.0, 38.0, 40.0, 42.0, 44.0, 45.0] | [28.0] |
| 8 | 2 | 17 / 17 / 17 | [34.0] | [34.0] |
| 4 | 2 | 56 / 56 / 17 | [28.0, 30.0, 32.0, 34.0, 36.0, 38.0, 40.0, 42.0, 44.0, 45.0] | [28.0] |
| 4 | 3 | 56 / 56 / 17 | [28.0, 30.0, 32.0, 34.0, 36.0, 38.0, 40.0, 42.0, 44.0, 45.0] | [28.0] |
| 8 | 3 | 17 / 17 / 17 | [34.0] | [34.0] |

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
