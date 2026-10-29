# Viabilidad del prototipo en tablets de gama media y baja

Comprobación documental del 26/10/2026. Se recalculan métricas de JSON existentes, sin nuevas inferencias, modificaciones de modelos ni pruebas en tablets.

## Dictamen

El proyecto es plausible para uso desde tablets modestas si estas capturan el audio y muestran los resultados de un motor alojado en un ordenador del aula o servidor. Esa arquitectura aún no está implementada ni validada. El alcance de un único lector activo reduce la concurrencia por clase, aunque no elimina el coste de las actualizaciones repetidas ni el de varias clases simultáneas.

No hay evidencia suficiente para dar por viable la ejecución íntegramente local y en directo en tablets de gama media/baja. Faster Whisper Small int8 es un candidato para estudiar una adaptación móvil; CrisperWhisper Small con Transformers float32 y los ajustes actuales no es una base razonable para exigir funcionamiento local en dispositivos de 3–4 GB. Incluso con 6–8 GB queda por demostrar memoria disponible, respuesta sostenida y consumo. Esto es un juicio sobre las implementaciones medidas, no una imposibilidad de optimizar estos modelos.

## Evidencia de las ejecuciones

Equipo registrado: Intel Core i7-11800H, 16 procesadores lógicos, 15,71 GiB de RAM física utilizable por Windows. Ambos motores usan CPU y cuatro hilos. La RTX 3050 no ejecuta el reconocimiento. La CPU acumulada dividida por la inferencia equivale aproximadamente a cuatro núcleos lógicos ocupados en ambos motores; un porcentaje cercano al 25 % de este equipo no significa una carga ligera trasladable a una tablet.

| Ensayo | Motor y precisión | Audio enviado (s) | Inferencia total (s) | RTF agregado | Carga única (s) | Pico residente de vida del proceso (MiB) | Máximo muestreado de commit privado (MiB) |
|---|---|---:|---:|---:|---:|---:|---:|
| 17 audios, 25/10 | Faster Whisper Small, int8 | 880,00 | 131,50 | 0,149 | 2,17 | 980,84 | 3.418,83 |
| Mismos 17 audios | CrisperWhisper Small, float32 | 880,00 | 426,57 | 0,485 | 18,91 | 4.466,64 | 5.600,49 |
| 6 audios de la caja, 26/10 | Faster Whisper Small, int8 | 670,00 | 99,14 | 0,148 | 1,25 | 970,42 | 3.416,44 |
| Mismos 6 audios completos | CrisperWhisper Small, float32 | 670,00 | 213,46 | 0,319 | 15,80 | 5.057,56 | 5.988,19 |
| 6 audios con final VAD | CrisperWhisper Small, float32 | 419,01 | 118,86 | 0,284 | 7,60 | 4.435,11 | 5.592,46 |

Fuentes, relativas a la raíz del proyecto:

- `resultados/literalidad/20261025_182446_557677_UTC/{baseline,candidato}.json`.
- `resultados/literalidad/20261026_081747_630720_UTC/{baseline,candidato}.json`.
- `resultados/literalidad/20261026_082404_701027_cola_vad_UTC/candidato.json`.

RTF = suma de tiempos de inferencia / suma de duración enviada, incluido silencio. No incluye carga, captura, interfaz, red ni todo el tratamiento de entrada; el VAD del último ensayo se reutiliza de un diagnóstico anterior. No son ensayos pareados repetidos. El pico residente incluye carga/importaciones y pertenece a toda la vida de cada proceso. El commit privado es memoria comprometida, que puede estar residente o respaldada por paginación: no se suma al working set ni representa una necesidad física idéntica en Android. Su tamaño sí impide interpretar «pico de 981 MiB» como «basta una tablet de 1 GB». La aplicación y el sistema operativo necesitan margen adicional.

Recortar el final reduce trabajo, pero mantiene el candidato alrededor de 4,33 GiB residentes de pico y 5,46 GiB de commit muestreado. En los seis audios completos alcanzó 4,94 GiB residentes y 5,85 GiB de commit. No hay evidencia de que el VAD resuelva el coste de alojar el modelo.

## El tiempo real es una exigencia distinta

Una transcripción completa más rápida que el audio no acredita seguimiento mientras se lee. En el lote de 17 audios el RTF por archivo del candidato varió entre 0,257 y 1,444: hubo una entrada que ya tardó más que su duración en este PC.

La comparación guardada `resultados/comparaciones/20261021_100926_258927` ejecuta el motor habitual sobre una lectura con lluvia en tres rondas, con bloques de 2 s:

| Ventana | Actualizaciones | Media inferencia (s) | P95 (s) | Máximo (s) | Inferencias mayores de 2 s | Cola máxima simulada (s) |
|---|---:|---:|---:|---:|---:|---:|
| 4 s | 60 | 1,198 | 1,656 | 1,740 | 0 | 0 |
| 8 s | 60 | 1,802 | 1,860 | 10,512 | 3 | 8,512 |

Son tres rondas de una grabación, no 60 lecturas independientes. No se midió RAM/CPU en esta comparación histórica. La ventana de 4 s tiene un margen de solo 0,344 s respecto al bloque en su P95 de inferencia, antes de incorporar el resto de la aplicación. Si cada inferencia tardara el doble, su media superaría 2 s y generaría cola; es un escenario aritmético, no una predicción del rendimiento de una tablet. Reducir ventana exige revisar también precisión y recuperación de relecturas.

## Traducción a dispositivos modestos

Como referencia de capacidades, no como inventario del alumnado, Samsung publicó Galaxy Tab A9/A9+ con 4 u 8 GB y Xiaomi especifica Redmi Pad SE con 4/6/8 GB y Snapdragon 680. Los fabricantes advierten de diferencias por mercado y memoria ocupada por el software. Fuentes oficiales consultadas el 26/10/2026: [Samsung](https://news.samsung.com/mx/samsung-galaxy-tab-a9-y-galaxy-tab-a9-entretenimiento-y-productividad-al-alcance-de-todos), [Xiaomi](https://www.mi.com/ke/product/redmi-pad-se/specs/).

| RAM física nominal | Motor habitual local | Candidato literal actual local |
|---|---|---|
| 2–3 GB, escenario de dispositivos limitados | No dar compatibilidad por supuesta; adaptación y medición imprescindibles | Descartarlo como objetivo para esta implementación |
| 4 GB | Memoria ajustada según los registros de Windows; velocidad desconocida | No razonable: el pico residente observado ya supera la RAM total nominal |
| 6–8 GB | Plausible para investigar, sin garantía de respuesta sostenida | Podría haber margen de memoria en algunos equipos; no hay validación de fluidez, estabilidad o batería |
| Tablet como cliente de un motor central | Arquitectura plausible para probar | Arquitectura plausible; el coste del candidato se traslada al equipo central |

Ni el número de núcleos ni los GHz permiten convertir directamente los tiempos del i7 a un SoC móvil. Tampoco se puede contar con aceleración GPU/NPU automática. CTranslate2 documenta soporte ARM64, pero sus paquetes Python publicados enumeran Linux, macOS y Windows; eso no acredita una instalación directa de este proyecto en Android o iPadOS. Haría falta una integración móvil y comprobar backend y operadores efectivos: [hardware](https://opennmt.net/CTranslate2/hardware_support.html), [instalación](https://opennmt.net/CTranslate2/installation.html).

## Decisión práctica y prueba de aceptación

La vía prioritaria para el objetivo escolar es un cliente ligero en cada tablet, reconocimiento en un ordenador del aula o servidor y un único flujo de lector por clase. El motor habitual puede servir para explorar el seguimiento; el candidato literal puede evaluarse como análisis posterior si su conservación de intentos lo justifica. No está demostrada todavía su calidad suficiente: persisten intentos omitidos y otros errores. No elegir un motor solo por velocidad.

Con PCM16 mono a 16 kHz, el audio sin comprimir representa 32.000 bytes/s, 256 kbit/s y 1,92 MB/min por lector, antes de protocolos. Son valores calculados del formato, no consumo de red medido; la captura nativa puede usar otro formato. Hay que medir Wi-Fi del aula, reconexiones, orden de turnos y demora completa. Un servidor local permitiría ensayar sin depender de Internet, pero requiere implementar esa ruta.

Antes de declarar compatibilidad:

1. Identificar al menos la tablet más limitada del centro y otra representativa: modelo, SoC, RAM física, SO y memoria disponible. Si hay Android e iPad, probar ambas plataformas.
2. Ejecutar en la arquitectura elegida sesiones de 20–30 minutos con pantalla, micrófono e interfaz activos; registrar arranque frío/caliente, memoria máxima con la métrica de esa plataforma, cierres, calentamiento y batería. Mantener condiciones de comparación constantes y repetir.
3. Para bloques de 2 s, exigir que el procesamiento sostenido no produzca una cola creciente. Como objetivo provisional, P95 de inferencia ≤1 s deja margen para captura, red e interfaz; es un criterio de ingeniería propuesto, no un umbral ya validado con docentes. Registrar también máximos y demora real desde voz hasta pantalla, porque un P95 bueno puede ocultar bloqueos.
4. Repetir normales, pausas, ruido, relecturas e intentos con referencias humanas compatibles; comparar calidad antes y después de cuantizar, reducir modelo o cambiar backend. Las grabaciones adultas actuales no validan lectura infantil.
5. En remoto, medir por separado cliente y servidor, probar cambios/pausas de turno y desconexiones, y dimensionar por clases activas simultáneas. Un lector por clase no equivale a un lector en todo el centro.

Conclusión: uso desde tablets modestas, plausible con procesamiento central; funcionamiento local universal en esas tablets, no acreditado; candidato literal float32 local, demasiado pesado como objetivo actual de gama baja. La siguiente evidencia decisiva es una sesión sostenida en el dispositivo mínimo real, con el recorrido completo de audio a pantalla.
