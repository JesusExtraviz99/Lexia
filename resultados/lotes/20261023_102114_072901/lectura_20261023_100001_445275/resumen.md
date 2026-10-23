# Comparación de reprocesamiento

3 ronda(s) por configuración, orden aleatorio reproducible por ronda. Ejecución secuencial para no competir por CPU. Tiempos orientativos, afectados por carga y calentamiento. No hay referencia humana de posición ni latencia visual. Comparar posiciones entre métodos no demuestra precisión.

Mismo modelo, CPU int8, VAD, bloques de 2 s, cuento y seguidor. La carga del modelo se excluye de los tiempos de inferencia. Solapamiento = ventana menos 2 s; no aplica al prefijo. El silencio final puede reducir los totales de las ventanas.

| Audio | Método | Ronda | Total inferencia (s) | Mediana (s) | P95 (s) | Inferencias >2 s | Cola máxima simulada (s) | Posición final | Retrocesos |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Lectura lenta - cuento 2 - lectura_02 - 23-10-2026.wav | ventana_8s | 1 | 77.50 | 2.02 | 2.33 | 26 | 3.42 | 56 | 0 |
| Lectura lenta - cuento 2 - lectura_02 - 23-10-2026.wav | ventana_4s | 1 | 66.49 | 1.64 | 1.87 | 2 | 6.70 | 56 | 0 |
| Lectura lenta - cuento 2 - lectura_02 - 23-10-2026.wav | ventana_8s | 2 | 66.46 | 1.77 | 1.93 | 2 | 0.33 | 56 | 0 |
| Lectura lenta - cuento 2 - lectura_02 - 23-10-2026.wav | ventana_4s | 2 | 68.61 | 1.73 | 1.87 | 1 | 6.85 | 56 | 0 |
| Lectura lenta - cuento 2 - lectura_02 - 23-10-2026.wav | ventana_4s | 3 | 69.66 | 1.76 | 1.92 | 1 | 7.18 | 56 | 0 |
| Lectura lenta - cuento 2 - lectura_02 - 23-10-2026.wav | ventana_8s | 3 | 68.71 | 1.84 | 1.95 | 0 | 0.00 | 56 | 0 |

## Posiciones en cada actualización

Comparación descriptiva con el prefijo, no referencia de precisión. El prefijo también puede equivocarse.

### Lectura lenta - cuento 2 - lectura_02 - 23-10-2026.wav, ronda 1

| Audio disponible (s) | ventana_4s | ventana_8s |
|---:|---:|---:|
| 2.0 | — | — |
| 4.0 | 2 | 2 |
| 6.0 | 2 | 2 |
| 8.0 | 6 | 6 |
| 10.0 | 7 | 7 |
| 12.0 | 10 | 10 |
| 14.0 | 10 | 10 |
| 16.0 | 14 | 14 |
| 18.0 | 14 | 14 |
| 20.0 | 16 | 16 |
| 22.0 | 16 | 17 |
| 24.0 | 19 | 19 |
| 26.0 | 19 | 21 |
| 28.0 | 21 | 21 |
| 30.0 | 23 | 23 |
| 32.0 | 25 | 25 |
| 34.0 | 26 | 26 |
| 36.0 | 26 | 28 |
| 38.0 | 29 | 30 |
| 40.0 | 31 | 30 |
| 42.0 | 35 | 35 |
| 44.0 | 35 | 35 |
| 46.0 | 39 | 39 |
| 48.0 | 41 | 41 |
| 50.0 | 43 | 43 |
| 52.0 | 46 | 46 |
| 54.0 | 46 | 46 |
| 56.0 | 46 | 47 |
| 58.0 | 46 | 49 |
| 60.0 | 52 | 52 |
| 62.0 | 53 | 53 |
| 64.0 | 55 | 55 |
| 66.0 | 56 | 56 |
| 68.0 | 56 | 56 |
| 70.0 | 56 | 56 |
| 72.0 | 56 | 56 |
| 74.0 | 56 | 56 |
| 76.0 | 56 | 56 |
| 78.0 | 56 | 56 |
| 80.0 | 56 | 56 |
| 82.0 | 56 | 56 |
| 84.0 | 56 | 56 |
| 86.0 | 56 | 56 |
| 88.0 | 56 | 56 |
| 90.0 | 56 | 56 |

### Lectura lenta - cuento 2 - lectura_02 - 23-10-2026.wav, ronda 2

| Audio disponible (s) | ventana_4s | ventana_8s |
|---:|---:|---:|
| 2.0 | — | — |
| 4.0 | 2 | 2 |
| 6.0 | 2 | 2 |
| 8.0 | 6 | 6 |
| 10.0 | 7 | 7 |
| 12.0 | 10 | 10 |
| 14.0 | 10 | 10 |
| 16.0 | 14 | 14 |
| 18.0 | 14 | 14 |
| 20.0 | 16 | 16 |
| 22.0 | 16 | 17 |
| 24.0 | 19 | 19 |
| 26.0 | 19 | 21 |
| 28.0 | 21 | 21 |
| 30.0 | 23 | 23 |
| 32.0 | 25 | 25 |
| 34.0 | 26 | 26 |
| 36.0 | 26 | 28 |
| 38.0 | 29 | 30 |
| 40.0 | 31 | 30 |
| 42.0 | 35 | 35 |
| 44.0 | 35 | 35 |
| 46.0 | 39 | 39 |
| 48.0 | 41 | 41 |
| 50.0 | 43 | 43 |
| 52.0 | 46 | 46 |
| 54.0 | 46 | 46 |
| 56.0 | 46 | 47 |
| 58.0 | 46 | 49 |
| 60.0 | 52 | 52 |
| 62.0 | 53 | 53 |
| 64.0 | 55 | 55 |
| 66.0 | 56 | 56 |
| 68.0 | 56 | 56 |
| 70.0 | 56 | 56 |
| 72.0 | 56 | 56 |
| 74.0 | 56 | 56 |
| 76.0 | 56 | 56 |
| 78.0 | 56 | 56 |
| 80.0 | 56 | 56 |
| 82.0 | 56 | 56 |
| 84.0 | 56 | 56 |
| 86.0 | 56 | 56 |
| 88.0 | 56 | 56 |
| 90.0 | 56 | 56 |

### Lectura lenta - cuento 2 - lectura_02 - 23-10-2026.wav, ronda 3

| Audio disponible (s) | ventana_4s | ventana_8s |
|---:|---:|---:|
| 2.0 | — | — |
| 4.0 | 2 | 2 |
| 6.0 | 2 | 2 |
| 8.0 | 6 | 6 |
| 10.0 | 7 | 7 |
| 12.0 | 10 | 10 |
| 14.0 | 10 | 10 |
| 16.0 | 14 | 14 |
| 18.0 | 14 | 14 |
| 20.0 | 16 | 16 |
| 22.0 | 16 | 17 |
| 24.0 | 19 | 19 |
| 26.0 | 19 | 21 |
| 28.0 | 21 | 21 |
| 30.0 | 23 | 23 |
| 32.0 | 25 | 25 |
| 34.0 | 26 | 26 |
| 36.0 | 26 | 28 |
| 38.0 | 29 | 30 |
| 40.0 | 31 | 30 |
| 42.0 | 35 | 35 |
| 44.0 | 35 | 35 |
| 46.0 | 39 | 39 |
| 48.0 | 41 | 41 |
| 50.0 | 43 | 43 |
| 52.0 | 46 | 46 |
| 54.0 | 46 | 46 |
| 56.0 | 46 | 47 |
| 58.0 | 46 | 49 |
| 60.0 | 52 | 52 |
| 62.0 | 53 | 53 |
| 64.0 | 55 | 55 |
| 66.0 | 56 | 56 |
| 68.0 | 56 | 56 |
| 70.0 | 56 | 56 |
| 72.0 | 56 | 56 |
| 74.0 | 56 | 56 |
| 76.0 | 56 | 56 |
| 78.0 | 56 | 56 |
| 80.0 | 56 | 56 |
| 82.0 | 56 | 56 |
| 84.0 | 56 | 56 |
| 86.0 | 56 | 56 |
| 88.0 | 56 | 56 |
| 90.0 | 56 | 56 |

## Resumen por configuración

| Audio | Método | Total medio (s) | Rango de totales (s) | Cola máxima media (s) | Inferencias >2 s | Posiciones finales |
|---|---|---:|---|---:|---|---|
| Lectura lenta - cuento 2 - lectura_02 - 23-10-2026.wav | ventana_4s | 68.25 | 66.49–69.66 | 6.91 | 4/135 | [56, 56, 56] |
| Lectura lenta - cuento 2 - lectura_02 - 23-10-2026.wav | ventana_8s | 70.89 | 66.46–77.50 | 1.25 | 28/135 | [56, 56, 56] |

<!-- recursos-computo-inicio -->
## Recursos y coste computacional

Datos de la ejecución original. «No medido» no significa cero. RTF = suma de inferencias / duración del audio completo (incluye silencio); no es latencia visual ni mide captura, escritura o muestreo. Las rondas de una grabación no son lecturas independientes.

| Registro | Dispositivo ASR | Precisión | GPU para ASR | RTF | Máx. inferencia (s) | CPU/RAM/GPU instrumentadas |
|---|---|---|---|---:|---:|---|
| lectura_20261023_100001_445275_ventana_8s_r1.json | cpu | int8 | no (CPU) | 0.861 | 2.426 | medido |

**lectura_20261023_100001_445275_ventana_8s_r1.json:** CPU 11th Gen Intel(R) Core(TM) i7-11800H @ 2.30GHz; 16 procesadores lógicos; Windows-11-10.0.26200-SP0. CPU media del proceso: 24.044% de capacidad lógica del equipo. Pico de RAM del proceso durante su vida: 706.094 MiB. Carga del modelo: 2.079 s.

CPU y RAM del proceso completo, incluido muestreo. CPU 100% equivale a un procesador lógico; puede superar 100%. GPU/VRAM/potencia/temperatura son del equipo completo, no del ASR. No se mide energía específica, FLOPs ni rendimiento de tablet. Intervalos reales registrados, máximos muestreados no garantizan pico. Muestreo separado de inferencia; puede influir en la carga.

Las muestras completas de RAM, uso de GPU, VRAM, potencia y temperatura disponibles están en el JSON de recursos. La potencia GPU global en vatios no equivale al consumo energético del ASR.

| GPU global | Muestras | Uso medio / máx. (%) | VRAM máx. (MiB) | Potencia media / máx. (W) | Temperatura máx. (°C) |
|---|---:|---|---:|---|---:|
| NVIDIA GeForce RTX 3050 Laptop GPU | 70 | 0.000 / 0.000 | 481.000 | 6.362 / 6.430 | 45.000 |
| lectura_20261023_100001_445275_ventana_4s_r1.json | cpu | int8 | no (CPU) | 0.739 | 8.701 | medido |

**lectura_20261023_100001_445275_ventana_4s_r1.json:** CPU 11th Gen Intel(R) Core(TM) i7-11800H @ 2.30GHz; 16 procesadores lógicos; Windows-11-10.0.26200-SP0. CPU media del proceso: 24.902% de capacidad lógica del equipo. Pico de RAM del proceso durante su vida: 967.086 MiB. Carga del modelo: 1.280 s.

CPU y RAM del proceso completo, incluido muestreo. CPU 100% equivale a un procesador lógico; puede superar 100%. GPU/VRAM/potencia/temperatura son del equipo completo, no del ASR. No se mide energía específica, FLOPs ni rendimiento de tablet. Intervalos reales registrados, máximos muestreados no garantizan pico. Muestreo separado de inferencia; puede influir en la carga.

Las muestras completas de RAM, uso de GPU, VRAM, potencia y temperatura disponibles están en el JSON de recursos. La potencia GPU global en vatios no equivale al consumo energético del ASR.

| GPU global | Muestras | Uso medio / máx. (%) | VRAM máx. (MiB) | Potencia media / máx. (W) | Temperatura máx. (°C) |
|---|---:|---|---:|---|---:|
| NVIDIA GeForce RTX 3050 Laptop GPU | 61 | 0.000 / 0.000 | 481.000 | 6.376 / 6.400 | 45.000 |
| lectura_20261023_100001_445275_ventana_8s_r2.json | cpu | int8 | no (CPU) | 0.738 | 2.184 | medido |

**lectura_20261023_100001_445275_ventana_8s_r2.json:** CPU 11th Gen Intel(R) Core(TM) i7-11800H @ 2.30GHz; 16 procesadores lógicos; Windows-11-10.0.26200-SP0. CPU media del proceso: 24.931% de capacidad lógica del equipo. Pico de RAM del proceso durante su vida: 705.934 MiB. Carga del modelo: 1.006 s.

CPU y RAM del proceso completo, incluido muestreo. CPU 100% equivale a un procesador lógico; puede superar 100%. GPU/VRAM/potencia/temperatura son del equipo completo, no del ASR. No se mide energía específica, FLOPs ni rendimiento de tablet. Intervalos reales registrados, máximos muestreados no garantizan pico. Muestreo separado de inferencia; puede influir en la carga.

Las muestras completas de RAM, uso de GPU, VRAM, potencia y temperatura disponibles están en el JSON de recursos. La potencia GPU global en vatios no equivale al consumo energético del ASR.

| GPU global | Muestras | Uso medio / máx. (%) | VRAM máx. (MiB) | Potencia media / máx. (W) | Temperatura máx. (°C) |
|---|---:|---|---:|---|---:|
| NVIDIA GeForce RTX 3050 Laptop GPU | 60 | 0.000 / 0.000 | 481.000 | 6.376 / 6.420 | 45.000 |
| lectura_20261023_100001_445275_ventana_4s_r2.json | cpu | int8 | no (CPU) | 0.762 | 8.852 | medido |

**lectura_20261023_100001_445275_ventana_4s_r2.json:** CPU 11th Gen Intel(R) Core(TM) i7-11800H @ 2.30GHz; 16 procesadores lógicos; Windows-11-10.0.26200-SP0. CPU media del proceso: 24.920% de capacidad lógica del equipo. Pico de RAM del proceso durante su vida: 967.027 MiB. Carga del modelo: 1.066 s.

CPU y RAM del proceso completo, incluido muestreo. CPU 100% equivale a un procesador lógico; puede superar 100%. GPU/VRAM/potencia/temperatura son del equipo completo, no del ASR. No se mide energía específica, FLOPs ni rendimiento de tablet. Intervalos reales registrados, máximos muestreados no garantizan pico. Muestreo separado de inferencia; puede influir en la carga.

Las muestras completas de RAM, uso de GPU, VRAM, potencia y temperatura disponibles están en el JSON de recursos. La potencia GPU global en vatios no equivale al consumo energético del ASR.

| GPU global | Muestras | Uso medio / máx. (%) | VRAM máx. (MiB) | Potencia media / máx. (W) | Temperatura máx. (°C) |
|---|---:|---|---:|---|---:|
| NVIDIA GeForce RTX 3050 Laptop GPU | 62 | 0.000 / 0.000 | 481.000 | 6.366 / 6.400 | 46.000 |
| lectura_20261023_100001_445275_ventana_4s_r3.json | cpu | int8 | no (CPU) | 0.774 | 9.177 | medido |

**lectura_20261023_100001_445275_ventana_4s_r3.json:** CPU 11th Gen Intel(R) Core(TM) i7-11800H @ 2.30GHz; 16 procesadores lógicos; Windows-11-10.0.26200-SP0. CPU media del proceso: 24.943% de capacidad lógica del equipo. Pico de RAM del proceso durante su vida: 954.922 MiB. Carga del modelo: 1.053 s.

CPU y RAM del proceso completo, incluido muestreo. CPU 100% equivale a un procesador lógico; puede superar 100%. GPU/VRAM/potencia/temperatura son del equipo completo, no del ASR. No se mide energía específica, FLOPs ni rendimiento de tablet. Intervalos reales registrados, máximos muestreados no garantizan pico. Muestreo separado de inferencia; puede influir en la carga.

Las muestras completas de RAM, uso de GPU, VRAM, potencia y temperatura disponibles están en el JSON de recursos. La potencia GPU global en vatios no equivale al consumo energético del ASR.

| GPU global | Muestras | Uso medio / máx. (%) | VRAM máx. (MiB) | Potencia media / máx. (W) | Temperatura máx. (°C) |
|---|---:|---|---:|---|---:|
| NVIDIA GeForce RTX 3050 Laptop GPU | 63 | 0.000 / 0.000 | 481.000 | 6.377 / 6.430 | 46.000 |
| lectura_20261023_100001_445275_ventana_8s_r3.json | cpu | int8 | no (CPU) | 0.763 | 1.969 | medido |

**lectura_20261023_100001_445275_ventana_8s_r3.json:** CPU 11th Gen Intel(R) Core(TM) i7-11800H @ 2.30GHz; 16 procesadores lógicos; Windows-11-10.0.26200-SP0. CPU media del proceso: 24.941% de capacidad lógica del equipo. Pico de RAM del proceso durante su vida: 705.773 MiB. Carga del modelo: 1.005 s.

CPU y RAM del proceso completo, incluido muestreo. CPU 100% equivale a un procesador lógico; puede superar 100%. GPU/VRAM/potencia/temperatura son del equipo completo, no del ASR. No se mide energía específica, FLOPs ni rendimiento de tablet. Intervalos reales registrados, máximos muestreados no garantizan pico. Muestreo separado de inferencia; puede influir en la carga.

Las muestras completas de RAM, uso de GPU, VRAM, potencia y temperatura disponibles están en el JSON de recursos. La potencia GPU global en vatios no equivale al consumo energético del ASR.

| GPU global | Muestras | Uso medio / máx. (%) | VRAM máx. (MiB) | Potencia media / máx. (W) | Temperatura máx. (°C) |
|---|---:|---|---:|---|---:|
| NVIDIA GeForce RTX 3050 Laptop GPU | 62 | 0.000 / 0.000 | 481.000 | 6.362 / 6.400 | 46.000 |

Para comparar tablets habrá que medir en el dispositivo de destino: RAM máxima, tiempo de respuesta sostenido y consumo/batería. Este ordenador no permite deducir esos valores. No se cambia CPU por GPU automáticamente.
<!-- recursos-computo-fin -->
