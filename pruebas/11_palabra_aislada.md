# Experimento: evidencia de una palabra aislada

Fecha: 19/10/2026. Variante de desarrollo, no activada en el seguidor habitual.

## Pregunta

¿Puede recuperarse un avance perdido en lectura lenta cuando el ASR entrega una sola palabra útil, sin alterar los otros casos de desarrollo?

## Cambio aislado

El seguidor original requiere al menos dos coincidencias. La variante permite avanzar exactamente una posición cuando la hipótesis entera consta de una palabra, tiene cinco o más caracteres normalizados, coincide exactamente con la siguiente palabra del cuento y esa coincidencia es única en la ventana local. Requiere una posición previa mayor que cero. Las demás hipótesis siguen el algoritmo original, que conserva la posibilidad de retroceder con evidencia de varias palabras.

La longitud mínima es una restricción provisional para este experimento, no un umbral óptimo demostrado. Una palabra inventada por el ASR que coincida con la siguiente palabra del cuento aún podría provocar un avance falso: la regla no comprueba el audio por sí misma.

## Método reproducible

```powershell
.\.venv\Scripts\python.exe -m scripts.comparar_seguidores
```

Se reproducen 36 registros guardados: normal y desviaciones con ventanas 4/6/8 s, y pausa, lenta y relectura con 4/8 s; tres rondas por configuración. Los audios de una misma condición y las rondas no son lectores independientes. Se verifica primero que el seguidor original reproduce exactamente posición, movimiento y modo de todos los registros seleccionados. Después se ejecuta la variante sobre las mismas hipótesis.

El experimento no carga el modelo, no descarga recursos, no graba audio y no cambia los registros originales ni scripts/seguir.py. Los JSON derivados conservan hipótesis y tiempos ASR anteriores. La duración propia de las actualizaciones del seguidor se mide aparte; no se afirma que los tiempos de inferencia, cola o latencia total sean nuevos. Se evalúan ambas variantes con las mismas anotaciones humanas cuando están disponibles. En desviaciones se compara comportamiento sin fabricar una referencia temporal.

## Resultados

Registro principal: resultados/seguidores/20261019_104824_848649/resumen.json y resumen.md. Se conservan huellas de fuentes, código y anotaciones.

- El seguidor original reproduce los 36 registros sin diferencias de posición, movimiento o modo.
- En lectura lenta con ventana 4 s, la nueva regla se aplica a Después en el corte 62 s de las tres rondas. La posición pasa de 45 a 46 en los cortes 62 y 64 s. El final humano de Después es 61,42 s: el avance está respaldado por esa ancla. En 66 s ambas versiones vuelven a coincidir en 49.
- Son seis posiciones modificadas entre las tres rondas; no son seis experimentos independientes.
- En las otras 33 ejecuciones no cambian las posiciones. Tampoco cambia el resto de cortes de las tres ejecuciones modificadas. Esto describe los casos observados, no demuestra ausencia universal de regresiones.
- El final de lectura lenta sigue sin resolverse: 4 s termina en 53 y 8 s en 55. La relectura conserva el comportamiento anterior; esta regla no pretende solucionar su demora.
- Pasan 35 pruebas automáticas, incluidas restricciones de palabra aislada, relectura hacia atrás y reproducción sin alterar datos ni tiempos de entrada.

## Decisión

Conservar la variante como candidata experimental por su mejora localizada. No sustituir todavía el seguidor habitual ni declarar resuelta la lectura lenta. Este resultado fue obtenido sobre datos usados para diseñar la regla y requiere contraste futuro con otras grabaciones antes de generalizar.

La siguiente pregunta es cómo conservar una llegada al final respaldada por evidencia sin bloquear una relectura real. Ese comportamiento debe estudiarse como otro cambio, separado de la aceptación de una palabra aislada.
