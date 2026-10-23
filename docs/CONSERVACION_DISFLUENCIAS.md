# Conservar y cuantificar disfluencias en Lexia

23/10/2026. Investigación y piloto de diagnóstico, antes de continuar con el lote. El objetivo es conservar eventos pronunciados para las estadísticas además de seguir la posición del cuento. Los WAV originales se conservan y permiten volver a analizar lo que no aparece en las hipótesis.

## Evidencia propia y diagnóstico

El lector revisó cuatro muestras de la lectura con trabadas (0–8, 16–24, 34–42 y 48–56 s) y valoró simplificación con ambas ventanas. Esto no significa que el ASR elimine el 100 % de los eventos: cuatro valoraciones cualitativas no proporcionan un denominador de episodios o sílabas. Las notas describen intentos parciales y repeticiones, sin límites por evento ni transcripción literal exhaustiva.

La configuración instalada de faster-whisper usa repetition_penalty=1 y no_repeat_ngram_size=0 por defecto: no estamos imponiendo una penalización adicional de repeticiones ni prohibición de n-gramas. initial_prompt proporciona contexto; no convierte automáticamente Whisper en un transcriptor literal. Nuestro reconocimiento habitual usa VAD, marcas de palabra y alineamiento textual, por lo que hay que separar sus etapas antes de atribuir la pérdida.

scripts/diagnosticar_vad_trabadas.py reproduce el VAD sobre 32 ventanas originales de ronda 1 alrededor de las cuatro muestras: 25 se conservan completas. En seis ventanas de inicio se retiran 0,432 s y en otra se retiran 0,112 s. Son ventanas solapadas, no 32 eventos independientes ni pérdidas acumulables del audio. Falta comprobar qué se oye en las partes recortadas para atribuir un evento a ese recorte. Fuente: diagnostico_vad_trabadas.json dentro de la comparación con trabadas.

scripts/probar_vad_literal.py ejecuta ocho transcripciones nuevas: cuatro fragmentos de 8 s con VAD sí/no, orden alternado, small CPU int8, mismas opciones y modelo local, guardando segmentos.text, palabras originales, palabras normalizadas y recursos del piloto. Salida: resultados/disfluencias/20261023_122442_840773. En cada fragmento, el texto bruto coincide entre condiciones y ya simplifica los intentos/repeticiones descritos por el lector; por ejemplo, «regre re regresaron» aparece como «regresaron». Desactivar VAD no resuelve estas muestras. Es una pasada por condición, no una estimación de mejora estadística ni de todos los modos de fallo. Los tiempos usan un modelo compartido y no se comparan directamente con rondas históricas. El texto bruto también muestra simplificación, de modo que la extracción de palabras de nuestro seguidor no es su única explicación.

## Vías candidatas y prioridad

| Vía | Qué se probaría | Qué demostraría una mejora | Límites |
|---|---|---|---|
| Ajustes del ASR actual | Contexto literal de ejemplo sin revelar las respuestas del fragmento; decodificación y fallback como factores separados. Conservar texto bruto y palabras. | Recupera eventos reales sin inventarlos en controles fluidos o ruido. | Una instrucción no garantiza obediencia. Desactivar límites puede generar bucles; más repeticiones escritas no significa más fidelidad. |
| Reconocedor orientado a transcripción literal | Evaluar un candidato especializado como CrisperWhisper 2.0; comprobar español, licencia del artefacto y recursos. Como comparación de arquitectura, un CTC español, por ejemplo wav2vec2-XLSR. | Mayor recuperación de eventos y menor error de conteo con el mismo audio y referencia. | No se ha descargado ni probado ninguno. Las pruebas consultadas de otros idiomas no validan español o lectura infantil; CTC tampoco garantiza conservar fragmentos. |
| Análisis acústico de eventos | Detector de repeticiones e intentos incompletos sobre audio, opcionalmente fusionado con ASR y texto esperado. | Detecta y localiza episodios que no aparecen en la transcripción. | Necesita referencias de eventos y validación; no basta contar picos, pausas o discrepancias textuales. |
| Adaptación de un modelo | Ajuste con datos de español etiquetados literalmente y por evento, si las opciones anteriores no bastan. | Mejora sobre voces/textos reservados sin degradar controles. | Las cuatro muestras actuales no son suficientes para entrenar ni demostrar generalización. |

Propuesta de arquitectura a evaluar: mantener la rama de seguimiento y añadir una rama de análisis de la lectura que use el audio original. La segunda podría ejecutarse después de leer, para medir primero su calidad y coste antes de exigir ambas en tiempo real en una tablet. Esto es una propuesta, no una implementación activada ni garantía de rendimiento móvil.

## Referencia mínima y estadísticas válidas

Definir un episodio alrededor de una palabra o tramo objetivo y distinguirlo de cuántos intentos contiene. Un intento parcial puede ser además una repetición: las etiquetas pueden solaparse sin contar dos veces el mismo episodio. Anotar solo un pequeño conjunto de eventos inequívocos de los fragmentos ya revisados, con intervalo aproximado, tipo, palabra/tramo, intentos cuando sean distinguibles, procedencia e incertidumbre. Acordar la convención y el criterio de correspondencia temporal antes de comparar opciones. No convertir la ortografía libre de las notas en un conteo fonético automático.

- Recuperación por tipo: eventos reales recuperados frente a eventos revisados de ese tipo.
- Precisión: eventos propuestos que tienen respaldo humano; conservar falsos positivos y controles fluidos/ruido.
- F1 por tipo y error absoluto de conteo por episodio; medir número de intentos solo donde la referencia sea clara.
- Si se revisan intervalos, localización temporal y duración con tolerancia fijada previamente. Una marca aproximada no es un límite fonético exacto.
- WER/CER literal solo con referencia compatible y normalización que preserve intentos; calidad de palabras pretendidas y seguimiento se evalúan por separado. Comparar con el cuento correcto puede ocultar las omisiones del lector.
- Coste: CPU/RAM, tiempo e instrumentación disponibles; evaluación específica en tablet posteriormente. No presentar GPU global o tiempos simulados como consumo propio o latencia visual.

No sumar las repeticiones de todas las hipótesis solapadas: pueden describir el mismo episodio, y una revisión del ASR no es un nuevo intento lector. El análisis final necesitará correspondencia y deduplicación temporal de eventos. Dato no detectado, referencia pendiente o conteo dudoso no equivalen a cero disfluencias.

Próximo experimento recomendado: comparar el ASR actual y una variante orientada a literalidad sobre estas muestras y controles revisados, con el seguidor congelado. Primero explorar calidad, después repetir y ampliar voces/textos con criterios ya fijados. Se mantiene el banco de audios y se crea una referencia más útil para comparar entornos; no se necesita regrabar todo ni elegir un motor ganador ahora.

## Fuentes primarias revisadas

- [Implementación de faster-whisper](https://github.com/SYSTRAN/faster-whisper/blob/master/faster_whisper/transcribe.py): opciones de repetición, prompts, VAD y salida de palabras; contrastadas con la versión instalada.
- [Smith et al., Interspeech 2025](https://www.isca-archive.org/interspeech_2025/smith25_interspeech.html): relaciona reconocimiento literal y detección de errores de lectura. Su sistema incorpora texto y entrenamiento; no demuestra que una instrucción en nuestro modelo sin adaptar reproduzca sus resultados.
- [Ferreira et al., DiSS 2025](https://www.isca-archive.org/diss_2025/ferreira25_diss.html): estudia fusión acústica/textual, con resultados favorables a cierta combinación de audio y texto de estilo pretendido en sus experimentos. Motiva la rama acústica; no valida automáticamente nuestra tarea española.
- [CrisperWhisper 2.0, ficha del modelo](https://huggingface.co/nyralabs/CrisperWhisper2.0_large): ofrece estilos literal/pretendido y anuncia capacidad multilingüe; modelo estándar con licencia de investigación no comercial. Las cifras y afirmaciones son de sus autores, sin medida propia en Lexia.
- [Benchmark de los autores de CrisperWhisper](https://nyra-labs.com/research/nyra-verbatim-speech-benchmark): evalúa conservación por tipos de evento; el texto consultado detalla inglés/alemán. No trasladar cifras a español ni a tablet.
- [wav2vec2-XLSR español, ficha del autor](https://huggingface.co/jonatasgrosman/wav2vec2-large-xlsr-53-spanish): candidato CTC en español; sus resultados de ASR no son una validación de conservación de trabadas.

## Piloto posterior de la rama literal

23/10/2026. Se instala CrisperWhisper 2.0 Small en un entorno separado y se comparan siete recortes fijados: cuatro muestras con trabadas, dos fluidas y una sin habla. No se modifica el seguidor. Salida resultados/literalidad/20261023_124047_726452 y protocolo pruebas/23_piloto_literalidad.md. El candidato conserva formas como «lu- lucia pa- paseaba» y «la la ayudó y y», pero el lector confirma una inserción en Intermedio 1: la última frase «el barco rojo» no se oye en sus 16–24 s. No contar esa aparición como repetición del lector; causa no determinada y resto pendiente de validación por evento. Ambos motores dejan vacío el control sin habla. No hay tasa de recuperación ni precisión por evento todavía.

Coste observado: actual CT2 int8 14,08 s de inferencia, 696,73 MiB de pico de RAM; candidato Transformers float32 50,37 s, 4.252,89 MiB. Incluyen distintos backends/precisiones y una pasada; el pico es del proceso durante toda su vida. No se extrapola a tablet. El cargador del candidato avisa de tensores auxiliares inesperados y de compatibilidad de atención/generación: los tiempos de palabra quedan sin validar. Modelo, paquetes, archivos y referencias están fijados/verificados; no se publican automáticamente. Próximo contraste compartido en el visor http://127.0.0.1:8775/: validar conservación e invenciones antes de cuantificar o adoptar el motor.

Contraste solicitado con el WAV completo (60 s): resultados/literalidad/20261023_131712_130708/comparacion_contexto.md. La última frase añadida «el barco rojo» del recorte ya no aparece como tal, con continuación «el el barco el barco flotaba…». Los recortes anteriores coinciden exactamente con sus intervalos; el candidato activa procesamiento largo por bloques 30 s/paso 26 s y contexto generado. No se aísla una causa ni se valida toda la transcripción; ahora el bloque inicial contiene también audio 24–30 s. Inferencia actual/candidato 5,23/15,50 s; pico RAM 696,68/4.417,32 MiB. Una pasada offline, con silencio final; no latencia visual ni tablet. Visor completo y recortes en http://127.0.0.1:8776/. Publicación autorizada por el usuario, conservando estas limitaciones.

**Revisión del audio completo por el lector.** El lector completa la escucha y valora el resto como bastante fiel; señala una omisión de intento: se oye «regres- re- regresaron» y el candidato escribe «regres- regresaron». Es un episodio conservado parcialmente, con tres intentos humanos (dos parciales y la palabra completa) frente a dos escritos; falta «re-». Confirmación con huellas en datos/anotaciones/lectura_02_literal_completa_revision.json, sin tiempos humanos interiores ni anotación exhaustiva por evento. No se calcula un porcentaje global de precisión. Las salidas ASR originales permanecen intactas; no se ejecuta reconocimiento nuevo.
