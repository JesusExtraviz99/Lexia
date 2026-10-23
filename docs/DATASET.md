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
