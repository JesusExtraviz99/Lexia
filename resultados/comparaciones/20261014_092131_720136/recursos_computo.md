## Recursos y coste computacional

Datos de la ejecución original. «No medido» no significa cero. RTF = suma de inferencias / duración del audio completo (incluye silencio); no es latencia visual ni mide captura, escritura o muestreo. Las rondas de una grabación no son lecturas independientes.

| Registro | Dispositivo ASR | Precisión | GPU para ASR | RTF | Máx. inferencia (s) | CPU/RAM/GPU instrumentadas |
|---|---|---|---|---:|---:|---|
| lectura_20261014_082953_219058_prefijo.json | cpu | int8 | no (CPU) | 1.772 | 6.075 | no_medido_en_la_ejecucion_original |
| lectura_20261014_082953_219058_ventana_6s.json | cpu | int8 | no (CPU) | 0.984 | 2.365 | no_medido_en_la_ejecucion_original |
| lectura_20261014_082953_219058_ventana_10s.json | cpu | int8 | no (CPU) | 1.107 | 2.653 | no_medido_en_la_ejecucion_original |

Para comparar tablets habrá que medir en el dispositivo de destino: RAM máxima, tiempo de respuesta sostenido y consumo/batería. Este ordenador no permite deducir esos valores. No se cambia CPU por GPU automáticamente.

<!-- identidad-audio-inicio -->
## Audio utilizado

- **Disfluencias: Ana repetida, omisión de despacio y mari… mariposa · cuento 1 · 14/10/2026** — Lectura con disfluencias (Ana repetida, sin despacio, mari-mariposa) - cuento 1 - 14-10-2026.wav
<!-- identidad-audio-fin -->
