# Comparación del seguidor: temporal

Experimento de desarrollo sobre hipótesis ASR fijas. Cambia solo el seguidor. ASR, ventanas, cortes y tiempos de inferencia permanecen reutilizados. Las métricas de salida visible son una comparación bajo esos tiempos, no latencia nueva medida. Una mejora en estos audios usados para diseñar la regla no prueba generalización. Variante no activada en seguir.py.

Solo para retrocesos: el final ASR de la última coincidencia exacta debe ser posterior a la marca de apoyo temporal ya aceptada. No se combina la regla de palabra aislada ni se usan tiempos humanos. Umbral sin tolerancia, provisional y sensible a errores de timestamps. Conserva la política original de no actualizar ante texto idéntico.

| Caso | Ventana | Ronda | Cortes con posición distinta | Aplicación de regla (audio s) | Final original | Final variante |
|---|---:|---:|---:|---|---:|---:|
| normal | 6 | 1 | 0 | [] | 56 | 56 |
| normal | 4 | 1 | 0 | [] | 56 | 56 |
| normal | 8 | 1 | 0 | [] | 56 | 56 |
| normal | 6 | 2 | 0 | [] | 56 | 56 |
| normal | 4 | 2 | 0 | [] | 56 | 56 |
| normal | 8 | 2 | 0 | [] | 56 | 56 |
| normal | 4 | 3 | 0 | [] | 56 | 56 |
| normal | 8 | 3 | 0 | [] | 56 | 56 |
| normal | 6 | 3 | 0 | [] | 56 | 56 |
| desviaciones | 8 | 1 | 0 | [] | 56 | 56 |
| desviaciones | 6 | 1 | 0 | [] | 56 | 56 |
| desviaciones | 4 | 1 | 0 | [] | 56 | 56 |
| desviaciones | 4 | 2 | 0 | [] | 56 | 56 |
| desviaciones | 6 | 2 | 0 | [] | 56 | 56 |
| desviaciones | 8 | 2 | 0 | [] | 56 | 56 |
| desviaciones | 8 | 3 | 0 | [] | 56 | 56 |
| desviaciones | 4 | 3 | 0 | [] | 56 | 56 |
| desviaciones | 6 | 3 | 0 | [] | 56 | 56 |
| pausa | 8 | 1 | 0 | [] | 56 | 56 |
| pausa | 4 | 1 | 0 | [] | 56 | 56 |
| pausa | 8 | 2 | 0 | [] | 56 | 56 |
| pausa | 4 | 2 | 0 | [] | 56 | 56 |
| pausa | 4 | 3 | 0 | [] | 56 | 56 |
| pausa | 8 | 3 | 0 | [] | 56 | 56 |
| lenta | 8 | 1 | 6 | [80.0] | 55 | 56 |
| lenta | 4 | 1 | 0 | [] | 53 | 53 |
| lenta | 8 | 2 | 6 | [80.0] | 55 | 56 |
| lenta | 4 | 2 | 0 | [] | 53 | 53 |
| lenta | 4 | 3 | 0 | [] | 53 | 53 |
| lenta | 8 | 3 | 6 | [80.0] | 55 | 56 |
| relectura | 8 | 1 | 0 | [] | 56 | 56 |
| relectura | 4 | 1 | 0 | [] | 56 | 56 |
| relectura | 8 | 2 | 0 | [] | 56 | 56 |
| relectura | 4 | 2 | 0 | [] | 56 | 56 |
| relectura | 4 | 3 | 0 | [] | 56 | 56 |
| relectura | 8 | 3 | 0 | [] | 56 | 56 |

Los JSON de resumen conservan las métricas humanas por variante y los cortes modificados. En desviaciones solo se compara el comportamiento; no se inventa una referencia temporal. Los registros originales permanecen intactos.

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
