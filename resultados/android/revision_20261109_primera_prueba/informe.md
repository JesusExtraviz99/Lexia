# Primeras lecturas Android · revisión técnica

Mesetas de posición no son por sí solas bloqueos de cómputo o errores lectores. Sin audio/anclas humanas no se miden demoras por palabra ni se atribuyen discrepancias a invenciones. SDK nativo y PC son configuraciones distintas; los tiempos de sus métricas no son directamente equivalentes.

| Modelo | Duración toma s | Callbacks | Final | Retrocesos | PSS máximo MiB | Latencia SDK línea completa mediana ms |
|---|---:|---:|---:|---:|---:|---:|
| Tiny | 69.24 | 116 | 56/56 | 0 | 238.5 | 115.5 |
| Small | 91.94 | 136 | 56/56 | 1 | 433.1 | 224.0 |

Dispositivo exportado: Xiaomi 23090RA98G, Android 16/API36 y unos 11,12 GiB de RAM física visible al sistema (variante comercial de 12 GB). PSS corresponde a toda la app durante la lectura; no se compara como si fuera RSS Windows. CPU acumulada puede superar el tiempo de pared al usar varios hilos. Batería/temperatura son observaciones cortas de app+sistema, no consumo neto del ASR.

Ambos llegan a 56; eso no acredita un seguimiento continuo correcto. Se enumeran posiciones que permanecen estables mientras llegan callbacks. Si cambia el texto pero el alineador rechaza evidencia, no es una congelación total de la interfaz. Si no hay callbacks, no se puede distinguir pausa del lector, segmentación/VAD, cálculo u otras causas solo con estos JSON.

La guía 0.1 esperaba completar cada pareja fija: añade una espera visual aun cuando la primera palabra ya está reconocida. La siguiente versión cambia solo esa presentación a dos palabras consecutivas que se desplazan una posición con cada avance, conservando ASR y umbrales del alineador. No se afirma que esto arregle todos los atascos. Se añaden diagnósticos de coincidencias/recuperación para la próxima prueba.

Las salidas contienen repeticiones y diferencias respecto al cuento; algunas pueden corresponder a intentos de relectura del usuario para desbloquear el marcador. No se puntúan como errores ni se cambia la referencia sin escucha o confirmación específica.

## Tiny

Posiciones estables ≥1,5 s (excluidos inicio y final): 15. Actualizaciones con evidencia incompatible en la reproducción: 10.

### Posición 19 · 23.65–34.79 s · 11.14 s

13 callbacks, 9 textos distintos y 5 rechazos de evidencia.

- 23.65 s: cerca de un árbol encontró una mariposa azul azul la la mariposa · local · {'position': 19, 'reason': 'coincidencia_local', 'window_indices': [7, 42], 'exact_matches': 6, 'hypothesis_words': 8, 'edit_cost': 2}
- 31.39 s: encontró una mariposa azul azul la la mariposa polo volo volo despacio · hipotesis_sin_cambios · {}
- 34.17 s: una mariposa azul azul la la mariposa polo volo volo despacio y · local · {'position': None, 'reason': 'evidencia_incompatible', 'window_indices': [8, 43], 'exact_matches': 4, 'hypothesis_words': 8, 'edit_cost': 4}

### Posición 46 · 55.00–62.97 s · 7.97 s

12 callbacks, 8 textos distintos y 5 rechazos de evidencia.

- 55.00 s: los dos se quedaron en silencio mirando sus a las después después · local · {'position': 46, 'reason': 'coincidencia_local', 'window_indices': [33, 56], 'exact_matches': 5, 'hypothesis_words': 8, 'edit_cost': 3}
- 61.85 s: silencio mirando sus a las después después después volvieron a a casa · local · {'position': None, 'reason': 'evidencia_incompatible', 'window_indices': [35, 56], 'exact_matches': 4, 'hypothesis_words': 8, 'edit_cost': 4}
- 61.85 s: silencio mirando sus a las después después después volvieron a a casa · hipotesis_sin_cambios · {}

### Posición 44 · 52.19–55.00 s · 2.82 s

6 callbacks, 4 textos distintos y 0 rechazos de evidencia.

- 52.19 s: para que pudiera verla los dos se quedaron en silencio mirando sus · local · {'position': 44, 'reason': 'coincidencia_local', 'window_indices': [32, 56], 'exact_matches': 8, 'hypothesis_words': 8, 'edit_cost': 0}
- 53.77 s: pudiera verla los dos se quedaron en silencio mirando sus a las · hipotesis_sin_cambios · {}
- 54.38 s: pudiera verla los dos se quedaron en silencio mirando sus a las · hipotesis_sin_cambios · {}

### Posición 36 · 44.25–46.11 s · 1.86 s

3 callbacks, 2 textos distintos y 0 rechazos de evidencia.

- 44.25 s: sobre una flor ana llamó a su hermano para que pudiera verla · local · {'position': 36, 'reason': 'coincidencia_local', 'window_indices': [24, 56], 'exact_matches': 8, 'hypothesis_words': 8, 'edit_cost': 0}
- 44.83 s: sobre una flor ana llamó a su hermano para que pudiera verla · hipotesis_sin_cambios · {}
- 45.45 s: sobre una flor ana llamó a su hermano para que pudiera verla · hipotesis_sin_cambios · {}

### Posición 8 · 8.99–10.81 s · 1.83 s

3 callbacks, 2 textos distintos y 0 rechazos de evidencia.

- 8.99 s: una mañana ana salió al jardín de su · local · {'position': 8, 'reason': 'coincidencia_local', 'window_indices': [1, 30], 'exact_matches': 8, 'hypothesis_words': 8, 'edit_cost': 0}
- 9.57 s: una mañana ana salió al jardín de su · hipotesis_sin_cambios · {}
- 10.16 s: una mañana ana salió al jardín de su · hipotesis_sin_cambios · {}

## Small

Posiciones estables ≥1,5 s (excluidos inicio y final): 29. Actualizaciones con evidencia incompatible en la reproducción: 36.

### Posición 53 · 73.88–89.83 s · 15.96 s

17 callbacks, 12 textos distintos y 11 rechazos de evidencia.

- 73.88 s: silencio mirando sus alas después volvieron a casa y dibujaron la mariposa · local · {'position': 53, 'reason': 'coincidencia_local', 'window_indices': [41, 56], 'exact_matches': 8, 'hypothesis_words': 8, 'edit_cost': 0}
- 88.69 s: en el sector de la pesca en un cuaderno dibujaron la marina · local · {'position': None, 'reason': 'evidencia_incompatible', 'window_indices': [42, 56], 'exact_matches': 4, 'hypothesis_words': 8, 'edit_cost': 4}
- 89.26 s: en el sector de la pesca en un cuaderno dibujaron la mariposa · local · {'position': None, 'reason': 'evidencia_incompatible', 'window_indices': [42, 56], 'exact_matches': 4, 'hypothesis_words': 8, 'edit_cost': 4}

### Posición 33 · 42.31–46.52 s · 4.21 s

3 callbacks, 2 textos distintos y 1 rechazos de evidencia.

- 42.31 s: se posó sobre una flor ana llamó a su hermano para qué · local · {'position': 33, 'reason': 'coincidencia_local', 'window_indices': [21, 56], 'exact_matches': 7, 'hypothesis_words': 8, 'edit_cost': 1}
- 42.31 s: se posó sobre una flor ana llamó a su hermano para qué · hipotesis_sin_cambios · {}
- 46.18 s: ana llamó a su hermano para qué para que se den cuenta · local · {'position': None, 'reason': 'evidencia_incompatible', 'window_indices': [22, 56], 'exact_matches': 3, 'hypothesis_words': 8, 'edit_cost': 5}

### Posición 34 · 46.52–48.98 s · 2.46 s

3 callbacks, 2 textos distintos y 1 rechazos de evidencia.

- 46.52 s: sobre una flor ana llamó a su hermano para qué para que · local · {'position': 34, 'reason': 'coincidencia_local', 'window_indices': [22, 56], 'exact_matches': 6, 'hypothesis_words': 8, 'edit_cost': 2}
- 47.20 s: sobre una flor ana llamó a su hermano para qué para que · hipotesis_sin_cambios · {}
- 48.34 s: flor ana llamó a su hermano para qué para que por ejemplo · local · {'position': None, 'reason': 'evidencia_incompatible', 'window_indices': [23, 56], 'exact_matches': 4, 'hypothesis_words': 8, 'edit_cost': 4}

### Posición 28 · 35.70–38.09 s · 2.39 s

4 callbacks, 3 textos distintos y 1 rechazos de evidencia.

- 35.70 s: azul la mariposa voló despacio y se posó sobre una flor ana · local · {'position': 28, 'reason': 'coincidencia_local', 'window_indices': [16, 51], 'exact_matches': 8, 'hypothesis_words': 8, 'edit_cost': 0}
- 37.02 s: y se posó sobre una flor ana y por último el problema · local · {'position': None, 'reason': 'evidencia_incompatible', 'window_indices': [17, 52], 'exact_matches': 3, 'hypothesis_words': 8, 'edit_cost': 5}
- 37.46 s: la mariposa voló despacio y se posó sobre una flor ana llamo · local · {'position': 28, 'reason': 'coincidencia_local', 'window_indices': [17, 52], 'exact_matches': 7, 'hypothesis_words': 8, 'edit_cost': 1}

### Posición 40 · 53.79–56.16 s · 2.37 s

3 callbacks, 2 textos distintos y 1 rechazos de evidencia.

- 53.79 s: su hermano para qué para que pudiera verla los dos se quedaron · local · {'position': 40, 'reason': 'coincidencia_local', 'window_indices': [27, 56], 'exact_matches': 8, 'hypothesis_words': 8, 'edit_cost': 0}
- 54.33 s: su hermano para qué para que pudiera verla los dos se quedaron · hipotesis_sin_cambios · {}
- 55.47 s: para que pudiera verla los dos se quedaron y lo que se · local · {'position': None, 'reason': 'evidencia_incompatible', 'window_indices': [29, 56], 'exact_matches': 4, 'hypothesis_words': 8, 'edit_cost': 4}

