# Revisión humana de otros lectores

Desde la raíz del proyecto:

```powershell
.\.venv\Scripts\python.exe -u -m scripts.revisar_lectores --puerto 8783
```

Abrir http://127.0.0.1:8783/ y mantener el servidor activo. Selección de WAV presentes y catalogados por huella, excluyendo lector_01. No ejecutar ASR ni importar resultados automáticos. El audio original se sirve localmente sin modificarlo, con soporte para desplazamiento y velocidad reducida.

Primero escuchar la toma completa, indicar si termina el texto y si se entiende, marcar incidencias y guardar. Se puede dejar la referencia literal pendiente y continuar después. La segunda fase transcribe lo realmente pronunciado, con intentos parciales, repeticiones, autocorrecciones y marcadores explícitos de fragmentos dudosos/voces ajenas. El cuento está oculto por defecto para evitar copiar la lectura prevista como referencia de lo ocurrido. Tiempos de eventos orientativos, sin pedir alineamiento palabra por palabra.

Guardar crea o actualiza datos/anotaciones/revision_lectores/ID.json, ligado a huellas del WAV y cuento. No marca automáticamente ninguna revisión como completada ni modifica referencias previas o catálogo. Cambiar de toma guarda los cambios pendientes; al cerrar la pestaña se avisa si hay cambios sin guardar. Las versiones anteriores quedan en datos/anotaciones/copias, fuera de Git. Anotaciones humanas pendientes hasta que el usuario escuche y confirme; no equivalen a validación independiente. No incluir datos personales en campos libres. Este visor no publica nada; las voces de otros lectores siguen excluidas de Git aunque sus resultados anónimos sean publicables previa revisión.
