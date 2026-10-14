# Prueba 05: cinco ventanas acústicas y dos rondas

Estado: comprobación local del desarrollador y reproducción del usuario completadas. Cambios sin subir a GitHub; pendiente de autorización.

Registros: `resultados/comparaciones/20261014_093754_597676/`.

## Pregunta y configuración

Se comparan el prefijo completo y ventanas de 4, 6, 8, 10 y 12 s, manteniendo bloques de 2 s, modelo Whisper small, CPU int8, VAD y seguidor. Solapamientos de 2, 4, 6, 8 y 10 s. Dos rondas en orden aleatorio reproducible (semilla 20261014), ejecutadas secuencialmente sobre el mismo WAV adulto de 30 s con desviaciones deliberadas. No hay nuevas grabaciones ni entrenamiento.

Comando:

```powershell
.\.venv\Scripts\python.exe -u scripts\comparar_ventanas.py --ventanas 0 4 6 8 10 12 --repeticiones 2
```

## Resultados

| Método | Total medio inferencia (s) | Rango entre rondas (s) | Inferencias >2 s | Media de cola máxima simulada (s) | Media de inferencia hasta corte 24 s |
|---|---:|---|---:|---:|---:|
| Prefijo | 44,39 | 44,31–44,47 | 20/30 | 13,09 | 30,82 |
| Ventana 4 s | 24,30 | 22,61–25,99 | 7/30 | 0,35 | 22,49 |
| Ventana 6 s | 26,92 | 24,93–28,90 | 10/30 | 0,76 | 23,10 |
| Ventana 8 s | 26,90 | 26,17–27,63 | 2/30 | 0,02 | 21,96 |
| Ventana 10 s | 28,88 | 28,83–28,92 | 12/30 | 0,49 | 23,53 |
| Ventana 12 s | 30,03 | 29,67–30,39 | 14/30 | 1,33 | 24,38 |

Se excluye carga del modelo de los tiempos de inferencia. La cola es simulada y no mide captura ni pantalla. La comparación hasta 24 s usa un corte común observado; no es una anotación humana del final de voz.

## Seguimiento

Las doce ejecuciones llegan al índice 56, cuaderno, al corte de 24 s y no presentan retrocesos. Para cada configuración, las posiciones en todos los cortes son iguales entre rondas. Las ventanas de 4, 6, 8 y 10 s tienen la misma secuencia de posiciones en esta grabación; prefijo y ventana de 12 s difieren en el corte de 16 s, conservando dos (38) en lugar de se (39). El prefijo queda en dibujaron (51) al corte de 22 s, mientras las ventanas llegan a la (52).

Esto describe concordancia y repetibilidad de las salidas. No valida qué posición es la real: falta anotación humana. Las transcripciones sí difieren con el contexto, especialmente alrededor de fragmentos incompletos.

## Interpretación y decisión provisional

- La ventana de 4 s tiene menor total medio, pero parte del ahorro proviene de descartar antes las ventanas de silencio al final.
- La ventana de 8 s presenta solo 2 de 30 inferencias superiores a 2 s y menor cola simulada en este experimento. Hasta el corte común de 24 s tiene el menor coste medio, con diferencias modestas frente a 4 y 6 s.
- Las ventanas de 4 y 6 s varían apreciablemente entre rondas. Aleatorizar el orden no elimina variación de carga, temperatura u otras condiciones, que no se midieron.
- Dos rondas sobre un único audio adulto no justifican declarar una ventana óptima universal ni un comportamiento infantil.
- Mantener 4 y 8 s como candidatos junto a la referencia de 6 s. No cambiar todavía el modo por defecto. Próxima decisión tras reproducir el usuario esta prueba y evaluar pausas/relecturas y precisión temporal.

## Comprobaciones

Trece pruebas automáticas pasan. Se verifican los intervalos de audio y rangos de posición de las 180 actualizaciones en los doce registros. El informe incluye plan y semilla, resultados por ronda, medias/rangos y posiciones por corte.

## Reproducción del usuario: tres rondas

Registros: `resultados/comparaciones/20261014_100148_765908/`. Se ejecutan 18 pruebas del mismo WAV, con 270 actualizaciones; no son nuevas lecturas.

| Método | Total medio (s) | Inferencias >2 s | Cola máxima media simulada (s) |
|---|---:|---:|---:|
| Prefijo | 44,85 | 30/45 | 13,73 |
| Ventana 4 s | 22,45 | 0/45 | 0,00 |
| Ventana 6 s | 24,71 | 6/45 | 0,14 |
| Ventana 8 s | 26,59 | 1/45 | 0,09 |
| Ventana 10 s | 28,18 | 13/45 | 0,28 |
| Ventana 12 s | 30,16 | 24/45 | 1,62 |

Las secuencias de posición se mantienen entre rondas; las ventanas 4/6/8/10 coinciden y alcanzan cuaderno al corte de 24 s. Hasta ese corte, el coste medio es 20,80 s en ventana 4, 21,52 s en ventana 6 y 21,72 s en ventana 8, frente a 31,04 s del prefijo.

La ventana de 4 s pasa a candidato principal para nuevas grabaciones, conservando 8 s como alternativa. Este resultado revisa la preferencia por estabilidad de 8 s en la ejecución anterior; los tiempos varían y no hay referencia humana de posición. No se modifica el modo por defecto ni se publica sin autorización. La ausencia de cola simulada en la ventana de 4 s no elimina la espera del bloque ni la inferencia.
