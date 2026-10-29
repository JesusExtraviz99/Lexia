# Revisión inicial de las seis lecturas de La caja del sendero

26/10/2026. Análisis documental de salidas y declaración del lector, pendiente de escucha compartida detallada. No es una revisión auditiva independiente ni una referencia literal completa.

Seis WAV nuevos, 670 s. Tres pasadas secuenciales sobre esta tanda: actual completo, literal completo y mismo literal con prefijo hasta última voz Silero VAD (margen 400 ms incluido). Sin cuento/consignas como prompt, sin ajustes nuevos del modelo, sin concatenar intervalos ni borrar pausas interiores. Los 17 WAV anteriores no se vuelven a reconocer.

| Toma | Observación que debe contrastarse escuchando |
|---|---|
| 1. Normal | Actual añade una frase de canal/subtítulos al final. Literal completo y VAD tienen texto idéntico, sin esa frase. |
| 2. Repeticiones | Literal conserva las cuatro repeticiones confirmadas por consigna/lector; actual conserva Mateo Mateo y junto junto pero simplifica una una y Clara Clara. El VAD elimina solo el sufijo literal ¿Para qué? |
| 3. Intentos | Ambas salidas conservan pe/pe y des/des, con puntuación distinta. Ambas simplifican regres- re- regresar a regresar; se requiere escuchar ese tramo para confirmar la secuencia exacta. VAD elimina solo ¿Para qué? |
| 4. Omisiones/sustituciones | Literal conserva roja y parque y no restaura madera/viejo. Actual pierde además regresar en Antes de..., según comparación con consigna; revisar audio. VAD y literal completo son idénticos. |
| 5. Pausa | Literal VAD conserva toda la lectura posterior a la pausa y elimina únicamente P- p. P- p. final. No hay marcas humanas para medir los 8 s ni probar cobertura de todas las sílabas. No usar este caso reservado para ajustar reglas. |
| 6. Mixta | Ambos escriben descubrieron encontraron, compatible con la autocorrección recordada por el lector. Literal escribe más parciales; no equivalen aún a eventos validados. VAD elimina solo P- por favor, si te da la pena... final. La etiqueta inicial [yawn] y fragmentos como Levam/la casa requieren escucha: no declararlos correctos, invenciones o estadísticas automáticamente. Caso reservado para comprobar cambios posteriores. |

## Control del límite final

En las seis nuevas salidas, el texto es un prefijo exacto del literal previo. Tomas 1/4 idénticas; en 2/3/5/6 solo cambian los sufijos indicados, compatibles con las continuaciones finales no previstas según declaración del lector. Esto demuestra estabilidad del resto de la salida escrita, no fidelidad completa ni ausencia de habla perdida por el VAD. No hay anclas humanas temporales nuevas (0 disponibles, no 100% de cobertura).

Duraciones enviadas: 52,592 / 65,840 / 70,320 / 59,984 / 72,112 / 98,160 s; total 419,008 s. Originales intactos. Inferencia total actual 99,14 s; literal completo 213,46 s; literal VAD 118,86 s. Cargas, CPU/RAM/GPU global y recursos por audio en JSON. VAD medido aparte, backends distintos, procesos y cargas distintos, una pasada: no demuestra rendimiento móvil ni precisión superior global.

## Revisión desde el ordenador del lector

- Actual frente a literal completo: http://127.0.0.1:8780/
- Literal completo frente a literal VAD: http://127.0.0.1:8781/

Ambos ofrecen audio y velocidad reducida. Prioridad de desarrollo: toma 3, Antes de regresar; comparar cuántos intentos reales faltan. Revisar también las repeticiones de la toma 2. Las tomas 5/6 se conservan como comprobación de cambios fijados, sin ajustar reglas con ellas. Sin cambios del seguidor ni publicación automática.
