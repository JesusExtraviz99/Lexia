# Comparación de reprocesamiento

3 ronda(s) por configuración, orden aleatorio reproducible por ronda. Ejecución secuencial para no competir por CPU. Tiempos orientativos, afectados por carga y calentamiento. No hay referencia humana de posición ni latencia visual. Comparar posiciones entre métodos no demuestra precisión.

Mismo modelo, CPU int8, VAD, bloques de 2 s, cuento y seguidor. La carga del modelo se excluye de los tiempos de inferencia. Solapamiento = ventana menos 2 s; no aplica al prefijo. El silencio final puede reducir los totales de las ventanas.

| Audio | Método | Ronda | Total inferencia (s) | Mediana (s) | P95 (s) | Inferencias >2 s | Cola máxima simulada (s) | Posición final | Retrocesos |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Lectura con ruido de fondo - cuento 2 - lectura_02 - 23-10-2026.wav | ventana_8s | 1 | 41.80 | 2.31 | 2.75 | 17 | 7.64 | 56 | 0 |
| Lectura con ruido de fondo - cuento 2 - lectura_02 - 23-10-2026.wav | ventana_4s | 1 | 26.34 | 1.68 | 1.82 | 0 | 0.00 | 56 | 0 |
| Lectura con ruido de fondo - cuento 2 - lectura_02 - 23-10-2026.wav | ventana_8s | 2 | 31.63 | 1.77 | 1.99 | 1 | 0.06 | 56 | 0 |
| Lectura con ruido de fondo - cuento 2 - lectura_02 - 23-10-2026.wav | ventana_4s | 2 | 26.67 | 1.70 | 1.87 | 0 | 0.00 | 56 | 0 |
| Lectura con ruido de fondo - cuento 2 - lectura_02 - 23-10-2026.wav | ventana_4s | 3 | 27.07 | 1.70 | 1.95 | 0 | 0.00 | 56 | 0 |
| Lectura con ruido de fondo - cuento 2 - lectura_02 - 23-10-2026.wav | ventana_8s | 3 | 32.83 | 1.90 | 2.11 | 4 | 0.22 | 56 | 0 |

## Posiciones en cada actualización

Comparación descriptiva con el prefijo, no referencia de precisión. El prefijo también puede equivocarse.

### Lectura con ruido de fondo - cuento 2 - lectura_02 - 23-10-2026.wav, ronda 1

| Audio disponible (s) | ventana_4s | ventana_8s |
|---:|---:|---:|
| 2.0 | 2 | 2 |
| 4.0 | 6 | 6 |
| 6.0 | 11 | 11 |
| 8.0 | 17 | 17 |
| 10.0 | 19 | 19 |
| 12.0 | 24 | 24 |
| 14.0 | 27 | 27 |
| 16.0 | 33 | 32 |
| 18.0 | 37 | 37 |
| 20.0 | 37 | 41 |
| 22.0 | 46 | 46 |
| 24.0 | 46 | 47 |
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

### Lectura con ruido de fondo - cuento 2 - lectura_02 - 23-10-2026.wav, ronda 2

| Audio disponible (s) | ventana_4s | ventana_8s |
|---:|---:|---:|
| 2.0 | 2 | 2 |
| 4.0 | 6 | 6 |
| 6.0 | 11 | 11 |
| 8.0 | 17 | 17 |
| 10.0 | 19 | 19 |
| 12.0 | 24 | 24 |
| 14.0 | 27 | 27 |
| 16.0 | 33 | 32 |
| 18.0 | 37 | 37 |
| 20.0 | 37 | 41 |
| 22.0 | 46 | 46 |
| 24.0 | 46 | 47 |
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

### Lectura con ruido de fondo - cuento 2 - lectura_02 - 23-10-2026.wav, ronda 3

| Audio disponible (s) | ventana_4s | ventana_8s |
|---:|---:|---:|
| 2.0 | 2 | 2 |
| 4.0 | 6 | 6 |
| 6.0 | 11 | 11 |
| 8.0 | 17 | 17 |
| 10.0 | 19 | 19 |
| 12.0 | 24 | 24 |
| 14.0 | 27 | 27 |
| 16.0 | 33 | 32 |
| 18.0 | 37 | 37 |
| 20.0 | 37 | 41 |
| 22.0 | 46 | 46 |
| 24.0 | 46 | 47 |
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
| Lectura con ruido de fondo - cuento 2 - lectura_02 - 23-10-2026.wav | ventana_4s | 26.69 | 26.34–27.07 | 0.00 | 0/75 | [56, 56, 56] |
| Lectura con ruido de fondo - cuento 2 - lectura_02 - 23-10-2026.wav | ventana_8s | 35.42 | 31.63–41.80 | 2.64 | 22/75 | [56, 56, 56] |

<!-- recursos-computo-inicio -->
## Recursos y coste computacional

Datos de la ejecución original. «No medido» no significa cero. RTF = suma de inferencias / duración del audio completo (incluye silencio); no es latencia visual ni mide captura, escritura o muestreo. Las rondas de una grabación no son lecturas independientes.

| Registro | Dispositivo ASR | Precisión | GPU para ASR | RTF | Máx. inferencia (s) | CPU/RAM/GPU instrumentadas |
|---|---|---|---|---:|---:|---|
| lectura_20261023_101133_857937_ventana_8s_r1.json | cpu | int8 | no (CPU) | 0.836 | 2.775 | medido |

**lectura_20261023_101133_857937_ventana_8s_r1.json:** CPU 11th Gen Intel(R) Core(TM) i7-11800H @ 2.30GHz; 16 procesadores lógicos; Windows-11-10.0.26200-SP0. CPU media del proceso: 24.324% de capacidad lógica del equipo. Pico de RAM del proceso durante su vida: 703.242 MiB. Carga del modelo: 1.425 s.

CPU y RAM del proceso completo, incluido muestreo. CPU 100% equivale a un procesador lógico; puede superar 100%. GPU/VRAM/potencia/temperatura son del equipo completo, no del ASR. No se mide energía específica, FLOPs ni rendimiento de tablet. Intervalos reales registrados, máximos muestreados no garantizan pico. Muestreo separado de inferencia; puede influir en la carga.

Las muestras completas de RAM, uso de GPU, VRAM, potencia y temperatura disponibles están en el JSON de recursos. La potencia GPU global en vatios no equivale al consumo energético del ASR.

| GPU global | Muestras | Uso medio / máx. (%) | VRAM máx. (MiB) | Potencia media / máx. (W) | Temperatura máx. (°C) |
|---|---:|---|---:|---|---:|
| NVIDIA GeForce RTX 3050 Laptop GPU | 38 | 0.000 / 0.000 | 481.000 | 6.349 / 6.450 | 45.000 |
| lectura_20261023_101133_857937_ventana_4s_r1.json | cpu | int8 | no (CPU) | 0.527 | 1.833 | medido |

**lectura_20261023_101133_857937_ventana_4s_r1.json:** CPU 11th Gen Intel(R) Core(TM) i7-11800H @ 2.30GHz; 16 procesadores lógicos; Windows-11-10.0.26200-SP0. CPU media del proceso: 24.801% de capacidad lógica del equipo. Pico de RAM del proceso durante su vida: 703.262 MiB. Carga del modelo: 0.986 s.

CPU y RAM del proceso completo, incluido muestreo. CPU 100% equivale a un procesador lógico; puede superar 100%. GPU/VRAM/potencia/temperatura son del equipo completo, no del ASR. No se mide energía específica, FLOPs ni rendimiento de tablet. Intervalos reales registrados, máximos muestreados no garantizan pico. Muestreo separado de inferencia; puede influir en la carga.

Las muestras completas de RAM, uso de GPU, VRAM, potencia y temperatura disponibles están en el JSON de recursos. La potencia GPU global en vatios no equivale al consumo energético del ASR.

| GPU global | Muestras | Uso medio / máx. (%) | VRAM máx. (MiB) | Potencia media / máx. (W) | Temperatura máx. (°C) |
|---|---:|---|---:|---|---:|
| NVIDIA GeForce RTX 3050 Laptop GPU | 25 | 0.000 / 0.000 | 481.000 | 6.350 / 6.390 | 46.000 |
| lectura_20261023_101133_857937_ventana_8s_r2.json | cpu | int8 | no (CPU) | 0.633 | 2.064 | medido |

**lectura_20261023_101133_857937_ventana_8s_r2.json:** CPU 11th Gen Intel(R) Core(TM) i7-11800H @ 2.30GHz; 16 procesadores lógicos; Windows-11-10.0.26200-SP0. CPU media del proceso: 24.783% de capacidad lógica del equipo. Pico de RAM del proceso durante su vida: 703.320 MiB. Carga del modelo: 0.978 s.

CPU y RAM del proceso completo, incluido muestreo. CPU 100% equivale a un procesador lógico; puede superar 100%. GPU/VRAM/potencia/temperatura son del equipo completo, no del ASR. No se mide energía específica, FLOPs ni rendimiento de tablet. Intervalos reales registrados, máximos muestreados no garantizan pico. Muestreo separado de inferencia; puede influir en la carga.

Las muestras completas de RAM, uso de GPU, VRAM, potencia y temperatura disponibles están en el JSON de recursos. La potencia GPU global en vatios no equivale al consumo energético del ASR.

| GPU global | Muestras | Uso medio / máx. (%) | VRAM máx. (MiB) | Potencia media / máx. (W) | Temperatura máx. (°C) |
|---|---:|---|---:|---|---:|
| NVIDIA GeForce RTX 3050 Laptop GPU | 30 | 0.000 / 0.000 | 481.000 | 6.347 / 6.390 | 45.000 |
| lectura_20261023_101133_857937_ventana_4s_r2.json | cpu | int8 | no (CPU) | 0.533 | 1.951 | medido |

**lectura_20261023_101133_857937_ventana_4s_r2.json:** CPU 11th Gen Intel(R) Core(TM) i7-11800H @ 2.30GHz; 16 procesadores lógicos; Windows-11-10.0.26200-SP0. CPU media del proceso: 24.791% de capacidad lógica del equipo. Pico de RAM del proceso durante su vida: 703.316 MiB. Carga del modelo: 0.923 s.

CPU y RAM del proceso completo, incluido muestreo. CPU 100% equivale a un procesador lógico; puede superar 100%. GPU/VRAM/potencia/temperatura son del equipo completo, no del ASR. No se mide energía específica, FLOPs ni rendimiento de tablet. Intervalos reales registrados, máximos muestreados no garantizan pico. Muestreo separado de inferencia; puede influir en la carga.

Las muestras completas de RAM, uso de GPU, VRAM, potencia y temperatura disponibles están en el JSON de recursos. La potencia GPU global en vatios no equivale al consumo energético del ASR.

| GPU global | Muestras | Uso medio / máx. (%) | VRAM máx. (MiB) | Potencia media / máx. (W) | Temperatura máx. (°C) |
|---|---:|---|---:|---|---:|
| NVIDIA GeForce RTX 3050 Laptop GPU | 25 | 0.000 / 0.000 | 481.000 | 6.354 / 6.380 | 45.000 |
| lectura_20261023_101133_857937_ventana_4s_r3.json | cpu | int8 | no (CPU) | 0.541 | 1.962 | medido |

**lectura_20261023_101133_857937_ventana_4s_r3.json:** CPU 11th Gen Intel(R) Core(TM) i7-11800H @ 2.30GHz; 16 procesadores lógicos; Windows-11-10.0.26200-SP0. CPU media del proceso: 24.784% de capacidad lógica del equipo. Pico de RAM del proceso durante su vida: 703.426 MiB. Carga del modelo: 0.944 s.

CPU y RAM del proceso completo, incluido muestreo. CPU 100% equivale a un procesador lógico; puede superar 100%. GPU/VRAM/potencia/temperatura son del equipo completo, no del ASR. No se mide energía específica, FLOPs ni rendimiento de tablet. Intervalos reales registrados, máximos muestreados no garantizan pico. Muestreo separado de inferencia; puede influir en la carga.

Las muestras completas de RAM, uso de GPU, VRAM, potencia y temperatura disponibles están en el JSON de recursos. La potencia GPU global en vatios no equivale al consumo energético del ASR.

| GPU global | Muestras | Uso medio / máx. (%) | VRAM máx. (MiB) | Potencia media / máx. (W) | Temperatura máx. (°C) |
|---|---:|---|---:|---|---:|
| NVIDIA GeForce RTX 3050 Laptop GPU | 25 | 0.000 / 0.000 | 481.000 | 6.341 / 6.380 | 45.000 |
| lectura_20261023_101133_857937_ventana_8s_r3.json | cpu | int8 | no (CPU) | 0.657 | 2.126 | medido |

**lectura_20261023_101133_857937_ventana_8s_r3.json:** CPU 11th Gen Intel(R) Core(TM) i7-11800H @ 2.30GHz; 16 procesadores lógicos; Windows-11-10.0.26200-SP0. CPU media del proceso: 24.816% de capacidad lógica del equipo. Pico de RAM del proceso durante su vida: 703.492 MiB. Carga del modelo: 1.001 s.

CPU y RAM del proceso completo, incluido muestreo. CPU 100% equivale a un procesador lógico; puede superar 100%. GPU/VRAM/potencia/temperatura son del equipo completo, no del ASR. No se mide energía específica, FLOPs ni rendimiento de tablet. Intervalos reales registrados, máximos muestreados no garantizan pico. Muestreo separado de inferencia; puede influir en la carga.

Las muestras completas de RAM, uso de GPU, VRAM, potencia y temperatura disponibles están en el JSON de recursos. La potencia GPU global en vatios no equivale al consumo energético del ASR.

| GPU global | Muestras | Uso medio / máx. (%) | VRAM máx. (MiB) | Potencia media / máx. (W) | Temperatura máx. (°C) |
|---|---:|---|---:|---|---:|
| NVIDIA GeForce RTX 3050 Laptop GPU | 31 | 0.000 / 0.000 | 481.000 | 6.345 / 6.390 | 45.000 |

Para comparar tablets habrá que medir en el dispositivo de destino: RAM máxima, tiempo de respuesta sostenido y consumo/batería. Este ordenador no permite deducir esos valores. No se cambia CPU por GPU automáticamente.
<!-- recursos-computo-fin -->
