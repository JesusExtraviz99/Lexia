# MLS dev · comparación de todos los candidatos

Siete nuevos modelos: 16.856 resultados recalculados, 2.408 audios y unas diez horas por motor. Descarga, firmas, cobertura, referencias/huellas, resúmenes y conteos de telemetría verificados. Mismos 2.408 FLAC cotejados localmente. Los cinco resultados anteriores proceden de su auditoría previa; sus manifiestos y resúmenes siguen intactos. Sin inferencias nuevas o escucha independiente.

| Modelo | WER % | CER % | ASR acumulado min | RTF | RAM RSS máx. MiB | VRAM PID máx. MiB |
|---|---:|---:|---:|---:|---:|---:|
| granite_turboctc | 3.35 | 1.28 | 2.21 | 0.0037 | 4885.4 | 2998.0 |
| canary_v2 | 3.50 | 1.24 | 27.34 | 0.0456 | 5949.5 | 5200.0 |
| whisper_turbo | 4.00 | 1.43 | 41.56 | 0.0694 | 5253.3 | 5094.0 |
| qwen_asr_17b | 4.72 | 1.51 | 85.43 | 0.1425 | 11702.7 | 10140.0 |
| moonshine_small_es | 4.95 | 1.76 | 28.44 | 0.0475 | 4235.6 | 1930.0 |
| moonshine_tiny_es | 5.79 | 1.95 | 17.73 | 0.0296 | 4232.3 | 1558.0 |
| parakeet | 6.57 | 2.37 | 9.35 | 0.0156 | 4674.4 | 4024.0 |
| qwen_asr_06b | 7.20 | 2.23 | 75.07 | 0.1253 | 5300.9 | 5314.0 |
| whisper | 7.79 | 2.42 | 20.87 | 0.0348 | 3203.8 | 2002.0 |
| crisper | 8.51 | 2.65 | 116.87 | 0.1950 | 6289.9 | 4130.0 |
| xlsr | 9.65 | 2.35 | 4.94 | 0.0082 | 4415.7 | 3112.0 |
| vosk | 12.93 | 4.24 | 50.83 | 0.0848 | 240.3 | CPU |

## Lectura de los resultados

- Granite obtiene el menor WER (3,35 %) y el menor tiempo ASR observado (2,21 min para unas diez horas de audio). Es el candidato más destacado de este dev para llevar a seguimiento, pendiente de test y prueba en directo; no se declara ganador definitivo.
- Canary obtiene el menor CER (1,24 %) y el segundo WER (3,50 %). Whisper Turbo mejora el WER del Small anterior (4,00 frente a 7,79 %), con mayor coste observado y otro backend.
- Moonshine Small (4,95 % WER, 1.930 MiB de VRAM por PID observados) merece conservarse como alternativa de menor memoria GPU frente a otros candidatos. Tiny reduce más esa memoria pero aumenta el error. Estas mediciones son del servidor; no prueban que funcionen bien en una tablet.
- Qwen 1.7B completa la prueba GPU pese al límite de RAM encontrado localmente al cargarlo en CPU. Su WER de 4,72 % requiere unos 10.140 MiB de VRAM y 85,43 min ASR en esta ejecución: no ofrece aquí la mejor relación observada entre error y coste. Qwen 0.6B tampoco mejora a varios candidatos más rápidos en este dev.
- Menor WER/CER significa menor error frente a las referencias oficiales; no acredita seguimiento en directo, literalidad ni voz infantil.
- Coste ASR con modelo cargado/calentado; excluye carga, lectura y escritura. RAM/VRAM son máximos observados de sesión, no picos garantizados. Ejecuciones concurrentes en fechas/asignaciones diferentes: no atribuir todas las diferencias de tiempo a la arquitectura.
- Se conserva la precisión float32; Whisper Turbo utiliza Transformers, frente a CT2 en Whisper Small, y los nuevos no generan marcas de palabra. Esas diferencias forman parte de cada configuración.
- Moonshine declara fuentes MLS/FLEURS/CommonVoice en entrenamiento. Auditar particiones/IDs antes de afirmar independencia del test o generalización; conocer el corpus de origen no prueba solapamiento de test.
- La revisión humana anterior confirmó referencias incompletas/diferentes en cuatro casos seleccionados: discrepancia frente al texto no equivale siempre a invención. No se han corregido referencias ni eliminado clips.
- No se descartan modelos solo por WER: para el seguidor interesan posición, demora, estabilidad y recuperación en directo, además de coste y viabilidad local.

## Indicadores de límite de generación

Son alertas del adaptador, no diagnóstico automático de truncamiento. Los tokens de inicio/fin y la regla de longitud requieren revisar cada caso; conservar las salidas y el protocolo antes de interpretar o modificar límites.

- moonshine_tiny_es: 0 alertas.
- moonshine_small_es: 0 alertas.
- granite_turboctc: 0 alertas.
- qwen_asr_06b: 0 alertas.
- qwen_asr_17b: 0 alertas.
- canary_v2: 0 alertas.
- whisper_turbo: 0 alertas.

## Casos de mayor error para revisión

### moonshine_tiny_es

**3678_1378_000014 · WER 123.53 %**

Referencia: segunda parte del ingenioso caballero don quijote de la mancha por miguel de cervantes saavedra y no

ASR: grabada por ángeles aún en pamplona eruña dos mil nueve segunda parte del ingenioso caballero don quijote de la mancha por miguel de cervantes saavedra capítulos setenta y uno y setenta y dos capítulos setenta y uno

**4589_1378_000069 · WER 75.00 %**

Referencia: fin del capítulo veinte

ASR: fin del capítulo treinta y cuatro

**133_1378_000084 · WER 66.67 %**

Referencia: fin del capítulo

ASR: fin de capítulo catorce

**10367_10282_000065 · WER 62.07 %**

Referencia: embriaguémonos de sidra y será el día de mañana como este o mucho más excelente fin del capítulo cincuenta y seis del libro de isaías grabado por rodrigo hinojosa

ASR: embriaguemos nos decidra y será el día de mañana como éste o mucho más excelente

**1227_567_000088 · WER 54.55 %**

Referencia: el rey por cuanto por parte de vos miguel de cervantes

ASR: fin de testimonio de las erratas el rey por cuanto por parte de vos miguel de cervantes

### moonshine_small_es

**11670_10604_000136 · WER 81.25 %**

Referencia: sección cuarenta y tres de poesías por miguel de unamuno esta grabación de librebox está en el dominio público grabado por antonio soto patiño meditaciones no busques luz mi corazón sino agua

ASR: no busques luz ni corazón sino agua

**3678_1378_000014 · WER 70.59 %**

Referencia: segunda parte del ingenioso caballero don quijote de la mancha por miguel de cervantes saavedra y no

ASR: grabada por ángeles aún en pamplona y ruña dos mil nueve segunda parte del ingenioso caballero don quijote de la mancha por miguel de cervantes saavedra y

**13257_11991_000046 · WER 52.38 %**

Referencia: primo suyo un joven pastor no opina usted miss elliot que debemos intentar hacerle venir a bath fin del capítulo dieciocho

ASR: un joven pastor no vio usted miseria que debemos intentar hacerle venir á la

**11670_10604_000030 · WER 52.38 %**

Referencia: ved cómo a quien debéis vuestro sendero no es si no a ella fin del poema grabado por antonio soto patiño

ASR: ved cómo a quien debéis vuestro sendero no es sino a él ya

**13257_11991_000102 · WER 48.15 %**

Referencia: o sin aguardar la respuesta qué es lo que trae a los croft vienen por el almirante creen que padece de gota gota y decrepitud dijo sir

ASR: sin acordar la respuesta qué es lo que trae el oscro bien el corel admirante creen que padece de gota gote in di gratitud dijo sir

### granite_turboctc

**11670_10604_000136 · WER 75.00 %**

Referencia: sección cuarenta y tres de poesías por miguel de unamuno esta grabación de librebox está en el dominio público grabado por antonio soto patiño meditaciones no busques luz mi corazón sino agua

ASR: meditaciones no busques luz mi corazón, sino agua.

**133_1378_000084 · WER 66.67 %**

Referencia: fin del capítulo

ASR: Fin de capítulo x.

**4589_1378_000069 · WER 50.00 %**

Referencia: fin del capítulo veinte

ASR: fin del capítulo ve y.

**10367_10282_000065 · WER 48.28 %**

Referencia: embriaguémonos de sidra y será el día de mañana como este o mucho más excelente fin del capítulo cincuenta y seis del libro de isaías grabado por rodrigo hinojosa

ASR: Embriaguémonos de sidra y será el día de mañana como éste o mucho más excelente capítulo l.

**1227_567_000013 · WER 48.28 %**

Referencia: grabada por alejandro garcía en la ciudad de méxico la primera parte del ingenioso hidalgo don quijote de la mancha por miguel de cervantes saavedra capítulo cuarenta y nueve

ASR: libro de la segunda parte del ingenioso caballero don Quijote de la mancha por miguel de Cervantes Saavedra.

### qwen_asr_06b

**3678_1378_000014 · WER 123.53 %**

Referencia: segunda parte del ingenioso caballero don quijote de la mancha por miguel de cervantes saavedra y no

ASR: gravada por Angelizao en Pamplona Irúña dos mil nueve segunda parte del ingenioso caballero don Quixote de la Mancha por Miguel de Cervantes Saavedra capítulos setenta y uno y setenta y dos capítulo setenta y uno

**11670_10604_000122 · WER 100.00 %**

Referencia: remedio contra el sueño de la vida

ASR: Remedio contra el sueño de la vida. Fin del poema. Grabado por Antonio Sotopatiño.

**10367_10282_000017 · WER 83.33 %**

Referencia: habiendo él llevado el pecado de muchos y orado por los transgresores

ASR: Habiendo él llevado el pecado de muchos y orado por los transgresores. Fin del capítulo cincuenta y tres del libro de Isaías.

**4589_1378_000133 · WER 75.00 %**

Referencia: este libro de la segunda parte del ingenioso caballero don quijote de la mancha por miguel de cervantes saavedra y

ASR: Gravada por Rafael Ernesto Moran El Salvador. Segunda parte del ingenioso caballero Don Quixote de la Mancha por Miguel de Cervantes Saavedra. Capítulos treinta y tres y treinta y cuatro.

**133_1378_000084 · WER 66.67 %**

Referencia: fin del capítulo

ASR: Fin de capítulo catorce.

### qwen_asr_17b

**3678_1378_000014 · WER 123.53 %**

Referencia: segunda parte del ingenioso caballero don quijote de la mancha por miguel de cervantes saavedra y no

ASR: Grabada por Ángel Ezáun en Pamplona Irunia, dos mil nueve. Segunda parte del ingenioso caballero Don Quijote de la Mancha, por Miguel de Cervantes Saavedra. Capítulos setenta y uno y setenta y dos. Capítulo setenta y uno.

**11670_10604_000122 · WER 100.00 %**

Referencia: remedio contra el sueño de la vida

ASR: Remedio contra el sueño de la vida. Fin del poema. Grabado por Antonio Sotopatíño.

**10367_10282_000017 · WER 83.33 %**

Referencia: habiendo él llevado el pecado de muchos y orado por los transgresores

ASR: habiendo él llevado el pecado de muchos y orado por los transgresores. Fin del capítulo cincuenta y tres del libro de Isaías.

**4589_1378_000069 · WER 75.00 %**

Referencia: fin del capítulo veinte

ASR: Fin del capítulo treinta y cuatro.

**4589_1378_000133 · WER 70.00 %**

Referencia: este libro de la segunda parte del ingenioso caballero don quijote de la mancha por miguel de cervantes saavedra y

ASR: Grabada por Rafael Ernesto Morán El Salvador. Segunda parte del ingenioso caballero Don Quijote de la Mancha, por Miguel de Cervantes Saavedra. Capítulos treinta y tres y treinta y cuatro.

### canary_v2

**13257_11991_000041 · WER 106.52 %**

Referencia: creo que hubo este otoño algo como un comienzo de amores entre luisa musgrove y él pero no me parece aventurado sospechar que a los dos se les ha pasado del mismo modo y sin que hayan tenido que imponerse la menor violencia me figuro que

ASR: I believe that this autumn there was something like a beginning of loves between Luisa Musgrove and him, but I do not think it is advisable to suspect that both of them have been treated in the same way, and without having had to impose the slightest violence. I imagine that

**3678_1378_000014 · WER 100.00 %**

Referencia: segunda parte del ingenioso caballero don quijote de la mancha por miguel de cervantes saavedra y no

ASR: por Ángel Ezaun en Pamplona Iruña, segunda parte del ingenioso caballero Don Quijote de la Mancha por Miguel de Cervantes Saavedra, capítulos setenta y uno y setenta y dos, capítulos setenta y uno.

**4589_1378_000069 · WER 75.00 %**

Referencia: fin del capítulo veinte

ASR: Fin del capítulo treinta y cuatro

**133_1378_000084 · WER 66.67 %**

Referencia: fin del capítulo

ASR: Fin de capítulo catorce

**13257_11991_000072 · WER 54.55 %**

Referencia: crees tú isabel que será bien presentarlos en laura place oh no creo que no dada nuestra situación con la señora de

ASR: ¿Crees que Isabel será bien presentarlos en su lugar? No, creo que no, no, no, no, no, no, no

### whisper_turbo

**10367_10282_000017 · WER 83.33 %**

Referencia: habiendo él llevado el pecado de muchos y orado por los transgresores

ASR:  habiendo él llevado el pecado de muchos y orado por los transgresores fin del capítulo cincuenta y tres del libro de isaías

**3678_1378_000014 · WER 76.47 %**

Referencia: segunda parte del ingenioso caballero don quijote de la mancha por miguel de cervantes saavedra y no

ASR:  Grabada por Ángel Ezaun en Pamplona, Heruña, 2009. Segunda parte del Ingenioso Caballero Don Quijote de la Mancha. Por Miguel de Cervantes Saavedra. Capítulos 71 y 72. Capítulos 71.

**11670_10604_000136 · WER 75.00 %**

Referencia: sección cuarenta y tres de poesías por miguel de unamuno esta grabación de librebox está en el dominio público grabado por antonio soto patiño meditaciones no busques luz mi corazón sino agua

ASR:  meditaciones no busques luz mi corazón sino agua

**133_1378_000084 · WER 66.67 %**

Referencia: fin del capítulo

ASR:  Fin de capítulo 14

**10367_10282_000052 · WER 56.25 %**

Referencia: quién ha creído á nuestro anuncio y sobre quién se ha manifestado el brazo de jehová

ASR:  grabado por rodrigo hinojosa isaías cincuenta y tres quién ha creído a nuestro anuncio y sobre quién se ha manifestado el brazo de jehová

