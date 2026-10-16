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
- Pendientes: lecturas lenta y con relectura, y referencia temporal de posición.
- Publicación autorizada: prueba de pausa, WAV, resultados y diario hasta E015. El commit de esta entrega se consulta en el historial de Git.
- Próximo trabajo local: lectura lenta del mismo cuento, comparando ventanas de 4 y 8 s; todavía no ejecutada.
- Candidato principal provisional: ventana de 4 s tras la reproducción del usuario; conservar 8 s como alternativa con más contexto y 6 s como referencia. Actualización cada 2 s. El modo por defecto sigue siendo prefijo completo.
- No implementados: subrayado visual, captura con seguimiento en directo y diagnóstico fiable de errores lectores.
- Datos actuales: tres lecturas de un mismo adulto (normal, desviaciones y pausa), con un cuento de 56 palabras. No permiten conclusiones sobre lectura infantil ni generalización a otros textos.

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

## Formato de futuras entradas (plantilla)

### E017 · Título del siguiente cambio o experimento

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
