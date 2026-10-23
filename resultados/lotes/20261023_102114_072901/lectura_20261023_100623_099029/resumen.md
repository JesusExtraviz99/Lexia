# Comparación de reprocesamiento

3 ronda(s) por configuración, orden aleatorio reproducible por ronda. Ejecución secuencial para no competir por CPU. Tiempos orientativos, afectados por carga y calentamiento. No hay referencia humana de posición ni latencia visual. Comparar posiciones entre métodos no demuestra precisión.

Mismo modelo, CPU int8, VAD, bloques de 2 s, cuento y seguidor. La carga del modelo se excluye de los tiempos de inferencia. Solapamiento = ventana menos 2 s; no aplica al prefijo. El silencio final puede reducir los totales de las ventanas.

| Audio | Método | Ronda | Total inferencia (s) | Mediana (s) | P95 (s) | Inferencias >2 s | Cola máxima simulada (s) | Posición final | Retrocesos |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Lectura pausa con relectura barco rojo - el barco - cuento 2 - lectura_02 - 23-10-2026.wav | ventana_8s | 1 | 46.70 | 1.89 | 2.08 | 2 | 3.84 | 56 | 1 |
| Lectura pausa con relectura barco rojo - el barco - cuento 2 - lectura_02 - 23-10-2026.wav | ventana_4s | 1 | 33.93 | 1.75 | 1.91 | 0 | 0.00 | 56 | 1 |
| Lectura pausa con relectura barco rojo - el barco - cuento 2 - lectura_02 - 23-10-2026.wav | ventana_8s | 2 | 48.13 | 1.93 | 2.17 | 8 | 3.81 | 56 | 1 |
| Lectura pausa con relectura barco rojo - el barco - cuento 2 - lectura_02 - 23-10-2026.wav | ventana_4s | 2 | 34.34 | 1.77 | 1.91 | 1 | 0.01 | 56 | 1 |
| Lectura pausa con relectura barco rojo - el barco - cuento 2 - lectura_02 - 23-10-2026.wav | ventana_4s | 3 | 34.33 | 1.80 | 1.94 | 0 | 0.00 | 56 | 1 |
| Lectura pausa con relectura barco rojo - el barco - cuento 2 - lectura_02 - 23-10-2026.wav | ventana_8s | 3 | 48.20 | 1.92 | 2.25 | 5 | 4.31 | 56 | 1 |

## Posiciones en cada actualización

Comparación descriptiva con el prefijo, no referencia de precisión. El prefijo también puede equivocarse.

### Lectura pausa con relectura barco rojo - el barco - cuento 2 - lectura_02 - 23-10-2026.wav, ronda 1

| Audio disponible (s) | ventana_4s | ventana_8s |
|---:|---:|---:|
| 2.0 | 2 | 2 |
| 4.0 | 6 | 6 |
| 6.0 | 10 | 10 |
| 8.0 | 15 | 15 |
| 10.0 | 19 | 19 |
| 12.0 | 19 | 19 |
| 14.0 | 19 | 19 |
| 16.0 | 19 | 19 |
| 18.0 | 19 | 19 |
| 20.0 | 13 | 13 |
| 22.0 | 17 | 17 |
| 24.0 | 19 | 19 |
| 26.0 | 23 | 23 |
| 28.0 | 26 | 27 |
| 30.0 | 31 | 31 |
| 32.0 | 37 | 37 |
| 34.0 | 40 | 40 |
| 36.0 | 44 | 44 |
| 38.0 | 48 | 47 |
| 40.0 | 53 | 53 |
| 42.0 | 56 | 56 |
| 44.0 | 56 | 56 |
| 46.0 | 56 | 56 |
| 48.0 | 56 | 56 |
| 50.0 | 56 | 56 |

### Lectura pausa con relectura barco rojo - el barco - cuento 2 - lectura_02 - 23-10-2026.wav, ronda 2

| Audio disponible (s) | ventana_4s | ventana_8s |
|---:|---:|---:|
| 2.0 | 2 | 2 |
| 4.0 | 6 | 6 |
| 6.0 | 10 | 10 |
| 8.0 | 15 | 15 |
| 10.0 | 19 | 19 |
| 12.0 | 19 | 19 |
| 14.0 | 19 | 19 |
| 16.0 | 19 | 19 |
| 18.0 | 19 | 19 |
| 20.0 | 13 | 13 |
| 22.0 | 17 | 17 |
| 24.0 | 19 | 19 |
| 26.0 | 23 | 23 |
| 28.0 | 26 | 27 |
| 30.0 | 31 | 31 |
| 32.0 | 37 | 37 |
| 34.0 | 40 | 40 |
| 36.0 | 44 | 44 |
| 38.0 | 48 | 47 |
| 40.0 | 53 | 53 |
| 42.0 | 56 | 56 |
| 44.0 | 56 | 56 |
| 46.0 | 56 | 56 |
| 48.0 | 56 | 56 |
| 50.0 | 56 | 56 |

### Lectura pausa con relectura barco rojo - el barco - cuento 2 - lectura_02 - 23-10-2026.wav, ronda 3

| Audio disponible (s) | ventana_4s | ventana_8s |
|---:|---:|---:|
| 2.0 | 2 | 2 |
| 4.0 | 6 | 6 |
| 6.0 | 10 | 10 |
| 8.0 | 15 | 15 |
| 10.0 | 19 | 19 |
| 12.0 | 19 | 19 |
| 14.0 | 19 | 19 |
| 16.0 | 19 | 19 |
| 18.0 | 19 | 19 |
| 20.0 | 13 | 13 |
| 22.0 | 17 | 17 |
| 24.0 | 19 | 19 |
| 26.0 | 23 | 23 |
| 28.0 | 26 | 27 |
| 30.0 | 31 | 31 |
| 32.0 | 37 | 37 |
| 34.0 | 40 | 40 |
| 36.0 | 44 | 44 |
| 38.0 | 48 | 47 |
| 40.0 | 53 | 53 |
| 42.0 | 56 | 56 |
| 44.0 | 56 | 56 |
| 46.0 | 56 | 56 |
| 48.0 | 56 | 56 |
| 50.0 | 56 | 56 |

## Resumen por configuración

| Audio | Método | Total medio (s) | Rango de totales (s) | Cola máxima media (s) | Inferencias >2 s | Posiciones finales |
|---|---|---:|---|---:|---|---|
| Lectura pausa con relectura barco rojo - el barco - cuento 2 - lectura_02 - 23-10-2026.wav | ventana_4s | 34.20 | 33.93–34.34 | 0.00 | 1/75 | [56, 56, 56] |
| Lectura pausa con relectura barco rojo - el barco - cuento 2 - lectura_02 - 23-10-2026.wav | ventana_8s | 47.68 | 46.70–48.20 | 3.98 | 15/75 | [56, 56, 56] |

<!-- recursos-computo-inicio -->
## Recursos y coste computacional

Datos de la ejecución original. «No medido» no significa cero. RTF = suma de inferencias / duración del audio completo (incluye silencio); no es latencia visual ni mide captura, escritura o muestreo. Las rondas de una grabación no son lecturas independientes.

| Registro | Dispositivo ASR | Precisión | GPU para ASR | RTF | Máx. inferencia (s) | CPU/RAM/GPU instrumentadas |
|---|---|---|---|---:|---:|---|
| lectura_20261023_100623_099029_ventana_8s_r1.json | cpu | int8 | no (CPU) | 0.934 | 5.754 | medido |

**lectura_20261023_100623_099029_ventana_8s_r1.json:** CPU 11th Gen Intel(R) Core(TM) i7-11800H @ 2.30GHz; 16 procesadores lógicos; Windows-11-10.0.26200-SP0. CPU media del proceso: 24.794% de capacidad lógica del equipo. Pico de RAM del proceso durante su vida: 964.227 MiB. Carga del modelo: 1.393 s.

CPU y RAM del proceso completo, incluido muestreo. CPU 100% equivale a un procesador lógico; puede superar 100%. GPU/VRAM/potencia/temperatura son del equipo completo, no del ASR. No se mide energía específica, FLOPs ni rendimiento de tablet. Intervalos reales registrados, máximos muestreados no garantizan pico. Muestreo separado de inferencia; puede influir en la carga.

Las muestras completas de RAM, uso de GPU, VRAM, potencia y temperatura disponibles están en el JSON de recursos. La potencia GPU global en vatios no equivale al consumo energético del ASR.

| GPU global | Muestras | Uso medio / máx. (%) | VRAM máx. (MiB) | Potencia media / máx. (W) | Temperatura máx. (°C) |
|---|---:|---|---:|---|---:|
| NVIDIA GeForce RTX 3050 Laptop GPU | 43 | 0.000 / 0.000 | 481.000 | 6.364 / 6.400 | 45.000 |
| lectura_20261023_100623_099029_ventana_4s_r1.json | cpu | int8 | no (CPU) | 0.679 | 1.942 | medido |

**lectura_20261023_100623_099029_ventana_4s_r1.json:** CPU 11th Gen Intel(R) Core(TM) i7-11800H @ 2.30GHz; 16 procesadores lógicos; Windows-11-10.0.26200-SP0. CPU media del proceso: 24.863% de capacidad lógica del equipo. Pico de RAM del proceso durante su vida: 703.641 MiB. Carga del modelo: 0.956 s.

CPU y RAM del proceso completo, incluido muestreo. CPU 100% equivale a un procesador lógico; puede superar 100%. GPU/VRAM/potencia/temperatura son del equipo completo, no del ASR. No se mide energía específica, FLOPs ni rendimiento de tablet. Intervalos reales registrados, máximos muestreados no garantizan pico. Muestreo separado de inferencia; puede influir en la carga.

Las muestras completas de RAM, uso de GPU, VRAM, potencia y temperatura disponibles están en el JSON de recursos. La potencia GPU global en vatios no equivale al consumo energético del ASR.

| GPU global | Muestras | Uso medio / máx. (%) | VRAM máx. (MiB) | Potencia media / máx. (W) | Temperatura máx. (°C) |
|---|---:|---|---:|---|---:|
| NVIDIA GeForce RTX 3050 Laptop GPU | 32 | 0.000 / 0.000 | 481.000 | 6.354 / 6.390 | 45.000 |
| lectura_20261023_100623_099029_ventana_8s_r2.json | cpu | int8 | no (CPU) | 0.963 | 5.566 | medido |

**lectura_20261023_100623_099029_ventana_8s_r2.json:** CPU 11th Gen Intel(R) Core(TM) i7-11800H @ 2.30GHz; 16 procesadores lógicos; Windows-11-10.0.26200-SP0. CPU media del proceso: 24.915% de capacidad lógica del equipo. Pico de RAM del proceso durante su vida: 965.227 MiB. Carga del modelo: 0.993 s.

CPU y RAM del proceso completo, incluido muestreo. CPU 100% equivale a un procesador lógico; puede superar 100%. GPU/VRAM/potencia/temperatura son del equipo completo, no del ASR. No se mide energía específica, FLOPs ni rendimiento de tablet. Intervalos reales registrados, máximos muestreados no garantizan pico. Muestreo separado de inferencia; puede influir en la carga.

Las muestras completas de RAM, uso de GPU, VRAM, potencia y temperatura disponibles están en el JSON de recursos. La potencia GPU global en vatios no equivale al consumo energético del ASR.

| GPU global | Muestras | Uso medio / máx. (%) | VRAM máx. (MiB) | Potencia media / máx. (W) | Temperatura máx. (°C) |
|---|---:|---|---:|---|---:|
| NVIDIA GeForce RTX 3050 Laptop GPU | 44 | 0.000 / 0.000 | 481.000 | 6.362 / 6.400 | 45.000 |
| lectura_20261023_100623_099029_ventana_4s_r2.json | cpu | int8 | no (CPU) | 0.687 | 2.008 | medido |

**lectura_20261023_100623_099029_ventana_4s_r2.json:** CPU 11th Gen Intel(R) Core(TM) i7-11800H @ 2.30GHz; 16 procesadores lógicos; Windows-11-10.0.26200-SP0. CPU media del proceso: 24.836% de capacidad lógica del equipo. Pico de RAM del proceso durante su vida: 703.266 MiB. Carga del modelo: 1.001 s.

CPU y RAM del proceso completo, incluido muestreo. CPU 100% equivale a un procesador lógico; puede superar 100%. GPU/VRAM/potencia/temperatura son del equipo completo, no del ASR. No se mide energía específica, FLOPs ni rendimiento de tablet. Intervalos reales registrados, máximos muestreados no garantizan pico. Muestreo separado de inferencia; puede influir en la carga.

Las muestras completas de RAM, uso de GPU, VRAM, potencia y temperatura disponibles están en el JSON de recursos. La potencia GPU global en vatios no equivale al consumo energético del ASR.

| GPU global | Muestras | Uso medio / máx. (%) | VRAM máx. (MiB) | Potencia media / máx. (W) | Temperatura máx. (°C) |
|---|---:|---|---:|---|---:|
| NVIDIA GeForce RTX 3050 Laptop GPU | 32 | 0.000 / 0.000 | 481.000 | 6.355 / 6.390 | 45.000 |
| lectura_20261023_100623_099029_ventana_4s_r3.json | cpu | int8 | no (CPU) | 0.687 | 1.939 | medido |

**lectura_20261023_100623_099029_ventana_4s_r3.json:** CPU 11th Gen Intel(R) Core(TM) i7-11800H @ 2.30GHz; 16 procesadores lógicos; Windows-11-10.0.26200-SP0. CPU media del proceso: 24.841% de capacidad lógica del equipo. Pico de RAM del proceso durante su vida: 703.500 MiB. Carga del modelo: 0.992 s.

CPU y RAM del proceso completo, incluido muestreo. CPU 100% equivale a un procesador lógico; puede superar 100%. GPU/VRAM/potencia/temperatura son del equipo completo, no del ASR. No se mide energía específica, FLOPs ni rendimiento de tablet. Intervalos reales registrados, máximos muestreados no garantizan pico. Muestreo separado de inferencia; puede influir en la carga.

Las muestras completas de RAM, uso de GPU, VRAM, potencia y temperatura disponibles están en el JSON de recursos. La potencia GPU global en vatios no equivale al consumo energético del ASR.

| GPU global | Muestras | Uso medio / máx. (%) | VRAM máx. (MiB) | Potencia media / máx. (W) | Temperatura máx. (°C) |
|---|---:|---|---:|---|---:|
| NVIDIA GeForce RTX 3050 Laptop GPU | 32 | 0.000 / 0.000 | 481.000 | 6.353 / 6.390 | 45.000 |
| lectura_20261023_100623_099029_ventana_8s_r3.json | cpu | int8 | no (CPU) | 0.964 | 5.955 | medido |

**lectura_20261023_100623_099029_ventana_8s_r3.json:** CPU 11th Gen Intel(R) Core(TM) i7-11800H @ 2.30GHz; 16 procesadores lógicos; Windows-11-10.0.26200-SP0. CPU media del proceso: 24.881% de capacidad lógica del equipo. Pico de RAM del proceso durante su vida: 967.059 MiB. Carga del modelo: 1.011 s.

CPU y RAM del proceso completo, incluido muestreo. CPU 100% equivale a un procesador lógico; puede superar 100%. GPU/VRAM/potencia/temperatura son del equipo completo, no del ASR. No se mide energía específica, FLOPs ni rendimiento de tablet. Intervalos reales registrados, máximos muestreados no garantizan pico. Muestreo separado de inferencia; puede influir en la carga.

Las muestras completas de RAM, uso de GPU, VRAM, potencia y temperatura disponibles están en el JSON de recursos. La potencia GPU global en vatios no equivale al consumo energético del ASR.

| GPU global | Muestras | Uso medio / máx. (%) | VRAM máx. (MiB) | Potencia media / máx. (W) | Temperatura máx. (°C) |
|---|---:|---|---:|---|---:|
| NVIDIA GeForce RTX 3050 Laptop GPU | 44 | 0.000 / 0.000 | 481.000 | 6.361 / 6.450 | 45.000 |

Para comparar tablets habrá que medir en el dispositivo de destino: RAM máxima, tiempo de respuesta sostenido y consumo/batería. Este ordenador no permite deducir esos valores. No se cambia CPU por GPU automáticamente.
<!-- recursos-computo-fin -->
