## Recursos y coste computacional

Datos de la ejecución original. «No medido» no significa cero. RTF = suma de inferencias / duración del audio completo (incluye silencio); no es latencia visual ni mide captura, escritura o muestreo. Las rondas de una grabación no son lecturas independientes.

| Registro | Dispositivo ASR | Precisión | GPU para ASR | RTF | Máx. inferencia (s) | CPU/RAM/GPU instrumentadas |
|---|---|---|---|---:|---:|---|
| lectura_20261014_081816_009646_prefijo.json | cpu | int8 | no (CPU) | 1.263 | 3.312 | no_medido_en_la_ejecucion_original |
| lectura_20261014_081816_009646_ventana_6s.json | cpu | int8 | no (CPU) | 0.648 | 2.078 | no_medido_en_la_ejecucion_original |
| lectura_20261014_081816_009646_ventana_10s.json | cpu | int8 | no (CPU) | 0.759 | 2.142 | no_medido_en_la_ejecucion_original |
| lectura_20261014_082953_219058_prefijo.json | cpu | int8 | no (CPU) | 1.491 | 4.674 | no_medido_en_la_ejecucion_original |
| lectura_20261014_082953_219058_ventana_6s.json | cpu | int8 | no (CPU) | 0.819 | 1.863 | no_medido_en_la_ejecucion_original |
| lectura_20261014_082953_219058_ventana_10s.json | cpu | int8 | no (CPU) | 0.967 | 2.257 | no_medido_en_la_ejecucion_original |

Para comparar tablets habrá que medir en el dispositivo de destino: RAM máxima, tiempo de respuesta sostenido y consumo/batería. Este ordenador no permite deducir esos valores. No se cambia CPU por GPU automáticamente.

<!-- identidad-audio-inicio -->
## Audio utilizado

- **Lectura normal · cuento 1 · 14/10/2026** — Lectura normal - cuento 1 - 14-10-2026.wav
- **Disfluencias: Ana repetida, omisión de despacio y mari… mariposa · cuento 1 · 14/10/2026** — Lectura con disfluencias (Ana repetida, sin despacio, mari-mariposa) - cuento 1 - 14-10-2026.wav
<!-- identidad-audio-fin -->
