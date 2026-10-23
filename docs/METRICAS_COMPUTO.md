# Métricas para comparar configuraciones y preparar pruebas en tablets

## Qué se registra desde esta versión

| Bloque | Métricas | Alcance |
|---|---|---|
| Equipo | SO, arquitectura, versión Python, CPU, procesadores lógicos, RAM total/disponible, GPU NVIDIA/driver/VRAM total | Equipo que ejecuta la prueba; no sustituye ficha de la tablet |
| Configuración | Modelo, tamaño del modelo en disco, precisión solicitada, CPU o CUDA, versiones, VAD, ventana, bloque | ASR habitual sigue en CPU int8; no se activa CUDA |
| Rendimiento | Carga del modelo; inferencia por actualización, total, mediana, P95, máximo, RTF; llamadas que exceden bloque; cola y salida lista simuladas | RTF del reprocesamiento sobre audio completo, incluido silencio; no es latencia visual |
| CPU | Tiempo CPU del proceso por inferencia y total, utilización media durante ejecución | Incluye hilos Python/nativos y muestreo; no otros procesos ni CPU de nvidia-smi. 100% de un procesador lógico puede superarse; normalización por capacidad lógica se muestra aparte |
| RAM | Working set muestreado, máximo de muestras, commit privado, pico working set de vida del proceso; RAM disponible del equipo | El pico de vida incluye importación/carga, no solo inferencia. Muestreo puede perder picos breves |
| GPU | Utilización, VRAM usada, potencia W, temperatura; mínimos/medias/máximos de muestras | NVIDIA, GPU completa del equipo; incluye otras aplicaciones. No atribuir al ASR. Si no hay sensor/driver: no disponible |
| Entrada | Duración, frecuencia/canales de entrada ASR, pico y RMS dBFS de señal completa | Mezcla voz, ruido y silencio; no es SNR ni calidad percibida |
| Seguimiento | Posiciones, movimientos, recuperaciones, conservación del final y anclas humanas cuando existen | Se conservan evaluadores actuales; finalizar bien no acredita todas las palabras |

RAM/CPU se consultan aproximadamente cada 0,25 s; la GPU aproximadamente cada segundo, con intervalos reales registrados. La consulta GPU puede retrasar el siguiente muestreo. Los máximos son de muestras, no máximos continuos garantizados. La carga del modelo se mide separadamente. Las medidas de recursos incluyen la ejecución y su monitor; la consulta inicial del inventario queda fuera del tramo monitorizado. La salida secuencial simulada conserva su definición de inferencias; no incluye captura, escritura, interfaz ni todo el coste del monitor.

El muestreo consume recursos. Mantenerlo igual en las configuraciones comparadas. Para contrastar su efecto se admite --sin-recursos en seguir.py/comparar_ventanas.py; CPU por inferencia sigue disponible, pero el muestreo de recursos se desactiva. No mezclar resultados con y sin instrumentación como si fueran condiciones idénticas.

No se miden FLOPs, energía específica del ASR en julios, batería atribuible al ASR ni temperatura CPU. Se guardan como no disponibles, no como cero. Los vatios del sensor GPU son potencia del equipo/GPU, no energía específica ni consumo de la tablet.

## Resultados históricos

Se añade recursos_computo.json/md a carpetas con fuentes ASR identificables. Se derivan tiempos/RTF/configuración que ya estaban guardados. CPU/RAM/GPU no instrumentadas permanecen no medidas. Los JSON originales no se reescriben ni se invalidan sus hashes; los resúmenes Markdown enlazan/incluyen la ficha. En comparaciones de variantes se reutilizan recursos del ASR de origen, no se presentan como una nueva medición de cada seguidor. Los recursos del código de reproducción no están medidos aquí.

Para actualizar solo una carpeta sin ejecutar ASR:

```powershell
.\.venv\Scripts\python.exe -m scripts.informar_recursos resultados/relectura_lejana/20261021_115941_383989
```

Para todas las carpetas compatibles y un inventario del equipo en este momento:

```powershell
.\.venv\Scripts\python.exe -m scripts.informar_recursos --todos --inventario
```

El inventario actual se guarda por separado en resultados/recursos_equipo; no se traslada retrospectivamente a pruebas anteriores. NVIDIA ausente/no disponible no equivale a ausencia de GPU.

## Comprobaciones realizadas

63 pruebas pasan, incluidas cuatro sobre métricas: no inventar telemetría histórica, separar GPU global de CPU para ASR, no modificar JSON originales y actualización idempotente, RTF/CPU sin convertirlos en latencia.

Prueba técnica adicional en resultados/verificacion_recursos: prefijo de 8 s de una grabación existente, cuatro inferencias en CPU, con monitor de memoria y GPU. Verifica que hay muestras reales y CPU por corte. No es otra lectura ni un experimento de precisión ni una prueba de tablet. No se utiliza su RTF/memoria como benchmark representativo.

## Al llevarlo a tablets

Registrar modelo de tablet, SO, backend/acelerador realmente usado, precisión y si el reconocimiento es local o remoto. Medir allí tiempo de arranque, respuesta sostenida, RAM máxima, batería/energía y calentamiento durante sesiones largas. En remoto, separar recursos del servidor y tiempos/red/recursos del cliente. No extrapolar la RTX 3050 del ordenador a una GPU móvil ni su consumo.

Quedan pendientes las mediciones de dispositivo de destino y la respuesta visual en directo; no se inventan valores a partir de este PC. Las estadísticas de calidad deben seguir contrastándose con las mismas grabaciones y referencias humanas, sin elegir solo la configuración más rápida.
