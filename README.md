# Prototipo de lectura asistida

Trabajo inicial de prácticas y TFG: reconocimiento, seguimiento y evaluación de lectura oral en español.

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

- [Diario de desarrollo y experimentación](docs/DIARIO_DESARROLLO.md).
- [Informe de investigación](docs/Informe%20Lectura%20Asistida%20Prototipo.md).
- [Alcance inicial](ALCANCE.md).
- [Guía de primera prueba](EMPEZAR.md).
- [Prueba 01](pruebas/01_lectura_normal.md).
- [Prueba 02](pruebas/02_lectura_con_disfluencias.md).

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

## Archivos conservados

Se incluyen código, dependencias, documentación, texto, grabaciones adultas de prueba y resultados. El entorno Python, las herramientas descargadas y el modelo quedan fuera de Git porque se pueden reconstruir. No se incluyen credenciales ni grabaciones infantiles.

Los JSON existentes conservan las rutas locales de origen como metadatos; al reproducir una prueba, pasa la ruta relativa de su WAV. Los tiempos por palabra son estimaciones del ASR, no anotaciones humanas. El tiempo de procesamiento posterior no mide la latencia del futuro subrayado.

## Corrección del entorno

Se fija PyAV 16.0.1: la combinación inicial de faster-whisper 1.2.1 y PyAV 19.0.1 fallaba al abrir archivos con el parámetro metadata_errors. Tras corregirla se procesó correctamente el WAV real de la primera prueba.
