# Diagnóstico del pico del corte 22 s

Nuevas inferencias instrumentadas sobre el mismo WAV; no son los tiempos originales. Modelo CPU int8 cargado una vez por ejecución. Orden aleatorio por ronda, sin calentamiento excluido. Cambian la carga de CPU y el coste de instrumentación; no comparar las cifras como benchmark emparejado. Sin cambio de reglas ni configuración habitual.

| Configuración | Ventana | Corte | Total medio (s) | Rango (s) | Generación media (s) | Intentos por llamada |
|---|---:|---:|---:|---|---:|---|
| Habitual | 4 | 20 | 2.17 | 2.05-2.33 | 0.40 | [[0], [0], [0]] |
| Habitual | 4 | 22 | 2.15 | 2.06-2.22 | 0.49 | [[0], [0], [0]] |
| Habitual | 4 | 24 | 2.14 | 2.11-2.19 | 0.42 | [[0], [0], [0]] |
| Habitual | 8 | 20 | 2.60 | 2.36-3.06 | 0.73 | [[0], [0], [0]] |
| Habitual | 8 | 22 | 13.04 | 11.84-13.86 | 11.29 | [[0, 0.2, 0.4], [0, 0.2, 0.4], [0, 0.2, 0.4]] |
| Habitual | 8 | 24 | 2.45 | 2.31-2.67 | 0.61 | [[0], [0], [0]] |
| Solo temperatura 0 | 4 | 22 | 2.14 | 2.12-2.19 | 0.47 | [[0], [0], [0]] |
| Solo temperatura 0 | 8 | 22 | 6.32 | 6.30-6.35 | 2.89 | [[0, 0], [0, 0], [0, 0]] |

## Mecanismo observado

En las tres rondas habituales de ventana 8 s/corte 22 s hay tres llamadas de generación: temperaturas 0, 0,2 y 0,4. La primera y segunda exceden el umbral de razón de compresión 2,4, por repetición excesiva; no fallan por log-probabilidad inferior a -1. El intento a 0,4 queda por debajo del umbral. El encoder y el alineamiento temporal son mucho más baratos que el conjunto de generación en ese corte.

La primera ronda genera inicialmente texto repetitivo con razón 2,552; el segundo intento llega a 2,679; el tercero a 1,078. Son heurísticas internas de repetición, no porcentajes de certeza ni mediciones del lector.

La ablación temperature=0 desactiva temperaturas alternativas, pero no garantiza una sola generación por llamada: en 8 s aparecen dos llamadas a temperatura 0 porque el procesamiento recorre más de un segmento/paso. Su salida conserva repeticiones de Ana llamó… y Después de un momento, la gente se volvió a ver a Ana, texto ajeno al cuento. No se recomienda activarla.

La instrumentación muestra dónde se consume el tiempo en estas nuevas ejecuciones. Los registros originales no guardaban intentos internos: no se puede reconstruir retrospectivamente su número exacto. El hallazgo no identifica la causa acústica inicial ni permite culpar a la lluvia. El corte y contexto influyen; no se ha comparado la misma señal con/sin lluvia.

## Ejecuciones

- Habitual: resultados/diagnostico_inferencia/20261021_101852_059105/resumen.json (18 llamadas, 3 rondas de cortes 20/22/24 y ventanas 4/8).
- Ablación: resultados/diagnostico_inferencia/20261021_102019_524726/resumen.json (6 llamadas, corte 22 y ventanas 4/8).

Sin cambios en seguir.py ni comparación de posiciones del seguidor en esta prueba. No se calcula precisión lexical, tasa de error ni latencia de pantalla. Pendiente de ejecución compartida.

<!-- identidad-audio-inicio -->
## Audio utilizado

- **Lectura normal con lluvia · cuento 1 · 21/10/2026** — Lectura normal con lluvia - cuento 1 - 21-10-2026.wav
<!-- identidad-audio-fin -->
