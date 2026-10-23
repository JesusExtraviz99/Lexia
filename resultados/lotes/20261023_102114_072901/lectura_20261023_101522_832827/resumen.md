# Comparación de reprocesamiento

3 ronda(s) por configuración, orden aleatorio reproducible por ronda. Ejecución secuencial para no competir por CPU. Tiempos orientativos, afectados por carga y calentamiento. No hay referencia humana de posición ni latencia visual. Comparar posiciones entre métodos no demuestra precisión.

Mismo modelo, CPU int8, VAD, bloques de 2 s, cuento y seguidor. La carga del modelo se excluye de los tiempos de inferencia. Solapamiento = ventana menos 2 s; no aplica al prefijo. El silencio final puede reducir los totales de las ventanas.

| Audio | Método | Ronda | Total inferencia (s) | Mediana (s) | P95 (s) | Inferencias >2 s | Cola máxima simulada (s) | Posición final | Retrocesos |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Lectura con muchas trabadas - cuento 2 - lectura_02 - 23-10-2026.wav | ventana_8s | 1 | 63.04 | 1.74 | 1.85 | 1 | 10.63 | 56 | 0 |
| Lectura con muchas trabadas - cuento 2 - lectura_02 - 23-10-2026.wav | ventana_4s | 1 | 58.89 | 1.70 | 4.43 | 2 | 5.05 | 56 | 0 |
| Lectura con muchas trabadas - cuento 2 - lectura_02 - 23-10-2026.wav | ventana_8s | 2 | 62.11 | 1.78 | 1.92 | 1 | 8.42 | 56 | 0 |
| Lectura con muchas trabadas - cuento 2 - lectura_02 - 23-10-2026.wav | ventana_4s | 2 | 62.62 | 1.72 | 4.27 | 2 | 8.66 | 56 | 0 |
| Lectura con muchas trabadas - cuento 2 - lectura_02 - 23-10-2026.wav | ventana_4s | 3 | 63.93 | 1.73 | 4.03 | 2 | 9.30 | 56 | 0 |
| Lectura con muchas trabadas - cuento 2 - lectura_02 - 23-10-2026.wav | ventana_8s | 3 | 63.99 | 1.86 | 1.92 | 1 | 8.40 | 56 | 0 |

## Posiciones en cada actualización

Comparación descriptiva con el prefijo, no referencia de precisión. El prefijo también puede equivocarse.

### Lectura con muchas trabadas - cuento 2 - lectura_02 - 23-10-2026.wav, ronda 1

| Audio disponible (s) | ventana_4s | ventana_8s |
|---:|---:|---:|
| 2.0 | — | — |
| 4.0 | — | — |
| 6.0 | 5 | — |
| 8.0 | 7 | 7 |
| 10.0 | 10 | 10 |
| 12.0 | 12 | 12 |
| 14.0 | 13 | 13 |
| 16.0 | 13 | 14 |
| 18.0 | 13 | 15 |
| 20.0 | 16 | 15 |
| 22.0 | 19 | 19 |
| 24.0 | 21 | 21 |
| 26.0 | 22 | 22 |
| 28.0 | 23 | 23 |
| 30.0 | 26 | 26 |
| 32.0 | 26 | 28 |
| 34.0 | 30 | 30 |
| 36.0 | 34 | 34 |
| 38.0 | 35 | 35 |
| 40.0 | 38 | 38 |
| 42.0 | 40 | 40 |
| 44.0 | 42 | 42 |
| 46.0 | 45 | 45 |
| 48.0 | 46 | 46 |
| 50.0 | 46 | 48 |
| 52.0 | 50 | 50 |
| 54.0 | 53 | 53 |
| 56.0 | 56 | 56 |
| 58.0 | 56 | 56 |
| 60.0 | 56 | 56 |

### Lectura con muchas trabadas - cuento 2 - lectura_02 - 23-10-2026.wav, ronda 2

| Audio disponible (s) | ventana_4s | ventana_8s |
|---:|---:|---:|
| 2.0 | — | — |
| 4.0 | — | — |
| 6.0 | 5 | — |
| 8.0 | 7 | 7 |
| 10.0 | 10 | 10 |
| 12.0 | 12 | 12 |
| 14.0 | 13 | 13 |
| 16.0 | 13 | 14 |
| 18.0 | 13 | 15 |
| 20.0 | 16 | 15 |
| 22.0 | 19 | 19 |
| 24.0 | 21 | 21 |
| 26.0 | 22 | 22 |
| 28.0 | 23 | 23 |
| 30.0 | 26 | 26 |
| 32.0 | 26 | 28 |
| 34.0 | 30 | 30 |
| 36.0 | 34 | 34 |
| 38.0 | 35 | 35 |
| 40.0 | 38 | 38 |
| 42.0 | 40 | 40 |
| 44.0 | 42 | 42 |
| 46.0 | 45 | 45 |
| 48.0 | 46 | 46 |
| 50.0 | 46 | 48 |
| 52.0 | 50 | 50 |
| 54.0 | 53 | 53 |
| 56.0 | 56 | 56 |
| 58.0 | 56 | 56 |
| 60.0 | 56 | 56 |

### Lectura con muchas trabadas - cuento 2 - lectura_02 - 23-10-2026.wav, ronda 3

| Audio disponible (s) | ventana_4s | ventana_8s |
|---:|---:|---:|
| 2.0 | — | — |
| 4.0 | — | — |
| 6.0 | 5 | — |
| 8.0 | 7 | 7 |
| 10.0 | 10 | 10 |
| 12.0 | 12 | 12 |
| 14.0 | 13 | 13 |
| 16.0 | 13 | 14 |
| 18.0 | 13 | 15 |
| 20.0 | 16 | 15 |
| 22.0 | 19 | 19 |
| 24.0 | 21 | 21 |
| 26.0 | 22 | 22 |
| 28.0 | 23 | 23 |
| 30.0 | 26 | 26 |
| 32.0 | 26 | 28 |
| 34.0 | 30 | 30 |
| 36.0 | 34 | 34 |
| 38.0 | 35 | 35 |
| 40.0 | 38 | 38 |
| 42.0 | 40 | 40 |
| 44.0 | 42 | 42 |
| 46.0 | 45 | 45 |
| 48.0 | 46 | 46 |
| 50.0 | 46 | 48 |
| 52.0 | 50 | 50 |
| 54.0 | 53 | 53 |
| 56.0 | 56 | 56 |
| 58.0 | 56 | 56 |
| 60.0 | 56 | 56 |

## Resumen por configuración

| Audio | Método | Total medio (s) | Rango de totales (s) | Cola máxima media (s) | Inferencias >2 s | Posiciones finales |
|---|---|---:|---|---:|---|---|
| Lectura con muchas trabadas - cuento 2 - lectura_02 - 23-10-2026.wav | ventana_4s | 61.81 | 58.89–63.93 | 7.67 | 6/90 | [56, 56, 56] |
| Lectura con muchas trabadas - cuento 2 - lectura_02 - 23-10-2026.wav | ventana_8s | 63.05 | 62.11–63.99 | 9.15 | 3/90 | [56, 56, 56] |

<!-- recursos-computo-inicio -->
## Recursos y coste computacional

Datos de la ejecución original. «No medido» no significa cero. RTF = suma de inferencias / duración del audio completo (incluye silencio); no es latencia visual ni mide captura, escritura o muestreo. Las rondas de una grabación no son lecturas independientes.

| Registro | Dispositivo ASR | Precisión | GPU para ASR | RTF | Máx. inferencia (s) | CPU/RAM/GPU instrumentadas |
|---|---|---|---|---:|---:|---|
| lectura_20261023_101522_832827_ventana_8s_r1.json | cpu | int8 | no (CPU) | 1.051 | 12.628 | medido |

**lectura_20261023_101522_832827_ventana_8s_r1.json:** CPU 11th Gen Intel(R) Core(TM) i7-11800H @ 2.30GHz; 16 procesadores lógicos; Windows-11-10.0.26200-SP0. CPU media del proceso: 24.818% de capacidad lógica del equipo. Pico de RAM del proceso durante su vida: 990.340 MiB. Carga del modelo: 1.376 s.

CPU y RAM del proceso completo, incluido muestreo. CPU 100% equivale a un procesador lógico; puede superar 100%. GPU/VRAM/potencia/temperatura son del equipo completo, no del ASR. No se mide energía específica, FLOPs ni rendimiento de tablet. Intervalos reales registrados, máximos muestreados no garantizan pico. Muestreo separado de inferencia; puede influir en la carga.

Las muestras completas de RAM, uso de GPU, VRAM, potencia y temperatura disponibles están en el JSON de recursos. La potencia GPU global en vatios no equivale al consumo energético del ASR.

| GPU global | Muestras | Uso medio / máx. (%) | VRAM máx. (MiB) | Potencia media / máx. (W) | Temperatura máx. (°C) |
|---|---:|---|---:|---|---:|
| NVIDIA GeForce RTX 3050 Laptop GPU | 58 | 0.000 / 0.000 | 481.000 | 6.350 / 6.380 | 45.000 |
| lectura_20261023_101522_832827_ventana_4s_r1.json | cpu | int8 | no (CPU) | 0.982 | 6.696 | medido |

**lectura_20261023_101522_832827_ventana_4s_r1.json:** CPU 11th Gen Intel(R) Core(TM) i7-11800H @ 2.30GHz; 16 procesadores lógicos; Windows-11-10.0.26200-SP0. CPU media del proceso: 24.974% de capacidad lógica del equipo. Pico de RAM del proceso durante su vida: 965.281 MiB. Carga del modelo: 0.914 s.

CPU y RAM del proceso completo, incluido muestreo. CPU 100% equivale a un procesador lógico; puede superar 100%. GPU/VRAM/potencia/temperatura son del equipo completo, no del ASR. No se mide energía específica, FLOPs ni rendimiento de tablet. Intervalos reales registrados, máximos muestreados no garantizan pico. Muestreo separado de inferencia; puede influir en la carga.

Las muestras completas de RAM, uso de GPU, VRAM, potencia y temperatura disponibles están en el JSON de recursos. La potencia GPU global en vatios no equivale al consumo energético del ASR.

| GPU global | Muestras | Uso medio / máx. (%) | VRAM máx. (MiB) | Potencia media / máx. (W) | Temperatura máx. (°C) |
|---|---:|---|---:|---|---:|
| NVIDIA GeForce RTX 3050 Laptop GPU | 54 | 0.000 / 0.000 | 481.000 | 6.361 / 6.430 | 45.000 |
| lectura_20261023_101522_832827_ventana_8s_r2.json | cpu | int8 | no (CPU) | 1.035 | 10.418 | medido |

**lectura_20261023_101522_832827_ventana_8s_r2.json:** CPU 11th Gen Intel(R) Core(TM) i7-11800H @ 2.30GHz; 16 procesadores lógicos; Windows-11-10.0.26200-SP0. CPU media del proceso: 24.924% de capacidad lógica del equipo. Pico de RAM del proceso durante su vida: 1046.953 MiB. Carga del modelo: 0.963 s.

CPU y RAM del proceso completo, incluido muestreo. CPU 100% equivale a un procesador lógico; puede superar 100%. GPU/VRAM/potencia/temperatura son del equipo completo, no del ASR. No se mide energía específica, FLOPs ni rendimiento de tablet. Intervalos reales registrados, máximos muestreados no garantizan pico. Muestreo separado de inferencia; puede influir en la carga.

Las muestras completas de RAM, uso de GPU, VRAM, potencia y temperatura disponibles están en el JSON de recursos. La potencia GPU global en vatios no equivale al consumo energético del ASR.

| GPU global | Muestras | Uso medio / máx. (%) | VRAM máx. (MiB) | Potencia media / máx. (W) | Temperatura máx. (°C) |
|---|---:|---|---:|---|---:|
| NVIDIA GeForce RTX 3050 Laptop GPU | 57 | 0.000 / 0.000 | 481.000 | 6.365 / 6.410 | 45.000 |
| lectura_20261023_101522_832827_ventana_4s_r2.json | cpu | int8 | no (CPU) | 1.044 | 10.467 | medido |

**lectura_20261023_101522_832827_ventana_4s_r2.json:** CPU 11th Gen Intel(R) Core(TM) i7-11800H @ 2.30GHz; 16 procesadores lógicos; Windows-11-10.0.26200-SP0. CPU media del proceso: 24.965% de capacidad lógica del equipo. Pico de RAM del proceso durante su vida: 1045.930 MiB. Carga del modelo: 0.973 s.

CPU y RAM del proceso completo, incluido muestreo. CPU 100% equivale a un procesador lógico; puede superar 100%. GPU/VRAM/potencia/temperatura son del equipo completo, no del ASR. No se mide energía específica, FLOPs ni rendimiento de tablet. Intervalos reales registrados, máximos muestreados no garantizan pico. Muestreo separado de inferencia; puede influir en la carga.

Las muestras completas de RAM, uso de GPU, VRAM, potencia y temperatura disponibles están en el JSON de recursos. La potencia GPU global en vatios no equivale al consumo energético del ASR.

| GPU global | Muestras | Uso medio / máx. (%) | VRAM máx. (MiB) | Potencia media / máx. (W) | Temperatura máx. (°C) |
|---|---:|---|---:|---|---:|
| NVIDIA GeForce RTX 3050 Laptop GPU | 57 | 0.000 / 0.000 | 481.000 | 6.347 / 6.390 | 45.000 |
| lectura_20261023_101522_832827_ventana_4s_r3.json | cpu | int8 | no (CPU) | 1.065 | 11.305 | medido |

**lectura_20261023_101522_832827_ventana_4s_r3.json:** CPU 11th Gen Intel(R) Core(TM) i7-11800H @ 2.30GHz; 16 procesadores lógicos; Windows-11-10.0.26200-SP0. CPU media del proceso: 24.945% de capacidad lógica del equipo. Pico de RAM del proceso durante su vida: 992.559 MiB. Carga del modelo: 0.996 s.

CPU y RAM del proceso completo, incluido muestreo. CPU 100% equivale a un procesador lógico; puede superar 100%. GPU/VRAM/potencia/temperatura son del equipo completo, no del ASR. No se mide energía específica, FLOPs ni rendimiento de tablet. Intervalos reales registrados, máximos muestreados no garantizan pico. Muestreo separado de inferencia; puede influir en la carga.

Las muestras completas de RAM, uso de GPU, VRAM, potencia y temperatura disponibles están en el JSON de recursos. La potencia GPU global en vatios no equivale al consumo energético del ASR.

| GPU global | Muestras | Uso medio / máx. (%) | VRAM máx. (MiB) | Potencia media / máx. (W) | Temperatura máx. (°C) |
|---|---:|---|---:|---|---:|
| NVIDIA GeForce RTX 3050 Laptop GPU | 58 | 0.000 / 0.000 | 481.000 | 6.368 / 6.400 | 45.000 |
| lectura_20261023_101522_832827_ventana_8s_r3.json | cpu | int8 | no (CPU) | 1.067 | 10.398 | medido |

**lectura_20261023_101522_832827_ventana_8s_r3.json:** CPU 11th Gen Intel(R) Core(TM) i7-11800H @ 2.30GHz; 16 procesadores lógicos; Windows-11-10.0.26200-SP0. CPU media del proceso: 24.887% de capacidad lógica del equipo. Pico de RAM del proceso durante su vida: 1055.250 MiB. Carga del modelo: 1.061 s.

CPU y RAM del proceso completo, incluido muestreo. CPU 100% equivale a un procesador lógico; puede superar 100%. GPU/VRAM/potencia/temperatura son del equipo completo, no del ASR. No se mide energía específica, FLOPs ni rendimiento de tablet. Intervalos reales registrados, máximos muestreados no garantizan pico. Muestreo separado de inferencia; puede influir en la carga.

Las muestras completas de RAM, uso de GPU, VRAM, potencia y temperatura disponibles están en el JSON de recursos. La potencia GPU global en vatios no equivale al consumo energético del ASR.

| GPU global | Muestras | Uso medio / máx. (%) | VRAM máx. (MiB) | Potencia media / máx. (W) | Temperatura máx. (°C) |
|---|---:|---|---:|---|---:|
| NVIDIA GeForce RTX 3050 Laptop GPU | 58 | 0.000 / 0.000 | 481.000 | 6.361 / 6.430 | 45.000 |

Para comparar tablets habrá que medir en el dispositivo de destino: RAM máxima, tiempo de respuesta sostenido y consumo/batería. Este ordenador no permite deducir esos valores. No se cambia CPU por GPU automáticamente.
<!-- recursos-computo-fin -->
