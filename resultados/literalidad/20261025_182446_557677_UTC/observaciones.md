# Observaciones del lote para revisión compartida

25/10/2026. Revisión técnica de textos y referencias previas, sin nueva escucha humana independiente ni anotación exhaustiva. Los hallazgos orientan la revisión del lector; no son una clasificación automática de todos los eventos. Salidas originales intactas.

## Lectura normal del primer cuento: texto añadido tras el cuento

La referencia del lector confirma que no dice nada antes ni después del cuento y estima el final del habla hacia 23–24 s, sin límites temporales acústicos precisos. El candidato largo coloca texto adicional en el bloque nativo 26–40 s, después de reconocer el cuento. La salida incluye «Vas por el lado de las chicas…» y repeticiones de «las mariposas». Es incompatible con esa confirmación del lector; no atribuirlo causalmente al ruido o a una opción concreta sin un contraste controlado. El recorte sin habla del piloto corto había dado vacío: el comportamiento en contexto largo es diferente, con múltiples factores cambiados.

**Candidato completo:** Una mañana, Ana, salió al jardín de su casa. Cerca de un árbol, encontró una mariposa azul. La mariposa voló despacio y se posó sobre una flor. Ana llamó a su hermano para que pudiera verla. Los dos se quedaron en silencio, mirando sus alas. Después volvieron a casa y dibujaron la mariposa en un cuaderno. Vas por el lado de las chicas, la mariposa, el cuaderno y la mariposa y los chicas, las mariposas, las mariposas, las mariposas, las mariposas.

Referencia: datos/referencias/lectura_normal.json, SHA256 a896d8d5320a90cd1338bb97a962ab7bbd84d3efebfad5cc9729f09ba7152646. La huella de su WAV coincide con esta entrada del lote.

## Lectura normal del segundo cuento: contraste en sentido contrario

El lector había confirmado una sola lectura del cuento. El actual añade «¡Suscríbete!» después de «estantería»; el candidato termina en «estantería». La diferencia muestra por qué no basta con buscar un ganador en una sola muestra. No es prueba de ausencia general de inserciones en el candidato.

**Actual:**  Una tarde, Lucía paseaba por el parque con su abuelo.  Junto a una fuente descubrió un pequeño barco rojo.  El barco flotaba despacio entre las hojas.  Lucía buscó una rama para acercarlo a la orilla.  Su abuelo la ayudó y juntos sacaron el barco del agua.  Después regresaron a casa y lo colocaron sobre una estantería.  ¡Suscríbete!

**Literal:** Una tarde, Lucía paseaba por el parque con su abuelo. Junto a una fuente descubrió un pequeño barco rojo. El barco flotaba despacio entre las hojas. Lucía buscó una rama para acercarlo a la orilla. Su abuelo la ayudó y juntos sacaron el barco del agua. Después regresaron a casa y lo colocaron sobre una estantería.

## Desviaciones, sustitución y omisión comunicadas por el lector

En las desviaciones del primer cuento, el candidato escribe «Ana Ana», conserva «mar- mariposa» y no escribe «despacio». Mantiene «cinesio», por lo que no soluciona todas las palabras dudosas. Es una comparación con las confirmaciones previas de ese audio, no una tasa de detección.

**Literal, desviaciones:** Una mañana, Ana Ana salió al jardín de su casa, cerca de un árbol encontró una mariposa azul. La mariposa voló y se posó sobre una flor. Ana llamó a su hermano para que pudiera verla. Los dos se quedaron en cinesio mirando sus alas. Después volvieron a casa y dibujaron la mar- mariposa en un cuaderno.

En la sustitución del segundo cuento escribe «barco azul»; en la omisión no aparece la palabra «abuelo». Esto no significa que anote explícitamente un error de lectura. En la segunda salida deforma el contexto como «Consu» y «Suu», que requieren escucha; no dar por fiel todo el tramo solo porque no restaura la palabra omitida.

**Literal, sustitución:** Una tarde, Lucía paseaba por el parque con su abuelo. Junto a una fuente descubrió un pequeño barco azul. El barco flotaba despacio entre las hojas. Lucía buscó una rama para acercarlo a la orilla. Su abuelo la ayudó y juntos sacaron el barco del agua. Después regresaron a casa y lo colocaron sobre una estantería.

**Literal, omisión:** Una tarde, Lucía paseaba por el parque Consu, junto a una fuente descubrió un pequeño barco rojo. El barco flotaba despacio entre las hojas. Lucía buscó una rama para acercarlo a la orilla. Suu la ayudó y juntos sacaron el barco del agua. Después regresaron a casa y lo colocaron sobre una estantería.

## Muchas trabadas y lectura lenta

La salida literal del audio con muchas trabadas coincide exactamente con el texto del ensayo completo del 23/10: True. Se mantiene la corrección puntual ya registrada por el lector: «regres- re- regresaron» frente a «regres- regresaron». Un episodio puede estar presente y perder un intento interior. La valoración cualitativa anterior no es una revisión independiente nueva ni un inventario de todos los eventos.

En la lectura lenta del primer cuento, el candidato escribe «desváceo» y termina «un jugador no. Ven.» en vez de conservar claramente «cuaderno». La referencia anterior del lector confirma que pronuncia cuaderno y después queda silencio con un ruido breve. No asumir que la mejora en las trabadas se extiende a todas las velocidades.

**Literal, lenta:** Una mañana Ana salió al jardín de su casa. Cerca de un árbol encontró una mariposa azul. La mariposa voló desváceo y se posó sobre una flor. Ana llamó a su hermano para que pudiera verla. Los dos se quedaron en silencio, mirando sus alas. Después volvieron a casa y dibujaron la mariposa en un jugador no. Ven.

## Decisión y revisión siguiente

Mantener el motor como candidato separado. Revisar primero los finales de las dos lecturas normales, después lenta y desviaciones; las restantes transcripciones están completas en resumen.md y en el visor. Conservar textos añadidos y omisiones para futuras métricas de precisión, recuperación e intentos. No cambiar parámetros a mitad de este lote ni filtrar sus salidas para mejorar retrospectivamente las cifras. Las etiquetas entre corchetes, como [throatclearing], son propuestas del modelo sobre eventos no verbales y también requieren escucha; no son palabras necesariamente pronunciadas.

Queda preparado un punto de comparación para posteriores ensayos de tratamiento de silencio/ruido o de otros entornos, usando los mismos audios y referencias. Este lote de una pasada no decide la configuración óptima ni aporta una evaluación final independiente.

## Procedencia

Confirmaciones de contenido/ambiente: catalogo_snapshot.json y los archivos de referencia enlazados en sus registros. Corrección de la secuencia de regresaron: datos/anotaciones/lectura_02_literal_completa_revision.json. Las 693 fuentes de resultados/anotaciones anteriores se comprueban en integridad.json.

Manifiesto SHA256: 53074ee81c5d1ff1d1d6ecd1c3597bed33506d7ff3e7ceac0388b86d76b41051
Actual SHA256: d46203a64e2506e385c9f0399fd9fe5e45e70bf7e05765d478da0435759d3e30
Candidato SHA256: 305f1de0527ef4847ea3e469e6f15c1deb73f6dc744a042f06b3dafb0e3e616b

## Selección posterior del lector

**Revisión del lector y contraste documental.** El usuario señala errores del candidato literal en 1, 4, 5, 6, 11 y 17 y solicita aprovechar las referencias anteriores. La revisión humana conserva esa aclaración sin atribuirle un desglose que no ha escrito. auditoria_errores_lector.md/.json cruza las mismas huellas con transcripciones y anclas humanas, sin inferencias nuevas: aparecen continuaciones añadidas en los últimos bloques de 1, 4, 5, 6 y 11; 4 sustituye despacio/cuaderno, 5 omite a y 17 representa con su/Su como Consu/Suu sin restaurar las omisiones deliberadas de abuelo. El soporte lexical humano es completo para 1,4,5,6 y descriptivo para 11,17; Suu no prueba una prolongación real. La coincidencia en bloques finales no aísla la causa ni justifica borrar relecturas reales. El modelo actual también inventa texto en algunos casos. Sin tasa global o cambios del motor; se mantienen informe y diarios en la misma E059.
