# Balance de la revisión temporal de eventos

Fecha: 19/10/2026. Evaluación de desarrollo de un adulto, un cuento y el entorno actual. Las tres rondas de cada caso reutilizan una misma grabación. No constituyen participantes independientes ni validación infantil.

| Caso | Referencia revisada por el lector | Resultado observado |
|---|---|---|
| Lectura normal | 56 palabras; nueve notas de límites ambiguos | Hipótesis próximas a las marcas en los once cortes durante la lectura; la salida visible simulada presenta mayor desfase por periodo de actualización y cómputo. |
| Pausa | Flor, Ana al retomar y cuaderno | Pausa sin lectura de 9,32 s. Hipótesis en posición 27 en los cinco cortes de la pausa de cada ejecución. El primer avance posterior aparece en el corte 24 s. |
| Lectura lenta | Después, mariposa final, un y cuaderno | Cuaderno termina en 77,34 s. Ventana 4 s: nunca llega a 56. Ventana 8 s: llega en el corte 78 s y retrocede a 55 desde 80 s. |
| Relectura | Dos intentos de Los dos se quedaron en silencio y mirando | Intentos 17,54–19,84 y 20,36–22,77 s. Solo un corte dentro del segundo intento. 4 s retrocede 42→41; 8 s mantiene 42. No se demuestra seguimiento completo desde Los. |

## Límite de la evidencia de relectura

Las seis ejecuciones presentan las mismas secuencias de posiciones para cada ventana en los cortes 20, 22 y 24 s: 42→41→45 para 4 s y 42→42→45 para 8 s. El movimiento negativo de 4 s pertenece al corte 22 s, pero la salida estaría lista entre 23,65 y 23,72 s, después del fin del segundo intento (22,77 s). Este cálculo usa la cola secuencial simulada, excluye carga inicial del modelo y no mide pantalla.

El texto ASR conserva evidencia de dos intentos en ventanas que abarcan ambos. Su conservación no equivale a localizar cada intento en tiempo real. Tampoco las marcas de frase completa permiten conocer el instante humano de cada palabra interior. No se exige una posición exacta de 37 en un corte que ocurre cerca del final del segundo intento.

## Decisión provisional

Conservar estos registros como comparación inicial antes de cambiar el seguidor. No bloquear todos los retrocesos: existe una relectura real. No elegir ventana solo por coste o por posición final: un método puede acertar el final y retroceder después, o conservar el texto repetido sin seguirlo a tiempo.

La siguiente intervención debe estudiar por separado:

1. Seguimiento de habla lenta con pocas palabras disponibles: revisar aceptación de evidencia y recuperación cuando la hipótesis contiene una sola palabra útil.
2. Diferenciar posición provisional y posición respaldada por evidencia, conservando la posibilidad de volver atrás ante una relectura. Evitar una regla fija de avance irreversible.
3. Coste de inferencia y política de actualización. Reducir el periodo de dos segundos sin medir coste puede acumular cola; no prometer menor demora solo por actualizar más a menudo.

Cambiar un componente por experimento y contrastarlo con normal, pausa, lenta y relectura, midiendo también regresiones. Después comparar modelos y ayudas de audio con la misma base de referencias, sin mezclar varios cambios. No se necesitan más marcas humanas para cerrar esta primera revisión de eventos; ampliar cobertura únicamente si una nueva pregunta lo exige.

## Evidencia reproducible

- Normal: resultados/comparaciones/20261019_084114_510023/evaluacion_humana.json y .md.
- Pausa: resultados/comparaciones/20261014_111548_094194/evaluacion_pausa.json y .md.
- Lenta: resultados/comparaciones/20261016_095252_869489/evaluacion_lenta.json y .md.
- Relectura: resultados/comparaciones/20261016_104206_415649/evaluacion_relectura.json y .md.

Los evaluadores registran huellas de anotaciones y registros reutilizados. Las referencias parciales no se interpolan para fabricar una referencia global.
