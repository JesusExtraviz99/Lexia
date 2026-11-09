# Revisión de la primera prueba paralela · 04/11/2026

Cinco motores, 10 audios idénticos de MLS dev, 142.08 s y 372 palabras de referencia. Los 50 resultados completos se han recalculado desde las transcripciones guardadas; coinciden WER/CER, alineamientos y conteos. Las diez huellas se han cotejado también con los audios locales si se indica en verificacion.json. Sin inferencias nuevas ni escucha humana independiente.

| Motor | Dispositivo | WER % | CER % | ASR total s | RTF | RAM RSS máx. observada MiB | VRAM PID máx. observada MiB |
|---|---|---:|---:|---:|---:|---:|---:|
| vosk | CPU | 13.17 | 3.92 | 12.71 | 0.0895 | 200.5 | no usa GPU |
| xlsr | GPU 0 | 11.29 | 2.44 | 1.17 | 0.0082 | 4116.3 | 3110 |
| parakeet | GPU 1 | 6.72 | 1.73 | 2.50 | 0.0176 | 4640.6 | 4024 |
| whisper | GPU 2 | 8.60 | 2.14 | 5.38 | 0.0379 | 3212.1 | 1970 |
| crisper | GPU 3 | 10.75 | 2.65 | 31.97 | 0.2250 | 6055.6 | 3928 |

ASR total es la suma de las diez llamadas con modelo ya cargado y calentado. No incluye carga, calentamiento, E/S ni escritura de informes. RAM/VRAM observadas abarcan la sesión, incluida carga y calentamiento. CPU/GPU y diferentes decodificadores/backends no son comparaciones de arquitectura en igualdad de condiciones.

| Motor | Carga/importación s | Calentamiento s | Sesión instrumentada s | Muestras RAM / GPU | Audios con alguna muestra GPU |
|---|---:|---:|---:|---:|---:|
| vosk | 0.44 | 1.59 | 15.13 | 60 / 0 | 0/10 |
| xlsr | 16.86 | 15.92 | 35.83 | 130 / 33 | 2/10 |
| parakeet | 17.66 | 15.67 | 38.45 | 126 / 33 | 5/10 |
| whisper | 2.73 | 5.58 | 14.91 | 55 / 14 | 6/10 |
| crisper | 19.93 | 20.97 | 74.85 | 273 / 69 | 10/10 |

## Interpretación y límites

- Circuito técnico correcto en esta cohorte: diez resultados por motor, sin fallos ni hipótesis vacías; misma entrada y referencias, firmas coherentes y muestras JSONL coincidentes con el informe final. No hubo otros procesos de cómputo detectados en las GPU seleccionadas durante las muestras.
- Parakeet tiene el menor WER observado (25 ediciones/372 palabras), Faster-Whisper 32, Crisper 40, XLSR 42 y Vosk 49. Solo diez clips; no seleccionar ganador ni extrapolar a niños, disfluencias u otros datasets.
- XLSR es el más rápido en las llamadas ya calentadas. La primera llamada/carga es mucho más larga; la prueba no aísla inicialización, compilación/cachés o interferencia como causas.
- Vosk necesita mucha menos RAM observada y funciona en CPU. No equivale a haber validado una tablet. Los otros motores usan RTX 3060 de 12 GB.
- GPU muestreada aproximadamente cada segundo: algunos audios rápidos no tienen ninguna muestra individual. No significa GPU inactiva. Los picos del allocator Torch están guardados por audio; no equivalen al pico completo de VRAM. Para potencia/uso, conservar agregados de sesión y medir un bloque sostenido en la evaluación de rendimiento.
- La energía estimada de sesión incluye carga, calentamiento e intervalos muestreados, sin reposo descontado: no dividirla para afirmar energía neta por audio ni compararla como consumo de tablet.
- Ejecución concurrente: hay CPU/RAM/disco compartidos y el solapamiento cambia al terminar motores. Los tiempos son observaciones de esta ejecución, no un benchmark aislado.
- Crisper: el backend instalado carga AutoModelForSpeechSeq2Seq/WhisperForConditionalGeneration y el log informa encoder_blank_head.weight/bias como UNEXPECTED. Se preserva el aviso; el paquete no consulta esa cabeza en su ruta Transformers. También hay avisos de generación/deprecación. No se ha demostrado que causen los errores textuales ni se han cambiado dependencias/decodificación. Revisar esa configuración antes de interpretar métricas de alineación fina.
- Whisper, Crisper y Vosk devuelven marcas de palabra con comprobación básica de rango; no hay anclas humanas para acreditar su precisión. Parakeet no alcanza el límite configurado de tokens en estos clips; eso no certifica ausencia de omisiones en general.
- Se conservan acentos/ortografía del dataset en la métrica primaria. Referencias como «fué», «despues», «ignorais» o construcciones antiguas pueden penalizar salidas con otra ortografía. Hay errores de nombres propios y segmentación en varios motores. No se corrigen referencias tras ver resultados ni se afirma por texto qué se pronunció realmente.
- Siguiente paso: revisar conjuntamente transcripciones y aceptar protocolo/cobertura; después desarrollo más amplio con configuración fijada, manteniendo test reservado. Rendimiento aislado en selección fija antes de conclusiones de coste.

## Transcripciones para comprobación

### 133_1378_000042 · 19.96 s

**Referencia:** advertid señor caballero que la condición de nuestra batalla es que el vencido como otra vez he dicho ha de quedar a discreción del vencedor ya la sé respondió don quijote con tal que lo que se le impusiere y mandare al vencido han de ser cosas que no salgan de los límites de la caballería

**vosk · WER 7.14%:** advertid señor caballero que la condición de nuestra batalla es que el vencido como otra vez he dicho ha de quedar a discreción del vencedor ya lo sé respondió don quijote con tal que lo que se le pusiere y mandaré al vencido han de ser cosas que nos salgan de los límites de la caballería

**xlsr · WER 5.36%:** advertid señor caballero que la condición de nuestra batalla es que el vencido como otra vez he dicho ha de quedar a discreción del vencedorya la sé respondió don quijote con tal que lo que se le impusiere y mandare al vencido han de ser cosas que no sagan de los límites de la caballería

**parakeet · WER 0.00%:** Advertid, señor caballero, que la condición de nuestra batalla es que el vencido, como otra vez he dicho, ha de quedar a discreción del vencedor. Ya la sé, respondió don Quijote, con tal que lo que se le impusiere y mandare al vencido han de ser cosas que no salgan de los límites de la caballería.

**whisper · WER 0.00%:** Advertid, señor caballero, que la condición de nuestra batalla es que el vencido, como otra vez he dicho, ha de quedar a discreción del vencedor. Ya la sé, respondió don Quijote, con tal que lo que se le impusiere y mandare al vencido han de ser cosas que no salgan de los límites de la caballería.

**crisper · WER 0.00%:** Advertid, señor caballero, que la condición de nuestra batalla es que el vencido, como otra vez he dicho, ha de quedar a discreción del vencedor. Ya la sé, respondió don Quijote, con tal que lo que se le impusiere y mandare al vencido, han de ser cosas que no salgan de los límites de la caballería.

### 1075_567_000050 · 11.10 s

**Referencia:** sino porque entonces los que en ella vivían ignoraban estas dos palabras de tuyo y mío eran en aquella santa edad todas las cosas comunes

**vosk · WER 8.00%:** sino porque entonces los quien ella vivían ignoraban estas dos palabras de tuyo y mío eran en aquella santa edad todas las cosas comunes

**xlsr · WER 8.00%:** sino porque entonces los que en ella vivían ignoraban estas dos palabras de tu yo y mío eran en aquella santa edad todas las cosas comunes

**parakeet · WER 0.00%:** sino porque entonces los que en ella vivían ignoraban estas dos palabras de tuyo y mío. Eran en aquella santa edad todas las cosas comunes.

**whisper · WER 8.00%:** sino porque entonces los que en ella vivían ignoraban estas dos palabras de tuyo y mío, eran en aquella santidad todas las cosas comunes.

**crisper · WER 8.00%:** Sino porque entonces los que en ella vivían ignoraban estas dos palabras de tuyo y mío eran en aquella santidad todas las cosas comunes.

### 6223_5079_000063 · 15.04 s

**Referencia:** efectivamente dijo otro nos traes a conocer a una dama y apenas si con mucha dificultad se ven los dedos de la mano y con todo hace un frío que no parece sino que estamos en la siberia añadió un tercero arrebujándose en el capote

**vosk · WER 17.78%:** efectivamente dijo otro nos traes a conocer a una dama y apenas y con mucha dificultad de menos de dos de la mano y contó hace un frío que no parece sino que estamos en la siberia añadió un tercero regocijándose en el capote

**xlsr · WER 4.44%:** efectivamente dijo otro nos traes a conocer a una dama y apenas si con mucha dificultad se ven los dedos de la manoy con todo hace un frío que no parece sino que estamos en la siberia añadió un tercero arrebujándose en el capote

**parakeet · WER 2.22%:** Efectivamente, dijo otro, nos traes a conocer a una dama y apenas y con mucha dificultad se ven los dedos de la mano. Y con todo hace un frío que no parece sino que estamos en la Siberia, añadió un tercero arrebujándose en el capote.

**whisper · WER 4.44%:** Efectivamente, dijo otro, nos traes a conocer a una dama y apenas y con mucha dificultad se ven los dedos de la mano. Y con todo hace un frío que no parece sino que estamos en la Siberia, añadió un tercero arregujándose en el capote.

**crisper · WER 6.67%:** Efectivamente, dijo otro, nos trae a conocer a una dama y, apenas y con mucha dificultad, se ven los dedos de la mano. Y con todo, hace un frío que no parece sino que estamos en la Siberia, añadió un tercero arregujándose en el capote.

### 3719_1378_000015 · 11.59 s

**Referencia:** y la cara quitadas las narices era la misma de tomé cecial como yo se la he visto muchas veces en mi pueblo y pared en medio de mi misma casa y el tono de la habla era todo uno

**vosk · WER 7.50%:** y la cara quitadas las narices era la misma de tome social como yo se la he visto muchas veces en mi pueblo y pared en medio de mí misma casa y el tono de la habla era todo uno

**xlsr · WER 7.50%:** en la cara quitadas las narices era la misma de tome cecial como jo se la he visto muchas veces en mi pueblo y pared en medio de mi misma casa y el tono de la habla era todo uno

**parakeet · WER 2.50%:** Y la cara, quitadas las narices, era la misma de Tomé Secial, como yo se la he visto muchas veces en mi pueblo y pared en medio de mi misma casa, y el tono de la habla era todo uno.

**whisper · WER 7.50%:** En la cara quitadas las narices era la misma de Tomé Cecial, como yo se la he visto muchas veces en mi pueblo y paré de en medio de mi misma casa, y el tono de la habla era todo uno.

**crisper · WER 12.50%:** En la cara, quitadas las narices, era la misma de tomes escial. Como yo se la he visto muchas veces en mi pueblo y paré de en medio de mi misma casa, y el tono de la habla era todo uno.

### 133_1378_000052 · 15.59 s

**Referencia:** todo lo confieso juzgo y siento como vos lo creéis juzgáis y sentís respondió el derrengado caballero dejadme levantar os ruego si es que lo permite el golpe de mi caída que asaz maltrecho me tiene

**vosk · WER 2.78%:** todo lo confieso juzgo y siento como os lo creéis juzgáis y sentís respondió el derrengado caballero dejadme levantar os ruego si es que lo permite el golpe de mi caída que asaz maltrecho me tiene

**xlsr · WER 22.22%:** todo lo confieso juzgo y siento como vozlo creéis juzgáis y sentir respondió el derrengado caballero dejadme levantar os luego si es que lo permite el golpe de micaída queazad maltrecho me tiene

**parakeet · WER 2.78%:** Todo lo confieso, juzgo y siento como vos lo creéis, juzgáis y sentís, respondió el derrengado caballero. Dejadme levantar, os ruego, si es que lo permite, el golpe de mi caída, que asad maltrecho me tiene.

**whisper · WER 2.78%:** Todo lo confieso, juzgo y siento como vos lo creéis, juzgáis y sentís, respondió el derrengado caballero. Dejadme levantar, os ruego, si es que lo permite el golpe de mi caída, que Asad maltrecho me tiene.

**crisper · WER 5.56%:** Todo lo confieso, juzgo y siento como vos lo creéis, juzgáis y sentís, respondió el derringado caballero. Dejadme levantar os ruego, si es que lo permite el golpe de mi caída, que Asad maltrecho me tiene.

### 10367_10282_000004 · 19.12 s

**Referencia:** mas él herido fué por nuestras rebeliones molido por nuestros pecados el castigo de nuestra paz sobre él y por su llaga fuimos nosotros curados todos nosotros nos descarriamos como ovejas cada cual se apartó por su camino mas jehová cargó en él el pecado de todos nosotros

**vosk · WER 4.17%:** mas él herido fue por nuestras rebeliones molido por nuestros pecados el castigo de nuestra paz sobre él y por su llaga fuimos nosotros curados todos nosotros nos descarriadas como ovejas cada cual se apartó por su camino mas jehová cargó en él el pecado de todos nosotros

**xlsr · WER 14.58%:** macel herido fue por nuestras rebeliones molido por nuestros pecados el castigo de nuestra paz sobre el y por su llaga fuimos nosotros curados todos nosotros nos descargamos como ovejas cada cual se apartó por su camino mas geová cargó en el el pecado de todos nosotros

**parakeet · WER 2.08%:** Mas Él, herido fue por nuestras rebeliones, molido por nuestros pecados, el castigo de nuestra paz sobre él, y por su llaga fuimos nosotros curados. Todos nosotros nos descarriamos como ovejas, cada cual se apartó por su camino, mas Jehová cargó en él el pecado de todos nosotros.

**whisper · WER 6.25%:** Mas él, herido, fue por nuestras rebeliones, molido por nuestros pecados, el castigo de nuestra paz sobre él, y por su yaga fuimos nosotros curados, todos nosotros nos descarriamos como vejas, cada cual se apartó por su camino, mas Jehová cargó en él el pecado de todos nosotros.

**crisper · WER 6.25%:** Mas él, herido, fue por nuestras rebeliones, molido por nuestros pecados, el castigo de nuestra paz sobre él, y por su llaga fuimos nosotros curados, todos nosotros nos descariamos como vejas, cada cual se apartó por su camino, mas Jehová cargó en él el pecado de todos nosotros.

### 3719_1378_000088 · 12.50 s

**Referencia:** que quien la sabe tratar la volverá en oro purísimo de un inestimable precio hala de tener el que la tuviere a raya o dejándola correr en torpes sátiras ni en desalmados sonetos

**vosk · WER 18.18%:** que quien la sabe tratar la volverá en oro purísimo de un inestimable precio a la detener el que la tuviere a raya o dejándola correr en torpeza sátiras mien desalmados sonetos

**xlsr · WER 9.09%:** que quien la sabe tratar la volverá en oro purísimo de un inestimable precio a la detener el que la tuviere a raya o dejándola correr en torpes sátiras ni en desalmados sonetos

**parakeet · WER 9.09%:** que quien la sabe tratar la volverá en oro purísimo de un inestimable precio, al a detener, el que la tuviere a raya, o dejándola correr en torpes sátiras ni en desalmados sonetos,

**whisper · WER 9.09%:** que quien la sabe tratar la volverá en oro purísimo de un inestimable precio, a la de tener el que la tuviera a raya o dejándola correr en torpes sátiras ni en desalmados sonetos.

**crisper · WER 18.18%:** Que quien la sabe tratarla volverá en oro purísimo de un inestimable precio, ala de tener el que la tuviera a Raya o dejando la correr en torpes sátiras ni en desalmados sonetos.

### 6671_9310_000004 · 10.66 s

**Referencia:** añadió despues de un silencio prolongado y solo desde ayer sé todo lo que os concierne sin duda no ignorais

**vosk · WER 30.00%:** añadió después de un silencio prolongado hizo batiste ayer se todo lo que os concierne sin duda no ignoráis

**xlsr · WER 20.00%:** añadió después de un silencio prolongado y solo desde ayer se todo lo que os considerne sin duda no ignoráis

**parakeet · WER 35.00%:** Agio, después de un silencio prolongado, Isolo Desde Yer say Todo lo que os concierne. Sin duda no ignorai.

**whisper · WER 20.00%:** añadió después de un silencio prolongado y sólo desde ayer se todo lo que os concierne sin duda no ignoráis

**crisper · WER 20.00%:** Añadió después de un silencio prolongado y sólo desde ayer se todo lo que os concierne, sin duda, no ignoráis.

### 2592_1378_000079 · 12.69 s

**Referencia:** calle señor bueno replicó el cartero que no hubo encanto alguno ni mudanza de rostro ninguna tan lacayo tosilos entré en la estacada como tosilos lacayo salí della

**vosk · WER 46.43%:** cae señor bueno replicó el cartero que no hubo encanto alguno ni mudanzas de rostro ninguna tan lacayo tus silos entreguen en la destacada como tus y los lacayos salid de ella

**xlsr · WER 25.00%:** calle señor bueno replicó el cartero que no hubo encanto alguno ni mudanza de rostro ninguna tan lacayo tusilos entre en la destacada como tusilos lacayos alideya

**parakeet · WER 35.71%:** Calle, señor bueno, replicó el cartero, que no hubo encanto alguno, ni mudanza de rostro ninguna tan la callo tus hilos entré en la estacada como tus hilos la callo salí de ella.

**whisper · WER 46.43%:** Calle, señor bueno, replicó el cartero, que no hubo en canto alguno ni mudanza de rostro ninguna, tan la Calle o tus hilos entré en la estacada como tus hilos la Calle salí de ella.

**crisper · WER 46.43%:** Calle, señor bueno, replicó el cartero, que no hubo en canto alguno ni mudanza de rostro ninguna, tan la calle o tus hilos entré en la estacada como tus hilos la calle salí de ella.

### 3719_1378_000049 · 13.83 s

**Referencia:** y cuando los reyes y príncipes ven la milagrosa ciencia de la poesía en sujetos prudentes virtuosos y graves los honran los estiman y los enriquecen y aun los coronan con las hojas del árbol a quien no ofende el rayo

**vosk · WER 9.76%:** y cuando los reyes y príncipes de en la milagrosa ciencia de la poesía en sujetos prudente virtuosos y graves los honran los estiman y los enriquecen y aun los coronan con las hojas del árbol a quien no ofende del rayo

**xlsr · WER 7.32%:** y cuando los reyes y príncipes veen la milagrosa ciencia de la poesía en sujetos prudentes virtuosos y graves los honran los estiman y los enriquecen y aún los coronan con las hojas del árbol a quien no ofenda el rayo

**parakeet · WER 2.44%:** Y cuando los reyes y príncipes veen la milagrosa ciencia de la poesía en sujetos prudentes, virtuosos y graves, los honran, los estiman y los enriquecen, y aun los coronan con las hojas del árbol a quien no ofende el rayo,

**whisper · WER 2.44%:** Y cuando los reyes y príncipes ven la milagrosa ciencia de la poesía en sujetos prudentes, virtuosos y graves, los honran, los estiman y los enriquecen. Y aún los coronan con las hojas del árbol a quien no ofende el rayo.

**crisper · WER 4.88%:** Y cuando los reyes y príncipes ven la milagrosa ciencia de la poesía en sujetos prudentes, virtuosos y graves, los honran, los estiman y los enriquecen, y aún los coronan con las hojas del árbol a quien ofende el rayo.

Fuentes técnicas del aviso de Crisper: transformers_engine.py de crisperwhisper 2.0.3 instalado localmente; https://github.com/nyrahealth/CrisperWhisper/blob/main/DOCS.md (ruta Transformers y alineación con estados blank derivados de energía). La evidencia decisiva de esta ejecución es crisper.log, conservado sin modificar.
