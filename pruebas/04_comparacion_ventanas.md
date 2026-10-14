# Prueba 04: ventanas acústicas con solapamiento

Estado: comprobaciones locales y reproducción del usuario completadas. Pendiente de autorización para subir a GitHub.

Registros e informe: `resultados/comparaciones/20261014_091512_716487/`.

## Configuración

Dos audios, tres configuraciones: prefijo completo, ventana de 6 s y ventana de 10 s. Bloques de 2 s, solapamiento respectivamente de 4 y 8 s. Se conserva el modelo Whisper small, CPU int8, beam_size=5, VAD y el seguidor. Una ejecución por configuración, en orden fijo; sin referencia humana de posición.

El modelo recibe únicamente muestras dentro del intervalo disponible. Los timestamps de cada ventana se trasladan al reloj global del WAV. Las hipótesis de ventanas solapadas no se concatenan ni se cuentan como nuevos intentos. Se conserva la posición global del cuento.

## Resultados orientativos

| Grabación | Método | Total de inferencia (s) | Inferencias >2 s | Cola máxima simulada (s) | Posición final |
|---|---|---:|---:|---:|---:|
| Normal | Prefijo | 50,51 | 14/20 | 10,18 | 56 |
| Normal | Ventana 6 s | 25,93 | 2/20 | 0,13 | 56 |
| Normal | Ventana 10 s | 30,35 | 6/20 | 0,44 | 56 |
| Con desviaciones | Prefijo | 44,74 | 10/15 | 13,39 | 56 |
| Con desviaciones | Ventana 6 s | 24,58 | 0/15 | 0,00 | 56 |
| Con desviaciones | Ventana 10 s | 29,01 | 6/15 | 0,66 | 56 |

Las seis ejecuciones alcanzan cuaderno en el corte de 24 s y no presentan retrocesos. Esto no demuestra precisión de todas las posiciones intermedias: por ejemplo, en el corte de 22 s de la lectura normal el prefijo queda en 51 y las ventanas llegan a 53.

Parte de la reducción total procede del silencio final: una ventana vacía se descarta rápidamente mediante VAD mientras el prefijo mantiene el habla antigua. Considerando solo las actualizaciones hasta el corte de 24 s, los costes fueron 26,07 / 22,56 / 23,23 s para prefijo / ventana 6 / ventana 10 en la lectura normal y 30,89 / 21,27 / 23,39 s en la lectura con desviaciones. El corte de 24 s se usa aquí como punto común de comparación observado, no como anotación humana del fin de voz.

## Hipótesis temporales

En la lectura con desviaciones, al corte de 16 s las ventanas llegan a se (39), mientras el prefijo queda en dos (38). Al corte de 22 s, el prefijo devuelve Hola Madi, la ventana de 6 s devuelve la marina y la de 10 s devuelve la mari. Los tres vuelven a alcanzar cuaderno al corte de 24 s. Es evidencia de sensibilidad al contexto, no detección validada de autocorrección.

## Comprobaciones y siguiente decisión

Once pruebas de lógica pasan. Se verificaron los intervalos de las 105 actualizaciones: inicio no negativo, fin igual al audio disponible, duración no superior a la ventana configurada y posición dentro del cuento.

La ventana de 6 s es el primer candidato para continuar probando. No se cambia el modo predeterminado del seguidor: sin --ventana sigue usando prefijos para conservar la comparación base. Falta anotación temporal para evaluar posición y pruebas más largas con pausas y relecturas antes de afirmar viabilidad en directo.

## Reproducción del usuario

Registros: `resultados/comparaciones/20261014_092131_720136/`, sobre el audio con desviaciones. Para prefijo / ventana 6 / ventana 10: totales de inferencia 53,17 / 29,51 / 33,22 s; medianas 3,46 / 2,10 / 2,32 s; actualizaciones que superan 2 s: 10 / 11 / 10 de 15; colas máximas simuladas: 21,04 / 2,15 / 4,31 s.

Los tres métodos mantienen exactamente sus secuencias de posiciones de la comprobación anterior y llegan a 56 al corte de 24 s. Los tiempos varían: la ventana de 6 s sigue siendo la de menor coste y cola, pero ya no sostiene todas las inferencias por debajo de 2 s. No hay datos para atribuir esta variación a carga, temperatura o alimentación.

Hasta el corte de 24 s, los costes son 35,47 / 25,46 / 27,38 s. La mejora no depende exclusivamente del silencio final. La ejecución del usuario completa la comprobación prevista, pero no implica aprobación para subir los cambios ni validación temporal del indicador.
