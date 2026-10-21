# Experimento: recuperación global exacta anticipada

Fecha: 19/10/2026. Variante de desarrollo añadida sobre la combinación anterior. Pendiente de comprobación del usuario; no activada en el seguidor habitual.

## Regla probada

Si la búsqueda local no acepta candidato y ya hay una posición con respaldo temporal, examinar la cola completa de hasta ocho palabras de la hipótesis. Debe tener al menos tres palabras, coincidir exactamente como secuencia consecutiva y aparecer una sola vez en todo el cuento. El destino debe estar detrás de la posición actual. Los tiempos ASR de la frase deben ser ordenados y no solaparse entre palabras; el inicio de la frase debe ser igual o posterior al último respaldo aceptado y su final debe ser posterior.

Si cumple todo, aceptar la posición sin esperar los fallos y la confirmación global habituales. En los demás casos, conservar el algoritmo combinado existente. No ampliar ventanas ni cambiar las reglas de palabra aislada, protección temporal o hipótesis de texto idéntico. Los tres términos y las restricciones temporales son provisionales; no representan un óptimo investigado.

No se usan anclas humanas para decidir el movimiento. La coincidencia temporal depende de las estimaciones ASR; una frase exacta y única no prueba que haya habla nueva ni que el texto sea correcto.

## Comprobar desde PowerShell

```powershell
.\.venv\Scripts\python.exe -m scripts.comparar_recuperacion
```

Compara original, combinación anterior y nueva variante en los mismos 36 registros. Usa hipótesis y tiempos ASR/cola existentes, sin inferencias nuevas ni grabaciones. El tiempo propio del seguidor se mide aparte; no se presentan medidas nuevas de latencia completa. Guarda huellas de código, fuentes y anotaciones, informes y trazas compactas.

Resultado principal: resultados/recuperacion/20261019_120146_079995/resumen.json y resumen.md.

## Grabaciones existentes

No cambia ninguna posición respecto a la combinación anterior ni se activa la recuperación nueva en los 36 registros. Se conservan sus mejoras previas de Después y estabilidad de cuaderno, así como sus problemas pendientes: lenta de 4 s termina en 53 y no se mejora el seguimiento temporal de la relectura. La nueva regla todavía no tiene un ejemplo positivo grabado: su mejora se ha observado en casos sintéticos diseñados para estudiarla.

## Controles sintéticos

| Control | Combinación anterior | Nueva variante | Interpretación |
|---|---|---|---|
| A. Frase nueva que después se repite igual | 14,14,14 | 3,3,3 | Recupera en la primera propuesta; las siguientes no actúan como confirmaciones. |
| B. Frase nueva, igual texto con tiempos posteriores | 14,14,14 | 3,3,3 | También recupera desde la primera; no se ha cambiado la política de texto idéntico. |
| C. Frase que va creciendo | 14,14,5 | 3,4,5 | Recupera antes, y los siguientes avances siguen la vía local. |
| D. Variaciones de texto con el mismo candidato | 14,14,3 | 3,3,3 | Recuperación inicial sin esperar dos candidatos globales. |
| E. Frase exacta de audio antiguo | 14 | 14 | No activa la regla. |
| F. Solo dos palabras | 14 | 14 | No activa la regla. |
| G. Una palabra incorrecta | 14 | 14 | No se permite coincidencia aproximada en esta nueva vía. |
| H. Frase que comienza antes del respaldo temporal | 14 | 14 | No activa la regla. |
| I. Texto antiguo rechazado seguido de igual texto con tiempos nuevos | 14,14 | 14,14 | Sigue la limitación de texto idéntico: la segunda propuesta no se procesa. |
| J. Frase que aparece dos veces en un cuento construido de 61 palabras | 61 | 61 | No activa recuperación exacta por ambigüedad. Estado inicial construido, no una lectura adicional. |

Las listas son actualizaciones sintéticas, no segundos ni intentos de un participante. Los negativos muestran que esta vía rápida no se activa bajo esas condiciones; no eliminan otras decisiones que pueda aceptar el algoritmo anterior.

## Comprobaciones y decisión pendiente

Pasan 51 pruebas automáticas. Las seis nuevas verifican recuperación en la primera propuesta, rechazo de tiempos antiguos/solapados/desordenados, secuencia completa exacta/única y longitud mínima, conservación de la limitación de texto idéntico y del camino local, y rechazo de tiempos inválidos.

Mantener la variante separada hasta revisión compartida. Después hará falta una grabación de relectura lejana con marcas selectivas para contrastar la mejora positiva con audio real. No declarar resuelta la relectura ni generalización a otros cuentos o voces. La política de texto idéntico y el coste de reconocimiento permanecen como preguntas separadas.
