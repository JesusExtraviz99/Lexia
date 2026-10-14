# Informe de investigación: lectura asistida

**Autor:** Jesús Extraviz Suárez  
**Fecha:** 9 de octubre de 2026    
**Contexto:** investigación previa al desarrollo durante las prácticas y continuación en el TFG.

**Estado de la investigación:** fichas de datasets consultadas el 9 de octubre de 2026. Los corpus no se han descargado ni auditado y sus licencias no se han tramitado.

## 1. Objetivo y alcance

El objetivo es recopilar métodos, herramientas, modelos y datasets que puedan ayudar a construir una aplicación de lectura asistida para alumnos hispanohablantes. El informe reúne aportaciones de distintos trabajos para diseñar una combinación que podamos implementar y evaluar.

Las necesidades principales son:

- Escuchar al alumno mientras lee un cuento conocido por la aplicación.
- Seguir su posición y actualizar el subrayado con poco retraso.
- Recuperar el seguimiento ante repeticiones, errores, omisiones y retrocesos.
- Obtener estadísticas finales sobre la lectura.

El núcleo técnico puede utilizarse tanto en práctica individual como en sesiones grupales con un lector activo seleccionado por el docente. En las pruebas iniciales se priorizará una sesión con un único lector.

Esta versión recoge antecedentes y alternativas. No contiene resultados de nuestra aplicación ni una selección definitiva de tecnologías. La gestión completa de usuarios, clases y materiales queda fuera de esta revisión técnica.

## 2. Distinciones fundamentales

### 2.1. Reconocimiento, seguimiento y evaluación

| Función | Pregunta que resuelve | Resultado esperado |
|---|---|---|
| Reconocimiento del habla | ¿Qué ha pronunciado el alumno? | Palabras, fonemas o características del audio. |
| Seguimiento | ¿En qué posición del texto está leyendo? | Posición estimada y actualización del subrayado. |
| Evaluación | ¿Cómo ha leído? | Errores, autocorrecciones, pausas y otras estadísticas. |

**Aceptar un intento para avanzar el cursor no significa considerar que la palabra se ha leído correctamente.** El seguimiento debe poder continuar cuando el alumno se equivoca; la evaluación registra ese intento de forma independiente.

### 2.2. Hipótesis parciales y resultados definitivos

Los reconocedores pueden producir transcripciones provisionales que cambian al recibir más audio. Por ello, una buena transcripción final no demuestra que el subrayado haya funcionado correctamente durante la lectura. Deben evaluarse tanto las actualizaciones en directo como el resultado posterior.

### 2.3. Fonemas y caracteres

La comparación fonética trabaja con sonidos, no con letras ni sílabas. Por ejemplo, «sí» contiene los fonemas /s/ e /i/. Si se utiliza Levenshtein para comparar fonemas, estos deben representarse como elementos de una secuencia: un símbolo fonético puede ocupar varios caracteres informáticos.

Convertir a fonemas una transcripción del ASR tampoco recupera los errores que el reconocedor haya corregido u omitido. Para evaluar pronunciación se debe investigar una salida fonética o un método que analice directamente el audio.

## 3. Trabajos revisados

Se revisan seis trabajos sobre seguimiento, reconocimiento y evaluación de la lectura infantil. Los ejemplos en español son ilustrativos y no pertenecen a los experimentos originales. Las propuestas de adaptación requieren implementación y validación; las cifras corresponden a cada estudio y no son resultados de nuestra aplicación.

### 3.1. Li y Mostow (2012): evaluación del seguimiento en tiempo real

**Título:** *Evaluating and improving real-time tracking of children’s oral reading*.  
**Autores:** Yuanpeng Li y Jack Mostow.  
**Publicación:** FLAIRS-25, 2012.  
**Fuente:** Publicación de referencia [1]. [Publicaciones oficiales de Project LISTEN](https://www.cs.cmu.edu/~listen/pubs.html).

#### Problema que estudia

El artículo analiza un problema directamente relacionado con nuestro subrayado: **obtener una transcripción final razonablemente buena no significa que el sistema haya señalado correctamente las palabras mientras el niño leía**.

Un tutor utiliza el reconocimiento automático del habla —ASR— para estimar qué palabras se están pronunciando. Después relaciona esas palabras con el texto presentado. Sin embargo, durante la lectura el reconocedor produce hipótesis parciales, es decir, resultados provisionales que pueden cambiar al recibir más audio. Una palabra puede aparecer demasiado pronto, desaparecer en una actualización o ser sustituida por otra. También pueden cambiar los tiempos que el sistema le asigna.

Esto tiene dos consecuencias. La primera es visual: un cursor que salta o se queda atrás puede distraer al alumno y hacerle perder su posición. La segunda afecta a la evaluación: si el sistema cree que el alumno está leyendo otra palabra, puede marcar como incorrecta una pronunciación que correspondía a la posición real.

#### Cómo explican la inestabilidad del reconocimiento

Los autores describen un ciclo de seis fases que ayuda a entender lo que sucede en el extremo más reciente de una hipótesis:

1. **Detección:** se acumula evidencia acústica y comienza a aparecer una palabra candidata.
2. **Propuesta con evidencia insuficiente:** esa candidata puede ser incorrecta porque todavía se ha escuchado poco audio.
3. **Reconocimiento prematuro:** la palabra puede ser la correcta, aunque el alumno aún no haya terminado de pronunciarla.
4. **Reconocimiento correcto:** al llegar al final de la pronunciación, la estimación temporal puede coincidir con la palabra real.
5. **Prolongación indebida:** mientras llega el siguiente sonido, el sistema puede seguir atribuyéndoselo a la palabra anterior y alargar su duración estimada.
6. **Recuperación:** cuando reconoce la siguiente palabra, reajusta el final de la anterior; entretanto, el ciclo comienza de nuevo.

Por ejemplo, si el alumno empieza a decir «mariposa», reconocer la palabra después de escuchar «mari…» puede servir para anticipar su posición. Pero no permite asegurar que haya pronunciado correctamente el resto. Esta diferencia resulta relevante para separar el movimiento del cursor de la puntuación final.

#### Método de evaluación y propuesta

El estudio compara la posición estimada con una referencia humana alineada temporalmente. En lugar de reconstruir todo el recorrido a partir de la transcripción definitiva, utiliza las hipótesis que realmente estaban disponibles durante la lectura.

Define dos métricas:

- **Precisión exacta:** porcentaje de tiempo durante el cual la posición estimada coincide con la posición real.
- **Precisión aproximada:** porcentaje de tiempo durante el cual la diferencia es de una palabra como máximo.

La propuesta consiste en estudiar cuánto mejora la estimación de la posición en un instante `t` si se utiliza evidencia disponible un poco después, en `t + desfase`. No elimina la espera: cuantifica el compromiso entre disponer de más información y responder rápidamente.

Además, calcula resultados por estudiante para evitar que los niños que aportan más lectura dominen la evaluación global.

#### Datos y resultados

El conjunto contiene **2.033 enunciados de 80 niños**, 40 niñas y 40 niños, y aproximadamente **2,95 horas de audio**.

| Evidencia utilizada | Precisión exacta global | Precisión aproximada global |
|---|---:|---:|
| Sin desfase adicional | 58,1 % | 81,6 % |
| Desfase de 0,1 s | 66,1 % | 82,6 % |
| Desfase de 0,2 s | 70,2 % | 83,6 % |
| Desfase de 0,5 s | 72,9 % | 85,2 % |
| Hipótesis final | 75,6 % | 87,3 % |

La mayor parte de la mejora inicial de precisión exacta aparece con una espera pequeña: entre 0 y 0,2 segundos aumenta **12,1 puntos porcentuales**. La precisión aproximada mejora menos porque ya acepta el caso frecuente de que el reconocedor vaya una palabra por detrás.

El estudio también distingue lectura y habla ajena a la tarea. Un **17,6 %** del habla del conjunto corresponde a conversaciones, tarareos u otras emisiones. Cuando el niño no está leyendo, su posición debería permanecer estable, pero el ASR puede intentar encajar esos sonidos en palabras del texto y provocar saltos. Considerando solo el habla relacionada con la lectura, la precisión exacta pasa del **63,4 % al 77,3 %** con 0,2 segundos de desfase.

#### Aportaciones para nuestro proyecto

La aportación principal es una **metodología para medir el subrayado tal como lo ve el alumno**. Deberíamos guardar las hipótesis parciales y el momento de cada actualización, además de la transcripción final. Esto permitiría identificar adelantos, retrasos, cambios bruscos y errores de posición.

También justifica comparar varias políticas de actualización: avanzar inmediatamente, esperar una confirmación o introducir una espera breve. Podríamos medir cuánto mejora cada política y cuánto retraso añade al sistema completo.

El habla ajena a la lectura debería formar parte de las pruebas. Detectar actividad vocal no bastaría para resolverlo: una conversación también contiene voz. Habría que comprobar si la emisión es compatible con la lectura antes de modificar la posición.

#### Límites y comprobaciones pendientes

Los **200 ms no son una latencia universal recomendada**, ni incluyen por sí solos captura de audio, envío, inferencia y actualización de pantalla. El resultado procede de un sistema y unos datos concretos.

También debemos definir qué señala nuestro indicador: la palabra pronunciada actualmente, la última reconocida o la siguiente que debe leerse. Las métricas solo tendrán sentido si esa convención está fijada de antemano.

### 3.2. Yılmaz, Van Compernolle y Van hamme (2012): seguimiento robusto mediante comparación fonética

Referencia bibliográfica: [2].

**Título:** *Robust Tracking for Automatic Reading Tutors*.  
**Autores:** Emre Yılmaz, Dirk Van Compernolle y Hugo Van hamme.  
**Publicación:** Interspeech 2012.  
**Fuente:** [PDF oficial](https://www.isca-archive.org/interspeech_2012/yilmaz12_interspeech.pdf). DOI: 10.21437/Interspeech.2012-247.

#### Problema que estudia

El artículo busca que el cursor siga al niño con un ritmo adecuado, incluso cuando duda, pronuncia mal o se salta palabras. Seguir directamente la posición interna del reconocedor puede producir movimientos tardíos o saltos prematuros. Exigir una coincidencia demasiado estricta también puede bloquear el cursor.

La investigación compara tres estrategias y muestra que una **combinación de evidencia fonética local y recuperación de posición** funciona mejor que cualquiera de las estrategias simples evaluadas.

#### Información que utiliza el sistema

El reconocedor proporciona tanto una estimación de la posición como una secuencia de sonidos reconocidos. El artículo distingue una parte estable del recorrido de reconocimiento y una parte correspondiente a la hipótesis más probable, todavía susceptible de cambiar.

Por otra parte, el texto conocido dispone de transcripciones fonéticas: las secuencias de sonidos esperados de sus palabras. El seguidor compara esos sonidos con los reconocidos. Por tanto, no se trata simplemente de comparar letras de una transcripción automática.

#### Los tres métodos comparados

**1. Seguimiento basado en estados.** El cursor avanza cuando la posición estimada por el reconocedor supera la posición actual. Solo se mueve hacia delante. Puede funcionar bien cuando hay silencios entre palabras, pero en lectura continua suele reaccionar tarde. Los cambios abruptos de estimación también pueden adelantarlo incorrectamente.

**2. Comparación fonética simplificada.** Busca una coincidencia suficiente entre la pronunciación esperada de la palabra resaltada y los sonidos reconocidos. Esto permite avanzar antes de esperar una palabra completa en algunos casos y tolerar pequeñas diferencias. Sin embargo, si el niño omite la palabra o la pronuncia de manera muy distinta, puede quedarse esperando indefinidamente.

**3. Comparación fonética avanzada.** Mantiene el criterio fonético, pero incorpora la posición estimada por el reconocedor como mecanismo de recuperación. Si la comparación local falla y existe evidencia persistente de que el lector está más adelante, el cursor recupera el seguimiento.

#### Funcionamiento de la comparación fonética

Se utiliza programación dinámica para buscar la secuencia esperada dentro de la cadena de sonidos reconocidos. La búsqueda puede comenzar en distintas posiciones, porque esa cadena también puede contener sonidos de palabras anteriores, silencios e intentos fallidos.

La distancia penaliza **inserciones, eliminaciones y sustituciones**. En la configuración evaluada, cada una cuesta 1 y una coincidencia cuesta 0. Es una comparación basada en distancia de edición, con inicialización adaptada a buscar una coincidencia local. El cálculo puede actualizarse con vectores de distancia, sin almacenar todo el historial de una matriz de alineamiento.

Los criterios de avance son:

- Para palabras de **dos fonemas**, exigir coincidencia exacta.
- Para las demás, aceptar una distancia de Levenshtein **menor o igual que 1**.
- Exigir que se haya reconocido la **primera vocal** de la palabra, reduciendo avances debidos a sonidos fácilmente insertados por ruido.

Ejemplo ilustrativo: entre `/s/, /o/, /l/` y `/s/, /o/` hay una eliminación y, por tanto, distancia 1. Un criterio permisivo puede reconocer un intento suficiente para avanzar antes del último sonido. Eso **no demuestra que la palabra se haya leído completa o correctamente**.

Tras un movimiento se retiran los sonidos del recorrido estable para evitar confundir una aparición anterior de la misma palabra con una nueva lectura.

#### Recuperación del seguimiento

La versión avanzada consulta la posición estimada **cada 150 ms**. Cuando el reconocedor indica **tres veces consecutivas la misma palabra situada más adelante**, el cursor pasa a la palabra posterior a esa estimación. El artículo describe esta comprobación como una persistencia de aproximadamente **450 ms**.

La finalidad es evitar que una única hipótesis provisional provoque un salto. La comparación fonética permite un avance local rápido y la persistencia de posición permite recuperarse cuando esa comparación no encuentra una coincidencia.

Estos seguidores muestran un cursor que solo avanza. Por tanto, la robustez ante relecturas no debe confundirse con representar visualmente todos los retrocesos del alumno.

#### Datos, evaluación y resultados

Se utilizan **279 sesiones de CHOREC**, con nueve relatos de **103 a 223 palabras**. El corpus completo contiene lectura de 400 niños de primaria de habla neerlandesa; ese número no debe confundirse con el de sesiones del experimento.

La referencia incluye límites temporales de palabras y anotaciones de errores. El estudio define **TAT**, precisión temporal del seguimiento, como la proporción de movimientos que caen en el intervalo aceptado: aproximadamente desde **0,3 segundos antes hasta 0,1 segundos después** del instante ideal. El margen es asimétrico porque el cursor puede señalar la siguiente palabra tras escuchar suficiente parte de la actual.

| Método | TAT | Casos muy tardíos | Casos muy tempranos |
|---|---:|---:|---:|
| Basado en estados | 32,36 % | 202 | 768 |
| Fonético simplificado | 50,63 % | 4.229 | 145 |
| Fonético avanzado | 81,03 % | 189 | 504 |

Los **4.229 casos muy tardíos** del método simplificado incluyen palabras que no llegan a resaltarse porque el cursor se bloquea. La recuperación reduce mucho este problema, aunque la versión avanzada todavía presenta avances excesivamente tempranos. Además, **244 de las 279 sesiones** superan un 70 % de precisión temporal con el método avanzado.

#### Aportaciones para nuestro proyecto

Podríamos adaptar la separación entre **avance local** y **recuperación global**. Primero se comprobaría la coincidencia cerca del cursor; si falla durante un tiempo, se buscaría una posición alternativa estable dentro del texto.

La comparación fonética ofrece un criterio interpretable, y el cálculo incremental puede ser interesante para actualizaciones frecuentes. El experimento también demuestra que no todos los trabajos se limitan a palabras aisladas: aquí se evalúan relatos, aunque de extensión moderada.

Deberíamos registrar por separado el intento pronunciado y la decisión de avance. Si el niño omite una palabra y el cursor se recupera, esa omisión debe conservarse para las estadísticas.

#### Límites y comprobaciones pendientes

Necesitamos comprobar si el ASR elegido ofrece fonemas y una posición comparable a la del reconocedor del artículo. Convertir posteriormente palabras reconocidas a fonemas no recupera los errores que el ASR haya corregido u omitido.

Los umbrales, la primera vocal y los tiempos deben probarse en español. También habrá que decidir qué hacer con palabras de un fonema, palabras largas, pronunciaciones dialectales, repeticiones y saltos fuera del fragmento activo. Copiar el umbral sin estudiar estos casos podría causar falsos avances o bloqueos.

### 3.3. Vidal y colaboradores (2025): ASR sensible a disfluencias en lectura infantil en español

Referencia bibliográfica: [3].

**Título:** *Improving Automatic Speech Recognition for Children’s Reading Assessment with Disfluency-aware Language Models*.  
**Autores:** Jazmín Vidal, Luciana Ferrer, Juan Esteban Kamienkowski y Pablo Riera.  
**Publicación:** Interspeech 2025.  
**Fuente:** [Artículo y PDF oficial](https://www.isca-archive.org/interspeech_2025/vidal25_interspeech.html). DOI: 10.21437/Interspeech.2025-936.

#### Problema que estudia

Un reconocedor entrenado con habla fluida puede producir una transcripción limpia, pero eliminar precisamente las señales que interesan al evaluar lectura: repeticiones, intentos incompletos, errores y autocorrecciones.

El trabajo parte de una ventaja: **se conoce el texto que debe leerse**. Ese texto puede guiar el reconocimiento, pero una restricción demasiado fuerte puede hacer que el sistema devuelva lo esperado aunque el alumno haya dicho otra cosa. Los autores investigan cómo incorporar desviaciones plausibles a la decodificación.

#### Datos y anotaciones

El conjunto contiene **1.327 estudiantes hispanohablantes de 8 a 13 años**, que leen un texto adecuado a su nivel durante aproximadamente un minuto. Se reúnen **13.043 oraciones**. Las grabaciones se obtienen en aulas y con distintos móviles, por lo que varían el ruido, la calidad y los formatos de audio.

Las transcripciones humanas intentan recoger lo pronunciado, incluidas las disfluencias. Para 450 alumnos se anotan tipos específicos. Aproximadamente el **10 % de las palabras** y el **45 % de las oraciones** contienen disfluencias.

| Categoría | Qué representa | Ejemplo ilustrativo |
|---|---|---|
| Sustitución, SUB | Otra palabra o pronunciación muy incorrecta | «casa» en lugar de «cama» |
| Error fonético, PHO | Desviación leve de pronunciación | Un sonido de la palabra cambiado |
| Repetición, REP | Relectura de palabras del texto | «el gato, el gato duerme» |
| Inserción, INS | Palabra adicional | «el pequeño gato» si «pequeño» no aparece |
| Omisión, DEL | Palabra no leída | Saltarse «gato» |
| Palabra truncada, CUT | Intento dejado incompleto | «mari…» sin completar «mariposa» |
| Intento previo a autocorrección, PRE | Intento erróneo seguido del correcto | «mari… mariposa» o «casa… cama» |

PRE se subdivide en **PRECUT**, truncamiento seguido de corrección, y **PRESUB**, sustitución seguida de corrección. Registrar la autocorrección permite diferenciar un error mantenido de un intento que el alumno resuelve.

#### Generación de disfluencias con disfluentES

Los autores desarrollan **disfluentES**, una herramienta abierta que genera variantes textuales de lectura a partir del texto correcto. Utiliza reglas y análisis lingüístico para crear repeticiones, omisiones, inserciones, sustituciones, palabras truncadas y autocorrecciones.

Emplea **spaCy** para etiquetar categorías gramaticales y **mlconjug3** para cambios de conjugación. También contempla modificaciones de concordancia y repeticiones de varias palabras. Las variantes sirven para entrenar un modelo de lenguaje específico del texto.

Es importante precisar que **genera texto, no audio**. Puede ayudar a representar posibles errores en un decodificador, pero no sustituye grabaciones infantiles para evaluar el reconocimiento acústico.

#### Modelo acústico y decodificación

El modelo acústico es un **Wav2Vec2.0 con CTC a nivel de caracteres**, basado en `wav2vec2-large-xlsr-53` y adaptado previamente con unas 944 horas de español del proyecto CIEMPIESS-UNAM.

El decodificador se implementa con **K2** y transductores de estados finitos, combinando:

- **H:** topología CTC, que relaciona salidas temporales con secuencias de símbolos.
- **L:** léxico, que relaciona símbolos con palabras.
- **G:** gramática, que restringe y pondera secuencias posibles.

Comparan dos formas de construir G:

1. **Modelos de lenguaje n-grama:** aprendidos con textos correctos o variantes sintéticas. Se construyen mediante **KenLM**, con suavizado **Kneser-Ney**. Los 3-gramas funcionan igual o mejor que los 5-gramas en la mayoría de los casos evaluados.
2. **Grafos específicos de la tarea, TSL:** contienen el camino correcto y alternativas explícitas para omisiones, truncamientos, autocorrecciones por truncamiento y repeticiones de una o dos palabras. Los pesos de esas alternativas se ajustan mediante búsqueda aleatoria y validación.

El grafo no obliga a una lectura perfecta. Por ejemplo, debe permitir que «cómo es la experiencia» se lea con una repetición inicial o un intento incompleto antes de «experiencia».

#### Alineamiento y métricas

Se alinean tres secuencias: **texto esperado, transcripción humana y transcripción automática**. Utilizan alineamiento múltiple de secuencias —MSA— con heurística de estrella central, el texto esperado como ancla y alineamientos por pares basados en **Needleman-Wunsch** y semejanza de Levenshtein.

Esto permite distinguir:

- Una palabra bien leída y aceptada correctamente.
- Una palabra bien leída que el sistema rechaza: falsa alarma.
- Una palabra mal leída que el sistema acepta: error ocultado.
- Una palabra mal leída que el sistema detecta como incorrecta.

Además de **WER**, miden errores de aceptación y rechazo mediante **BER**, y la calidad del diagnóstico mediante **DER**. En este artículo, BER se define como la **suma** de la tasa de falsas aceptaciones y la de falsos rechazos; hay que conservar esa definición para reproducir sus resultados.

También consideran las **palabras correctas por minuto, CWPM**. Una estimación total aparentemente buena puede esconder errores compensados: rechazar unas palabras correctas y aceptar otras incorrectas puede dejar casi igual el recuento final. Por eso no basta con comparar únicamente el total.

#### Resultados y lecciones

Los mejores n-gramas sintéticos incluyen **repeticiones y omisiones**. Incorporar más categorías no siempre ayuda: las inserciones y sustituciones generadas amplían las palabras candidatas y pueden aumentar errores de reconocimiento.

El grafo **RepPreDelTSL** destaca en la clasificación correcto/incorrecto y en diagnóstico. Como ejemplo, en tercero reduce BER de **13,3 % con Whisper Large-v3 a 4,9 %**, y DER de **36,3 % a 17,9 %**. En octavo, BER pasa de **13,7 % a 9,7 %** y DER de **40,0 % a 27,7 %**. Son comparaciones del estudio, no rendimiento esperado en nuestra aplicación.

Los pesos óptimos del grafo no coinciden simplemente con las frecuencias observadas de cada disfluencia. También resulta **inconclusa** la mejora por ajuste fino del modelo acústico: ayuda en algunos escenarios, pero no en otros.

Para tratar el ruido utilizan **FullSubNet** y evalúan la señal con **DNSMOS**, obteniendo una mejora relativa del 27 % en el indicador SIG de calidad de voz. Esta cifra describe calidad de señal; no significa una reducción del 27 % de los errores de lectura o de ASR.

#### Recursos y aplicación a nuestro proyecto

Se publican [disfluentES](https://github.com/habla-liaa/disfluentES) y [transcripciones anotadas](https://zenodo.org/records/15522540). Los audios originales no se comparten por restricciones de confidencialidad.

La aportación más útil es **guiar el ASR con el cuento sin borrar las desviaciones del lector**. Podemos investigar decodificadores que permitan repeticiones, omisiones e intentos truncados, y utilizar las etiquetas para diseñar las estadísticas finales.

Sin embargo, el artículo evalúa reconocimiento y puntuación de lectura; no demuestra que su sistema actualice un cursor con la latencia que necesitamos. El uso incremental de grafos, el tamaño del contexto y el alineamiento de hipótesis parciales deberán probarse específicamente con cuentos completos.

### 3.4. Gao y colaboradores (2024): detección de errores lectores mediante ASR

Referencia bibliográfica: [4].

**Título:** *Reading Miscue Detection in Primary School through Automatic Speech Recognition*.  
**Autores:** Lingyun Gao, Cristian Tejedor-Garcia, Helmer Strik y Catia Cucchiarini.  
**Publicación:** Interspeech 2024.  
**Fuente:** [Artículo y PDF oficial](https://www.isca-archive.org/interspeech_2024/gao24d_interspeech.html). DOI: 10.21437/Interspeech.2024-1180.

#### Preguntas que plantea

El estudio pregunta cómo reconocen el habla infantil los modelos entrenados principalmente con adultos y hasta qué punto sus transcripciones permiten detectar errores lectores. Su principal interés para nosotros es que **el modelo que mejor transcribe no tiene por qué ser el que mejor detecta las dificultades del alumno**.

Una salida puede parecer correcta porque el reconocedor elimina un intento fallido. Eso mejora la limpieza del texto, pero hace perder información para evaluar lectura.

#### Datos y modelos comparados

Utiliza lectura en neerlandés del corpus **Jasmin-CGN**, correspondiente a **71 niños de 6 a 13 años**, con **2,05 horas de audio** y **14.251 intentos de lectura**. Dispone de anotaciones ortográficas, fonéticas y de estrategias lectoras.

Para reconocimiento fonético compara Wav2Vec2 Base, XLSR Large y HuBERT Large adaptado al neerlandés. Para reconocimiento de palabras compara Wav2Vec2 Large, XLSR Large, MMS con adaptador neerlandés y **Whisper Large-v2 mediante faster-whisper**.

Usa **SCTK** para puntuar y alinear transcripciones. Antes normaliza mayúsculas, puntuación, formatos de palabras y alfabetos fonéticos. Esa normalización evita contar como errores diferencias meramente de representación.

#### Detección de errores y clasificación

Primero alinea el texto esperado con la transcripción humana para construir una referencia de errores, y después con la salida del ASR para obtener los errores predichos. Evalúa coincidencia de tipo y posición de error.

La clasificación general contempla inserciones, sustituciones y omisiones. Después diferencia sustituciones por palabras de significado similar, de escritura similar o sin esas semejanzas, además de inserciones y omisiones lectoras.

Para esta categorización emplea semejanza ortográfica y semántica, con umbrales concretos del estudio. También analiza si una inserción corresponde a un reinicio o repetición. Según el criterio educativo utilizado, ciertos intentos seguidos de lectura correcta no se contabilizan como inserciones lectoras que deban penalizarse.

Esto muestra que **detectar una diferencia y decidir cómo puntuarla son decisiones distintas**. En nuestra aplicación podemos conservar una repetición como indicador de fluidez sin tratarla como una palabra final incorrecta.

#### Resultados de reconocimiento

| Modelo de palabras | WER en lectura infantil |
|---|---:|
| Wav2Vec2 Large | 13,2 % |
| XLSR Large | 17,6 % |
| MMS-NL | 21,0 % |
| Whisper | 9,8 % |

En reconocimiento fonético, HuBERT adaptado obtiene **23,1 % de PER** en niños, frente al **6,3 %** en adultos del conjunto comparativo. La diferencia muestra que un buen resultado adulto no basta para garantizar precisión infantil.

El artículo calcula además la relación entre errores predichos y errores reales. Whisper obtiene **0,58**, mientras los otros modelos de palabras superan 1. Esto indica tendencias distintas: Whisper señala menos errores que los anotados; los demás generan más diferencias, incluidas falsas alarmas.

#### Resultados de detección de errores lectores

| Modelo | Precisión | Recall | F1 |
|---|---:|---:|---:|
| Wav2Vec2 Large | 0,29 | 0,83 | 0,43 |
| Whisper | 0,52 | 0,53 | 0,52 |

Aquí **precisión** significa qué proporción de los errores señalados son reales, y **recall** qué proporción de los errores reales se detectan. Wav2Vec2 encuentra más errores, pero con más falsas alarmas. Whisper presenta mejor precisión y F1 global, aunque deja sin detectar una parte importante.

Ambos reconocen mejor las palabras correctamente leídas que los intentos incorrectos o incompletos:

| Tipo de intento | Wav2Vec2 Large | Whisper |
|---|---:|---:|
| Palabra correcta | 0,90 | 0,93 |
| Parte de palabra | 0,29 | 0,23 |
| Intento incorrecto | 0,60 | 0,53 |

La dificultad con fragmentos es relevante: «mari… mariposa» contiene una autocorrección que desaparecería si solo conservamos la palabra completa final. El análisis muestra que Whisper tiende a omitir intentos incorrectos, mientras Wav2Vec2 produce salidas más variadas, a veces conservando evidencia del intento y otras introduciendo sustituciones o fusiones.

#### Aportaciones y límites

Podemos utilizar este diseño para comparar candidatos españoles con **WER, conservación de disfluencias, precisión, recall y F1**, además de latencia. Las falsas alarmas deberían analizarse porque pueden hacer que el alumno repita innecesariamente una palabra bien leída.

El estudio usa fragmentos de inferencia de **10 segundos** y una GPU Tesla V100. Los tiempos totales reportados no demuestran respuesta por palabra en directo. Necesitamos medir la latencia con nuestra forma de capturar y procesar audio.

Los resultados son en neerlandés y la clasificación de ciertos errores se deriva de semejanzas automáticas. Los autores reconocen posibles discrepancias con categorías humanas y errores de alineamiento. Es una referencia de evaluación, no una selección definitiva de ASR para español.

### 3.5. SARA (2026): evaluación automatizada de respuestas infantiles en español

Referencia bibliográfica: [5].

**Título:** *Development and validation of SARA: an AI-assisted reading assessment tool for primary school children in low-resource Spanish-speaking contexts*.  
**Autores:** Daniel Cubilla-Bonnetier, Enzo Casamassima, Hugo Marte-Santana y Laura V. Sánchez-Vincitore.  
**Publicación:** Frontiers in Education, 2026.  
**Fuente:** [Artículo mediante DOI](https://doi.org/10.3389/feduc.2026.1882718).

#### Qué es SARA y qué evalúa

SARA —*Self-Applied Reading Assessment*— es una aplicación para tablets Android que permite administrar pruebas de lectura de forma autónoma y sin conexión. Integra la batería **ECLEC**, adaptada al contexto dominicano, y busca reducir la dependencia de un examinador que presente y corrija cada respuesta.

En las tareas de decodificación relevantes para este prototipo, SARA incluye identificación de letras y lectura de sílabas, palabras y pseudopalabras. Las respuestas orales se clasifican con IA como correctas o incorrectas.

Las pseudopalabras ayudan a estudiar la conversión de letras a sonidos sin depender únicamente de reconocer una palabra familiar.

#### Diferencia respecto a nuestra aplicación

El núcleo de IA descrito **evalúa respuestas breves asociadas a estímulos**, no el recorrido continuo por un cuento. En las tareas de decodificación, cada elemento genera su propio archivo de audio.

Por eso, SARA resulta especialmente interesante para la evaluación acústica y la metodología de validación, pero no ofrece directamente el seguimiento del cursor, la segmentación de una lectura larga o la recuperación de posición.

Tampoco hay una oposición entre IA y algoritmos fonéticos: un sistema puede utilizar una red neuronal para reconocer sonidos y después programación dinámica para seguir el texto. Son componentes que pueden complementarse.

#### Recogida y preparación de datos

La validación se realiza con **1.860 alumnos de segundo a sexto de primaria**, de **34 centros de Santo Domingo**. La administración se efectúa en grupos de ocho alumnos y dura de media unos **30,8 minutos**.

Cada participante genera hasta 80 grabaciones de decodificación. Dos equipos humanos corrigen independientemente los audios siguiendo criterios y una fase de calibración. Tras aplicar los filtros descritos, el desarrollo de IA utiliza **101.037 grabaciones de 1.263 alumnos**.

El audio se normaliza a **16 kHz y mono**, y a una longitud de **50.000 muestras**, aproximadamente **3,125 segundos**. Las respuestas cortas se rellenan; cuando sobra audio, se recorta por el comienzo para conservar el final con la respuesta.

La división se realiza **por participante**: 70 % entrenamiento, 15 % validación y 15 % prueba. Ningún alumno aparece en más de una partición, evitando evaluar con voces que el modelo ya haya aprendido.

#### Primer enfoque: red neuronal con audio y estímulo esperado

El primer método utiliza una **CNN de doble entrada**, entrenada por separado para cada subprueba:

- Una entrada representa el audio mediante un **espectrograma log-Mel de 64 bandas**.
- La otra representa el estímulo esperado mediante una secuencia de caracteres convertida a vectores.

La rama acústica aplica convoluciones y bloques residuales para extraer características; ambas representaciones se concatenan y una salida sigmoide clasifica la pareja como correcta o incorrecta.

Su interés es que la decisión depende de **lo pronunciado y de lo que debía pronunciarse**, sin exigir que la salida final sea una transcripción textual completa.

Como predominan las respuestas correctas, equilibran el entrenamiento creando parejas incorrectas: un audio real correcto se asocia a otro estímulo de la misma categoría. Esto genera un desacuerdo audio-texto, aunque no reproduce todos los errores fonéticos reales de un niño. También aumentan datos con transformaciones acústicas, como cambios de tempo, eco o filtrado.

#### Segundo enfoque: Wav2Vec2, PCA y XGBoost

El segundo método utiliza un **Wav2Vec2 español**, ajustado con una parte de grabaciones perteneciente exclusivamente al entrenamiento, para extraer representaciones acústicas de sus capas ocultas.

Después aplica **PCA**, conservando el 95 % de la variabilidad, y usa esas características junto con la identidad de la subprueba para entrenar **XGBoost**. En la configuración descrita se emplean 500 árboles y profundidad máxima 9. El desequilibrio se trata mediante pesos de clase.

No conviene describir este enfoque como equivalente a la CNN de doble entrada: el artículo especifica representaciones acústicas y la subprueba como características de XGBoost, mientras la CNN incorpora explícitamente el estímulo en caracteres. La generalización a palabras nuevas de cuentos requeriría investigación adicional.

#### Selección de modelos y resultados

Para cada subprueba se selecciona el modelo según **MCC** en validación y se ajusta allí el umbral de clasificación. El conjunto de prueba se reserva para los resultados finales. La validación y la prueba mantienen la distribución natural de clases, aproximadamente 86 % correctas y 14 % incorrectas.

La IA alcanza **91,97 % de exactitud global** y **MCC de 0,689**. El rendimiento por clase es mejor para respuestas correctas —**90,0–96,2 %** según subprueba— que para incorrectas —**73,9–80,1 %**—. Por tanto, la cifra global no implica detectar casi todos los errores.

Los equipos humanos presentan **86,11 % de acuerdo** y kappa de **0,550**. La evaluación de IA utiliza los casos en los que ambos equipos coinciden. Comparar directamente 91,97 % y 86,11 % para afirmar que la IA supera a los humanos sería inadecuado: no son el mismo procedimiento ni la misma referencia de evaluación.

#### Aportaciones para nuestro proyecto

Podemos investigar clasificadores acústicos para palabras o fragmentos previamente localizados. En ese diseño, otro componente tendría que determinar a qué posición pertenece el audio antes de evaluarlo.

La metodología aporta decisiones claras: separar alumnos entre particiones, anotar independientemente, medir cada clase, ajustar umbrales con validación y reservar la prueba. También conviene distinguir el desequilibrio de entrenamiento de la distribución real de uso.

#### Límites y recursos

El artículo no proporciona un repositorio público del sistema completo ni identifica una descarga pública del corpus de audio. Su existencia no implica que podamos entrenar directamente con sus grabaciones.

La validación corresponde al español dominicano y a estímulos concretos. Debemos comprobar variantes de pronunciación de nuestra población y la aplicación a lectura continua.

Además, el filtrado excluye grabaciones de baja calidad y participantes con menos del 30 % de aciertos globales. No deberíamos trasladarlo automáticamente: las lecturas difíciles pueden ser precisamente los casos que nuestra aplicación necesita atender. El recorte a tres segundos tampoco resulta adecuado para cuentos ni garantiza conservar todos los intentos de una palabra.

### 3.6. Project LISTEN: tutor de cuentos e integración de ayuda educativa

**Proyecto:** Project LISTEN, Carnegie Mellon University.  
**Fuentes:** [Resumen oficial](https://www.cs.cmu.edu/~listen/), *Why and How Our Automated Reading Tutor Listens* de Jack Mostow (2012).

#### Qué aporta como sistema completo

Project LISTEN desarrolló un tutor que presenta cuentos, escucha la lectura infantil y ofrece ayuda visual y hablada. Utiliza una adaptación de **CMU Sphinx** e interviene ante errores, bloqueos o solicitudes de ayuda. Su interés es la integración de reconocimiento, seguimiento y apoyo educativo en una actividad de lectura, más allá de clasificar respuestas aisladas.

#### Seguimiento y organización del cuento

El artículo de Mostow describe el procesamiento por frases para restringir el reconocimiento y disponer de momentos de intervención. **MultiMatch** alinea palabras reconocidas con posiciones del texto mediante programación dinámica. Penaliza diferencias ortográficas y fonéticas, además de saltos, y admite relecturas. Los costes evitan buscar una coincidencia lejana cuando una sustitución local explica mejor el intento.

También diferencia posición real e indicación de qué debe leerse después. La estimación interna debe modelar el comportamiento del lector, aunque la interfaz utilice una guía más estable. Para fluidez analiza tiempos y características prosódicas como duración, intensidad y tono. [Artículo de Mostow](https://www.cs.cmu.edu/~listen/pdfs/2012-05-05%20ISADEPT2012%20keynote%20final.pdf).

#### Adaptación propuesta para nuestra aplicación

Podemos mantener el cuento completo en pantalla y trabajar internamente con un fragmento próximo al cursor. Cada palabra tendría un índice global, de manera que cambiar de fragmento no reiniciara el progreso. Esta es una propuesta de adaptación; no equivale a copiar la interfaz original.

Ejemplo ilustrativo de ambigüedad: si un cuento contiene «el gato» varias veces y el alumno repite esas palabras, buscar su primera coincidencia en todo el documento puede situarlo en un párrafo incorrecto. Una ventana local y penalizaciones de salto deberían favorecer la continuidad, ampliando la búsqueda cuando exista evidencia de que se perdió el seguimiento.

#### Límites de transferencia

LISTEN es una línea de investigación con varias publicaciones, no un único algoritmo que resuelva todo el proyecto. El paper de Li y Mostow del primer apartado pertenece a esa línea: su resultado de los 200 ms no es una evidencia independiente adicional.

La existencia de componentes de CMU Sphinx no demuestra que esté disponible el tutor completo. Deberíamos estudiar por separado acceso a código, modelos, datos y condiciones de uso. Las decisiones de seguimiento e intervención necesitan validación con lectura infantil en español y con los cuentos de nuestra aplicación.

#### Modelado del lector y confianza

El modelo probabilístico del lector representa lectura correcta, palabras incompletas, omisiones y reinicios. Es una alternativa que deberá compararse con reglas de seguimiento más sencillas. La confianza acústica y la confianza en la posición deben tratarse por separado: evaluar un audio contra una palabra mal localizada puede producir una falsa alarma.

Los datos de lectura infantil se describen en el apartado 6. Las fuentes de LISTEN y seguimiento se recogen en [6] y [7].

## 4. Matriz de necesidades y alternativas

Las ventajas y limitaciones siguientes son una valoración para nuestro proyecto. Los componentes son candidatos, no decisiones definitivas.

### 4.1. Reconocimiento y decodificación

| Necesidad | Alternativa | Ventajas | Limitaciones | Comprobaciones |
|---|---|---|---|---|
| Reconocer lectura en español | Wav2Vec2/XLSR | Adaptable; salida CTC o características acústicas. | Requiere modelo y datos adecuados. | Precisión infantil, disfluencias, memoria y retraso. |
| Obtener transcripción base | Whisper/faster-whisper | Alternativa para comparar reconocimiento. | Puede omitir o normalizar desviaciones; necesita estrategia de audio continuo. | Errores preservados y latencia con fragmentos cortos. |
| Reconocer fonemas | Wav2Vec2/XLSR fonético; HuBERT adaptado | Apoya comparación de sonidos. | La salida fonética depende del entrenamiento; modelos de Gao en neerlandés. | Modelo español, precisión y alfabeto fonético. |
| Comparar otro ASR | MMS | Alternativa multilingüe. | No validado en nuestro contexto. | Calidad y coste frente a otros modelos. |
| Reconocimiento local configurable | PocketSphinx/SphinxTrain | Componentes abiertos de reconocimiento y entrenamiento. | No incluyen el tutor LISTEN ni garantizan precisión infantil. | Modelos españoles y rendimiento. |
| Guiar ASR por texto conocido | K2 y FST | Representan caminos correctos y alternativos. | Integración y ajuste complejos. | Velocidad y conservación de errores. |
| Modelar secuencias de lectura | KenLM/Kneser-Ney | Puede incorporar disfluencias textuales. | No sigue el cursor; depende del corpus y decodificador. | Mejora real y efecto de las restricciones. |

### 4.2. Seguimiento del cuento

| Necesidad | Alternativa | Ventajas | Limitaciones | Comprobaciones |
|---|---|---|---|---|
| Tolerar pequeñas desviaciones | Levenshtein sobre fonemas | Simple e interpretable. | Depende del reconocimiento fonético; umbral sensible. | Palabras cortas y parecidas, costes y variantes. |
| Reducir avances por ruido | Primera vocal y coincidencia exacta en dos fonemas | Condiciones adicionales de aceptación. | Pueden aumentar bloqueos. | Falsos avances frente a intentos válidos rechazados. |
| Recuperarse de omisiones | Comparación avanzada y posición estable | Evita depender de una única hipótesis. | El cursor de Yılmaz solo avanza; añade espera y requiere una posición estimada. | Saltos falsos, recuperación y adaptación de retrocesos. |
| Representar relecturas | MultiMatch | Admite repeticiones y retrocesos. | Necesita implementación y ajuste de penalizaciones. | Palabras repetidas y cambios de hipótesis. |
| Modelar lectura no lineal | Estados probabilísticos | Contempla omisiones, reinicios y saltos. | Más parámetros y complejidad. | Mejora frente a reglas sencillas y coste. |
| Comparar secuencias | MSA/estrella central/Needleman-Wunsch | Relacionan texto y transcripciones. | No demuestran seguimiento inmediato; cuidado con retrocesos. | Uso posterior o incremental y casos ambiguos. |
| Limitar posiciones candidatas | Frases y ventana móvil propuesta | Reduce contexto manteniendo posición global. | Puede perder saltos fuera de la ventana. | Tamaño y ampliación al perder seguimiento. |
| Estabilizar actualizaciones | Hipótesis parciales y espera breve | Aprovecha evidencia adicional. | Añade latencia. | Desfase visible, precisión y oscilaciones. |

### 4.3. Evaluación y estadísticas

| Necesidad | Alternativa | Ventajas | Limitaciones | Comprobaciones |
|---|---|---|---|---|
| Clasificar respuestas | CNN audio-texto de SARA | Analiza pronunciación y estímulo juntos. | Entrenamiento y datos etiquetados; respuestas breves. | Palabras nuevas, errores reales y falsas alarmas. |
| Clasificar características acústicas | Wav2Vec2/PCA/XGBoost | Reutiliza representaciones y reduce dimensiones. | Necesita entrenamiento y segmentación previa. | Rendimiento y coste por fragmento. |
| Rechazar reconocimiento dudoso | Clasificador de confianza contextual | Combina audio, alineación e historial. | Una posición errónea invalida la comparación. | Calibración y rendimiento con seguimiento perdido. |
| Medir fluidez | Duración, pausas y prosodia | Amplía estadísticas más allá de errores. | Depende de alineamiento fiable. | Pausas de puntuación y comparación humana. |
| Obtener tiempos posteriores | WhisperX | Alineamiento temporal por palabra. | No demuestra seguimiento inmediato ni lectura correcta. | Disfluencias y calidad de tiempos. |
| Medir ASR | SCTK, WER y PER | Evaluación reproducible. | No miden directamente subrayado ni diagnóstico. | Normalización y relecturas. |
| Medir errores lectores | Precisión/recall/F1/MCC; BER y DER de Vidal | Visibilizan falsas alarmas, errores ocultados y desequilibrio. | Requieren referencia fiable, clase positiva y definición de cada métrica. | Resultados por clase, tipo y posición; BER como suma de tasas según Vidal. |
| Medir cursor | TAT, posición y latencia | Evalúan actualización visible. | Requieren anotaciones y definir palabra actual o siguiente. | Exactitud, saltos, bloqueos y recuperación. |

### 4.4. Datos y audio

| Necesidad | Alternativa | Ventajas | Limitaciones | Comprobaciones |
|---|---|---|---|---|
| Generar disfluencias | disfluentES | Variantes textuales reproducibles. | No genera audio ni todos los errores reales. | Realismo y mejora del modelo de lenguaje. |
| Crear variantes gramaticales | spaCy y mlconjug3 | Apoyan generación de sustituciones. | No procesan voz. | Vocabulario y conjugaciones adecuadas. |
| Limpiar audio | FullSubNet | Puede mejorar calidad perceptiva. | Puede alterar señales y añadir retraso. | ASR y errores con/sin limpieza. |
| Medir calidad de señal | DNSMOS | Comparación automática del audio. | No mide éxito del seguimiento. | Relación con resultados reales. |
| Preparar muestras | Mono/16 kHz según modelo | Entradas homogéneas. | No todos los modelos requieren lo mismo. | Remuestreo, saturación y continuidad. |
| Crear etiquetas fiables | Dos equipos independientes | Detecta desacuerdos. | Coste y casos ambiguos. | Criterios y acuerdo entre anotadores. |
| Evitar filtraciones | División por alumno | Prueba voces no utilizadas para aprender. | Necesita diversidad y suficientes participantes. | Identidades disjuntas y representatividad. |
| Compensar escasez de errores | Pesos, parejas incorrectas y aumento acústico | Refuerza casos menos frecuentes. | Ejemplos sintéticos distintos de errores reales. | Rendimiento con distribución natural. |

## 5. Librerías y componentes para implementar

Los modelos y algoritmos anteriores necesitan librerías concretas. Se distingue entre componentes identificados en los trabajos y propuestas adicionales. Que un paper use un algoritmo no permite atribuirle una librería no mencionada.

| Componente | Función | Procedencia o estado | Aspecto a validar |
|---|---|---|---|
| Transformers | Cargar y ajustar Wav2Vec2, XLSR, HuBERT o MMS. | Herramientas de Hugging Face utilizadas en Gao. | Modelo, idioma, salida y recursos. |
| faster-whisper | Ejecutar Whisper. | Gao. | Latencia y preservación de errores. |
| K2 | Operaciones FSA/FST y decodificación. | Vidal. | Integración y compatibilidad. |
| KenLM | Modelos de lenguaje n-grama. | Vidal. | Datos y conexión con decodificador. |
| spaCy | Análisis lingüístico. | disfluentES. | Modelo español y vocabulario. |
| mlconjug3 | Conjugación verbal. | Recurso enlazado por Vidal. | Variantes generadas. |
| XGBoost | Clasificación de características. | SARA. | Entrenamiento y rendimiento por clase. |
| PocketSphinx/SphinxTrain | Reconocimiento y entrenamiento acústico. | Ecosistema CMU Sphinx; no equivalen al tutor histórico. | Modelos españoles y precisión. |
| SCTK | Evaluación y alineamiento textual. | Gao. | Tratamiento de repeticiones. |
| PyTorch | Ejecución y entrenamiento de redes. | Propuesta de implementación. | CPU/GPU, memoria y versiones. |
| SoundFile | Leer/escribir archivos y bloques de audio. | Propuesta adicional. | Formatos; no captura micrófono web. |
| librosa | Preparar señales y extraer características. | Propuesta adicional. | Coste en procesamiento directo. |
| Silero VAD | Detectar voz y silencios. | Propuesta adicional. | No separar hablantes; evitar cortes. |
| Phonemizer/eSpeak NG | Convertir texto esperado a fonemas. | Propuesta adicional. | Variantes del español; no reconoce audio. |
| RapidFuzz | Levenshtein sobre secuencias. | Propuesta adicional. | Tokenización de fonemas y umbrales. |
| scikit-learn | PCA y métricas de clasificación. | Propuesta para implementar esos métodos. | Ajustar transformaciones solo con entrenamiento. |
| WhisperX | Marcas temporales mediante alineamiento. | Candidato para revisión posterior. | Disfluencias y tiempos fiables. |
| getUserMedia/AudioWorklet | Captura y procesamiento de audio web. | API del navegador, no librería Python. | Tablets, permisos, formato y latencia. |

La aplicación deberá registrar las versiones y licencias de los componentes finalmente utilizados. No hace falta incorporar todas las herramientas al prototipo: cada una debe responder a una necesidad comprobada.

## 6. Datasets y disponibilidad

Los datasets se organizan según su utilidad para tres tareas: reconocer voz infantil, seguir un texto conocido y evaluar errores. Se incluyen datos en inglés y neerlandés cuando aportan anotaciones o métodos útiles. Las prioridades siguientes son propuestas para el prototipo; las fichas se han consultado, pero no se han descargado ni auditado los corpus completos ni tramitado sus licencias.

### 6.1. Lectura infantil y errores: candidatos prioritarios

| Dataset | Contenido e idioma | Utilidad para el proyecto | Acceso y límites |
|---|---|---|---|
| **[disfluentES: transcripciones reales](https://ri.conicet.gov.ar/handle/11336/263019)** | Transcripciones y tipos de disfluencias de pruebas de lectura de niños de Argentina; español. La ficha de CONICET publica un JSON de unos 12,43 MB. | Analizar errores y disfluencias y preparar pruebas de comparación con el texto esperado. | Ficha con CC BY-NC-SA 2.5. **No se ha confirmado distribución del audio**. También se identifican [datos de Vidal en Zenodo](https://zenodo.org/records/15522540); no se ha comprobado la equivalencia entre ambas ediciones. La ficha de CONICET se consultó previamente, pero no pudo volver a verificarse en la última consulta. |
| **[Maharashtra Primary Schools — MPS](https://github.com/DAP-Lab/mps_dataset)** | 19 horas, 1.600 intentos de lectura y 1.110 niños de 7–11 años; inglés como segunda lengua, tercero a quinto en India. Audio, texto esperado, transcripciones y etiquetas de palabra correcta, sustitución, inserción y omisión. | **Primer candidato en inglés para errores lectores**: comparar intentos reales con el texto y comprobar recuperación ante omisiones, repeticiones y palabras incompletas. | Repositorio público con WAV mono de 16 bits a 16 kHz y `data.json`. El uso está sujeto a una licencia cuyo detalle debe consultarse con Preeti Rao (`prao@iitb.ac.in`). El alineamiento mostrado es textual: **no confirma tiempos por palabra** ni una etiqueta independiente de autocorrección. Hay pocos textos; comprobar generalización a cuentos nuevos. |
| **[CMU Kids Corpus](https://catalog.ldc.upenn.edu/LDC97S63)** | 5.180 enunciados de 76 niños de 6–11 años en inglés; incluye grupos de lectura correcta y lectura con errores. Creado para Project LISTEN [8]. | Ensayar ASR y detección de errores con lectura infantil nativa y texto conocido. | Distribución LDC bajo acuerdo y tarifa aplicable; acceso institucional no confirmado. No equivale a las grabaciones exactas de todos los experimentos de LISTEN ni valida español. |
| **[CHOREC](https://taalmaterialen.ivdnt.org/download/tstc-chorec-spraakcorpus/)** | Corpus completo de 130 horas de 400 niños flamencos leyendo textos y listas, con anotaciones de estrategia y errores; neerlandés. Yılmaz utiliza 279 sesiones de nueve relatos de 103–223 palabras. | Referencia para seguimiento de relatos, recuperación y diseño de anotaciones de errores. | La ficha ofrece acceso gratuito previa firma de licencia e inicio de sesión. Distinguir corpus completo y muestra experimental; revisar cobertura de tiempos y etiquetas al obtener los archivos. |
| **[JASMIN-CGN](https://taalmaterialen.ivdnt.org/download/tstc-jasmin-spraakcorpus/)** | La ficha actual describe unas 115 horas totales de distintos grupos, con lectura y diálogos; neerlandés/flamenco. WAV y anotaciones TXT/TextGrid. | Reproducir o estudiar evaluación de ASR y errores como en Gao, seleccionando grupo y tarea pertinentes. | Gratuito para la modalidad de investigación descrita, previa licencia e inicio de sesión; uso comercial separado. Las 115 horas no son exclusivamente infantiles. No asumir que todas las etiquetas del subconjunto de Gao acompañan a la edición general. |

El [generador disfluentES](https://github.com/habla-liaa/disfluentES), con licencia MIT, es una **herramienta complementaria**, no un corpus de audio. Permite crear variantes textuales con omisiones, sustituciones, inserciones, repeticiones y palabras incompletas para pruebas controladas o modelos de lenguaje. Sus salidas son sintéticas y no sustituyen errores reales.

### 6.2. Voz en español y adaptación a voces infantiles

| Dataset | Contenido | Utilidad | Acceso y límites |
|---|---|---|---|
| **[Common Voice Scripted Speech 27.0 — español](https://mozilladatacollective.com/datasets/cmu5kitx700pemi073feoiqqu)** | La ficha describe 2.282,72 horas grabadas, 597,6 validadas y 26.960 hablantes; metadatos autodeclarados de edad y acento, incluido el canario. MP3, paquete de unos 48,38 GB. | Primera base para comparar reconocedores en español, acentos y entrada de audio. Seleccionar muestras validadas y registrar versión y partición. | Licencia declarada CC0-1.0 y condiciones visibles de plataforma que prohíben identificar hablantes y volver a alojar o redistribuir el dataset. Flujo de descarga no completado. **No es un corpus específico de primaria con errores lectores**; clips invalidados no son etiquetas fiables de esos errores. |
| **[IESC-Child](https://www.sciencedirect.com/science/article/abs/pii/S0885230817301547)** | 34,88 horas de español mexicano de 174 niños de 6–11 años, segmentadas y transcritas, con emoción y actitud. | Candidato para evaluar reconocimiento de voces infantiles en español. | Disponible para investigación previa solicitud a los autores; licencia y formato de entrega pendientes. Interacción con robots, **no lectura de cuentos**. El artículo presenta discrepancias en el recuento de segmentos; revisar el inventario recibido. |
| **[MyST — My Science Tutor](https://catalog.ldc.upenn.edu/LDC2021S05)** | La edición LDC describe unas 470 horas en inglés de 1.371 alumnos de tercero a quinto y 102.433 enunciados transcritos, aproximadamente el 45%. Diálogos con tutor de ciencias; audio a 16 kHz y texto UTF-8. | Adaptar o evaluar ASR infantil con habla conversacional. | LDC distribuye una edición bajo acuerdo propio; acceso y tarifa no tramitados. Los antiguos enlaces gratuitos de los autores no funcionaron en esta consulta. La preparación del artículo describe 393 horas: no mezclar ediciones. **No es lectura de texto esperado**. |

Para un primer prototipo, Common Voice sirve como comprobación general en español, e IESC-Child como candidato infantil sujeto a acceso. MyST aporta voces infantiles en inglés, pero no reemplaza MPS/CMU Kids para errores de lectura. No se propone entrenar un reconocedor desde cero ni descargar todos los paquetes antes de comparar modelos existentes.

### 6.3. Complementos para pronunciación y condiciones acústicas

| Recurso | Uso propuesto | Acceso y límites |
|---|---|---|
| **[speechocean762](https://www.openslr.org/101/)** | Experimentar con puntuaciones de pronunciación: 5.000 frases en inglés, cinco evaluadores, mitad hablantes infantiles y mitad adultos. | CC BY 4.0, unos 520 MB. Todos son hablantes de lengua materna mandarín: pronunciación en segunda lengua, no errores de niños hispanohablantes. Opcional para una fase posterior. |
| **[MUSAN](https://www.openslr.org/17/)** | Añadir música, habla y ruido de forma controlada para evaluar robustez del ASR y detección de voz. | CC BY 4.0, unos 11 GB. Las mezclas no representan automáticamente un aula real. |
| **[RIRS_NOISES](https://www.openslr.org/28/)** | Simular reverberación y efectos de salas o micrófono distante. | Apache 2.0, unos 1,3 GB, 16 kHz/16 bits. Parte de los ruidos procede de MUSAN: revisar solapamientos entre entrenamiento y prueba. |

Se incorporarán ruido y reverberación cuando el sistema funcione con un lector en silencio; se complementarán con pruebas en los dispositivos y salas reales.

### 6.4. Corpus con acceso pendiente de confirmar

| Dataset | Contenido y utilidad | Acceso y límites |
|---|---|---|
| **Corpus de SARA [5]** | 101.037 grabaciones de 1.263 alumnos en el desarrollo de IA, en español dominicano. Referencia para clasificación acústica y anotación de respuestas infantiles. | No se identifica una descarga pública. Sus respuestas breves y filtrado no equivalen a lectura de cuentos. |
| **[Rose et al., CoNLL 2026](https://aclanthology.org/2026.conll-main.35/)** | Lectura de 63 alumnos de primero a tercero en inglés, con tiempos manuales por palabra/oración, fonemas y errores. Útil para estudiar el diseño de anotaciones temporales. | Descarga pública y licencia no confirmadas. No se considera un corpus disponible para el prototipo hasta aclarar el acceso. |

### 6.5. Prioridades y carencias de datos

1. **Lógica de errores:** transcripciones reales de disfluentES y variantes sintéticas controladas.
2. **Audio con errores reales:** MPS en inglés si se aclara la licencia; CMU Kids si hay acceso institucional. CHOREC aporta una referencia adicional de seguimiento.
3. **Reconocimiento:** muestras validadas de Common Voice; buscar acceso a IESC-Child y valorar MyST como complemento infantil.
4. **Robustez:** MUSAN/RIRS_NOISES después de las pruebas en silencio.

No se ha confirmado un recurso accesible que reúna niños hispanohablantes de primaria, cuentos completos, texto esperado, transcripción literal, autocorrecciones y tiempos manuales por palabra. El futuro piloto del proyecto necesitaría esos elementos, junto con información del dispositivo y entorno y revisión humana de casos ambiguos. Su recogida requiere el procedimiento y autorizaciones que determine el centro.

El inglés permite ensayar alineamiento, recuperación y evaluación, pero los modelos acústicos, fonemas, variedades y patrones de error deben comprobarse de nuevo en español. Un alineamiento textual entre palabras no equivale a tiempos acústicos; una transcripción final tampoco demuestra seguimiento correcto en directo.

## 7. Propuesta inicial de funcionamiento

Esta arquitectura es una hipótesis de desarrollo basada en la revisión; todavía debe probarse.

1. **Preparar el cuento:** separar palabras y frases, manteniendo identificadores globales para cada palabra.
2. **Capturar audio continuo:** obtener bloques con sus tiempos, conservando la grabación completa durante las pruebas autorizadas.
3. **Preparar el audio:** adaptar formato y, si ayuda, detectar voz. No confundir detectar voz con identificar al alumno.
4. **Reconocer:** obtener hipótesis provisionales con un modelo base.
5. **Alinear y seguir:** comparar con un fragmento próximo a la posición actual, tolerar pequeñas desviaciones y recuperar ante pérdidas de seguimiento.
6. **Actualizar subrayado:** aplicar una política de estabilidad y medir el retraso visible.
7. **Evaluar:** registrar intentos y revisar errores con resultados definitivos o procesamiento posterior.
8. **Generar estadísticas:** calcular medidas respaldadas por datos fiables sobre errores, autocorrecciones, pausas y fluidez.

### 7.1. Cuento completo y contexto limitado

Leer un cuento completo no exige comparar cada bloque de audio con todo el cuento. Proponemos una ventana que incluya palabras anteriores y posteriores, manteniendo índices globales. Si el alumno sale de esa ventana, el sistema ampliaría la búsqueda o permitiría intervención del docente.

La ventana deberá admitir retrocesos. Las palabras repetidas y los cambios de lector en sesiones grupales necesitan pruebas específicas.

### 7.2. Separar seguimiento rápido y valoración posterior

El seguimiento dará prioridad a continuidad y estabilidad. La evaluación podrá utilizar información más completa, conservando las diferencias entre primer intento, autocorrección y resultado final.

Esta separación no obliga a utilizar dos modelos: pueden compartir reconocimiento y alineamiento. Lo que debe mantenerse independiente son los criterios de avance y de calificación.

### 7.3. Registro de intentos y decisiones de puntuación

Cada intento debería relacionarse con un intervalo de audio, una posición candidata del cuento y las hipótesis disponibles en ese momento. Como propuesta de implementación, se conservarían la categoría del evento, el vínculo con una posible autocorrección, la decisión de avance y la valoración final. Una revisión posterior podría modificar la valoración sin borrar el historial del cursor.

La taxonomía de Vidal permite partir de SUB, PHO, REP, INS, DEL y CUT, además de PRECUT y PRESUB para intentos previos a corrección. Deben fijarse reglas de anotación para distinguir una sustitución de un error fonético, una repetición de una inserción y una omisión de una pérdida de seguimiento. Estas etiquetas se usarían inicialmente como referencia de diseño, sin asumir que todas son detectables automáticamente.

Por ejemplo, «mari… mariposa» puede registrar un intento truncado seguido de autocorrección y una palabra final correcta. La repetición o el intento previo puede informar sobre fluidez sin penalizarse como error final. El criterio educativo debe acordarse antes de evaluar el sistema, porque cambiarlo modifica tanto las etiquetas como las métricas.

## 8. Plan de prototipo y validación

### 8.1. Etapas propuestas

| Etapa | Trabajo | Evidencia esperada |
|---|---|---|
| 1 | Captura de audio y un reconocedor base. | Formato correcto, transcripción y tiempos de procesamiento. |
| 2 | Dos políticas de seguimiento sobre los mismos audios. | Comparación de posición, retraso y recuperación. |
| 3 | Errores y estadísticas con anotación humana. | Precisión, recall y falsas alarmas por tipo. |
| 4 | Cuentos completos y distintos dispositivos. | Continuidad, estabilidad y consumo. |

Las lecturas adultas con errores deliberados pueden servir para depurar el sistema, pero no sustituyen las pruebas con voces infantiles.

### 8.2. Casos de prueba

- Lectura correcta a distintas velocidades.
- Repetición de una palabra y de una frase completa.
- Omisión de una o varias palabras.
- Sustitución, palabra incompleta y autocorrección.
- Pausa larga, silencio y solicitud de ayuda.
- Palabras iguales en posiciones distintas.
- Ruido, voz de fondo y comentario ajeno al cuento.
- Cambio de frase, párrafo o lector activo.
- Lectura de un cuento completo sin reiniciar el estado.

### 8.3. Métricas

| Dimensión | Medidas propuestas | Interpretación |
|---|---|---|
| Reconocimiento | WER; PER si hay salida fonética. | Diferencias respecto a transcripción humana. |
| Posición | Exactitud temporal y distancia en palabras. | Dónde está el cursor frente al lector. |
| Rapidez | Mediana y percentil 95 del retraso visible. | Respuesta habitual y retrasos más altos. |
| Estabilidad | Saltos falsos, oscilaciones y bloqueos. | Continuidad del indicador. |
| Recuperación | Tiempo tras repetición, omisión o salto. | Capacidad de volver al texto correcto. |
| Errores lectores | Precisión, recall, F1 y MCC; BER y DER al reproducir Vidal. | Errores detectados, falsas alarmas, falsas aceptaciones y diagnóstico. |
| Fluidez | Palabras correctas por minuto (CWPM), pausas y tiempos por palabra. | Comprobar cada decisión; un total correcto puede ocultar errores compensados. |
| Recursos | Tiempo de inferencia, memoria y CPU/GPU. | Viabilidad en dispositivos previstos. |

Antes de medir, se definirá si el indicador señala la palabra actual o la siguiente. Se conservará el historial de hipótesis parciales: medir solo la transcripción final sería insuficiente.

### 8.4. Preparación de datos

Se separarán alumnos entre entrenamiento, validación y prueba. Los criterios de anotación distinguirán errores, repeticiones, intentos incompletos y autocorrecciones. Los umbrales se ajustarán con validación, y el conjunto de prueba se reservará para la evaluación final.

La primera comparación de errores podrá realizarse con MPS o CMU Kids en inglés, condicionada a sus licencias; la validación final se realizará con lectura infantil española. Si el dataset solo tiene alineamiento textual, habrá que añadir o revisar tiempos humanos para evaluar el cursor. Se registrarán edición, procedencia y condiciones de uso de cada muestra. En MPS, la escasez de textos limita la evidencia de generalización a cuentos nuevos.

Los ruidos y respuestas impulsionales utilizados en entrenamiento y evaluación se separarán para evitar que las mismas condiciones sintéticas aparezcan en ambos conjuntos.
No se trasladará automáticamente el filtrado de SARA a nuestra aplicación: las lecturas con muchos errores y ruido pueden ser precisamente los casos que necesitamos evaluar. Se documentarán las exclusiones y su efecto.

### 8.5. Comparaciones controladas y análisis de resultados

Las alternativas se compararían con los mismos audios, textos, reglas de anotación y condiciones de ejecución. Se propone variar un componente cada vez: reconocimiento base frente a guiado por texto; seguimiento inmediato frente a confirmación; avance local frente a avance con recuperación; y audio original frente a audio mejorado. La mejora perceptiva de FullSubNet/DNSMOS se evaluaría aparte de los cambios en ASR y diagnóstico.

La latencia se desglosaría en captura, espera de contexto, transferencia si hay servidor, inferencia, alineamiento y actualización visual. Se registrarían dispositivo, configuración y duración de los bloques. Los fragmentos de diez segundos y la GPU de Gao no equivalen a una respuesta por palabra; los desfases de Li y Mostow tampoco representan el retraso total de nuestra aplicación.

Además de los resultados agregados, se calcularían medidas por alumno y por tipo de intento. Se distinguirían lectura y habla ajena a la tarea, palabras completas y truncadas, y errores mantenidos y autocorregidos. La TAT de Yılmaz es una proporción de movimientos dentro de un intervalo temporal; la exactitud temporal de Li y Mostow es un porcentaje de tiempo en posición correcta. Deben mantenerse como medidas diferentes.

En clasificación se declararía qué clase se considera positiva y cómo se calculan los denominadores. Para reproducir Vidal, BER es la suma de las tasas de falsas aceptaciones y falsos rechazos, según la definición de ese artículo. La exactitud global se acompañaría de resultados por clase y de la distribución real de respuestas. Los parámetros de PCA, los modelos, los pesos y los umbrales se ajustarían sin utilizar el conjunto de prueba.

### 8.6. Trazabilidad de las decisiones

| Evidencia revisada | Consecuencia para el prototipo | Comprobación necesaria |
|---|---|---|
| Li y Mostow: las hipótesis parciales cambian y una espera puede mejorar posición. | Guardar historial y comparar políticas de actualización. | Precisión temporal y retraso visible por alumno. |
| Yılmaz: la comparación local puede bloquearse; la recuperación mejora TAT. | Combinar avance local y recuperación, manteniendo eventos de omisión. | Bloqueos, saltos tempranos y retrocesos en español. |
| Vidal: guiar por texto ayuda si conserva disfluencias; añadir alternativas puede perjudicar. | Comparar restricciones y categorías de disfluencia por separado. | Falsas aceptaciones, falsos rechazos y diagnóstico. |
| Gao: menor WER no garantiza conservar intentos incorrectos. | Comparar ASR por transcripción y detección de errores. | Fragmentos, autocorrecciones y falsas alarmas. |
| SARA: clasificación condicionada por tarea y validación por participante. | Separar alumnos y evaluar por clase; investigar segmentación previa. | Palabras nuevas, variedades del español y casos difíciles. |
| LISTEN: integración de seguimiento y ayuda educativa. | Mantener índices globales y contexto local para el seguimiento. | Cuentos completos, relecturas e intervención. |

## 9. Decisiones pendientes

| Decisión | Evidencia necesaria |
|---|---|
| Modelo inicial y alternativa | Reconocimiento y retraso en español infantil. |
| Comparación textual o fonética | Errores conservados y recuperación. |
| Contexto y ventana | Cuentos completos, repeticiones y saltos. |
| Umbrales de avance | Falsos avances y bloqueos. |
| Procesamiento local o servidor | Capacidad, red y concurrencia. |
| Estadísticas mostradas | Fiabilidad suficiente para el docente. |
| Datos accesibles | Licencias, autorizaciones y anotaciones. |

La bibliografía permite iniciar un prototipo. Las decisiones definitivas deben basarse en pruebas de la combinación implementada, ya que los resultados de distintos papers no son directamente comparables ni se pueden sumar.

## 10. Referencias y recursos

1. Li, Y. y Mostow, J. (2012). *Evaluating and improving real-time tracking of children’s oral reading*. FLAIRS-25. [Listado oficial de publicaciones de LISTEN](https://www.cs.cmu.edu/~listen/pubs.html).
2. Yılmaz, E., Van Compernolle, D. y Van hamme, H. (2012). *Robust Tracking for Automatic Reading Tutors*. Interspeech. [PDF de ISCA](https://www.isca-archive.org/interspeech_2012/yilmaz12_interspeech.pdf).
3. Vidal, J., Ferrer, L., Kamienkowski, J. E. y Riera, P. (2025). *Improving Automatic Speech Recognition for Children’s Reading Assessment with Disfluency-aware Language Models*. Interspeech. [Artículo y DOI](https://www.isca-archive.org/interspeech_2025/vidal25_interspeech.html).
4. Gao, L., Tejedor-Garcia, C., Strik, H. y Cucchiarini, C. (2024). *Reading Miscue Detection in Primary School through Automatic Speech Recognition*. Interspeech. [Artículo y DOI](https://www.isca-archive.org/interspeech_2024/gao24d_interspeech.html).
5. Cubilla-Bonnetier, D., Casamassima, E., Marte-Santana, H. y Sánchez-Vincitore, L. V. (2026). *Development and validation of SARA: an AI-assisted reading assessment tool for primary school children in low-resource Spanish-speaking contexts*. Frontiers in Education, 11:1882718. [DOI](https://doi.org/10.3389/feduc.2026.1882718).
6. Carnegie Mellon University. *Project LISTEN: A Reading Tutor that Listens*. [Resumen oficial](https://www.cs.cmu.edu/~listen/).
7. Mostow, J. (2012). *Why and How Our Automated Reading Tutor Listens*. [PDF](https://www.cs.cmu.edu/~listen/pdfs/2012-05-05%20ISADEPT2012%20keynote%20final.pdf).
8. Eskenazi, M., Mostow, J. y Graff, D. (1997). *The CMU Kids Corpus*, LDC97S63. [Catálogo y condiciones](https://catalog.ldc.upenn.edu/LDC97S63).
9. [disfluentES](https://github.com/habla-liaa/disfluentES) y [datos publicados de Vidal](https://zenodo.org/records/15522540).
10. [Transformers: Wav2Vec2](https://huggingface.co/docs/transformers/model_doc/wav2vec2).
11. [faster-whisper](https://github.com/SYSTRAN/faster-whisper).
12. [WhisperX](https://github.com/m-bain/whisperX).
13. [K2](https://github.com/k2-fsa/k2) y [KenLM](https://github.com/kpu/kenlm).
14. [spaCy](https://spacy.io/) y [mlconjug3](https://github.com/Ars-Linguistica/mlconjug3).
15. [CMU Sphinx: componentes disponibles](https://cmusphinx.github.io/wiki/download/).
16. [SCTK](https://github.com/usnistgov/SCTK).
17. [PyTorch](https://pytorch.org/) y [XGBoost](https://xgboost.readthedocs.io/).
18. [SoundFile](https://python-soundfile.readthedocs.io/) y [librosa](https://librosa.org/doc/latest/).
19. [Silero VAD](https://github.com/snakers4/silero-vad).
20. [Phonemizer](https://bootphon.github.io/phonemizer/).
21. [RapidFuzz: Levenshtein](https://rapidfuzz.github.io/RapidFuzz/Usage/distance/Levenshtein.html).
22. [scikit-learn: PCA](https://scikit-learn.org/stable/modules/generated/sklearn.decomposition.PCA.html).
23. [AudioWorklet](https://developer.mozilla.org/en-US/docs/Web/API/AudioWorklet).
24. [disfluentES: transcripciones en CONICET](https://ri.conicet.gov.ar/handle/11336/263019); audio y equivalencia con la edición Zenodo pendientes.
25. [MPS: audio, textos y etiquetas de errores](https://github.com/DAP-Lab/mps_dataset); licencia por aclarar.
26. [CHOREC: ficha y condiciones](https://taalmaterialen.ivdnt.org/download/tstc-chorec-spraakcorpus/).
27. [JASMIN-CGN: ficha y condiciones](https://taalmaterialen.ivdnt.org/download/tstc-jasmin-spraakcorpus/).
28. [Common Voice Scripted Speech 27.0, español](https://mozilladatacollective.com/datasets/cmu5kitx700pemi073feoiqqu).
29. [IESC-Child: artículo y disponibilidad previa solicitud](https://www.sciencedirect.com/science/article/abs/pii/S0885230817301547).
30. [MyST: edición LDC2021S05](https://catalog.ldc.upenn.edu/LDC2021S05).
31. [speechocean762](https://www.openslr.org/101/), [MUSAN](https://www.openslr.org/17/) y [RIRS_NOISES](https://www.openslr.org/28/).
32. [Rose et al. (2026): corpus de lectura infantil con anotación temporal](https://aclanthology.org/2026.conll-main.35/); descarga de datos no confirmada.

Los enlaces reúnen las publicaciones, datasets, código y documentación utilizados en el informe. Las condiciones de acceso y la utilidad de cada dataset se detallan en el apartado 6; las funciones de los componentes se recogen en el apartado 5. La compatibilidad y el rendimiento deberán comprobarse en el prototipo, registrando las versiones efectivamente utilizadas.
