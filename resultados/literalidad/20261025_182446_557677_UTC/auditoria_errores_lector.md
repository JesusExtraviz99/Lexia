# Contraste de los seis audios señalados por el lector

25/10/2026. El lector aclara que los errores señalados son del candidato literal y solicita aprovechar las comprobaciones anteriores. Este informe cruza esas referencias y sus huellas con las salidas completas guardadas. No se ejecuta reconocimiento nuevo ni se presenta esta revisión documental como una escucha humana independiente.

| Audio | Grabación | Hallazgo en el literal | Soporte disponible |
|---|---|---|---|
| 1 | Lectura normal - cuento 1 - 14-10-2026.wav | Añade una continuación ajena al audio, desde Vas por el lado de las chicas hasta las repeticiones de las mariposas. | referencia lexical humana completa y anotacion temporal |
| 4 | Lectura lenta - cuento 1 - 16-10-2026.wav | Sustituye despacio por desváceo, cuaderno por jugador no y añade Ven al final. | referencia lexical humana completa y anclas seleccionadas |
| 5 | Lectura con relectura (Los dos se quedaron en silencio) - cuento 1 - 16-10-2026.wav | Omite a en llamó a su hermano y añade Ven; las dos apariciones de Los dos se quedaron en silencio sí son reales. | referencia lexical humana completa y anclas seleccionadas |
| 6 | Lectura con relectura lejana (Los dos-alas) - cuento 1 - 21-10-2026.wav | Conserva la relectura real y luego añade ¿Y por qué no se puede ver el maravilla?. | referencia lexical humana completa y anclas seleccionadas |
| 11 | Lectura lenta - cuento 2 - lectura_02 - 23-10-2026.wav | Añade A la vez de hoy, la familia está en su casa, y el joven se lo lleva. tras estantería. | consigna y finalizacion confirmadas sin transcripcion literal exhaustiva |
| 17 | Lectura omisión abuelo - cuento 2 - lectura_02 - 23-10-2026.wav | Escribe Consu y Suu; no restaura abuelo. El problema es principalmente representación/segmentación, sin frase final inventada identificada. | dos omisiones confirmadas sin referencia fonetica completa |

## Patrón observado y alcance

En 1,4,5,6,11 hay texto añadido en el último bloque corto de continuación, aunque el soporte humano es más completo en 1,4,5,6. El 4 además sustituye palabras y el 5 omite a. El 17 es representación/segmentación; la omisión deliberada de abuelo no debe corregirse como si fuera un error del ASR.

Los añadidos aparecen en los últimos bloques de entrada: 1 → 26–40 s; 4 → 78–90 s; 5 y 6 → 52–60 s; 11 → 78–90 s. Los casos 1, 4, 5 y 6 tienen referencias lexicales completas confirmadas por el lector y anclas humanas; para 11 hay confirmación de lectura/consigna, pero no transcripción literal exhaustiva. No convertir estos bloques en tiempos precisos de errores. El final humano de cuaderno en 1 está en 22,36–22,94 s; cuaderno en 4, 75,14–77,34 s; alas de la relectura en 6, 32,17–32,73 s.

Esto justifica un futuro contraste controlado de tratamiento de ausencia de habla y continuación larga. Todavía no aísla el efecto del ruido, contexto generado, cierre temprano o límites de bloques. Mantener esta ejecución intacta y no suprimir repeticiones indiscriminadamente: algunas son precisamente los eventos que queremos conservar.

## Audio 1 · Lectura normal - cuento 1 - 14-10-2026.wav

Añade una continuación ajena al audio, desde Vas por el lado de las chicas hasta las repeticiones de las mariposas.

**Actual completo:**  Una mañana Ana salió al jardín de su casa. Cerca de un árbol encontró una mariposa azul.  La mariposa voló despacio y se posó sobre una flor. Ana llamó a su hermano para que pudiera  verla. Los dos se quedaron en silencio mirando sus alas. Después volvieron a casa y dibujaron  la mariposa en un cuaderno.

**Literal completo:** Una mañana, Ana, salió al jardín de su casa. Cerca de un árbol, encontró una mariposa azul. La mariposa voló despacio y se posó sobre una flor. Ana llamó a su hermano para que pudiera verla. Los dos se quedaron en silencio, mirando sus alas. Después volvieron a casa y dibujaron la mariposa en un cuaderno. Vas por el lado de las chicas, la mariposa, el cuaderno y la mariposa y los chicas, las mariposas, las mariposas, las mariposas, las mariposas.

**Referencia lexical confirmada por el lector:** Una mañana, Ana salió al jardín de su casa. Cerca de un árbol encontró una mariposa azul. La mariposa voló despacio y se posó sobre una flor. Ana llamó a su hermano para que pudiera verla. Los dos se quedaron en silencio, mirando sus alas. Después volvieron a casa y dibujaron la mariposa en un cuaderno.

- insercion texto final: «Vas por el lado de las chicas, la mariposa, el cuaderno y la mariposa y los chicas, las mariposas, las mariposas, las mariposas, las mariposas.». Referencia/alcance: Sin palabras después del cuento; el lector confirmó que no hay habla adicional. Bloque de entrada [26, 40]. 

La salida actual del lote coincide lexicalmente con la referencia normal, sin ese añadido.

Fuentes: datos/referencias/lectura_normal.json, datos/anotaciones/lectura_normal.json. Las huellas y anclas exactas están en auditoria_errores_lector.json.

## Audio 4 · Lectura lenta - cuento 1 - 16-10-2026.wav

Sustituye despacio por desváceo, cuaderno por jugador no y añade Ven al final.

**Actual completo:**  Una mañana Ana salió al jardín de su casa, cerca de un árbol encontró una mariposa azul.  La mariposa voló despacio y se posó sobre una flor.  Ana llamó a su hermano para que pudiera verla.  Los dos se quedaron en silencio, mirando sus alas.  Después volvieron a casa y dibujaron la mariposa en un cuaderno.

**Literal completo:** Una mañana Ana salió al jardín de su casa. Cerca de un árbol encontró una mariposa azul. La mariposa voló desváceo y se posó sobre una flor. Ana llamó a su hermano para que pudiera verla. Los dos se quedaron en silencio, mirando sus alas. Después volvieron a casa y dibujaron la mariposa en un jugador no. Ven.

**Referencia lexical confirmada por el lector:** Una mañana, Ana salió al jardín de su casa. Cerca de un árbol encontró una mariposa azul. La mariposa voló despacio y se posó sobre una flor. Ana llamó a su hermano para que pudiera verla. Los dos se quedaron en silencio, mirando sus alas. Después volvieron a casa y dibujaron la mariposa en un cuaderno.

- sustitucion: «desváceo». Referencia/alcance: despacio Bloque de entrada [26, 56]. 
- sustitucion y segmentacion: «jugador no». Referencia/alcance: cuaderno Bloque de entrada [52, 82]. 
- insercion texto final: «Ven.». Referencia/alcance: Sin habla tras el cuento; silencio y ruido leve de silla según el lector. Bloque de entrada [78, 90]. 

El actual completo del lote conserva despacio y cuaderno. En el experimento antiguo de ventanas aparecía jugaderno: la corrección humana de cuaderno evita tomar ese ASR histórico como verdad.

Fuentes: datos/referencias/lectura_lenta.json, datos/anotaciones/lectura_lenta_fragmentos.json. Las huellas y anclas exactas están en auditoria_errores_lector.json.

## Audio 5 · Lectura con relectura (Los dos se quedaron en silencio) - cuento 1 - 16-10-2026.wav

Omite a en llamó a su hermano y añade Ven; las dos apariciones de Los dos se quedaron en silencio sí son reales.

**Actual completo:**  Una mañana Ana salió al jardín de su casa.  Cerca de un árbol encontró una mariposa azul.  La mariposa voló despacio y se posó sobre una flor.  Ana llamó a su hermano para que pudiera verla.  Los dos se quedaron en silencio.  Los dos se quedaron en silencio mirando sus alas.  Después volvieron a casa y dibujaron la mariposa en un cuaderno.  Bueno, nos vemos en el próximo vídeo, ¡hasta la próxima!

**Literal completo:** Una mañana Ana salió al jardín de su casa. Cerca de un árbol encontró una mariposa azul. La mariposa voló despacio y se posó sobre una flor. Ana llamó su hermano para que pudiera verla. Los dos se quedaron en silencio. Los dos se quedaron en silencio mirando sus alas. Después volvieron a casa y dibujaron la mariposa en un cuaderno. Ven.

**Referencia lexical confirmada por el lector:** Una mañana, Ana salió al jardín de su casa. Cerca de un árbol encontró una mariposa azul. La mariposa voló despacio y se posó sobre una flor. Ana llamó a su hermano para que pudiera verla. Los dos se quedaron en silencio… Los dos se quedaron en silencio, mirando sus alas. Después volvieron a casa y dibujaron la mariposa en un cuaderno.

- omision lexical: «llamó su hermano». Referencia/alcance: llamó a su hermano Bloque de entrada [0, 30]. 
- insercion texto final: «Ven.». Referencia/alcance: Sin palabras adicionales al finalizar el cuento. Bloque de entrada [52, 60]. 

El actual mantiene llamó a su hermano, pero añade Bueno, nos vemos en el próximo vídeo, ¡hasta la próxima!: también falla. No borrar la relectura verdadera para arreglar la invención.

Fuentes: datos/referencias/lectura_relectura.json, datos/anotaciones/lectura_relectura_fragmentos.json. Las huellas y anclas exactas están en auditoria_errores_lector.json.

## Audio 6 · Lectura con relectura lejana (Los dos-alas) - cuento 1 - 21-10-2026.wav

Conserva la relectura real y luego añade ¿Y por qué no se puede ver el maravilla?.

**Actual completo:**  Una mañana Ana salió al jardín de su casa.  Cerca de un árbol encontró una mariposa azul.  La mariposa voló despacio y se posó sobre una flor.  Ana llamó a su hermano para que pudiera verla.  Los dos se quedaron en silencio mirando sus alas.  Después volvieron a casa y dibujaron la mariposa en un cuaderno.  Los dos se quedaron en silencio mirando sus alas.  y

**Literal completo:** Una mañana Ana salió al jardín de su casa. Cerca de un árbol encontró una mariposa azul. La mariposa voló despacio y se posó sobre una flor. Ana llamó a su hermano para que pudiera verla. Los dos se quedaron en silencio mirando sus alas. Después volvieron a casa y dibujaron la mariposa en un cuaderno. Los dos se quedaron en silencio mirando sus alas. ¿Y por qué no se puede ver el maravilla?

**Referencia lexical confirmada por el lector:** Una mañana, Ana salió al jardín de su casa. Cerca de un árbol encontró una mariposa azul. La mariposa voló despacio y se posó sobre una flor. Ana llamó a su hermano para que pudiera verla. Los dos se quedaron en silencio, mirando sus alas. Después volvieron a casa y dibujaron la mariposa en un cuaderno. Los dos se quedaron en silencio, mirando sus alas.

- insercion texto final: «¿Y por qué no se puede ver el maravilla?». Referencia/alcance: La última frase pronunciada es la relectura Los dos se quedaron en silencio mirando sus alas. Bloque de entrada [52, 60]. 

El actual conserva el contenido esperado pero añade una y final; tampoco es una salida perfecta.

Fuentes: datos/referencias/lectura_relectura_lejana.json, datos/anotaciones/lectura_relectura_lejana_fragmentos.json. Las huellas y anclas exactas están en auditoria_errores_lector.json.

## Audio 11 · Lectura lenta - cuento 2 - lectura_02 - 23-10-2026.wav

Añade A la vez de hoy, la familia está en su casa, y el joven se lo lleva. tras estantería.

**Actual completo:**  Una tarde Lucía paseaba por el parque con su abuelo.  Junto a una fuente descubrió un pequeño barco rojo.  El barco flotaba despacio entre las hojas.  Lucia buscó una rama para acercarlo a la orilla.  Su abuelo la ayudó y junto sacaron el barco del agua.  Después regresaron a casa y lo colocaron sobre una estantería.

**Literal completo:** Una tarde, Lucía paseaba por el parque con su abuelo. Junto a una fuente descubrió un pequeño barco rojo. El barco flotaba despacio entre las hojas. Lucía buscó una rama para acercarlo a la orilla. Su abuelo la ayudó y juntos sacaron el barco del agua. Después regresaron a casa y lo colocaron sobre una estantería. A la vez de hoy, la familia está en su casa, y el joven se lo lleva.

- anadido ajeno al texto y senalado por lector: «A la vez de hoy, la familia está en su casa, y el joven se lo lleva.». Referencia/alcance: El cuento comunicado termina en sobre una estantería; no contiene esta frase. Bloque de entrada [78, 90]. No hay referencia literal exhaustiva ni final humano temporizado para este WAV. Es texto añadido respecto al cuento y a la descripción, coherente con la señal de error del lector; no se afirma que todo el bloque sea silencio ni se valida cada palabra del resto.

El actual no añade esa frase, aunque escribe junto en el lugar de juntos respecto al cuento. Falta referencia literal completa para adjudicar todas sus diferencias.

Fuentes: pruebas/22_lote_segundo_cuento.md. Las huellas y anclas exactas están en auditoria_errores_lector.json.

## Audio 17 · Lectura omisión abuelo - cuento 2 - lectura_02 - 23-10-2026.wav

Escribe Consu y Suu; no restaura abuelo. El problema es principalmente representación/segmentación, sin frase final inventada identificada.

**Actual completo:**  Una tarde, Lucía paseaba por el parque Konsu. Junto a una fuente descubrió un pequeño barco rojo.  El barco flotaba despacio entre las hojas. Lucía buscó una rama para acercarlo a la orilla.  Su, la ayudó y juntos sacaron el barco del agua. Después regresaron a casa y lo colocaron sobre  una estantería.

**Literal completo:** Una tarde, Lucía paseaba por el parque Consu, junto a una fuente descubrió un pequeño barco rojo. El barco flotaba despacio entre las hojas. Lucía buscó una rama para acercarlo a la orilla. Suu la ayudó y juntos sacaron el barco del agua. Después regresaron a casa y lo colocaron sobre una estantería.

- fusion de palabras: «Consu». Referencia/alcance: con su, con omisión de abuelo confirmada en este punto Bloque de entrada [0, 30]. Compatible con unir con su; no demuestra que se invente un nombre propio.
- representacion grafica por comprobar foneticamente: «Suu la ayudó». Referencia/alcance: Su la ayudó, con omisión de abuelo confirmada Bloque de entrada [0, 30]. Sin anotación fonética no se resuelve si la u repetida representa una prolongación real o una grafía defectuosa; no contar como una repetición nueva.

El actual también escribe Konsu y Su, la ayudó. La omisión de abuelo es del lector, no un fallo que el ASR deba corregir añadiendo la palabra.

Fuentes: pruebas/22_lote_segundo_cuento.md. Las huellas y anclas exactas están en auditoria_errores_lector.json.

## Límites

- Los números de bloques son intervalos de entrada al modelo, no instantes humanos de habla ni marcas validadas del texto inventado.
- El patrón en bloques finales no prueba por sí solo causa por ruido, contexto generado o una opción concreta; no se modifican reglas ni se ejecuta una prueba causal.
- Las diferencias lexicales se agrupan con SequenceMatcher tras NFC, minúsculas y retirada de puntuación, conservando tildes; son una ayuda visual, no WER ni anotación de disfluencias.
- No se adjudican palabras o tiempos humanos inexistentes para 11 y 17, ni se considera correcto el resto de audios por no estar señalado.
- Las relecturas confirmadas se conservan como eventos reales; los ASR actual e histórico tampoco son referencias perfectas.

Para revisar sin pedir al lector que enumere cada fallo, el visor conserva los 17 WAV y ambas salidas. Priorizar los finales indicados y las sustituciones de 4; no reemplazar sus textos por el cuento correcto ni restaurar abuelo en 17.

Fuentes ASR e input permanecen idénticas a las verificadas en integridad.json. Corrección del registro de revisión: el motor señalado ya es candidato; el detalle de este informe lo aporta el asistente y no se atribuye al lector como si lo hubiera escrito.
