# Comparación de reprocesamiento

Una ejecución por configuración en orden fijo. Tiempos orientativos, afectados por carga y calentamiento. No hay referencia humana de posición ni latencia visual. Comparar posiciones entre métodos no demuestra precisión.

Mismo modelo, CPU int8, VAD, bloques de 2 s, cuento y seguidor. La carga del modelo se excluye de los tiempos de inferencia. El solapamiento es 4 s en la ventana de 6 s y 8 s en la de 10 s.

| Audio | Método | Total inferencia (s) | Mediana (s) | P95 (s) | Inferencias >2 s | Cola máxima simulada (s) | Posición final | Retrocesos |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| lectura_20261014_082953_219058.wav | prefijo | 53.17 | 3.46 | 6.07 | 10 | 21.04 | 56 | 0 |
| lectura_20261014_082953_219058.wav | ventana_6s | 29.51 | 2.10 | 2.36 | 11 | 2.15 | 56 | 0 |
| lectura_20261014_082953_219058.wav | ventana_10s | 33.22 | 2.32 | 2.65 | 10 | 4.31 | 56 | 0 |

## Posiciones en cada actualización

Comparación descriptiva con el prefijo, no referencia de precisión. El prefijo también puede equivocarse.

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

<!-- recursos-computo-inicio -->
## Recursos y coste computacional

Datos de la ejecución original. «No medido» no significa cero. RTF = suma de inferencias / duración del audio completo (incluye silencio); no es latencia visual ni mide captura, escritura o muestreo. Las rondas de una grabación no son lecturas independientes.

| Registro | Dispositivo ASR | Precisión | GPU para ASR | RTF | Máx. inferencia (s) | CPU/RAM/GPU instrumentadas |
|---|---|---|---|---:|---:|---|
| lectura_20261014_082953_219058_prefijo.json | cpu | int8 | no (CPU) | 1.772 | 6.075 | no_medido_en_la_ejecucion_original |
| lectura_20261014_082953_219058_ventana_6s.json | cpu | int8 | no (CPU) | 0.984 | 2.365 | no_medido_en_la_ejecucion_original |
| lectura_20261014_082953_219058_ventana_10s.json | cpu | int8 | no (CPU) | 1.107 | 2.653 | no_medido_en_la_ejecucion_original |

Para comparar tablets habrá que medir en el dispositivo de destino: RAM máxima, tiempo de respuesta sostenido y consumo/batería. Este ordenador no permite deducir esos valores. No se cambia CPU por GPU automáticamente.
<!-- recursos-computo-fin -->

<!-- identidad-audio-inicio -->
## Audio utilizado

- **Disfluencias: Ana repetida, omisión de despacio y mari… mariposa · cuento 1 · 14/10/2026** — Lectura con disfluencias (Ana repetida, sin despacio, mari-mariposa) - cuento 1 - 14-10-2026.wav
<!-- identidad-audio-fin -->
