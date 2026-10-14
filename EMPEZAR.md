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

## Entorno

Python 3.12 aislado en .tools/python; entorno en .venv. No hace falta activarlo: los comandos usan directamente su ejecutable. Librerías en requirements.txt; versiones completas en requirements-lock.txt tras la instalación. Modelo multilingüe small en modelos/faster-whisper-small, ejecución inicial CPU int8.

El audio se procesa localmente. La carpeta está dentro de OneDrive: su sincronización depende de tu configuración. Las grabaciones y los modelos están excluidos de Git, lo que no modifica OneDrive.
