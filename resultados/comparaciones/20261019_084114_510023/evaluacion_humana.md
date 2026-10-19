# Seguimiento frente a marcas humanas

Referencia de desarrollo revisada por el lector, no independiente. Posición de referencia = última palabra terminada (fin <= instante). Error firmado = posición estimada menos referencia: negativo es retraso. Muestras cada 2 s dentro de la lectura, desde la primera palabra hasta el fin de la última; se excluye el silencio final de las medias. La hipótesis al corte ignora coste de cómputo; la posición visible simulada conserva la última salida ya lista en ese mismo instante, incluyendo cola secuencial y sin carga de modelo ni latencia de pantalla. Límites ambiguos y muestreo de 2 s limitan la interpretación. Tres rondas del mismo audio no son tres lectores ni validación en otros entornos.

| Ventana | Ronda | Cortes | Error absoluto medio hipótesis (palabras) | Error absoluto medio visible simulado (palabras) | Demora final simulada (s) |
|---:|---:|---:|---:|---:|---:|
| 6.0 | 1 | 11 | 0.36 | 8.82 | 3.66 |
| 4.0 | 1 | 11 | 0.45 | 7.27 | 4.70 |
| 8.0 | 1 | 11 | 0.36 | 10.27 | 7.32 |
| 6.0 | 2 | 11 | 0.36 | 7.27 | 3.52 |
| 4.0 | 2 | 11 | 0.45 | 4.55 | 2.75 |
| 8.0 | 2 | 11 | 0.36 | 5.27 | 3.09 |
| 4.0 | 3 | 11 | 0.45 | 4.55 | 2.77 |
| 8.0 | 3 | 11 | 0.36 | 4.64 | 2.95 |
| 6.0 | 3 | 11 | 0.36 | 4.64 | 2.91 |

## Posición por corte

| Ventana | Ronda | Audio (s) | Referencia | Hipótesis | Visible simulado |
|---:|---:|---:|---:|---:|---:|
| 6.0 | 1 | 2.0 | 1 | 0 | 0 |
| 6.0 | 1 | 4.0 | 5 | 5 | 0 |
| 6.0 | 1 | 6.0 | 11 | 12 | 0 |
| 6.0 | 1 | 8.0 | 17 | 17 | 5 |
| 6.0 | 1 | 10.0 | 20 | 20 | 12 |
| 6.0 | 1 | 12.0 | 27 | 27 | 17 |
| 6.0 | 1 | 14.0 | 34 | 34 | 20 |
| 6.0 | 1 | 16.0 | 37 | 38 | 27 |
| 6.0 | 1 | 18.0 | 43 | 43 | 34 |
| 6.0 | 1 | 20.0 | 46 | 46 | 38 |
| 6.0 | 1 | 22.0 | 52 | 53 | 43 |
| 4.0 | 1 | 2.0 | 1 | 0 | 0 |
| 4.0 | 1 | 4.0 | 5 | 5 | 0 |
| 4.0 | 1 | 6.0 | 11 | 12 | 5 |
| 4.0 | 1 | 8.0 | 17 | 17 | 12 |
| 4.0 | 1 | 10.0 | 20 | 20 | 17 |
| 4.0 | 1 | 12.0 | 27 | 27 | 17 |
| 4.0 | 1 | 14.0 | 34 | 34 | 20 |
| 4.0 | 1 | 16.0 | 37 | 38 | 27 |
| 4.0 | 1 | 18.0 | 43 | 43 | 34 |
| 4.0 | 1 | 20.0 | 46 | 47 | 38 |
| 4.0 | 1 | 22.0 | 52 | 53 | 43 |
| 8.0 | 1 | 2.0 | 1 | 0 | 0 |
| 8.0 | 1 | 4.0 | 5 | 5 | 0 |
| 8.0 | 1 | 6.0 | 11 | 12 | 0 |
| 8.0 | 1 | 8.0 | 17 | 17 | 5 |
| 8.0 | 1 | 10.0 | 20 | 20 | 12 |
| 8.0 | 1 | 12.0 | 27 | 27 | 17 |
| 8.0 | 1 | 14.0 | 34 | 34 | 20 |
| 8.0 | 1 | 16.0 | 37 | 38 | 27 |
| 8.0 | 1 | 18.0 | 43 | 43 | 27 |
| 8.0 | 1 | 20.0 | 46 | 46 | 34 |
| 8.0 | 1 | 22.0 | 52 | 53 | 38 |
| 6.0 | 2 | 2.0 | 1 | 0 | 0 |
| 6.0 | 2 | 4.0 | 5 | 5 | 0 |
| 6.0 | 2 | 6.0 | 11 | 12 | 5 |
| 6.0 | 2 | 8.0 | 17 | 17 | 12 |
| 6.0 | 2 | 10.0 | 20 | 20 | 17 |
| 6.0 | 2 | 12.0 | 27 | 27 | 17 |
| 6.0 | 2 | 14.0 | 34 | 34 | 20 |
| 6.0 | 2 | 16.0 | 37 | 38 | 27 |
| 6.0 | 2 | 18.0 | 43 | 43 | 34 |
| 6.0 | 2 | 20.0 | 46 | 46 | 38 |
| 6.0 | 2 | 22.0 | 52 | 53 | 43 |
| 4.0 | 2 | 2.0 | 1 | 0 | 0 |
| 4.0 | 2 | 4.0 | 5 | 5 | 0 |
| 4.0 | 2 | 6.0 | 11 | 12 | 5 |
| 4.0 | 2 | 8.0 | 17 | 17 | 12 |
| 4.0 | 2 | 10.0 | 20 | 20 | 17 |
| 4.0 | 2 | 12.0 | 27 | 27 | 20 |
| 4.0 | 2 | 14.0 | 34 | 34 | 27 |
| 4.0 | 2 | 16.0 | 37 | 38 | 34 |
| 4.0 | 2 | 18.0 | 43 | 43 | 38 |
| 4.0 | 2 | 20.0 | 46 | 47 | 43 |
| 4.0 | 2 | 22.0 | 52 | 53 | 47 |
| 8.0 | 2 | 2.0 | 1 | 0 | 0 |
| 8.0 | 2 | 4.0 | 5 | 5 | 0 |
| 8.0 | 2 | 6.0 | 11 | 12 | 5 |
| 8.0 | 2 | 8.0 | 17 | 17 | 12 |
| 8.0 | 2 | 10.0 | 20 | 20 | 17 |
| 8.0 | 2 | 12.0 | 27 | 27 | 20 |
| 8.0 | 2 | 14.0 | 34 | 34 | 27 |
| 8.0 | 2 | 16.0 | 37 | 38 | 27 |
| 8.0 | 2 | 18.0 | 43 | 43 | 38 |
| 8.0 | 2 | 20.0 | 46 | 46 | 43 |
| 8.0 | 2 | 22.0 | 52 | 53 | 46 |
| 4.0 | 3 | 2.0 | 1 | 0 | 0 |
| 4.0 | 3 | 4.0 | 5 | 5 | 0 |
| 4.0 | 3 | 6.0 | 11 | 12 | 5 |
| 4.0 | 3 | 8.0 | 17 | 17 | 12 |
| 4.0 | 3 | 10.0 | 20 | 20 | 17 |
| 4.0 | 3 | 12.0 | 27 | 27 | 20 |
| 4.0 | 3 | 14.0 | 34 | 34 | 27 |
| 4.0 | 3 | 16.0 | 37 | 38 | 34 |
| 4.0 | 3 | 18.0 | 43 | 43 | 38 |
| 4.0 | 3 | 20.0 | 46 | 47 | 43 |
| 4.0 | 3 | 22.0 | 52 | 53 | 47 |
| 8.0 | 3 | 2.0 | 1 | 0 | 0 |
| 8.0 | 3 | 4.0 | 5 | 5 | 0 |
| 8.0 | 3 | 6.0 | 11 | 12 | 5 |
| 8.0 | 3 | 8.0 | 17 | 17 | 12 |
| 8.0 | 3 | 10.0 | 20 | 20 | 17 |
| 8.0 | 3 | 12.0 | 27 | 27 | 20 |
| 8.0 | 3 | 14.0 | 34 | 34 | 27 |
| 8.0 | 3 | 16.0 | 37 | 38 | 34 |
| 8.0 | 3 | 18.0 | 43 | 43 | 38 |
| 8.0 | 3 | 20.0 | 46 | 46 | 43 |
| 8.0 | 3 | 22.0 | 52 | 53 | 46 |
| 6.0 | 3 | 2.0 | 1 | 0 | 0 |
| 6.0 | 3 | 4.0 | 5 | 5 | 0 |
| 6.0 | 3 | 6.0 | 11 | 12 | 5 |
| 6.0 | 3 | 8.0 | 17 | 17 | 12 |
| 6.0 | 3 | 10.0 | 20 | 20 | 17 |
| 6.0 | 3 | 12.0 | 27 | 27 | 20 |
| 6.0 | 3 | 14.0 | 34 | 34 | 27 |
| 6.0 | 3 | 16.0 | 37 | 38 | 34 |
| 6.0 | 3 | 18.0 | 43 | 43 | 38 |
| 6.0 | 3 | 20.0 | 46 | 46 | 43 |
| 6.0 | 3 | 22.0 | 52 | 53 | 46 |

## Lectura de los resultados

Medias de las tres rondas: error absoluto de hipótesis 0,45 / 0,36 / 0,36 palabras para 4 / 6 / 8 s; error visible simulado 5,45 / 6,91 / 6,73 palabras; demora final simulada 3,40 / 3,36 / 4,45 s. Todas alcanzan la palabra 56. Son once cortes durante una sola lectura, repetida tres veces, con nueve límites anotados como ambiguos. Las pequeñas diferencias de posición no permiten declarar una ventana óptima. La primera ronda tiene mayor coste en las tres configuraciones, sin causa monitorizada. 4 s mantiene menor coste medio; 6 s presenta una demora final media ligeramente menor. El desfase visible incluye el periodo de actualización y la cola de inferencia, no solo errores del reconocedor.
