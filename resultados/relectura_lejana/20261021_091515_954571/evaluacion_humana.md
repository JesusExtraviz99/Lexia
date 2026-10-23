# Relectura lejana: contraste temporal humano

Anclas del propio lector, sin revisión independiente ni tiempos interiores de la frase. Salidas listas según cola secuencial simulada: no latencia visual medida; se reutilizan tiempos ASR y no se añade el coste de las variantes. La demora hasta alas se cuenta desde su final humano; el primer retroceso se cuenta desde el inicio de Los. Sin nuevas inferencias ni cambios del seguidor.

| Ventana | Ronda | Variante | Corte del retroceso (s) | Retroceso listo (s) | Alas listo (s) | Demora tras final de alas (s) |
|---:|---:|---|---:|---:|---:|---:|
| 8 | 1 | original | 38.00 | 39.55 | 39.55 | 6.82 |
| 8 | 1 | combinada | 38.00 | 39.55 | 39.55 | 6.82 |
| 8 | 1 | nueva | 34.00 | 35.79 | 35.79 | 3.06 |
| 4 | 1 | original | no detectado | no detectado | no detectado | no detectado |
| 4 | 1 | combinada | no detectado | no detectado | no detectado | no detectado |
| 4 | 1 | nueva | 32.00 | 33.69 | 35.65 | 2.92 |
| 8 | 2 | original | 38.00 | 39.63 | 39.63 | 6.90 |
| 8 | 2 | combinada | 38.00 | 39.63 | 39.63 | 6.90 |
| 8 | 2 | nueva | 34.00 | 35.89 | 35.89 | 3.16 |
| 4 | 2 | original | no detectado | no detectado | no detectado | no detectado |
| 4 | 2 | combinada | no detectado | no detectado | no detectado | no detectado |
| 4 | 2 | nueva | 32.00 | 33.64 | 35.61 | 2.88 |
| 4 | 3 | original | no detectado | no detectado | no detectado | no detectado |
| 4 | 3 | combinada | no detectado | no detectado | no detectado | no detectado |
| 4 | 3 | nueva | 32.00 | 33.64 | 35.60 | 2.87 |
| 8 | 3 | original | 38.00 | 39.61 | 39.61 | 6.88 |
| 8 | 3 | combinada | 38.00 | 39.61 | 39.61 | 6.88 |
| 8 | 3 | nueva | 34.00 | 35.69 | 35.69 | 2.96 |

<!-- recursos-computo-inicio -->
## Recursos y coste computacional

Datos de la ejecución original. «No medido» no significa cero. RTF = suma de inferencias / duración del audio completo (incluye silencio); no es latencia visual ni mide captura, escritura o muestreo. Las rondas de una grabación no son lecturas independientes.

| Registro | Dispositivo ASR | Precisión | GPU para ASR | RTF | Máx. inferencia (s) | CPU/RAM/GPU instrumentadas |
|---|---|---|---|---:|---:|---|
| lectura_20261021_090304_259866_ventana_8s_r1.json | cpu | int8 | no (CPU) | 0.609 | 3.357 | no_medido_en_la_ejecucion_original |
| lectura_20261021_090304_259866_ventana_4s_r1.json | cpu | int8 | no (CPU) | 0.500 | 1.800 | no_medido_en_la_ejecucion_original |
| lectura_20261021_090304_259866_ventana_8s_r2.json | cpu | int8 | no (CPU) | 0.617 | 3.372 | no_medido_en_la_ejecucion_original |
| lectura_20261021_090304_259866_ventana_4s_r2.json | cpu | int8 | no (CPU) | 0.486 | 1.727 | no_medido_en_la_ejecucion_original |
| lectura_20261021_090304_259866_ventana_4s_r3.json | cpu | int8 | no (CPU) | 0.482 | 1.730 | no_medido_en_la_ejecucion_original |
| lectura_20261021_090304_259866_ventana_8s_r3.json | cpu | int8 | no (CPU) | 0.603 | 3.256 | no_medido_en_la_ejecucion_original |

Para comparar tablets habrá que medir en el dispositivo de destino: RAM máxima, tiempo de respuesta sostenido y consumo/batería. Este ordenador no permite deducir esos valores. No se cambia CPU por GPU automáticamente.
<!-- recursos-computo-fin -->
