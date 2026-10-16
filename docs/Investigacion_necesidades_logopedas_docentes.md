# Necesidades de docentes y logopedas en una herramienta de lectura asistida

**Fecha:** 16 de octubre de 2026.  
**Contexto:** informe complementario a la investigación técnica inicial de las prácticas y el TFG.

## 1. Introducción

El proyecto plantea una herramienta de lectura asistida en grupo: la profesora selecciona desde su tablet al alumno que tiene el turno, se habilita únicamente su micrófono y el sistema sigue su posición en un texto en español. La profesora también puede pausar la sesión cuando necesita explicar algo o se produce una interrupción ajena a la lectura. El primer informe abordaba principalmente cómo resolver el reconocimiento y seguimiento desde el punto de vista técnico. Este documento se centra en otra cuestión: **qué tendría que aportar la herramienta para resultar útil al docente o al logopeda que acompaña al lector**.

Se han seleccionado cinco estudios por su relación con esa cuestión. Uno presenta una aplicación de evaluación de lectura desarrollada con docentes; otro recoge las funciones que solicitan logopedas para trabajar durante las sesiones. Los restantes permiten entender las barreras de adopción, el equilibrio entre información y carga de trabajo, y las condiciones de uso en un contexto educativo español.

El análisis toma como referencia la aplicación final prevista, con el seguimiento, la gestión de turnos, la pausa docente y la consulta de resultados correctamente integrados en la actividad grupal. No describe una fase de desarrollo ni las pruebas del prototipo. Las funciones se presentan como características del diseño final hipotético; su relación con los estudios es una interpretación propia y no implica que estos hayan evaluado la aplicación. Los ejemplos en español son ilustrativos y no pertenecen a los experimentos originales.

## 2. Estudios seleccionados

### 2.1. Mich et al. (2020): qué esperan los docentes de una aplicación que evalúa lectura oral

*Automatically Assess Children’s Reading Skills*, publicado en el congreso READI 2020, es el antecedente más próximo al proyecto entre los trabajos seleccionados. Describe una aplicación para evaluar lectura oral infantil en italiano, basada en reconocimiento automático del habla y en la batería de lectura MT. Los autores implicaron a docentes en el diseño de la interfaz. [Artículo y texto completo](https://aclanthology.org/2020.readi-1.4/).

En un grupo de discusión participaron siete docentes de tres centros. Sus peticiones incluían separar las puntuaciones de velocidad y precisión, imprimir los resultados, analizar tanto pausas excesivas como ausentes y adaptar el uso a tabletas y al aula. También valoraron disponer de información sobre la evolución del alumno. Los autores incorporaron las puntuaciones separadas y la impresión; otras peticiones quedaron como trabajo futuro. Además, realizaron un piloto de usabilidad con tres docentes.

La participación reducida y el contexto italiano limitan la generalización. Sus reglas de puntuación no pueden trasladarse directamente a nuestro alumnado. Su principal interés aquí son las necesidades expresadas por los docentes y su traducción en funciones concretas.

#### Aportación al diseño de la aplicación final

En la aplicación final, el acompañamiento durante la lectura y la información posterior cumplen funciones complementarias. Mientras un alumno lee, el texto compartido señala la posición y permite que el grupo siga el cuento. Desde su tablet, la profesora controla quién tiene el turno. Al terminar la actividad, consulta un resumen individual de la participación de cada lector, con los fragmentos que ha leído y las observaciones relevantes. Esta organización es una aplicación al proyecto de las necesidades de presentación y seguimiento recogidas en el estudio.

Los resultados distinguen las dimensiones de la lectura. Por ejemplo, dos alumnos pueden tardar el mismo tiempo en leer un párrafo, aunque uno avance lentamente y con precisión y el otro lea con rapidez pero omita varias palabras. Una valoración global puede ocultar esa diferencia. Presentar por separado el tiempo de lectura activa y los tipos de eventos permite al profesional interpretar situaciones distintas y relacionarlas con las actividades de apoyo que considere adecuadas. Las métricas deben conservar una definición clara y un respaldo apropiado para su uso.

La información permanece vinculada al texto y al alumno que tenía el turno. Así, la profesora puede localizar una dificultad en una palabra o un fragmento concreto, en lugar de recibir únicamente un recuento al final. El informe también puede compartirse en un formato legible con otros profesionales o con las familias, según corresponda, sin exigir que accedan a los registros internos de la aplicación.

El tratamiento de pausas incorpora el contexto de la sesión. Una detención del alumno durante su turno se conserva como parte de su lectura, mientras que una explicación marcada mediante el botón de pausa queda diferenciada y excluida del tiempo de lectura activa. El estudio fundamenta el interés por analizar y presentar las pausas; la gestión mediante ese botón es una decisión específica del diseño de nuestro proyecto, no una función evaluada por sus autores.

### 2.2. Avant et al. (2025): registrar y consultar información sin aumentar el trabajo del logopeda

El artículo *Participatory Design: Addressing Speech-Language Pathologists’ Challenges through Collaborative Interface Design*, publicado en **Design Issues**, describe un taller de diseño con seis logopedas que tenían experiencia en biofeedback por ultrasonidos. Aunque la intervención es distinta de la lectura, el estudio aborda una cuestión relevante: qué información y controles necesita el profesional durante una sesión. [Artículo y DOI](https://doi.org/10.1162/desi_a_00805).

Las tablas de requisitos recogen peticiones de notas durante la sesión para reducir documentación posterior, gráficos de progreso dentro de una sesión y a lo largo del tiempo, vistas personalizables e impresión. También aparecen la consulta de registros y funciones de exportación en el diseño propuesto. Se revisaron estos apartados en el PDF completo disponible en EBSCO.

Se trata de un caso de diseño con un grupo pequeño, no de una prueba de eficacia clínica. Tampoco demuestra que las mismas funciones tengan idéntica prioridad en lectura infantil. Su aportación es mostrar necesidades concretas expresadas por profesionales, en lugar de deducirlas exclusivamente desde la tecnología.

#### Aportación al diseño de la aplicación final

En el diseño final, el registro de la sesión acompaña al trabajo del profesional. La aplicación reúne las intervenciones de los alumnos, los eventos detectados y las observaciones añadidas por la profesora o el logopeda. De esta manera, la consulta posterior dispone del contexto de lo ocurrido y no depende únicamente de la memoria de quien dirigió la actividad. Esta organización traduce al escenario de lectura grupal las necesidades de anotación y consulta expresadas por los participantes del estudio.

Una observación puede asociarse a una palabra o a un momento del cuento. Por ejemplo, junto a una repetición, el profesional puede anotar que el alumno volvió voluntariamente al inicio de una frase para corregirse. El registro automático y la observación profesional aportan información distinta sobre un mismo episodio. La aplicación permite consultarlas juntas, escuchar el fragmento correspondiente y revisar su interpretación, conservando el contexto de la sesión.

El historial individual diferencia lo ocurrido dentro de una actividad de la evolución entre sesiones. Una lectura repetida del mismo fragmento permite observar cómo cambia la ejecución durante esa práctica. La comparación entre días permite examinar una trayectoria más amplia, teniendo en cuenta el texto, su dificultad y las condiciones de la actividad. La presentación no convierte automáticamente una mejora de velocidad en una mejora general de la competencia lectora.

La consulta se adapta a la finalidad profesional. La profesora puede utilizar una vista de conjunto para seguir la participación del grupo y revisar un resumen por alumno. El logopeda puede profundizar en determinados intentos o comparar episodios de varias sesiones. El interés de esta personalización reside en ofrecer el detalle necesario para cada tarea, manteniendo una relación clara entre la información general y la evidencia que la sostiene. Son características del diseño previsto, inspiradas en un estudio realizado en otro tipo de intervención.

### 2.3. Thompson y Zimmerman (2019): disponer de una aplicación no basta para que el logopeda la adopte

En *Pediatric Speech-Language Pathologists’ Use of Mobile Health Technology: Qualitative Questionnaire Study*, publicado en **JMIR Rehabilitation and Assistive Technology**, se analizaron respuestas de 485 logopedas pediátricos de Estados Unidos sobre el uso de aplicaciones móviles. El trabajo estudia usos, barreras y necesidades de tecnología. [Artículo y DOI](https://doi.org/10.2196/13966).

Entre quienes respondieron a la pregunta sobre barreras, 46 de 135 señalaron el coste y 36 de 135 la falta de evidencia. Esos denominadores corresponden a esa pregunta, no a la muestra completa. También se recoge interés en tecnología para evaluación, registro o consulta de datos y educación de familias.

El estudio se basa en autoinformes, abarca distintas intervenciones y se desarrolla en Estados Unidos. Por tanto, no permite afirmar qué porcentaje de logopedas españoles utilizaría nuestro programa ni cuáles serían sus prioridades exactas. Sí identifica condiciones de adopción que merecen atención: utilidad concreta, coste y respaldo de las funciones que se ofrecen.

#### Aportación al diseño de la aplicación final

En la aplicación final, la confianza profesional se apoya en que los resultados tengan un significado claro y se puedan comprobar. El informe individual explica qué representa cada indicador, a qué tramo de lectura corresponde y cómo influyen las interrupciones de la sesión en el cálculo del tiempo. Así, la profesora o el logopeda dispone de información interpretable para acompañar al lector y valorar su evolución.

La aplicación distingue los eventos detectados automáticamente de las observaciones confirmadas por el profesional. Esta posibilidad de revisión forma parte del diseño de un producto completo: incluso un sistema correctamente implementado puede encontrar pronunciaciones, ruidos o situaciones ambiguas. La interfaz permite examinar esos casos sin obligar a aceptar una clasificación automática como una conclusión definitiva sobre el alumno.

Por ejemplo, ante una posible sustitución, el profesional puede localizar la palabra, escuchar el intento y confirmar o corregir la clasificación. Si se produjo una autocorrección, el informe puede conservar tanto el intento como su resolución. La información final describe lo ocurrido de una forma comprensible para quien va a utilizarla; no confunde una diferencia de transcripción con un diagnóstico clínico o educativo.

El coste de uso también interviene en el diseño final. Además de un precio asumible, la aplicación debe ajustarse a los dispositivos disponibles y al tiempo que el profesional puede dedicar a preparar, conducir y revisar una actividad grupal. Esta consideración del esfuerzo de uso es una interpretación aplicada al proyecto, no una medida económica calculada por la encuesta. Automatizar parte del registro tiene sentido cuando facilita el trabajo de la profesora y le permite mantener la atención en el grupo.

La contribución de este estudio es, por tanto, fundamentar la importancia de una finalidad profesional clara y de evidencia que respalde las prestaciones ofrecidas. Una aplicación terminada no equivale por sí sola a una intervención eficaz: la solidez de sus resultados y su utilidad educativa son cuestiones que deben estar sustentadas.

### 2.4. Francotte, Colognesi y Coertjens (2023): el seguimiento del progreso debe ser viable en la práctica docente

El estudio *Co-creating tools to monitor first graders’ progress in reading: a balancing act between perceived usefulness, flexibility, and workload*, publicado en **Frontiers in Education**, se centra en cómo construir herramientas de seguimiento lector que se ajusten a la práctica docente. Cinco docentes de Bélgica francófona cocrearon cuatro herramientas durante cuatro grupos de discusión. [Artículo abierto](https://doi.org/10.3389/feduc.2023.1111420).

Su aportación central es la relación entre utilidad percibida, flexibilidad y carga de trabajo. Disponer de información sobre las habilidades del alumnado tiene interés si esa información ayuda a adaptar la enseñanza y puede obtenerse de manera asumible. La elaboración conjunta permite que las condiciones reales del aula influyan en el diseño.

La muestra es pequeña y voluntaria; el trabajo no evalúa reconocimiento de voz ni una aplicación equivalente a la nuestra. Aun así, permite analizar el proyecto desde una perspectiva que las medidas de procesamiento no cubren: el esfuerzo necesario para incorporar el resultado a la actividad docente.

#### Aportación al diseño de la aplicación final

En la aplicación final, el seguimiento del progreso está integrado en la actividad de lectura grupal. La profesora prepara el texto y dirige los turnos desde su tablet, mientras la aplicación organiza la información de cada intervención por alumno. Al finalizar, dispone de una visión de la sesión y puede consultar los casos que requieren más atención. La finalidad es que el registro contribuya a conocer la lectura del alumnado con un esfuerzo de interpretación asumible.

La presentación organiza la información por niveles de detalle. Una vista general muestra la participación de los lectores y un resumen de sus resultados. Desde ella se accede a los fragmentos concretos, las observaciones y los registros necesarios para comprender una dificultad. Esta estructura es una interpretación de diseño para el proyecto: no corresponde a una interfaz evaluada en el artículo. Su interés es permitir que la profesora examine primero lo más relevante y profundice cuando lo necesite.

La flexibilidad se relaciona con la finalidad pedagógica. Un cuento utilizado para practicar y un texto empleado para observar el rendimiento pueden requerir interpretaciones distintas. Por ello, el historial conserva el material y el contexto de la actividad. También diferencia la duración total de la sesión del tiempo de lectura activa, para que las explicaciones o interrupciones marcadas por la profesora no alteren la interpretación del ritmo lector.

El diseño evita que el registro se convierta en una segunda tarea que compita continuamente con la atención al alumnado. El cambio de turno, la pausa y la consulta de resultados se integran en el desarrollo de la clase. Los indicadores se presentan con una finalidad comprensible, en lugar de acumular datos que el profesional tenga que reorganizar por su cuenta.

Desde esta perspectiva, la aportación del estudio es explicar que la utilidad depende de la relación entre información, flexibilidad y carga de trabajo. En nuestro diseño final, disponer de más datos solo aporta valor cuando ayuda a comprender la actividad y a adaptar el apoyo al lector.

### 2.5. Cáceres Reche et al. (2024): las condiciones de uso en un contexto español

*Teachers’ perceptions and experiences with mobile apps to enhance literacy skills in the classroom*, publicado en **Porta Linguarum**, ofrece una referencia próxima al contexto del proyecto. Es un estudio cualitativo exploratorio con docentes de centros de Granada, basado en entrevistas semiestructuradas. [Artículo oficial](https://revistaseug.ugr.es/index.php/portalin/article/view/30130).

El resumen editorial destaca dificultades relacionadas con la formación digital, el acceso limitado a recursos tecnológicos y la selección de aplicaciones adecuadas. Los docentes también reconocen beneficios de motivación y participación, y señalan la importancia de un uso constante, normas claras y aprovechamiento de la interacción.

En esta revisión se consultaron la ficha y el resumen oficiales. Por ello, el análisis se limita a esas aportaciones y no atribuye al artículo resultados detallados que no se hayan comprobado en el texto completo. Además, sus percepciones locales sobre aplicaciones de lectoescritura no representan a todo el profesorado español ni prueban la eficacia de un sistema de evaluación oral.

#### Aportación al diseño de la aplicación final

La aplicación final se concibe para que la profesora pueda dirigir una lectura grupal mediante acciones relacionadas con su actividad habitual: elegir un texto, seleccionar al lector, pausar, reanudar y consultar los resultados. La interfaz expresa qué alumno tiene el turno y si la sesión está activa o interrumpida. Esa claridad permite comprender qué está haciendo la herramienta en cada momento sin conocer los parámetros internos del reconocimiento de voz.

La sencillez de uso incluye la incorporación de la aplicación a la práctica del centro. La profesora dispone de indicaciones comprensibles sobre los controles y de una forma clara de reconocer incidencias de conexión o captura. La herramienta se ajusta a los dispositivos del escenario previsto y mantiene coherencia entre lo que muestra la tablet de control y el estado efectivo del turno de los alumnos. Estos son criterios de diseño propios, relacionados con las dificultades de formación y recursos que señala el estudio.

La disponibilidad tecnológica sigue siendo una condición relevante aunque todas las funciones estén correctamente implementadas. La organización de la actividad depende de que los centros cuenten con dispositivos y micrófonos adecuados y de que el uso resulte sostenible durante la clase. Por ello, la utilidad del producto final debe entenderse en relación con ese contexto de utilización. El estudio de Granada aporta una referencia española, aunque no permite dar por supuestas las condiciones de todos los centros.

El acompañamiento visual tiene una finalidad concreta: ayudar al grupo a seguir el texto y mantener una relación clara entre la lectura y la posición señalada. La profesora conserva el control de la actividad y puede detenerla para explicar una palabra o comentar el contenido. El atractivo de la interfaz debe estar al servicio de esa experiencia compartida, evitando que la atención se desplace continuamente de la lectura a los controles.

La motivación y la participación son aspectos relevantes, pero no equivalen por sí solos a una mejora de la precisión o de la comprensión. En el diseño final se distingue la facilidad de participación que ofrece la aplicación de los resultados educativos que puedan obtenerse con su uso.

## 3. Relación conjunta de los estudios con la herramienta

Los cinco trabajos permiten entender la utilidad profesional como una combinación de información, interpretación y esfuerzo de uso. Mich et al. aporta peticiones vinculadas directamente a evaluación oral. Avant et al. concreta funciones para registrar y consultar una sesión. Thompson y Zimmerman sitúa la evidencia y el coste entre las condiciones de adopción. Francotte et al. explica el equilibrio entre seguimiento y carga docente. Cáceres Reche et al. añade contexto español sobre formación y recursos.

La aplicación final prevista reúne las siguientes dimensiones de utilidad profesional. La tabla sintetiza su relación con la literatura; no atribuye a los estudios la evaluación de estas funciones en nuestro producto.

| Dimensión | Significado para la herramienta | Estudios relacionados |
|---|---|---|
| Información diferenciada | Distinguir tiempo, precisión y eventos observados para que una cifra global no oculte dificultades distintas | Mich et al. |
| Revisión de la sesión | Relacionar resultados con audio, observaciones y registros que el profesional pueda examinar | Avant et al.; interpretación aplicada al diseño final |
| Seguimiento contextualizado | Consultar cambios dentro de una actividad y entre sesiones, teniendo en cuenta el texto y las condiciones | Mich et al.; Avant et al.; Francotte et al. |
| Confianza en las salidas | Explicar qué representa cada indicador y qué respaldo tiene; mantener distinguibles las hipótesis automáticas y las valoraciones profesionales | Thompson y Zimmerman; interpretación aplicada al diseño final |
| Esfuerzo de uso asumible | Reducir preparación, documentación e interpretación innecesarias | Avant et al.; Francotte et al.; Cáceres Reche et al. |
| Control de interrupciones | Diferenciar una pausa marcada por la profesora de los silencios del alumno durante su turno | Propuesta del proyecto, relacionada con la contextualización de tiempos; no evaluada en estos estudios |

En el escenario final, la herramienta articula la lectura compartida, el control docente y la consulta de información individual. El subrayado acompaña al grupo durante el cuento; la organización de turnos vincula cada intervención con su lector, y los informes permiten revisar la sesión y contextualizar la evolución de cada alumno. Los estudios seleccionados fundamentan distintas necesidades profesionales a las que responde este diseño, sin demostrar por sí mismos su eficacia educativa.



## Referencias

1. Mich, O., Mana, N., Gretter, R., Matassoni, M., & Falavigna, D. (2020). *Automatically Assess Children’s Reading Skills*. Proceedings of the 1st Workshop on Tools and Resources to Empower People with REAding DIfficulties (READI), 20–26. European Language Resources Association. [Publicación](https://aclanthology.org/2020.readi-1.4/).
2. Avant, J., et al. (2025). *Participatory Design: Addressing Speech-Language Pathologists’ Challenges through Collaborative Interface Design*. Design Issues, 41(2), 44–59. [DOI](https://doi.org/10.1162/desi_a_00805).
3. Thompson, K., & Zimmerman, E. (2019). *Pediatric Speech-Language Pathologists’ Use of Mobile Health Technology: Qualitative Questionnaire Study*. JMIR Rehabilitation and Assistive Technology, 6(2), e13966. [DOI](https://doi.org/10.2196/13966).
4. Francotte, E., Colognesi, S., & Coertjens, L. (2023). *Co-creating tools to monitor first graders’ progress in reading: a balancing act between perceived usefulness, flexibility, and workload*. Frontiers in Education, 8, 1111420. [DOI](https://doi.org/10.3389/feduc.2023.1111420).
5. Cáceres Reche, M. P., Trujillo Torres, J. M., Romero Rodríguez, J. M., & Berral Ortiz, B. (2024). *Teachers’ perceptions and experiences with mobile apps to enhance literacy skills in the classroom*. Porta Linguarum, número especial XI, 61–74. [DOI](https://doi.org/10.30827/portalin.viXI.30130).
