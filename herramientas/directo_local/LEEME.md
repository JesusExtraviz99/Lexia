# Lectura en directo en el ordenador

Primera prueba local con micrófono, hipótesis ASR y resaltado del texto. El navegador captura audio; Python y los pesos ya descargados realizan el reconocimiento **en la CPU del mismo ordenador**, sin servicios de voz externos o servidor de la empresa. Escucha únicamente en `127.0.0.1`.

Tras el segundo feedback humano del 09/11, se separa posición reconocida de guía visual: fondo amarillo para la palabra siguiente a la última reconocida, subrayado discreto para esta última. Antes de empezar se señala la primera; al reconocer la última no se señala una palabra inexistente. No se suman palabras al registro del alineador ni se avanza por temporizador; relecturas siguen la nueva posición reconocida. Es una guía textual derivada, no predicción acústica ni demostración de menor latencia. Si la hipótesis llega tarde, la guía también puede quedarse detrás del lector.

Nuevo contraste solicitado: frecuencia experimental de 0,125 s (valor inicial de la interfaz) y selector de guía «Una palabra»/«Bloques de 2 palabras», con una palabra inicialmente. En bloques se mantienen posiciones 1–2 hasta reconocer ambas, después 3–4, etc.; el último bloque puede tener una sola palabra. No son dos palabras futuras que se deslicen con cada coincidencia. La posición ASR permanece intacta; el modo visual se registra como `visual_guide` por sesión. El marcador sigue la voz, sin temporizador que avance el texto. La frecuencia solicitada no garantiza ocho reconocimientos por segundo.

Tras la primera prueba Android se sustituye esa presentación de parejas fijas por **Dos palabras móviles**, tanto en PC como en la APK 0.2: cada avance reconocido desplaza la ventana visual una palabra. La guía abarca las dos siguientes desde la posición reconocida; al final puede quedar solo una. Se registra como `sliding_next_words`, conservando `fixed_pairs` en los registros históricos. No cambia los umbrales del alineador ni acredita menos demora de reconocimiento.

Orden de la prueba: con Tiny, ventana 4 s y una palabra, comparar 0,125 frente a 0,25 s manteniendo ritmo parecido; después, con la misma configuración acústica, comparar bloques de dos. El usuario aclaró que «aumentar ritmo» significa aumentar frecuencia de actualización, no leer más rápido. Agrupar palabras es un experimento visual distinto: no reduce el tiempo de reconocimiento. No cambiar ambos factores a la vez para interpretar el resultado.

Los tres modelos iniciales fueron una selección práctica para construir el prototipo: Granite por su equilibrio MLS y Moonshine Small/Tiny para contrastar opciones compactas en CPU. Todos reutilizan el mismo alineador. No es una selección definitiva mediante pruebas en directo de todos los motores. Posteriormente se incorporan Parakeet y Canary v2, con pesos existentes cotejados y el mismo alineador; Whisper y otros siguen pendientes.

En la sonda técnica de tres ventanas públicas de cuatro segundos, Canary tarda 1,00–1,12 s y Parakeet 1,52–3,39 s en esta CPU. Incluye primeras inferencias y escritorio compartido; no es benchmark aislado o prueba humana, pero aconseja comprobar el retraso antes de considerarlos equivalentes a Tiny/Small. No se cambia a otro modelo silenciosamente si alguno no sigue el ritmo. La interfaz ofrece los cinco y permite preparar uno a la vez.

Desde la raíz del proyecto:

```powershell
.\.tools\asr-ampliacion-env\Scripts\python.exe -u -m scripts.directo_local --puerto 8790 --hilos 8
```

Abrir [Lexia local](http://127.0.0.1:8790/). Esperar a «Granite preparado», elegir texto y pulsar «Activar micrófono y empezar». Aceptar personalmente el permiso de Chrome. Terminar con el botón de la página. Para otro reconocedor, finalizar, seleccionarlo y pulsar «Preparar modelo». Solo un modelo cargado y una sesión activa; no se ejecutan reconocedores en paralelo.

## Qué se compara

- Granite TurboCTC, Moonshine Small/Tiny español, Parakeet y Canary v2 disponibles con checkpoints instalados. El argumento --modelo permite escoger el inicial; el servicio conserva el seleccionado al actualizarlo cuando es posible. CPU float32, adaptadores anteriores y revisión/huellas de pesos verificadas. El servicio inicial usaba cuatro hilos; tras una sonda local se activa con ocho mediante `--hilos 8`. El argumento permite 1/2/4/8, se registra por sesión y es un ajuste de este ordenador, no una conclusión sobre Android. Sin descargas al ejecutar.
- Tras la primera lectura humana con retraso (09/11/2026), valores iniciales de la interfaz: ventana de cuatro segundos y petición cada medio segundo. Selectores permiten ventanas 4/6/8 y pasos 0,5/1/2; 8 s y 2 s reproducen la configuración inicial. En el registro de esa lectura, las 19 inferencias tardan 0,44–0,82 s y el alineador añade un tiempo despreciable: la espera de unos dos segundos entre peticiones contribuye al retraso, pero no se ha medido demora por palabra contra referencia humana.
- El paso es una solicitud, no garantía de frecuencia. Si el motor tarda más, se envía la ventana más reciente al quedar libre, sin acumular tareas antiguas. Acortar la ventana reduce contexto y puede perjudicar reconocimiento o recuperación; comparar precisión y acompañamiento en una nueva lectura. La configuración elegida queda guardada por sesión y el servidor valida su límite de muestras. Se registra cualquier hueco de audio que dejara de procesarse si el cálculo supera la ventana.
- Ajuste posterior de respuesta del mismo día: paso inicial 0,25 s, conservando ventana de 4 s y una sola palabra resaltada. AudioWorklet entrega bloques de 512 muestras (32 ms a 16 kHz) en vez de 2.048 (128 ms). Se envía inmediatamente el corte más reciente si ya corresponde actualizar al terminar una petición. Copia del anillo mediante segmentos contiguos. El informe de tiempos del DOM anterior viaja en la siguiente petición de audio y el último se guarda al finalizar: no requiere una segunda petición antes de continuar. El registro conserva `client_profile`, bloque de captura, política de envío de métricas e hilos; no se inventan actualizaciones ni palabras futuras.
- Sonda local de 1/2/4/8 hilos: nueve inferencias por opción, tres ventanas de un clip público y tres rondas con orden mezclado; calentamiento tras cambiar hilos. Medianas de 0,86/0,48/0,34/0,31 s, todas las hipótesis idénticas. Es una sonda pequeña de coste, no generalización o latencia de micrófono. Prueba HTTP final con cuatro cortes públicos: 0,31–0,34 s ASR, tiempos DOM conservados. Queda pendiente comprobar la mejora percibida en una nueva lectura humana.
- Captura mono, AudioWorklet y remuestreo a 16 kHz cuando hace falta. Se solicitan cancelación de eco, supresión de ruido y ganancia automática desactivadas; los valores reales concedidos se registran, no se presupone que el dispositivo respete la petición. Sin VAD o limpieza externa añadidos.
- Se reutilizan Tracker original y su política de hipótesis idéntica para los tres candidatos; no se inventan tiempos de palabra para activar variantes temporales experimentales que requieren esas marcas. La posición es la última coincidencia apoyada por texto; no es la palabra acústica instantánea ni diagnóstico lector. Relecturas lejanas conservan los límites conocidos del alineador original.

## Registros y privacidad

`resultados/directo_local/<sesión>.json` guarda texto reconocido, posición/movimientos, intervalos de captura, tiempo real ASR, CPU consumida por inferencia, RSS después del cálculo, ajustes de captura y tiempos de ida/vuelta medidos por el navegador. Este directorio está excluido de GitHub por posible contenido de otros lectores.

«Antigüedad estimada del corte» se calcula con el reloj del navegador al actualizar el DOM respecto al extremo de audio estimado desde la primera entrega del AudioWorklet. No es latencia acústica exacta ni prueba del instante físico de pintura. No se calcula error de posición o calidad lectora sin referencia humana. RSS es una observación, no máximo garantizado; no equivale a batería, GPU o rendimiento de tablet.

El servidor no persiste PCM/WAV. La opción de copia WAV acumula audio en memoria del navegador y ofrece una descarga al finalizar; no la descarga ni publica automáticamente. Si no se marca, solo se conservan los registros de texto y tiempos. La duración de una toma está limitada a diez minutos; para esta primera prueba usar 30–60 segundos. Mantener la pestaña activa.

## Prueba propuesta

Leer el primer cuento una vez de forma normal y comprobar si el resaltado llega al final. Repetir después con pausa y relectura; anotar lo observado por el usuario junto con el registro. Una comprobación técnica con un clip público verifica transporte/motor, pero no se presenta como prueba de micrófono o seguimiento humano en vivo.

## Android: siguiente fase

El usuario dispone de Android. La prueba objetivo posterior debe cargar y ejecutar el modelo **dentro del móvil**, también sin ordenador/servidor. Abrir una web alojada en el PC desde el teléfono solo cambiaría la pantalla/micrófono y no cumpliría esa condición.

Antes de esa fase hay que conocer modelo de teléfono, RAM y versión Android, comprobar runtime/exportación compatibles y medir tamaño, memoria, velocidad sostenida y temperatura. No se garantiza que el checkpoint float32 del PC pueda ejecutarse directamente en Android. Una implementación nativa u otro runtime optimizado deberá validarse con el mismo material; la cuantización sería una configuración nueva para comparar.

Referencias técnicas: [captura de micrófono y contexto seguro](https://developer.mozilla.org/en-US/docs/Web/API/MediaDevices/getUserMedia), [procesamiento AudioWorklet](https://developer.mozilla.org/en-US/docs/Web/API/AudioWorklet). La web de esta fase se utiliza desde localhost; no se abre el servicio a la red.
