# Anotador temporal local de Lexia

Primera versión: únicamente la lectura normal. No necesita instalar librerías ni descargar modelos.

## Abrir

Desde la raíz del proyecto, en PowerShell:

```powershell
.\.venv\Scripts\python.exe -u scripts\anotar.py
```

Abrir http://127.0.0.1:8765 en el navegador. Mantener la terminal abierta y cerrarla con Ctrl+C al acabar. --puerto 8766 permite elegir otro puerto; en ese caso abrir la dirección que muestra la terminal. El servidor escucha únicamente en 127.0.0.1 y no activa el micrófono.

## Primera tarea: palabras 1–9

Frase: Una mañana, Ana salió al jardín de su casa.

1. Opcionalmente, cargar el borrador ASR. Contiene tiempos propuestos, ninguno revisado. Si ya aparece Origen: borrador asr, está cargado. El borrador solo está disponible si todas las palabras coinciden con la transcripción humana validada; no es alineamiento temporal humano.
2. Seleccionar Una y pulsar Escuchar fragmento. Comenzar a velocidad normal, usando 0,8×, 0,6× o 0,4× para aclarar límites cuando haga falta. El campo Contexto añade audio de alrededor, que no forma parte del intervalo de la palabra.
3. Ajustar inicio y fin para incluir la palabra completa. La onda ampliada permite clic para inicio y Mayús + clic para fin. También se pueden escribir los segundos, o situarse con el reproductor y pulsar Inicio aquí / Fin aquí.
4. Escuchar otra vez, comprobando la palabra completa y sus vecinos. Si el intervalo es adecuado, marcar Revisada por escucha. Si queda una duda, anotarla y dejar la palabra pendiente.
5. Continuar con Siguiente. Guardar progreso al acabar la primera frase; no hace falta completar las 56 palabras en una sesión.

No separar sonidos a la fuerza por una cuadrícula de centésimas. En habla ligada puede haber límites ambiguos; registrar la duda y usar una convención consistente. Para esta primera referencia los intervalos se mantienen ordenados, con límites compartidos si no hay silencio y huecos cuando lo hay. No permitir solapamientos entre palabras ni tiempos fuera del audio. Marcar una revisión declara una escucha humana; el programa no puede verificar que se haya escuchado.

## Guardado y procedencia

- datos/anotaciones/lectura_normal.json conserva tiempos, estado por palabra, origen y notas.
- Los tiempos ASR permanecen como borrador hasta revisión explícita. Ajustarlos desmarca la revisión de esa palabra.
- Guardar no modifica datos/referencias/lectura_normal.json ni los JSON originales del reconocedor.
- Los guardados posteriores crean copias en datos/anotaciones/copias, excluidas de Git. Cerrar el navegador con cambios no guardados muestra un aviso.
- Recargar la página recupera la anotación guardada. Usar una sola pestaña de anotación para evitar sobrescribir cambios desde otra sesión.
- Aunque todas las palabras estén marcadas revisadas, hará falta comprobar el conjunto antes de utilizarlo como referencia temporal. No se importa automáticamente al evaluador.

La semilla procede de las marcas del mismo reconocedor evaluado; su revisión humana puede tener sesgo de anclaje. Conservar esa procedencia, revisar especialmente bordes y silencios, y plantear una segunda revisión independiente para conclusiones más sólidas.

## Alcance y comprobaciones

Reproducción por fragmentos con contexto opcional, velocidad, repetición, onda general/ampliada, selección de palabra, edición de límites, notas y progreso. Validación de identidad de audio/texto, tiempos, orden y revisión. El guardado es local, separado de las referencias y con copia anterior.

17 pruebas automáticas pasan. Se comprobó en navegador carga de audio/onda, borrador, reproducción de un fragmento, guardado y recuperación. Durante la comprobación técnica se guardó un borrador con cero palabras revisadas; no se validó temporalmente ninguna palabra del usuario.

Primera versión limitada a la lectura normal. Repeticiones y fragmentos requerirán una extensión que conserve cada intento con su índice del cuento e intervalo propio. No reutilizar esta interfaz sin esa adaptación para anotar los demás casos.
