# Lectura lenta frente a cuatro anclas humanas

Cuatro anclas manuales revisadas por el lector, cobertura parcial y sin revisión independiente. Referencia = última palabra terminada. Entre anclas se indica un rango posible, sin interpolar tiempos. Cuando las cotas coinciden se conoce una posición exacta; tras cuaderno es 56. Una hipótesis dentro de un rango amplio no demuestra posición correcta. Un adelanto respecto al final anotado puede corresponder a una palabra todavía en curso. No se calcula un error medio para todo el audio. La posición visible usa la última salida ya lista según cola secuencial simulada, sin carga del modelo ni latencia de pantalla. Se reutilizan seis registros existentes, sin nuevas inferencias ni cambios del seguidor.

| Ventana | Ronda | Primer corte con 56 tras terminar (s) | Demora final simulada (s) | Posición final | Posiciones tras el fin humano |
|---:|---:|---:|---:|---:|---|
| 8 | 1 | 78.0 | 18.73 | 55 | [56, 55, 55, 55, 55, 55, 55] |
| 4 | 1 | No alcanzada | — | 53 | [53, 53, 53, 53, 53, 53, 53] |
| 8 | 2 | 78.0 | 15.07 | 55 | [56, 55, 55, 55, 55, 55, 55] |
| 4 | 2 | No alcanzada | — | 53 | [53, 53, 53, 53, 53, 53, 53] |
| 4 | 3 | No alcanzada | — | 53 | [53, 53, 53, 53, 53, 53, 53] |
| 8 | 3 | 78.0 | 9.05 | 55 | [56, 55, 55, 55, 55, 55, 55] |

## Cortes desde el final de Después

| Ventana | Ronda | Audio (s) | Referencia posible | Hipótesis | Retraso mínimo (palabras) | Visible simulado | Texto ASR |
|---:|---:|---:|---|---:|---:|---:|---|
| 8 | 1 | 62.0 | 46–52 | 46 | 0 | 29 | mirando sus alas Después |
| 8 | 1 | 64.0 | 46–52 | 47 | 0 | 31 | sus alas Después volvieron |
| 8 | 1 | 66.0 | 46–52 | 49 | 0 | 34 | después volvieron a casa |
| 8 | 1 | 68.0 | 46–52 | 50 | 0 | 34 | Pues volvieron a casa y digo |
| 8 | 1 | 70.0 | 46–52 | 52 | 0 | 36 | volvieron a casa y dibujaron la |
| 8 | 1 | 72.0 | 46–52 | 53 | 0 | 38 | a casa y dibujaron la mariposa |
| 8 | 1 | 74.0 | 53–54 | 54 | 0 | 40 | y dibujaron la mariposa en |
| 8 | 1 | 76.0 | 55–55 | 55 | 0 | 42 | Lujaron la mariposa en un cuar |
| 8 | 1 | 78.0 | 56–56 | 56 | 0 | 42 | mariposa en un cuaderno |
| 8 | 1 | 80.0 | 56–56 | 55 | 1 | 44 | en un jugaderno |
| 8 | 1 | 82.0 | 56–56 | 55 | 1 | 45 | Un jugaderno |
| 8 | 1 | 84.0 | 56–56 | 55 | 1 | 46 | Aderno |
| 8 | 1 | 86.0 | 56–56 | 55 | 1 | 49 |  |
| 8 | 1 | 88.0 | 56–56 | 55 | 1 | 50 |  |
| 8 | 1 | 90.0 | 56–56 | 55 | 1 | 52 |  |
| 4 | 1 | 62.0 | 46–52 | 45 | 1 | 45 | Después |
| 4 | 1 | 64.0 | 46–52 | 45 | 1 | 45 | Pues volvieron |
| 4 | 1 | 66.0 | 46–52 | 49 | 0 | 45 | volvieron a casa |
| 4 | 1 | 68.0 | 46–52 | 50 | 0 | 45 | casa y divu |
| 4 | 1 | 70.0 | 46–52 | 52 | 0 | 49 | y dibujaron la |
| 4 | 1 | 72.0 | 46–52 | 53 | 0 | 50 | Lujaron la mariposa |
| 4 | 1 | 74.0 | 53–54 | 53 | 0 | 53 | Madibosa En |
| 4 | 1 | 76.0 | 55–55 | 53 | 2 | 53 | y nos vemos en el próximo vídeo hasta la próxima |
| 4 | 1 | 78.0 | 56–56 | 53 | 3 | 53 | Un jugaderno |
| 4 | 1 | 80.0 | 56–56 | 53 | 3 | 53 | Aderno |
| 4 | 1 | 82.0 | 56–56 | 53 | 3 | 53 |  |
| 4 | 1 | 84.0 | 56–56 | 53 | 3 | 53 |  |
| 4 | 1 | 86.0 | 56–56 | 53 | 3 | 53 |  |
| 4 | 1 | 88.0 | 56–56 | 53 | 3 | 53 |  |
| 4 | 1 | 90.0 | 56–56 | 53 | 3 | 53 |  |
| 8 | 2 | 62.0 | 46–52 | 46 | 0 | 31 | mirando sus alas Después |
| 8 | 2 | 64.0 | 46–52 | 47 | 0 | 34 | sus alas Después volvieron |
| 8 | 2 | 66.0 | 46–52 | 49 | 0 | 34 | después volvieron a casa |
| 8 | 2 | 68.0 | 46–52 | 50 | 0 | 36 | Pues volvieron a casa y digo |
| 8 | 2 | 70.0 | 46–52 | 52 | 0 | 38 | volvieron a casa y dibujaron la |
| 8 | 2 | 72.0 | 46–52 | 53 | 0 | 40 | a casa y dibujaron la mariposa |
| 8 | 2 | 74.0 | 53–54 | 54 | 0 | 42 | y dibujaron la mariposa en |
| 8 | 2 | 76.0 | 55–55 | 55 | 0 | 42 | Lujaron la mariposa en un cuar |
| 8 | 2 | 78.0 | 56–56 | 56 | 0 | 45 | mariposa en un cuaderno |
| 8 | 2 | 80.0 | 56–56 | 55 | 1 | 46 | en un jugaderno |
| 8 | 2 | 82.0 | 56–56 | 55 | 1 | 47 | Un jugaderno |
| 8 | 2 | 84.0 | 56–56 | 55 | 1 | 49 | Aderno |
| 8 | 2 | 86.0 | 56–56 | 55 | 1 | 52 |  |
| 8 | 2 | 88.0 | 56–56 | 55 | 1 | 53 |  |
| 8 | 2 | 90.0 | 56–56 | 55 | 1 | 54 |  |
| 4 | 2 | 62.0 | 46–52 | 45 | 1 | 45 | Después |
| 4 | 2 | 64.0 | 46–52 | 45 | 1 | 45 | Pues volvieron |
| 4 | 2 | 66.0 | 46–52 | 49 | 0 | 45 | volvieron a casa |
| 4 | 2 | 68.0 | 46–52 | 50 | 0 | 45 | casa y divu |
| 4 | 2 | 70.0 | 46–52 | 52 | 0 | 49 | y dibujaron la |
| 4 | 2 | 72.0 | 46–52 | 53 | 0 | 52 | Lujaron la mariposa |
| 4 | 2 | 74.0 | 53–54 | 53 | 0 | 53 | Madibosa En |
| 4 | 2 | 76.0 | 55–55 | 53 | 2 | 53 | y nos vemos en el próximo vídeo hasta la próxima |
| 4 | 2 | 78.0 | 56–56 | 53 | 3 | 53 | Un jugaderno |
| 4 | 2 | 80.0 | 56–56 | 53 | 3 | 53 | Aderno |
| 4 | 2 | 82.0 | 56–56 | 53 | 3 | 53 |  |
| 4 | 2 | 84.0 | 56–56 | 53 | 3 | 53 |  |
| 4 | 2 | 86.0 | 56–56 | 53 | 3 | 53 |  |
| 4 | 2 | 88.0 | 56–56 | 53 | 3 | 53 |  |
| 4 | 2 | 90.0 | 56–56 | 53 | 3 | 53 |  |
| 4 | 3 | 62.0 | 46–52 | 45 | 1 | 45 | Después |
| 4 | 3 | 64.0 | 46–52 | 45 | 1 | 45 | Pues volvieron |
| 4 | 3 | 66.0 | 46–52 | 49 | 0 | 45 | volvieron a casa |
| 4 | 3 | 68.0 | 46–52 | 50 | 0 | 45 | casa y divu |
| 4 | 3 | 70.0 | 46–52 | 52 | 0 | 49 | y dibujaron la |
| 4 | 3 | 72.0 | 46–52 | 53 | 0 | 52 | Lujaron la mariposa |
| 4 | 3 | 74.0 | 53–54 | 53 | 0 | 53 | Madibosa En |
| 4 | 3 | 76.0 | 55–55 | 53 | 2 | 53 | y nos vemos en el próximo vídeo hasta la próxima |
| 4 | 3 | 78.0 | 56–56 | 53 | 3 | 53 | Un jugaderno |
| 4 | 3 | 80.0 | 56–56 | 53 | 3 | 53 | Aderno |
| 4 | 3 | 82.0 | 56–56 | 53 | 3 | 53 |  |
| 4 | 3 | 84.0 | 56–56 | 53 | 3 | 53 |  |
| 4 | 3 | 86.0 | 56–56 | 53 | 3 | 53 |  |
| 4 | 3 | 88.0 | 56–56 | 53 | 3 | 53 |  |
| 4 | 3 | 90.0 | 56–56 | 53 | 3 | 53 |  |
| 8 | 3 | 62.0 | 46–52 | 46 | 0 | 35 | mirando sus alas Después |
| 8 | 3 | 64.0 | 46–52 | 47 | 0 | 38 | sus alas Después volvieron |
| 8 | 3 | 66.0 | 46–52 | 49 | 0 | 40 | después volvieron a casa |
| 8 | 3 | 68.0 | 46–52 | 50 | 0 | 42 | Pues volvieron a casa y digo |
| 8 | 3 | 70.0 | 46–52 | 52 | 0 | 42 | volvieron a casa y dibujaron la |
| 8 | 3 | 72.0 | 46–52 | 53 | 0 | 45 | a casa y dibujaron la mariposa |
| 8 | 3 | 74.0 | 53–54 | 54 | 0 | 46 | y dibujaron la mariposa en |
| 8 | 3 | 76.0 | 55–55 | 55 | 0 | 47 | Lujaron la mariposa en un cuar |
| 8 | 3 | 78.0 | 56–56 | 56 | 0 | 49 | mariposa en un cuaderno |
| 8 | 3 | 80.0 | 56–56 | 55 | 1 | 52 | en un jugaderno |
| 8 | 3 | 82.0 | 56–56 | 55 | 1 | 53 | Un jugaderno |
| 8 | 3 | 84.0 | 56–56 | 55 | 1 | 54 | Aderno |
| 8 | 3 | 86.0 | 56–56 | 55 | 1 | 55 |  |
| 8 | 3 | 88.0 | 56–56 | 55 | 1 | 56 |  |
| 8 | 3 | 90.0 | 56–56 | 55 | 1 | 55 |  |

<!-- identidad-audio-inicio -->
## Audio utilizado

- **Lectura lenta · cuento 1 · 16/10/2026** — Lectura lenta - cuento 1 - 16-10-2026.wav
<!-- identidad-audio-fin -->
