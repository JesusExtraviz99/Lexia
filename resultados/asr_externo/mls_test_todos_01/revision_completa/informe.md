# MLS test · comparación de los doce candidatos

Auditoría técnica: 12 motores, 2385 audios (10.0036 h) por motor; 28,620 resultados y alineamientos recalculados. Transferencia SHA256 cotejada, selección oficial local completa y huellas verificadas, configuración fijada desde dev, firmas/cobertura/resúmenes/telemetría comprobados. Originales y referencias conservados. Sin nuevas inferencias ni escucha humana independiente.

## Conclusiones para la preselección

- Canary registra el menor WER test (3,45 %) y CER (1,22 %); Granite queda en 3,50 % WER. Son 3.053 frente a 3.101 errores sobre 88.500 palabras: diferencia de 48 errores, unos 0,054 puntos porcentuales. Sin contraste estadístico no se declara una superioridad concluyente. Granite obtiene más clips exactamente coincidentes (42,01 % frente a 40,92 %); ambas métricas resumen aspectos distintos.
- Granite mantiene el menor tiempo ASR observado: 2,27 min para diez horas de audio, frente a 27,87 min de Canary; su sesión completa dura 7,46 min y no debe confundirse con tiempo ASR. Es el candidato principal por equilibrio observado entre error y coste, pendiente de seguimiento real y tablet.
- Parakeet queda casi al nivel de Moonshine Small en WER (4,81 frente a 4,79 %) y procesa más rápido en estas configuraciones (8,67 frente a 28,48 min). Moonshine Small consume menos VRAM por PID observada (1.938 frente a 4.460 MiB). Conservar ambos para contrastar rapidez/memoria, sin atribuir a tablet las mediciones de servidor. El menor WER de Parakeet respecto a dev no supone cambios del modelo: se han evaluado audios diferentes.
- Whisper Turbo conserva interés como referencia de precisión (4,08 %), con mayor coste que Granite/Parakeet. Qwen1.7B (4,58 %) requiere 10.202 MiB de VRAM y 88,87 min ASR, sin superar aquí a varios modelos menos costosos. Qwen0.6B, XLSR y Vosk no encabezan precisión; Vosk conserva el extremo de memoria CPU reducida, unos 233 MiB RSS, con WER 12,85 %.
- Los doce motores se ejecutaron de nuevo en esta cohorte: no se reutilizó ningún test anterior. Todos completaron 2.385/2.385, sin fallos operativos ni hipótesis vacías; esto no significa ausencia de errores de reconocimiento.
- Moonshine Tiny activa el indicador de límite en dos clips y sus salidas contienen repeticiones extensas (676_567_000042 y 676_567_000072); pendientes de escucha. Crisper presenta marcas nativas fuera de rango en once clips. No modificar límites, referencias o pesos a partir de este test para volver a presentarlo como independiente.
- Los resúmenes de recursos de los doce motores también se han recalculado a partir de las muestras, con coincidencia. Dev/test no comparten FLAC idénticos por SHA256. Detalles en verificacion_recursos_alertas.json; esto no comprueba independencia frente al entrenamiento.

Siguiente paso propuesto: revisar selectivamente estas alertas y las referencias de mayor discrepancia, continuar el contraste externo en FLEURS con configuraciones fijadas y después valorar los candidatos sobre nuestro banco y seguimiento en directo. La preselección es provisional; todavía no se activa ningún motor en la aplicación.

## Precisión: dev frente a test

| Modelo | WER dev % | WER test % | Diferencia pp | CER test % | Audios exactos % | S / D / I test |
|---|---:|---:|---:|---:|---:|---|
| canary_v2 | 3.50 | 3.45 | -0.05 | 1.22 | 40.92 | 2219 / 464 / 370 |
| granite_turboctc | 3.35 | 3.50 | +0.15 | 1.26 | 42.01 | 2269 / 551 / 281 |
| whisper_turbo | 4.00 | 4.08 | +0.08 | 1.46 | 37.48 | 2624 / 601 / 390 |
| qwen_asr_17b | 4.72 | 4.58 | -0.14 | 1.47 | 32.16 | 3013 / 453 / 587 |
| moonshine_small_es | 4.95 | 4.79 | -0.16 | 1.65 | 33.58 | 3079 / 608 / 551 |
| parakeet | 6.57 | 4.81 | -1.77 | 1.59 | 33.84 | 3089 / 577 / 587 |
| moonshine_tiny_es | 5.79 | 5.83 | +0.04 | 1.99 | 28.09 | 3718 / 648 / 793 |
| qwen_asr_06b | 7.20 | 7.03 | -0.17 | 2.14 | 17.36 | 4618 / 705 / 898 |
| whisper | 7.79 | 7.51 | -0.28 | 2.31 | 17.19 | 4866 / 680 / 1097 |
| crisper | 8.51 | 8.23 | -0.27 | 2.49 | 14.68 | 5327 / 666 / 1294 |
| xlsr | 9.65 | 9.86 | +0.21 | 2.34 | 10.90 | 6068 / 1993 / 662 |
| vosk | 12.93 | 12.85 | -0.08 | 4.17 | 6.42 | 7929 / 1523 / 1920 |

WER: sustituciones + omisiones + inserciones por palabra de referencia. No es porcentaje de audios erróneos ni tasa de acierto; puede superar el 100 %. CER por caracteres, incluidos espacios. Una diferencia negativa significa menos error en test; son conjuntos distintos, no una mejora de pesos o reglas. No se ha realizado contraste estadístico pareado entre modelos.

## Coste y recursos observados

| Modelo | ASR min | RTF | RAM RSS máx. MiB | VRAM PID máx. MiB | Carga s | Sesión min | Reutilizado |
|---|---:|---:|---:|---:|---:|---:|---|
| canary_v2 | 27.87 | 0.0464 | 5935.9 | 5640.0 | 12.41 | 32.94 | no |
| granite_turboctc | 2.27 | 0.0038 | 4924.6 | 2986.0 | 8.83 | 7.46 | no |
| whisper_turbo | 41.35 | 0.0689 | 5262.9 | 5094.0 | 10.05 | 46.69 | no |
| qwen_asr_17b | 88.87 | 0.1481 | 11769.0 | 10202.0 | 15.05 | 96.43 | no |
| moonshine_small_es | 28.48 | 0.0474 | 4228.2 | 1938.0 | 8.85 | 33.40 | no |
| parakeet | 8.67 | 0.0144 | 4654.5 | 4460.0 | 16.16 | 14.72 | no |
| moonshine_tiny_es | 18.11 | 0.0302 | 4224.3 | 1778.0 | 7.75 | 23.34 | no |
| qwen_asr_06b | 77.41 | 0.1290 | 5299.9 | 5376.0 | 11.00 | 83.19 | no |
| whisper | 20.22 | 0.0337 | 3208.1 | 2002.0 | 2.14 | 24.82 | no |
| crisper | 101.77 | 0.1696 | 6169.3 | 4192.0 | 17.18 | 110.26 | no |
| xlsr | 4.90 | 0.0082 | 4368.8 | 4682.0 | 8.42 | 10.13 | no |
| vosk | 48.33 | 0.0805 | 233.2 | CPU | 0.52 | 49.26 | no |

ASR excluye carga, calentamiento, E/S, puntuación y escritura. Sesión incluye más operaciones. Máximos RAM/VRAM muestreados, no picos garantizados. Configuraciones y backends diferentes; GPU dedicadas por tarea propia pero CPU/RAM/disco compartidos y concurrencia variable. Los reutilizados conservarían recursos de su ejecución original. No equivale a una medición aislada, latencia del seguidor, batería o rendimiento de tablet. Telemetría completa (CPU/RAM/E/S/GPU/potencia/energía cuando disponible) en los JSON originales y resource_summary del verificador.

## Alertas y revisión pendiente

Las alertas son diagnósticas: ausencia de un indicador no prueba ausencia de truncamiento. Muestras GPU ausentes durante una inferencia rápida no significan GPU inactiva. Marcas temporales con tolerancia de 100 ms al final del archivo.
- canary_v2: 0 indicadores de límite; marcas fuera de rango en 0 clips; muestras GPU en 1686/2385 audios; máximo de otros procesos GPU observado 0.
- granite_turboctc: 0 indicadores de límite; marcas fuera de rango en 0 clips; muestras GPU en 264/2385 audios; máximo de otros procesos GPU observado 0.
- whisper_turbo: 0 indicadores de límite; marcas fuera de rango en 0 clips; muestras GPU en 2292/2385 audios; máximo de otros procesos GPU observado 0.
- qwen_asr_17b: 0 indicadores de límite; marcas fuera de rango en 0 clips; muestras GPU en 2383/2385 audios; máximo de otros procesos GPU observado 0.
- moonshine_small_es: 0 indicadores de límite; marcas fuera de rango en 0 clips; muestras GPU en 1714/2385 audios; máximo de otros procesos GPU observado 0.
- parakeet: 0 indicadores de límite; marcas fuera de rango en 0 clips; muestras GPU en 657/2385 audios; máximo de otros procesos GPU observado 0.
- moonshine_tiny_es: 2 indicadores de límite; marcas fuera de rango en 0 clips; muestras GPU en 1152/2385 audios; máximo de otros procesos GPU observado 0.
- qwen_asr_06b: 0 indicadores de límite; marcas fuera de rango en 0 clips; muestras GPU en 2382/2385 audios; máximo de otros procesos GPU observado 0.
- whisper: 0 indicadores de límite (sin indicador equivalente instrumentado); marcas fuera de rango en 0 clips; muestras GPU en 1274/2385 audios; máximo de otros procesos GPU observado 0.
- crisper: 0 indicadores de límite (sin indicador equivalente instrumentado); marcas fuera de rango en 11 clips; muestras GPU en 2385/2385 audios; máximo de otros procesos GPU observado 0.
- xlsr: 0 indicadores de límite (sin indicador equivalente instrumentado); marcas fuera de rango en 0 clips; muestras GPU en 411/2385 audios; máximo de otros procesos GPU observado 0.
- vosk: 0 indicadores de límite (sin indicador equivalente instrumentado); marcas fuera de rango en 0 clips; muestras GPU en 0/2385 audios; máximo de otros procesos GPU observado no disponible/CPU.

La escucha de referencias problemáticas de dev no valida las de test. WER alto o discrepancias no prueban invención: revisar audio antes de clasificar fallos. Mantener métricas oficiales y anotaciones humanas separadas. Las fuentes de entrenamiento de Moonshine incluyen MLS/FLEURS/CommonVoice: falta auditoría de particiones/IDs antes de afirmar independencia. Este test no acredita literalidad/disfluencias, voz infantil o seguimiento en vivo; se estudiarán en el banco propio. No ajustar configuraciones a partir de test para presentar después este mismo test como evaluación independiente.

## Casos para escucha compartida

Cinco mayores WER por motor; selección dirigida a fallos, no estimación de su frecuencia. Diez ejemplos por modelo en verificacion.json y todos los resultados por audio en las carpetas originales.

### vosk

**3471_1378_000115 · WER 133.33 % · 17.38 s**

Referencia: fin del capítulo

ASR: capitulo cincuenta y uno

**4747_2162_000038 · WER 125.00 % · 20.00 s**

Referencia: la historia del hombre contada por sus casas

ASR: fin de la historia del hombre contada por sus casas grabado por alejandro gonzález en estaba ontario canadá

**97_567_000071 · WER 120.00 % · 12.95 s**

Referencia: encendió el cuadrillero otro candil

ASR: encendió el cuadrillero otro candil fin del capítulo dieciseis capítulo diecisiete

**3471_1378_000091 · WER 63.16 % · 18.22 s**

Referencia: libro de la segunda parte del ingenioso caballero don quijote de la mancha por miguel de cervantes saavedra y

ASR: grabada por daniel escobar en bogotá colombia segunda parte del ingenioso caballero don quijote de la mancha por miguel de cervantes saavedra capítulos cincuenta y cincuenta y uno

**1448_567_000046 · WER 54.17 % · 14.35 s**

Referencia: soy rocinante el famobisnieto del gran babiepor pecados de flaquefui a poder de un don quijoparejas corrí a lo flomas por uña de cabano

ASR: sobre rocinante el famoso bisnieto del babia por pecados de fla que fui a poder de un don quijote parejas corrí a of lo más por uña de caballo


### crisper

**3471_1378_000115 · WER 200.00 % · 17.38 s**

Referencia: fin del capítulo

ASR: Him de El Capítulo cincuenta y uno.

**4747_2162_000038 · WER 137.50 % · 20.00 s**

Referencia: la historia del hombre contada por sus casas

ASR: Fin de La Historia del Hombre contaba por sus casas, grabado por Alejandra González en Ottawa, Ontario, Canadá.

**97_567_000071 · WER 120.00 % · 12.95 s**

Referencia: encendió el cuadrillero otro candil

ASR: Encendió el cuadrillero otro candil. Fin del capítulo dieciséis. Capítulo diecisiete.

**97_567_000146 · WER 66.67 % · 15.10 s**

Referencia: fin del capítulo

ASR: Fim del capítulo diecisiete.

**3471_1378_000091 · WER 63.16 % · 18.22 s**

Referencia: libro de la segunda parte del ingenioso caballero don quijote de la mancha por miguel de cervantes saavedra y

ASR: Gravada por Daniel Escobar en Bogotá, Colombia. Segunda parte del ingenioso caballero Don Quijote de la Mancha por Miguel de Cervantes Saavedra, capítulos cincuenta y cincuenta y uno.


### qwen_asr_17b

**4747_2162_000038 · WER 125.00 % · 20.00 s**

Referencia: la historia del hombre contada por sus casas

ASR: Fin de la historia del hombre contada por sus casas, grabado por Alejandra González en Ottawa, Ontario, Canadá.

**97_567_000071 · WER 120.00 % · 12.95 s**

Referencia: encendió el cuadrillero otro candil

ASR: Encendió el cuadrillero otro candil. Fin del capítulo dieciséis. Capítulo diecisiete.

**3471_1378_000115 · WER 100.00 % · 17.38 s**

Referencia: fin del capítulo

ASR: Fin del capítulo cincuenta y uno.

**12249_11991_000035 · WER 91.18 % · 17.77 s**

Referencia: a su vuelta de lyme los calurosos elogios que de él hiciera como excelente muchacho y como oficial siempre merecedor de su más alta estima que ya le habían granjeado el aprecio de todos

ASR: a su vuelta del ím

**3471_1378_000091 · WER 63.16 % · 18.22 s**

Referencia: libro de la segunda parte del ingenioso caballero don quijote de la mancha por miguel de cervantes saavedra y

ASR: Grabada por Daniel Escobar en Bogotá, Colombia. Segunda parte del ingenioso caballero Don Quijote de la Mancha, por Miguel de Cervantes Saavedra. Capítulos cincuenta y cincuenta y uno.


### qwen_asr_06b

**4747_2162_000038 · WER 125.00 % · 20.00 s**

Referencia: la historia del hombre contada por sus casas

ASR: Fin de la historia del hombre contada por sus casas, grabado por Alejandra González en Ottawa Ontario, Canadá.

**97_567_000071 · WER 120.00 % · 12.95 s**

Referencia: encendió el cuadrillero otro candil

ASR: Encendió el cuadrillero otro candil. Fin del capítulo dieciséis. Capítulo diecisiete.

**3471_1378_000115 · WER 100.00 % · 17.38 s**

Referencia: fin del capítulo

ASR: Fin del capítulo cincuenta y uno.

**3471_1378_000091 · WER 68.42 % · 18.22 s**

Referencia: libro de la segunda parte del ingenioso caballero don quijote de la mancha por miguel de cervantes saavedra y

ASR: Gravada por Daniel Escobar en Bogotá Colombia. Segunda parte del ingenioso caballero Don Quixote de la Mancha por Miguel de Cervantes Saavedra. Capítulos cincuenta y cincuenta y uno.

**3471_1378_000063 · WER 53.33 % · 14.56 s**

Referencia: capítulo li del progreso del gobierno de sancho panza con otros sucesos tales como buenos

ASR: Fin del capítulo cincuenta. Capítulo cincuenta y uno. Del progreso del gobierno de Sancho Pansa con otros sucesos tales como buenos.


### whisper_turbo

**97_567_000071 · WER 120.00 % · 12.95 s**

Referencia: encendió el cuadrillero otro candil

ASR:  encendió el cuadrillero otro candil fin del capítulo 16 capítulo 17

**4747_2162_000038 · WER 100.00 % · 20.00 s**

Referencia: la historia del hombre contada por sus casas

ASR:  La historia del hombre contada por sus casas, grabado por Alejandra González en Ottawa, Ontario, Canadá.

**4096_1378_000012 · WER 54.05 % · 16.58 s**

Referencia: segunda parte del ingenioso caballero don quijote de la mancha por miguel de cervantes saavedra capítulo cincuenta y ocho que trata de como menudearon sobre don quijote aventuras tantas que no se daban vagar unas a otras

ASR:  que trata de cómo menudearon sobre don quijote aventuras tantas que no se daban vagar unas a otras

**1448_567_000046 · WER 45.83 % · 14.35 s**

Referencia: soy rocinante el famobisnieto del gran babiepor pecados de flaquefui a poder de un don quijoparejas corrí a lo flomas por uña de cabano

ASR:  soy rocinante el famó bisnieto del gran babié por pecados de flaqué fui a poder de un don quijó parejas corrí a lo flo más por uña de cabá

**3471_1378_000091 · WER 36.84 % · 18.22 s**

Referencia: libro de la segunda parte del ingenioso caballero don quijote de la mancha por miguel de cervantes saavedra y

ASR:  por daniel escobar en bogotá colombia segunda parte del ingenioso caballero don quijote de la mancha por miguel de cervantes saavedra


### canary_v2

**3471_1378_000115 · WER 166.67 % · 17.38 s**

Referencia: fin del capítulo

ASR: fines capítulo cincuenta y uno

**4747_2162_000038 · WER 125.00 % · 20.00 s**

Referencia: la historia del hombre contada por sus casas

ASR: Fin de la historia del hombre contada por sus casas, grabado por Alejandra González en Ottawa, Ontario, Canadá.

**11168_11991_000026 · WER 52.94 % · 11.96 s**

Referencia: de que al partir se les unieran las musgrove a instigación de maría fin del capítulo cinco

ASR: que al partir de ellos se unieran las Musgrove a instigator de María.

**3471_1378_000091 · WER 52.63 % · 18.22 s**

Referencia: libro de la segunda parte del ingenioso caballero don quijote de la mancha por miguel de cervantes saavedra y

ASR: Daniel Escobar en Bogotá, Colombia Segunda parte del ingenioso Caballero Don Quijote de la Mancha por Miguel de Cervantes Saavedra Capítulos cincuenta y cincuenta y uno.

**1448_567_000046 · WER 45.83 % · 14.35 s**

Referencia: soy rocinante el famobisnieto del gran babiepor pecados de flaquefui a poder de un don quijoparejas corrí a lo flomas por uña de cabano

ASR: Soy Rocinante, el famoso bisnieto del gran Babié. Por pecados de flaqué fui a poder de un don Quijo. Parejas corrí a lo fló mas por uña de cava.


### moonshine_small_es

**4747_2162_000038 · WER 100.00 % · 20.00 s**

Referencia: la historia del hombre contada por sus casas

ASR: la historia del hombre contada por sus casas grabado por alejandra gonzález en ottawa ontario canadá

**1448_567_000046 · WER 45.83 % · 14.35 s**

Referencia: soy rocinante el famobisnieto del gran babiepor pecados de flaquefui a poder de un don quijoparejas corrí a lo flomas por uña de cabano

ASR: soy rocinante el famó bisnieto del gambavíe por pecados de flaqué fui a poder de un don quijo parejas corrí a lo flo más por uña de cavá

**97_567_000071 · WER 40.00 % · 12.95 s**

Referencia: encendió el cuadrillero otro candil

ASR: encendió el cuadrillero otro candil capítulo dieciséis

**7510_9951_000051 · WER 36.36 % · 10.47 s**

Referencia: sea tu misericordia oh jehová sobre nosotros como esperamos en ti

ASR: sea tu misericordia oh jehová sobre nosotros como esperamos en ti salmo treinta y cuatro

**12249_11991_000098 · WER 36.00 % · 11.81 s**

Referencia: afición decidid a la lectura e inclinación a las ocupaciones sedentarias acabó el dramático relato diciendo que la amistad de aquel hombre con los har

ASR: afición decidida la lectura y inclinación a las ocupaciones sedentarias acabó el drama de correr el hato diciendo que la amistad de aquel hombre con los


### moonshine_tiny_es

**4747_2162_000038 · WER 125.00 % · 20.00 s**

Referencia: la historia del hombre contada por sus casas

ASR: fin de la historia del hombre contada por sus casas grabado por alejandra gonzález en octava antario canadá

**3471_1378_000115 · WER 100.00 % · 17.38 s**

Referencia: fin del capítulo

ASR: fin del capítulo cincuenta y uno

**676_567_000042 · WER 100.00 % · 20.00 s**

Referencia: con la punta del lanzón un cojín y una maleta asida a él medio podridos o podridos del todo y deshechos mas pesaban tanto que fue necesario que sancho se apease a tomarlos y mandóle su amo que viese lo que en la maleta venía hízolo con mucha presteza sancho y aunque la maleta vení

ASR: alzaba con la punta del lanzón un cojín y una maleta asida él, medio podridos o podridos del todo y deshechos, mas pesaban tanto que fue necesario que Sancho se apease, se a tomarlos y mandóle su amo que viese lo que en la maleta venía. Hizo loco mucha presteza Sancho, y aunque la maleta venía con la de la de la de la de la de la de la de la de la de la de la de la de la de la de la de la de la de la de la de la de la de la de la de la de

**97_567_000071 · WER 80.00 % · 12.95 s**

Referencia: encendió el cuadrillero otro candil

ASR: encendió el cuadrillero otro candil capítulo dieciséis capítulo diecisiete

**1448_567_000046 · WER 45.83 % · 14.35 s**

Referencia: soy rocinante el famobisnieto del gran babiepor pecados de flaquefui a poder de un don quijoparejas corrí a lo flomas por uña de cabano

ASR: soy rocinante el famou bisnieto del bambabie por pecados de flaquet fui a poder de un don quijo parejas corrí a lo flo mas por uña de cava


### granite_turboctc

**3471_1378_000115 · WER 66.67 % · 17.38 s**

Referencia: fin del capítulo

ASR: Fin del capítulo veinte y.

**12249_11991_000016 · WER 60.87 % · 12.05 s**

Referencia: y por un sincero movimiento de su espíritu sintióse impulsada a platicar con él benwick se mostraba abstraído y propenso a la nostalgia

ASR: E por um sincero movimento de su espirito sentió-se impulsionada a praticar com el benwick se mostrava abstrahido e propenso á la nostalgia.

**1448_567_000046 · WER 50.00 % · 14.35 s**

Referencia: soy rocinante el famobisnieto del gran babiepor pecados de flaquefui a poder de un don quijoparejas corrí a lo flomas por uña de cabano

ASR: Soy Rocinante, el famoso bisnieto del gran babier por pecados de flaqué fui a poder de un don Quijó. parejas corrí aloflo, más por uña de caba.

**97_567_000071 · WER 40.00 % · 12.95 s**

Referencia: encendió el cuadrillero otro candil

ASR: Encendió el cuadrillero otro candil capítulo capítulo.

**12249_11991_000027 · WER 38.10 % · 19.47 s**

Referencia: al cerrar la noche no podía ana menos de sonreír ante la idea de haber venido a lyme a predicar resignación y paciencia a un hombre a quien nunca había visto pero le sugería más serias reflexiones el hecho de que ella

ASR: La noche no podia ana menos de sonreir ante la idea de haber venido á lime á predicar resignacion y paciencia á un hombre á quien nunca habia visto pero le sugeria mas séias reflexiones el lecho de que.


### parakeet

**4747_2162_000038 · WER 125.00 % · 20.00 s**

Referencia: la historia del hombre contada por sus casas

ASR: Fin de la historia del hombre contada por sus casas, grabado por Alejandra González en Ottawa, Ontario, Canadá.

**97_567_000071 · WER 120.00 % · 12.95 s**

Referencia: encendió el cuadrillero otro candil

ASR: encendió el cuadrillero otro candil. Fin del capítulo dieciséis. CAPITULO diecisiete

**3471_1378_000115 · WER 100.00 % · 17.38 s**

Referencia: fin del capítulo

ASR: Fin del capítulo cincuenta y uno

**11168_11991_000039 · WER 81.48 % · 20.00 s**

Referencia: colonos que habían recibido indicaciones de acudir a despedirle ana marchaba al mismo tiempo presa de una desolada tranquilidad a la casita donde había de pasar la primera semana no encontró a su amiga mucho más satisfecha que ella la señora de rusell sintió sobremanera el trasplante familiar pues estimaba la receptividad de los

ASR: Anna marchava at the same time, presa to a desolada tranquilidad, at the casita that the case is a very good thing. No encontration, much more satisfecha que ella. The señora de Russell since familiar, which estimately

**12249_11991_000058 · WER 70.27 % · 18.14 s**

Referencia: y que eran la señora de harville su marido y el capitán benwick que vivía con ellos el capitán benwick había sido algún tiempo atrás primer teniente del laconia y las noticias que de él había dado

ASR: Equieren La Signora de Harville, Summarido El Capitan Benwick, Vivia Conos. El Capitan Benwick Aviasido atras Primer Teniente del Conia, ilas noticias went.


### xlsr

**4747_2162_000038 · WER 125.00 % · 20.00 s**

Referencia: la historia del hombre contada por sus casas

ASR: finn de la historia del hombre contada por sus casas grabado por alejandra gonzabres en ottawa ontario canadá

**3471_1378_000115 · WER 100.00 % · 17.38 s**

Referencia: fin del capítulo

ASR: fin del capítulo cincuenta y uno

**97_567_000071 · WER 100.00 % · 12.95 s**

Referencia: encendió el cuadrillero otro candil

ASR: encendió el cuadrillero otro candilfin del capítulo dieciséiscapítulo diecisiete

**7510_9951_000051 · WER 63.64 % · 10.47 s**

Referencia: sea tu misericordia oh jehová sobre nosotros como esperamos en ti

ASR: sea tu misericordia o geová sobre nosotros  cómo esperamos en tisalmo treinta y cuatro

**3471_1378_000091 · WER 63.16 % · 18.22 s**

Referencia: libro de la segunda parte del ingenioso caballero don quijote de la mancha por miguel de cervantes saavedra y

ASR: grabada por daniel escobar en bogotá colombiasegunda parte del ingenioso caballero don quijote de la mancha por miguel de cervantes saavedracapítulos cincuenta y cincuenta ay uno


### whisper

**4747_2162_000038 · WER 125.00 % · 20.00 s**

Referencia: la historia del hombre contada por sus casas

ASR: Fin de la historia del hombre contada por sus casas, grabado por Alejandra González en Ottawa, Ontario, Canadá.

**97_567_000071 · WER 120.00 % · 12.95 s**

Referencia: encendió el cuadrillero otro candil

ASR: Encendió el cuadrillero otro candil. Fin del capítulo 16. Capítulo 17.

**3471_1378_000115 · WER 100.00 % · 17.38 s**

Referencia: fin del capítulo

ASR: hindes capítulo 51

**3471_1378_000091 · WER 52.63 % · 18.22 s**

Referencia: libro de la segunda parte del ingenioso caballero don quijote de la mancha por miguel de cervantes saavedra y

ASR: Grabada por Daniel Escobar en Bogotá, Colombia. Segunda parte del ingenioso caballero Don Quijote de la Mancha por Miguel de Cervantes Saavedra. Capítulos 50 y 51.

**3471_1378_000152 · WER 51.52 % · 14.03 s**

Referencia: pídese a vuesa merced señor gobernador qué harán los jueces del tal hombre que aun hasta agora están dudosos y suspensos y habiendo tenido noticia del agudo y elevado entendimiento de vuestra merced

ASR: Pídese a Huesa Merced, Señor Gobernador, que eran los jueces del tal hombre, que aun hasta ahora están dudosos y suspensos, y, habiendo tenido noticia del agudo y elevado entendimiento de Huesa Merced, que aún hasta ahora están dudosos y suspensos, y, habiendo tenido noticia

