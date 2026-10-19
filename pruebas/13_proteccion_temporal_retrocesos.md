# Experimento: respaldo temporal para aceptar retrocesos

Fecha: 19/10/2026. Variante experimental independiente; pendiente de comprobación del usuario en su terminal. No sustituye el seguidor habitual ni se combina con la regla de palabra aislada.

## Motivo y cambio

El usuario reproduce el diagnóstico anterior y confirma la secuencia cuaderno→un cuando el ASR cambia en un cuaderno por en un jugaderno al reprocesar audio solapado. Este experimento conserva el alineamiento original y añade solo una condición para retroceder.

Se mantiene la mayor marca de final ASR de la última coincidencia exacta que respaldó una posición aceptada. Si una nueva hipótesis propone retroceder, el final ASR de la coincidencia que respalda ese candidato debe ser posterior a dicha marca. Si no lo es, se conserva la posición y el estado de seguimiento anteriores. Las anclas humanas no intervienen en la decisión; se usan después para evaluar.

Para identificar la palabra ASR que respalda el candidato se usa el recorrido del mismo alineamiento, no la última palabra de la hipótesis ni una búsqueda por su escritura. locate incorpora una opción diagnóstica para devolver ese índice; por defecto su salida y las reglas originales no cambian.

En el caso diagnosticado, cuaderno había respaldado 56 con final ASR 77,26 s. La revisión propone 55 por un con final ASR 74,66 s: no aporta un respaldo posterior y se rechaza. Estas son estimaciones del ASR, distintas de las marcas humanas.

## Comprobación desde PowerShell

```powershell
.\.venv\Scripts\python.exe -m scripts.comparar_seguidores --variante temporal
```

El comando imprime la comparación y guarda registros e informes en una carpeta nueva de resultados/retrocesos. Solo reproduce hipótesis guardadas: no usa micrófono ni ejecuta nuevas inferencias. La opción por defecto de comparar_seguidores continúa reproduciendo el experimento de palabra aislada.

## Método y resultado

Referencia inicial: resultados/retrocesos/20261019_110452_881233/resumen.json y resumen.md. Treinta y seis registros, los mismos casos y ventanas del experimento anterior. Se comprueba primero que el original reproduce todas las posiciones, movimientos y modos guardados.

- Lectura lenta, ventana 8 s, tres rondas: retroceso rechazado en el corte 80 s. La posición permanece en 56 en los seis cortes 80–90 s; el original se mantenía en 55. El primer corte que alcanza 56 sigue siendo 78 s: no se mejora la demora inicial de llegada.
- Otros 33 registros: ninguna posición cambia. En particular, las rondas de relectura conservan el movimiento 42→41 de 4 s y la retención en 42 de 8 s. Conservar ese movimiento no demuestra seguimiento completo de la frase repetida.
- Ventana lenta de 4 s: sigue terminando en 53. Este cambio no resuelve ni el reconocimiento del final en esa ventana ni el bloqueo de Después.
- Pasan 42 pruebas en total. Las cinco nuevas verifican rechazo de apoyo temporal antiguo, aceptación de un retroceso con apoyo posterior, trazabilidad de la coincidencia, política de texto idéntico y rechazo de timestamps inválidos.
- Los tiempos de inferencia/cola son los de los registros originales; las métricas visibles derivadas no son nuevas medidas de latencia real. El coste propio del seguidor se mide aparte.

## Límites y decisión pendiente

Los tiempos ASR tienen errores. Esta primera condición no admite tolerancia temporal: un pequeño desplazamiento erróneo hacia delante podría permitir un retroceso falso, y un tiempo erróneo hacia atrás podría frenar una relectura real. Tampoco comprueba por sí sola que haya nueva voz. No debe presentarse como detector de habla o relecturas.

Se conserva la política original que no vuelve a actualizar ante una hipótesis con texto idéntico, aunque cambien sus tiempos. Puede limitar relecturas con hipótesis idénticas; no se cambia en este experimento para evitar mezclar efectos.

Resultado de desarrollo sobre audios empleados para diseñar la regla, sin validación independiente. Mantener la variante separada, revisar la salida con el usuario y decidir después sobre su incorporación. No unir ambas mejoras ni modificar el seguidor de uso habitual antes de esa revisión.
