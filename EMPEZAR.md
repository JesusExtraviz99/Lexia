# Primera prueba de lectura asistida

## 1. Abrir PowerShell en esta carpeta

```powershell
cd 'C:\Users\PC\OneDrive\Documentos\ChatGPT\Practicas y TFG'
```

## 2. Grabar una lectura propia

```powershell
.\.venv\Scripts\python.exe scripts\grabar.py --segundos 40
```

El programa muestra el texto y espera a que pulses Enter. Solo entonces activa el micrófono. Lee el texto con normalidad y espera a que termine. Si necesitas más tiempo, usa --segundos 60. El WAV se guarda en datos/audio.

Para consultar micrófonos:

```powershell
.\.venv\Scripts\python.exe scripts\grabar.py --dispositivos
```

Para elegir uno, añade --dispositivo seguido de su número. Si Windows impide grabar, revisa el acceso al micrófono de las aplicaciones de escritorio en Configuración.

## 3. Transcribir la última grabación

```powershell
.\.venv\Scripts\python.exe scripts\transcribir.py
```

Muestra texto y guarda un JSON con tiempos estimados y duración de procesamiento en resultados. También puedes pasar la ruta de un archivo como argumento.

## 4. Revisar lo ocurrido

Escucha el audio y compara con la transcripción: ¿faltan palabras?, ¿inventa alguna?, ¿conserva una repetición? El cuento esperado no equivale a una transcripción humana de lo pronunciado.

Esta prueba procesa el audio después de grabarlo. El seguimiento en directo se construirá en el siguiente hito. Los tiempos estimados del ASR no son referencia humana.

## 5. Alinear la transcripción con el cuento

```powershell
.\.venv\Scripts\python.exe scripts\alinear.py
```

Compara el último JSON de transcripción con el cuento. Guarda un informe Markdown y un JSON en resultados/alineamientos. No necesita descargar librerías ni ejecutar otra vez el modelo.

Para elegir una transcripción concreta:

```powershell
.\.venv\Scripts\python.exe scripts\alinear.py resultados\lectura_20261014_082953_219058_20261014_083013_046227.json
```

Para otro texto, añade --cuento seguido de la ruta de su archivo TXT. Los índices del cuento empiezan en 1. Se ignoran mayúsculas y puntuación, pero se conservan tildes y ñ.

El informe muestra coincidencias, omisiones, inserciones, sustituciones y repeticiones candidatas. No decide si una diferencia corresponde al lector o al ASR. Las omisiones no reciben tiempos inventados; las palabras reconocidas conservan los tiempos estimados originales. Un fragmento eliminado por el ASR, como mari…, no se recupera comparando textos.

## 6. Probar seguimiento progresivo con una grabación

```powershell
.\.venv\Scripts\python.exe -u scripts\seguir.py
```

Usa el último WAV. No activa el micrófono ni descarga modelos. Cada dos segundos de audio disponible vuelve a reconocer el prefijo acumulado, sin proporcionar el audio futuro al ASR. Se ejecuta como simulación, sin esperar los intervalos reales entre bloques.

La posición es el índice de la última palabra del cuento apoyada por coincidencia textual. Puede retroceder al revisar la hipótesis; no equivale todavía a señalar la palabra que se pronuncia en ese instante. La primera palabra sola no basta para mover el indicador: se exigen al menos dos coincidencias.

El seguidor compara las últimas ocho palabras de cada hipótesis dentro de una ventana local de hasta 12 palabras anteriores y 24 posteriores a su posición. Tolera algunas inserciones, omisiones y sustituciones. Una búsqueda global de recuperación exige dos posiciones candidatas consecutivas iguales; no se confirma con una hipótesis idéntica repetida en silencio. Estos umbrales son iniciales y no están validados con niños.

Para reproducir la primera grabación:

```powershell
.\.venv\Scripts\python.exe -u scripts\seguir.py datos\audio\lectura_20261014_081816_009646.wav
```

Guarda un informe Markdown y el historial JSON en resultados/seguimiento. El historial conserva cada hipótesis, corte de audio, posición, movimiento, evidencia y tiempos de procesamiento. También estima la cola que se formaría procesando los bloques secuencialmente: no es una medición de latencia visual.

Comprueba si llega al final, si se detiene con la repetición/omisión y si hay retrocesos o saltos inesperados. Una posición conservada durante silencio es esperable. Como reprocesa prefijos cada vez más largos, esta versión se limita a grabaciones de hasta 120 segundos y no es la arquitectura final para cuentos largos.

Cada nueva versión se prueba localmente y se sube a GitHub después de la confirmación del usuario.

## 7. Comparar ventanas acústicas con el prefijo completo

```powershell
.\.venv\Scripts\python.exe -u scripts\comparar_ventanas.py
```

Procesa la última grabación tres veces: prefijo completo, ventana de 6 s y ventana de 10 s. Mantiene bloques de 2 s, modelo, CPU, VAD y seguidor. No usa audio futuro, no activa el micrófono y no descarga nada.

Las ventanas se desplazan 2 s por actualización: solapamiento de 4 s para la ventana de 6 y de 8 s para la de 10. Los tiempos de cada hipótesis se trasladan al reloj global del audio. Las palabras solapadas no se concatenan ni se cuentan como nuevos intentos lectores.

Guarda un resumen comparativo y los historiales de cada método en resultados/comparaciones, dentro de una carpeta por ejecución. La posición previa del cuento se mantiene entre ventanas. No se fusiona todavía una transcripción final de ventanas.

Para comparar ambas grabaciones:

```powershell
.\.venv\Scripts\python.exe -u scripts\comparar_ventanas.py --todos
```

Para probar únicamente una ventana de 6 s:

```powershell
.\.venv\Scripts\python.exe -u scripts\seguir.py --ventana 6
```

Revisa el total de procesamiento, las inferencias que superan 2 s, la cola simulada y las posiciones por bloque. Llegar al final no demuestra que el seguimiento temporal sea preciso. La comparación usa una ejecución por método en orden fijo: es orientativa y no controla calentamiento ni carga del ordenador.

### Experimento ampliado: cinco ventanas y dos rondas

```powershell
.\.venv\Scripts\python.exe -u scripts\comparar_ventanas.py --ventanas 0 4 6 8 10 12 --repeticiones 2
```

El 0 representa el prefijo completo. Las otras ventanas tienen solapamientos de 2, 4, 6, 8 y 10 s, manteniendo una actualización cada 2 s. Se realizan doce ejecuciones secuenciales sobre el último WAV. Puede tardar varios minutos; conviene mantener condiciones similares del ordenador durante la prueba.

El orden se aleatoriza por ronda con una semilla registrada. El informe muestra cada ejecución, las medias y rangos de procesamiento, colas simuladas y posiciones por bloque. Dos rondas permiten observar variación, pero no bastan para una validación estadística ni infantil. No cambia el modo predeterminado: el comando sin opciones sigue comparando 0, 6 y 10 s una vez, ahora en orden aleatorio.

Las nuevas ampliaciones quedan locales hasta que las pruebes y autorices subirlas.

## Entorno

Python 3.12 aislado en .tools/python; entorno en .venv. No hace falta activarlo: los comandos usan directamente su ejecutable. Librerías en requirements.txt; versiones completas en requirements-lock.txt tras la instalación. Modelo multilingüe small en modelos/faster-whisper-small, ejecución inicial CPU int8.

El audio se procesa localmente. La carpeta está dentro de OneDrive: su sincronización depende de tu configuración. Las grabaciones y los modelos están excluidos de Git, lo que no modifica OneDrive.
