# Referencias humanas del banco inicial

Estado: las cinco transcripciones literales están validadas por el usuario tras escucha. Todos los tiempos humanos por palabra siguen pendientes.

catalogo.json identifica los cinco WAV mediante rutas relativas y SHA-256, y conserva formato y duración. Todos pertenecen al mismo adulto y al mismo cuento, y ya se han usado para tomar decisiones de desarrollo. Las rondas del comparador no añaden lecturas independientes. Se necesitarán audios nuevos para una comprobación final reservada.

## Primer paso: revisar la lectura normal

Audio: datos/audio/lectura_20261014_081816_009646.wav, 40 s.

1. Escuchar el archivo completo, incluidas las partes anterior y posterior al cuento.
2. Escribir las palabras realmente pronunciadas. Conservar repeticiones, intentos incompletos, autocorrecciones y comentarios. No copiar el cuento como si fuera lo que ocurrió.
3. Si coincide con el cuento, confirmarlo explícitamente después de la escucha. Indicar cualquier sonido o palabra dudosa.
4. Indicar si antes o después hay voz humana o solo ambiente/silencio. El ruido ambiental no se escribe como palabras; se describe aparte.

No hace falta marcar segundos todavía. Primero acordamos una transcripción literal. El texto del cuento sirve para localizar palabras esperadas; las salidas ASR son material de comparación, no referencia humana.

lectura_normal.json contiene el texto confirmado por el usuario y las observaciones de ambiente. La revisión es del propio lector, no de un anotador independiente. La estimación de fin de lectura, alrededor de 23–24 s, no es un límite temporal preciso. Los tiempos por palabra permanecen sin anotar. Los demás casos no se consideran validados por esta confirmación. Las palabras inciertas o inaudibles se documentarán sin inventar contenido.

## Después

lectura_relectura.json conserva dos apariciones de Los dos se quedaron en silencio (una repetición adicional), vinculadas a índices 37–42 del cuento. El resto coincide con el texto según el usuario. Registra ausencia de habla desde aproximadamente 30 s, con ruido mínimo final; la limpieza del audio es una valoración del usuario. La elipsis del texto es editorial, no una medida de pausa.

lectura_lenta.json contiene el cuento tras confirmación explícita del usuario de que coincide íntegramente, sin otras diferencias. El usuario confirma cuaderno claramente pronunciado y que la frase del vídeo no está en el audio, sin voz de fondo. Se registra silencio con ruido de silla desde aproximadamente 78 s; no se infiere causalidad del ruido ni tiempos por palabra.

lectura_pausa.json contiene el cuento confirmado y una pausa entre flor (27) y Ana (28), sin límites medidos. El usuario indica ausencia de habla desde aproximadamente 31 s; una revisión anterior mencionaba pájaros al final. Se conserva esa diferencia de descripción sin asumir silencio acústico absoluto. El ruido al final del silencio tiene ubicación todavía ambigua y no recibe una marca temporal inventada.

lectura_desviaciones.json conserva Ana, Ana; la omisión de despacio; y mari… mariposa al final. El fragmento mari se identifica como intento incompleto seguido de autocorrección y deberá conservarse al evaluar disfluencias. No aplicar una normalización que lo borre ni interpretarlo como palabra completa sin declarar la regla.

Silencio se conserva como referencia lexical, según la escucha del usuario, con una observación separada de articulación poco clara. No se adjudica un error fonético. Los pájaros intermitentes y los ruidos de silla/mochila posteriores a aproximadamente 24 s se registran como ambiente, sin convertirlos en palabras ni atribuirles causalmente salidas ASR concretas.

Una vez revisado el texto, acordar las convenciones temporales (palabra actual, última completada, silencios e intentos) y comenzar a marcar intervalos por escucha. No tratar los tiempos del ASR ni un alineamiento automático como verdad humana sin revisión. La validez textual y la temporal se registran por separado.

Ya existe un [reproductor local](../../herramientas/anotador/LEEME.md) para la lectura normal: `python scripts/anotar.py`. Guarda el progreso en datos/anotaciones, separado de estas referencias. Se comienza por las nueve palabras de la primera frase. Cualquier borrador ASR y los límites aún no escuchados siguen pendientes. El programa no modifica automáticamente los tiempos humanos de referencia.

Extender las reglas a los demás casos antes de implementar puntuaciones de precisión. Conservar el audio original y las salidas antiguas. Las nuevas referencias y herramientas quedan locales hasta que el usuario las revise y autorice su publicación.
