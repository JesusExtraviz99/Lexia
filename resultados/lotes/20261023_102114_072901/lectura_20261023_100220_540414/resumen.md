# Comparación de reprocesamiento

3 ronda(s) por configuración, orden aleatorio reproducible por ronda. Ejecución secuencial para no competir por CPU. Tiempos orientativos, afectados por carga y calentamiento. No hay referencia humana de posición ni latencia visual. Comparar posiciones entre métodos no demuestra precisión.

Mismo modelo, CPU int8, VAD, bloques de 2 s, cuento y seguidor. La carga del modelo se excluye de los tiempos de inferencia. Solapamiento = ventana menos 2 s; no aplica al prefijo. El silencio final puede reducir los totales de las ventanas.

| Audio | Método | Ronda | Total inferencia (s) | Mediana (s) | P95 (s) | Inferencias >2 s | Cola máxima simulada (s) | Posición final | Retrocesos |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Lectura rápida - cuento 2 - lectura_02 - 23-10-2026.wav | ventana_8s | 1 | 23.47 | 2.00 | 2.38 | 7 | 1.84 | 56 | 0 |
| Lectura rápida - cuento 2 - lectura_02 - 23-10-2026.wav | ventana_4s | 1 | 17.31 | 1.77 | 2.13 | 3 | 0.19 | 56 | 0 |
| Lectura rápida - cuento 2 - lectura_02 - 23-10-2026.wav | ventana_8s | 2 | 23.65 | 1.84 | 2.69 | 7 | 2.49 | 56 | 0 |
| Lectura rápida - cuento 2 - lectura_02 - 23-10-2026.wav | ventana_4s | 2 | 17.06 | 1.77 | 2.05 | 2 | 0.08 | 56 | 0 |
| Lectura rápida - cuento 2 - lectura_02 - 23-10-2026.wav | ventana_4s | 3 | 17.08 | 1.77 | 2.06 | 3 | 0.07 | 56 | 0 |
| Lectura rápida - cuento 2 - lectura_02 - 23-10-2026.wav | ventana_8s | 3 | 24.04 | 2.02 | 2.60 | 8 | 2.71 | 56 | 0 |

## Posiciones en cada actualización

Comparación descriptiva con el prefijo, no referencia de precisión. El prefijo también puede equivocarse.

### Lectura rápida - cuento 2 - lectura_02 - 23-10-2026.wav, ronda 1

| Audio disponible (s) | ventana_4s | ventana_8s |
|---:|---:|---:|
| 2.0 | 4 | 4 |
| 4.0 | 13 | 13 |
| 6.0 | 19 | 19 |
| 8.0 | 26 | 26 |
| 10.0 | 32 | 32 |
| 12.0 | 43 | 44 |
| 14.0 | 49 | 49 |
| 16.0 | 56 | 56 |
| 18.0 | 56 | 56 |
| 20.0 | 56 | 56 |
| 22.0 | 56 | 56 |
| 24.0 | 56 | 56 |
| 26.0 | 56 | 56 |
| 28.0 | 56 | 56 |
| 30.0 | 56 | 56 |

### Lectura rápida - cuento 2 - lectura_02 - 23-10-2026.wav, ronda 2

| Audio disponible (s) | ventana_4s | ventana_8s |
|---:|---:|---:|
| 2.0 | 4 | 4 |
| 4.0 | 13 | 13 |
| 6.0 | 19 | 19 |
| 8.0 | 26 | 26 |
| 10.0 | 32 | 32 |
| 12.0 | 43 | 44 |
| 14.0 | 49 | 49 |
| 16.0 | 56 | 56 |
| 18.0 | 56 | 56 |
| 20.0 | 56 | 56 |
| 22.0 | 56 | 56 |
| 24.0 | 56 | 56 |
| 26.0 | 56 | 56 |
| 28.0 | 56 | 56 |
| 30.0 | 56 | 56 |

### Lectura rápida - cuento 2 - lectura_02 - 23-10-2026.wav, ronda 3

| Audio disponible (s) | ventana_4s | ventana_8s |
|---:|---:|---:|
| 2.0 | 4 | 4 |
| 4.0 | 13 | 13 |
| 6.0 | 19 | 19 |
| 8.0 | 26 | 26 |
| 10.0 | 32 | 32 |
| 12.0 | 43 | 44 |
| 14.0 | 49 | 49 |
| 16.0 | 56 | 56 |
| 18.0 | 56 | 56 |
| 20.0 | 56 | 56 |
| 22.0 | 56 | 56 |
| 24.0 | 56 | 56 |
| 26.0 | 56 | 56 |
| 28.0 | 56 | 56 |
| 30.0 | 56 | 56 |

## Resumen por configuración

| Audio | Método | Total medio (s) | Rango de totales (s) | Cola máxima media (s) | Inferencias >2 s | Posiciones finales |
|---|---|---:|---|---:|---|---|
| Lectura rápida - cuento 2 - lectura_02 - 23-10-2026.wav | ventana_4s | 17.15 | 17.06–17.31 | 0.12 | 8/45 | [56, 56, 56] |
| Lectura rápida - cuento 2 - lectura_02 - 23-10-2026.wav | ventana_8s | 23.72 | 23.47–24.04 | 2.34 | 22/45 | [56, 56, 56] |

<!-- recursos-computo-inicio -->
## Recursos y coste computacional

Datos de la ejecución original. «No medido» no significa cero. RTF = suma de inferencias / duración del audio completo (incluye silencio); no es latencia visual ni mide captura, escritura o muestreo. Las rondas de una grabación no son lecturas independientes.

| Registro | Dispositivo ASR | Precisión | GPU para ASR | RTF | Máx. inferencia (s) | CPU/RAM/GPU instrumentadas |
|---|---|---|---|---:|---:|---|
| lectura_20261023_100220_540414_ventana_8s_r1.json | cpu | int8 | no (CPU) | 0.782 | 2.380 | medido |

**lectura_20261023_100220_540414_ventana_8s_r1.json:** CPU 11th Gen Intel(R) Core(TM) i7-11800H @ 2.30GHz; 16 procesadores lógicos; Windows-11-10.0.26200-SP0. CPU media del proceso: 24.646% de capacidad lógica del equipo. Pico de RAM del proceso durante su vida: 701.707 MiB. Carga del modelo: 1.122 s.

CPU y RAM del proceso completo, incluido muestreo. CPU 100% equivale a un procesador lógico; puede superar 100%. GPU/VRAM/potencia/temperatura son del equipo completo, no del ASR. No se mide energía específica, FLOPs ni rendimiento de tablet. Intervalos reales registrados, máximos muestreados no garantizan pico. Muestreo separado de inferencia; puede influir en la carga.

Las muestras completas de RAM, uso de GPU, VRAM, potencia y temperatura disponibles están en el JSON de recursos. La potencia GPU global en vatios no equivale al consumo energético del ASR.

| GPU global | Muestras | Uso medio / máx. (%) | VRAM máx. (MiB) | Potencia media / máx. (W) | Temperatura máx. (°C) |
|---|---:|---|---:|---|---:|
| NVIDIA GeForce RTX 3050 Laptop GPU | 22 | 0.000 / 0.000 | 481.000 | 6.365 / 6.390 | 46.000 |
| lectura_20261023_100220_540414_ventana_4s_r1.json | cpu | int8 | no (CPU) | 0.577 | 2.130 | medido |

**lectura_20261023_100220_540414_ventana_4s_r1.json:** CPU 11th Gen Intel(R) Core(TM) i7-11800H @ 2.30GHz; 16 procesadores lógicos; Windows-11-10.0.26200-SP0. CPU media del proceso: 24.590% de capacidad lógica del equipo. Pico de RAM del proceso durante su vida: 701.770 MiB. Carga del modelo: 0.971 s.

CPU y RAM del proceso completo, incluido muestreo. CPU 100% equivale a un procesador lógico; puede superar 100%. GPU/VRAM/potencia/temperatura son del equipo completo, no del ASR. No se mide energía específica, FLOPs ni rendimiento de tablet. Intervalos reales registrados, máximos muestreados no garantizan pico. Muestreo separado de inferencia; puede influir en la carga.

Las muestras completas de RAM, uso de GPU, VRAM, potencia y temperatura disponibles están en el JSON de recursos. La potencia GPU global en vatios no equivale al consumo energético del ASR.

| GPU global | Muestras | Uso medio / máx. (%) | VRAM máx. (MiB) | Potencia media / máx. (W) | Temperatura máx. (°C) |
|---|---:|---|---:|---|---:|
| NVIDIA GeForce RTX 3050 Laptop GPU | 17 | 0.000 / 0.000 | 481.000 | 6.375 / 6.410 | 45.000 |
| lectura_20261023_100220_540414_ventana_8s_r2.json | cpu | int8 | no (CPU) | 0.788 | 2.694 | medido |

**lectura_20261023_100220_540414_ventana_8s_r2.json:** CPU 11th Gen Intel(R) Core(TM) i7-11800H @ 2.30GHz; 16 procesadores lógicos; Windows-11-10.0.26200-SP0. CPU media del proceso: 24.743% de capacidad lógica del equipo. Pico de RAM del proceso durante su vida: 701.977 MiB. Carga del modelo: 0.993 s.

CPU y RAM del proceso completo, incluido muestreo. CPU 100% equivale a un procesador lógico; puede superar 100%. GPU/VRAM/potencia/temperatura son del equipo completo, no del ASR. No se mide energía específica, FLOPs ni rendimiento de tablet. Intervalos reales registrados, máximos muestreados no garantizan pico. Muestreo separado de inferencia; puede influir en la carga.

Las muestras completas de RAM, uso de GPU, VRAM, potencia y temperatura disponibles están en el JSON de recursos. La potencia GPU global en vatios no equivale al consumo energético del ASR.

| GPU global | Muestras | Uso medio / máx. (%) | VRAM máx. (MiB) | Potencia media / máx. (W) | Temperatura máx. (°C) |
|---|---:|---|---:|---|---:|
| NVIDIA GeForce RTX 3050 Laptop GPU | 22 | 0.000 / 0.000 | 481.000 | 6.378 / 6.410 | 45.000 |
| lectura_20261023_100220_540414_ventana_4s_r2.json | cpu | int8 | no (CPU) | 0.569 | 2.052 | medido |

**lectura_20261023_100220_540414_ventana_4s_r2.json:** CPU 11th Gen Intel(R) Core(TM) i7-11800H @ 2.30GHz; 16 procesadores lógicos; Windows-11-10.0.26200-SP0. CPU media del proceso: 24.652% de capacidad lógica del equipo. Pico de RAM del proceso durante su vida: 701.910 MiB. Carga del modelo: 0.975 s.

CPU y RAM del proceso completo, incluido muestreo. CPU 100% equivale a un procesador lógico; puede superar 100%. GPU/VRAM/potencia/temperatura son del equipo completo, no del ASR. No se mide energía específica, FLOPs ni rendimiento de tablet. Intervalos reales registrados, máximos muestreados no garantizan pico. Muestreo separado de inferencia; puede influir en la carga.

Las muestras completas de RAM, uso de GPU, VRAM, potencia y temperatura disponibles están en el JSON de recursos. La potencia GPU global en vatios no equivale al consumo energético del ASR.

| GPU global | Muestras | Uso medio / máx. (%) | VRAM máx. (MiB) | Potencia media / máx. (W) | Temperatura máx. (°C) |
|---|---:|---|---:|---|---:|
| NVIDIA GeForce RTX 3050 Laptop GPU | 17 | 0.000 / 0.000 | 481.000 | 6.362 / 6.420 | 45.000 |
| lectura_20261023_100220_540414_ventana_4s_r3.json | cpu | int8 | no (CPU) | 0.569 | 2.058 | medido |

**lectura_20261023_100220_540414_ventana_4s_r3.json:** CPU 11th Gen Intel(R) Core(TM) i7-11800H @ 2.30GHz; 16 procesadores lógicos; Windows-11-10.0.26200-SP0. CPU media del proceso: 24.657% de capacidad lógica del equipo. Pico de RAM del proceso durante su vida: 701.777 MiB. Carga del modelo: 1.019 s.

CPU y RAM del proceso completo, incluido muestreo. CPU 100% equivale a un procesador lógico; puede superar 100%. GPU/VRAM/potencia/temperatura son del equipo completo, no del ASR. No se mide energía específica, FLOPs ni rendimiento de tablet. Intervalos reales registrados, máximos muestreados no garantizan pico. Muestreo separado de inferencia; puede influir en la carga.

Las muestras completas de RAM, uso de GPU, VRAM, potencia y temperatura disponibles están en el JSON de recursos. La potencia GPU global en vatios no equivale al consumo energético del ASR.

| GPU global | Muestras | Uso medio / máx. (%) | VRAM máx. (MiB) | Potencia media / máx. (W) | Temperatura máx. (°C) |
|---|---:|---|---:|---|---:|
| NVIDIA GeForce RTX 3050 Laptop GPU | 17 | 0.000 / 0.000 | 481.000 | 6.365 / 6.410 | 45.000 |
| lectura_20261023_100220_540414_ventana_8s_r3.json | cpu | int8 | no (CPU) | 0.801 | 2.604 | medido |

**lectura_20261023_100220_540414_ventana_8s_r3.json:** CPU 11th Gen Intel(R) Core(TM) i7-11800H @ 2.30GHz; 16 procesadores lógicos; Windows-11-10.0.26200-SP0. CPU media del proceso: 24.765% de capacidad lógica del equipo. Pico de RAM del proceso durante su vida: 701.656 MiB. Carga del modelo: 1.023 s.

CPU y RAM del proceso completo, incluido muestreo. CPU 100% equivale a un procesador lógico; puede superar 100%. GPU/VRAM/potencia/temperatura son del equipo completo, no del ASR. No se mide energía específica, FLOPs ni rendimiento de tablet. Intervalos reales registrados, máximos muestreados no garantizan pico. Muestreo separado de inferencia; puede influir en la carga.

Las muestras completas de RAM, uso de GPU, VRAM, potencia y temperatura disponibles están en el JSON de recursos. La potencia GPU global en vatios no equivale al consumo energético del ASR.

| GPU global | Muestras | Uso medio / máx. (%) | VRAM máx. (MiB) | Potencia media / máx. (W) | Temperatura máx. (°C) |
|---|---:|---|---:|---|---:|
| NVIDIA GeForce RTX 3050 Laptop GPU | 23 | 0.000 / 0.000 | 481.000 | 6.365 / 6.380 | 45.000 |

Para comparar tablets habrá que medir en el dispositivo de destino: RAM máxima, tiempo de respuesta sostenido y consumo/batería. Este ordenador no permite deducir esos valores. No se cambia CPU por GPU automáticamente.
<!-- recursos-computo-fin -->
