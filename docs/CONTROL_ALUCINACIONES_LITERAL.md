# Control de texto inventado y conservación de eventos

25/10/2026. Investigación y diagnóstico de la rama literal. Modelo y ajustes del lote permanecen intactos. El primer ensayo de entrada limitada por VAD ya se ha ejecutado aparte; no hay parámetros adoptados en el seguidor habitual.

## Dos problemas distintos

En 1, 4, 5, 6 y 11 hay continuaciones ajenas a las referencias disponibles en los bloques finales; 4 además sustituye palabras dentro de la lectura y 5 omite una palabra. En 17 aparecen grafías/segmentación como Consu y Suu: no deben confundirse con frases finales inventadas ni con la omisión deliberada de abuelo, que el ASR debe conservar. El episodio regres- re- regresaron pierde un intento aunque conserve la palabra final. Una sola corrección no resuelve los tres problemas: inserciones, errores lexicales y conteo de intentos.

El modo literal sigue siendo un instrumento con error. Para las estadísticas se necesita cuantificar qué eventos conserva, cuáles añade y cuáles quedan sin resolver, con referencias por episodio y por intento; no convertir automáticamente toda su salida en hechos sobre el lector.

## Evidencia del diagnóstico VAD

Se ejecuta Silero v6 ya incluido en faster-whisper sobre los mismos 17 arrays del lote resultados/literalidad/20261025_182446_557677_UTC. Es inferencia VAD nueva; no se repite ASR ni se cambian audios/transcripciones. Resultados y fuente exacta: diagnostico_vad_literal.md/.json y fuente_diagnostico_vad.txt en esa carpeta.

Parámetros iniciales: threshold 0,5; min_speech_duration_ms 0; min_silence_duration_ms 2000; speech_pad_ms 400. Son un punto de partida, no valores ideales demostrados. Las zonas positivas contienen margen y pueden incluir silencio; no son etiquetas humanas ni detectan de forma infalible toda voz débil.

| Audio | Bloque final con texto añadido | Segundos de solapamiento con zonas VAD positivas, incluido margen |
|---|---|---:|
| 1 | 26–40 s | 0 |
| 4 | 78–90 s | 0 |
| 5 | 52–60 s | 0 |
| 6 | 52–60 s | 0 |
| 11 | 78–90 s | 0 |

Las 75 anclas humanas ya revisadas de los audios con anotación están completamente dentro de las zonas VAD con margen. Esto comprueba esos intervalos disponibles; no mide sensibilidad global ni demuestra que estén protegidos todos los intentos parciales, muchos sin tiempos humanos. En el último bloque de muchas trabadas hay 4,528 s positivos con margen, y en el de omisión de abuelo 1,632 s: no sería adecuado descartar todos los últimos bloques de forma fija.

Inferencia VAD total: 1,68 s para 880 s de entrada, con carga y CPU/RAM/GPU global registradas aparte. No es una medida de tablet ni coste ASR nuevo. Las 80 pruebas del proyecto pasan tras añadir comprobaciones de unión/intersección de intervalos. Las salidas ASR del lote conservan sus SHA256.

## Primer ensayo recomendado: proteger los finales sin voz

Comparar el candidato original con una variante de análisis offline que use el VAD para limitar el reconocimiento del final posterior a la última voz detectada con margen, conservando todo el audio anterior y sus pausas internas. No reescribir el WAV original ni concatenar zonas de voz eliminando pausas. Guardar el intervalo enviado, duración original, duración enviada, márgenes y relación temporal. Los silencios originales siguen disponibles para medir las pausas. Si no se detecta voz, registrar ese estado y permitir revisión; no inventar una transcripción ni declarar ausencia humana de habla a partir del VAD solo.

Una alternativa de implementación es omitir únicamente bloques internos sin solapamiento VAD. Debe ensayarse aparte de recortar la cola: puede requerir integrar la decisión en la estrategia de continuación y gestionar sus límites/contexto. No aplicar dos cambios a la vez ni asumir equivalencia entre ambos métodos. Acortar la entrada puede cambiar la geometría de bloques y la ruta corta/larga; se registra como cambio de la canalización completa, no prueba causal de un parámetro interno.

Primero usar los seis audios señalados más controles de lectura normal del cuento 2 y muchas trabadas; siguen siendo desarrollo. Evaluar si desaparecen frases añadidas y si aparecen pérdidas nuevas, especialmente la última palabra, sílabas breves, relecturas tras pausa y episodios con varios intentos. Si resulta favorable, aplicar a los 17 y después comprobar audios nuevos reservados antes de fijar ajustes. Las anclas humanas son comprobación externa, no se emplean para decidir dónde recortar cada audio de evaluación.

## Segundo ensayo: mecanismos de continuación, uno por vez

La instalación y documentación oficial confirman que ya estaban activadas hallucination_mitigation, temperature_fallback y early_eot_recovery. No basta con activar una protección que ya estaba presente. La mitigación trata bucles de tokens; no garantiza que toda frase generada tenga apoyo acústico.

Comparar con la configuración original una variante con early_eot_recovery=False y otra con temperature_fallback=False, manteniendo el resto idéntico. La primera evita el intento adicional de prolongar cierres sospechosos; la segunda evita redecodificaciones a temperaturas alternativas cuando la cobertura parece escasa. No se afirma que hayan disparado nuestros fallos: las salidas actuales no registran esa traza. Instrumentar las activaciones en los ensayos, sin modificar silenciosamente el paquete ni atribuir el resultado a un mecanismo no observado.

Cambiar la estrategia de continuación/contexto sería otro contraste posterior independiente. Desactivar indiscriminadamente repeticiones, aplicar listas negras de palabras o corregir todo hacia el cuento puede borrar precisamente los datos buscados. El detector de bucles también necesita comprobación en repeticiones reales intensas; no atribuirle el intento re- perdido sin traza del decodificador.

## Errores que no arregla un filtro de finales

Despacio/desváceo y cuaderno/jugador no suceden durante voz real; el VAD no decide qué palabra se pronunció. Necesitan contraste lexical/acústico y, si persisten, comparar otros modelos literales o un reconocedor acústico complementario en español sobre los mismos audios. Su desacuerdo permite priorizar revisión, pero no establece automáticamente la verdad. Una grafía como Suu no demuestra una prolongación fonética sin evidencia temporal/acústica.

No usar el cuento correcto como transcripción literal de una lectura con errores: restaurar abuelo o convertir azul en rojo invalidaría las estadísticas del lector. El texto del cuento sirve al seguimiento; la referencia de lo pronunciado debe conservar omisiones, sustituciones e intentos reales. Los tramos dudosos se marcan como no resueltos antes de emitir conteos definitivos. Las marcas automáticas del candidato y sus advertencias de compatibilidad siguen pendientes de validación antes de medir duraciones.

## Fuentes y alcance

Primer contraste realizado: [protocolo y resultados](../pruebas/25_final_vad_literal.md), resultados/literalidad/20261025_193651_692690_cola_vad_UTC. Ocho inferencias nuevas frente a textos originales reutilizados: desaparecen los cinco añadidos finales conocidos y no cambia el resto del texto reconocido; controles normal/trabadas y audio 17 idénticos. Persisten errores dentro del habla y el intento re- perdido. Entrada 480→341,12 s, inferencia previa/nueva 287,48/87,95 s (contextos de medición distintos). Se verifican prefijos, fuentes y 66 anclas disponibles; no es evaluación independiente ni fidelidad completa. Pendiente de revisión compartida.

- [Silero VAD, repositorio oficial](https://github.com/snakers4/silero-vad): detección de actividad de voz. En este diagnóstico se usa la adaptación instalada en faster-whisper, con modelo ONNX y código fijados por SHA256 en el resultado.
- [CrisperWhisper, documentación oficial](https://github.com/nyrahealth/CrisperWhisper/blob/main/DOCS.md): continuación, recuperación de cierres, temperaturas alternativas y reparación de bucles. Contrastado con crisperwhisper 2.0.3 instalado; las garantías y cifras publicadas por los autores no sustituyen nuestros resultados.
- [Ficha oficial del candidato Small](https://huggingface.co/nyralabs/CrisperWhisper2.0_small): estilos literal/pretendido y capacidades declaradas. En Lexia se mantiene la revisión fijada del piloto; no se actualiza el modelo al consultar la ficha actual.

Datos internos: auditoria_errores_lector.md/.json, manifiesto del lote, referencias del propio lector y diagnostico_vad_literal.md/.json. Sin descarga nueva, limpieza del audio, transcripción nueva, adopción de ajustes o publicación automática.
