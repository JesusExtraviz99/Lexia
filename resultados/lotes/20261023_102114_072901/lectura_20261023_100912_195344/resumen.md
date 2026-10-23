# Comparación de reprocesamiento

3 ronda(s) por configuración, orden aleatorio reproducible por ronda. Ejecución secuencial para no competir por CPU. Tiempos orientativos, afectados por carga y calentamiento. No hay referencia humana de posición ni latencia visual. Comparar posiciones entre métodos no demuestra precisión.

Mismo modelo, CPU int8, VAD, bloques de 2 s, cuento y seguidor. La carga del modelo se excluye de los tiempos de inferencia. Solapamiento = ventana menos 2 s; no aplica al prefijo. El silencio final puede reducir los totales de las ventanas.

| Audio | Método | Ronda | Total inferencia (s) | Mediana (s) | P95 (s) | Inferencias >2 s | Cola máxima simulada (s) | Posición final | Retrocesos |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Lectura sustitución rojo por azul - cuento 2 - lectura_02 - 23-10-2026.wav | ventana_8s | 1 | 38.87 | 1.82 | 3.55 | 4 | 6.58 | 56 | 0 |
| Lectura sustitución rojo por azul - cuento 2 - lectura_02 - 23-10-2026.wav | ventana_4s | 1 | 27.49 | 1.74 | 1.94 | 0 | 0.00 | 56 | 0 |
| Lectura sustitución rojo por azul - cuento 2 - lectura_02 - 23-10-2026.wav | ventana_8s | 2 | 39.58 | 1.86 | 3.68 | 4 | 7.27 | 56 | 0 |
| Lectura sustitución rojo por azul - cuento 2 - lectura_02 - 23-10-2026.wav | ventana_4s | 2 | 27.23 | 1.72 | 1.92 | 0 | 0.00 | 56 | 0 |
| Lectura sustitución rojo por azul - cuento 2 - lectura_02 - 23-10-2026.wav | ventana_4s | 3 | 28.38 | 1.74 | 2.04 | 2 | 0.47 | 56 | 0 |
| Lectura sustitución rojo por azul - cuento 2 - lectura_02 - 23-10-2026.wav | ventana_8s | 3 | 42.67 | 1.80 | 3.63 | 4 | 10.54 | 56 | 0 |

## Posiciones en cada actualización

Comparación descriptiva con el prefijo, no referencia de precisión. El prefijo también puede equivocarse.

### Lectura sustitución rojo por azul - cuento 2 - lectura_02 - 23-10-2026.wav, ronda 1

| Audio disponible (s) | ventana_4s | ventana_8s |
|---:|---:|---:|
| 2.0 | 2 | 2 |
| 4.0 | 7 | 7 |
| 6.0 | 12 | 11 |
| 8.0 | 17 | 17 |
| 10.0 | 18 | 18 |
| 12.0 | 23 | 23 |
| 14.0 | 26 | 26 |
| 16.0 | 31 | 31 |
| 18.0 | 37 | 37 |
| 20.0 | 40 | 41 |
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
| 42.0 | 56 | 56 |
| 44.0 | 56 | 56 |
| 46.0 | 56 | 56 |
| 48.0 | 56 | 56 |
| 50.0 | 56 | 56 |

### Lectura sustitución rojo por azul - cuento 2 - lectura_02 - 23-10-2026.wav, ronda 2

| Audio disponible (s) | ventana_4s | ventana_8s |
|---:|---:|---:|
| 2.0 | 2 | 2 |
| 4.0 | 7 | 7 |
| 6.0 | 12 | 11 |
| 8.0 | 17 | 17 |
| 10.0 | 18 | 18 |
| 12.0 | 23 | 23 |
| 14.0 | 26 | 26 |
| 16.0 | 31 | 31 |
| 18.0 | 37 | 37 |
| 20.0 | 40 | 41 |
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
| 42.0 | 56 | 56 |
| 44.0 | 56 | 56 |
| 46.0 | 56 | 56 |
| 48.0 | 56 | 56 |
| 50.0 | 56 | 56 |

### Lectura sustitución rojo por azul - cuento 2 - lectura_02 - 23-10-2026.wav, ronda 3

| Audio disponible (s) | ventana_4s | ventana_8s |
|---:|---:|---:|
| 2.0 | 2 | 2 |
| 4.0 | 7 | 7 |
| 6.0 | 12 | 11 |
| 8.0 | 17 | 17 |
| 10.0 | 18 | 18 |
| 12.0 | 23 | 23 |
| 14.0 | 26 | 26 |
| 16.0 | 31 | 31 |
| 18.0 | 37 | 37 |
| 20.0 | 40 | 41 |
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
| 42.0 | 56 | 56 |
| 44.0 | 56 | 56 |
| 46.0 | 56 | 56 |
| 48.0 | 56 | 56 |
| 50.0 | 56 | 56 |

## Resumen por configuración

| Audio | Método | Total medio (s) | Rango de totales (s) | Cola máxima media (s) | Inferencias >2 s | Posiciones finales |
|---|---|---:|---|---:|---|---|
| Lectura sustitución rojo por azul - cuento 2 - lectura_02 - 23-10-2026.wav | ventana_4s | 27.70 | 27.23–28.38 | 0.16 | 2/75 | [56, 56, 56] |
| Lectura sustitución rojo por azul - cuento 2 - lectura_02 - 23-10-2026.wav | ventana_8s | 40.38 | 38.87–42.67 | 8.13 | 12/75 | [56, 56, 56] |

<!-- recursos-computo-inicio -->
## Recursos y coste computacional

Datos de la ejecución original. «No medido» no significa cero. RTF = suma de inferencias / duración del audio completo (incluye silencio); no es latencia visual ni mide captura, escritura o muestreo. Las rondas de una grabación no son lecturas independientes.

| Registro | Dispositivo ASR | Precisión | GPU para ASR | RTF | Máx. inferencia (s) | CPU/RAM/GPU instrumentadas |
|---|---|---|---|---:|---:|---|
| lectura_20261023_100912_195344_ventana_8s_r1.json | cpu | int8 | no (CPU) | 0.777 | 7.146 | medido |

**lectura_20261023_100912_195344_ventana_8s_r1.json:** CPU 11th Gen Intel(R) Core(TM) i7-11800H @ 2.30GHz; 16 procesadores lógicos; Windows-11-10.0.26200-SP0. CPU media del proceso: 24.758% de capacidad lógica del equipo. Pico de RAM del proceso durante su vida: 974.648 MiB. Carga del modelo: 1.341 s.

CPU y RAM del proceso completo, incluido muestreo. CPU 100% equivale a un procesador lógico; puede superar 100%. GPU/VRAM/potencia/temperatura son del equipo completo, no del ASR. No se mide energía específica, FLOPs ni rendimiento de tablet. Intervalos reales registrados, máximos muestreados no garantizan pico. Muestreo separado de inferencia; puede influir en la carga.

Las muestras completas de RAM, uso de GPU, VRAM, potencia y temperatura disponibles están en el JSON de recursos. La potencia GPU global en vatios no equivale al consumo energético del ASR.

| GPU global | Muestras | Uso medio / máx. (%) | VRAM máx. (MiB) | Potencia media / máx. (W) | Temperatura máx. (°C) |
|---|---:|---|---:|---|---:|
| NVIDIA GeForce RTX 3050 Laptop GPU | 36 | 0.000 / 0.000 | 481.000 | 6.364 / 6.400 | 45.000 |
| lectura_20261023_100912_195344_ventana_4s_r1.json | cpu | int8 | no (CPU) | 0.550 | 1.999 | medido |

**lectura_20261023_100912_195344_ventana_4s_r1.json:** CPU 11th Gen Intel(R) Core(TM) i7-11800H @ 2.30GHz; 16 procesadores lógicos; Windows-11-10.0.26200-SP0. CPU media del proceso: 24.803% de capacidad lógica del equipo. Pico de RAM del proceso durante su vida: 703.328 MiB. Carga del modelo: 1.013 s.

CPU y RAM del proceso completo, incluido muestreo. CPU 100% equivale a un procesador lógico; puede superar 100%. GPU/VRAM/potencia/temperatura son del equipo completo, no del ASR. No se mide energía específica, FLOPs ni rendimiento de tablet. Intervalos reales registrados, máximos muestreados no garantizan pico. Muestreo separado de inferencia; puede influir en la carga.

Las muestras completas de RAM, uso de GPU, VRAM, potencia y temperatura disponibles están en el JSON de recursos. La potencia GPU global en vatios no equivale al consumo energético del ASR.

| GPU global | Muestras | Uso medio / máx. (%) | VRAM máx. (MiB) | Potencia media / máx. (W) | Temperatura máx. (°C) |
|---|---:|---|---:|---|---:|
| NVIDIA GeForce RTX 3050 Laptop GPU | 26 | 0.000 / 0.000 | 481.000 | 6.350 / 6.440 | 45.000 |
| lectura_20261023_100912_195344_ventana_8s_r2.json | cpu | int8 | no (CPU) | 0.792 | 7.423 | medido |

**lectura_20261023_100912_195344_ventana_8s_r2.json:** CPU 11th Gen Intel(R) Core(TM) i7-11800H @ 2.30GHz; 16 procesadores lógicos; Windows-11-10.0.26200-SP0. CPU media del proceso: 24.962% de capacidad lógica del equipo. Pico de RAM del proceso durante su vida: 973.762 MiB. Carga del modelo: 0.975 s.

CPU y RAM del proceso completo, incluido muestreo. CPU 100% equivale a un procesador lógico; puede superar 100%. GPU/VRAM/potencia/temperatura son del equipo completo, no del ASR. No se mide energía específica, FLOPs ni rendimiento de tablet. Intervalos reales registrados, máximos muestreados no garantizan pico. Muestreo separado de inferencia; puede influir en la carga.

Las muestras completas de RAM, uso de GPU, VRAM, potencia y temperatura disponibles están en el JSON de recursos. La potencia GPU global en vatios no equivale al consumo energético del ASR.

| GPU global | Muestras | Uso medio / máx. (%) | VRAM máx. (MiB) | Potencia media / máx. (W) | Temperatura máx. (°C) |
|---|---:|---|---:|---|---:|
| NVIDIA GeForce RTX 3050 Laptop GPU | 37 | 0.000 / 0.000 | 481.000 | 6.344 / 6.380 | 45.000 |
| lectura_20261023_100912_195344_ventana_4s_r2.json | cpu | int8 | no (CPU) | 0.545 | 1.947 | medido |

**lectura_20261023_100912_195344_ventana_4s_r2.json:** CPU 11th Gen Intel(R) Core(TM) i7-11800H @ 2.30GHz; 16 procesadores lógicos; Windows-11-10.0.26200-SP0. CPU media del proceso: 24.793% de capacidad lógica del equipo. Pico de RAM del proceso durante su vida: 703.336 MiB. Carga del modelo: 0.972 s.

CPU y RAM del proceso completo, incluido muestreo. CPU 100% equivale a un procesador lógico; puede superar 100%. GPU/VRAM/potencia/temperatura son del equipo completo, no del ASR. No se mide energía específica, FLOPs ni rendimiento de tablet. Intervalos reales registrados, máximos muestreados no garantizan pico. Muestreo separado de inferencia; puede influir en la carga.

Las muestras completas de RAM, uso de GPU, VRAM, potencia y temperatura disponibles están en el JSON de recursos. La potencia GPU global en vatios no equivale al consumo energético del ASR.

| GPU global | Muestras | Uso medio / máx. (%) | VRAM máx. (MiB) | Potencia media / máx. (W) | Temperatura máx. (°C) |
|---|---:|---|---:|---|---:|
| NVIDIA GeForce RTX 3050 Laptop GPU | 25 | 0.000 / 0.000 | 481.000 | 6.348 / 6.400 | 45.000 |
| lectura_20261023_100912_195344_ventana_4s_r3.json | cpu | int8 | no (CPU) | 0.568 | 2.434 | medido |

**lectura_20261023_100912_195344_ventana_4s_r3.json:** CPU 11th Gen Intel(R) Core(TM) i7-11800H @ 2.30GHz; 16 procesadores lógicos; Windows-11-10.0.26200-SP0. CPU media del proceso: 24.684% de capacidad lógica del equipo. Pico de RAM del proceso durante su vida: 703.516 MiB. Carga del modelo: 0.993 s.

CPU y RAM del proceso completo, incluido muestreo. CPU 100% equivale a un procesador lógico; puede superar 100%. GPU/VRAM/potencia/temperatura son del equipo completo, no del ASR. No se mide energía específica, FLOPs ni rendimiento de tablet. Intervalos reales registrados, máximos muestreados no garantizan pico. Muestreo separado de inferencia; puede influir en la carga.

Las muestras completas de RAM, uso de GPU, VRAM, potencia y temperatura disponibles están en el JSON de recursos. La potencia GPU global en vatios no equivale al consumo energético del ASR.

| GPU global | Muestras | Uso medio / máx. (%) | VRAM máx. (MiB) | Potencia media / máx. (W) | Temperatura máx. (°C) |
|---|---:|---|---:|---|---:|
| NVIDIA GeForce RTX 3050 Laptop GPU | 27 | 0.000 / 0.000 | 481.000 | 6.356 / 6.390 | 45.000 |
| lectura_20261023_100912_195344_ventana_8s_r3.json | cpu | int8 | no (CPU) | 0.853 | 10.929 | medido |

**lectura_20261023_100912_195344_ventana_8s_r3.json:** CPU 11th Gen Intel(R) Core(TM) i7-11800H @ 2.30GHz; 16 procesadores lógicos; Windows-11-10.0.26200-SP0. CPU media del proceso: 24.870% de capacidad lógica del equipo. Pico de RAM del proceso durante su vida: 1051.055 MiB. Carga del modelo: 1.056 s.

CPU y RAM del proceso completo, incluido muestreo. CPU 100% equivale a un procesador lógico; puede superar 100%. GPU/VRAM/potencia/temperatura son del equipo completo, no del ASR. No se mide energía específica, FLOPs ni rendimiento de tablet. Intervalos reales registrados, máximos muestreados no garantizan pico. Muestreo separado de inferencia; puede influir en la carga.

Las muestras completas de RAM, uso de GPU, VRAM, potencia y temperatura disponibles están en el JSON de recursos. La potencia GPU global en vatios no equivale al consumo energético del ASR.

| GPU global | Muestras | Uso medio / máx. (%) | VRAM máx. (MiB) | Potencia media / máx. (W) | Temperatura máx. (°C) |
|---|---:|---|---:|---|---:|
| NVIDIA GeForce RTX 3050 Laptop GPU | 39 | 0.000 / 0.000 | 481.000 | 6.361 / 6.390 | 46.000 |

Para comparar tablets habrá que medir en el dispositivo de destino: RAM máxima, tiempo de respuesta sostenido y consumo/batería. Este ordenador no permite deducir esos valores. No se cambia CPU por GPU automáticamente.
<!-- recursos-computo-fin -->
