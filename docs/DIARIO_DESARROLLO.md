# Diario de desarrollo y experimentación — Lexia

Proyecto de prácticas y TFG de lectura asistida en español.

Inicio del diario: 14 de octubre de 2026, zona horaria Atlantic/Canary. Las primeras entradas se reconstruyen a partir de la conversación, las fichas de pruebas, los registros y los commits. Las horas de los nombres de archivo se conservan como identificadores, sin asumir que corresponden a la hora local del usuario.

## Cómo se mantiene

Se añadirá una entrada tras cada cambio relevante, experimento, incidencia o decisión. Cada entrada recoge objetivo, cambios/configuración, evidencia, interpretación, límites y siguiente paso. Los resultados comunicados por el lector se distinguirán de las comprobaciones automáticas y de las hipótesis del desarrollador.

Las conclusiones provisionales se revisarán mediante entradas nuevas que enlacen las anteriores. No se borrarán observaciones porque después cambie el método. Se conservarán configuraciones y archivos para reproducir las pruebas.

El diario se actualiza durante el trabajo, sin necesitar una petición nueva para cada entrada. Primero se prueba localmente, después el usuario revisa los cambios y finalmente autoriza su subida a GitHub. No se publican cambios por el mero hecho de anotarlos aquí.

## Estado del proyecto a 21/10/2026

- Implementados: grabación/transcripción local, alineamiento, seguimiento simulado, comparaciones de ventanas/reglas, anotación humana y evaluación temporal, explorador acústico, métricas de cómputo y catálogo de audios con nombres legibles.
- Dataset actual: diez grabaciones, 8,5 minutos, un adulto y dos textos, todas utilizadas en desarrollo. Referencias literales y temporales tienen cobertura distinta; los tiempos del ASR no sustituyen revisión humana. No existe test final reservado.
- La recuperación exacta aporta mejoras en tres relecturas grabadas de dos cuentos y no introduce retrocesos en los controles normales observados. Sigue experimental, sin activar en seguir.py; quedan problemas y generalización por comprobar.
- Pasan 66 pruebas. Última publicación 30c4c83; los cambios posteriores permanecen locales. Diario alternativo excluido de Git.
- Prioridad: consolidar un dataset documentado, reservar nuevo material y comparar sistemas sobre idénticos audios/referencias. Ficha Common Voice revisada, sin descargar. Pendiente de revisión compartida la evaluación temporal de rojo del segundo cuento.
- Recursos nuevos instrumentados; los históricos no medidos permanecen como tales. Sin medición de latencia visual ni energía específica/batería en tablets. No hay configuración definitiva ni validación infantil.

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

## E041 · Comparación de las mejoras aisladas y combinadas

**Fecha:** 19/10/2026. Primera comparación; la reproducción del usuario se registra en E042.

**Pregunta.** ¿La combinación conserva los avances de palabra aislada y protección temporal, o aparecen efectos adicionales al aplicarlas juntas?

**Configuración y método.** Se comparan original, palabra aislada, protección temporal y combinación sobre los mismos 36 registros. Son 144 reproducciones de seguimiento, no grabaciones ni participantes nuevos. Se verifican posiciones, movimientos y modos del original. Se mantienen hipótesis, ventanas, cortes y parámetros; no se ejecutan inferencias nuevas. Los tiempos ASR/cola se reutilizan, mientras el coste propio del seguidor se mide aparte.

**Implementación.** La envoltura temporal llama a la regla de palabra aislada y conserva también el respaldo temporal de sus avances. Se comprueba ese enlace con una secuencia sintética que aplica ambas reglas y después vuelve atrás con evidencia posterior. Las trazas compactas identifican la fuente original por huella sin duplicar sus hipótesis.

**Resultado en grabaciones.** Con 4 s, la combinación mantiene la mejora 45→46 en los cortes 62/64 s de las tres rondas lentas, aunque su final sigue siendo 53. Con 8 s, conserva 56 en los seis cortes 80–90 s y termina en 56, igual que la protección temporal aislada; original y palabra aislada terminan en 55. No cambian posiciones de normal, desviaciones, pausa o relectura. No se mejora todavía la demora del seguimiento de la frase repetida.

**Interacción y límite descubierto.** No aparecen posiciones nuevas exclusivas de combinar reglas en los registros. Sin embargo, un control sintético de relectura lejana muestra que, tras conservar 14 en vez de 13, mirando sus alas hacia posición 3 deja solo alas dentro de la ventana local. Original y palabra aislada aceptan 3; temporal y combinación mantienen 14 en esa actualización. El candidato no supera la búsqueda local antes de comprobar sus tiempos. El límite afecta ya a la regla temporal aislada; no surge únicamente de la combinación. No se había evaluado aún la recuperación global con hipótesis posteriores.

**Decisión.** Mantener la combinación experimental y analizar la recuperación fuera de la búsqueda local. No observar posiciones nuevas por interacción no demuestra independencia de las reglas ni ausencia universal de regresiones. No se activa aún en el seguidor habitual ni se mide latencia real nueva. El commit c99035d conserva los experimentos previos; este experimento posterior sigue local.

**Evidencia.** scripts/comparar_combinacion.py, pruebas/14_combinacion_reglas.md y resumen.json/md de ambas ejecuciones.

## E042 · Comprobación del usuario de ambas reglas juntas

**Fecha:** 19/10/2026.

**Comprobación del usuario.** Ejecuta comparar_combinacion y comparte resultados/combinacion/20261019_112218_565950, reproduciendo tanto las mejoras de las grabaciones como el control negativo. La primera comparación y sus huellas se conservan en resultados/combinacion/20261019_112016_077915. Pasan 45 pruebas automáticas.

**Resultado compartido.** Se conservan las mejoras de Después en 62/64 s con ventana de 4 s y de cuaderno en 80–90 s con 8 s. No cambian las posiciones de normal, desviaciones, pausa o relectura. El usuario también reproduce el control sintético: original 3, palabra aislada 3, temporal 14 y combinación 14.

**Decisión.** Mantener la combinación experimental y estudiar la recuperación de una relectura que queda fuera de la zona local. La ausencia de nuevas posiciones exclusivas de combinar reglas en las grabaciones no elimina ese límite. Sin nuevas grabaciones ni publicación en esta revisión.

## E043 · Diagnóstico de búsqueda global y confirmación de recuperación

**Fecha:** 19/10/2026. Cuatro secuencias sintéticas reproducidas por el usuario.

**Objetivo.** Explicar cuándo recupera la combinación una relectura que queda fuera de la ventana local, sin corregir todavía ninguna regla.

**Mecanismo.** Desde 14, la búsqueda local abarca 3–14 y solo encuentra una coincidencia de mirando sus alas (1–3). La consulta global encuentra 3/3 y candidato 3, pero el algoritmo exige dos fallos locales procesados para consultarla. Su primer candidato queda pendiente hasta que otra actualización procesada proponga el mismo índice. Un candidato local aceptado puede recuperar directamente y reiniciar los fallos. Solo se procesan textos distintos: timestamps posteriores con texto idéntico no llegan al filtro temporal.

**Controles y resultado.** A: texto y tiempos repetidos mantiene 14 en las tres propuestas. B: el mismo texto con tiempos posteriores también mantiene 14. C: frase creciente recupera por búsqueda local a 5 en el tercer paso, después de guardar candidato global 4 en el segundo. D: textos distintos construidos para el candidato 3 recuperan globalmente a 3 en el tercero, con respaldo temporal posterior. El diagnóstico verifica posiciones y modos contra replay en las cuatro secuencias, doce propuestas en total. La consulta global adicional que se imprime para explicar el resultado no modifica el seguimiento.

**Comprobación compartida.** El usuario ejecuta diagnosticar_recuperacion y aporta la salida completa de los cuatro casos, confirmando la diferencia entre encontrar una frase globalmente y aceptar su candidato. El comando solo lee registros y construye secuencias: no escribe archivos ni ejecuta ASR.

**Interpretación y límites.** No afirmar bloqueo permanente: la recuperación depende de las hipótesis siguientes. Son propuestas construidas, no grabaciones ni segundos de latencia. Dos textos diferentes tampoco prueban dos eventos independientes de habla. La política de texto idéntico evita confirmar repetidamente el mismo texto en silencio, pero también puede impedir examinar nueva información temporal.

**Decisión.** Probar por separado una recuperación adelantada con coincidencia global exacta, inequívoca y temporalmente posterior. No ampliar la ventana solo para hacer caber el ejemplo ni tratar la repetición del mismo texto como confirmación independiente. No se introduce una corrección en este diagnóstico.

**Evidencia.** scripts/diagnosticar_recuperacion.py y pruebas/15_diagnostico_recuperacion.md.

## E044 · Recuperación anticipada por frase exacta única y posterior

**Fecha:** 19/10/2026. Primera comparación de la variante; revisión posterior del usuario en E045.

**Pregunta y cambio.** Evitar la espera de recuperación cuando la búsqueda local falla pero hay evidencia global especialmente clara. ExactRecoveryTracker se añade sobre la combinación sin activarse en el seguidor habitual. Examina la cola completa de 3–8 palabras: deben coincidir exactamente como secuencia consecutiva, aparecer una sola vez en todo el cuento y conducir a una posición anterior. Sus tiempos ASR deben estar ordenados y no solaparse entre palabras; el inicio de la frase no debe ser anterior al respaldo aceptado y su final debe ser posterior. Si no cumple todo, conserva la combinación anterior. No usa tiempos humanos para decidir ni modifica la política de texto idéntico.

**Método y evidencia.** comparar_recuperacion contrasta original, combinación y nueva variante sobre los mismos 36 registros y verifica reproducción del original. No ejecuta inferencias ni grabaciones nuevas. Los tiempos ASR/cola se reutilizan y el tiempo propio del seguidor se mide aparte. Código, fuentes y anotaciones se identifican por huellas; se guardan informes y trazas compactas. Primera ejecución en resultados/recuperacion/20261019_120146_079995.

**Resultado en grabaciones.** La nueva recuperación no se activa y no cambia ninguna posición frente a la combinación en los 36 registros. Se conservan sus mejoras previas y sus fallos pendientes: lenta de 4 s termina en 53 y no se mejora la demora de la relectura. No hay todavía un ejemplo positivo grabado de esta nueva vía.

**Controles sintéticos positivos.** A/B pasan de 14/14/14 a 3/3/3; C, frase creciente, de 14/14/5 a 3/4/5; D, textos distintos para el mismo candidato, de 14/14/3 a 3/3/3. Se recupera desde la primera propuesta y los siguientes avances pueden seguir por la búsqueda local. Las listas son propuestas, no segundos de demora.

**Controles negativos y límite conservado.** No se activa la vía rápida con frase de audio antiguo, solo dos palabras, una palabra incorrecta, frase que empieza antes del respaldo aceptado ni frase con dos apariciones. Este último control usa un cuento construido de 61 palabras y mantiene 61. En I, texto antiguo rechazado seguido del mismo texto con tiempos nuevos, se mantiene 14/14: la segunda propuesta sigue ignorándose. Estos controles no eliminan otras decisiones que pueda aceptar el algoritmo anterior.

**Interpretación y decisión.** El resultado positivo es todavía sintético, sobre datos usados para diseñar la regla. El umbral de tres palabras y las restricciones temporales son provisionales. Timestamps estimados, exactitud y unicidad no prueban habla nueva: el ASR puede equivocarse o inventar texto. No se declara resuelta la relectura ni se incorpora la variante al seguidor habitual. Este experimento y sus revisiones permanecen locales.

**Evidencia.** scripts/comparar_recuperacion.py, pruebas/16_recuperacion_global_exacta.md, informes enlazados y protocolo de contraste grabado.

**Comprobaciones automáticas.** Pasan 51 pruebas. Las seis nuevas cubren recuperación inicial, condiciones de exactitud/unicidad/longitud, tiempos antiguos/solapados/desordenados o inválidos, preservación de datos, camino local y política de texto idéntico.

## E045 · Revisión compartida y propuesta de relectura lejana real

**Fecha:** 19/10/2026.

**Comprobación del usuario.** Ejecuta comparar_recuperacion y comparte resultados/recuperacion/20261019_120351_062213, confirmando cero activaciones en grabaciones y los resultados de los diez controles. Pasan 51 pruebas, incluidas seis nuevas sobre recuperación inicial, condiciones de exactitud/unicidad/longitud, tiempos antiguos/solapados/desordenados o inválidos, preservación de datos, camino local y política de texto idéntico.

**Conclusión de la revisión.** Se confirma cero activaciones de la nueva recuperación en los 36 registros existentes y las recuperaciones sintéticas de A–D desde la primera propuesta. E–H/J no activan la vía rápida; I conserva la limitación del texto idéntico. No se declara validación positiva con audio real de esta nueva vía.

**Contraste siguiente, aún no realizado.** Está preparado pruebas/17_relectura_lejana_grabada.md: grabar el cuento completo a ritmo normal, pausa aproximada de dos segundos y volver a Los dos se quedaron en silencio mirando sus alas lentamente, terminando en alas. Posición final esperada 45, no 56. Tras identificar el WAV y revisar su contenido, comparar ventanas 4/8 s y bloques 2 s, con referencias selectivas si hacen falta. No ajustar la regla para favorecer esa primera comparación. La consigna no constituye una anotación temporal ni valida otras voces o entornos.

**Estado.** Protocolo preparado en pruebas/17_relectura_lejana_grabada.md. Se espera la ruta del WAV y revisión de contenido antes de generar referencias o resultados. La grabación y el análisis siguen pendientes; no se ha activado el micrófono ni publicado nada en esta revisión.

## E046 · Primer contraste grabado de relectura lejana

**Fecha:** 21/10/2026. Contenido confirmado, tres anclas humanas revisadas y comparaciones/evaluación comprobadas por el usuario y por el asistente.

**Grabación y método.** WAV lectura_20261021_090304_259866.wav, 60 s, nivel máximo comunicado 0,8252. Consigna: cuento completo y vuelta a Los dos se quedaron en silencio mirando sus alas, terminando en alas (45). La consigna no sustituye una referencia humana. El usuario ejecuta ventanas 4/8 s, bloques de 2 s y tres rondas: resultados/comparaciones/20261021_090720_432047. Son repeticiones de cómputo sobre un solo audio del mismo adulto, cuento y entorno.

**Resultado del seguidor original.** Ventana 4 s: final 56 en las tres rondas; inferencia total media 29,38 s, ninguna de 90 llamadas supera 2 s. Ventana 8 s: final 45 en las tres rondas; total medio 36,57 s, seis de 90 llamadas superan 2 s. En 8 s reconoce la frase releída en el corte 34, deja recuperación pendiente y solo vuelve a 45 en el corte 38; el texto idéntico del corte 36 no confirma recuperación. En 4 s los candidatos globales cambian de 43 (corte 32) a 45 (34), sin confirmar dos candidatos iguales antes de perder suficiente texto. No equivale a una omisión del lector.

**Comparación de variantes.** Se añade scripts/comparar_relectura_lejana.py para recibir una carpeta explícita y reproducir original, combinación y recuperación exacta sobre idénticas hipótesis. Guarda huellas de fuentes/código, evidencia y posiciones por corte, con tiempos de salida lista simulados reutilizados. Comprueba reproducción exacta de posiciones, movimientos y modos originales en los seis registros. No cambia ninguna regla ni parámetros. Primera ejecución: resultados/relectura_lejana/20261021_091237_442232.

**Resultado experimental.** En las tres rondas de 4 s la nueva vía se activa en el corte 32, desde 56 a 43 (mirando), y avanza localmente a 45 en el corte 34; original y combinación terminan en 56. En las tres rondas de 8 s la nueva vía se activa en 34 y vuelve directamente a 45, mientras original y combinación recuperan en 38. Los cuatro segundos de diferencia corresponden a cortes de audio, no a una reducción de latencia humana medida. Los tiempos ASR de las frases que activan la regla son posteriores al respaldo aceptado: primera ronda 4 s, inicio 28,78 frente a respaldo 25,32; 8 s, inicio de la cola 29,36 frente a respaldo 25,88. Pasan las nueve pruebas específicas de combinación y recuperación.

**Comprobación compartida.** El usuario ejecuta el comparador y comparte resultados/relectura_lejana/20261021_091515_954571. Se contrasta con la ejecución del asistente: coinciden los seis registros completos de comparación, incluidas posiciones, modos y evidencias. Se confirman las activaciones en 32 s (ventana 4 s) y 34 s (8 s). Esta comprobación reproduce el cálculo; todavía no constituye revisión humana del contenido del audio.

**Referencia confirmada y anotación preparada.** El usuario confirma el cuento completo seguido únicamente de la frase 37–45, sin continuar con Después. Se guarda datos/referencias/lectura_relectura_lejana.json, identificado por hash del WAV. El anotador añade el caso relectura_lejana con tres palabras sin tiempos propuestos: cuaderno (56, intento 1), Los (37, intento 2) y alas (45, intento 2). El inicio de Los y el final de alas delimitan la frase sin anotar sus palabras interiores; la revisión se completa y se documenta a continuación.

**Anclas humanas y contraste temporal.** El usuario guarda y revisa los tres intervalos: cuaderno 24,65–25,48 s, Los de la relectura 29,16–29,43 y alas 32,17–32,73. Pausa entre final del cuento y relectura: 3,68 s; frase releída: 3,57 s. La duración real difiere de la consigna aproximada y no se modifica la grabación para ajustarla. scripts/evaluar_relectura_lejana.py contrasta las trazas con esas anclas, verifica audio/fuentes y guarda evaluacion_humana.json/md en la carpeta del comparador del usuario. En ventana 4 s, la nueva variante llega a alas con demora simulada 2,87–2,92 s desde su final humano (media 2,89); original/combinación no recuperan durante el registro. En 8 s, la nueva demora es 2,96–3,16 s (media 3,06), frente a 6,82–6,90 (media 6,87) de original/combinación. Se reutilizan tiempos de inferencia/cola: no es latencia visual medida ni incluye el coste adicional de las variantes. No se estima precisión de palabras internas no anotadas. Pasan dos pruebas específicas del evaluador: excluye alas de la primera lectura y conserva ausencia de detección sin inventar demora. El usuario ejecuta el evaluador y comparte su salida: confirma las 18 filas de resultados, con las mismas demoras simuladas que la comprobación del asistente. La revisión compartida de este contraste temporal queda completada; las variantes siguen experimentales y sin activar.

**Apoyo a la interpretación.** Se prepara un explorador local de ventanas (scripts/explorar_ventanas.py, herramientas/explorador_ventanas) para comparar por escucha fragmentos exactos por corte, transcripciones guardadas y decisiones de los tres seguidores. Solo consulta: sin nuevas inferencias. Se validan seis originales y 180 límites, ocho clips por muestras dentro de la cuantización PCM16, y en navegador cambio de corte y reproducción excluyente de 4/8 s. Permite revisar auditivamente el efecto del contexto conservado/descartado; no genera nuevas métricas ni modifica reglas.

**Interpretación y siguiente comprobación.** Primera activación positiva de esta vía sobre hipótesis procedentes de una nueva grabación, con contenido confirmado y anclas revisadas por el lector. Comparador y evaluación temporal comprobados por ambas partes. Una grabación con tres rondas no demuestra generalización. Antes de publicar, pasan las 53 pruebas de la batería completa. El contraste siguiente será una nueva lectura completa sin relectura: buscar retrocesos falsos antes de adoptar la regla. Ninguna variante se activa en seguir.py. El usuario autoriza publicar código, resultados y diario original; el diario alternativo permanece local.

## E047 · Control sin relectura con lluvia de fondo

**Fecha:** 21/10/2026. Comparación ASR y reproducción de variantes comprobadas por usuario y asistente. El usuario confirma una sola lectura; no se dispone de revisión lexical palabra por palabra ni de anclas temporales nuevas.

**Objetivo y condiciones.** Comprobar si las reglas provocan retrocesos en una nueva lectura sin relectura. El usuario informa de lluvia de fondo y reduce la duración prevista de 60 a 40 s; no se cambia el modelo, las reglas ni el tratamiento del audio. WAV lectura_20261021_100814_321948.wav, 40 s comprobados, máximo comunicado 0,8782. No hay comparación emparejada que permita atribuir efectos a la lluvia.

**Procedimiento.** El usuario ejecuta ventanas 4/8 s, bloques 2 s y tres rondas: resultados/comparaciones/20261021_100926_258927. El comparador admite --control-sin-relectura para presentar este control y registrar retrocesos y pérdidas del final después de alcanzarlo. Solo cambia la presentación/registro; no las reglas. Reproduce los seis originales y conserva fuentes, evidencia y huellas. Ejecución del asistente: resultados/controles_sin_relectura/20261021_101354_783663.

**Resultado.** Las tres versiones coinciden en todas las posiciones de los seis registros: sin movimientos negativos, sin activaciones de recuperación exacta, final 56 en todos y sin perderlo después de alcanzarlo. No basta con mirar la posición final: también se comprueba toda la trayectoria. Es un control favorable de ausencia de retrocesos nuevos en este audio, no una tasa general de falsos positivos.

**Procesamiento.** Ventana 4 s: inferencia total media 23,96 s, ninguna de 60 llamadas supera 2 s. Ventana 8 s: 36,04 s y tres de 60 llamadas superan 2 s; los picos se sitúan en el corte 22 de cada ronda. La cola máxima simulada va de 4,35 a 8,51 s. No se conoce la causa del coste elevado ni se atribuye al ruido de lluvia. Las tres rondas repiten una sola grabación y no son lecturas independientes.

**Revisión compartida y decisión.** El usuario confirma una sola lectura y ejecuta el comparador: resultados/controles_sin_relectura/20261021_101537_824815. Los seis registros coinciden íntegramente con la ejecución del asistente, incluidas las posiciones, movimientos y evidencias de las tres versiones. Control revisado sin retrocesos ni activaciones de la vía nueva. Esta confirmación no valida automáticamente cada palabra de la transcripción ASR ni fija límites de habla/silencio. Sin marcas humanas nuevas no se calcula demora respecto al final de la lectura. Antes de elegir configuración conviene diagnosticar el pico del corte 22 en ventana 8 s; causa pendiente. Se mantienen las reglas experimentales sin activar; no se publica este nuevo control sin petición.

## E048 · Diagnóstico del pico de reconocimiento en el corte 22 s

**Fecha:** 21/10/2026. Diagnóstico solicitado por el usuario; ejecutado por el asistente, pendiente de contraste compartido.

**Pregunta y método.** Aislar el coste que produce la ventana 8 s en el control con lluvia. scripts/diagnosticar_inferencia.py instrumenta llamadas nativas encode/generate/align, conserva opciones/resultados y guarda todos los intentos, temperaturas, textos, razón de compresión y log-probabilidad. Configuración habitual: 18 inferencias aisladas (ventanas 4/8, cortes 20/22/24, tres rondas de orden aleatorio). Modelo local CPU int8 cargado una vez, sin calentamiento excluido. Fuentes, audio, versiones y código con hash. Ejecución: resultados/diagnostico_inferencia/20261021_101852_059105.

**Hallazgo.** En las tres rondas de ventana 8 s/corte 22 se repiten tres intentos de generación, temperaturas 0/0,2/0,4. Los primeros dos textos superan la razón de compresión máxima 2,4 por repetición excesiva; el tercero pasa. La log-probabilidad no es el motivo de rechazo en esos intentos. Primera ronda: razones 2,552 y 2,679 frente a 1,078 al aceptar. El tiempo de generación, 10,02–12,08 s, domina el total de 11,84–13,86 s; encoder aproximadamente 1,43–1,58 s y alineamiento 0,17–0,21 s. Las ventanas 4 s/corte 22 y las de 8 s/cortes vecinos usan un solo intento a temperatura 0. No es una decisión ni coste del seguidor.

**Ablación limitada.** Otras seis inferencias del corte 22 con temperature=0 (solo diagnóstico): resultados/diagnostico_inferencia/20261021_102019_524726. Ventana 8 s tarda 6,30–6,35 s, pero mantiene repeticiones de Ana llamó… y texto ajeno al cuento: Después de un momento, la gente se volvió a ver a Ana. Aun sin temperaturas alternativas, hay dos llamadas a generación a temperatura cero por el recorrido de segmentos/pasos; no equivale a una sola llamada interna. El filtro cumple una función útil y no se desactiva en la configuración habitual.

**Límites e interpretación.** Son tiempos nuevos instrumentados, distintos de los 6,35–10,51 s originales; carga, estado del proceso e instrumentación afectan las duraciones. Los registros originales no guardaban los intentos internos y no se reconstruye su número exacto. Se identifica un mecanismo reproducible del pico, pero no la causa acústica de la primera salida repetitiva ni un efecto causal de lluvia. La razón de compresión no es un porcentaje de certeza. Sin evaluación lexical completa ni medición de latencia visual.

**Decisión y evidencia.** Mantener intactos seguir.py y las reglas. Informe resultados/diagnostico_inferencia/20261021_101852_059105/diagnostico.md. Invitar al usuario a ejecutar el diagnóstico del corte 22 y contrastar intentos/costes; los textos de temperaturas no nulas pueden variar. No se publica este trabajo sin petición. No requiere nuevas grabaciones.

## E049 · Segunda relectura lejana: vuelta a Cerca de un árbol

**Fecha:** 21/10/2026. Contenido confirmado, tres anclas revisadas y comparador/evaluación temporal comprobados por usuario y asistente.

**Objetivo y grabación.** Contrastar otro destino sin modificar reglas: cuento completo hasta cuaderno, seguido de Cerca de un árbol encontró una mariposa azul y terminar en azul (17). WAV lectura_20261021_103917_243241.wav, duración comprobada 45 s frente a los 60 previstos; máximo comunicado 0,958. La duración no invalida por sí sola la prueba si contiene la consigna completa; todavía no constituye referencia humana. No se presupone que la lluvia del control anterior siga igual en esta grabación.

**Método y fuentes.** Ventanas 4/8 s, bloques 2 s, tres rondas: resultados/comparaciones/20261021_104005_265730. El usuario comparte las seis ejecuciones. Comparación de original, combinación y recuperación exacta sobre las mismas hipótesis, sin inferencias nuevas ni cambio de parámetros: resultados/relectura_lejana/20261021_104431_582794. Se verifica reproducción de posiciones, movimientos y modos originales.

**Resultado.** En las tres rondas de ventana 4 s, original/combinación permanecen en 56. La nueva regla vuelve de 56 a 12 (un) en el corte 28 con Cerca de un, frase de tres palabras exacta y única en este cuento, y después avanza localmente a 13 en 30, 15 en 32 y 17 en 34. En las tres rondas de 8 s, original/combinación recuperan a 17 en 36; la nueva recupera directamente a 17 en 34 con las ocho palabras exactas. En 4 s, el respaldo ASR de la frase empieza en 25,42, posterior al apoyo aceptado 22,42; en 8 s empieza en 26,00 frente a 22,68. Son tiempos ASR estimados, no anclas humanas.

**Anclas revisadas y evaluación temporal.** El usuario guarda cuaderno 21,79–22,51 s, Cerca de la relectura 25,73–26,84 y azul 33,32–34,32. Pausa entre final del cuento y relectura 3,22 s; frase releída 8,59 s. Se amplía evaluar_relectura_lejana con --caso relectura_azul y destino parametrizado, conservando claves históricas para el primer caso. En la nueva variante, la primera hipótesis que señala azul usa el corte 34, anterior en 0,32 s al final humano de la palabra: el reconocimiento usa una palabra todavía incompleta. Se distingue esa primera hipótesis de la actualización con corte posterior al final humano. Primera salida lista desde el final humano: nueva 4 s 1,25–1,26 s (media 1,26), nueva 8 s 1,28–1,55 (media 1,39), original/combinación 8 s 3,19–3,31 (media 3,25); original/combinación 4 s no recuperan. Con criterio de corte posterior al final completo, todas las versiones que recuperan apoyan azul en el corte 36 y sus salidas quedan listas aproximadamente 37,51–37,63. Son medidas distintas: no se presenta la primera como reconocimiento garantizado de la palabra completa. Se reutiliza cola simulada, sin medir pantalla ni coste extra de variantes. La evaluación queda en resultados/relectura_lejana/20261021_104703_885196/evaluacion_humana.json/md. Pasan tres pruebas específicas, incluida separación de palabra incompleta y actualización posterior con otro destino. El usuario ejecuta el evaluador y comparte las 18 filas: coinciden con la evaluación del asistente, incluidas las primeras salidas 1,26/1,39 s de media y el indicador de corte anterior al final humano en la nueva variante. Revisión conjunta de esta prueba completada. Se conserva la distinción entre primera hipótesis parcial y actualización con audio completo. Ninguna regla cambia ni se activa.

**Interpretación.** Segundo caso grabado favorable con un destino diferente y reglas sin ajustar. En 4 s la reubicación inicial permite seguir aproximaciones ASR posteriores por la búsqueda local; no significa que todo el reconocimiento sea exacto. Cerca de un cumple el mínimo provisional de tres palabras, pero su unicidad en este cuento no demuestra que esa longitud sea segura en otros textos. Ventana 8 s conserva más contexto y espera hasta tener una cola exacta completa. Las anclas humanas permiten contrastar los tiempos, distinguiendo hipótesis sobre palabra incompleta y actualizaciones posteriores a su final.

**Procesamiento y siguiente comprobación.** Total medio 30,68 s (4 s) y 36,05 s (8 s), ninguna de las 69 inferencias por ventana supera 2 s; en este audio no aparece el pico del control anterior. Tres rondas de un audio no son tres lecturas. El usuario confirma cuento completo seguido solo de la frase indicada y comparte resultados/relectura_lejana/20261021_104703_885196. Los seis registros completos coinciden con los del asistente, incluidas posiciones y evidencias. Se guarda datos/referencias/lectura_relectura_azul.json y se prepara el caso relectura_azul en el anotador: cuaderno (56, intento 1), Cerca (10, intento 2), azul (17, intento 2). Las tres anclas empiezan sin tiempos ni revisión ficticia; sirven para delimitar la relectura sin anotar palabras interiores. Antes de publicar pasan las 54 pruebas completas. Mantener variantes sin activar. El usuario autoriza publicar esta actualización, incluido el control y el diagnóstico de inferencia; este último sigue pendiente de reproducción por el usuario. Solo se publica el diario original, manteniendo el alternativo local.

## E050 · Preparación del segundo cuento y selección explícita del texto

**Fecha:** 21/10/2026. Lectura normal confirmada y comparación de variantes comprobada por usuario y asistente. Relectura planificada todavía pendiente.

**Objetivo y diseño.** El usuario acepta probar otro cuento antes de comparar otros sistemas y ayudas de audio. Se crea lectura_02.txt, texto original de 56 palabras sobre Lucía, su abuelo y un barco, misma longitud que el anterior. Dos casos previstos: lectura normal y, tras revisarla, lectura completa seguida de Junto a una fuente descubrió un pequeño barco rojo. Final normal 56 (estantería), final de relectura 19 (rojo), tramo 11–19. Mantener adulto, micrófono, configuración, ventanas 4/8 y tres rondas; registrar condiciones acústicas reales. No ajustar reglas al ver estos primeros resultados. El protocolo 21 conserva huellas del texto y de los tres archivos de reglas antes de grabar.

**Cambios de herramientas.** grabar.py incorpora --cuento, muestra la ruta/texto elegido y sigue esperando Enter; por defecto conserva lectura_01.txt. comparar_ventanas.py incorpora --cuento, comprueba que el texto se puede leer/no está vacío, lo transmite a cada seguir.py y guarda su ruta/hash en el manifiesto. No cambia el reconocimiento ni el seguidor. Los registros guardan las palabras del cuento elegido para reproducir las variantes sin asociaciones basadas en el último WAV.

**Comprobación.** Pasan cuatro pruebas específicas: dos de comparación existentes y dos nuevas que comprueban la transmisión/identidad de un texto diferente a través de la comparación y la presentación del texto elegido sin saltarse la espera de Enter. El reconocimiento está simulado en esas pruebas y no se ha grabado audio ni ejecutado ASR sobre el segundo cuento. La grabación normal y el análisis ASR se realizan a continuación; la siguiente comprobación compartida es reproducir las variantes sobre esas hipótesis.

**Primera grabación normal y comparación.** El usuario guarda lectura_20261021_110858_556291.wav, 40 s, e informa de que sigue lloviendo. Máximo comunicado 1,0; comprobación PCM16: una muestra exactamente al límite entre 1.764.000, sin racha prolongada. Ese dato no basta para evaluar distorsión audible. Ejecuta y comparte resultados/comparaciones/20261021_111057_752726 con lectura_02 explícita. Se verifica hash/texto correcto en los seis registros y que siguen intactas las huellas de los tres archivos de reglas fijadas antes de grabar. Comparación del asistente: resultados/controles_sin_relectura/20261021_111428_479787. Original, combinación y recuperación nueva coinciden en todas las posiciones: ningún retroceso, ninguna recuperación exacta, alcanzan 56 (estantería) en el corte 26 y no pierden el final. No demuestra generalización completa ni precisión lexical o temporal. El usuario confirma la lectura y comparte resultados/controles_sin_relectura/20261021_111600_102761: los seis registros completos coinciden con los del asistente. Revisión conjunta del control completada. No se dispone de tiempos humanos nuevos ni de revisión lexical independiente.

**Coste en este audio.** Total medio 26,89 s (4 s) y 29,67 s (8 s); inferencias superiores al bloque 18/60 y 11/60 respectivamente. Cola máxima por ejecución de hasta 2,07 s (4 s) y 2,27 s (8 s). Los costes aumentan en varias ejecuciones y ambas ventanas; no se atribuye una causa al ruido, al texto o a la temperatura del equipo sin medirla. Se comparan rondas sobre la misma grabación, no lectores independientes. Después de revisar este control, realizar la relectura planificada del segundo cuento sin ajustar reglas.

**Protección de resultados.** Se refuerza el guardado del seguimiento/comparador con scripts/archivos.py: escribir un temporal cerrado en la misma carpeta y sustituir el destino, con hasta cuatro intentos para ciertos errores de acceso/escritura. Si persiste el fallo se informa sin truncar el último destino válido. No se cambia ninguna regla: audio_bounds, locate y Tracker se contrastan por AST con la versión publicada. Pasan 13 pruebas específicas (incluidas tres de guardado que simulan error transitorio y persistente) y diez escrituras sucesivas en la carpeta de resultados. La repetición de una comparación crea otra carpeta, conservando la ejecución parcial; no se mezclan inferencias incompletas con rondas nuevas. El refuerzo de guardado no garantiza resolver cualquier fallo del sistema de archivos ni identifica su causa.

**Evidencia y límites.** pruebas/21_segundo_cuento.md y tests/test_cuento_configurable.py. Es un contraste con otro texto del mismo adulto; no sustituye diferentes voces ni es una validación final. Queda local hasta revisión y autorización de publicación.

## E051 · Relectura del segundo cuento y texto ajeno a la lectura

**Fecha:** 21/10/2026. Contenido y comparador comprobados por ambas partes; anclas humanas revisadas. Evaluación temporal ejecutada por el asistente, pendiente de contraste compartido.

**Datos y método.** WAV lectura_20261021_114202_408281.wav, 45 s, máximo comunicado 0,8402. El usuario confirma cuento completo correcto y la repetición lenta solicitada de Junto a una fuente descubrió un pequeño barco rojo, sin los textos extraños que aparecen en ASR. Referencia de contenido datos/referencias/lectura_02_relectura.json, sin tiempos humanos. Fuente completa resultados/comparaciones/20261021_115105_998651: ventanas 4/8, tres rondas, 23 cortes por registro hasta 45 s. Se comprueban cuento/hash correctos y se comparan los tres seguidores sobre idénticas hipótesis, sin cambiar reglas ni ejecutar inferencias nuevas. Resultado del asistente resultados/relectura_lejana/20261021_115740_472120.

**Seguimiento.** En ventana 4 s, original/combinación permanecen en 56; la recuperación nueva vuelve directamente a 19 (rojo) en corte 40 con un pequeño barco rojo. En 8 s, la nueva vuelve a 16 (un) en corte 36 con junto a una fuente descubrió un, avanza a 17 (pequeño) en 38 y a 19 en 40. Original/combinación esperan hasta 42 para recuperar 19. Se repite en las tres rondas. La regla vuelve a aportar mejora en un segundo cuento, pero en este audio la ventana corta no dispone antes de una cola exacta suficiente; no mantiene siempre la ventaja temporal observada en otros casos. Sin anclas humanas solo se comparan cortes, no demora desde la pronunciación.

**Contenido ASR no pronunciado.** En corte 30, ventana 4 s (audio 26–30), ronda 1 genera y nos vemos en el próximo vídeo; ronda 2 añade hasta la próxima; ronda 3 devuelve Hum. El lector confirma que no dijo esos textos. Las tres versiones conservan 56 en ese corte: no se produce retroceso por estas hipótesis. El rechazo local tiene 1/7 coincidencias en ronda 1, 0/8 en ronda 2 y evidencia insuficiente en ronda 3. No se atribuye al ruido una causa demostrada ni se fija el intervalo como silencio puro sin revisión acústica. Las variaciones sobre el mismo WAV confirman que la hipótesis automática puede cambiar; no son palabras pronunciadas distintas por el lector.

**Coste y límites.** Total medio 36,35 s (4 s) y 40,00 s (8 s); llamadas >2 s 3/69 y 2/69. La cola puede existir también con costes inferiores a 2 s al final porque el último salto 44–45 dura 1 s. La nueva recuperación no corrige el texto ASR: solo modifica localización. Los textos no pronunciados siguen siendo una limitación del reconocedor aunque no hayan desplazado al seguidor en este caso. Tres rondas no son tres lecturas ni validación de otras voces.

**Anclas humanas y evaluación.** El usuario revisa estantería 25,25–26,13 s, Junto 29,25–30,13 y rojo 38,81–39,95, con nota Ruido de fondo algo notable en rojo. Pausa 3,12 s y relectura 10,70 s; no se transfieren estos tiempos al ASR. evaluar_relectura_lejana incorpora --caso relectura_cuento_02 (tramo 11–19), sin cambios en el seguidor. Evaluación del asistente: resultados/relectura_lejana/20261021_115941_383989/evaluacion_humana.json/md. Primera salida en rojo respecto a su final humano: nueva 4 s 1,63–2,25 s (media 1,85), nueva 8 s 1,63–1,69 (media 1,65), original/combinación 8 s 3,56–3,80 (media 3,69); original/combinación 4 s no recuperan. Aquí todos los cortes que identifican rojo son posteriores al final humano (corte 40 frente a 39,95), a diferencia del caso azul. La nueva 8 s ya vuelve a un antes de terminar la frase, salidas listas 37,48–37,64; la nueva 4 s solo se recoloca al identificar rojo. Cola simulada reutilizada, sin coste adicional de variantes ni pantalla; no es latencia visual real. Pasan las tres pruebas del evaluador. Pendiente de que el usuario repita la evaluación.

**Siguiente comprobación.** El usuario ejecuta el comparador y comparte resultados/relectura_lejana/20261021_115941_383989. Sus seis registros completos coinciden con los del asistente. Se prepara el caso relectura_cuento_02 en el anotador para estantería (56, intento 1), Junto (11, intento 2) y rojo (19, intento 2), con tiempos inicialmente vacíos. Anclas revisadas y evaluación preparada; queda su ejecución compartida. Se mantienen reglas/ASR habituales y este trabajo permanece local hasta autorización de publicación. Los resultados de una ejecución parcial anterior no se mezclan con las rondas completas.

## E052 · Recursos de cómputo y comparación orientada a tablets

**Fecha:** 21/10/2026. Solicitado por el usuario: añadir métricas útiles de CPU/GPU/memoria/rendimiento y mantener límites claros para el destino tablet. Implementado y comprobado por el asistente; pendiente de revisión del usuario.

**Implementación y alcance.** scripts/recursos.py obtiene equipo/SO/CPU/RAM y NVIDIA disponible, muestrea CPU/RAM del proceso y GPU global (uso, VRAM, potencia y temperatura), y resume carga, tiempo CPU, inferencia mediana/P95/máxima, RTF y cola. seguir.py añade monitor, CPU por inferencia, tamaño del modelo y pico/RMS de señal ASR; comparar_ventanas y los comparadores/evaluador recientes adjuntan recursos_computo.json/md. --sin-recursos permite contrastar sobrecoste de muestreo. No se cambia CPU por GPU ni se alteran reglas de posición/ventana, verificadas por AST con la versión publicada. GPU global incluye otras aplicaciones; no es consumo exclusivo del ASR. CPU/RAM del proceso incluyen la instrumentación.

**Históricos y pruebas.** Se complementan 32 carpetas con estadísticas derivadas de fuentes originales, sin modificar sus JSON ni hashes. CPU/RAM/GPU históricas no medidas se indican como tales. Inventario actual separado en resultados/recursos_equipo/20261021_125210_444804/equipo.json: Intel i7-11800H, 16 procesadores lógicos, NVIDIA RTX 3050 Laptop de 4096 MiB; no se atribuye esa medición temporal a las pruebas anteriores. Comprobación técnica con un prefijo de 8 s ya grabado, cuatro inferencias y muestras reales en resultados/verificacion_recursos; no se presenta como prueba de precisión ni benchmark de tablet. Pasan 63 pruebas, incluidas cuatro nuevas de integridad y semántica de métricas. JSON de pruebas anteriores intactos.

**Interpretación y límites.** Tiempo de salida sigue siendo simulado. RTF incluye silencio y audio reprocesado; no mide latencia de pantalla. Potencia GPU W no equivale a energía del ASR J. CPU térmica, energía específica, batería y FLOPs no disponibles se conservan sin valor, no como cero. El monitor puede influir en la carga y no se deben mezclar condiciones instrumentadas/no instrumentadas en comparaciones directas. El ASR actual usa CPU int8 aunque exista GPU. Antes de implementación móvil habrá que medir en la tablet elegida y distinguir procesamiento local/remoto, memoria, arranque, batería y respuesta sostenida.

**Evidencia y continuación.** docs/METRICAS_COMPUTO.md; scripts/informar_recursos.py permite al usuario actualizar/ver las fichas sin inferencias nuevas. No se publica esta actualización sin petición. Sigue pendiente la comprobación compartida del evaluador temporal del segundo cuento; esta ampliación no cambia los resultados de aquella prueba.

## E053 · Catálogo legible y consolidación del dataset antes de comparar sistemas

**Fecha:** 21/10/2026. El usuario traslada la recomendación de su profesor: construir un banco amplio y documentado antes de cambiar de entorno, reutilizando los mismos audios para todas las configuraciones. Solicita identificar cada grabación por tipo, eventos y fecha.

**Catálogo y trazabilidad.** Se amplía datos/referencias/catalogo.json a diez grabaciones, dos textos, un adulto y 8,5 minutos; se conservan los IDs iniciales y los WAV originales, con SHA256. Todas quedan en desarrollo por haber sido utilizadas. Se crea AUDIOS.md con nombres legibles (normal, lluvia, pausa, lenta, disfluencias concretas y cada relectura), texto, duración, lector, referencia/anotación y ambiente confirmado. Los artefactos del ASR se mantienen separados de eventos del lector. No se rellenan condiciones de lluvia ni referencias literales inexistentes por extrapolación.

**Uso y validación.** scripts/catalogo.py lista/verifica WAV, registra nuevas grabaciones sin validarlas y añade nombres a Markdown sin cambiar JSON históricos. Se etiquetan 170 informes. grabar.py admite --nombre/--caso/--lector/--ambiente y registra solo después de guardar el WAV, con contenido pendiente y partición sin asignar. Transcripción, seguimiento, comparación, evaluación y páginas reciben el nombre descriptivo junto al archivo técnico. El visor se reinicia y se comprueba en navegador su nombre visible. Pasan 66 pruebas y todas las huellas de WAV coinciden. No se activa micrófono ni ejecuta ASR con esta catalogación.

**Fuente externa revisada.** Se consulta la ficha propuesta: Common Voice Scripted Speech 27.0 - Spanish, ID cmu5kitx700pemi073feoiqqu, versión cv-corpus-27.0-2026-09-11, paquete mostrado 48,38 GB, MP3, CC0-1.0. La ficha prohíbe reidentificar hablantes y volver a alojar/compartir el dataset. Procedencia y estado sin descargar quedan en datos/externos/FUENTES.json; audio/descargas externos se ignoran por Git. Se propone como complemento de diversidad para ASR, no sustituto de pruebas continuas con pausas/disfluencias/relecturas y referencias temporales. No se ha descargado ni subido el corpus.

**Diseño del banco.** docs/DATASET.md especifica identidad/versionado, grabaciones propias y externas separadas, cobertura de textos/voces/eventos, revisión literal/temporal, particiones y métricas. Los audios vistos no pasan a ser test independiente. Reservar hablantes/textos/audios nuevos antes de evaluar según la pregunta; no mezclar copias procesadas entre particiones. Congelar audios/referencias/normalización antes de comparar sistemas y reportar calidad y recursos, sin tratar rondas como lecturas independientes. Cantidades iniciales propuestas son orientativas, no un requisito estadístico validado ni un lote ya acordado. Prioridad siguiente: revisar catálogo y acordar la matriz/selección, manteniendo pendiente la comprobación compartida del último evaluador temporal. Mantener ambos diarios; solo el original es publicable tras autorización.

## E054 · Nombres descriptivos en los archivos de audio

**Fecha:** 23/10/2026. Se renombran físicamente los diez WAV con tipo de lectura, cuento, fecha y disfluencias o tramo de relectura cuando corresponde. Se retira AUDIOS.md y su generación automática. El catálogo técnico conserva los IDs y alias anteriores para resolver informes y anotaciones históricos sin reescribir sus JSON. La grabadora aplica nombres descriptivos a nuevas lecturas; los informes usan IDs breves y la selección del último WAV usa fecha de modificación.

**Comprobación.** Las diez huellas SHA256 coinciden con las anteriores. Cargan la anotación completa, las seis sesiones de intervalos y el explorador del segundo cuento. Pasan 66 pruebas, incluida la conservación del contenido y resolución del nombre anterior tras renombrar. No se ejecuta ASR ni se cambian reglas. El usuario se encarga de descargar el dataset externo; sigue pendiente su inspección local. Cambios sin publicar.

## E055 · Preparación de un texto con frase repetida

**23/10/2026, pendiente de grabación.** Se prepara lectura_03.txt, texto original de 77 palabras con «El tren llegó a la estación» en 1–6 y 41–46, y protocolo pruebas/22_frase_repetida.md. Primero lectura normal como control; después podrá contrastarse una relectura ambigua. Se mantienen modelo, reglas y ventanas 4/8 s para ampliar cobertura textual sin cambiar el sistema. Una frase repetida en el texto no es disfluencia y por sí sola no identifica el destino pretendido. Se verifican posiciones y hash del texto; aún no hay resultados acústicos. Sin publicación.

## E056 · Siete lecturas del segundo cuento con velocidades, eventos y ruido

**Fecha y referencia:** 23/10/2026. Siete WAV nuevos (6 min 10 s). El lector confirma cuento terminado en todos, fragmentos/repeticiones durante «muchas trabadas», pausa aproximada de 8 s y relectura de Junto…rojo antes de continuar, y omisión de ambas apariciones de abuelo. Solo comunica ruido en la prueba que reproduce sonidos de calle desde el móvil. Consignas y confirmaciones en pruebas/22_lote_segundo_cuento.md; no se inventa transcripción literal completa de las trabadas ni tiempos humanos. Los audios usados pasan a desarrollo.

**Experimento y comprobación.** scripts/comparar_lote.py selecciona por fecha, cuento y huella y ejecuta secuencialmente ventanas 4/8 s, actualización de 2 s y tres rondas con small CPU int8 y VAD. Conserva manifiesto, logs, seis registros por audio e informes de recursos. Se verifican siete WAV, cuento, 42 ejecuciones y 1.110 actualizaciones en resultados/lotes/20261023_102114_072901; revision_asistente.json guarda las huellas de los registros. El catálogo resuelve nombres compartidos por huella y rechaza alias de contenido distinto. Pasan 67 pruebas; Tracker, locate y audio_bounds coinciden por AST con 30c4c83. No se activan reglas experimentales.

**Resultados e interpretación.** Todas las posiciones finales son 56; las trayectorias se repiten entre rondas por configuración, aunque algunos textos ASR de lenta/trabadas varían. Total medio ASR 4/8 s: lenta 68,25/70,89; rápida 17,15/23,72; pausa/relectura 34,20/47,68; sustitución 27,70/40,38; ruido 26,69/35,42; trabadas 61,81/63,05; omisión 27,42/37,91. Los 4 s tienen menor total, pero lenta presenta máximo de inferencia 9,18 s frente a 2,43 con 8 s y trabadas supera 11 s con ambas. Relectura local: las seis pasadas retroceden 19→13 en corte 20 s, regresan a 19 y continúan. Azul permanece en hipótesis de sustitución y abuelo no aparece en ninguna del audio con omisiones. Alcanzar el final no demuestra exactitud literal ni detección de disfluencias. Totales con silencio y colas simuladas, sin latencia visual ni referencia temporal nueva.

**Continuación.** Revisar juntos inicio y algunos tramos de trabadas, después omisiones/relectura, sin ajustar reglas antes del contraste. El ruido de móvil es una condición artificial concreta, no prueba general de robustez. Actualizados catálogo, documentación del dataset (17 WAV presentes verificados, 14 min 40 s) y ambos diarios. Pendiente de revisión del usuario; sin publicación automática.

## E057 · Revisión cualitativa de muestras de la lectura con trabadas

**23/10/2026, revisión del lector completada.** Ante la dificultad de transcribir todos los intentos aleatorios, se prepara una revisión de cuatro intervalos (0–8, 16–24, 34–42 y 48–56 s) del audio del segundo cuento con trabadas. La web permite escuchar primero el contexto y después los recortes e hipótesis de ventanas 4/8 s, ronda 1, con el seguidor habitual. Se solicita tipo de evento escuchado y valoración cualitativa del ASR, admitiendo dudas y notas sin contar sílabas ni fijar límites de palabras. Se compara cada hipótesis con el recorte que realmente recibió: perder contexto fuera de ventana no se etiqueta como eliminación del ASR.

**Procedencia y alcance.** scripts/revisar_trabadas.py guarda, solo cuando lo solicita el usuario, una revisión separada con intervalos, huella del WAV, huellas de fuentes y notas; conserva copias al actualizar. Es revisión del propio lector asistida por ASR, no transcripción literal ni revisión independiente o exhaustiva. No mide tasa de detección de todas las trabadas ni precisión temporal. Audio y resultados originales intactos; sin inferencias nuevas ni cambios de reglas. Pasan 71 pruebas, incluidas validación de dudas, estados incompletos, etiquetas contradictorias e integridad de metadatos/copias. Se verifica en navegador la carga de la página y las duraciones de los recortes. Sin valoraciones humanas prellenadas ni publicación.

**Resultado compartido.** El usuario guarda los cuatro fragmentos como revisados y valora simplificación del ASR con ambas ventanas en los cuatro. Describe, entre otros, «lu lucia», «Descu descubrió», «la la ayudó» y «regre re regresaron». Se verifican huella del WAV, fuentes y estructura de la revisión. La conclusión es pérdida parcial de fragmentos/repeticiones en estas muestras, compatible con seguimiento hasta 56; no equivale a que desaparezcan todas las trabadas ni permite calcular porcentaje de detección. Las valoraciones no distinguen una ventana superior para conservarlas. Referencia: datos/anotaciones/lectura_02_trabadas_revision_cualitativa.json; resumen e integridad en resultados/lotes/20261023_102114_072901/revision_humana_trabadas.md y .json. Se enlaza la revisión cualitativa en catálogo sin convertirla en tiempos de palabras. Siguiente contraste: omisiones y pausa/relectura con registros existentes; mantener reglas hasta cerrar esa revisión. Sin nuevas inferencias ni publicación.

**Diagnóstico y posibles soluciones para conservar eventos.** El usuario prioriza cuantificar lo pronunciado antes de seguir: la salida simplificada pierde datos para las estadísticas. Se revisa la configuración (penalización neutra y sin prohibición de n-gramas), bibliografía sobre transcripción literal/detección y vías de ASR especializado, CTC español y análisis acústico. Reproducción del VAD: 25/32 ventanas examinadas se conservan completas; algunos recortes iniciales requieren escucha, sin atribuirles eventos no temporizados. Piloto nuevo en resultados/disfluencias/20261023_122442_840773: ocho transcripciones, cuatro fragmentos con VAD sí/no y texto bruto/palabras; las dos condiciones producen el mismo texto bruto por fragmento y mantienen simplificación. Por tanto, quitar VAD no resuelve estas muestras y la extracción de palabras no explica por sí sola toda la pérdida. Una pasada por condición, sin tasa cuantitativa ni ganador. docs/CONSERVACION_DISFLUENCIAS.md documenta evidencia, fuentes, necesidad de referencia mínima por episodio, recuperación/precisión/F1, conteo, controles negativos y deduplicación temporal entre ventanas. Se propone separar seguimiento y análisis del audio y probar literalidad sobre muestras y controles, manteniendo el seguidor. Se conservan WAV y registros anteriores, sin instalar otro motor ni publicar.

## E058 · Primer candidato para la rama de transcripción literal

**23/10/2026, revisión compartida parcial del candidato.** Se acuerda mantener el seguidor y ensayar por separado análisis literal del mismo audio. Se instala crisperwhisper 2.0.3 con backend Transformers en .tools/literal-env (Python 3.12.15, torch 2.14.1+cpu, transformers 5.20.2), sin modificar .venv. Checkpoint CrisperWhisper2.0_small fijado a bcaecf0a584a1f600d8897fe6032b9e2e56429a7, token de español y 13 archivos con SHA256 comprobados; licencia de investigación registrada. No se envían audios a un servicio externo.

**Diseño y evidencia.** Siete recortes de 8 s: cuatro muestras con trabadas ya revisadas, dos controles fluidos de lectura normal y uno sin habla según el lector. Mismos arrays a 16 kHz; una pasada secuencial por motor en procesos separados, sin VAD, cuento o notas como prompt. Actual Small CT2 CPU int8 frente a candidato Small Transformers CPU float32 en modo verbatim, cuatro hilos y marcas de palabra automáticas. resultados/literalidad/20261023_124047_726452 conserva manifiesto, textos brutos, palabras, parámetros, versiones, recursos, procedencia del modelo y fuente exacta ejecutada. Verificador comprueba entradas/outputs y los 42 registros del lote anterior intactos; 71 pruebas del proyecto pasan. Visor de solo lectura preparado para comprobación del usuario; protocolo pruebas/23_piloto_literalidad.md.

**Resultado provisional y coste.** El candidato escribe intentos/repeticiones compatibles con las notas («lu- lucia pa- paseaba», «Descu- descubrió», «la la ayudó y y», «lo y lo colocaron») que el baseline simplifica. Revisión parcial del lector: confirma que la última aparición de «el barco rojo» en Intermedio 1 (16–24 s) no se oye. Se registra como inserción del ASR, no como repetición real; no se determina si anticipa o genera una repetición. Referencia separada con huellas en datos/anotaciones/lectura_02_piloto_literal_revision.json. Esta confirmación puntual no valida todos los eventos. En control 8–16 s, «Los dos» del candidato cuenta con apoyo parcial de marcas humanas (Los 15,46–15,77; dos 15,78–16,10), no se etiqueta invención por comparar solo con el otro ASR. Ambos devuelven vacío sin habla y los controles fluidos no muestran nuevas repeticiones textuales. Inferencia total de 56 s de entrada: 14,08 s actual frente a 50,37 candidato; carga 1,15/18,33 s; pico RAM del proceso 696,73/4.252,89 MiB. Cambian backend/precisión; una pasada no demuestra superioridad ni rendimiento en tablet. El cargador avisa de tensores auxiliares inesperados y compatibilidad de generación/atención, por lo que los tiempos de palabra del candidato siguen sin validar. Próximo paso: escuchar y confirmar eventos/posibles invenciones antes de contar o adoptar. Sin nuevas reglas del seguidor ni publicación.

**Contraste con audio completo.** Tras confirmar la inserción final de «el barco rojo» en Intermedio 1, el lector solicita procesar la grabación completa y publicar las novedades. resultados/literalidad/20261023_131712_130708 conserva una pasada por motor sobre los mismos 60 s y verifica igualdad exacta de los cuatro recortes previos. El candidato largo usa bloques 0–30, 26–56 y 52–60 s con continuación; ya no escribe esa frase extra y continúa «el el barco el barco flotaba…». El primer bloque incluye también audio posterior al corte previo de 24 s: cambia entrada/contexto y ruta interna, sin demostrar una causa única ni validar todos los intentos. Inferencia actual/candidato 5,23/15,50 s, carga 1,00/7,44 s y pico RAM 696,68/4.417,32 MiB; RTF sobre audio total, incluido silencio. Se mantienen advertencias y límites de tiempos automáticos/tablet. Informe comparacion_contexto.md, fuentes ejecutadas y huellas preservadas, visor de escucha http://127.0.0.1:8776/; 74 pruebas pasan. El lector completa la escucha y valora el resto como bastante fiel; señala una omisión de intento: se oye «regres- re- regresaron» y el candidato escribe «regres- regresaron». Es un episodio conservado parcialmente, con tres intentos humanos (dos parciales y la palabra completa) frente a dos escritos; falta «re-». Confirmación con huellas en datos/anotaciones/lectura_02_literal_completa_revision.json, sin tiempos humanos interiores ni anotación exhaustiva por evento. No se calcula un porcentaje global de precisión. Se autoriza publicación del estado exploratorio sin activar el motor ni publicar el diario alternativo, dependencias, modelos o audio externo.

## E059 · Lote literal de todos los audios propios

**25/10/2026, ejecución completada; pendiente de revisión compartida.** El usuario solicita procesar todos los audios disponibles con el candidato literal. Se fijan 17 WAV propios, 880 s, dos cuentos y un lector; cobertura exacta del catálogo y huellas verificadas. Una entrada histórica sin WAV coincidente se conserva aparte y no se cuenta como otro audio. Ambos motores reconocen grabaciones completas con arrays idénticos mono a 16 kHz, sin VAD, limpieza de ruido o cuento/notas como prompt. Se mantienen modelo/ajustes del piloto; el candidato usa continuación interna 30 s/paso 26 s al superar 30 s. Un proceso por motor y modelo reutilizado secuencialmente, una pasada por WAV; no equivale a optimización de parámetros o prueba final independiente.

**Registro y contraste.** resultados/literalidad/20261025_182446_557677_UTC conserva catálogo y fuentes previas congelados, entradas/modelos/arrays con huellas, texto bruto, palabras y bloques, tiempos de inferencia/CPU/RTF, carga única, RAM y GPU global por proceso y subintervalos. Máximos de RAM por audio muestreados, con memoria reutilizada; pico Windows de toda la vida del proceso. GPU global no implica ASR en GPU y RTF con silencio no es latencia en directo ni rendimiento móvil. 77 pruebas pasan antes de las inferencias. Protocolo pruebas/24_lote_literalidad.md y visor de comparación por nombres descriptivos. Pendiente de valoración literal por evento antes de calcular fidelidad o elegir motor; no se activa en el seguidor ni se publica automáticamente.

**Resultado del lote.** Completadas 34 transcripciones (17 por motor), sin nuevas inferencias por ventanas. Inferencia total actual/candidato 131,50/426,57 s para 880 s de entrada; carga única 2,17/18,91 s; pico RAM de la vida del proceso 980,84/4.466,64 MiB. RTF total 0,149/0,485, con silencio. Verificados los 17 WAV/arrays, archivos de ambos modelos, fuente exacta ejecutada y 693 fuentes previas intactas. El candidato conserva Ana repetida, mar- mariposa y azul, y no restaura abuelo, pero deforma contexto y añade texto en el final sin habla de la primera lectura normal; el actual añade Suscríbete en la segunda normal y el literal no. La lenta del primer cuento pierde cuaderno en la salida literal. En muchas trabadas el texto coincide con el ensayo anterior y conserva la omisión de re- ya señalada por el lector. No se atribuyen estos contrastes a una causa única ni se calculan tasas globales sin referencia por evento. Resumen, métricas e integridad separados y observaciones.md documentan evidencia y límites; visor http://127.0.0.1:8777/ para revisión de todas las salidas. Candidato y ajustes habituales del seguidor permanecen separados; sin publicación automática.

**Revisión del lector y contraste documental.** El usuario señala errores del candidato literal en 1, 4, 5, 6, 11 y 17 y solicita aprovechar las referencias anteriores. La revisión humana conserva esa aclaración sin atribuirle un desglose que no ha escrito. auditoria_errores_lector.md/.json cruza las mismas huellas con transcripciones y anclas humanas, sin inferencias nuevas: aparecen continuaciones añadidas en los últimos bloques de 1, 4, 5, 6 y 11; 4 sustituye despacio/cuaderno, 5 omite a y 17 representa con su/Su como Consu/Suu sin restaurar las omisiones deliberadas de abuelo. El soporte lexical humano es completo para 1,4,5,6 y descriptivo para 11,17; Suu no prueba una prolongación real. La coincidencia en bloques finales no aísla la causa ni justifica borrar relecturas reales. El modelo actual también inventa texto en algunos casos. Sin tasa global o cambios del motor; se mantienen informe y diarios en la misma E059.

**Diagnóstico de finales y propuesta de control.** Se revisan la implementación instalada y fuentes oficiales: mitigación de bucles, temperaturas alternativas y recuperación de cierre ya estaban activadas; no se conoce aún qué mecanismos dispararon los fallos. Silero v6 ya instalado se aplica a los mismos 17 arrays sin ASR nuevo: no detecta solapamiento de voz en los cinco bloques finales con texto añadido y cubre completamente las 75 anclas humanas disponibles con margen de 400 ms; no valida todos los fragmentos ni elimina el riesgo de pérdidas. Inferencia VAD 1,68 s, recursos/modelo/código y huellas conservados en diagnostico_vad_literal.md/.json; 80 pruebas pasan. docs/CONTROL_ALUCINACIONES_LITERAL.md propone primero un contraste de final sin voz conservando originales, pausas y tiempos, después desactivar por separado recuperaciones internas si procede. Despacio/cuaderno e intentos interiores requieren análisis adicional: no se promete resolverlos con VAD ni se corrige hacia el cuento. No se cambia el motor o configuración activa ni se publica.

## E060 · Ensayo de final VAD en la rama literal

**25/10/2026, ejecutado y pendiente de revisión compartida.** El usuario autoriza la variante en casos 1,4,5,6,11,17 y controles 9/16. Se limita únicamente el prefijo enviado hasta la última voz VAD detectada con margen ya incluido, manteniendo muestra cero, pausas interiores y originales completos. VAD del diagnóstico previo reutilizado, sin usar marcas humanas para elegir el límite. Modelo, versiones, trabajador y parámetros idénticos al literal original; ocho inferencias nuevas frente a salidas anteriores reutilizadas, no una nueva ejecución del motor habitual. Entrada 480→341,12 s; puede cambiar la geometría y ruta corta/larga de bloques.

**Resultado y límites.** resultados/literalidad/20261025_193651_692690_cola_vad_UTC: los únicos cambios textuales son retirar los cinco sufijos finales añadidos de 1,4,5,6,11. Controles 9/16 y audio 17 mantienen texto completo idéntico. Siguen desváceo/jugador no en 4, omisión de a en 5, Consu/Suu en 17 y falta re- en las trabadas. Se demuestra estabilidad del resto del texto escrito, no conservación de todos los intentos reales ni precisión global. Inferencia previa/nueva 287,48/87,95 s, carga nueva 11,62 s y pico de proceso 4.451,94 MiB; tiempos sin VAD nuevo, procesos de 17/8 casos y una pasada, no comparación pareada repetida o medida de tablet. Ocho prefijos exactos, modelo/fuentes previas y 66 anclas disponibles verificados; 83 pruebas pasan antes de inferir.

**Comprobación del lector.** Protocolo pruebas/25_final_vad_literal.md, informes/huellas/código en la carpeta del ensayo y visor http://127.0.0.1:8778/ con original completo o prefijo enviado y dos salidas literales claramente identificadas. Pendiente de escucha compartida antes de ampliar o adoptar. Se conservan originales, pausas y límites de marcas automáticas; no se cambia el seguidor ni se publica automáticamente.

**Controles adicionales de pausa larga.** A raíz de la pregunta del usuario se aclara que 3/13 no estaban en la primera tanda y se realizan dos inferencias nuevas con la misma variante, resultados/literalidad/20261025_195038_565692_cola_vad_UTC. Se conservan muestra a muestra las pausas interiores; en 3, flor 11,88→Ana 21,20 s delimita 9,32 s íntegros y tres anclas retenidas. En 13 se conserva la relectura dos veces y el texto completo es idéntico; sus ~8 s son descripción/consigna, sin medida humana precisa. En 3 solo desaparece la etiqueta [throatclearing], sin adjudicarla como correcta o errónea; persisten errores lexicales previos. Entrada 110→73,152 s; inferencia previa/nueva 38,98/21,21 s, carga nueva 7,91 s; 85 pruebas pasan antes de inferir. control_pausas.md/validacion_pausas.json e integridad conservan comprobaciones; visor 8779. Es análisis offline que usa la última voz del archivo, no validación de cierre automático de sesión en directo. Actualización en la misma E060, sin activar ni publicar.

## E061 · Nueva tanda de lecturas: La caja del sendero

**26/10/2026, preparación; ejecución posterior documentada en esta misma entrada.** Se amplía el dataset antes de repetir el lote anterior. Nuevo texto de 98 palabras en datos/textos/lectura_04.txt, conservando lectura_03.txt ya existente. Se preparan seis tomas: normal, cuatro repeticiones de palabras, tres episodios de intentos parciales, dos omisiones/dos sustituciones, pausa aproximada de 8 s con continuación y dificultades mixtas libres. Consignas en lectura_04_tomas.json y protocolo pruebas/26_grabaciones_caja_sendero.md. scripts/grabar_tanda.py reutiliza el grabador existente, espera Enter en cada toma y registra nombres descriptivos reales, cuento y huellas en el catálogo; permite reanudar por número. Verificada la presentación de las seis consignas sin acceder al micrófono.

**Diseño y límites.** Duraciones 90/100/120/90/120/150 s, conservando originales y silencio final. Consignas no equivalen a eventos confirmados; revisión por escucha pendiente antes de contar disfluencias. Tomas 1–4 para desarrollo, 5–6 previstas para validar cambios posteriores sin ajustarlos con ellas; asignación a WAV pendiente de su creación. Un adulto simulando dificultades, mismo texto: no demuestra generalización clínica o infantil. Estado al preparar: sin nuevos WAV ni inferencias; ejecución documentada a continuación. No se publica automáticamente.

**Ejecución y primera comparación, 26/10/2026.** El lector termina seis WAV, 670 s, y confirma las consignas; en la sexta recuerda descubrieron→encontraron una caja..., otra autocorrección no recordada, parciales y velocidades variadas. Se conserva la declaración con huellas sin inventar texto literal ni tiempos. Verificados WAV/catálogo/cuento; nuevo selector por cuento evita repetir los 17 audios anteriores y rechaza textos modificados. Pasan nueve comprobaciones de selección, recursos y prefijos. Lote resultados/literalidad/20261026_081747_630720_UTC: actual/literal completos sobre mismos arrays, inferencia 99,14/213,46 s; seis WAV, trabajador/modelos y 712 fuentes previas intactos. Diagnóstico Silero con ajustes previos, sin anclas humanas nuevas. Contraste resultados/literalidad/20261026_082404_701027_cola_vad_UTC: seis inferencias literales nuevas, 670→419,008 s de entrada, 118,86 s de inferencia y carga 7,60 s. Los seis textos nuevos son prefijos exactos del literal completo: 1/4 idénticos; 2/3 pierden solo ¿Para qué?, 5 P- p. P- p., y 6 la continuación P- por favor...; resto escrito intacto, no garantía de conservar todo el habla real. El literal mantiene las cuatro repeticiones de palabras y roja/parque sin reponer madera/viejo, pero simplifica regres- re- regresar. Ambos conservan descubrieron encontraron en la sexta; parciales adicionales y [yawn] pendientes de escucha. revision_inicial.md documenta prioridades y límites; visores 8780/8781 con audio comprobado. Reserva 5/6 mantenida sin ajustar reglas con ella. Referencia descriptiva del lector, sin WER/F1 ni fidelidad global. Misma E061 en ambos diarios; seguidor sin cambios y sin publicación automática.

**Revisión compartida de intentos y notación.** El lector confirma que en toma 3 falta regres- re- antes de regresar. La causa sigue sin determinarse: simplificación por contexto es hipótesis, no evidencia del mecanismo interno. En toma 6 pregunta cómo interpretar des-/descubrí, Levam/le- y ca-/casa/caja; no se convierten esas grafías automáticamente en intentos validados. Comprobado que trabajador y visor conservan el texto del motor sin añadir guiones: no hay un clasificador propio detrás de esa puntuación. Referencia nueva separada lectura_04_revision_intentos.json, conservando las fuentes congeladas. El lector considera necesario el VAD para finales; se mantiene su utilidad observada como control offline, sin extenderla a habla interna o garantizar ausencia universal de invenciones. Sin inferencias nuevas ni cambio de reglas.

## E062 · Contraste de ajustes para los intentos omitidos

**26/10/2026, siete inferencias completadas; escucha compartida preparada.** Se investiga regres- re- regresar confirmado por el lector en toma 3. Marca ASR orientativa 60,10–60,68 s, dentro del último bloque 52–70,32 s; no tiempo humano. Mismo literal CPU float32/cuatro hilos y prefijos VAD fijados. Tres ablaciones de un parámetro: reparación de repeticiones, temperaturas alternativas y recuperación de cierre, cada una desactivada por separado en tomas 3 y 2 (control de cuatro repeticiones). Diagnóstico adicional del último bloque aislado con ajustes originales, sin contexto textual previo. No se suministra el cuento/palabra objetivo, ni se utilizan las tomas reservadas 5/6. Protocolo pruebas/27_intentos_literal.md; script independiente sin modificar trabajador/modelo habitual.

**Resultados y decisión.** resultados/literalidad/20261026_084437_140574_intentos_UTC conserva fuentes/modelo/arrays con huellas, siete textos brutos/bloques/palabras/recursos y resumen/conclusiones. Las seis salidas de ablación son idénticas a sus referencias: control de palabras repetidas conservado, regres- re- sigue omitido. El recorte también escribe regresar; el bloque nativo previo ya lo simplificaba antes de unir resultados. No se identifica causa ni se demuestra si cada mecanismo se activó en la referencia; el recorte cambia varias condiciones y no permite atribución causal única. Inferencia 108,46 s, carga 6,05 s, pico del proceso 4.403,49 MiB; no benchmark pareado ni rendimiento móvil. Se conservan ajustes originales con control de final, ninguna variante mejora este episodio. Visor de escucha 8782 con fragmento y velocidad 0,4×; tiempos humanos y evaluación por evento pendientes. Decisión del usuario: dejar la omisión de intentos como observación pendiente para cuando se cambie de entorno; no continuar ahora con nuevos ajustes o reconocedores. Comparar entonces el mismo WAV y fragmento con los controles conservados. Sin publicación automática.

## E063 · Estadísticas bajo demanda después de la lectura

**26/10/2026, decisión de diseño del usuario.** Durante la sesión se mantienen grabación y seguimiento; el literal y el cálculo de estadísticas empiezan únicamente cuando el profesor los solicita después de finalizar. Se conserva el original y se procesa una copia; se prevé liberar el modelo del seguidor antes de cargar el literal. Así se evita concurrencia de inferencias, sin afirmar viabilidad o memoria suficiente en tablet. El tiempo de espera y recursos del análisis se medirán aparte. No se ha implementado todavía este flujo ni decidido ejecución remota.

**Fidelidad y medición.** docs/CONSERVACION_DISFLUENCIAS.md recoge el flujo y la conservación temporal: probar limpieza frente al original antes de adoptarla, sin asumir que más filtrado mejora los intentos. VAD final con evidencia exploratoria, manteniendo pausas interiores y cronología original para estadísticas; distinguir duración de sesión/lectura y cola de grabación. Conservar procedencia/parámetros de copias y salidas brutas, revisión de eventos dudosos y mapa temporal si se alteran tiempos. No se ejecutan inferencias nuevas ni se modifican motores o reglas. Registro en ambos diarios, sin publicación automática.

## E064 · Recogida por lotes y pruebas de mayor dificultad

**26/10/2026, preparada; pendiente de grabación.** El usuario decide reunir primero más audios, empezar por seis pruebas exigentes del cuento actual y continuar después con otros textos; el reconocimiento se pospone hasta que indique que ha terminado la recogida. Se verifica el estado de partida: 23 WAV disponibles, 1.550 s de archivo con silencios, tres textos y un adulto. Cantidad de ejecuciones no equivale a nuevas voces/lecturas; un objetivo orientativo de 60–80 audios propios se propone como banco exploratorio, sin umbral científico de suficiencia ni validación de lectores infantiles. Importan cobertura, referencia revisada y reserva de textos/voces.

**Preparación útil.** lectura_04_tomas_limite.json fija cadenas de intentos, sustituciones/autocorrecciones, vuelta atrás de tres frases, frase omitida recuperada fuera de orden, pausas/velocidades y mezcla libre. Duraciones 150/150/180/180/180/180 s, 17 minutos; consignas no son eventos confirmados. scripts/grabar_tanda.py admite --plan y --lector, conserva el plan anterior por defecto y permite listar/reanudar sin iniciar reconocimiento. Verificadas presentación de ambos planes y rechazo de intervalo inválido sin micrófono. Protocolo pruebas/28_tanda_limite.md; nombres Limite 1–6 reales en WAV, originales conservados. Toda esta tanda es exploratoria; se mantiene la reserva anterior. No se crean grabaciones, resultados ASR o publicaciones automáticamente.

**Control de duración solicitado por el usuario.** La tanda activa ahora parada y guardado con Enter; la siguiente toma espera otra pulsación de inicio. El tiempo del plan queda como máximo de seguridad. El grabador guarda solo muestras recibidas y registra su duración real sin relleno; no deja un hilo de entrada esperando al agotarse el tiempo. Cinco pruebas simuladas de captura/configuración pasan sin micrófono: parada manual, límite exacto, rechazo de captura vacía y comportamiento previo del cuento. Protocolos actualizados dentro de esta misma E064; grabaciones anteriores intactas. No se ejecuta ASR ni se publica.

**Tanda de mayor dificultad terminada.** El lector comunica finalización; se verifican seis WAV nuevos con duración real por parada manual, 457,57 s (7 min 37,57 s), nombres/huellas/cabeceras coherentes. Total disponible: 29 grabaciones, 2.007,57 s de archivo (33 min 27,57 s), tres textos y un adulto. En la toma 6 comunica estornudo deliberado cerca del final, sustitución termina→empieza en Busca donde... seguida de relectura íntegra correcta y otras trabadas sin desglose. El estornudo se registra como evento vocal no verbal, separado de errores léxicos/disfluencias; sin tiempos inventados ni validación exhaustiva de las otras consignas. Declaración, consignas y huellas en datos/anotaciones/lectura_04_limite_confirmacion.json; catálogo actualizado. Las nuevas tomas son de desarrollo y la reserva anterior se mantiene. No se ejecuta ASR: esperar a que el usuario cierre la recogida completa antes de fijar el lote. Misma E064 en ambos diarios.

## E065 · Primera tanda del texto 3: controles y dificultad creciente

**26/10/2026, preparada; pendiente de grabación.** A petición del usuario se conserva lectura_03.txt (77 palabras, El tren y el pañuelo verde) y se preparan doce consignas en lectura_03_tomas.json: normal/lenta/rápida, palabras repetidas, cadenas parciales, omisiones, sustituciones/autocorrección, pausa larga, relectura lejana, frase recuperada fuera de orden, carraspeo y mezcla libre. La frase El tren llegó a la estación aparece dos veces en el cuento: no etiquetar por sí sola esa repetición como disfluencia. La relectura lejana termina en andén, no en el final original casa.

**Registro y límites.** Protocolo pruebas/29_tanda_texto_03.md y nombres reales Tren 01–12. Se reutiliza el grabador de tandas con Enter para iniciar/terminar y reanudación por número. Máximos acumulados 1.590 s, no duración obligatoria; se verifican las doce consignas sin activar micrófono. Todas son exploratorias de desarrollo, sin modificar reservas anteriores. No se asumen hechos pronunciados hasta confirmación/escucha; evento no verbal separado de errores léxicos. Sin WAV nuevos, inferencias ni publicación automática: esperar al cierre de la recogida completa. El estado disponible sigue siendo 29 grabaciones.

**Tanda completada.** El lector comunica Tanda completa. Se comprueban doce WAV disponibles del texto 3, con huellas, cuento y duraciones coherentes en catálogo y cabeceras PCM16 mono; suman 562,44 s (9 min 22,44 s). El banco disponible pasa a 41 audios, cuatro textos y 2.570,00 s de archivo (42 min 50 s), un adulto. Declaración y consignas previstas enlazadas a cada huella en datos/anotaciones/lectura_03_tanda_confirmacion.json. La finalización no confirma automáticamente eventos, lectura exacta, tiempos o ausencia de desviaciones; no se inventa transcripción. Catálogo actualizado como desarrollo, conservando reservas anteriores. Sin nuevas inferencias: esperar al cierre de la recogida completa indicado por el usuario. Misma entrada E065 en ambos diarios.

## E066 · Texto más largo: El recuerdo del banco azul

**26/10/2026, preparado; pendiente de grabación.** Se crea lectura_05.txt, texto original de 250 palabras en cinco párrafos. Plan lectura_05_tomas.json con ocho tomas: normal/lenta/rápida, intentos repartidos, omisiones/sustituciones, pausa aproximada de 15 s, relectura del tercer párrafo tras terminar y mezcla libre. La frase La puerta estaba cerrada se repite legítimamente en dos lugares. En la relectura el destino previsto es ventana; no asumir final del cuento como objetivo de toda la toma.

**Captura y alcance.** Protocolo pruebas/30_tanda_texto_largo.md; nombres Biblioteca 01–08. Enter inicia/termina y registra duración real. Se amplía el límite admisible a 600 s; la toma lenta permite 480 s para no truncar una lectura extensa. Máximos del plan suman 2.880 s, sin obligación de agotarlos. Se comprueban ocho consignas sin micrófono y captura simulada. Se conservan cuentos, WAV y reservas previos; nuevas tomas exploratorias de desarrollo, aún sin grabar ni referencias humanas. El procesamiento seguirá pendiente hasta cierre de recogida por el usuario; duración mayor no implica una sola ventana interna, crecimiento lineal del coste o fidelidad garantizada. Registro en ambos diarios, sin publicación automática.

**Tanda larga completada.** El lector comunica Tanda terminada. Se verifican ocho WAV disponibles del texto 5, con huellas, cuento y duraciones coherentes con cabeceras mono PCM16; suman 1.351,97 s (22 min 31,97 s), incluyendo 339,18 s de lectura lenta y 289,25 s de mezcla libre. El banco disponible pasa a 49 audios propios, cinco textos y 3.921,97 s de archivo (1 h 5 min 21,97 s), un adulto. Declaración de finalización, consignas previstas y huellas por toma en datos/anotaciones/lectura_05_tanda_confirmacion.json; no se presupone que cada evento ocurra exactamente ni se inventan marcas humanas. Catálogo actualizado como desarrollo, manteniendo reservas anteriores. No se ejecuta ASR: esperar a que el usuario cierre la recogida completa. Actualización dentro de la misma E066 en ambos diarios.

## E067 · Preselección pública de reconocedores y comparación propia posterior

**28/10/2026, revisión de fuentes y decisión metodológica.** El usuario comunica el criterio del profesor: usar un dataset externo para preseleccionar ASR y el corpus propio para elegir entre finalistas. Se registra en docs/DATASET.md sin reinterpretar ensayos previos como evaluación ciega. Instalados solo Whisper Small y CrisperWhisper Small; candidaturas propuestas (no descargadas) wav2vec2/XLSR español CTC, Vosk español Small y Parakeet TDT v3. La ficha de Parakeet limita uso literal/incompleto; no inferir conservación de trabadas de un buen WER. Separar selección de modelo, backend, precisión y dispositivo.

**Datos y controles.** Fichas oficiales de FLEURS es_419 y MLS español revisadas y añadidas a datos/externos/FUENTES.json, sin descargas. Propuesta FLEURS para primera selección, Common Voice como diversidad adicional y MLS como fragmentos de audiolibros. Fijar muestra/partición/IDs/normalización y recursos comparables; auditar contaminación por entrenamiento (XLSR declara Common Voice 6.1). Retener finalistas por precisión/coste y luego evaluar eventos literales/seguimiento con referencias propias revisadas. No presentar todo el banco como test independiente: hay audios ya usados para desarrollo y reservas que conservar. Las nuevas tandas siguen sin procesar hasta cierre de recogida del usuario. Ambas ramas pueden requerir elecciones distintas. Sin modelos instalados, inferencias nuevas o publicación automática; actualización en ambos diarios.

## E068 · Importación y verificación local de FLEURS español

**28/10/2026, completada.** A petición del usuario se copian desde Descargas los tres paquetes y tres TSV de FLEURS es_419 a datos/externos/descargas/fleurs_es_419, conservando los originales descargados y comprimidos. Carpetas por dataset; mls_es preparada, descarga MLS en curso según el usuario y sin tocar. Scripts/importar_fleurs.py restringe rutas/tipos de tar, impide sobrescribir importaciones y verifica copias/CRC; tres pruebas de seguridad pasan. Fuente exacta y huellas conservadas, sin instalar dependencias.

**Evidencia.** 408 dev (4.871,58 s), 908 test (11.126,10 s), 2.796 train (31.699,92 s): 4.112 WAV FLOAT mono a 16 kHz, 47.697,60 s (13 h 14 min 57,6 s). Todos decodificados completos y coincidentes con filas/número de muestras TSV; sin faltantes/sobrantes, valores no finitos, archivos enteramente silenciosos ni huellas de audio idénticas entre particiones. Índice local por WAV y resumen en datos/externos/fleurs_es_419_verificacion.json; FUENTES.json actualizado con estado/rutas y huellas. Integridad local, sin cotejo de hashes publicados ni certificación de fidelidad textual o independencia de entrenamiento. Datos externos excluidos de Git. No se ejecuta ASR, no se altera el banco propio ni se selecciona todavía una muestra. Registro en ambos diarios, sin publicación automática.

**Reubicación solicitada por el usuario.** Los datasets pasan directamente a datos/externos/fleurs_es_419 y datos/externos/mls_es. Se mueven primero ambas carpetas y se elimina solo descargas vacía, verificando límites del proyecto. Registro de fuentes, índice, informes y futuro importador actualizados; se conserva la fuente exacta histórica y copia de metadatos anterior. Las 4.112 huellas de audio y las seis de entrada permanecen idénticas. Exclusiones de Git adaptadas antes del movimiento. MLS continúa pendiente y no se toca su descarga. Actualización en la misma E068 de ambos diarios.

## E069 · Instalación aislada de los tres candidatos ASR

**28/10/2026, completada y comprobada.** El usuario autoriza instalar reconocedores mientras continúa la preparación de datasets. Nuevo entorno .tools/asr-candidatos-env, Python 3.12.15 y 63 paquetes fijados en requirements-asr-candidatos-lock.txt: PyTorch 2.14.1+cpu, Transformers 5.20.2, Vosk 0.3.45 y librosa 1.0.0, entre otros. No se modifican .venv/literal-env ni Whisper/CrisperWhisper. Modelos locales XLSR español (96d7e9b4…), Vosk Small es 0.42 y Parakeet TDT v3 (541d1f99…); revisiones completas, licencias y huellas por archivo en resultados/instalacion_asr/20261028_candidatos_cpu. Descargas oficiales; cotejo LFS cuando existe y CRC/huellas locales Vosk; ZIP con rutas restringidas y dos pruebas de seguridad correctas. Pesos/cachés/entorno excluidos de Git, sin publicar.

**Configuración y límites.** XLSR preparado como CTC greedy sin LM externo, Vosk con su grafo y Parakeet mediante Transformers/TDT; CPU float32 y cuatro hilos Torch en los dos modelos neuronales, hilos nativos Vosk no fijados. Cada candidato supera carga y ejecución/decodificación con un segundo sintético de ceros, sin micrófono, grabaciones propias o datasets. Recursos capturados solo como comprobación técnica, no rendimiento comparativo o de tablet; las tareas de descompresión pueden coexistir. Fuentes exactas de descarga/pruebas y resultados finales conservados. docs/RECONOCEDORES_CANDIDATOS.md documenta comandos y la configuración explícita del procesador XLSR. Ningún modelo se activa ni se declara ganador: faltan preselección pública y comparación propia con muestras/configuraciones fijadas. Registro en ambos diarios.

## E070 · Grabación individual con selección de texto y lector

**28/10/2026, preparado y comprobado.** Nuevo selector scripts/grabar_lector.py para recoger voces de varios lectores: elige uno de los cinco textos, ID del lector, tipo de lectura y ambiente opcional. Una sola grabación por ejecución, inicio y final con Enter y máximo de seguridad de diez minutos; reutiliza la captura existente. Nuevos nombres WAV: tipo - lectura_NN - fecha - lector; sufijo adicional ante colisión, sin renombrar archivos históricos. El catálogo conserva lector, identidad estable, texto y huella, con contenido pendiente de revisión. Instrucciones en docs/GRABAR_LECTORES.md. Doce comprobaciones correctas del selector, catálogo y captura manual: selección transmitida, ejecución única y preservación de audio/referencias. Sin activar micrófono durante las pruebas, inferencias o publicación. Ambos diarios actualizados.

## E071 · Nombres homogéneos del banco de audios

**29/10/2026, completado.** Los 57 WAV disponibles pasan al formato descripción de la lectura - lectura_NN - fecha - lector_NN. Se retiran prefijos de tanda como Biblioteca/Tren/Limite y títulos redundantes, conservando las condiciones particulares y fechas. El lector original adulto_01 se normaliza a lector_01 y lector_2…9 a lector_02…09; IDs previos conservados en el catálogo. scripts/unificar_nombres_audio.py ofrece vista previa, detecta colisiones, conserva un respaldo local y aliases para resolver nombres históricos. El registro de nuevas tomas también normaliza IDs numéricos. Comprobaciones: seis pruebas del selector/nombres correctas, 57 huellas WAV idénticas antes/después, referencias históricas de audios disponibles resolubles y segunda planificación sin cambios de nombre. Los JSON originales de experimentos no se reescriben. Sin reconocimiento ni publicación. Registro en ambos diarios.

## E072 · Publicación del avance y protección de voces de otros lectores

**29/10/2026.** El usuario autoriza publicar el avance pendiente, limitando los audios a lector_01, y aclara que sí pueden publicarse resultados anónimos de los otros lectores. Se excluyen por defecto todos los archivos de datos/audio salvo WAV del lector_01, todos los directorios de datasets externos y el catálogo completo local. El catálogo público contiene solo entradas del lector original; lectura/registro/migración y snapshots usan el catálogo local cuando existe, conservando el trabajo con todos los lectores. exportar_catalogo_publico.py genera la copia publicable sin modificar la selección privada. No se ejecuta ASR sobre nuevos audios para esta publicación. Diario alternativo, pesos, entornos, cachés y respaldos siguen fuera del repositorio.

## Formato de futuras entradas (plantilla)

### E073 · Título del siguiente cambio o experimento

- Fecha y estado.
- Objetivo o pregunta.
- Cambios y configuración.
- Evidencia y procedencia de la referencia.
- Resultados, interpretación y límites.
- Decisión y siguiente comprobación.

Este último bloque es una plantilla, no un experimento ya realizado.
