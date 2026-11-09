# Lexia · piloto Android local

Estado: versiones 0.1–0.4 ensayadas por el usuario; versión 0.5 preparada con guía de tres palabras, pendiente de lectura en el teléfono.

Los dos JSON originales de la primera prueba se han importado con copia byte a byte en `resultados/android/sesiones/20261109`, excluidos de GitHub, e informe en `resultados/android/revision_20261109_primera_prueba`. Ambos llegan a 56, pero se observan posiciones estables con nuevas hipótesis rechazadas por el alineador; no una congelación total acreditada. Tiny: PSS máximo 238,5 MiB y mediana del SDK para líneas completas 115,5 ms; Small: 433,1 MiB y 224 ms. Son métricas distintas de los tiempos de ventanas del PC y no prueban latencia por palabra. Se confirma Android16/API36 y unos 11,12 GiB de RAM visible al sistema (variante comercial de 12 GB).

## Dispositivo comunicado

Redmi Note 13 Pro+ 5G. La [ficha oficial de Xiaomi España](https://www.mi.com/es/product/redmi-note-13-pro-plus-5g/specs/) indica MediaTek Dimensity 7200-Ultra (ocho núcleos, hasta 2,8 GHz), GPU Mali-G610, variantes 8 GB/256 GB o 12 GB/512 GB y batería de 5.000 mAh. No se presupone qué variante de RAM posee el usuario ni su versión Android actual: el registro recoge modelo, versión del sistema, ABI y memoria física disponible.

## Pasar la APK al teléfono

Actualización preparada: `.descartados/android/lexia-piloto-0.5-arm64.apk` en la raíz del proyecto. Se puede enviar con LocalSend como la anterior. Mantiene el mismo identificador y certificado: instalar como actualización conserva modelos y registros. Las APK anteriores se conservan como evidencia. También se puede transferir por USB, sin depuración USB, root o Python en el teléfono.

1. Abrir **Lexia · piloto local**.
2. Elegir `lectura_01.txt`, **Moonshine Tiny español** y **Dos palabras móviles**; pulsar **Preparar**. Reutiliza los modelos que ya se descargaron. Solo necesita Wi-Fi si falta alguno. La APK no incluye pesos adicionales.
3. Esperar a «Preparado». Activar modo avión y mantener Wi-Fi apagado para comprobar ejecución local sin conexión. No se necesita tener encendido el ordenador ni mantener abierta la web del PC.
4. Pulsar **Empezar**, conceder el permiso del micrófono y leer normalmente. Mantener la app visible.
5. Pulsar **Terminar**. Se cierra el micrófono/modelo y se guarda un registro privado. Pulsar **Exportar registro JSON** y elegir una ubicación para traer después el archivo al proyecto. La última exportación sigue disponible al volver a abrir la app.
6. Antes de otra toma, pulsar Preparar de nuevo; los archivos descargados se reutilizan. Para probar Small hay que descargarlo una vez con conexión, manteniéndolo como otra configuración.

En la 0.2 la guía pasa de «Ana salió» a «salió al» al reconocer Ana; deja de esperar a completar parejas fijas. Al principio el alineador puede necesitar más de una palabra para situarse, igual que antes. Se mantienen pesos/SDK/umbral del alineador y se añaden a los registros motivo, coincidencias, coste, candidato y línea ASR actual. La guía no fuerza avance por tiempo ni resuelve por sí sola las hipótesis incompatibles. La reproducción Java conserva las mismas posiciones en 2.141 actualizaciones del PC y móvil; extremos/avance deslizante comprobados.

Si falla la preparación, conservar el mensaje exacto de la app; no se cambia silenciosamente a inglés, a reconocimiento del sistema o a un servidor remoto. La primera prueba debe confirmar descarga/carga de español, apertura del micrófono, seguimiento y cierre. Un fallo en esta fase no debe anotarse como resultado de precisión del modelo.

## Prueba 0.5: tres palabras móviles y resultados0.4

Cuatro lecturas reales0.4 con avance con apoyo, contexto original y guía de dos palabras: Tiny0,125 s/0,25 s, Small0,125 s/0,25 s. Todas terminan en56; retrocesos registrados0/1/1/0 y PSS máximo243,1/233,9/436,9/450,1 MiB. El usuario describe menos avances/retrocesos problemáticos. Quedan posiciones estables, incluida una meseta de8,66 s en Small0,125. Son tomas distintas, sin audio/anclas para calcular exactitud o demora acústica: no se afirma que cero retrocesos equivalga a seguimiento correcto, ni se elige cadencia por una sola toma. Informe `resultados/android/revision_20261109_v04/informe.md` y conclusiones complementarias en esa carpeta.

La0.5 añade únicamente **Tres palabras móviles** al selector de guía. Mantiene dos por defecto y las opciones1/2/3. Cada palabra reconocida desplaza la guía una posición; no espera a completar el trío ni mueve el cursor por tiempo. SDK/pesos, cadencias fijas0,125/0,25 y reglas de avance/relectura son los de0.4; el JSON ya registra el ancho elegido.

Para aislar el efecto visual, repetir las cuatro combinaciones anteriores eligiendo **Tres palabras móviles + Avance con apoyo + Contexto local original**, mismo cuento y ritmo normal parecido. Exportar los JSON. Si es necesario reducir la tanda, comparar primero dos y tres palabras con el mismo modelo y la misma cadencia.

**Cadencia adaptativa: propuesta, no activada.** El usuario amplía su rango experimental a0,125/0,25/0,5 s: lectura lenta estable → intervalo mayor/menos llamadas; rápida → menor/más llamadas. El binding Java0.1.5 expone `setUpdateInterval` como ajuste dinámico y ya adapta su puerta de cálculo a la duración del pase anterior. La opción nativa `transcription_interval` se configura al cargar: cambiar solo el binding no garantiza igual cadencia efectiva del ASR. Habría que diseñar el control con base nativa compatible, registrar ambos intervalos y cada cambio, y medir carga/resultado. El ritmo inferido de los avances es una estimación contaminada por errores, agrupación de hipótesis y recuperaciones: no son tiempos humanos por palabra. No ralentizar solo por ausencia de avance; podría ser un atasco. Propuesta: promediar varios avances respaldados, cambios con histéresis y volver a modo rápido ante incertidumbre. Comparar más adelante contra cadencias fijas, conservando la misma guía y reglas. La0.5 no incluye modo automático ni opción fija0,5.

## Historial0.4: apoyo de avances y recuperación reciente

El usuario fija 0,25 s como intervalo máximo de futuras pruebas. La 0.4 ofrece **0,25 y 0,125 s**, este último preseleccionado. Los dos JSON0.2 ya estaban importados; se incorpora la nueva toma0.3 con Small,0,125 s y contexto original. Conserva exactamente los archivos del modelo Small. Termina en56, pero con tres retrocesos breves después de avances sobre hipótesis dudosas y una meseta en53 durante27,33 s. No hay audio/anclas nuevas para cuantificar cuánto se anticipó a la voz. El feedback humano comunica invenciones y avances excesivos; el registro permite explicar las decisiones, no escuchar esas palabras.

Nuevo selector **Seguidor original · referencia / Avance con apoyo · experimental**. Sigue preseleccionado el original: la variante debe elegirse explícitamente. Conserva las dos palabras móviles, VAD/modelos y recuperación global; no cambia la transcripción ni aplica un bloqueo general de retrocesos.

- **Original:** últimas ocho palabras normalizadas, al menos dos exactas, proporción exacta≥60 %, coste de edición≤40 %; usa la última coincidencia del alineamiento, que puede quedar antes de una terminación incorrecta. Texto idéntico no actualiza. Tras dos fallos locales puede buscar globalmente y exige repetir el candidato en otra hipótesis procesada.
- **Avance con apoyo:** mantiene esos umbrales, pero un destino hacia delante debe coincidir con la última palabra de la hipótesis; si avanza más de una posición, exige además dos palabras finales consecutivas exactas.
- **Recuperación reciente de la variante:** si no avanza, permite un sufijo de la línea ASR actual de3–8 palabras consecutivas exactas, al menos una de cinco caracteres, con una sola aparición en el cuento y destino dentro de las24 posiciones siguientes. Evita que texto antiguo incompatible impida aprovechar una frase reciente clara. No acepta una palabra aislada ni dos palabras como recuperación nueva.

La reproducción de cinco tomas Android conserva todos los finales y pasa de seis a cero retrocesos registrados. En la última evita los avances dudosos de28,93/47,03/52,25 s y acepta el final en el callback99,45 frente a110,31 s: son momentos guardados de la misma toma, **no latencias acústicas nuevas**. No se etiqueta todo cambio como mejora humana. Siete controles unitarios incluyen límites adversos: puede retrasar palabras ya correctas si después llega una palabra incompleta; una frase inventada exacta todavía puede activarla. No corrige las invenciones del ASR. Informe completo `resultados/android/apoyos_20261109/informe.md` y revisión de tres tomas `resultados/android/revision_20261109_v03_0125`.

**Siguiente comprobación compartida:** instalar0.4 como actualización, elegir Small, lectura_01, dos palabras móviles,0,125 s y contexto original. Comparar una toma con seguidor original y otra con **Avance con apoyo**, manteniendo el mismo ritmo normal, y exportar ambos JSON. No modificar a la vez el margen de cinco. Si interesa contrastar carga/cadencia, repetir después el experimental a0,25 s. No continuar repitiendo frases para forzar un resultado perfecto: anotar dónde se atasca y terminar la toma permite conservar evidencia del fallo.

## Historial 0.3: cadencia nativa y margen local

La 0.2 ya tiene dos lecturas reales importadas: ambas llegan a 56; Tiny sin retrocesos y Small con dos. La 0.3 está compilada y comprobada, pendiente de lectura real. Conserva SDK/pesos y añade dos selectores independientes; sus valores se exportan en cada JSON.

- **ASR 0,50 / 0,25 / 0,125 s**: fija explícitamente `transcription_interval` del motor nativo. En 0.1/0.2 solo se pedía `setUpdateInterval(.125)` al binding Java; no se fijaba la opción interna. La [documentación oficial](https://moonshine-voice.readthedocs.io/en/stable/api/options/) separa ambas y documenta 0,5 s por defecto. La fuente Java 0.1.5 advierte de esa diferencia; la clave existe en el binario utilizado. Esto no acredita que cada pase termine dentro del intervalo solicitado ni que el tiempo real sea el documentado por defecto. No se cambia VAD, precisión numérica, idioma, contexto del ASR o modelo.
- **Contexto local original / buscar desde cinco palabras atrás**: el segundo comienza cinco posiciones antes de la aceptada, incluyendo también la palabra actual (offset interno 6, frente al original 12). Mantiene 24 posiciones por delante, los umbrales y la recuperación global tras fallos; no es una prohibición absoluta de relectura lejana. El cuento se usa para alinear hipótesis, no se entrega al reconocedor. En las cuatro tomas guardadas evita un retroceso de los tres observados y conserva los cuatro finales. No mejora los otros dos retrocesos, situados dentro del margen, ni demuestra aceleración del ASR.

Orden propuesto, mismo texto/modelo **Small**, guía de dos palabras móviles y ritmo normal semejante:

1. Referencia: **0,50 s + contexto original**. Exportar JSON.
2. Cambiar solo a **0,25 s**, Preparar y repetir. Exportar JSON y comparar sensación/atascos.
3. Mantener **0,25 s**, cambiar solo a **cinco palabras atrás** y repetir. Exportar JSON.
4. Si 0,25 s resulta estable, ensayar **0,125 s + contexto original**; no se presupone que más frecuencia sea más rápida bajo carga.

No saltar directamente a lectura extrema: primero comparar lectura normal. Las tomas no contienen audio/anclas humanas, así que se contrastan hipótesis, movimientos, tiempos de callback, PSS/CPU y feedback; no se declara latencia acústica por palabra. La 0.3 registra también tiempo propio del alineador, separado del ASR. Valores iniciales de la app: 0,50 s y contexto original, para disponer de referencia explícita. El selector de ASR obliga a preparar de nuevo antes de empezar.

## Configuración distinta del ordenador

- En el PC, Transformers/PyTorch reprocesa ventanas móviles de cuatro segundos. Esta app usa **Moonshine Voice 0.1.5 para Android**, modelos españoles streaming Tiny/Small en el formato nativo del SDK/ONNX y captura/segmentación de la propia biblioteca. El código y modelos streaming españoles están documentados por el proveedor como de uso gratuito con licencia MIT; no requiere cuenta o API de pago. [API y guía oficial](https://moonshine-voice.readthedocs.io/en/latest/quickstart/), [modelos](https://moonshine-voice.readthedocs.io/en/latest/models/available-models/).
- Se pide actualización cada 0,125 s; el SDK adapta la cadencia a la carga y sus parámetros internos. No se garantizan ocho actualizaciones por segundo ni se iguala esta cadencia a latencia de voz a pantalla. No se fuerza el número de hilos del PC ni se emplean CUDA/QNN de Qualcomm en MediaTek.
- No se presume que los archivos SDK coincidan byte a byte con los checkpoints safetensors ensayados. Al preparar el modelo, se guardan manifiesto de dependencias, arquitectura, idioma y SHA256 de sus archivos; permite identificar la configuración real. Su calidad y rendimiento deben evaluarse como nueva configuración.
- El alineador Java replica el Tracker textual original y la política de hipótesis idéntica del PC, sin restricciones nuevas que impidan relecturas. Se verificó igualdad de posiciones en 1.889 actualizaciones guardadas. La guía por parejas no modifica las posiciones reconocidas ni la transcripción.

## Datos y métricas

La app no guarda ni sube la voz. Guarda texto/posiciones dentro de su almacenamiento privado y solo exporta el JSON al elegirlo el usuario. Copias automáticas de datos desactivadas. La conexión de la preparación se usa para archivos oficiales del modelo; después del caché la prueba se realiza sin conexión.

El JSON incluye:

- Identidad y huellas del texto/modelo, modo de guía y configuración del SDK.
- Modelo/versión Android, ABI y RAM física/ disponible al comenzar.
- Hipótesis parciales/finales, posición/movimiento y momento de los callbacks.
- Latencia reportada por el SDK en líneas completas cuando existe, sin presentarla como latencia acústica física de cada palabra.
- PSS de toda la app y CPU acumulada de la app, muestreados aproximadamente cada segundo.
- Duración, posición final, motivo de cierre; batería y temperatura de batería al principio/final. Esta temperatura no es la del procesador y el cambio de batería en una toma corta no es energía del modelo.

No hay métricas de error lector/literalidad, demora por palabra o exactitud de posición sin referencia humana; tampoco medidas directas de utilización/energía GPU. No se comparan sin más PSS Android y RSS Windows ni la CPU del móvil con la GPU del servidor. Las voces/registros de los lectores siguen sujetos a las reglas de privacidad del proyecto.

## Construcción y comprobaciones

Proyecto Java/Gradle, minSdk 26, objetivo Android 35, compilación SDK 36, ABI arm64-v8a. Para recompilar desde la raíz del proyecto con las herramientas ya instaladas:

```powershell
.\scripts\compilar_android.ps1
```

Se fijan AGP 8.13.0, Moonshine SDK 0.1.5 y dependencias transitivas mediante `app/gradle.lockfile`. El SDK oficial tiene versiones posteriores; no se cambia automáticamente la versión ensayada. Java, Android SDK y Gradle existentes se usan sin modificar configuraciones del sistema.

La entrega tiene compilación y Android Lint sin errores (persisten avisos no bloqueantes de textos españoles sin internacionalizar, target/API/ABI o versión de dependencia). Firma APK v2 y alineación de empaquetado verificadas. No equivale a prueba instrumentada ni reconocimiento verificado en el dispositivo real. Código, README y evidencia de preparación son publicables; APK, cachés, propiedades locales y registros no se añaden automáticamente a GitHub.
