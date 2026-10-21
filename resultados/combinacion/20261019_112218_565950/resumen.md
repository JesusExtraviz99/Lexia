# Comparación de cuatro seguidores

Comparación de cuatro seguidores sobre las mismas hipótesis guardadas. No hay nuevas inferencias ni nuevas grabaciones. Tiempos ASR/cola reutilizados, no mediciones nuevas de latencia total. Parámetros de ambas reglas sin cambios. Datos de desarrollo usados para diseñarlas; no demuestra generalización. Seguidor habitual sin activar variantes.

| Caso | Ventana | Ronda | Final original | Solo palabra | Solo temporal | Ambas | Cortes distintos original/ambas | Posiciones nuevas por interacción |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| normal | 6 | 1 | 56 | 56 | 56 | 56 | 0 | 0 |
| normal | 4 | 1 | 56 | 56 | 56 | 56 | 0 | 0 |
| normal | 8 | 1 | 56 | 56 | 56 | 56 | 0 | 0 |
| normal | 6 | 2 | 56 | 56 | 56 | 56 | 0 | 0 |
| normal | 4 | 2 | 56 | 56 | 56 | 56 | 0 | 0 |
| normal | 8 | 2 | 56 | 56 | 56 | 56 | 0 | 0 |
| normal | 4 | 3 | 56 | 56 | 56 | 56 | 0 | 0 |
| normal | 8 | 3 | 56 | 56 | 56 | 56 | 0 | 0 |
| normal | 6 | 3 | 56 | 56 | 56 | 56 | 0 | 0 |
| desviaciones | 8 | 1 | 56 | 56 | 56 | 56 | 0 | 0 |
| desviaciones | 6 | 1 | 56 | 56 | 56 | 56 | 0 | 0 |
| desviaciones | 4 | 1 | 56 | 56 | 56 | 56 | 0 | 0 |
| desviaciones | 4 | 2 | 56 | 56 | 56 | 56 | 0 | 0 |
| desviaciones | 6 | 2 | 56 | 56 | 56 | 56 | 0 | 0 |
| desviaciones | 8 | 2 | 56 | 56 | 56 | 56 | 0 | 0 |
| desviaciones | 8 | 3 | 56 | 56 | 56 | 56 | 0 | 0 |
| desviaciones | 4 | 3 | 56 | 56 | 56 | 56 | 0 | 0 |
| desviaciones | 6 | 3 | 56 | 56 | 56 | 56 | 0 | 0 |
| pausa | 8 | 1 | 56 | 56 | 56 | 56 | 0 | 0 |
| pausa | 4 | 1 | 56 | 56 | 56 | 56 | 0 | 0 |
| pausa | 8 | 2 | 56 | 56 | 56 | 56 | 0 | 0 |
| pausa | 4 | 2 | 56 | 56 | 56 | 56 | 0 | 0 |
| pausa | 4 | 3 | 56 | 56 | 56 | 56 | 0 | 0 |
| pausa | 8 | 3 | 56 | 56 | 56 | 56 | 0 | 0 |
| lenta | 8 | 1 | 55 | 55 | 56 | 56 | 6 | 0 |
| lenta | 4 | 1 | 53 | 53 | 53 | 53 | 2 | 0 |
| lenta | 8 | 2 | 55 | 55 | 56 | 56 | 6 | 0 |
| lenta | 4 | 2 | 53 | 53 | 53 | 53 | 2 | 0 |
| lenta | 4 | 3 | 53 | 53 | 53 | 53 | 2 | 0 |
| lenta | 8 | 3 | 55 | 55 | 56 | 56 | 6 | 0 |
| relectura | 8 | 1 | 56 | 56 | 56 | 56 | 0 | 0 |
| relectura | 4 | 1 | 56 | 56 | 56 | 56 | 0 | 0 |
| relectura | 8 | 2 | 56 | 56 | 56 | 56 | 0 | 0 |
| relectura | 4 | 2 | 56 | 56 | 56 | 56 | 0 | 0 |
| relectura | 4 | 3 | 56 | 56 | 56 | 56 | 0 | 0 |
| relectura | 8 | 3 | 56 | 56 | 56 | 56 | 0 | 0 |

## Cambios de posición con ambas reglas

lenta, ventana 8, ronda 1: palabra aislada []; retrocesos rechazados [80.0]; cambios [{'audio_seconds': 80.0, 'first': 55, 'second': 56}, {'audio_seconds': 82.0, 'first': 55, 'second': 56}, {'audio_seconds': 84.0, 'first': 55, 'second': 56}, {'audio_seconds': 86.0, 'first': 55, 'second': 56}, {'audio_seconds': 88.0, 'first': 55, 'second': 56}, {'audio_seconds': 90.0, 'first': 55, 'second': 56}]
lenta, ventana 4, ronda 1: palabra aislada [62.0]; retrocesos rechazados []; cambios [{'audio_seconds': 62.0, 'first': 45, 'second': 46}, {'audio_seconds': 64.0, 'first': 45, 'second': 46}]
lenta, ventana 8, ronda 2: palabra aislada []; retrocesos rechazados [80.0]; cambios [{'audio_seconds': 80.0, 'first': 55, 'second': 56}, {'audio_seconds': 82.0, 'first': 55, 'second': 56}, {'audio_seconds': 84.0, 'first': 55, 'second': 56}, {'audio_seconds': 86.0, 'first': 55, 'second': 56}, {'audio_seconds': 88.0, 'first': 55, 'second': 56}, {'audio_seconds': 90.0, 'first': 55, 'second': 56}]
lenta, ventana 4, ronda 2: palabra aislada [62.0]; retrocesos rechazados []; cambios [{'audio_seconds': 62.0, 'first': 45, 'second': 46}, {'audio_seconds': 64.0, 'first': 45, 'second': 46}]
lenta, ventana 4, ronda 3: palabra aislada [62.0]; retrocesos rechazados []; cambios [{'audio_seconds': 62.0, 'first': 45, 'second': 46}, {'audio_seconds': 64.0, 'first': 45, 'second': 46}]
lenta, ventana 8, ronda 3: palabra aislada []; retrocesos rechazados [80.0]; cambios [{'audio_seconds': 80.0, 'first': 55, 'second': 56}, {'audio_seconds': 82.0, 'first': 55, 'second': 56}, {'audio_seconds': 84.0, 'first': 55, 'second': 56}, {'audio_seconds': 86.0, 'first': 55, 'second': 56}, {'audio_seconds': 88.0, 'first': 55, 'second': 56}, {'audio_seconds': 90.0, 'first': 55, 'second': 56}]

No observar posiciones nuevas por interacción no demuestra independencia de las reglas ni ausencia universal de regresiones. Ver evaluaciones humanas por variante en resumen.json.

## Límite observado en una relectura sintética lejana

Caso sintético, no grabación adicional. La relectura apunta a 3. Al conservar 14, la búsqueda local empieza en 3 y solo contiene una de las tres palabras, insuficiente para aceptar el salto en esta actualización. El original en 13 todavía incluye sus y alas y acepta 3. No se prueba aquí la recuperación global posterior.

{'original': 3, 'palabra_aislada': 3, 'temporal': 14, 'combinada': 14}
