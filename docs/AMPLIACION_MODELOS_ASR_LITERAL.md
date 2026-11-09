# Ampliación de candidatos ASR y transcripción literal

Revisión documental del 06/11/2026. Fuentes primarias: fichas de los autores, documentación de proveedores y artículos. No se han instalado modelos nuevos, descargado pesos, enviado audios a servicios externos ni obtenido resultados propios. Esta lista no modifica las configuraciones fijadas de MLS test. Las prioridades son propuestas del proyecto, no rankings medidos.

## Candidatos adicionales para reconocimiento que alimente al seguidor

| Candidato | Evidencia documental y licencia | Interés para Lexia y límite pendiente |
|---|---|---|
| Moonshine Streaming Tiny/Small español | Modelos streaming en español; MIT para las variantes actuales. [Documentación oficial](https://moonshine-voice.readthedocs.io/en/latest/models/available-models/) y [Tiny es](https://huggingface.co/moonshine-ai/moonshine-streaming-tiny-es). | Primera prioridad para explorar ejecución local ligera. La ficha Tiny identifica 27 M parámetros, mientras la tabla general dice 34 M: fijar artefacto/revisión y contar parámetros reales, sin mezclar cifras. No valida tablet ni lectura infantil. |
| Granite Speech 5.0 470M TurboCTC | Español, CTC no autorregresivo, Apache-2.0; versión multilingüe publicada 21/10/2026. [Ficha IBM](https://huggingface.co/ibm-granite/granite-speech-5.0-470m-turboctc). | Alta prioridad para velocidad y alternativa arquitectónica. Requiere Transformers >=5.16 según ficha; comprobar dependencias y uso en ventanas antes de asumir streaming. No promete conservar sílabas cortadas. |
| Qwen3-ASR 0.6B y 1.7B | Español y modos offline/streaming, Apache-2.0. [Ficha Qwen](https://huggingface.co/Qwen/Qwen3-ASR-0.6B) y [artículo](https://arxiv.org/abs/2601.21337). | Comparar primero la variante 0.6B y después 1.7B si el coste lo permite. Nombre comercial no basta para estimar tamaño residente total. No confundir ASR con Qwen3-ForcedAligner, que necesita un texto previo y no recupera palabras omitidas. |
| Canary 1B v2 | Español entre 25 idiomas europeos; CC-BY-4.0. NeMo y ruta Transformers documentadas. [Ficha NVIDIA](https://huggingface.co/nvidia/canary-1b-v2). | Ampliar comparación con otra familia multilingüe. Elegir transcripción, no traducción; backend y memoria se medirán en nuestro servidor. No hay evidencia aquí de literalidad de trabadas. |
| Whisper large-v3-turbo y large-v3 | Variantes multilingües de 809 M y 1.550 M parámetros; MIT. [Ficha oficial](https://huggingface.co/openai/whisper-large-v3-turbo). | Controles de capacidad frente a nuestro Whisper Small. Son otros pesos/tamaños, no una arquitectura completamente distinta. No se consideran especialistas en disfluencias. |
| Granite Speech 5.0 2B | Español, Apache-2.0, modelo habla-lenguaje; [ficha IBM](https://huggingface.co/ibm-granite/granite-speech-5.0-2b). | Segunda ronda para precisión/ruido frente al CTC de IBM. La ficha recomienda segmentar audios largos; eso sería otra condición experimental. Prompt de transcripción sin formato no demuestra literalidad de errores. |
| Omnilingual ASR CTC/LLM, tamaños pequeños | Meta documenta familias 300M/1B/3B/7B y variantes v2. [Repositorio oficial](https://github.com/facebookresearch/omnilingual-asr). | Explorar la variante pequeña con comprobación de español, vocabulario, memoria y licencia exacta de pesos. Entorno fairseq2 aparte; no asumir compatibilidad con los perfiles actuales. |

La ficha Moonshine declara datos de entrenamiento procedentes de MLS, Common Voice y FLEURS, además de pseudoetiquetas. No se puede afirmar independencia respecto a nuestros tests sin comprobar las particiones/IDs. Su ficha también avisa de bucles de repetición y ausencia de evaluación infantil. Esas limitaciones justifican probarlo, no darlo por ganador. Sus cifras de WER publicadas no son directamente comparables con nuestras cifras.

## Alternativas para estadísticas y transcripción literal posterior a la lectura

| Opción | Qué está documentado | Cómo compararla |
|---|---|---|
| CrisperWhisper 2.0 medium / turbo / large | La documentación actual ofrece cuatro tamaños, modos verbatim/intended y licencia no comercial para investigación; Pro exige licencia comercial. [Ficha del proveedor](https://huggingface.co/nyralabs/CrisperWhisper2.0_small). | Comparar medium frente al small fijado antes de escalar a large. Es variación dentro de una familia, no competidor independiente. El modo verbatimize usa una transcripción de apoyo: no darle el cuento ideal cuando precisamente buscamos omisiones y errores de lectura. Las afirmaciones multilingües actuales no reemplazan la evidencia de nuestro checkpoint fijado. |
| ElevenLabs Scribe v2 | Servicio con español; no_verbatim=false mantiene el modo sin eliminación de muletillas/falsos comienzos; la opción opuesta los elimina. [Capacidades](https://elevenlabs.io/docs/overview/capabilities/speech-to-text) y [API](https://elevenlabs.io/docs/api-reference/speech-to-text/convert). | Alternativa independiente prioritaria si se decide comparar servicios. No demuestra captura fiable de todas las sílabas parciales de niños. No hay pesos para instalar en una tablet ni medición de GPU propia del servicio. No se ha usado la API. |
| Speechmatics | La documentación actual incluye español en etiquetado de vacilaciones y permite conservarlas con remove_disfluencies=false. [Formato](https://docs.speechmatics.com/speech-to-text/formatting) y [notas de versiones](https://speechmatics.featurebase.app/en/changelog). | Alternativa independiente; API o despliegue comercial según producto. Etiquetar sonidos de vacilación no equivale a reconocer todos los reinicios silábicos, sustituciones y autocorrecciones. Fijar modelo y versión, porque documentación antigua limitaba el etiquetado al inglés. |
| Omnilingual ASR, exploratorio | Su corpus documenta fragmentos con guion y repeticiones en raw_text. [Ficha del corpus](https://huggingface.co/datasets/facebook/omnilingual-asr-corpus). | Es una pista a investigar, no evidencia de que sus modelos preserven disfluencias españolas. Revisar preprocesado/normalización y medir contra referencias propias antes de clasificarlo como literal. |

No he localizado en esta revisión otro candidato abierto listo para usar con garantía demostrada de todos nuestros fenómenos en español infantil. No significa que no exista. Un ASR CTC también puede omitir disfluencias aprendidas como ruido; una instrucción de transcribir literalmente tampoco garantiza su recuperación.

## Evaluación que distingue los objetivos

Para reconocimiento general: misma muestra y referencias externas, WER/CER, fallos, inserciones extremas, tiempos y recursos. Para el seguidor real: posición, avances/retrocesos, recuperación y latencia con las mismas reglas; los resultados offline generales no equivalen a esas métricas.

Para literalidad: utilizar nuestras referencias humanas, con eventos marcados como fragmentos, repeticiones completas, autocorrecciones, sustituciones/omisiones, sonidos y pausas. Medir precisión, cobertura/recall y F1 por tipo, además de falsas palabras/disfluencias inventadas y pérdidas de voz por VAD. WER por sí solo puede premiar una salida que elimina justo los intentos que necesitamos contar. Evaluar fronteras temporales únicamente donde existan marcas humanas. No tratar el guion escrito como evento acústico suficiente.

La estadística literal se ejecutará al finalizar la lectura, cuando la solicite el profesor, como ya se acordó. VAD, limpieza y segmentación deben ser condiciones explícitas: no introducirlas solo en un competidor y atribuir la diferencia a sus pesos. Nunca completar la referencia humana desde una salida ASR.

## Integración y recursos

Las tarjetas actuales son RTX 3060 de 12 GB con driver 525.147.05. Aún no se ha probado ninguno de los candidatos nuevos en ellas. Separar entornos, fijar revisiones y dependencias; verificar requisitos CUDA/driver antes de descargar o instalar. No actualizar el driver/Python compartido para satisfacer un modelo. La VRAM no se deduce únicamente de parámetros: incluir activaciones, backend, precisión, duración y batch.

Para tablets: registrar primero plataforma/SoC/RAM y si el procesamiento será local o servidor. Moonshine, CTC y variantes cuantizadas son líneas interesantes, no compatibilidad certificada. Cuantización/runtime móvil constituyen condiciones nuevas que requieren su propia evaluación. Los servicios no exponen RAM/VRAM interna verificable: registrar coste, latencia de red y límites, y dejar recursos internos como no disponibles.

No se han transmitido voces de lectores a servicios ni contratado cuentas. Una prueba de API requeriría elegir audios autorizados para ese destino y condiciones; la autorización de publicación de lector_01 no es autorización automática para enviar otras voces.

## Artículo adicional para el estado del arte

[Learning to Hear Hesitation: Continual Learning for Disfluency-Aware ASR, Interspeech 2026](https://arxiv.org/abs/2606.14391) estudia aprendizaje continuo con marcadores explícitos de disfluencia y el compromiso con ASR general. Referencia metodológica, no modelo español listo para integrar confirmado en esta revisión.

## Prioridad propuesta

Primer grupo local nuevo: Moonshine español, Granite TurboCTC y Qwen3-ASR 0.6B. Segundo: Canary, Whisper Turbo/large y modelos mayores si aportan mejoras. Literal: Crisper medium más Scribe v2/Speechmatics si se acuerda evaluar servicios; Omnilingual como exploración. No sustituir candidatos de MLS test a mitad del protocolo ni ajustar los nuevos con sus resultados test.
