# Una grabación por lector y texto

Desde la carpeta del proyecto, en PowerShell:

```powershell
.\.venv\Scripts\python.exe -u -m scripts.grabar_lector
```

Elige el número del texto (se muestran inicio y número de palabras), escribe un identificador de lector como lector_02, elige el tipo de lectura e indica el ambiente si interesa. Usa siempre el mismo identificador para la misma persona y uno diferente para cada lector. Evita nombres y apellidos en los archivos.

Se muestra el texto completo antes de abrir la captura. Enter inicia; otro Enter termina y guarda. El límite de seguridad es diez minutos. Ctrl+C cancela, no sirve para terminar y guardar. Cada ejecución hace una sola grabación y termina: vuelve a ejecutar el comando para la siguiente persona o lectura.

Ejemplo de archivo: `Lectura normal - lectura_03 - 28-10-2026 - lector_02.wav`, dentro de datos/audio. Si se repiten texto, tipo, lector y fecha se añade un sufijo de hora para conservar las tomas anteriores. El catálogo conserva ID estable, huella, texto y lector; el nombre indica la consigna, no valida lo realmente pronunciado. El 29/10/2026 se unificaron también los nombres de las grabaciones existentes, conservando aliases históricos. Los IDs numéricos se normalizan a lector_01, lector_02, etc. Los futuros registros con --lector, también desde grabar.py, incluyen el lector en el nombre.

Para ver los textos sin grabar:

```powershell
.\.venv\Scripts\python.exe -m scripts.grabar_lector --listar
```

Este selector no ejecuta reconocimiento ni publica los audios. Para elegir otro micrófono consulta scripts.grabar --dispositivos y pasa su índice con --dispositivo.

## Publicación y privacidad

Solo se publican los WAV del lector_01. Los audios de los demás lectores quedan excluidos de Git. Sus resultados de reconocimiento y evaluación sí pueden publicarse con identificadores anónimos, según autorización del usuario del 29/10/2026; esta autorización no incluye adjuntar voces, clips ni audio incrustado en páginas o informes.

El catálogo completo se mantiene en datos/referencias/catalogo_local.json (ignorado por Git), que los scripts usan si existe. datos/referencias/catalogo.json es una exportación pública limitada al lector original. Antes de publicar, ejecutar `python -m scripts.exportar_catalogo_publico` para actualizarla. En un clon público, los scripts usan directamente el catálogo público. Los resultados pueden incluir los IDs de otros lectores; revisar por separado que no contengan archivos de voz.
