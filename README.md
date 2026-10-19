# Prototipo de lectura asistida

Trabajo inicial de prácticas y TFG: reconocimiento, seguimiento y evaluación de lectura oral en español.

El objetivo final es la lectura asistida en grupo: la profesora selecciona al lector desde su tablet y solo se habilita el micrófono de ese alumno. Puede pausar la sesión para explicaciones u otras interrupciones, excluyendo ese intervalo del tiempo de lectura activa. Este control de turnos y pausa está definido en [el alcance](ALCANCE.md) y pendiente de implementación; el prototipo actual trabaja con un lector y audio local.

## Estado actual

- Grabación de audio local en WAV.
- Transcripción posterior con Whisper small, faster-whisper y CPU int8.
- Registro de palabras, tiempos estimados y duración de procesamiento en JSON.
- Alineamiento global posterior con el cuento e informes de diferencias candidatas.
- Simulación de seguimiento por prefijos crecientes de audio, con historial de hipótesis y posición provisional.
- Dos grabaciones adultas de depuración y resultados de las primeras pruebas.
- Seguimiento incremental, subrayado y evaluación automática pendientes.

La segunda prueba conserva una repetición y una omisión, pero elimina un intento truncado y sustituye silencio por cinesio según la referencia del lector. Los resultados no validan funcionamiento con alumnos ni puntuación de pronunciación.

## Documentación

- [Investigación sobre necesidades de logopedas y docentes](docs/Investigacion_necesidades_logopedas_docentes.md).

- [Diario de desarrollo y experimentación](docs/DIARIO_DESARROLLO.md).
- [Informe de investigación](docs/Informe%20Lectura%20Asistida%20Prototipo.md).
- [Alcance inicial](ALCANCE.md).
- [Guía de primera prueba](EMPEZAR.md).
- [Prueba 01](pruebas/01_lectura_normal.md).
- [Prueba 02](pruebas/02_lectura_con_disfluencias.md).
- [Seguimiento progresivo](pruebas/03_seguimiento_progresivo.md).
- [Primera comparación de ventanas](pruebas/04_comparacion_ventanas.md).
- [Experimento ampliado de ventanas](pruebas/05_ventanas_ampliadas.md).
- [Pausa y protocolo de relectura](pruebas/06_protocolo_pausas_relecturas.md).
- [Lectura lenta: bloqueos y regresión](pruebas/07_lectura_lenta.md).
- [Relectura de una frase](pruebas/08_relectura_frase.md).
- [Referencias humanas del banco](datos/referencias/LEEME.md).
- [Reproductor de anotación temporal](herramientas/anotador/LEEME.md).

## Instalación reproducible en Windows

Con Python 3.12 instalado, desde la raíz del repositorio:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-lock.txt
.\.venv\Scripts\python.exe scripts\preparar_modelo.py
```

El último comando descarga el modelo. Para grabar y transcribir:

```powershell
.\.venv\Scripts\python.exe scripts\grabar.py --segundos 40
.\.venv\Scripts\python.exe scripts\transcribir.py
```

Para reproducir la segunda prueba sin grabar:

```powershell
.\.venv\Scripts\python.exe scripts\transcribir.py datos\audio\lectura_20261014_082953_219058.wav
```

## Alineamiento con el cuento

```powershell
.\.venv\Scripts\python.exe scripts\alinear.py
```

Usa la última transcripción de resultados, o pasa la ruta de un JSON concreto. El parámetro --cuento permite elegir otro TXT. Se generan informes Markdown y JSON en resultados/alineamientos.

El método es distancia de edición global con costes unitarios. Conserva índices globales desde 1 y tiempos ASR. Ignora caja y puntuación, pero conserva tildes y ñ. Las inserciones que duplican un fragmento contiguo se etiquetan como repeticiones candidatas; otras ambigüedades requieren revisión.

Primera prueba: 56 coincidencias. Segunda prueba: 54 coincidencias, una repetición candidata, una omisión candidata y una sustitución candidata. No recupera mari… porque ese fragmento no está en la salida del reconocedor. No califica la lectura ni demuestra seguimiento en directo.

Comprobaciones del alineador:

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

## Seguimiento progresivo experimental

```powershell
.\.venv\Scripts\python.exe -u scripts\seguir.py
```

Procesa el último WAV en cortes de dos segundos. El modelo solo recibe el prefijo disponible. El seguidor utiliza las últimas ocho palabras ASR, una ventana local y recuperación con confirmación; admite retrocesos. Guarda historial JSON e informe Markdown en resultados/seguimiento. Usa VAD, por lo que las hipótesis pueden diferir de las transcripciones anteriores sin VAD.

La posición representa la última palabra apoyada por coincidencia textual; no mide palabra actual ni corrección lectora. El procesamiento repetido de prefijos es una base experimental, no streaming nativo. La cola secuencial estimada no incluye carga del modelo, captura ni pantalla. No se evalúa precisión temporal sin referencia humana. Grabaciones limitadas a 120 segundos.

## Comparación experimental de ventanas

```powershell
.\.venv\Scripts\python.exe -u scripts\comparar_ventanas.py
```

Compara prefijo acumulado, ventana de 6 s y ventana de 10 s en el último audio, manteniendo bloques de 2 s y las mismas opciones del modelo y seguidor. Usa --todos para las dos grabaciones. Guarda registros y un resumen en resultados/comparaciones. También se puede ejecutar seguir.py --ventana 6. Los timestamps de cada ventana se trasladan al reloj global; se mantiene posición del cuento sin concatenar palabras de ventanas solapadas.

Son tiempos orientativos de una ejecución por configuración, no un benchmark con repeticiones. La posición del prefijo tampoco es una referencia humana de precisión. No hay medición de latencia visual ni evaluación de errores lectores.

Experimento ampliado configurable (cinco ventanas, prefijo y dos rondas):

```powershell
.\.venv\Scripts\python.exe -u scripts\comparar_ventanas.py --ventanas 0 4 6 8 10 12 --repeticiones 2
```

Cada ronda ejecuta las configuraciones en orden aleatorio reproducible, sin competir por CPU. El informe conserva el plan, semilla, resultados por ronda y medias/rangos. Los valores predeterminados son 0, 6 y 10 s, una ronda. El 0 significa prefijo completo, las demás duraciones son ventanas con solapamiento igual a duración menos 2 s. Dos rondas no validan precisión ni generalización infantil.

## Archivos conservados

Se incluyen código, dependencias, documentación, texto, grabaciones adultas de prueba y resultados. El entorno Python, las herramientas descargadas y el modelo quedan fuera de Git porque se pueden reconstruir. No se incluyen credenciales ni grabaciones infantiles.

Los JSON existentes conservan las rutas locales de origen como metadatos; al reproducir una prueba, pasa la ruta relativa de su WAV. Los tiempos por palabra de las transcripciones ASR son estimaciones automáticas. La revisión humana se guarda por separado en datos/anotaciones, con procedencia y notas sobre límites ambiguos. El tiempo de procesamiento posterior no mide la latencia del futuro subrayado.

## Evaluación con marcas revisadas

Tras completar una comparación de la lectura normal, ejecutar (sustituir CARPETA por la carpeta generada):

```powershell
.\.venv\Scripts\python.exe -m scripts.evaluar_seguimiento resultados/comparaciones/CARPETA
```

Genera evaluacion_humana.json y evaluacion_humana.md. Compara la última palabra terminada según la revisión humana con la posición estimada en cada corte de 2 s durante la lectura. Separa el error de la hipótesis del error de la posición visible en una simulación secuencial con cola. Excluye el silencio posterior de las medias y registra la demora simulada hasta alcanzar la palabra final. No mide latencia real de pantalla ni califica al lector. Solo admite el caso normal con todas sus palabras revisadas; no interpreta relecturas ni omisiones mediante esta referencia.

## Corrección del entorno

Se fija PyAV 16.0.1: la combinación inicial de faster-whisper 1.2.1 y PyAV 19.0.1 fallaba al abrir archivos con el parámetro metadata_errors. Tras corregirla se procesó correctamente el WAV real de la primera prueba.
