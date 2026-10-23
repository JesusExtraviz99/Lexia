# Comparación de reprocesamiento

3 ronda(s) por configuración, orden aleatorio reproducible por ronda. Ejecución secuencial para no competir por CPU. Tiempos orientativos, afectados por carga y calentamiento. No hay referencia humana de posición ni latencia visual. Comparar posiciones entre métodos no demuestra precisión.

Mismo modelo, CPU int8, VAD, bloques de 2 s, cuento y seguidor. La carga del modelo se excluye de los tiempos de inferencia. Solapamiento = ventana menos 2 s; no aplica al prefijo. El silencio final puede reducir los totales de las ventanas.

| Audio | Método | Ronda | Total inferencia (s) | Mediana (s) | P95 (s) | Inferencias >2 s | Cola máxima simulada (s) | Posición final | Retrocesos |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Lectura omisión abuelo - cuento 2 - lectura_02 - 23-10-2026.wav | ventana_8s | 1 | 39.44 | 2.29 | 2.62 | 16 | 5.43 | 56 | 0 |
| Lectura omisión abuelo - cuento 2 - lectura_02 - 23-10-2026.wav | ventana_4s | 1 | 31.13 | 1.98 | 2.24 | 9 | 1.26 | 56 | 0 |
| Lectura omisión abuelo - cuento 2 - lectura_02 - 23-10-2026.wav | ventana_8s | 2 | 43.76 | 2.51 | 2.96 | 17 | 9.70 | 56 | 0 |
| Lectura omisión abuelo - cuento 2 - lectura_02 - 23-10-2026.wav | ventana_4s | 2 | 25.72 | 1.68 | 1.83 | 0 | 0.00 | 56 | 0 |
| Lectura omisión abuelo - cuento 2 - lectura_02 - 23-10-2026.wav | ventana_4s | 3 | 25.42 | 1.64 | 1.81 | 0 | 0.00 | 56 | 0 |
| Lectura omisión abuelo - cuento 2 - lectura_02 - 23-10-2026.wav | ventana_8s | 3 | 30.54 | 1.81 | 1.96 | 0 | 0.00 | 56 | 0 |

## Posiciones en cada actualización

Comparación descriptiva con el prefijo, no referencia de precisión. El prefijo también puede equivocarse.

### Lectura omisión abuelo - cuento 2 - lectura_02 - 23-10-2026.wav, ronda 1

| Audio disponible (s) | ventana_4s | ventana_8s |
|---:|---:|---:|
| 2.0 | 2 | 2 |
| 4.0 | 5 | 5 |
| 6.0 | 9 | 9 |
| 8.0 | 16 | 16 |
| 10.0 | 19 | 19 |
| 12.0 | 23 | 23 |
| 14.0 | 26 | 27 |
| 16.0 | 30 | 30 |
| 18.0 | 35 | 35 |
| 20.0 | 40 | 40 |
| 22.0 | 46 | 46 |
| 24.0 | 48 | 47 |
| 26.0 | 53 | 53 |
| 28.0 | 56 | 56 |
| 30.0 | 56 | 56 |
| 32.0 | 56 | 56 |
| 34.0 | 56 | 56 |
| 36.0 | 56 | 56 |
| 38.0 | 56 | 56 |
| 40.0 | 56 | 56 |

### Lectura omisión abuelo - cuento 2 - lectura_02 - 23-10-2026.wav, ronda 2

| Audio disponible (s) | ventana_4s | ventana_8s |
|---:|---:|---:|
| 2.0 | 2 | 2 |
| 4.0 | 5 | 5 |
| 6.0 | 9 | 9 |
| 8.0 | 16 | 16 |
| 10.0 | 19 | 19 |
| 12.0 | 23 | 23 |
| 14.0 | 26 | 27 |
| 16.0 | 30 | 30 |
| 18.0 | 35 | 35 |
| 20.0 | 40 | 40 |
| 22.0 | 46 | 46 |
| 24.0 | 48 | 47 |
| 26.0 | 53 | 53 |
| 28.0 | 56 | 56 |
| 30.0 | 56 | 56 |
| 32.0 | 56 | 56 |
| 34.0 | 56 | 56 |
| 36.0 | 56 | 56 |
| 38.0 | 56 | 56 |
| 40.0 | 56 | 56 |

### Lectura omisión abuelo - cuento 2 - lectura_02 - 23-10-2026.wav, ronda 3

| Audio disponible (s) | ventana_4s | ventana_8s |
|---:|---:|---:|
| 2.0 | 2 | 2 |
| 4.0 | 5 | 5 |
| 6.0 | 9 | 9 |
| 8.0 | 16 | 16 |
| 10.0 | 19 | 19 |
| 12.0 | 23 | 23 |
| 14.0 | 26 | 27 |
| 16.0 | 30 | 30 |
| 18.0 | 35 | 35 |
| 20.0 | 40 | 40 |
| 22.0 | 46 | 46 |
| 24.0 | 48 | 47 |
| 26.0 | 53 | 53 |
| 28.0 | 56 | 56 |
| 30.0 | 56 | 56 |
| 32.0 | 56 | 56 |
| 34.0 | 56 | 56 |
| 36.0 | 56 | 56 |
| 38.0 | 56 | 56 |
| 40.0 | 56 | 56 |

## Resumen por configuración

| Audio | Método | Total medio (s) | Rango de totales (s) | Cola máxima media (s) | Inferencias >2 s | Posiciones finales |
|---|---|---:|---|---:|---|---|
| Lectura omisión abuelo - cuento 2 - lectura_02 - 23-10-2026.wav | ventana_4s | 27.42 | 25.42–31.13 | 0.42 | 9/60 | [56, 56, 56] |
| Lectura omisión abuelo - cuento 2 - lectura_02 - 23-10-2026.wav | ventana_8s | 37.91 | 30.54–43.76 | 5.04 | 33/60 | [56, 56, 56] |

<!-- recursos-computo-inicio -->
## Recursos y coste computacional

Datos de la ejecución original. «No medido» no significa cero. RTF = suma de inferencias / duración del audio completo (incluye silencio); no es latencia visual ni mide captura, escritura o muestreo. Las rondas de una grabación no son lecturas independientes.

| Registro | Dispositivo ASR | Precisión | GPU para ASR | RTF | Máx. inferencia (s) | CPU/RAM/GPU instrumentadas |
|---|---|---|---|---:|---:|---|
| lectura_20261023_101713_339466_ventana_8s_r1.json | cpu | int8 | no (CPU) | 0.986 | 2.764 | medido |

**lectura_20261023_101713_339466_ventana_8s_r1.json:** CPU 11th Gen Intel(R) Core(TM) i7-11800H @ 2.30GHz; 16 procesadores lógicos; Windows-11-10.0.26200-SP0. CPU media del proceso: 24.246% de capacidad lógica del equipo. Pico de RAM del proceso durante su vida: 702.777 MiB. Carga del modelo: 1.511 s.

CPU y RAM del proceso completo, incluido muestreo. CPU 100% equivale a un procesador lógico; puede superar 100%. GPU/VRAM/potencia/temperatura son del equipo completo, no del ASR. No se mide energía específica, FLOPs ni rendimiento de tablet. Intervalos reales registrados, máximos muestreados no garantizan pico. Muestreo separado de inferencia; puede influir en la carga.

Las muestras completas de RAM, uso de GPU, VRAM, potencia y temperatura disponibles están en el JSON de recursos. La potencia GPU global en vatios no equivale al consumo energético del ASR.

| GPU global | Muestras | Uso medio / máx. (%) | VRAM máx. (MiB) | Potencia media / máx. (W) | Temperatura máx. (°C) |
|---|---:|---|---:|---|---:|
| NVIDIA GeForce RTX 3050 Laptop GPU | 36 | 0.000 / 0.000 | 481.000 | 6.338 / 6.360 | 45.000 |
| lectura_20261023_101713_339466_ventana_4s_r1.json | cpu | int8 | no (CPU) | 0.778 | 2.482 | medido |

**lectura_20261023_101713_339466_ventana_4s_r1.json:** CPU 11th Gen Intel(R) Core(TM) i7-11800H @ 2.30GHz; 16 procesadores lógicos; Windows-11-10.0.26200-SP0. CPU media del proceso: 24.411% de capacidad lógica del equipo. Pico de RAM del proceso durante su vida: 702.727 MiB. Carga del modelo: 1.114 s.

CPU y RAM del proceso completo, incluido muestreo. CPU 100% equivale a un procesador lógico; puede superar 100%. GPU/VRAM/potencia/temperatura son del equipo completo, no del ASR. No se mide energía específica, FLOPs ni rendimiento de tablet. Intervalos reales registrados, máximos muestreados no garantizan pico. Muestreo separado de inferencia; puede influir en la carga.

Las muestras completas de RAM, uso de GPU, VRAM, potencia y temperatura disponibles están en el JSON de recursos. La potencia GPU global en vatios no equivale al consumo energético del ASR.

| GPU global | Muestras | Uso medio / máx. (%) | VRAM máx. (MiB) | Potencia media / máx. (W) | Temperatura máx. (°C) |
|---|---:|---|---:|---|---:|
| NVIDIA GeForce RTX 3050 Laptop GPU | 29 | 0.000 / 0.000 | 481.000 | 6.364 / 6.390 | 46.000 |
| lectura_20261023_101713_339466_ventana_8s_r2.json | cpu | int8 | no (CPU) | 1.094 | 3.158 | medido |

**lectura_20261023_101713_339466_ventana_8s_r2.json:** CPU 11th Gen Intel(R) Core(TM) i7-11800H @ 2.30GHz; 16 procesadores lógicos; Windows-11-10.0.26200-SP0. CPU media del proceso: 24.236% de capacidad lógica del equipo. Pico de RAM del proceso durante su vida: 702.723 MiB. Carga del modelo: 1.080 s.

CPU y RAM del proceso completo, incluido muestreo. CPU 100% equivale a un procesador lógico; puede superar 100%. GPU/VRAM/potencia/temperatura son del equipo completo, no del ASR. No se mide energía específica, FLOPs ni rendimiento de tablet. Intervalos reales registrados, máximos muestreados no garantizan pico. Muestreo separado de inferencia; puede influir en la carga.

Las muestras completas de RAM, uso de GPU, VRAM, potencia y temperatura disponibles están en el JSON de recursos. La potencia GPU global en vatios no equivale al consumo energético del ASR.

| GPU global | Muestras | Uso medio / máx. (%) | VRAM máx. (MiB) | Potencia media / máx. (W) | Temperatura máx. (°C) |
|---|---:|---|---:|---|---:|
| NVIDIA GeForce RTX 3050 Laptop GPU | 39 | 0.000 / 0.000 | 481.000 | 6.367 / 6.380 | 46.000 |
| lectura_20261023_101713_339466_ventana_4s_r2.json | cpu | int8 | no (CPU) | 0.643 | 1.847 | medido |

**lectura_20261023_101713_339466_ventana_4s_r2.json:** CPU 11th Gen Intel(R) Core(TM) i7-11800H @ 2.30GHz; 16 procesadores lógicos; Windows-11-10.0.26200-SP0. CPU media del proceso: 24.798% de capacidad lógica del equipo. Pico de RAM del proceso durante su vida: 702.777 MiB. Carga del modelo: 1.005 s.

CPU y RAM del proceso completo, incluido muestreo. CPU 100% equivale a un procesador lógico; puede superar 100%. GPU/VRAM/potencia/temperatura son del equipo completo, no del ASR. No se mide energía específica, FLOPs ni rendimiento de tablet. Intervalos reales registrados, máximos muestreados no garantizan pico. Muestreo separado de inferencia; puede influir en la carga.

Las muestras completas de RAM, uso de GPU, VRAM, potencia y temperatura disponibles están en el JSON de recursos. La potencia GPU global en vatios no equivale al consumo energético del ASR.

| GPU global | Muestras | Uso medio / máx. (%) | VRAM máx. (MiB) | Potencia media / máx. (W) | Temperatura máx. (°C) |
|---|---:|---|---:|---|---:|
| NVIDIA GeForce RTX 3050 Laptop GPU | 24 | 0.000 / 0.000 | 481.000 | 6.351 / 6.390 | 46.000 |
| lectura_20261023_101713_339466_ventana_4s_r3.json | cpu | int8 | no (CPU) | 0.635 | 1.842 | medido |

**lectura_20261023_101713_339466_ventana_4s_r3.json:** CPU 11th Gen Intel(R) Core(TM) i7-11800H @ 2.30GHz; 16 procesadores lógicos; Windows-11-10.0.26200-SP0. CPU media del proceso: 24.804% de capacidad lógica del equipo. Pico de RAM del proceso durante su vida: 702.754 MiB. Carga del modelo: 0.933 s.

CPU y RAM del proceso completo, incluido muestreo. CPU 100% equivale a un procesador lógico; puede superar 100%. GPU/VRAM/potencia/temperatura son del equipo completo, no del ASR. No se mide energía específica, FLOPs ni rendimiento de tablet. Intervalos reales registrados, máximos muestreados no garantizan pico. Muestreo separado de inferencia; puede influir en la carga.

Las muestras completas de RAM, uso de GPU, VRAM, potencia y temperatura disponibles están en el JSON de recursos. La potencia GPU global en vatios no equivale al consumo energético del ASR.

| GPU global | Muestras | Uso medio / máx. (%) | VRAM máx. (MiB) | Potencia media / máx. (W) | Temperatura máx. (°C) |
|---|---:|---|---:|---|---:|
| NVIDIA GeForce RTX 3050 Laptop GPU | 24 | 0.000 / 0.000 | 481.000 | 6.345 / 6.390 | 45.000 |
| lectura_20261023_101713_339466_ventana_8s_r3.json | cpu | int8 | no (CPU) | 0.763 | 1.986 | medido |

**lectura_20261023_101713_339466_ventana_8s_r3.json:** CPU 11th Gen Intel(R) Core(TM) i7-11800H @ 2.30GHz; 16 procesadores lógicos; Windows-11-10.0.26200-SP0. CPU media del proceso: 24.857% de capacidad lógica del equipo. Pico de RAM del proceso durante su vida: 702.863 MiB. Carga del modelo: 0.889 s.

CPU y RAM del proceso completo, incluido muestreo. CPU 100% equivale a un procesador lógico; puede superar 100%. GPU/VRAM/potencia/temperatura son del equipo completo, no del ASR. No se mide energía específica, FLOPs ni rendimiento de tablet. Intervalos reales registrados, máximos muestreados no garantizan pico. Muestreo separado de inferencia; puede influir en la carga.

Las muestras completas de RAM, uso de GPU, VRAM, potencia y temperatura disponibles están en el JSON de recursos. La potencia GPU global en vatios no equivale al consumo energético del ASR.

| GPU global | Muestras | Uso medio / máx. (%) | VRAM máx. (MiB) | Potencia media / máx. (W) | Temperatura máx. (°C) |
|---|---:|---|---:|---|---:|
| NVIDIA GeForce RTX 3050 Laptop GPU | 28 | 0.000 / 0.000 | 481.000 | 6.346 / 6.380 | 45.000 |

Para comparar tablets habrá que medir en el dispositivo de destino: RAM máxima, tiempo de respuesta sostenido y consumo/batería. Este ordenador no permite deducir esos valores. No se cambia CPU por GPU automáticamente.
<!-- recursos-computo-fin -->
