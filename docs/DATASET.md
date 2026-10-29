# Dataset de evaluación de Lexia

Fecha de diseño: 21/10/2026. Prioridad acordada: consolidar un banco documentado y reproducible antes de comparar otros sistemas. Cambiar de reconocedor reutilizando exactamente los mismos audios, referencias y criterios. Aumentar grabaciones no equivale por sí solo a mejorar el dataset: hacen falta cobertura y referencias fiables.

## Estado actual e identidad de audios

23/10/2026: 17 WAV locales verificados, 14 minutos y 40 segundos, dos textos y un adulto. Los siete nuevos corresponden al segundo cuento: lenta, rápida, pausa con relectura, sustitución, ruido de calle reproducido desde móvil, fragmentos/repeticiones y omisión de las dos apariciones de abuelo. Todos se han visto durante desarrollo; no constituyen prueba final independiente. Las rondas repiten cómputo sobre un WAV, no aportan nuevas voces/lecturas. Los propios archivos de datos/audio tienen nombres descriptivos; sus metadatos técnicos están en datos/referencias/catalogo.json. El lote selecciona archivos presentes con huella coincidente, no cuenta como otro WAV una entrada histórica sin contenido local coincidente.

Cada audio conserva su ID y SHA256. El nombre físico del WAV incluye tipo, cuento y fecha; disfluencias/relecturas especifican qué ocurrió. Desde el 23/10/2026 el catálogo guarda la ruta actual y los nombres antiguos como alias: los scripts resuelven las referencias históricas sin reescribir los JSON originales ni las anotaciones humanas. No se generan índices Markdown adicionales. La selección automática del último audio usa fecha de modificación, no orden alfabético. Un nombre describe la consigna hasta confirmar por escucha lo que ocurrió; no valida automáticamente su transcripción.

Se conservan por separado: texto esperado, transcripción literal revisada (con repeticiones e intentos incompletos), eventos observados, tiempos revisados y artefactos ASR. No etiquetar cinesio o despedidas inventadas como errores del lector. Ruido observado no demuestra causalidad de una alucinación. No llamar disfluencia a una voz o condición clínica sin evidencia.

## Dos componentes complementarios

**Grabaciones propias:** lecturas continuas de textos narrativos, descriptivos o informativos, cortos y largos dentro de los límites de las herramientas (hasta 120 s en seguimiento actual). Incluir normales, lentas, pausas, omisiones/sustituciones, repeticiones/autocorrecciones y relecturas cercanas/lejanas. Añadir secuencias repetidas en el texto para probar ambigüedad, sin eliminar los fallos observados. Registrar condiciones reales de ambiente/equipo, evitando atribuir intensidad/SNR sin medirlos. Ampliar hablantes además de textos. Las desviaciones provocadas por un adulto son casos controlados, no representaciones validadas de lectura infantil.

**Dataset externo:** el enlace facilitado es Common Voice Scripted Speech 27.0 - Spanish, MP3, CC0-1.0, paquete mostrado 48,38 GB. Fuente: https://mozilladatacollective.com/datasets/cmu5kitx700pemi073feoiqqu (consultada el 21/10/2026). Sus condiciones prohíben reidentificar hablantes y volver a alojar/compartir el dataset. Solo guardar aquí procedencia, selección y resultados; los audios/descargas externos quedan ignorados por Git. No se ha descargado el paquete. Su función propuesta es evaluar ASR con más voces: no proporciona automáticamente nuestros eventos de relectura ni tiempos humanos. No concatenar clips y presentarlos como lectura continua natural. Los clips invalidados no son por sí solos disfluencias etiquetadas. La frase que se pidió leer tampoco sustituye comprobar lo realmente dicho.

## Cobertura y tamaño inicial propuesto

Trabajar por lotes revisables, no grabar cientos de casos sin un esquema previo. Como arranque orientativo, tres textos nuevos por seis condiciones producirían 18 lecturas adicionales; revisar cobertura/fallos y añadir voces antes de decidir tamaño final. Una muestra externa de 100–200 clips podría servir como primera comprobación de importación y métricas, no como tamaño estadísticamente suficiente garantizado. Estos números son propuestas pendientes de acordar, no grabaciones realizadas ni un cálculo de potencia estadística.

Cubrir texto, hablante, ritmo, evento, posición del evento y ambiente de forma equilibrada en la medida posible. No mezclar cambios de texto, modelo y filtros en una comparación que pretende aislar una sola variable. Conservar audios crudos y procesados con parentesco explícito. Una variante con reducción de ruido no cuenta como otra lectura independiente.

## Particiones y congelación

- Desarrollo: los diez audios ya utilizados, para diseñar/diagnosticar reglas.
- Validación: material nuevo para comparar opciones durante el trabajo; separar por hablante y/o texto según la pregunta, documentando qué puede generalizarse.
- Prueba final reservada: audios nuevos asignados antes de consultar salidas del sistema. Cerrar reglas, muestra, normalización y métricas antes de abrir resultados. No reajustar y seguir llamándolo test independiente.

Evitar que el mismo hablante/texto o copias procesadas crucen particiones cuando se evalúa generalización a voces/textos nuevos. Mantener splits oficiales de fuentes externas y documentar cualquier selección. No asumir que Common Voice no se usó para entrenar el modelo preentrenado: si no se conoce, registrar posible solapamiento/contaminación. Comparar audios propios y externos por estratos y no esconder diferencias en una sola media global.

Cada versión del banco tendrá manifiesto con IDs, hashes, fuentes, partición, versión del texto, semilla/lista de selección, lector anonimizado, condiciones y estado de revisión. Guardar el conjunto concreto usado en cada experimento; no seleccionar automáticamente todo lo que aparezca en la carpeta.

## Referencias y métricas

Para ASR: transcripción literal revisada y normalización explícita para WER/CER, conservando en una evaluación separada los fragmentos/repeticiones relevantes. No comparar WER calculados con convenciones diferentes. No hay WER/CER nuevos calculados con esta catalogación.

Para seguimiento: posición/errores con referencias humanas disponibles, recuperación y falsos retrocesos, conservación del final, omisiones/repeticiones cuando estén etiquetadas, y demora de reubicación. Distinguir primera identificación parcial, palabra completamente disponible y respuesta visible. No interpolar tiempos interiores no anotados ni dar métricas temporales exactas a un clip sin anclas.

Para cómputo: tiempos por corte y percentiles, carga del modelo, RTF, cola, CPU/RAM/GPU, configuración y versión de instrumentación según docs/METRICAS_COMPUTO.md. Misma instrumentación en todas las opciones; la reproducción de hipótesis no mide otra inferencia. Recursos del ordenador no son consumo de la tablet. Reportar fallos y datos ausentes. Resumir variación entre audios/hablantes aparte de las rondas de cómputo; no tratar las rondas como observaciones independientes para intervalos de confianza.

## Uso de nombres y comprobación

```powershell
.\.venv\Scripts\python.exe -m scripts.catalogo --verificar
```

Muestra nombre, archivo, duración y partición y verifica hashes. Para etiquetar Markdown existentes sin modificar JSON:

```powershell
.\.venv\Scripts\python.exe -m scripts.catalogo --actualizar-informes
```

Para grabaciones nuevas se admiten --nombre, --caso, --lector y --ambiente en grabar.py. Ejemplo de uso futuro, no ejecutado:

```powershell
.\.venv\Scripts\python.exe scripts\grabar.py --segundos 40 --cuento .\datos\textos\lectura_02.txt --nombre "Lectura normal - cuento 2" --caso normal --lector adulto_01 --ambiente "lluvia de fondo"
```

El WAV conserva identificador único y el catálogo añade fecha a la etiqueta. Una grabación nueva empieza sin partición asignada ni referencia validada; clasificarla antes de evaluar. Los nombres normales de archivo son compatibles con Windows; las barras de la fecha se reservan a la etiqueta legible.

El siguiente trabajo es acordar la matriz de cobertura y las particiones, completar la revisión temporal pendiente del segundo cuento y preparar el primer lote. Revisar acceso y método de selección de Common Voice antes de iniciar una descarga grande. No se cambia todavía de modelo ni se publican nuevos datos automáticamente.


## Actualización metodológica · 28/10/2026

El usuario transmite el criterio del profesor: preseleccionar reconocedores con datasets públicos y usar después el banco propio para decidir entre los finalistas según lectura asistida. Este orden pasa a orientar las comparaciones siguientes; no convierte retrospectivamente las pruebas exploratorias anteriores en evaluación ciega. No se descargan datos/modelos ni se ejecuta ASR en esta revisión.

En modelos/ constan únicamente faster-whisper-small y crisperwhisper2-small. Nuevas candidaturas propuestas, aún no instaladas:
- [wav2vec2 XLSR-53 español](https://huggingface.co/jonatasgrosman/wav2vec2-large-xlsr-53-spanish), CTC, afinado con train/validation de Common Voice 6.1.
- [Vosk español Small 0.42](https://alphacephei.com/vosk/models), modelo de 39 MB orientado también a Android; el tamaño del archivo no equivale a RAM medida en tablet. La variante grande es otra configuración, no una cuarta familia.
- [Parakeet TDT 0.6B v3](https://huggingface.co/nvidia/parakeet-tdt-0.6b-v3), transductor multilingüe con español. La ficha señala limitaciones para transcripción palabra por palabra/frases incompletas; incluirlo como contraste de ASR general no supone validarlo para intentos parciales.
Whisper se conserva como referencia y CrisperWhisper como candidato literal ya explorado de la misma familia; no son arquitecturas independientes. Ejecutores, versiones, precisión y hardware se documentarán por separado de los pesos del modelo. No se han elegido ganadores.

Fuentes públicas adicionales revisadas, aún sin importar:
- [FLEURS de Google](https://huggingface.co/datasets/google/fleurs), configuración es_419, audio/texto y licencia CC-BY-4.0. Propuesta de primera preselección manejable; añadir diversidad de fuentes con Common Voice cuando esté importado.
- [Multilingual LibriSpeech, español](https://www.openslr.org/94/), fragmentos leídos de audiolibros y particiones train/dev/test, CC-BY-4.0. Complemento de dominio; no sustituye relatos propios con errores ni se concatenará para simular lectura continua.
FUENTES.json añade fichas/procedencia, no audios descargados. Common Voice sigue en esa carpeta solo como ficha: no se ha comprobado una descarga que el usuario pueda tener fuera del proyecto.

Criterio propuesto: fijar una muestra externa compartida y su versión/IDs antes de consultar salidas; usar validación/desarrollo para preseleccionar y reservar test para comprobar ajustes ya cerrados. WER/CER con normalización idéntica, errores por estratos, inserciones/omisiones/sustituciones y recursos (tiempo, RTF, carga, RAM y GPU realmente atribuible cuando pueda medirse). No comparar solo cifras publicadas en fichas ni mezclar muestras. Auditar posible solapamiento de entrenamiento: Common Voice 27 puede contener clips de versiones anteriores y XLSR declara Common Voice 6.1, por lo que una versión posterior no garantiza independencia.

Conservar dos o tres finalistas por compromiso entre precisión/coste, sin descartar un literal únicamente por su posición en WER de lectura fluida. El corpus público de palabras completas no valida conservación de fragmentos. En el banco propio se medirán por separado seguimiento y literalidad: repeticiones/intentos/autocorrecciones, omisiones reales, falsos añadidos, pausas y recuperación. Las transcripciones de referencia se revisarán antes de convertirlas en conteos.

Los 23 WAV anteriores ya se han usado en exploraciones; los 26 de las tandas límite/texto 3/texto 5 todavía no tienen reconocimiento de esta recogida. Antes de evaluar, verificar de nuevo disponibilidad y resultados existentes y fijar qué se usará para selección y qué quedará reservado. Las reservas anteriores no se reasignan. Elegir un ganador con el banco propio es selección para la tarea, no una prueba final independiente si se sigue reajustando con él. Mantener la limitación de un adulto, sin validación de población infantil. Todo cambio de filtro requiere comparación con originales y referencias, preservando pausas y cronología. El usuario todavía no ha cerrado la recogida completa.


## FLEURS disponible localmente · 28/10/2026

FLEURS es_419 importado desde Descargas en datos/externos/fleurs_es_419: originales comprimidos en archivos/, tablas en la raíz y WAV en audio/dev, audio/test, audio/train. Se conservan originales sin conversión. Resultado técnico completo en datos/externos/fleurs_es_419_verificacion.json e índice local por archivo. Dev 408, test 908, train 2.796; total 4.112 audios, 47.697,6 s. WAV FLOAT mono 16 kHz. Copia/CRC, correspondencia TSV y decodificación completa correctas, sin faltantes/sobrantes o audio idéntico cruzado. Hashes locales, no contrastados con hashes publicados. Sin evaluación ASR ni referencia humana nueva. El corpus propio permanece separado (49 audios según última comprobación); no sumar estos clips como nuevas lecturas propias. MLS tiene carpeta mls_es preparada y su descarga sigue pendiente de importar. Datos externos excluidos de Git.

La estructura vigente sitúa cada dataset directamente bajo datos/externos: fleurs_es_419 y mls_es. Se retiró solo la carpeta descargas ya vacía; índices, registro de fuentes y scripts apuntan a las rutas nuevas. Las huellas de los 4.112 WAV y de las seis entradas originales permanecen iguales. La fuente histórica de importación se conserva sin reescribir.
