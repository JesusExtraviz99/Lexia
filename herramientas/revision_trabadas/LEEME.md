# Revisión cualitativa de la lectura con trabadas

Desde la carpeta del proyecto:

```powershell
.\.venv\Scripts\python.exe -m scripts.revisar_trabadas --puerto 8774
```

Abrir http://127.0.0.1:8774/. No iniciar otra instancia si el servidor ya está abierto. El proceso debe permanecer activo mientras se usa la página.

Se reutilizan los registros de ronda 1 del audio con trabadas del lote 20261023_102114_072901. Cuatro intervalos de 8 s: inicio 0–8, intermedios 16–24 y 34–42, final 48–56. No son una muestra aleatoria representativa de todo el audio: combinan cobertura temporal con un inicio cuyas hipótesis variaban. No se ejecuta ASR ni se activa ninguna variante del seguidor.

Escuchar el contexto antes de mostrar la comparación. Recorrer los cortes del selector y escuchar cada ventana antes de juzgar su hipótesis. Una trabada fuera del recorte de 4 s no ha sido eliminada por el ASR: no estaba en esa entrada. La clasificación resume los cortes revisados del fragmento; las notas pueden precisar el corte o la palabra.

Las categorías son descriptivas, no diagnósticas. Se admite duda, sin forzar conteos silábicos ni transcripción literal. Marcar cada fragmento revisado y pulsar Guardar revisión; también pueden guardarse avances parciales. Navegar entre fragmentos conserva el formulario en memoria, pero hay que guardar antes de cerrar o recargar.

Destino: datos/anotaciones/lectura_02_trabadas_revision_cualitativa.json. Guarda huella del WAV, huellas de los dos registros de ronda 1 e intervalos del servidor; las actualizaciones conservan copia previa en datos/anotaciones/copias, ignorada por Git. No toca el audio ni el ASR original.

Es revisión del propio lector con acceso a hipótesis, no revisión independiente, anotación de límites de palabras ni referencia completa para WER o detección de todas las disfluencias. Tras guardar, el asistente comprobará la integridad y resumirá las observaciones del usuario por separado de sus propios diagnósticos.
