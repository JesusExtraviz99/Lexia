# Cierre de la revisión humana de MLS dev

06/11/2026 · Nueve casos escuchados y guardados por el usuario. Identidad de los nueve audios cotejada con los FLAC originales. Sin segunda escucha humana independiente. Anotaciones originales conservadas.

## Resultado de las comprobaciones

| Caso | Resultado comunicado por el usuario |
|---|---|
| 3678_1378_000014 | La referencia omite presentación y capítulos que sí se oyen. No atribuir esas frases añadidas a invención del ASR. |
| 11670_10604_000122 | La referencia omite cierre/crédito que sí se oye. |
| 10367_10282_000017 | La referencia tiene texto ausente; el usuario aporta cierre de capítulo audible. |
| 133_1378_000084 | Referencia diferente al audio; el usuario transcribe «fin de capítulo catorce». |
| 6671_9310_000053 | Referencia coincide; repetición extensa de Crisper confirmada como error. El sonido inicial parecido a «lo» puede ser real. |
| 13257_11991_000034 | Referencia coincide; usuario confirma salida inventada de Parakeet. |
| 13257_11991_000061 | Referencia valorada como correcta, palabra final casi cortada; las notas señalan palabras de Crisper inexistentes. Casilla de motores vacía en la anotación: se conserva tal cual. |
| 13257_11991_000037 | Referencia valorada como correcta; transcripción humana y observación de pronunciación. No hay diagnóstico específico de causa del desfase temporal. |
| 6671_9310_000073 | Referencia valorada como correcta; se oye «grim» parcial al final. Completar la palabra es una explicación posible de la salida, no una causa demostrada del tiempo fuera de rango. |

## Consecuencias para las métricas

- Cuatro de estos nueve casos presentan referencias incompletas o diferentes según la escucha del usuario. La selección buscaba errores extremos/alertas: no significa que el 44 % de MLS esté mal.
- WER/CER oficiales permanecen calculados con las referencias originales y todos los clips. No se eliminan casos ni se sustituyen referencias después de observar salidas.
- Esos errores de referencia pueden penalizar palabras realmente audibles. Por tanto, un WER alto o una inserción respecto al texto de referencia no basta para declarar alucinación.
- Conservar las transcripciones humanas como capa de revisión. Una evaluación secundaria con referencias revisadas requeriría fijar criterios, alcance y versión, y mostrar resultados oficiales y secundarios por separado. No se ha ejecutado esa evaluación.
- Los errores confirmados de Crisper y Parakeet se conservan como casos de diagnóstico. No permiten descartar o elegir un modelo por sí solos; Parakeet sigue teniendo el menor WER global oficial de este lote.
- Comentarios sobre edad/acento son percepciones del revisor; no se convierten en edad/nacionalidad verificadas ni prueban la causa de un fallo. Las marcas temporales de Crisper siguen siendo aproximaciones del ASR; la escucha no acredita su precisión palabra por palabra.

Las nueve anotaciones y sus textos literales están en escucha_humana/. No cambian el entrenamiento, pesos, configuración ni resultados ASR. No se ejecutó reconocimiento nuevo ni se publicó en GitHub.
