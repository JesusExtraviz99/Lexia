# Comparación de cuatro seguidores

Comparación de cuatro seguidores sobre las mismas hipótesis guardadas. No hay nuevas inferencias ni nuevas grabaciones. Tiempos ASR/cola reutilizados, no mediciones nuevas de latencia total. Parámetros de ambas reglas sin cambios. Datos de desarrollo usados para diseñarlas; no demuestra generalización. Seguidor habitual sin activar variantes.

| Caso | Ventana | Ronda | Final original | Solo palabra | Solo temporal | Ambas | Cortes distintos original/ambas | Posiciones nuevas por interacción |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| normal | 6 | 1 | 56 | 56 | 56 | 56 | 0 | 0 |
| normal | 4 | 1 | 56 | 56 | 56 | 56 | 0 | 0 |
| normal | 8 | 1 | 56 | 56 | 56 | 56 | 0 | 0 |
| normal | 6 | 2 | 56 | 56 | 56 | 56 | 0 | 0 |
| normal | 4 | 2 | 56 | 56 | 56 | 56 | 0 | 0 |
| normal | 8 | 2 | 56 | 56 | 56 | 56 | 0 | 0 |
| normal | 4 | 3 | 56 | 56 | 56 | 56 | 0 | 0 |
| normal | 8 | 3 | 56 | 56 | 56 | 56 | 0 | 0 |
| normal | 6 | 3 | 56 | 56 | 56 | 56 | 0 | 0 |
| desviaciones | 8 | 1 | 56 | 56 | 56 | 56 | 0 | 0 |
| desviaciones | 6 | 1 | 56 | 56 | 56 | 56 | 0 | 0 |
| desviaciones | 4 | 1 | 56 | 56 | 56 | 56 | 0 | 0 |
| desviaciones | 4 | 2 | 56 | 56 | 56 | 56 | 0 | 0 |
| desviaciones | 6 | 2 | 56 | 56 | 56 | 56 | 0 | 0 |
| desviaciones | 8 | 2 | 56 | 56 | 56 | 56 | 0 | 0 |
| desviaciones | 8 | 3 | 56 | 56 | 56 | 56 | 0 | 0 |
| desviaciones | 4 | 3 | 56 | 56 | 56 | 56 | 0 | 0 |
| desviaciones | 6 | 3 | 56 | 56 | 56 | 56 | 0 | 0 |
| pausa | 8 | 1 | 56 | 56 | 56 | 56 | 0 | 0 |
| pausa | 4 | 1 | 56 | 56 | 56 | 56 | 0 | 0 |
| pausa | 8 | 2 | 56 | 56 | 56 | 56 | 0 | 0 |
| pausa | 4 | 2 | 56 | 56 | 56 | 56 | 0 | 0 |
| pausa | 4 | 3 | 56 | 56 | 56 | 56 | 0 | 0 |
| pausa | 8 | 3 | 56 | 56 | 56 | 56 | 0 | 0 |
| lenta | 8 | 1 | 55 | 55 | 56 | 56 | 6 | 0 |
| lenta | 4 | 1 | 53 | 53 | 53 | 53 | 2 | 0 |
| lenta | 8 | 2 | 55 | 55 | 56 | 56 | 6 | 0 |
| lenta | 4 | 2 | 53 | 53 | 53 | 53 | 2 | 0 |
| lenta | 4 | 3 | 53 | 53 | 53 | 53 | 2 | 0 |
| lenta | 8 | 3 | 55 | 55 | 56 | 56 | 6 | 0 |
| relectura | 8 | 1 | 56 | 56 | 56 | 56 | 0 | 0 |
| relectura | 4 | 1 | 56 | 56 | 56 | 56 | 0 | 0 |
| relectura | 8 | 2 | 56 | 56 | 56 | 56 | 0 | 0 |
| relectura | 4 | 2 | 56 | 56 | 56 | 56 | 0 | 0 |
| relectura | 4 | 3 | 56 | 56 | 56 | 56 | 0 | 0 |
| relectura | 8 | 3 | 56 | 56 | 56 | 56 | 0 | 0 |

## Cambios de posición con ambas reglas

lenta, ventana 8, ronda 1: palabra aislada []; retrocesos rechazados [80.0]; cambios [{'audio_seconds': 80.0, 'first': 55, 'second': 56}, {'audio_seconds': 82.0, 'first': 55, 'second': 56}, {'audio_seconds': 84.0, 'first': 55, 'second': 56}, {'audio_seconds': 86.0, 'first': 55, 'second': 56}, {'audio_seconds': 88.0, 'first': 55, 'second': 56}, {'audio_seconds': 90.0, 'first': 55, 'second': 56}]
lenta, ventana 4, ronda 1: palabra aislada [62.0]; retrocesos rechazados []; cambios [{'audio_seconds': 62.0, 'first': 45, 'second': 46}, {'audio_seconds': 64.0, 'first': 45, 'second': 46}]
lenta, ventana 8, ronda 2: palabra aislada []; retrocesos rechazados [80.0]; cambios [{'audio_seconds': 80.0, 'first': 55, 'second': 56}, {'audio_seconds': 82.0, 'first': 55, 'second': 56}, {'audio_seconds': 84.0, 'first': 55, 'second': 56}, {'audio_seconds': 86.0, 'first': 55, 'second': 56}, {'audio_seconds': 88.0, 'first': 55, 'second': 56}, {'audio_seconds': 90.0, 'first': 55, 'second': 56}]
lenta, ventana 4, ronda 2: palabra aislada [62.0]; retrocesos rechazados []; cambios [{'audio_seconds': 62.0, 'first': 45, 'second': 46}, {'audio_seconds': 64.0, 'first': 45, 'second': 46}]
lenta, ventana 4, ronda 3: palabra aislada [62.0]; retrocesos rechazados []; cambios [{'audio_seconds': 62.0, 'first': 45, 'second': 46}, {'audio_seconds': 64.0, 'first': 45, 'second': 46}]
lenta, ventana 8, ronda 3: palabra aislada []; retrocesos rechazados [80.0]; cambios [{'audio_seconds': 80.0, 'first': 55, 'second': 56}, {'audio_seconds': 82.0, 'first': 55, 'second': 56}, {'audio_seconds': 84.0, 'first': 55, 'second': 56}, {'audio_seconds': 86.0, 'first': 55, 'second': 56}, {'audio_seconds': 88.0, 'first': 55, 'second': 56}, {'audio_seconds': 90.0, 'first': 55, 'second': 56}]

No observar posiciones nuevas por interacción no demuestra independencia de las reglas ni ausencia universal de regresiones. Ver evaluaciones humanas por variante en resumen.json.

## Límite observado en una relectura sintética lejana

Caso sintético, no grabación adicional. La relectura apunta a 3. Al conservar 14, la búsqueda local empieza en 3 y solo contiene una de las tres palabras, insuficiente para aceptar el salto en esta actualización. El original en 13 todavía incluye sus y alas y acepta 3. No se prueba aquí la recuperación global posterior.

{'original': 3, 'palabra_aislada': 3, 'temporal': 14, 'combinada': 14}

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
| lectura_20261014_082953_219058_ventana_8s_r1.json | cpu | int8 | no (CPU) | 0.850 | 1.905 | no_medido_en_la_ejecucion_original |
| lectura_20261014_082953_219058_ventana_6s_r1.json | cpu | int8 | no (CPU) | 0.791 | 1.894 | no_medido_en_la_ejecucion_original |
| lectura_20261014_082953_219058_ventana_4s_r1.json | cpu | int8 | no (CPU) | 0.716 | 1.902 | no_medido_en_la_ejecucion_original |
| lectura_20261014_082953_219058_ventana_4s_r2.json | cpu | int8 | no (CPU) | 0.808 | 1.991 | no_medido_en_la_ejecucion_original |
| lectura_20261014_082953_219058_ventana_6s_r2.json | cpu | int8 | no (CPU) | 0.872 | 2.146 | no_medido_en_la_ejecucion_original |
| lectura_20261014_082953_219058_ventana_8s_r2.json | cpu | int8 | no (CPU) | 0.910 | 2.277 | no_medido_en_la_ejecucion_original |
| lectura_20261014_082953_219058_ventana_8s_r3.json | cpu | int8 | no (CPU) | 0.899 | 1.973 | no_medido_en_la_ejecucion_original |
| lectura_20261014_082953_219058_ventana_4s_r3.json | cpu | int8 | no (CPU) | 0.721 | 1.990 | no_medido_en_la_ejecucion_original |
| lectura_20261014_082953_219058_ventana_6s_r3.json | cpu | int8 | no (CPU) | 0.808 | 2.114 | no_medido_en_la_ejecucion_original |
| lectura_20261014_111454_984161_ventana_8s_r1.json | cpu | int8 | no (CPU) | 0.645 | 2.387 | no_medido_en_la_ejecucion_original |
| lectura_20261014_111454_984161_ventana_4s_r1.json | cpu | int8 | no (CPU) | 0.535 | 2.176 | no_medido_en_la_ejecucion_original |
| lectura_20261014_111454_984161_ventana_8s_r2.json | cpu | int8 | no (CPU) | 0.661 | 2.338 | no_medido_en_la_ejecucion_original |
| lectura_20261014_111454_984161_ventana_4s_r2.json | cpu | int8 | no (CPU) | 0.523 | 2.058 | no_medido_en_la_ejecucion_original |
| lectura_20261014_111454_984161_ventana_4s_r3.json | cpu | int8 | no (CPU) | 0.542 | 2.110 | no_medido_en_la_ejecucion_original |
| lectura_20261014_111454_984161_ventana_8s_r3.json | cpu | int8 | no (CPU) | 0.674 | 2.381 | no_medido_en_la_ejecucion_original |
| lectura_20261016_095108_269618_ventana_8s_r1.json | cpu | int8 | no (CPU) | 1.092 | 26.214 | no_medido_en_la_ejecucion_original |
| lectura_20261016_095108_269618_ventana_4s_r1.json | cpu | int8 | no (CPU) | 0.790 | 4.271 | no_medido_en_la_ejecucion_original |
| lectura_20261016_095108_269618_ventana_8s_r2.json | cpu | int8 | no (CPU) | 1.042 | 27.030 | no_medido_en_la_ejecucion_original |
| lectura_20261016_095108_269618_ventana_4s_r2.json | cpu | int8 | no (CPU) | 0.746 | 3.913 | no_medido_en_la_ejecucion_original |
| lectura_20261016_095108_269618_ventana_4s_r3.json | cpu | int8 | no (CPU) | 0.754 | 3.910 | no_medido_en_la_ejecucion_original |
| lectura_20261016_095108_269618_ventana_8s_r3.json | cpu | int8 | no (CPU) | 0.975 | 20.903 | no_medido_en_la_ejecucion_original |
| lectura_20261016_104151_933317_ventana_8s_r1.json | cpu | int8 | no (CPU) | 0.515 | 1.847 | no_medido_en_la_ejecucion_original |
| lectura_20261016_104151_933317_ventana_4s_r1.json | cpu | int8 | no (CPU) | 0.435 | 1.692 | no_medido_en_la_ejecucion_original |
| lectura_20261016_104151_933317_ventana_8s_r2.json | cpu | int8 | no (CPU) | 0.529 | 1.961 | no_medido_en_la_ejecucion_original |
| lectura_20261016_104151_933317_ventana_4s_r2.json | cpu | int8 | no (CPU) | 0.441 | 1.721 | no_medido_en_la_ejecucion_original |
| lectura_20261016_104151_933317_ventana_4s_r3.json | cpu | int8 | no (CPU) | 0.435 | 1.769 | no_medido_en_la_ejecucion_original |
| lectura_20261016_104151_933317_ventana_8s_r3.json | cpu | int8 | no (CPU) | 0.530 | 1.903 | no_medido_en_la_ejecucion_original |

Para comparar tablets habrá que medir en el dispositivo de destino: RAM máxima, tiempo de respuesta sostenido y consumo/batería. Este ordenador no permite deducir esos valores. No se cambia CPU por GPU automáticamente.
<!-- recursos-computo-fin -->

<!-- identidad-audio-inicio -->
## Audio utilizado

- **Lectura normal · cuento 1 · 14/10/2026** — Lectura normal - cuento 1 - 14-10-2026.wav
- **Disfluencias: Ana repetida, omisión de despacio y mari… mariposa · cuento 1 · 14/10/2026** — Lectura con disfluencias (Ana repetida, sin despacio, mari-mariposa) - cuento 1 - 14-10-2026.wav
- **Lectura con pausa entre flor y Ana · cuento 1 · 14/10/2026** — Lectura con pausa (flor-Ana) - cuento 1 - 14-10-2026.wav
- **Lectura lenta · cuento 1 · 16/10/2026** — Lectura lenta - cuento 1 - 16-10-2026.wav
- **Relectura de Los dos se quedaron en silencio · cuento 1 · 16/10/2026** — Lectura con relectura (Los dos se quedaron en silencio) - cuento 1 - 16-10-2026.wav
<!-- identidad-audio-fin -->
