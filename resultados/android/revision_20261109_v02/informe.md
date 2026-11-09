# Lecturas Android · revisión técnica

Mesetas de posición no son por sí solas bloqueos de cómputo o errores lectores. Sin audio/anclas humanas no se miden demoras por palabra ni se atribuyen discrepancias a invenciones. SDK nativo y PC son configuraciones distintas; los tiempos de sus métricas no son directamente equivalentes.

| Modelo | Duración toma s | Callbacks | Final | Retrocesos | PSS máximo MiB | Latencia SDK línea completa mediana ms |
|---|---:|---:|---:|---:|---:|---:|
| Tiny | 58.23 | 105 | 56/56 | 0 | 246.2 | 180.0 |
| Small | 53.66 | 107 | 56/56 | 2 | 428.0 | 222.0 |

Dispositivo exportado: Xiaomi 23090RA98G, Android 16/API36 y unos 11,12 GiB de RAM física visible al sistema (variante comercial de 12 GB). PSS corresponde a toda la app durante la lectura; no se compara como si fuera RSS Windows. CPU acumulada puede superar el tiempo de pared al usar varios hilos. Batería/temperatura son observaciones cortas de app+sistema, no consumo neto del ASR.

Llegar al final no acredita un seguimiento continuo correcto. Se enumeran posiciones que permanecen estables mientras llegan callbacks. Si cambia el texto pero el alineador rechaza evidencia, no es una congelación total de la interfaz. Si no hay callbacks, no se puede distinguir pausa del lector, segmentación/VAD, cálculo u otras causas solo con estos JSON.

La política visual se conserva por sesión en revision.json: fixed_pairs en las parejas de 0.1 y sliding_next_words en 0.2. Esta última desplaza las dos palabras guía con cada avance reconocido. Lecturas diferentes no permiten atribuir diferencias de rendimiento solo a esa presentación.

Las salidas contienen repeticiones y diferencias respecto al cuento; algunas pueden corresponder a intentos de relectura del usuario para desbloquear el marcador. No se puntúan como errores ni se cambia la referencia sin escucha o confirmación específica.

## Tiny

Posiciones estables ≥1,5 s (excluidos inicio y final): 8. Actualizaciones con evidencia incompatible en la reproducción: 1.

### Posición 9 · 13.80–16.00 s · 2.19 s

3 callbacks, 2 textos distintos y 0 rechazos de evidencia.

- 13.80 s: una una mañana ana salió al al jardín de su casa · local · {'position': 9, 'reason': 'coincidencia_local', 'window_indices': [1, 32], 'exact_matches': 7, 'hypothesis_words': 8, 'edit_cost': 1}
- 13.80 s: una una mañana ana salió al al jardín de su casa · hipotesis_sin_cambios · {}
- 15.38 s: una una mañana ana salió al al jardín de su casa ser · local · {'position': 9, 'reason': 'coincidencia_local', 'window_indices': [1, 33], 'exact_matches': 6, 'hypothesis_words': 8, 'edit_cost': 2}

### Posición 2 · 4.32–6.45 s · 2.12 s

4 callbacks, 3 textos distintos y 0 rechazos de evidencia.

- 4.32 s: una una mañana · local · {'position': 2, 'reason': 'coincidencia_local', 'window_indices': [1, 24], 'exact_matches': 2, 'hypothesis_words': 3, 'edit_cost': 1}
- 4.81 s: una una mañana · hipotesis_sin_cambios · {}
- 5.87 s: una una mañana · hipotesis_sin_cambios · {}

### Posición 10 · 16.00–17.89 s · 1.89 s

3 callbacks, 2 textos distintos y 0 rechazos de evidencia.

- 16.00 s: una una mañana ana salió al al jardín de su casa cerca · local · {'position': 10, 'reason': 'coincidencia_local', 'window_indices': [1, 33], 'exact_matches': 7, 'hypothesis_words': 8, 'edit_cost': 1}
- 16.00 s: una una mañana ana salió al al jardín de su casa cerca · hipotesis_sin_cambios · {}
- 17.15 s: una una mañana ana salió al al jardín de su casa cerca · hipotesis_sin_cambios · {}

### Posición 4 · 8.10–9.87 s · 1.77 s

3 callbacks, 2 textos distintos y 0 rechazos de evidencia.

- 8.10 s: una una mañana ana salió · local · {'position': 4, 'reason': 'coincidencia_local', 'window_indices': [1, 27], 'exact_matches': 4, 'hypothesis_words': 5, 'edit_cost': 1}
- 8.10 s: una una mañana ana salió · hipotesis_sin_cambios · {}
- 9.19 s: una una mañana ana salió · hipotesis_sin_cambios · {}

### Posición 3 · 6.45–8.10 s · 1.66 s

3 callbacks, 2 textos distintos y 0 rechazos de evidencia.

- 6.45 s: una una mañana ana · local · {'position': 3, 'reason': 'coincidencia_local', 'window_indices': [1, 26], 'exact_matches': 3, 'hypothesis_words': 4, 'edit_cost': 1}
- 6.45 s: una una mañana ana · hipotesis_sin_cambios · {}
- 7.53 s: una una mañana ana · hipotesis_sin_cambios · {}

## Small

Posiciones estables ≥1,5 s (excluidos inicio y final): 7. Actualizaciones con evidencia incompatible en la reproducción: 17.

### Posición 27 · 26.27–28.09 s · 1.82 s

4 callbacks, 3 textos distintos y 1 rechazos de evidencia.

- 26.27 s: mariposa azul la mariposa voló despacio y ce posó sobre una flor · local · {'position': 27, 'reason': 'coincidencia_local', 'window_indices': [15, 50], 'exact_matches': 7, 'hypothesis_words': 8, 'edit_cost': 1}
- 26.74 s: mariposa azul la mariposa voló despacio y ce posó sobre una flor · hipotesis_sin_cambios · {}
- 27.47 s: mariposa voló despacio y ce posó sobre una flor a la gente · local · {'position': None, 'reason': 'evidencia_incompatible', 'window_indices': [16, 51], 'exact_matches': 4, 'hypothesis_words': 8, 'edit_cost': 4}

### Posición 2 · 4.74–6.54 s · 1.80 s

3 callbacks, 2 textos distintos y 1 rechazos de evidencia.

- 4.74 s: una mañana · local · {'position': 2, 'reason': 'coincidencia_local', 'window_indices': [1, 24], 'exact_matches': 2, 'hypothesis_words': 2, 'edit_cost': 0}
- 5.33 s: una mañana · hipotesis_sin_cambios · {}
- 5.92 s: una mañana y aquí · local · {'position': None, 'reason': 'evidencia_incompatible', 'window_indices': [1, 26], 'exact_matches': 2, 'hypothesis_words': 4, 'edit_cost': 2}

### Posición 40 · 37.51–39.28 s · 1.77 s

4 callbacks, 3 textos distintos y 2 rechazos de evidencia.

- 37.51 s: llamó a su hermano para que pudiera verla los dos se quedaron · local · {'position': 40, 'reason': 'coincidencia_local', 'window_indices': [28, 56], 'exact_matches': 8, 'hypothesis_words': 8, 'edit_cost': 0}
- 38.20 s: que pudiera verla los dos se quedaron y lo que es la · local · {'position': None, 'reason': 'evidencia_incompatible', 'window_indices': [29, 56], 'exact_matches': 3, 'hypothesis_words': 8, 'edit_cost': 5}
- 38.78 s: pudiera verla los dos se quedaron en el centro de la zona · local · {'position': None, 'reason': 'evidencia_incompatible', 'window_indices': [29, 56], 'exact_matches': 3, 'hypothesis_words': 8, 'edit_cost': 5}

### Posición 38 · 35.26–36.95 s · 1.69 s

3 callbacks, 2 textos distintos y 0 rechazos de evidencia.

- 35.26 s: flor ana llamó a su hermano para que pudiera verla los dos · local · {'position': 38, 'reason': 'coincidencia_local', 'window_indices': [26, 56], 'exact_matches': 8, 'hypothesis_words': 8, 'edit_cost': 0}
- 35.80 s: flor ana llamó a su hermano para que pudiera verla los dos · hipotesis_sin_cambios · {}
- 36.52 s: a su hermano para que pudiera verla los dos setenta y cinco · local · {'position': 38, 'reason': 'coincidencia_local', 'window_indices': [27, 56], 'exact_matches': 5, 'hypothesis_words': 8, 'edit_cost': 3}

### Posición 42 · 39.28–40.91 s · 1.63 s

3 callbacks, 2 textos distintos y 1 rechazos de evidencia.

- 39.28 s: su hermano para que pudiera verla los dos se quedaron en silencio · local · {'position': 42, 'reason': 'coincidencia_local', 'window_indices': [29, 56], 'exact_matches': 8, 'hypothesis_words': 8, 'edit_cost': 0}
- 39.81 s: su hermano para que pudiera verla los dos se quedaron en silencio · hipotesis_sin_cambios · {}
- 40.52 s: pudiera verla los dos se quedaron en silencio lo que yo quiero · local · {'position': None, 'reason': 'evidencia_incompatible', 'window_indices': [31, 56], 'exact_matches': 4, 'hypothesis_words': 8, 'edit_cost': 4}

