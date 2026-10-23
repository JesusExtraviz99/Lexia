# Seguimiento progresivo simulado

Simulación posterior, no streaming nativo ni medida de latencia visual. Tiempos ASR estimados. Posiciones provisionales, sin valoración lectora.

Convención: última palabra apoyada por coincidencia textual; no se califica pronunciación.

Audio por inferencia: últimos 4.0 segundos. Bloque: 2.0 s. Sin audio futuro.
Las hipótesis de ventanas solapadas se alinean de forma independiente manteniendo el estado del seguidor. No se concatenan como una transcripción definitiva ni se cuentan intentos repetidos por el solapamiento.
La cola secuencial simulada supone el modelo ya cargado y no mide transferencia ni pantalla.

| Audio disponible (s) | Posición | Palabra | Movimiento | Procesamiento (s) | Cola simulada (s) | Modo |
|---:|---:|---|---:|---:|---:|---|
| 2.0 | 2 | tarde | 2 | 2.07 | 0.00 | local |
| 4.0 | 7 | parque | 5 | 1.81 | 0.07 | local |
| 6.0 | 12 | a | 5 | 1.99 | 0.00 | local |
| 8.0 | 17 | pequeño | 5 | 1.92 | 0.00 | local |

## Hipótesis disponibles

- Hasta 2.0 s: una tarde
- Hasta 4.0 s: Una tarde Lucía paseaba por el parque
- Hasta 6.0 s: Lucía paseaba por el parque con su abuelo junto a un
- Hasta 8.0 s: con su abuelo Junto a una fuente descubrió un pequeño

## Recursos y coste computacional

Datos de la ejecución original. «No medido» no significa cero. RTF = suma de inferencias / duración del audio completo (incluye silencio); no es latencia visual ni mide captura, escritura o muestreo. Las rondas de una grabación no son lecturas independientes.

| Registro | Dispositivo ASR | Precisión | GPU para ASR | RTF | Máx. inferencia (s) | CPU/RAM/GPU instrumentadas |
|---|---|---|---|---:|---:|---|
| verificacion_4s.json | cpu | int8 | no (CPU) | 0.974 | 2.074 | medido |

**verificacion_4s.json:** CPU 11th Gen Intel(R) Core(TM) i7-11800H @ 2.30GHz; 16 procesadores lógicos; Windows-11-10.0.26200-SP0. CPU media del proceso: 22.541% de capacidad lógica del equipo. Pico de RAM del proceso durante su vida: 697.395 MiB. Carga del modelo: 1.881 s.

CPU y RAM del proceso completo, incluido muestreo. CPU 100% equivale a un procesador lógico; puede superar 100%. GPU/VRAM/potencia/temperatura son del equipo completo, no del ASR. No se mide energía específica, FLOPs ni rendimiento de tablet. Intervalos reales registrados, máximos muestreados no garantizan pico. Muestreo separado de inferencia; puede influir en la carga.

Las muestras completas de RAM, uso de GPU, VRAM, potencia y temperatura disponibles están en el JSON de recursos. La potencia GPU global en vatios no equivale al consumo energético del ASR.

| GPU global | Muestras | Uso medio / máx. (%) | VRAM máx. (MiB) | Potencia media / máx. (W) | Temperatura máx. (°C) |
|---|---:|---|---:|---|---:|
| NVIDIA GeForce RTX 3050 Laptop GPU | 9 | 0.000 / 0.000 | 504.000 | 6.408 / 6.430 | 48.000 |

Para comparar tablets habrá que medir en el dispositivo de destino: RAM máxima, tiempo de respuesta sostenido y consumo/batería. Este ordenador no permite deducir esos valores. No se cambia CPU por GPU automáticamente.

