# Relectura contrastada con intentos humanos

Dos intentos completos y una palabra revisados por el lector, sin revisión independiente. No hay tiempos humanos de las seis palabras interiores: no se calcula error exacto de posición dentro de la frase ni demora de detección de su primer Los. Un retroceso pequeño no acredita seguir la frase completa desde su inicio. Se distingue el corte del audio del instante de salida lista según cola secuencial simulada, sin carga del modelo ni pantalla. Se reutilizan seis registros existentes, sin nuevas inferencias.

Primer intento: 17.54–19.84 s. Segundo: 20.36–22.77 s. Mirando: 22.91–23.29 s.

| Ventana | Ronda | Cortes durante segundo intento | Retrocesos de hipótesis en esos cortes | Salidas con retroceso listas durante el segundo intento (simulado) |
|---:|---:|---:|---:|---:|
| 8 | 1 | 1 | 0 | 0 |
| 4 | 1 | 1 | 1 | 0 |
| 8 | 2 | 1 | 0 | 0 |
| 4 | 2 | 1 | 1 | 0 |
| 4 | 3 | 1 | 1 | 0 |
| 8 | 3 | 1 | 0 | 0 |

## Cortes próximos a la relectura

| Ventana | Ronda | Audio (s) | Fase | Posición | Movimiento | Salida lista simulada (s) | Visible simulado en el corte | Texto ASR |
|---:|---:|---:|---|---:|---:|---:|---:|---|
| 8 | 1 | 18.0 | primer_intento | 38 | 4 | 19.73 | 34 | voló despacio y se posó sobre una flor Ana llamó su hermano para que pudiera verla Los dos |
| 8 | 1 | 20.0 | entre_intentos | 42 | 4 | 21.76 | 38 | sobre una flor Anna llamó a su hermano para que pudiera verla Los dos se quedaron en silencio |
| 8 | 1 | 22.0 | segundo_intento | 42 | 0 | 23.85 | 42 | Ana llamó a su hermano para que pudiera verla Los dos se quedaron en silencio Los dos se quedaron |
| 8 | 1 | 24.0 | mirando_terminada | 45 | 3 | 25.75 | 42 | pudiera verla Los dos se quedaron en silencio Los dos se quedaron en silencio mirando sus alas |
| 4 | 1 | 18.0 | primer_intento | 36 | 2 | 19.67 | 34 | Lana llamó a su hermano para que pudiera verla |
| 4 | 1 | 20.0 | entre_intentos | 42 | 6 | 21.69 | 36 | pudiera verla Los dos se quedaron en silencio |
| 4 | 1 | 22.0 | segundo_intento | 41 | -1 | 23.65 | 42 | los dos se quedaron en silencio los dos se quedaron en |
| 4 | 1 | 24.0 | mirando_terminada | 45 | 4 | 25.66 | 41 | Los dos se quedaron en silencio mirando sus alas |
| 8 | 2 | 18.0 | primer_intento | 38 | 4 | 19.93 | 34 | voló despacio y se posó sobre una flor Ana llamó su hermano para que pudiera verla Los dos |
| 8 | 2 | 20.0 | entre_intentos | 42 | 4 | 21.83 | 38 | sobre una flor Anna llamó a su hermano para que pudiera verla Los dos se quedaron en silencio |
| 8 | 2 | 22.0 | segundo_intento | 42 | 0 | 23.96 | 42 | Ana llamó a su hermano para que pudiera verla Los dos se quedaron en silencio Los dos se quedaron |
| 8 | 2 | 24.0 | mirando_terminada | 45 | 3 | 25.85 | 42 | pudiera verla Los dos se quedaron en silencio Los dos se quedaron en silencio mirando sus alas |
| 4 | 2 | 18.0 | primer_intento | 36 | 2 | 19.70 | 34 | Lana llamó a su hermano para que pudiera verla |
| 4 | 2 | 20.0 | entre_intentos | 42 | 6 | 21.69 | 36 | pudiera verla Los dos se quedaron en silencio |
| 4 | 2 | 22.0 | segundo_intento | 41 | -1 | 23.72 | 42 | los dos se quedaron en silencio los dos se quedaron en |
| 4 | 2 | 24.0 | mirando_terminada | 45 | 4 | 25.66 | 41 | Los dos se quedaron en silencio mirando sus alas |
| 4 | 3 | 18.0 | primer_intento | 36 | 2 | 19.69 | 34 | Lana llamó a su hermano para que pudiera verla |
| 4 | 3 | 20.0 | entre_intentos | 42 | 6 | 21.62 | 36 | pudiera verla Los dos se quedaron en silencio |
| 4 | 3 | 22.0 | segundo_intento | 41 | -1 | 23.67 | 42 | los dos se quedaron en silencio los dos se quedaron en |
| 4 | 3 | 24.0 | mirando_terminada | 45 | 4 | 25.61 | 41 | Los dos se quedaron en silencio mirando sus alas |
| 8 | 3 | 18.0 | primer_intento | 38 | 4 | 19.88 | 34 | voló despacio y se posó sobre una flor Ana llamó su hermano para que pudiera verla Los dos |
| 8 | 3 | 20.0 | entre_intentos | 42 | 4 | 21.81 | 38 | sobre una flor Anna llamó a su hermano para que pudiera verla Los dos se quedaron en silencio |
| 8 | 3 | 22.0 | segundo_intento | 42 | 0 | 23.90 | 42 | Ana llamó a su hermano para que pudiera verla Los dos se quedaron en silencio Los dos se quedaron |
| 8 | 3 | 24.0 | mirando_terminada | 45 | 3 | 25.81 | 42 | pudiera verla Los dos se quedaron en silencio Los dos se quedaron en silencio mirando sus alas |
