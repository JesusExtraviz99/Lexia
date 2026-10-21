# Comparación de las dos mejoras juntas

Fecha: 19/10/2026. Estado: experimento local pendiente de comprobación del usuario.

## Publicación anterior

Antes de este experimento se publica c99035d: mejoras aisladas, diagnóstico, registros y comprobaciones del usuario. Se retira docs/RUTA_TRABAJO.md por petición del usuario. Esta comparación conjunta no pertenece a ese commit.

## Pregunta y método

¿Conserva la combinación la mejora de evidencia escasa y la protección ante revisiones de audio anterior, sin cambios adicionales en los registros de desarrollo?

Se comparan original, palabra aislada, protección temporal y ambas reglas, con parámetros idénticos a los experimentos individuales. Son 36 registros por cuatro versiones, no 144 grabaciones ni participantes. Mismo ASR, hipótesis, ventanas y cortes; no se ejecutan nuevas inferencias. Los tiempos de ASR/cola se reutilizan y no son medidas nuevas de latencia real.

La regla temporal envuelve el algoritmo de palabra aislada. Cuando esa palabra produce un avance, también debe conservarse su tiempo ASR como respaldo; de otro modo la combinación olvidaría parte de la evidencia que ya ha aceptado. Se comprueba explícitamente este enlace entre reglas.

## Comprobación desde PowerShell

```powershell
.\.venv\Scripts\python.exe -m scripts.comparar_combinacion
```

El comando muestra los cuatro finales por ejecución, cambios frente al original, posiciones combinadas no observadas en las versiones aisladas y detalle de las reglas aplicadas. Conserva anclas humanas y huellas de código y registros. Las trazas compactas identifican la fuente original con sus hipótesis completas, sin duplicarlas.

## Resultados en grabaciones

Informe principal: resultados/combinacion/20261019_112016_077915/resumen.json y resumen.md.

- Lectura lenta con 4 s: la combinación conserva el avance 45→46 en los cortes 62/64 s, en las tres rondas. Final 53 en las cuatro versiones.
- Lectura lenta con 8 s: conserva 56 tras el corte 80 s en las tres rondas, igual que la protección temporal aislada. Original y palabra aislada terminan en 55; temporal y combinación en 56.
- Normal, desviaciones, pausa y relectura: no cambian las posiciones en ninguna de las variantes. No se mejora todavía la demora de relectura.
- No aparecen posiciones nuevas exclusivas de la combinación en las grabaciones. No equivale a demostrar independencia de reglas ni ausencia universal de efectos adversos.
- Pasan 45 pruebas automáticas. Las nuevas comprueban ambas reglas en una misma secuencia sintética, un retroceso con respaldo posterior dentro de la búsqueda local, actualización temporal de palabra aislada y detección de posiciones nuevas en el informe de interacción.

## Límite adicional encontrado

Un caso sintético muestra un efecto de conservar la posición que no aparece en las grabaciones disponibles. Tras mantener 14 en lugar de retroceder a 13, una relectura de mirando sus alas hacia la posición 3 deja solo alas dentro de la ventana local (empieza en 3). Una coincidencia es insuficiente. El original, que estaba en 13, todavía incluye sus y alas en su ventana local (empieza en 2) y acepta 3.

Resultado de esa actualización: original 3, palabra aislada 3, temporal 14, combinación 14. El candidato no supera el filtro textual local antes de llegar a la comprobación temporal. No es un rechazo por tiempos antiguos: el alcance de búsqueda necesita una recuperación adicional. No se evalúa aquí cuánto tardaría la recuperación global con hipótesis posteriores.

Este caso es construido, no una grabación humana adicional. Se incluye en la salida para evitar concluir que conservar un final no puede perjudicar una vuelta larga. El límite afecta ya a la regla temporal aislada, no surge exclusivamente al combinarla con palabra aislada.

## Decisión pendiente

Mantener las cuatro versiones como experimento. No activar aún la combinación en el seguidor habitual. Revisar el resultado con el usuario y estudiar por separado la recuperación de relecturas que quedan fuera de la búsqueda local. Se conservan los límites conocidos de timestamps y de hipótesis con texto idéntico. No se solicita más anotación humana para ejecutar esta comparación.
