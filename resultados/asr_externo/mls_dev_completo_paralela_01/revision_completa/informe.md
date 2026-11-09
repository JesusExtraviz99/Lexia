# MLS dev completo · revisión compartida

Revisión técnica del 06/11/2026: 2408 audios, 9.9887 horas por motor y 87,446 palabras. Cinco motores completados, sin fallos ni hipótesis vacías. Recalculadas métricas y alineamientos de los 12.040 resultados; mismos IDs, referencias y huellas entre motores; cotejadas las 2.408 huellas con FLAC locales. Sin reconocimiento nuevo ni escucha humana independiente.

Transferencia verificada: SHA256 del TAR coincide con el checksum del servidor. Archivos originales conservados.

## Precisión y coste observado

| Motor | WER % | CER % | S / D / I | ASR acumulado min | RTF | RAM RSS máx. MiB | VRAM PID máx. MiB |
|---|---:|---:|---|---:|---:|---:|---:|
| parakeet | 6.57 | 2.37 | 3894 / 1318 / 535 | 9.35 | 0.0156 | 4674.4 | 4024.0 |
| whisper | 7.79 | 2.42 | 5077 / 711 / 1024 | 20.87 | 0.0348 | 3203.8 | 2002.0 |
| crisper | 8.51 | 2.65 | 5410 / 714 / 1316 | 116.87 | 0.1950 | 6289.9 | 4130.0 |
| xlsr | 9.65 | 2.35 | 5962 / 1861 / 613 | 4.94 | 0.0082 | 4415.7 | 3112.0 |
| vosk | 12.93 | 4.24 | 7797 / 1524 / 1983 | 50.83 | 0.0848 | 240.3 | CPU |

WER es (sustituciones + omisiones + inserciones) / palabras de referencia; menor es mejor, no es porcentaje de audios incorrectos. CER aplica errores a caracteres. Se conservan tildes y ortografía original; se ignoran mayúsculas y puntuación según el protocolo. RTF divide tiempo ASR por duración de audio; 0,01 equivale a un segundo de cálculo por cien de audio.

Los tiempos ASR excluyen carga, calentamiento, lectura, puntuación y escritura. RAM/VRAM son máximos muestreados de la sesión, incluida carga y calentamiento. Los cinco procesos se ejecutaron concurrentemente: CPU, RAM y disco compartidos. No equivalen a rendimiento aislado ni predicen una tablet.

## Distribución y cobertura

| Motor | Audios exactos % | WER p95 % | WER máximo % | Carga s | Calentamiento s | Sesión min | Audios con muestra GPU |
|---|---:|---:|---:|---:|---:|---:|---:|
| vosk | 6.06 | 30.15 | 117.65 | 0.50 | 1.54 | 51.83 | 0/2408 |
| xlsr | 12.00 | 24.14 | 117.65 | 9.56 | 2.84 | 12.05 | 481/2408 |
| parakeet | 34.18 | 26.99 | 100.00 | 11.34 | 2.90 | 17.00 | 754/2408 |
| whisper | 16.03 | 21.74 | 88.24 | 2.36 | 4.79 | 26.04 | 1321/2408 |
| crisper | 14.12 | 22.22 | 644.44 | 9.78 | 8.11 | 124.79 | 2408/2408 |

## Conclusiones y límites

- Parakeet presenta el menor WER global en este conjunto. Su cola de errores por audio es más desfavorable que la de Whisper: el promedio global no elimina casos problemáticos. Revisar ejemplos antes de seleccionar candidatos.
- XLSR presenta el menor CER y el menor tiempo ASR acumulado. El orden por caracteres y por palabras difiere; no reducir la comparación a una única métrica.
- Crisper conserva utilidad potencial para literalidad, pero esta evaluación externa no tiene referencias de disfluencias: no demuestra que conserve mejor trabadas. Sus inserciones extremas deben revisarse. Vosk usa CPU y menos RAM; no se compara su velocidad como si usara la misma GPU.
- Las tres GPU neuronales más rápidas terminan antes que Crisper. El grado de concurrencia cambia durante la sesión; reservar una prueba aislada y fija para comparar costes.
- Muestreo GPU aproximadamente cada segundo: llamadas rápidas pueden no contener muestras. No significa GPU inactiva. Energía y potencia de GPU física incluyen carga/calentamiento y cualquier proceso concurrente; no son consumo neto por audio ni medida de batería/tablet.
- Avisos de Crisper sobre encoder_blank_head y parámetros de generación se conservan en logs/verificacion.json. No se atribuyen errores a ese aviso sin demostrarlo. Límites de generación y marcas fuera de rango se enumeran abajo.
- Conservamos todos los clips, incluidos valores extremos. Un WER superior al 100 % es posible por inserciones; no se recorta. Los ejemplos siguientes son discrepancias frente a referencias, no prueba por escucha de una alucinación.
- Test sigue reservado. Revisar casos extremos y fijar configuraciones antes de evaluar test u otro corpus. Las métricas de lectura/disfluencias se estudiarán en el banco propio con referencias humanas.

## Alertas de revisión

- vosk: indicador de límite de generación no instrumentado; marcas fuera de rango en 0 clips; máximo de otros procesos GPU observado: no disponible/CPU.
- xlsr: indicador de límite de generación no instrumentado; marcas fuera de rango en 0 clips; máximo de otros procesos GPU observado: 0.
- parakeet: indicador de límite de generación activado en 0 clips; marcas fuera de rango en 0 clips; máximo de otros procesos GPU observado: 0.
- whisper: indicador de límite de generación no instrumentado; marcas fuera de rango en 0 clips; máximo de otros procesos GPU observado: 0.
- crisper: indicador de límite de generación no instrumentado; marcas fuera de rango en 3 clips; máximo de otros procesos GPU observado: 0.

El indicador de límite de generación se instrumenta explícitamente en Parakeet: no se activa en ninguno de sus 2.408 clips. La ausencia de indicador en otros motores no demuestra que no alcanzaran límites internos.

Crisper presenta tres palabras con final unos 140 ms posterior a la duración del archivo (IDs en verificacion.json). Es una alerta temporal independiente del WER.

## Revisión humana completada · 06/11/2026

Los nueve casos están revisados por el usuario. Cuatro referencias resultan incompletas o diferentes al audio; esas inserciones no deben interpretarse automáticamente como invenciones. Se confirman la repetición extensa de Crisper y una salida inventada de Parakeet, además de observaciones sobre palabras cortadas y añadidos. Métricas oficiales intactas; selección de diagnóstico, no estimación del porcentaje de referencias defectuosas del corpus. Detalle en [cierre_escucha_humana.md](cierre_escucha_humana.md), anotaciones originales en escucha_humana/. Sin segunda escucha independiente.

## Escuchas prioritarias (selección inicial, ya revisada)

- **6671_9310_000053**: Crisper repite extensamente «lo digo»; referencia de 27 palabras, WER 644,44 %. Conservar el caso como fallo de salida para diagnóstico.
- **3678_1378_000014**: varios motores incluyen una presentación de la grabación y números de capítulo ausentes de la referencia. Escuchar antes de atribuirlo a invención.
- **11670_10604_000122**: Parakeet añade un cierre y un crédito de grabación; comprobar si forman parte del audio sin transcribir en la referencia.

No se modifica ninguna referencia ni se elimina ningún clip.

## Casos para comprobación textual

Diez clips con mayor WER por motor; selección de diagnóstico, no muestra representativa. Las salidas completas están en transcripciones_comparadas.json y los JSON originales por audio.

### vosk

**3678_1378_000014 · 16.34 s · WER 117.65 %**

Referencia: segunda parte del ingenioso caballero don quijote de la mancha por miguel de cervantes saavedra y no

Hipótesis: grabadas por ángeles a en pamplona y dos mil nueve segunda parte del ingenioso caballero don quijote de la mancha por miguel de cervantes saavedra capítulos setenta y uno setenta y dos capitulo setenta y uno

**11670_10604_000122 · 15.62 s · WER 114.29 %**

Referencia: remedio contra el sueño de la vida

Hipótesis: remedio contra el sueño de la vida fin del poema grabado por antonio soto patiño

**10367_10282_000017 · 11.12 s · WER 83.33 %**

Referencia: habiendo él llevado el pecado de muchos y orado por los transgresores

Hipótesis: habiendo él llevado el pecado de muchos y orado por los transgresores fin del capítulo cincuenta y tres del libro de isaías

**4589_1378_000069 · 11.58 s · WER 75.00 %**

Referencia: fin del capítulo veinte

Hipótesis: fin del capítulo treinta y cuatro

**1227_567_000088 · 14.16 s · WER 72.73 %**

Referencia: el rey por cuanto por parte de vos miguel de cervantes

Hipótesis: sin de testimonio de la hacer ratas el rey por cuanto por parte de voz miguel de cervantes

**4589_1378_000133 · 18.84 s · WER 70.00 %**

Referencia: este libro de la segunda parte del ingenioso caballero don quijote de la mancha por miguel de cervantes saavedra y

Hipótesis: grabada por rafael ernesto moran el salvador segunda parte del ingenioso caballero don quijote de la mancha por miguel de cervantes saavedra capítulos treinta y tres y treinta y cuatro

**133_1378_000084 · 10.51 s · WER 66.67 %**

Referencia: fin del capítulo

Hipótesis: fin de capítulo catorce

**3678_1378_000058 · 11.03 s · WER 60.00 %**

Referencia: fin del capítulo veinte y

Hipótesis: fin del capitulo setenta y dos

**10367_10282_000052 · 10.46 s · WER 56.25 %**

Referencia: quién ha creído á nuestro anuncio y sobre quién se ha manifestado el brazo de jehová

Hipótesis: grabado por rodrigo hinojosa isaías cincuenta y tres quién ha creído á nuestro anuncio y sobre quien se ha manifestado el brazo de jehová

**133_1378_000024 · 11.87 s · WER 53.33 %**

Referencia: aljófar los sauces destilaban maná sabroso reíanse las fuentes murmuraban los arroyos alegrábanse las selvas

Hipótesis: al jofaina los sauces desfilaban manas sabroso reían se las fuentes murmuraban los arroyos alegraban se las selvas

### xlsr

**3678_1378_000014 · 16.34 s · WER 117.65 %**

Referencia: segunda parte del ingenioso caballero don quijote de la mancha por miguel de cervantes saavedra y no

Hipótesis: grabada por angelezaun en pamplona iruña dos mil nueve segunda parte del ingenioso caballero don quijote de la mancha por miguel de cervantes saavedra capítulos setenta y uno y setenta y dos capítulo setenta y uno

**11670_10604_000122 · 15.62 s · WER 100.00 %**

Referencia: remedio contra el sueño de la vida

Hipótesis: remedio contra el sueño de la vidafin del poema grabado por antonio sotopatiño

**10367_10282_000017 · 11.12 s · WER 91.67 %**

Referencia: habiendo él llevado el pecado de muchos y orado por los transgresores

Hipótesis: habiendo el llevado el pecado de muchos y orado por los transgresoresfin del capítulo cincuenta y tres del libro de isaíes

**10367_10282_000052 · 10.46 s · WER 75.00 %**

Referencia: quién ha creído á nuestro anuncio y sobre quién se ha manifestado el brazo de jehová

Hipótesis: grabado por rodrigo hinojosa is ahía cincuenta y tresquién ha creído a nuestro anuncio y sobre quien se ha manifestado el brazo de geová

**4589_1378_000069 · 11.58 s · WER 75.00 %**

Referencia: fin del capítulo veinte

Hipótesis: fin del capítulo treinta y cuatro

**1227_567_000088 · 14.16 s · WER 72.73 %**

Referencia: el rey por cuanto por parte de vos miguel de cervantes

Hipótesis: fin de testimonio de las herratasel reypor cuanto por parte de voz miguel de cervantes

**4589_1378_000133 · 18.84 s · WER 70.00 %**

Referencia: este libro de la segunda parte del ingenioso caballero don quijote de la mancha por miguel de cervantes saavedra y

Hipótesis: grabada por rafael ernesto morán el salvadorsegunda parte del ingenioso caballero don quijote de la mancha por miguel de cervantes saavedra capítulos treinta y tres y treinta y cuatro

**133_1378_000084 · 10.51 s · WER 66.67 %**

Referencia: fin del capítulo

Hipótesis: fin de capítulo catorce

**2592_1378_000032 · 11.64 s · WER 58.82 %**

Referencia: segunda parte del ingenioso caballero don quijote de la mancha por miguel de cervantes saavedra y no

Hipótesis: rds segunda parte del engenioso caballero don quijote de la mancha por miguel de cervantes avedra capítulos sesenta y cinco a sesenta y seis

**6671_9310_000002 · 15.96 s · WER 54.17 %**

Referencia: este paquete encerral a una caria asaz insignificante para inés fleming y tambien un testamento á favor de esajoven qué conlenia esa carta preguntó

Hipótesis: este paquete encerraba una carta a saz insignificante para iness fleming y también un testamento a favor de esa jovenqué contenía esa carta preguntó mr bro

### parakeet

**11670_10604_000122 · 15.62 s · WER 100.00 %**

Referencia: remedio contra el sueño de la vida

Hipótesis: Remedio contra el sueño de la vida. Fin del poema grabado por Antonio Sotopatiño.

**13257_11991_000034 · 20.00 s · WER 88.37 %**

Referencia: usted me diga el nombre de la muchacha de quien voy a hablarle esa muchacha por la que tanto nos hemos interesado todos la miss musgrove a quien le ocurrió aquello su nombre siempre se me olvida ana se habría ruborizado de dar

Hipótesis: La Miss Musgrove Aquile Corrior Aquello Sumbre Siempre Semolida Anna Cabri Rub.

**3678_1378_000014 · 16.34 s · WER 88.24 %**

Referencia: segunda parte del ingenioso caballero don quijote de la mancha por miguel de cervantes saavedra y no

Hipótesis: Grabada por Ángel Ezaun en Pamplona Yerruña, dos mil nueve segunda parte del Ingenioso Caballero Don Quijote de la Mancha por Miguel de Cervantes Saavedra, CAPOLO SETENTION y SETENTIO, CAPÍTULO SETENTION

**13257_11991_000017 · 18.03 s · WER 87.50 %**

Referencia: tú si te preocupa lo que ocurra en uppercross donde como sabes no es fácil hallar materia para escribir hemos pasado unas pascuas bien aburridas míster musgrove y su señora no han tenido gente a comer ni una sola vez

Hipótesis: In Uppercross, donde Composades no es facil ayar material para scribir.

**13257_11991_000002 · 10.12 s · WER 85.00 %**

Referencia: han llegado a bath los croft los arrendatarios de kellynch qué es lo que te han traído una carta de

Hipótesis: Angegablos Croft, Los Arendatarios de Kelnik, Caes Loketean Traido, Unacarte de Uppercaster,

**10367_10282_000017 · 11.12 s · WER 83.33 %**

Referencia: habiendo él llevado el pecado de muchos y orado por los transgresores

Hipótesis: Habiendo él llevado el pecado de muchos y orado por los transgresores. Fin del capítulo cincuenta y tres del Libro de Isaías.

**13257_11991_000067 · 20.00 s · WER 82.98 %**

Referencia: daremos juntos un delicioso paseo y además tengo que decirle a usted algo mientras vamos andando cójase usted de mi brazo eso es no me hallo satisfecho si no voy así con una mujer pues señor vaya un barco dijo mirando por última vez el cuadro al

Hipótesis: Deremos un delicioso passo y a Di mas Tango de Cleuste Argo Mentres Bamus Andando Casted Mibrazo Es Nisfecho Sino Buasiconamer. Pues signor Bayon Bargo de Murando Purulamis El Cuadro

**13257_11991_000064 · 20.00 s · WER 82.22 %**

Referencia: nave de menos en nuestra actual casita es porque nos recuerda la primera que vivimos en yarmouth hasta el detalle de colarse el viento por una de las ventanas al avanzar un poco más se aventuró ana a reordarle su promesa de comunicarle algo interesante

Hipótesis: Nada de menos in Casita is Purchinos in Yarmouth, as the Colasel Bento Puruna de la Ventanas. Alavancerumpo Massaventurana Recordarle su promessa de communicale.

**13257_11991_000025 · 16.50 s · WER 80.49 %**

Referencia: y nos sorprendió que no hubiese venido con ellos el capitán benwick que también había sido invitado y no sabes cuál es la explicación pues ni más ni menos que el estar en amores con luisa y no querer venir a

Hipótesis: E no Surprendiocenoubies Venukaneos El Capitan Benwick Catamina Besido Invitado. E no Sabesquales, Nimas Nimeno Cel Star in Amores Con Luis No Cervenir Apocraft.

**13257_11991_000083 · 20.00 s · WER 80.43 %**

Referencia: tiene que ir pensando en otra yo creo que lo mejor es traerle a bath sofía tiene que escribirle suplicándole que venga aquí hay lindas muchachas no tiene para qué volver a uppercross porque según tengo entendido la otra miss musgrove está ya comprometida a un

Hipótesis: Yo creo que lo mejor is Trail Abath. Sofia Tine Scribile supplicando cross Porque Seguntengo Tendido Lautra Miss Musgrove Staya Comprometida.

### whisper

**3678_1378_000014 · 16.34 s · WER 88.24 %**

Referencia: segunda parte del ingenioso caballero don quijote de la mancha por miguel de cervantes saavedra y no

Hipótesis: Grabada por Ángeles Záun en Pamplona Eruña 2009. Segunda parte del ingenioso caballero Don Quijote de la Mancha, por Miguel de Cervantes a Avedra, capítulos 71 y 72, capítulos 71.

**10367_10282_000017 · 11.12 s · WER 66.67 %**

Referencia: habiendo él llevado el pecado de muchos y orado por los transgresores

Hipótesis: habiendo él llevado el pecado de muchos y orado por los transgresores. Fin del capítulo 53 del libro de Isaías.

**133_1378_000084 · 10.51 s · WER 66.67 %**

Referencia: fin del capítulo

Hipótesis: fin de capítulo 14

**1227_567_000088 · 14.16 s · WER 63.64 %**

Referencia: el rey por cuanto por parte de vos miguel de cervantes

Hipótesis: fin de testimonio de las erratas el rey por cuanto por parte de vos miguel de serbantes

**13257_11991_000067 · 20.00 s · WER 59.57 %**

Referencia: daremos juntos un delicioso paseo y además tengo que decirle a usted algo mientras vamos andando cójase usted de mi brazo eso es no me hallo satisfecho si no voy así con una mujer pues señor vaya un barco dijo mirando por última vez el cuadro al

Hipótesis: y daremos juntos un delicioso paseo, y además tengo que decirle a usted algo mientras vamos andando. ¡Cójase usted de mi brazo, eso es! No me ayúdase a desfecho si no voy así con una mujer. Pues, señor, vaya a un barco, dijo Morando, por última vez, el cuadro, al punto de ver que hay que ir a un barco, y que hay que ir a un barco, y que hay que

**4589_1378_000133 · 18.84 s · WER 50.00 %**

Referencia: este libro de la segunda parte del ingenioso caballero don quijote de la mancha por miguel de cervantes saavedra y

Hipótesis: Grabada por Rafael Ernesto Morán El Salvador Segunda parte del ingenioso caballero Don Quijote de la Mancha por Miguel de Cervantes Saavedra Capítulos 33 y 34

**13257_11991_000044 · 13.82 s · WER 48.15 %**

Referencia: ser creída y sólo a costa de ímprobos esfuerzos logró ana dominarse bastante para no salir de la estancia adoptar un aire de tranquila indiferencia y contestar

Hipótesis: Se ha creído, y sólo a cosa de improbos esfuerzos logró anadominarse bastante para no salir de la estancia. A lo tal, un aire de tranquila en diferencia y contestar acuerd...

**2592_1378_000079 · 12.69 s · WER 46.43 %**

Referencia: calle señor bueno replicó el cartero que no hubo encanto alguno ni mudanza de rostro ninguna tan lacayo tosilos entré en la estacada como tosilos lacayo salí della

Hipótesis: Calle, señor bueno, replicó el cartero, que no hubo en canto alguno ni mudanza de rostro ninguna, tan la Calle o tus hilos entré en la estacada como tus hilos la Calle salí de ella.

**6671_9310_000002 · 15.96 s · WER 45.83 %**

Referencia: este paquete encerral a una caria asaz insignificante para inés fleming y tambien un testamento á favor de esajoven qué conlenia esa carta preguntó

Hipótesis: Este paquete encerraba una carta asas insignificante para Inés Fleming y también un testamento a favor de esa joven. ¿Qué contenía esa carta? preguntó Mr. Brown.

**1227_567_000075 · 11.64 s · WER 45.45 %**

Referencia: fecha en valladolid a veinte y seis días del mes de setiembre de mil y seiscientos y cuatro años yo el rey

Hipótesis: Fecha en Valladolid a 26 días del mes de septiembre de 1604 años. Yo es rey.

### crisper

**6671_9310_000053 · 14.68 s · WER 644.44 %**

Referencia: la confesion de su falta y votos de prosperidad para la joven respondió monks nada mas en aquel entonces ella se hallaba en cinta de algunos meses

Hipótesis: Lo lo que lo que lo que lo digo, lo que lo digo, lo digo, lo digo, lo digo, lo digo, lo digo, lo digo, lo digo, lo digo, lo digo, lo digo, lo digo, lo digo, lo digo, lo digo, lo digo, lo digo, lo digo, lo digo, lo digo, lo digo, lo digo, lo digo, lo digo, lo digo, lo digo, lo digo, lo digo, lo digo, lo digo, lo digo, lo digo, lo digo, lo digo, lo digo, lo digo, lo digo, lo digo, lo digo, lo digo, lo digo, lo digo, lo digo, lo digo, lo digo, lo digo, lo digo, lo digo, lo digo, lo digo, lo digo, lo digo, lo digo, lo digo, lo digo, lo digo, lo digo, lo digo, lo digo, lo digo, lo digo, lo digo, lo digo, lo digo, lo digo, lo digo, lo digo, lo digo, lo digo, lo digo, lo digo, lo digo, lo digo, lo digo, lo digo, lo digo, lo digo, lo digo, lo digo, lo digo, lo digo, lo

**3678_1378_000014 · 16.34 s · WER 123.53 %**

Referencia: segunda parte del ingenioso caballero don quijote de la mancha por miguel de cervantes saavedra y no

Hipótesis: Crabada por Ángel Ezaun en Pamplona Eruña dos mil nueve, segunda parte del ingenioso caballero Don Quijote de la Mancha por Miguel de Cervantes Saavedra, capítulos setenta y uno y setenta y dos, capítulos setenta y uno.

**11670_10604_000122 · 15.62 s · WER 100.00 %**

Referencia: remedio contra el sueño de la vida

Hipótesis: Remedio contra el sueño de la vida. Fin del poema, grabado por Antonio Sotopatiño.

**4589_1378_000069 · 11.58 s · WER 100.00 %**

Referencia: fin del capítulo veinte

Hipótesis: Fín del capítulo treinta y cuatro.

**10367_10282_000017 · 11.12 s · WER 83.33 %**

Referencia: habiendo él llevado el pecado de muchos y orado por los transgresores

Hipótesis: Habiendo él llevado el pecado de muchos y orado por los transgresores. Fin del capítulo cincuenta y tres del libro de Isaías.

**4589_1378_000133 · 18.84 s · WER 70.00 %**

Referencia: este libro de la segunda parte del ingenioso caballero don quijote de la mancha por miguel de cervantes saavedra y

Hipótesis: Gravada por Rafael Ernesto Morán el Salvador. Segunda parte del ingenioso caballero Don Quijote de la Mancha por Miguel de Cervantes Saavedra, capítulos treinta y tres y treinta y cuatro.

**10367_10282_000052 · 10.46 s · WER 68.75 %**

Referencia: quién ha creído á nuestro anuncio y sobre quién se ha manifestado el brazo de jehová

Hipótesis: Gravado por Rodrigo Inojosa, Isaías cincuenta y tres, quien ha creído a nuestro anuncio y sobre quien se ha manifestado el brazo de Jehová.

**133_1378_000084 · 10.51 s · WER 66.67 %**

Referencia: fin del capítulo

Hipótesis: Fin de capítulo catorce.

**1227_567_000088 · 14.16 s · WER 63.64 %**

Referencia: el rey por cuanto por parte de vos miguel de cervantes

Hipótesis: Fín de testimonio de las erratas. El rey, por cuanto por parte de voz, Miguel de Cervantes.

**13257_11991_000044 · 13.82 s · WER 51.85 %**

Referencia: ser creída y sólo a costa de ímprobos esfuerzos logró ana dominarse bastante para no salir de la estancia adoptar un aire de tranquila indiferencia y contestar

Hipótesis: Se ha creído, y sólo a causa de improbos esfuerzos logró anadominarse bastante para no salir de la estancia, a lo tal un aire de tranquila en diferencia y contestar a coedas.

