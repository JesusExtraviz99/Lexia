# Diario de desarrollo y experimentación — Lexia

Proyecto de prácticas y TFG de lectura asistida en español.

Inicio del diario: 14 de octubre de 2026, zona horaria Atlantic/Canary. Las primeras entradas se reconstruyen a partir de la conversación, las fichas de pruebas, los registros y los commits. Las horas de los nombres de archivo se conservan como identificadores, sin asumir que corresponden a la hora local del usuario.

## Cómo se mantiene

Se añadirá una entrada tras cada cambio relevante, experimento, incidencia o decisión. Cada entrada recoge objetivo, cambios/configuración, evidencia, interpretación, límites y siguiente paso. Los resultados comunicados por el lector se distinguirán de las comprobaciones automáticas y de las hipótesis del desarrollador.

Las conclusiones provisionales se revisarán mediante entradas nuevas que enlacen las anteriores. No se borrarán observaciones porque después cambie el método. Se conservarán configuraciones y archivos para reproducir las pruebas.

El diario se actualiza durante el trabajo, sin necesitar una petición nueva para cada entrada. Primero se prueba localmente, después el usuario revisa los cambios y finalmente autoriza su subida a GitHub. No se publican cambios por el mero hecho de anotarlos aquí.

## Estado del proyecto

- Implementados: grabación local, transcripción posterior, alineamiento textual, seguimiento simulado por prefijos y comparación con ventanas solapadas.
- Probados por el usuario: grabación/transcripción, alineamiento, seguimiento por prefijos y comparación de ventanas de 6 y 10 s.
- Probado también por el usuario: experimento ampliado de ventanas, con tres rondas sobre el mismo audio.
- Probada por el usuario: grabación con pausa de unos 8 s y revisión humana del ruido de pájaros al final.
- Probada por el usuario: lectura lenta, con bloqueos, regresión final y pico de procesamiento documentados.
- Probada por el usuario: relectura de una frase; completado el primer recorrido de cinco casos adultos.
- Banco de pruebas catalogado y cinco transcripciones literales confirmadas por escucha del usuario. Pendientes: tiempos humanos por palabra/evento y evaluador de calidad.
- Publicación autorizada: relectura, WAV, resultados y diario hasta E020; primer ciclo de cinco casos adultos conservado. El commit de esta entrega se consulta en el historial de Git.
- Próximo trabajo local: referencias y métricas de calidad para comparar configuraciones sin limitarse a tiempos y posición final.
- Configuración pendiente de selección: 4 s reduce coste en las primeras lecturas, pero se bloquea al final de la lectura lenta; 8 s alcanza el final y después retrocede, con un pico de procesamiento. Mantener ambas como comparación. Bloque de 2 s, modo predeterminado de prefijo sin cambios.
- No implementados: subrayado visual, captura con seguimiento en directo y diagnóstico fiable de errores lectores.
- Datos actuales: cinco lecturas de un mismo adulto (normal, desviaciones, pausa, lenta y relectura), con un cuento de 56 palabras. No permiten conclusiones sobre lectura infantil ni generalización a otros textos.

## E001 · Del informe al primer prototipo

**Fecha:** 14/10/2026. Reconstrucción retrospectiva.

**Objetivo.** Pasar de la revisión bibliográfica del 09/10/2026 a una prueba pequeña y reproducible.

**Decisión.** Empezar por un lector adulto, cuento corto en español y procesamiento local. Separar reconocimiento, seguimiento y evaluación. Aceptar una hipótesis para mover el indicador no significa calificar la palabra como correcta.

**Cambios.** Se crean el alcance, la guía y los scripts de preparación del modelo, grabación y transcripción. Se prepara un entorno aislado de Python 3.12, manteniendo el Python 3.14 existente. El ordenador dispone de unos 16 GB de RAM y una RTX 3050 Laptop de 4 GB; la primera ejecución utiliza CPU int8.

**Configuración.** Whisper small multilingüe, faster-whisper 1.2.1, sounddevice 0.5.5 y soundfile 0.13.1. Las versiones completas se guardan en requirements-lock.txt. Se descarga el modelo para inferencia local.

**Evidencia y límites.** La comprobación inicial carga el modelo y procesa audio en memoria. No cubre aún la apertura de WAV, limitación que se manifiesta en E002.

**Referencias.** [Informe original](Informe%20Lectura%20Asistida%20Prototipo.md), [alcance](../ALCANCE.md), [guía](../EMPEZAR.md).

## E002 · Incidencia al abrir el WAV y primera lectura normal

**Fecha:** 14/10/2026. Reconstrucción retrospectiva.

**Observación del usuario.** La grabación se guarda, pero la transcripción falla con `TypeError: open() got an unexpected keyword argument 'metadata_errors'`.

**Causa y cambio.** faster-whisper 1.2.1 llama a PyAV con un parámetro rechazado por PyAV 19.0.1. Se fija `av==16.0.1`, se actualiza el archivo de versiones y se prueba la apertura del WAV real.

**Resultado.** La transcripción funciona. La ejecución mostrada por el usuario tarda 3,99 s de inferencia y 0,87 s de carga. El texto reconocido coincide con las palabras del cuento, salvo puntuación. Son tiempos de procesamiento posterior, no latencia del indicador.

**Aprendizaje.** Cargar el modelo y procesar un array no verifica el recorrido completo desde archivo. Las comprobaciones posteriores deben incluir el formato real de entrada.

**Evidencia.** [Ficha 01](../pruebas/01_lectura_normal.md), WAV `datos/audio/lectura_20261014_081816_009646.wav` y JSON con ese prefijo en resultados.

## E003 · Repetición, omisión y autocorrección deliberadas

**Fecha:** 14/10/2026. Reconstrucción retrospectiva.

**Objetivo.** Comprobar si el ASR conserva desviaciones que interesan para evaluar lectura.

**Referencia del lector.** Repite Ana dos veces al principio, omite despacio e introduce mari… mariposa en la última frase. Indica haber pronunciado silencio, aunque la salida muestra cinesio. No se ha realizado una anotación humana independiente del audio.

**Resultados del JSON.** Dos entradas Ana; no aparece despacio; una sola entrada para la última mariposa, de 20,98 a 22,86 s; sustitución silencio/cinesio según la referencia del lector. Inferencia: 3,85 s; carga: 0,84 s; archivo: 30 s.

**Interpretación.** La transcripción preserva repetición y ausencia de la palabra omitida, pero no representa el fragmento mari… por separado. El intervalo largo de mariposa puede abarcar varios intentos; no prueba por sí solo una autocorrección. Cinesio no debe atribuirse automáticamente al lector.

**Decisión.** Conservar audio y salida original. No corregir silenciosamente contra el cuento. Comparar textos no recupera lo que el reconocedor elimina.

**Evidencia.** [Ficha 02](../pruebas/02_lectura_con_disfluencias.md).

## E004 · Alineamiento textual posterior

**Fecha:** 14/10/2026. Reconstrucción retrospectiva.

**Cambios.** Se añade scripts/alinear.py: distancia de edición global con costes unitarios e índices del cuento desde 1. Ignora caja y puntuación, conservando tildes y ñ. Marca diferencias candidatas y reconoce inserciones que duplican un fragmento contiguo como repeticiones candidatas. Genera Markdown y JSON.

**Resultados.** Lectura normal: 56 coincidencias. Lectura con desviaciones: 54 coincidencias, repetición de Ana, omisión de despacio y sustitución silencio/cinesio. El usuario ejecuta el programa y confirma esa salida. Pasan cinco pruebas automáticas.

**Aprendizaje.** Cuento y segunda transcripción tienen ambos 56 palabras: repetición y omisión se compensan en el total. El recuento no permite diagnosticar la lectura. Una coincidencia textual tampoco certifica pronunciación correcta.

**Límites.** Usa la transcripción completa y puede ser ambiguo con palabras repetidas. No demuestra seguimiento en directo ni recupera mari….

**Evidencia.** Informes de resultados/alineamientos. Publicado en commit `7b4f83b`.

## E005 · Seguimiento con audio disponible progresivamente

**Fecha:** 14/10/2026. Reconstrucción retrospectiva.

**Cambios.** Se añade scripts/seguir.py. Cada 2 s del WAV se vuelve a reconocer únicamente el prefijo disponible. El seguidor usa las últimas 8 palabras ASR, una ventana textual de hasta 12 palabras anteriores y 24 posteriores, tolerancia a ediciones y recuperación con confirmación. Se activa VAD: la configuración difiere de la transcripción inicial sin VAD.

**Convención.** La posición es la última palabra del cuento respaldada por coincidencia textual, no la palabra pronunciada actualmente. Las hipótesis pueden revisar posiciones anteriores. Se registra tiempo de inferencia y una cola secuencial simulada, excluyendo carga del modelo, captura y pantalla.

**Resultados.** Ambas grabaciones alcanzan cuaderno, índice 56, al corte de 24 s. Pasan diez pruebas automáticas. El usuario reproduce la prueba con desviaciones.

**Observación del usuario.** Al corte de 16 s aparece Los dos secu; al de 18 s se revisa a Los dos se quedaron. El seguidor pasa de dos (38) a sus (44). Al corte de 22 s aparece Hola Madi y posteriormente se revisa a la mariposa en un cuaderno.

**Coste.** En la ejecución del usuario, 15 inferencias suman aproximadamente 41,77 s para un audio de 30 s. Varias actualizaciones superan los 2 s. La disponibilidad final secuencial simulada es aproximadamente 45,84 s. No es una medición de latencia visual.

**Decisión.** Comparar ventanas acústicas limitadas para reducir reprocesamiento. Guardar cada hipótesis disponible; no fabricar el seguimiento a partir del resultado final.

**Evidencia.** [Ficha 03](../pruebas/03_seguimiento_progresivo.md), registro con sufijo `090803_312561_seguimiento`. Publicado en commit `22c7ab3` después de autorización del usuario.

## E006 · Comparación de ventanas de 6 y 10 segundos

**Fecha:** 14/10/2026. Comprobación del desarrollador, pendiente del usuario.

**Objetivo.** Reducir coste sin perder continuidad, conservando el método de prefijos como comparación.

**Cambios.** scripts/seguir.py acepta --ventana y scripts/comparar_ventanas.py ejecuta tres configuraciones sobre el mismo audio. Ventanas de 6 y 10 s, actualización cada 2 s, solapamientos de 4 y 8 s. Mismos modelo, CPU, VAD y seguidor. Los tiempos ASR se trasladan al reloj global. Las hipótesis solapadas no se concatenan ni se cuentan como intentos nuevos.

**Resultados orientativos.** Una ejecución por configuración, en orden fijo.

| Audio | Método | Inferencia total (s) | Actualizaciones >2 s | Cola máxima simulada (s) |
|---|---|---:|---:|---:|
| Normal | Prefijo | 50,51 | 14/20 | 10,18 |
| Normal | Ventana 6 s | 25,93 | 2/20 | 0,13 |
| Normal | Ventana 10 s | 30,35 | 6/20 | 0,44 |
| Con desviaciones | Prefijo | 44,74 | 10/15 | 13,39 |
| Con desviaciones | Ventana 6 s | 24,58 | 0/15 | 0,00 |
| Con desviaciones | Ventana 10 s | 29,01 | 6/15 | 0,66 |

**Posición.** Las seis ejecuciones llegan a 56 al corte de 24 s, sin retrocesos. Algunas posiciones intermedias difieren. En la lectura con desviaciones, al corte de 22 s la ventana de 6 s devuelve la marina y la de 10 s la mari, frente a Hola Madi del prefijo.

**Límites.** Parte del ahorro procede de dejar de reprocesar habla antigua durante el silencio final. Hasta el corte común de 24 s, los costes prefijo/6 s/10 s son 26,07/22,56/23,23 s en la lectura normal y 30,89/21,27/23,39 s en la lectura con desviaciones. No hay referencia humana temporal ni repeticiones que controlen carga o calentamiento del ordenador.

**Comprobaciones.** Once pruebas de lógica pasan. Se verifican intervalos y rangos de posición en 105 actualizaciones de los seis registros.

**Decisión provisional.** La ventana de 6 s es el candidato inicial para continuar experimentando. No se cambia el modo por defecto. Alcanzar el final no prueba precisión temporal ni funcionamiento infantil.

**Evidencia.** [Ficha 04](../pruebas/04_comparacion_ventanas.md), [resumen comparativo](../resultados/comparaciones/20261014_091512_716487/resumen.md). Sin subir a GitHub.

## E007 · Qué aporta la bibliografía a la elección de ventana

**Fecha:** 14/10/2026. Interpretación discutida con el usuario.

**Pregunta.** ¿Existe una ventana acústica recomendada por los papers? ¿Qué podemos concluir usando un adulto?

**Evidencia bibliográfica.** Gao et al. (2024), apartado 2.2, describe fragmentos de 10 s y GPU Tesla V100, sin establecer mediante comparación una ventana óptima para nuestro subrayado. Yılmaz et al. (2012) actualiza la estimación cada 150 ms y usa tres estimaciones para ciertas recuperaciones (aproximadamente 450 ms): son intervalos de actualización/confirmación de su sistema, no tamaños acústicos que podamos copiar a Whisper.

**Fuentes.** [Gao 2024](https://www.isca-archive.org/interspeech_2024/gao24d_interspeech.pdf), [Yılmaz 2012](https://www.isca-archive.org/interspeech_2012/yilmaz12_interspeech.pdf).

**Decisión.** Usar la bibliografía para diseñar pruebas y elegir parámetros mediante mediciones propias. Separar ventana acústica, intervalo de actualización y ventana textual. Las lecturas adultas sirven para depuración; la configuración infantil necesita evaluación específica.

**Propuesta aún no ejecutada.** Comparar 4, 6, 8 y 10 s con bloque de 2 s; después probar actualizaciones de 1 y 2 s. Añadir lecturas lentas, pausas y relecturas, y una referencia temporal humana. Una actualización cada 2 s ya puede dejar el indicador atrás aunque la inferencia termine antes del siguiente bloque.

## E008 · Registro continuo de decisiones y experimentos

**Fecha:** 14/10/2026.

**Petición del usuario.** Mantener un diario/informe mientras se desarrolla y prueba el sistema, incluyendo novedades, descubrimientos, cambios y experimentación.

**Cambio.** Se crea este diario y se enlaza desde README. Reúne el contexto de desarrollo; las fichas y registros detallados siguen siendo la evidencia de cada experimento.

**Pendiente inmediato.** El usuario debe ejecutar la comparación de ventanas, compartir su resumen y revisar cambios de hipótesis/posición. Su autorización para publicar la versión anterior no se extiende automáticamente a esta nueva versión.

## E009 · Reproducción de la comparación de ventanas por el usuario

**Fecha:** 14/10/2026. Ejecutado por el usuario; resultados comprobados en los JSON locales. Sin autorización nueva para publicar.

**Configuración.** Mismo audio adulto con desviaciones deliberadas; prefijo, ventana de 6 s y ventana de 10 s; actualización cada 2 s. No se cambia el código ni se ejecuta otra inferencia durante esta revisión.

**Evidencia.** Salida completa aportada como texto; [informe de la ejecución del usuario](../resultados/comparaciones/20261014_092131_720136/resumen.md) y tres registros JSON de esa carpeta.

| Método | Inferencia total (s) | Mediana (s) | Inferencias >2 s | Cola máxima simulada (s) |
|---|---:|---:|---:|---:|
| Prefijo | 53,17 | 3,46 | 10/15 | 21,04 |
| Ventana 6 s | 29,51 | 2,10 | 11/15 | 2,15 |
| Ventana 10 s | 33,22 | 2,32 | 10/15 | 4,31 |

**Seguimiento.** Las tres ejecuciones alcanzan el índice 56 al corte de 24 s y no presentan retrocesos. Para cada método, la secuencia de posiciones coincide exactamente con la obtenida en E006 sobre el mismo audio. Es repetibilidad de la salida en este caso, no validación frente a una referencia humana.

**Diferencia respecto a E006.** Los tiempos son mayores en esta ejecución. La ventana de 6 s pasa de cero a once inferencias que superan 2 s y acumula una cola simulada de 2,15 s. No se ha medido carga de fondo, alimentación ni temperatura: no se atribuye la variación a una causa concreta.

**Interpretación.** La ventana de 6 s sigue siendo el candidato de menor coste total y menor cola, pero aún no garantiza sostener actualizaciones cada 2 s. El prefijo tiene menos actualizaciones que superan 2 s que la ventana de 6 s, pero sus excesos son mucho mayores; ese recuento aislado no determina viabilidad.

**Control del silencio final.** Hasta el corte común de 24 s, los costes prefijo/6 s/10 s son 35,47/25,46/27,38 s. La reducción de la ventana de 6 s se mantiene al excluir las actualizaciones posteriores a ese corte, aunque este corte no es una anotación humana de fin de voz.

**Decisión provisional.** Mantener 6 s como candidato, sin declarar el sistema listo para directo. Siguiente propuesta: probar 4 y 8 s con el mismo intervalo de actualización y revisar posición junto con coste; después estudiar configuración del ASR e intervalo de actualización. Falta evaluar pausas, relecturas, textos largos y voces infantiles.

## E010 · Publicación y ampliación del experimento

**Fecha:** 14/10/2026.

**Autorización.** El usuario pide subir la versión probada y hacer el siguiente experimento, permitiendo añadir más ventanas. Se publica la comparación anterior y el diario en `d63d7f1`. La ampliación nueva se mantiene local hasta su revisión.

**Pregunta.** ¿Reducir a 4 s mejora el coste sin perjudicar el seguimiento? ¿Aportan 8 o 12 s contexto útil frente a 6 y 10 s? ¿Cuánto varían los tiempos entre rondas?

**Configuración.** Prefijo completo y ventanas de 4, 6, 8, 10 y 12 s; bloques de 2 s. Dos rondas sobre el audio adulto con desviaciones. Se conservan modelo, CPU int8, VAD y seguidor. Orden aleatorio reproducible, semilla 20261014; ejecuciones secuenciales. Cada ventana conserva solapamiento igual a su duración menos 2 s.

**Cambios.** El comparador permite --ventanas, --repeticiones y --semilla; guarda plan de ejecución, registros individuales y resumen por configuración con medias/rangos. No reutiliza tiempos de pruebas anteriores: vuelve a ejecutar cada candidato bajo el mismo protocolo.

**Comprobaciones.** Pasan trece pruebas automáticas, incluidas integridad/reproducibilidad del plan de rondas y resumen que distingue alcanzar una posición del resultado final tras un retroceso.

**Resultados locales.** Doce ejecuciones completas. Totales medios de inferencia para prefijo/4/6/8/10/12 s: 44,39/24,30/26,92/26,90/28,88/30,03 s. Inferencias superiores al bloque de 2 s: 20/7/10/2/12/14 de 30, respectivamente. Las doce llegan a cuaderno (56) al corte de 24 s sin retrocesos. Cada configuración conserva sus posiciones entre rondas; las ventanas de 4, 6, 8 y 10 s coinciden en todas sus posiciones sobre este audio.

**Aprendizaje.** La ventana de 4 s minimiza el total medio; la de 8 s tiene menos inferencias lentas y menor cola simulada. Hasta el corte común de 24 s, la ventana de 8 s tiene menor coste medio (21,96 s) que 4 (22,49 s) y 6 (23,10 s); el silencio final favorece el total de la ventana más corta. No hay anotación humana temporal ni evidencia para atribuir variación a una causa del ordenador. No interpretar pequeñas diferencias como superioridad estadística.

**Comprobación adicional.** Intervalos y posiciones verificados en 180 actualizaciones. Informe y registros en resultados/comparaciones/20261014_093754_597676; [ficha detallada](../pruebas/05_ventanas_ampliadas.md).

**Decisión provisional.** Conservar 4 y 8 s como candidatos, junto a la referencia de 6 s, y no cambiar el modo predeterminado. La nueva versión queda local para reproducción del usuario. Sin referencia humana temporal; dos rondas no permiten declarar una ventana óptima universal.

## E011 · El usuario amplía a tres rondas

**Fecha:** 14/10/2026. Ejecutado por el usuario; registros locales revisados. Sin nueva autorización para publicar.

**Configuración.** El usuario reproduce la prueba con --ventanas 0 4 6 8 10 12 --repeticiones 3. Mismo WAV adulto de 30 s; 18 ejecuciones, 270 actualizaciones. Son repeticiones de procesamiento del mismo audio, no nuevas lecturas ni nuevos participantes.

**Evidencia.** [Informe del usuario](../resultados/comparaciones/20261014_100148_765908/resumen.md), resumen JSON y dieciocho historiales en esa carpeta.

| Método | Inferencia total media (s) | Rango entre rondas (s) | Inferencias >2 s | Media de cola máxima simulada (s) |
|---|---:|---|---:|---:|
| Prefijo | 44,85 | 43,15–48,09 | 30/45 | 13,73 |
| Ventana 4 s | 22,45 | 21,49–24,25 | 0/45 | 0,00 |
| Ventana 6 s | 24,71 | 23,72–26,17 | 6/45 | 0,14 |
| Ventana 8 s | 26,59 | 25,49–27,30 | 1/45 | 0,09 |
| Ventana 10 s | 28,18 | 27,90–28,58 | 13/45 | 0,28 |
| Ventana 12 s | 30,16 | 28,94–32,23 | 24/45 | 1,62 |

**Seguimiento.** Las dieciocho ejecuciones llegan al índice 56 al corte de 24 s, sin retrocesos en la salida presentada. Se verifican intervalos de audio en 270 actualizaciones. Cada configuración mantiene la misma secuencia de posiciones entre las tres rondas. Las ventanas 4/6/8/10 coinciden en sus posiciones sobre este audio, aunque sus transcripciones difieren.

**Control del silencio final.** Hasta el corte de 24 s, los costes medios prefijo/4/6/8/10/12 s son 31,04/20,80/21,52/21,72/22,89/24,26 s. En esta ejecución 4 s tiene también menor coste hasta ese corte; la ventaja total no procede exclusivamente del silencio final. El corte de 24 s no es una anotación humana de fin de voz.

**Revisión de E010.** La ventana de 4 s no supera 2 s en ninguna de las 45 inferencias de esta ejecución, mientras sí lo hacía en siete inferencias de la comprobación anterior. Las condiciones del ordenador no se han medido; no se atribuye la variación a una causa ni se garantiza ese comportamiento en otras ejecuciones.

**Decisión provisional.** Adoptar 4 s como candidato principal para la siguiente prueba, conservando 8 s como alternativa de mayor contexto y sin modificar todavía el modo predeterminado. Pasar de repetir este audio a añadir lecturas con pausas, ritmo lento y retrocesos, y revisar posición frente a referencia temporal humana.

**Límites.** Tres rondas mejoran la observación de variación de tiempos, pero no añaden diversidad de voz, texto ni errores. Cola cero significa ausencia de espera acumulada antes de las inferencias en la simulación; persisten espera del bloque, inferencia y otras etapas. No prueba latencia visual cero ni precisión infantil. La prueba del usuario no constituye autorización para publicar la nueva versión.

## E012 · Guardar resultados y pasar a nuevas lecturas

**Fecha:** 14/10/2026.

**Autorización.** El usuario pide subir los resultados a GitHub y explicar con qué continuar. Se prepara la publicación de la ampliación configurable, las 12 ejecuciones del desarrollador, las 18 del usuario y el diario actualizado.

**Decisión de siguiente paso.** Comparar ventanas de 4 y 8 s en nuevas lecturas adultas del mismo cuento: ritmo lento, pausa de 8 s y relectura de una frase. Hacer grabaciones separadas para distinguir los efectos. Mantener bloque de 2 s y ASR igual. No modificar aún modelo ni subrayado.

**Objetivo.** Comprobar si el indicador se mantiene durante silencio, retoma posición tras una pausa y representa/repara retrocesos. Revisar los instantes difíciles contra el audio, no solo la posición final. El punto de partida es el [protocolo propuesto](../pruebas/06_protocolo_pausas_relecturas.md).

**Estado.** Protocolo propuesto; audios nuevos y resultados todavía inexistentes. La futura implementación y sus resultados se mantendrán locales hasta revisión y nueva autorización para publicar.

## E013 · Nueva grabación con pausa de unos ocho segundos

**Fecha:** 14/10/2026. Ejecutado por el usuario; salida aportada y JSON locales revisados. Sin autorización nueva para publicar.

**Configuración.** Nuevo WAV adulto lectura_20261014_111454_984161, duración 60 s. El usuario informa una pausa de 8 s tras flor. Ventanas de 4 y 8 s, bloque de 2 s, tres rondas por configuración. Se mantienen ASR, VAD y seguidor.

**Evidencia.** [Informe](../resultados/comparaciones/20261014_111548_094194/resumen.md) y seis historiales JSON de esa carpeta. Los instantes exactos de inicio/fin de pausa no tienen todavía anotación humana.

| Ventana | Total medio inferencia (s) | Rango entre rondas (s) | Inferencias >2 s | Media de cola máxima simulada (s) |
|---|---:|---|---:|---:|
| 4 s | 32,01 | 31,37–32,54 | 12/90 | 0,15 |
| 8 s | 39,60 | 38,72–40,44 | 30/90 | 1,34 |

**Posición observada.** En las seis ejecuciones se mantiene flor (27) en los cortes de 12, 14, 16, 18, 20 y 22 s. En el corte de 24 s se reconoce Ana llamó a su hermano para que pudiera verla y avanza a verla (36). Al corte de 32 s llega a cuaderno (56). No hay retrocesos. Cada ventana reproduce sus posiciones entre rondas; salvo el corte de 10 s (4 s llega a despacio, 8 s queda en voló), las secuencias de ambas ventanas coinciden.

**Interpretación.** No se pierde la posición cuando desaparece la voz del contexto acústico, y ambas ventanas vuelven a localizar la continuación. Esto no permite medir retraso exacto al retomar: los cortes de audio disponible no son tiempos de respuesta visual y falta referencia humana de reanudación.

**Incidencia nueva.** Aparece Suscríbete, ajeno al cuento: con ventana 4 en el corte de 20 s y en 36/38 s, y con ventana 8 en 40/42 s. Se repite en todas las rondas (15 actualizaciones en total). No mueve la posición en estos casos. Sin escuchar esos tramos y confirmar posibles voces de fondo, no se afirma su origen: si no está en el audio, es una alucinación del ASR. El VAD activo no basta en esta ejecución para evitar la salida ajena al cuento. No corregir ni borrar las hipótesis originales.

**Decisión provisional.** Mantener 4 s como candidato principal por menor coste y cola en esta prueba. Se retira cualquier interpretación de que garantice inferencias inferiores a 2 s: aquí 12 de 90 las superan. El largo silencio final influye en estadísticas globales; no confundir media o mediana global con rendimiento durante voz continua.

**Pendientes.** Confirmar por escucha la salida Suscríbete, anotar aproximadamente los límites de pausa/reanudación y continuar con lecturas lenta y con relectura. No se modifica código ni se publica en esta revisión.

## E014 · Revisión humana del ruido de pájaros al final

**Fecha:** 14/10/2026. Confirmación del lector tras escuchar la grabación.

**Observación del usuario.** En el tramo final donde el reconocedor devuelve Suscríbete solo se oye el trino de los pájaros. No hay una persona pronunciando esa palabra en ese tramo, según su escucha.

**Actualización de E013.** La salida Suscríbete del final se clasifica como texto inventado por el ASR sobre audio ambiente con pájaros, respaldado por la revisión humana del usuario. Es una confirmación de ausencia de habla en ese fragmento, no un experimento que aísle causalmente el trino ni una escucha independiente del desarrollador.

**Alcance.** La confirmación se refiere al final: cortes 36/38 s en ventana 4 y 40/42 s en ventana 8. La aparición en el corte de 20 s durante la pausa requiere revisión específica. Estos cortes identifican las ventanas procesadas; no son tiempos humanos del canto ni una localización acústica precisa de la palabra inventada.

**Consecuencia.** El procesamiento con VAD activo ha permitido una salida textual sobre un tramo sin habla humana confirmada por el usuario. El seguidor no movió la posición en esos registros, lo que no garantiza rechazo de otras salidas falsas. Conservar audio e hipótesis originales para futuras pruebas de habla frente a ambiente.

**Pendiente.** Incorporar el final revisado como caso de ruido ambiental al evaluar cambios de detección de voz/ASR. No atribuir qué componente falló ni ajustar umbrales antes de inspeccionar su evidencia. No se modifica código ni se publica en esta entrada.

## E015 · Publicación de la pausa y preparación de lectura lenta

**Fecha:** 14/10/2026.

**Autorización.** El usuario pide guardar en GitHub la prueba de pausa y sus resultados y avanzar a la siguiente. Se prepara la publicación del WAV lectura_20261014_111454_984161, seis ejecuciones, resúmenes, protocolo actualizado y confirmación humana sobre los pájaros.

**Siguiente prueba.** Nueva lectura adulta del mismo cuento a ritmo más lento, sin pausa prolongada, relecturas ni errores deliberados. Orientación: unos 40–50 s para el cuento, sin separar artificialmente cada palabra. Grabar 60 s; si hace falta más, 90 s. Comparar ventanas 4 y 8 s, bloque 2 s, tres rondas, ASR y seguidor sin cambios.

**Pregunta.** ¿La ventana de 4 s aporta suficientes palabras para mantener el seguimiento cuando disminuye el ritmo, o la de 8 s ofrece mejor continuidad? Revisar posiciones e intervalos sin avance durante voz; distinguirlos del silencio final y de falta de evidencia tras una palabra aislada.

**Estado.** Lectura lenta propuesta; aún no hay un nuevo WAV ni resultados. Se registrarán incidencias y desviaciones reales que comunique el usuario. Los nuevos archivos quedarán locales hasta su revisión y autorización para publicar.

## E016 · Informe de utilidad profesional y alcance grupal

**Fecha:** 16/10/2026.

**Petición.** El usuario informa de la finalización de un miniinforme en otro chat y autoriza subir los cambios del proyecto a GitHub.

**Archivos revisados.** Nuevo [informe de necesidades de docentes y logopedas](Investigacion_necesidades_logopedas_docentes.md), cambios en README y ALCANCE. En esta publicación no se verifican de nuevo los estudios citados ni se modifican sus conclusiones.

**Novedad de diseño.** Se documenta como objetivo final una lectura grupal con selección del lector desde la tablet docente, habilitación de un único micrófono y pausa/reanudación de sesión. La interrupción marcada por la profesora se diferencia del silencio del lector; el tiempo de lectura activa se separa del tiempo total. Estas funciones están propuestas, no implementadas.

**Estado técnico.** El prototipo sigue trabajando con un lector y audio local. No se han cambiado los scripts de reconocimiento o seguimiento ni se han generado nuevas pruebas en esta revisión.

**Siguiente prueba pendiente.** Lectura lenta del mismo cuento, sin pausa larga ni errores deliberados: grabar 60 s y comparar ventanas de 4 y 8 s con tres rondas, manteniendo el bloque de 2 s. Después queda la relectura de una frase. Los cambios de alcance no sustituyen estas comprobaciones del núcleo técnico.

## E017 · La lectura lenta expone bloqueo, regresión y pico de coste

**Fecha:** 16/10/2026. Ejecutado por el usuario; registros revisados. Nuevos archivos locales, sin autorización para publicar.

**Configuración y evidencia.** WAV lectura_20261016_095108_269618, 90 s, ventanas 4/8 s, bloque 2 s, tres rondas. [Ficha](../pruebas/07_lectura_lenta.md) e [informe](../resultados/comparaciones/20261016_095252_869489/resumen.md). ASR y reglas sin cambios.

**Resultados.** Ventana 4: total medio 68,74 s, 9/135 inferencias superiores a 2 s, cola máxima media simulada 2,03 s; termina en mariposa (53) sin alcanzar 56. Ventana 8: 93,29 s, 4/135, cola media 22,72 s; alcanza cuaderno (56) al corte de 78 s y retrocede a un (55) al corte de 80 s, al cambiar la hipótesis a en un jugaderno. Estos comportamientos se repiten en las tres rondas.

**Mecanismo observado.** Con 4 s, Después aparece sola en el corte de 62 s: la regla mínima de dos coincidencias mantiene la posición. Pues volvieron tampoco supera los criterios en 64 s. Recupera al aparecer volvieron a casa. Al final, las hipótesis cortas/deformadas no permiten recuperar el final. Con 8 s, dos coincidencias antiguas en un bastan para aceptar una posición anterior tras perder cuaderno en la nueva hipótesis. Falta referencia humana que confirme el movimiento real del lector.

**Pico reproducible.** Ventana 8, audio 2–10 s: 26,21/27,03/20,90 s de procesamiento y salida vacía. No se registra el desglose interno que permita atribuirlo a un componente. La mediana habitual de 1,6–1,8 s y el pequeño número de inferencias lentas ocultan una espera acumulada elevada.

**Otra observación.** La ventana 4 genera y nos vemos en el próximo vídeo hasta la próxima en el corte de 76 s. Texto ajeno al cuento, posible alucinación pendiente de escucha; no extrapolar a esta grabación la confirmación de pájaros del audio anterior.

**Decisión.** Revisar la preferencia por 4 s: ninguna configuración resuelve esta lectura completamente. Mantener el código para terminar la prueba base de relectura. Después comparar reglas que distingan revisiones de retrocesos reales, contexto insuficiente y tratamiento del pico de inferencia; no impedir todos los retrocesos. Registrar posiciones y costes extremos además del resultado final y la mediana.

## E018 · Conservar el fallo de lectura lenta y probar un retroceso real

**Fecha:** 16/10/2026.

**Decisión.** El usuario autoriza publicar la lectura lenta y pasar a la siguiente prueba. Se conservan el WAV y los seis registros originales, incluidos el pico de inferencia, bloqueo en 53 y regresión de 56 a 55. No se cambian todavía reglas ni parámetros para corregirlos.

**Siguiente experimento.** Leer normalmente el mismo cuento, repetir una vez Los dos se quedaron en silencio tras pronunciar ese fragmento, y continuar con mirando sus alas. Grabar 60 s; comparar ventanas 4 y 8 s, tres rondas, bloque de 2 s, mismo ASR y seguidor. No introducir omisiones ni errores deliberados adicionales.

**Pregunta.** ¿El seguidor distingue un retroceso real del lector de una revisión del ASR? Revisar la hipótesis y las posiciones durante la relectura y la recuperación posterior. La actualización cada 2 s puede no representar todos los movimientos de una repetición breve; la ausencia de retroceso visible no basta para afirmar que la repetición no ocurrió.

**Referencia.** El lector confirmará el fragmento realmente repetido y las desviaciones de la prueba. Se necesita escucha temporal para cuantificar precisión y recuperación. La lectura lenta queda como comparación de regresión automática, sin asumir que su retroceso final fue lector.

**Estado.** Prueba de relectura propuesta, todavía sin audio ni resultados. Los nuevos archivos permanecerán locales hasta su revisión y autorización de publicación.

## E019 · Relectura: conservar el intento no equivale a representar su recorrido

**Fecha:** 16/10/2026. Prueba del usuario, JSON revisados. Nuevos archivos locales, sin autorización para publicar.

**Configuración.** WAV lectura_20261016_104151_933317, 60 s. Ventanas 4/8 s, bloque 2 s, tres rondas, mismo ASR/VAD/seguidor. Consigna: repetir Los dos se quedaron en silencio. [Ficha](../pruebas/08_relectura_frase.md) e [informe](../resultados/comparaciones/20261016_104206_415649/resumen.md).

**Resultados.** Totales medios 26,21 s (4 s) y 31,49 s (8 s), 0/90 inferencias superiores a 2 s por ventana y cola simulada cero. Las seis ejecuciones alcanzan cuaderno al corte de 30 s y lo mantienen. Las posiciones se reproducen entre rondas.

**Repetición.** Ambas hipótesis muestran la frase repetida. En cortes de 20/22/24 s, la ventana 4 señala 42/41/45 y la de 8 señala 42/42/45. En 8 s se rechaza la evidencia del corte de 22 s (cuatro coincidencias de ocho, coste cuatro), por lo que conserva la última posición. En 4 s se acepta un retroceso de una palabra, que no demuestra representar todo el retorno al inicio del fragmento. No hay referencia humana temporal para puntuar el recorrido.

**Aprendizaje.** Reconocimiento de la repetición, representación visual de retroceso y evaluación lectora no son equivalentes. Menos retrocesos no significa necesariamente mejor seguimiento; deben distinguirse relecturas reales y regresiones del ASR, como la observada al final de la lectura lenta.

**Decisión.** Primer ciclo de cinco casos adultos completado. Pasar a organizar el banco y añadir referencias humanas literales y temporales antes de modificar reglas o comparar modelos/ayudas. No elegir una ventana definitiva solo por coste o por llegar al final. La posible influencia de ruido al final de la lectura lenta sigue sin comprobarse específicamente; no se extrapola la revisión de pájaros del audio de pausa.

## E020 · Cerrar la base inicial y preparar evaluación con referencia humana

**Fecha:** 16/10/2026.

**Autorización.** El usuario pide subir la relectura y sus resultados y concretar el siguiente trabajo. Se conservan la quinta grabación, las seis ejecuciones y sus resúmenes sin modificar ASR ni seguidor.

**Siguiente fase propuesta.** Catalogar los cinco WAV por caso y configuración. Crear una referencia literal de lo pronunciado, incluyendo repeticiones, fragmentos, autocorrecciones y habla ajena al cuento, y una referencia temporal de palabras/eventos revisada por escucha. Comenzar por un audio para acordar las reglas antes de anotar los demás.

**Criterio.** Las referencias no se obtienen tomando el cuento ni el JSON ASR como verdad. Las ayudas automáticas de transcripción/alineamiento solo podrán ser borradores explícitos y necesitarán revisión humana. Registrar incertidumbre, intervalos de silencio/ruido y pronunciaciones ambiguas sin inventar palabras o tiempos.

**Objetivo.** Poder medir diferencias de transcripción, preservación de intentos, posición y recuperación en tramos revisados; posteriormente calcular retraso con el reloj de disponibilidad simulado, separado de la precisión de posición y de la futura latencia visual. Los tiempos ASR actuales no son referencia temporal humana.

**Decisión.** No seguir eligiendo combinaciones por velocidad y posición final solamente. Preparar primero referencias y métricas, conservar una base sin cambios y después comparar reconocedores y ayudas de audio. Añadir grabaciones nuevas reservadas para comprobar las decisiones, sin presentarlas como independientes si se usan para ajustar parámetros.

**Estado.** Plan propuesto; referencias humanas y evaluador aún pendientes. No se afirma disponer ya de métricas de precisión temporal ni validación infantil.

## E021 · Catalogación y primera plantilla de referencia

**Fecha:** 16/10/2026.

**Objetivo.** Preparar una base común para medir calidad de reconocimiento y seguimiento, empezando por la lectura normal.

**Cambios.** Se crea datos/referencias/catalogo.json con los cinco casos, rutas relativas, SHA-256, duración, frecuencia, canales y tamaño de muestra de los WAV. Se identifica un único adulto y se asignan todos a desarrollo porque ya se han utilizado en las decisiones anteriores. No se presenta ninguna ronda como participante ni un audio usado como prueba independiente.

**Referencia humana.** Se crea lectura_normal.json con texto nulo y estado pendiente, sin importar la salida ASR como verdad. LEEME.md define la revisión literal por escucha y separa validación textual de anotación temporal. No se han inferido palabras ni tiempos humanos.

**Siguiente acción del usuario.** Escuchar los 40 s de la lectura normal y confirmar qué se pronuncia, incluidos comentarios o fragmentos adicionales y ambiente al final. Aún no se piden tiempos por palabra. Se empezará por un audio para fijar reglas antes de extenderlas al resto.

**Estado.** Preparación local; pendiente de revisión del usuario. No hay evaluador de precisión ni nuevas inferencias. Sin publicación.

## E022 · Primera transcripción literal confirmada por escucha

**Fecha:** 16/10/2026.

**Referencia del usuario.** Tras escuchar la lectura normal, confirma que pronuncia exactamente el cuento, sin habla antes ni después. Indica ruido ambiental muy breve al inicio y, aproximadamente desde 23–24 s, silencio con ruido muy leve que apenas se percibe con auriculares.

**Acción.** Se incorpora el texto del cuento como transcripción literal únicamente tras esa confirmación humana. Se registran revisor (usuario/lector), fecha, fuente y observaciones de ambiente. Se verifican los SHA-256 del WAV y del cuento contra el catálogo. La puntuación es editorial y no implica anotación fonética.

**Límites.** Primer ruido sin duración medida: la expresión primer milisegundo se conserva como descripción del usuario, no como un intervalo exacto de 0,001 s. El fin estimado 23–24 s tampoco se usa como etiqueta temporal precisa. Los tiempos por palabra quedan vacíos y pendientes. Revisión del propio lector, no de un anotador independiente; los otros cuatro audios no quedan validados automáticamente.

**Estado.** Una transcripción literal revisada, cero alineamientos temporales humanos. Cambios locales; sin publicación ni nuevas inferencias.

## E023 · Referencia literal con desviaciones y pronunciación ambigua

**Fecha:** 16/10/2026.

**Confirmación humana.** El usuario confirma Ana, Ana, la omisión de despacio y mari… mariposa al final. Describe silencio como pronunciado con poca claridad, aunque comprensible como esa palabra. Informa pájaros intermitentes y ruidos notables de silla y cierre de mochila después de aproximadamente 24 s.

**Acción.** Se crea datos/referencias/lectura_desviaciones.json con texto literal, tres eventos lectores separados e índices del cuento. Se conserva silencio como palabra de referencia con observación de pronunciación, sin asignar etiqueta de error fonético. Se verifica SHA-256 del WAV y se actualiza catálogo. Ruido y palabras quedan separados; sus tiempos humanos no se inventan.

**Aprendizaje metodológico.** La salida cinesio difiere de la referencia lexical del usuario, pero su observación de articulación poco clara impide presentar este caso como pronunciación inequívocamente correcta o usarlo como diagnóstico fonético. El fragmento mari es un intento incompleto que debe preservarse al puntuar disfluencias, aunque un tokenizador pueda extraerlo como texto.

**Estado.** Dos transcripciones revisadas por el propio lector, ninguna anotación temporal humana por palabra. Referencias locales; sin cambios del modelo ni publicación. Pendiente la revisión literal del audio con pausa, seguida de lenta y relectura.

## E024 · Referencia lexical de lectura con pausa

**Fecha:** 16/10/2026.

**Confirmación humana.** El usuario confirma el cuento correcto y la pausa entre flor y Ana llamó. Describe ruido de silla al principio, otro ruido al final del silencio y solo silencio desde aproximadamente el segundo 31.

**Acción.** Se crea datos/referencias/lectura_pausa.json, se verifica la identidad del WAV y se actualiza catálogo. La pausa queda vinculada a los índices 27/28 sin inventar tiempos. La duración de 8 s se conserva como estimación de la consigna y descripción previa, no medición humana.

**Precisión de etiquetas.** Se registra ausencia de habla desde aproximadamente 31 s, pero no silencio acústico absoluto: en la revisión previa del mismo archivo el usuario describía pájaros al final. Se conservan ambas observaciones y su incertidumbre. La ubicación del ruido al final del silencio no se fuerza a un intervalo sin aclaración.

**Estado.** Tres transcripciones literales confirmadas por el lector; tiempos humanos por palabra y límites de pausa pendientes. Faltan las lecturas lenta y repetida. Sin nuevas inferencias, cambios del modelo ni publicación.

## E025 · Revisión humana del fallo final en lectura lenta

**Fecha:** 16/10/2026.

**Confirmación del usuario tras escucha.** Ritmo deliberadamente lento; cuaderno se pronuncia claramente. Desde aproximadamente 1:18 hay silencio con un pequeño ruido de silla, y otro al inicio. La frase y nos vemos en el próximo vídeo es inventada por el ASR: no se pronuncia ni hay habla de fondo. El usuario considera el ruido ambiental poco marcado.

**Consecuencia sobre E017.** La ausencia de cuaderno en la ventana 4 y la pérdida de esa palabra tras reconocerla en ventana 8 son fallos respecto a la palabra final confirmada por el lector. No se explican como omisión lectora. La frase del vídeo pasa de candidata a salida inventada confirmada por escucha del usuario. No se atribuye el fallo a ruido leve sin un experimento controlado; el pico de 2–10 s sigue sin causa identificada.

**Referencia.** Se crea datos/referencias/lectura_lenta.json y se verifica identidad del WAV. Observaciones confirmadas y estimaciones temporales separadas. Se conserva el resto del cuento como borrador, pendiente de confirmación literal explícita de que no hubo otras diferencias. No se rellenan tiempos de palabra ni se puntúa contra el borrador.

**Estado.** Tres transcripciones completas revisadas, una revisión parcial y una pendiente. Sin cambios de código ni publicación.

## E026 · Transcripción lenta completa confirmada

**Fecha:** 16/10/2026.

**Confirmación.** El usuario confirma explícitamente que toda la lectura lenta coincide con el cuento, sin cambios, omisiones ni repeticiones. La lentitud es deliberada.

**Acción.** El borrador se convierte en transcripción literal revisada en lectura_lenta.json y se actualiza catálogo. Se conservan las observaciones previas de ruido, cuaderno y frase inventada del ASR. Los tiempos por palabra permanecen sin anotar.

**Estado.** Cuatro transcripciones completas revisadas por el lector; queda la relectura. Referencias locales, sin publicación ni nuevas inferencias.

## E027 · Relectura confirmada y cierre de referencias literales

**Fecha:** 16/10/2026.

**Confirmación humana.** El usuario confirma una repetición adicional exacta de Los dos se quedaron en silencio y coincidencia del resto con el cuento. Describe esta grabación como la más limpia, sin habla desde aproximadamente 30 s, con un ruido mínimo en los últimos segundos.

**Acción.** Se crea lectura_relectura.json, se verifica SHA-256 y se actualiza catálogo. Se vinculan las dos apariciones al fragmento 37–42 del cuento, conservando el orden de los intentos. La puntuación es editorial; no se inventa duración de la pausa ni tiempos de los intentos.

**Resultado de fase.** Cinco transcripciones literales revisadas por el propio lector. Se separan observaciones de ambiente y pronunciación de los eventos lectores. El banco es de desarrollo, un adulto y un cuento; la confirmación no constituye anotación independiente ni validación infantil.

**Siguiente trabajo.** Preparar anotación temporal asistida, empezando por la lectura normal: escuchar fragmentos y revisar inicios/finales por palabra con posiciones globales. Las referencias temporales solo se considerarán revisadas después de escucha humana; cualquier propuesta automática conservará estado de borrador. Para relecturas, cada intento debe mantener índice de cuento e intervalo propio.

**Estado.** Referencias locales, sin publicación. Cero alineamientos temporales humanos completos y ninguna nueva inferencia en esta revisión.

## E028 · Reproductor de revisión temporal de la lectura normal

**Fecha:** 16/10/2026.

**Objetivo.** Revisar tiempos por escucha, empezando por una frase para fijar el flujo antes de anotar todo el cuento.

**Implementación.** scripts/anotar.py sirve una interfaz local en 127.0.0.1. Reproducción del WAV original, velocidad, selección de palabra, contexto, repetición, onda general/ampliada, edición de inicio/fin, notas y estado de revisión. Primer alcance: lectura normal, palabras 1–9 de la primera frase.

**Borrador explícito.** Los tiempos ASR se ofrecen opcionalmente solo cuando las palabras coinciden con el texto humano. Cargarlos no marca revisión. Cambiar límites desmarca la palabra. La procedencia ASR se conserva por palabra; esta ayuda puede introducir sesgo de anclaje y requiere escucha y posterior comprobación, idealmente independiente.

**Datos.** Anotaciones guardadas en datos/anotaciones/lectura_normal.json, con copias de seguridad y validación de identidad, límites y orden. Los JSON de referencia literal y ASR permanecen intactos. Se rechazan tiempos inválidos, palabras alteradas y revisiones sin tiempos. La interfaz todavía no representa los intentos múltiples de otras grabaciones.

**Comprobaciones.** Pasan 17 pruebas automáticas. En navegador se comprueban carga/onda, borrador, reproducción, guardado y recuperación. Se guarda un borrador técnico con cero palabras revisadas; no se presenta ninguna marca como humana. El programa no puede comprobar la escucha: esa revisión depende del usuario.

**Estado.** Herramienta y referencias locales, sin publicación. Siguiente tarea: el usuario revisa por escucha las palabras Una mañana Ana salió al jardín de su casa, guarda y comunica si los límites son cómodos o ambiguos. La visualización de centésimas no implica precisión acústica de centésimas.

## E029 · Reproducción a 0,4× para revisar límites

**Fecha:** 19/10/2026.

**Cambio.** Se añade 0,4× al selector de velocidad del anotador a petición del usuario, para facilitar la escucha de inicios y finales. Utiliza el control de velocidad existente; los tiempos de anotación siguen referidos al audio original. Opción comprobada en el HTML y conectada al manejador existente de playbackRate; pendiente de comprobación por escucha del usuario. Cambio local, sin publicación.

## E030 · Revisión temporal completa de la lectura normal

**Fecha:** 19/10/2026.

**Resultado.** El usuario termina la revisión por escucha y quedan guardadas 56/56 palabras en datos/anotaciones/lectura_normal.json. Primera palabra: 1,79–2,00 s; última: 22,36–22,94 s. Nueve palabras conservan notas sobre dificultad para separar límites.

**Comprobación.** Workspace.current() valida identidad del audio y texto, número e índices de palabras, límites, orden y estados de revisión sin errores. Esta comprobación es estructural; no sustituye una segunda escucha ni demuestra precisión acústica. Se conserva la procedencia de los tiempos propuestos por ASR y ajustados por el usuario.

**Decisión.** Usar esta anotación como referencia de desarrollo revisada por el lector, con límites ambiguos identificados. No exigir anotación exhaustiva de todos los audios: priorizar intervalos representativos y eventos críticos, indicando la cobertura evaluada. Siguiente paso: comparar las posiciones del seguimiento con esta referencia y distinguir desfase del seguimiento y demora de procesamiento. Datos locales, sin publicación.

## E031 · Publicación de anotaciones y primera evaluación temporal

**Fecha:** 19/10/2026.

**Publicado.** Commit 664893e en origin/main: anotador, referencias literales, catálogo, 56 palabras revisadas y diario hasta E030. Antes de publicar pasan las 17 pruebas existentes.

**Nuevo experimento local.** Lectura normal, ventanas 4/6/8 s y tres rondas, mismos parámetros del seguidor. Registros en resultados/comparaciones/20261019_084114_510023. scripts.evaluar_seguimiento lee explícitamente la anotación validada y genera evaluacion_humana.json/md, con huellas de los registros y la anotación. Protocolo: pruebas/09_evaluacion_temporal.md. Pasan 20 pruebas, incluidas fronteras de palabras, separación de cola/silencio y rechazo de identidad o revisión incorrectas.

**Métricas.** Referencia: última palabra terminada. Once cortes durante la lectura por ejecución; se excluye silencio posterior. Error absoluto medio de hipótesis, en palabras: 4 s = 0,45; 6 s = 0,36; 8 s = 0,36. Error absoluto medio de posición visible simulada en esos mismos cortes: 5,45 / 6,91 / 6,73 palabras. Demora media hasta mostrar la palabra final simulada: 3,40 / 3,36 / 4,45 s. Todas las ejecuciones llegan a 56. Totales medios de inferencia: 23,83 / 26,63 / 29,92 s por audio de 40 s; estos totales incluyen silencio y no son latencia.

**Interpretación.** Las hipótesis están próximas a la referencia en esta lectura, pero actualización por bloques y cómputo añaden retraso. Diferencias de 0,09 palabras entre ventanas en solo once cortes no permiten declarar una ganadora. La primera ronda presenta más carga de cómputo; no se ha monitorizado su causa. 4 s conserva menor coste y menor error visible medio; 6 s tiene demora final media ligeramente menor. La evaluación secuencial no mide pantalla ni carga inicial del modelo. Lectura única, adulto, referencia asistida por ASR y revisada por el propio lector; nueve límites ambiguos.

**Siguiente paso.** Revisar fragmentos críticos de pausa, lectura lenta y relectura con representación de intervalos e intentos adecuada antes de comparar ayudas de audio. No exigir otra anotación exhaustiva. Nuevo evaluador y experimento se conservan locales para revisión; no están en el commit publicado.

## E032 · Publicación de la evaluación y revisión selectiva por eventos

**Fecha:** 19/10/2026.

**Publicado.** Commit d803551 en origin/main: evaluador de lectura normal, protocolo, nueve ejecuciones de 4/6/8 s y comparación con marcas humanas.

**Nuevo cambio local.** El anotador admite --caso pausa, lenta y relectura. Se revisan respectivamente tres palabras clave, cuatro palabras clave y dos intentos de una frase más la palabra siguiente. Las frases repetidas conservan el mismo rango del cuento y distinto intento, con intervalos cronológicos propios. No se propone una posición palabra por palabra dentro de las frases. Los tiempos comienzan vacíos y las ventanas de orientación solo permiten navegar; no se validan automáticamente.

**Datos y cobertura.** Archivos separados con sufijo _fragmentos.json y copias de seguridad por caso. Estado y contador específicos de intervalos seleccionados; completar la lista no equivale a anotar todo el audio. Se conserva sin cambios la anotación normal de 56 palabras. No se ejecuta todavía evaluación de eventos, pendiente de marcas humanas.

**Comprobación.** Pasan 23 pruebas automáticas, incluyendo separación de archivos, guardado/recuperación, intentos repetidos con índices del cuento iguales y tiempos ordenados. app.js supera node --check. Nuevo modo pendiente de revisión visual y escucha del usuario. Servidor de pausa preparado en puerto 8767.

**Siguiente acción del usuario.** Marcar flor antes de la pausa, Ana al retomar y cuaderno al final, revisar por escucha y guardar. Después calcular duración de la pausa y revisar el comportamiento del seguimiento en ese intervalo. Esta extensión permanece local.

## E033 · Pausa medida con tres anclas humanas

**Fecha:** 19/10/2026.

**Referencia.** El usuario completa flor (11,37–11,88 s), Ana al retomar (21,20–21,50 s) y cuaderno (30,47–30,99 s). Se valida identidad y orden mediante EventWorkspace.current(). Cobertura parcial de tres palabras, sin interpolación de tiempos del resto del cuento. Pausa sin lectura: 11,88–21,20 s, duración 9,32 s; no equivale a ausencia de ruido.

**Evaluación local.** scripts.evaluar_pausa contrasta los seis registros existentes en resultados/comparaciones/20261014_111548_094194 con estas anclas y guarda evaluacion_pausa.json/md con huellas de los archivos y de la anotación. No se ejecutan nuevas inferencias. Pasan tres pruebas nuevas: límites del intervalo, separación de salida visible/corte, datos incompatibles, referencia sin revisar y ausencia de avance/final.

**Resultado.** En cada ejecución, posición de hipótesis 27 en los cinco cortes 12/14/16/18/20 s, concordantes con flor durante la pausa: 30/30 muestras entre las seis ejecuciones. La posición visible simulada coincide en 3/5 cortes por ejecución salvo una con 4/5, debido al retraso de procesamiento al inicio de la pausa. Primer avance tras retomar: corte 24 s, posición 36 en las seis ejecuciones; salida lista entre 4,29 y 4,53 s después del final humano de Ana. Esta demora no mide detección exacta de Ana ni precisión temporal de verla, que no está anotada. Primer corte con cuaderno: 32 s, con demora final simulada de 2,86–4,23 s respecto a 30,99 s. Todos los cortes posteriores al final mantienen 56.

**Interpretación.** El seguidor mantiene la posición durante la pausa en las muestras observadas y recupera el avance después, con demora. Mantener la posición no implica que el texto ASR esté libre de invenciones. Las hipótesis no vacías pueden incluir audio anterior por solapamiento; no se atribuyen automáticamente a habla en la pausa. Solo tres anclas permiten estas métricas de evento, no un error medio de posición en todo el cuento.

**Siguiente paso.** Revisar cuatro anclas del audio lento: Después, mariposa de la última frase, un y cuaderno. Servidor preparado en puerto 8768. Extensión, anotación y evaluación nuevas permanecen locales.

## E034 · Lectura lenta: final humano y retroceso del seguidor

**Fecha:** 19/10/2026.

**Referencia.** Cuatro intervalos manuales revisados y validados estructuralmente: Después 59,38–61,42 s; mariposa de la última frase 70,40–72,73 s; un 74,26–75,01 s; cuaderno 75,14–77,34 s. Se conservan en lectura_lenta_fragmentos.json como cobertura parcial.

**Evaluación local.** scripts.evaluar_lenta contrasta las seis ejecuciones de resultados/comparaciones/20261016_095252_869489 y guarda evaluacion_lenta.json/md con procedencia y huellas. No se ejecutan nuevas inferencias. Entre anclas se calculan cotas de posición según palabras terminadas, sin interpolar el resto. Las cotas pueden coincidir: por ejemplo, en el corte 76 s la última palabra terminada es un (55). Tras 77,34 s la referencia final es 56. Pasan dos pruebas nuevas que verifican cotas sin interpolación y que una llegada al final no oculte un retroceso posterior.

**Resultados.** En las tres rondas de 4 s, Después está terminada en el corte 62 s pero el seguidor mantiene 45; lo mismo en 64 s, aunque la hipótesis ya contiene Después o Pues volvieron. En 66 s salta a 49; las anclas no permiten precisar el instante real de las palabras intermedias. En el corte 76 s la referencia exacta es 55 y la hipótesis del seguidor mantiene 53. Después del final humano, las siete actualizaciones 78–90 s se mantienen en 53: no se llega a cuaderno.

**Ventana de 8 s.** En las tres rondas llega a 56 en el corte 78 s y retrocede a 55 desde 80 s hasta el final. Este retroceso es incompatible con el final humano y con la revisión previa que descarta una relectura en ese momento. La salida del corte 78 estaría lista entre 9,05 y 18,73 s después de terminar cuaderno según la cola simulada; alcanzar el final en el audio no equivale a mostrarlo inmediatamente. La causa del coste de cómputo y del retroceso no queda aislada por estas anclas.

**Interpretación.** Se confirma un fallo de seguimiento al final, no una omisión del lector. Reconocer parte de una palabra antes de su final anotado puede producir adelantos respecto a la convención sin ser necesariamente un fallo del ASR. No calcular precisión global a partir de cuatro palabras. No eliminar todos los retrocesos antes de revisar una relectura real.

**Siguiente paso.** Marcar los dos intentos completos de Los dos se quedaron en silencio y mirando después del segundo intento. Caso relectura preparado en puerto 8769. Cambios y resultados nuevos locales, sin publicación.

## E035 · Relectura contrastada con ambos intentos humanos

**Fecha:** 19/10/2026.

**Referencia.** Usuario revisa primer intento de Los dos se quedaron en silencio (17,54–19,84 s), segundo intento (20,36–22,77 s) y mirando (22,91–23,29 s). Intervalo entre intentos: 0,52 s. Guardado validado por EventWorkspace.current(); las seis palabras interiores no tienen tiempos humanos individuales.

**Evaluación local.** scripts.evaluar_relectura reutiliza las seis ejecuciones existentes de resultados/comparaciones/20261016_104206_415649; genera evaluacion_relectura.json/md con huellas y fases por corte. No se ejecutan nuevas inferencias. Pasan tres pruebas nuevas para fronteras de fase, salida diferida respecto al corte y rechazo de registros incompatibles o intentos sin revisar.

**Resultado.** Solo hay un corte de audio dentro del segundo intento: 22 s. Secuencia 20→22→24 s: posición 42→41→45 en 4 s y 42→42→45 en 8 s, repetida en las tres rondas. El retroceso de una palabra con 4 s es compatible con relectura, pero no demuestra seguirla desde el inicio ni reconstruir todos sus pasos. Su salida estaría lista a 23,65–23,72 s, después del final humano del segundo intento (22,77 s). Ninguna salida con movimiento negativo queda lista durante el segundo intento en la simulación. El ASR conserva evidencia textual de dos intentos; esto no equivale a seguimiento temporal correcto.

**Decisión.** Se cierra la primera revisión de eventos con cobertura selectiva. Balance en pruebas/10_revision_eventos.md. No se eliminan todos los retrocesos ni se declara una ventana óptima. Siguiente trabajo: estudiar evidencia escasa de habla lenta, posición provisional/respaldada y coste de actualización en experimentos separados, conservando la comparación inicial. No se piden más marcas humanas en esta fase. Nuevos resultados y cambios locales, sin publicación.

## E036 · Cierre del primer bloque de evaluación y escaleta

**Fecha:** 19/10/2026.

**Cambio.** Se reúne la revisión selectiva de pausa, lenta y relectura, sus anotaciones, evaluadores, informes y pruebas para publicación autorizada por el usuario. La batería completa pasa 31 pruebas. Se corrige una prueba que dependía del estado de progreso real: ahora comprueba una plantilla inicial independiente de las anotaciones del lector, sin alterar sus datos.

**Plan.** docs/RUTA_TRABAJO.md registra el estado de los ocho bloques, la comparación posterior de modelos/ejecución, ayudas de audio y entornos, y el alcance aún pendiente en directo y aula. Primer bloque de evaluación cerrado con alcance limitado a desarrollo adulto; no se declara validación infantil ni una ventana óptima.

**Siguiente experimento propuesto.** Aislar una mejora de aceptación de evidencia escasa para lectura lenta mediante reproducción de hipótesis ya guardadas. Conservar el seguidor actual y comprobar normal, desviaciones, pausa, lenta y relectura antes de adoptar el cambio. Reutilizar tiempos ASR no produce nuevas medidas completas de rendimiento. No se implementa aún la variante en esta entrada.

## E037 · Primer cambio aislado del seguidor: palabra consecutiva

**Fecha:** 19/10/2026.

**Objetivo.** Aceptar evidencia escasa de lectura lenta sin cambiar ASR, ventanas, VAD ni tiempos de entrada. Se añade scripts.comparar_seguidores con una variante separada del Tracker habitual. Una hipótesis de una única palabra puede avanzar una posición si tiene al menos cinco caracteres, coincidencia exacta única en la ventana local y corresponde a la siguiente palabra del cuento. La decisión no usa tiempos humanos ni etiquetas del caso; el umbral es provisional.

**Método.** Reproducción de 36 registros de normal, desviaciones, pausa, lenta y relectura. El original reproduce posición, movimiento y modo de los 36 sin diferencias. La variante conserva la política de hipótesis sin cambios y los retrocesos multiword. Se reutilizan tiempos ASR/cola; el tiempo propio del seguidor se mide aparte y no se presenta como latencia total nueva. Fuentes y anclas con huellas en resultados/seguidores/20261019_104824_848649/resumen.json. Protocolo en pruebas/11_palabra_aislada.md.

**Resultado.** Regla activada en Después, corte 62 s de las tres rondas lentas de 4 s. Posición 46 en lugar de 45 en 62/64 s; ambas versiones coinciden de nuevo en 49 desde 66 s. La ancla humana sitúa el final de Después en 61,42 s. No cambia ninguna posición de las otras 33 ejecuciones. Final lento sin resolver: 53 en 4 s y 55 en 8 s. Sin nuevas grabaciones ni inferencias. Pasan las 35 pruebas automáticas.

**Decisión.** Mejora localizada; mantener como variante experimental, sin sustituir seguir.py. No se demuestra generalización ni ausencia de avances falsos ante una palabra inventada que coincida con la siguiente palabra del cuento. Siguiente intervención separada: estabilidad tras llegar al final y preservación de relecturas reales.

**Organización.** Se retira docs/RUTA_TRABAJO.md por petición del usuario para que desaparezca del repositorio en la próxima actualización. Las decisiones técnicas de este experimento permanecen documentadas. Cambios y resultados locales, sin publicación.

## E038 · Diagnóstico reproducible del retroceso cuaderno→un

**Fecha:** 19/10/2026.

**Comprobación compartida previa.** El usuario ejecuta comparar_seguidores y confirma la mejora localizada de Después (45→46 en 62/64 s, tres rondas de 4 s), sin cambios de posiciones en los otros registros. Solicita estudiar la causa del retroceso del final antes de corregirlo.

**Diagnóstico.** Nuevo comando scripts.diagnosticar_retroceso muestra cortes 76–86 s y comprueba reproducción exacta de posiciones, movimientos y modos de las tres rondas lentas de 8 s. En 78 s, hipótesis mariposa en un cuaderno lleva a 56; en 80 s, en un jugaderno produce dos coincidencias de tres (66,7%) y coste 1/3 (33,3%), aceptables para locate. La última coincidencia exacta es un (55); Tracker.update reemplaza 56 sin exigir evidencia adicional de relectura. Después las hipótesis no recuperan cuaderno y mantiene 55.

**Audio y límites.** Las ventanas 70–78 y 72–80 s contienen cuaderno completo según la marca humana 75,14–77,34 s. Son reconocimientos solapados, no evidencia de volver a pronunciar un. Se explica la decisión del seguidor; no se determina por qué el ASR cambia cuaderno por jugaderno ni se atribuye a ruido. Se distingue corte de audio de salida en pantalla.

**Evidencia y estado.** Protocolo y comando para el usuario en pruebas/12_diagnostico_retroceso.md. Pasan dos pruebas nuevas del mecanismo. El diagnóstico solo lee registros; no ejecuta ASR ni cambia seguir.py o la variante anterior. Pendiente de comprobación del usuario en su terminal. Sin publicación ni corrección nueva en esta entrada.

## E039 · Variante temporal para retrocesos sobre audio solapado

**Fecha:** 19/10/2026.

**Revisión compartida.** El usuario ejecuta diagnosticar_retroceso y reproduce el cambio 56→55 al pasar de cuaderno a jugaderno, así como las coincidencias 2/3 y coste 1/3. Se prueba una corrección separada, no una combinación con la regla de palabra aislada.

**Implementación.** TemporalBacktrackTracker conserva una marca máxima de final ASR de la última coincidencia exacta aceptada. Solo permite retroceder si la coincidencia del candidato aporta un final ASR posterior. Se usa el recorrido del alineamiento para identificar el token que respalda la posición. locate añade una opción diagnóstica, desactivada por defecto; la regla del Tracker habitual no cambia. Se conserva también la política de no reconfirmar texto idéntico.

**Experimento.** comparar_seguidores --variante temporal reproduce los 36 registros y confirma exactitud de la reproducción original. Resultados en resultados/retrocesos/20261019_110452_881233; protocolo pruebas/13_proteccion_temporal_retrocesos.md. No hay nuevas inferencias. Los tiempos ASR/cola siguen reutilizados; se mide el tiempo del seguidor por separado.

**Resultado.** Tres rondas lentas de 8 s: en el corte 80 s se rechaza posición 55 apoyada por un con fin ASR 74,66 s, anterior al apoyo aceptado de cuaderno con fin ASR 77,26 s. Conserva 56 en los seis cortes 80–90 s, en lugar de 55. La primera llegada a 56 sigue en 78 s. Sin cambios de posiciones en los otros 33 registros; se conserva el pequeño retroceso de la relectura de 4 s. Lectura lenta de 4 s sigue terminando en 53. Pasan las 42 pruebas automáticas.

**Límites y estado.** Timestamps estimados, sin tolerancia ni prueba de nueva voz; pueden permitir retrocesos falsos o frenar reales si son erróneos. Texto idéntico con tiempos distintos sigue sin actualizarse. Datos de desarrollo usados para diseñar la regla; no demuestra generalización ni seguimiento completo de relectura. Variante separada, pendiente de comprobación del usuario antes de decidir incorporación. Cambios locales sin publicación.

## E040 · Comprobación del usuario de la variante temporal

**Fecha:** 19/10/2026.

**Evidencia.** El usuario ejecuta comparar_seguidores --variante temporal y comparte la salida de resultados/retrocesos/20261019_111048_743268. En las tres rondas lentas de 8 s se rechaza el retroceso en 80 s y se mantiene 56 en los seis cortes 80–90 s, frente a 55 del original. No cambian las posiciones de los otros 33 registros. Lectura lenta de 4 s sigue en 53. La relectura mantiene su comportamiento anterior; no se presenta como resuelta.

**Decisión.** Comprobación compartida de esta mejora localizada sobre los mismos datos de desarrollo. La variante permanece experimental, sin activar en el seguidor habitual ni publicar. Siguiente comparación propuesta: original, palabra aislada, protección temporal y ambas juntas, para estudiar interacción antes de integrar. No se requieren nuevas grabaciones para esa reproducción; los tiempos ASR seguirán siendo reutilizados.

## Formato de futuras entradas (plantilla)

### E041 · Título del siguiente cambio o experimento

- Fecha y estado: propuesta / implementado / probado localmente / revisado por el usuario / publicado.
- Objetivo o pregunta.
- Cambio y configuración, incluyendo qué varía y qué permanece igual.
- Datos utilizados y procedencia de la referencia.
- Evidencia: comandos, registros, informe y commit si existe.
- Resultados medidos y observaciones del usuario.
- Interpretación y limitaciones.
- Decisión: provisional o confirmada, con motivo.
- Próximo paso y comprobaciones pendientes.

Este último bloque es una plantilla, no un experimento ya realizado.
