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
- Aunque todas las palabras estén marcadas revisadas, hace falta comprobar el conjunto antes de utilizarlo como referencia temporal. El guardado no lanza ninguna evaluación. Tras la revisión completa del usuario y la comprobación estructural se puede ejecutar explícitamente scripts.evaluar_seguimiento para el caso normal, conservando procedencia y límites ambiguos. No modifica los JSON de datos/referencias.

La semilla procede de las marcas del mismo reconocedor evaluado; su revisión humana puede tener sesgo de anclaje. Conservar esa procedencia, revisar especialmente bordes y silencios, y plantear una segunda revisión independiente para conclusiones más sólidas.

## Alcance y comprobaciones

Reproducción por fragmentos con contexto opcional, velocidad, repetición, onda general/ampliada, selección de palabra, edición de límites, notas y progreso. Validación de identidad de audio/texto, tiempos, orden y revisión. El guardado es local, separado de las referencias y con copia anterior.

17 pruebas automáticas pasan. Se comprobó en navegador carga de audio/onda, borrador, reproducción de un fragmento, guardado y recuperación. Durante la comprobación técnica se guardó un borrador con cero palabras revisadas; no se validó temporalmente ninguna palabra del usuario.

El modo normal conserva las 56 palabras. Los modos siguientes revisan solo intervalos seleccionados, en archivos separados; no presentan una lista completada como anotación de todo el audio.

## Fragmentos clave

```powershell
.\.venv\Scripts\python.exe -u scripts\anotar.py --caso pausa --puerto 8767
```

Abrir http://127.0.0.1:8767. Seleccionar cada elemento, escuchar la zona de orientación y marcar inicio/final con los campos, la onda o Inicio aquí / Fin aquí. Escuchar de nuevo el fragmento delimitado, marcar Revisado por escucha y guardar. Se mantiene la velocidad 0,4×. Las zonas de orientación no son propuestas de límites ni cuentan como anotación: los tiempos comienzan vacíos.

- pausa: flor antes de la pausa (27), Ana al retomar (28), cuaderno (56). La pausa se podrá medir entre el final de flor y el inicio de Ana, sin inventar sus límites a partir del ASR.
- lenta: Después (46), mariposa de la última frase (53), un (55), cuaderno (56). Sirven para revisar recuperación y final; no permiten evaluar posiciones en todo el audio.
- relectura: frase completa Los dos se quedaron en silencio, intento 1 e intento 2 (ambos 37–42), y mirando (43). Cada intento conserva un intervalo cronológico independiente, aunque vuelva al mismo tramo del cuento. Los límites de la frase no permiten asignar tiempos a sus seis palabras interiores.

Para cambiar de caso, parar el proceso con Ctrl+C y arrancar el mismo comando con --caso lenta o --caso relectura. Guardar antes de recargar. Los archivos son datos/anotaciones/lectura_pausa_fragmentos.json, lectura_lenta_fragmentos.json y lectura_relectura_fragmentos.json, con copias anteriores separadas. No se sobrescribe lectura_normal.json.

El evaluador de lectura normal no consume estos intervalos; la evaluación de eventos se hará explícitamente cuando estén revisados. En el formato compartido, words contiene los elementos editables, pero annotation_kind=selected_intervals, story_range y attempt indican que son intervalos de cobertura parcial; reviewed_intervals cuenta elementos, no palabras. Solo se permiten tiempos ordenados, sin solapamiento y dentro del audio. La validación estructural no sustituye la escucha.

Tras revisar las tres anclas del caso pausa, se pueden contrastar con sus seis registros existentes sin repetir inferencias:

```powershell
.\.venv\Scripts\python.exe -m scripts.evaluar_pausa resultados/comparaciones/20261014_111548_094194
```

Genera evaluacion_pausa.json/md: duración entre flor y Ana, posiciones por corte dentro de la pausa, posición visible simulada, primer avance después de retomar y demora final. La demora del primer avance se mide desde el final de Ana, pero no implica reconocer precisamente Ana: el seguidor puede saltar a una posición posterior. No se extrapola la posición humana fuera de la pausa ni se clasifica toda hipótesis no vacía como alucinación.

Tras revisar las cuatro anclas de lectura lenta:

```powershell
.\.venv\Scripts\python.exe -m scripts.evaluar_lenta resultados/comparaciones/20261016_095252_869489
```

Genera evaluacion_lenta.json/md reutilizando las seis ejecuciones existentes. Entre anclas solo acota la posición posible sin asignar tiempos a palabras no anotadas; tras el final de cuaderno la referencia es 56. Conserva tanto la primera llegada al final como los retrocesos posteriores, y separa el corte de audio de la demora simulada de procesamiento. No calcula un error medio de todo el audio a partir de cuatro palabras.

Tras revisar los dos intentos completos y mirando:

```powershell
.\.venv\Scripts\python.exe -m scripts.evaluar_relectura resultados/comparaciones/20261016_104206_415649
```

Genera evaluacion_relectura.json/md con los cortes próximos a ambos intentos, movimiento del seguidor, salidas listas simuladas y posición visible. No asigna tiempos a las palabras interiores ni considera que un retroceso de una palabra demuestre seguimiento completo de la relectura. Distingue una hipótesis calculada con audio de la relectura de una salida disponible mientras el lector aún la realiza.

Comprobación de esta extensión: 23 pruebas automáticas pasan y app.js supera node --check. Revisión visual y de uso del nuevo modo pendiente del usuario.
