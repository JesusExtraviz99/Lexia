# Relectura lejana: contraste temporal humano

Anclas del propio lector, sin revisión independiente ni tiempos interiores de la frase. Salidas listas según cola secuencial simulada: no latencia visual medida; se reutilizan tiempos ASR y no se añade el coste de las variantes. La diferencia hasta azul se cuenta desde su final humano; el primer retroceso desde el inicio de la frase. Se distingue la primera hipótesis del destino (puede usar palabra incompleta) de la primera con corte posterior a su final humano. Un valor negativo significa anticipación, no una demora nula. Sin nuevas inferencias ni cambios del seguidor.

| Ventana | Ronda | Variante | Retroceso listo (s) | Primer azul listo (s) | Diferencia respecto al final humano (s) | Corte antes del final humano | Destino listo con corte posterior al final humano (s) |
|---:|---:|---|---:|---:|---:|---|---:|
| 8 | 1 | original | 37.51 | 37.51 | 3.19 | no | 37.51 |
| 8 | 1 | combinada | 37.51 | 37.51 | 3.19 | no | 37.51 |
| 8 | 1 | nueva | 35.60 | 35.60 | 1.28 | sí | 37.51 |
| 4 | 1 | original | no detectado | no detectado | no detectado | no detectado | no detectado |
| 4 | 1 | combinada | no detectado | no detectado | no detectado | no detectado | no detectado |
| 4 | 1 | nueva | 29.53 | 35.57 | 1.25 | sí | 37.51 |
| 8 | 2 | original | 37.63 | 37.63 | 3.31 | no | 37.63 |
| 8 | 2 | combinada | 37.63 | 37.63 | 3.31 | no | 37.63 |
| 8 | 2 | nueva | 35.65 | 35.65 | 1.33 | sí | 37.63 |
| 4 | 2 | original | no detectado | no detectado | no detectado | no detectado | no detectado |
| 4 | 2 | combinada | no detectado | no detectado | no detectado | no detectado | no detectado |
| 4 | 2 | nueva | 29.52 | 35.58 | 1.26 | sí | 37.52 |
| 4 | 3 | original | no detectado | no detectado | no detectado | no detectado | no detectado |
| 4 | 3 | combinada | no detectado | no detectado | no detectado | no detectado | no detectado |
| 4 | 3 | nueva | 29.55 | 35.58 | 1.26 | sí | 37.51 |
| 8 | 3 | original | 37.58 | 37.58 | 3.26 | no | 37.58 |
| 8 | 3 | combinada | 37.58 | 37.58 | 3.26 | no | 37.58 |
| 8 | 3 | nueva | 35.87 | 35.87 | 1.55 | sí | 37.58 |

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
