# Relectura lejana: contraste temporal humano

Anclas del propio lector, sin revisión independiente ni tiempos interiores de la frase. Salidas listas según cola secuencial simulada: no latencia visual medida; se reutilizan tiempos ASR y no se añade el coste de las variantes. La diferencia hasta rojo se cuenta desde su final humano; el primer retroceso desde el inicio de la frase. Se distingue la primera hipótesis del destino (puede usar palabra incompleta) de la primera con corte posterior a su final humano. Un valor negativo significa anticipación, no una demora nula. Sin nuevas inferencias ni cambios del seguidor.

| Ventana | Ronda | Variante | Retroceso listo (s) | Primer rojo listo (s) | Diferencia respecto al final humano (s) | Corte antes del final humano | Destino listo con corte posterior al final humano (s) |
|---:|---:|---|---:|---:|---:|---|---:|
| 8 | 1 | original | 43.51 | 43.51 | 3.56 | no | 43.51 |
| 8 | 1 | combinada | 43.51 | 43.51 | 3.56 | no | 43.51 |
| 8 | 1 | nueva | 37.48 | 41.58 | 1.63 | no | 41.58 |
| 4 | 1 | original | no detectado | no detectado | no detectado | no detectado | no detectado |
| 4 | 1 | combinada | no detectado | no detectado | no detectado | no detectado | no detectado |
| 4 | 1 | nueva | 41.58 | 41.58 | 1.63 | no | 41.58 |
| 8 | 2 | original | 43.65 | 43.65 | 3.70 | no | 43.65 |
| 8 | 2 | combinada | 43.65 | 43.65 | 3.70 | no | 43.65 |
| 8 | 2 | nueva | 37.64 | 41.60 | 1.65 | no | 41.60 |
| 4 | 2 | original | no detectado | no detectado | no detectado | no detectado | no detectado |
| 4 | 2 | combinada | no detectado | no detectado | no detectado | no detectado | no detectado |
| 4 | 2 | nueva | 41.63 | 41.63 | 1.68 | no | 41.63 |
| 4 | 3 | original | no detectado | no detectado | no detectado | no detectado | no detectado |
| 4 | 3 | combinada | no detectado | no detectado | no detectado | no detectado | no detectado |
| 4 | 3 | nueva | 42.20 | 42.20 | 2.25 | no | 42.20 |
| 8 | 3 | original | 43.75 | 43.75 | 3.80 | no | 43.75 |
| 8 | 3 | combinada | 43.75 | 43.75 | 3.80 | no | 43.75 |
| 8 | 3 | nueva | 37.63 | 41.64 | 1.69 | no | 41.64 |

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
