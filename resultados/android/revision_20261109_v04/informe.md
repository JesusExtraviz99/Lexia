# Lecturas Android · revisión técnica

Mesetas de posición no son por sí solas bloqueos de cómputo o errores lectores. Sin audio/anclas humanas no se miden demoras por palabra ni se atribuyen discrepancias a invenciones. SDK nativo y PC son configuraciones distintas; los tiempos de sus métricas no son directamente equivalentes.

| Modelo | Duración toma s | Callbacks | Final | Retrocesos | PSS máximo MiB | Latencia SDK línea completa mediana ms |
|---|---:|---:|---:|---:|---:|---:|
| Tiny | 45.48 | 112 | 56/56 | 0 | 243.1 | 148.0 |
| Tiny | 45.18 | 112 | 56/56 | 1 | 233.9 | 127.0 |
| Small | 55.05 | 165 | 56/56 | 1 | 436.9 | 173.0 |
| Small | 55.43 | 138 | 56/56 | 0 | 450.1 | 197.0 |

Dispositivo exportado: Xiaomi 23090RA98G, Android 16/API36 y unos 11,12 GiB de RAM física visible al sistema (variante comercial de 12 GB). PSS corresponde a toda la app durante la lectura; no se compara como si fuera RSS Windows. CPU acumulada puede superar el tiempo de pared al usar varios hilos. Batería/temperatura son observaciones cortas de app+sistema, no consumo neto del ASR.

Llegar al final no acredita un seguimiento continuo correcto. Se enumeran posiciones que permanecen estables mientras llegan callbacks. Si cambia el texto pero el alineador rechaza evidencia, no es una congelación total de la interfaz. Si no hay callbacks, no se puede distinguir pausa del lector, segmentación/VAD, cálculo u otras causas solo con estos JSON.

La política visual se conserva por sesión en revision.json: fixed_pairs en las parejas de 0.1 y sliding_next_words en 0.2. Esta última desplaza las dos palabras guía con cada avance reconocido. Lecturas diferentes no permiten atribuir diferencias de rendimiento solo a esa presentación.

Las salidas contienen repeticiones y diferencias respecto al cuento; algunas pueden corresponder a intentos de relectura del usuario para desbloquear el marcador. No se puntúan como errores ni se cambia la referencia sin escucha o confirmación específica.

## Tiny

Posiciones estables ≥1,5 s (excluidos inicio y final): 3. Actualizaciones con evidencia incompatible en la reproducción: 3.

### Posición 19 · 15.85–18.48 s · 2.63 s

3 callbacks, 3 textos distintos y 1 rechazos de evidencia.

- 15.85 s: su casa cerca de un árbol encontró una mariposa azul la mariposa · local · {'reason': 'coincidencia_local', 'exact_matches': 8, 'edit_cost': 0, 'hypothesis_words': 8}
- 16.95 s: un árbol encontró una mariposa azul la mariposa bobosa bobosa bobosa bo · local · {'reason': 'evidencia_incompatible', 'exact_matches': 4, 'edit_cost': 4, 'hypothesis_words': 8}
- 18.15 s: cerca de un árbol encontró una mariposa azul la mariposa voló despojo · avance_rechazado · {'reason': 'sin_apoyo_final', 'exact_matches': 7, 'edit_cost': 1, 'hypothesis_words': 8}

### Posición 42 · 32.60–34.34 s · 1.74 s

5 callbacks, 4 textos distintos y 0 rechazos de evidencia.

- 32.60 s: su hermano para que pudiera verla los dos se quedaron en silencio · local · {'reason': 'coincidencia_local', 'exact_matches': 8, 'edit_cost': 0, 'hypothesis_words': 8}
- 34.01 s: hermano para que pudiera verla los dos se quedaron en silencio mirad · local · {'reason': 'coincidencia_local', 'exact_matches': 7, 'edit_cost': 1, 'hypothesis_words': 8}
- 34.17 s: hermano para que pudiera verla los dos se quedaron en silencio miran · local · {'reason': 'coincidencia_local', 'exact_matches': 7, 'edit_cost': 1, 'hypothesis_words': 8}

### Posición 38 · 30.34–32.06 s · 1.72 s

5 callbacks, 5 textos distintos y 0 rechazos de evidencia.

- 30.34 s: flor ana llamó a su hermano para que pudiera verla los dos · local · {'reason': 'coincidencia_local', 'exact_matches': 8, 'edit_cost': 0, 'hypothesis_words': 8}
- 31.25 s: a su hermano para que pudiera verla los dos c que dar · local · {'reason': 'coincidencia_local', 'exact_matches': 5, 'edit_cost': 3, 'hypothesis_words': 8}
- 31.79 s: llamó a su hermano para que pudiera verla los dos c quedaron · avance_rechazado · {'reason': 'sin_apoyo_final', 'exact_matches': 7, 'edit_cost': 1, 'hypothesis_words': 8}

## Tiny

Posiciones estables ≥1,5 s (excluidos inicio y final): 4. Actualizaciones con evidencia incompatible en la reproducción: 0.

### Posición 42 · 30.21–32.21 s · 2.00 s

3 callbacks, 2 textos distintos y 0 rechazos de evidencia.

- 30.21 s: su hermano para que pudiera verla los dos ce quedaron en silencio · local · {'reason': 'coincidencia_local', 'exact_matches': 7, 'edit_cost': 1, 'hypothesis_words': 8}
- 30.52 s: su hermano para que pudiera verla los dos ce quedaron en silencio · hipotesis_sin_cambios · {'reason': 'texto_identico', 'exact_matches': 0, 'edit_cost': 0, 'hypothesis_words': 8}
- 31.63 s: su hermano para que pudiera verla los dos ce quedaron en silencio · hipotesis_sin_cambios · {'reason': 'texto_identico', 'exact_matches': 0, 'edit_cost': 0, 'hypothesis_words': 8}

### Posición 12 · 9.02–10.80 s · 1.78 s

3 callbacks, 3 textos distintos y 0 rechazos de evidencia.

- 9.02 s: una mañana ana salió al jardín de su casa cerca de un · local · {'reason': 'coincidencia_local', 'exact_matches': 8, 'edit_cost': 0, 'hypothesis_words': 8}
- 9.75 s: mañana ana salió al jardín de su casa cerca de un arbo · local · {'reason': 'coincidencia_local', 'exact_matches': 7, 'edit_cost': 1, 'hypothesis_words': 8}
- 10.09 s: ana salió al jardín de su casa cerca de un árbol en · avance_rechazado · {'reason': 'sin_apoyo_final', 'exact_matches': 7, 'edit_cost': 1, 'hypothesis_words': 8}

### Posición 38 · 28.62–30.21 s · 1.59 s

6 callbacks, 5 textos distintos y 0 rechazos de evidencia.

- 28.62 s: ana llamó a su hermano para que pudiera verla los dos ce · local · {'reason': 'coincidencia_local', 'exact_matches': 7, 'edit_cost': 1, 'hypothesis_words': 8}
- 29.58 s: llamó a su hermano para que pudiera verla los dos ce quedaron · avance_rechazado · {'reason': 'sin_apoyo_final', 'exact_matches': 7, 'edit_cost': 1, 'hypothesis_words': 8}
- 29.89 s: su hermano para que pudiera verla los dos ce quedaron en sí · avance_rechazado · {'reason': 'sin_apoyo_final', 'exact_matches': 6, 'edit_cost': 2, 'hypothesis_words': 8}

### Posición 43 · 32.21–33.77 s · 1.56 s

3 callbacks, 2 textos distintos y 0 rechazos de evidencia.

- 32.21 s: hermano para que pudiera verla los dos ce quedaron en silencio mirando · local · {'reason': 'coincidencia_local', 'exact_matches': 7, 'edit_cost': 1, 'hypothesis_words': 8}
- 32.54 s: hermano para que pudiera verla los dos ce quedaron en silencio mirando · hipotesis_sin_cambios · {'reason': 'texto_identico', 'exact_matches': 0, 'edit_cost': 0, 'hypothesis_words': 8}
- 33.09 s: hermano para que pudiera verla los dos ce quedaron en silencio mirando · hipotesis_sin_cambios · {'reason': 'texto_identico', 'exact_matches': 0, 'edit_cost': 0, 'hypothesis_words': 8}

## Small

Posiciones estables ≥1,5 s (excluidos inicio y final): 5. Actualizaciones con evidencia incompatible en la reproducción: 35.

### Posición 38 · 32.77–41.42 s · 8.66 s

18 callbacks, 14 textos distintos y 7 rechazos de evidencia.

- 32.77 s: flor ana llamó a su hermano para que pudiera verla los dos · local · {'reason': 'coincidencia_local', 'exact_matches': 8, 'edit_cost': 0, 'hypothesis_words': 8}
- 40.95 s: pudiera verla los dos ce quedaron ce quedaron y lo que se · local · {'reason': 'evidencia_incompatible', 'exact_matches': 2, 'edit_cost': 6, 'hypothesis_words': 8}
- 41.27 s: verla los dos ce quedaron ce quedaron en el mundo de la · local · {'reason': 'evidencia_incompatible', 'exact_matches': 2, 'edit_cost': 6, 'hypothesis_words': 8}

### Posición 27 · 23.27–25.07 s · 1.80 s

4 callbacks, 3 textos distintos y 1 rechazos de evidencia.

- 23.27 s: mariposa azul la mariposa voló despacio y se posó sobre una flor · local · {'reason': 'coincidencia_local', 'exact_matches': 8, 'edit_cost': 0, 'hypothesis_words': 8}
- 24.51 s: mariposa voló despacio y se posó sobre una flor por lo tanto · local · {'reason': 'coincidencia_local', 'exact_matches': 5, 'edit_cost': 3, 'hypothesis_words': 8}
- 24.81 s: voló despacio y se posó sobre una flor a la hora de · local · {'reason': 'evidencia_incompatible', 'exact_matches': 4, 'edit_cost': 4, 'hypothesis_words': 8}

### Posición 24 · 21.10–22.70 s · 1.60 s

6 callbacks, 5 textos distintos y 2 rechazos de evidencia.

- 21.10 s: árbol encontró una mariposa azul la mariposa voló despacio y se posó · local · {'reason': 'coincidencia_local', 'exact_matches': 8, 'edit_cost': 0, 'hypothesis_words': 8}
- 22.07 s: encontró una mariposa azul la mariposa voló despacio y se posó solo · local · {'reason': 'coincidencia_local', 'exact_matches': 7, 'edit_cost': 1, 'hypothesis_words': 8}
- 22.42 s: la mariposa voló despacio y se posó sobre todo sobre el problema · local · {'reason': 'evidencia_incompatible', 'exact_matches': 4, 'edit_cost': 4, 'hypothesis_words': 8}

### Posición 54 · 52.14–53.71 s · 1.57 s

5 callbacks, 4 textos distintos y 1 rechazos de evidencia.

- 52.14 s: mirando sus alas después volvieron a casa y dibujaron la mariposa en · local · {'reason': 'coincidencia_local', 'exact_matches': 8, 'edit_cost': 0, 'hypothesis_words': 8}
- 53.11 s: después volvieron a casa y dibujaron la mariposa en un buen día · avance_rechazado · {'reason': 'sin_apoyo_final', 'exact_matches': 6, 'edit_cost': 2, 'hypothesis_words': 8}
- 53.43 s: alas después volvieron a casa y dibujaron la mariposa en un cupcakes · avance_rechazado · {'reason': 'sin_apoyo_final', 'exact_matches': 7, 'edit_cost': 1, 'hypothesis_words': 8}

### Posición 50 · 48.87–50.40 s · 1.54 s

3 callbacks, 3 textos distintos y 0 rechazos de evidencia.

- 48.87 s: ce quedaron en silencio mirando sus alas después volvieron a casa y · local · {'reason': 'coincidencia_local', 'exact_matches': 8, 'edit_cost': 0, 'hypothesis_words': 8}
- 49.83 s: quedaron en silencio mirando sus alas después volvieron a casa y di · local · {'reason': 'coincidencia_local', 'exact_matches': 7, 'edit_cost': 1, 'hypothesis_words': 8}
- 50.13 s: quedaron en silencio mirando sus alas después volvieron a casa y dibujar · local · {'reason': 'coincidencia_local', 'exact_matches': 7, 'edit_cost': 1, 'hypothesis_words': 8}

## Small

Posiciones estables ≥1,5 s (excluidos inicio y final): 8. Actualizaciones con evidencia incompatible en la reproducción: 19.

### Posición 22 · 19.81–24.42 s · 4.61 s

11 callbacks, 8 textos distintos y 4 rechazos de evidencia.

- 19.81 s: de un árbol encontró una mariposa azul la mariposa voló despacio y · local · {'reason': 'coincidencia_local', 'exact_matches': 8, 'edit_cost': 0, 'hypothesis_words': 8}
- 21.86 s: encontró una mariposa azul la mariposa voló despacio y ce ce pozo · hipotesis_sin_cambios · {'reason': 'texto_identico', 'exact_matches': 0, 'edit_cost': 0, 'hypothesis_words': 8}
- 24.22 s: mariposa voló despacio y ce ce pozo y lo que se dice · local · {'reason': 'evidencia_incompatible', 'exact_matches': 2, 'edit_cost': 6, 'hypothesis_words': 8}

### Posición 40 · 39.15–41.62 s · 2.46 s

6 callbacks, 5 textos distintos y 1 rechazos de evidencia.

- 39.15 s: llamó a su hermano para que pudiera verla los dos se quedaron · local · {'reason': 'coincidencia_local', 'exact_matches': 8, 'edit_cost': 0, 'hypothesis_words': 8}
- 41.08 s: pudiera verla los dos se quedaron en el caso de la in · local · {'reason': 'evidencia_incompatible', 'exact_matches': 3, 'edit_cost': 5, 'hypothesis_words': 8}
- 41.32 s: su hermano para que pudiera verla los dos se quedaron en silicona · avance_rechazado · {'reason': 'sin_apoyo_final', 'exact_matches': 7, 'edit_cost': 1, 'hypothesis_words': 8}

### Posición 38 · 36.98–39.15 s · 2.17 s

6 callbacks, 5 textos distintos y 0 rechazos de evidencia.

- 36.98 s: flor ana llamó a su hermano para que pudiera verla los dos · local · {'reason': 'coincidencia_local', 'exact_matches': 8, 'edit_cost': 0, 'hypothesis_words': 8}
- 38.46 s: llamó a su hermano para que pudiera verla los dos se quieren · avance_rechazado · {'reason': 'sin_apoyo_final', 'exact_matches': 7, 'edit_cost': 1, 'hypothesis_words': 8}
- 38.88 s: llamó a su hermano para que pudiera verla los dos se quedan · avance_rechazado · {'reason': 'sin_apoyo_final', 'exact_matches': 7, 'edit_cost': 1, 'hypothesis_words': 8}

### Posición 24 · 24.95–27.13 s · 2.17 s

6 callbacks, 5 textos distintos y 4 rechazos de evidencia.

- 24.95 s: mariposa azul la mariposa voló despacio y ce ce pozo se posó · local · {'reason': 'coincidencia_local', 'exact_matches': 5, 'edit_cost': 3, 'hypothesis_words': 8}
- 26.32 s: la mariposa voló despacio y ce ce pozo se posó sobre todo · local · {'reason': 'evidencia_incompatible', 'exact_matches': 4, 'edit_cost': 4, 'hypothesis_words': 8}
- 26.85 s: despacio y ce ce pozo se posó sobre el sistema de seguridad · local · {'reason': 'evidencia_incompatible', 'exact_matches': 3, 'edit_cost': 5, 'hypothesis_words': 8}

### Posición 42 · 41.62–43.60 s · 1.98 s

6 callbacks, 5 textos distintos y 0 rechazos de evidencia.

- 41.62 s: su hermano para que pudiera verla los dos se quedaron en silencio · local · {'reason': 'coincidencia_local', 'exact_matches': 8, 'edit_cost': 0, 'hypothesis_words': 8}
- 43.10 s: para que pudiera verla los dos se quedaron en silencio me gusta · local · {'reason': 'coincidencia_local', 'exact_matches': 6, 'edit_cost': 2, 'hypothesis_words': 8}
- 43.39 s: que pudiera verla los dos se quedaron en silencio me dan miedo · local · {'reason': 'coincidencia_local', 'exact_matches': 5, 'edit_cost': 3, 'hypothesis_words': 8}

