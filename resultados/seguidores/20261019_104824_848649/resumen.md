# Comparación de regla de palabra aislada

Experimento de desarrollo sobre hipótesis ASR fijas. Cambia solo el seguidor. ASR, ventanas, cortes y tiempos de inferencia permanecen reutilizados. Las métricas de salida visible son una comparación bajo esos tiempos, no latencia nueva medida. Una mejora en estos audios usados para diseñar la regla no prueba generalización. Variante no activada en seguir.py.

Una sola palabra ASR, al menos cinco caracteres normalizados, coincidencia exacta única en la ventana local y exactamente la siguiente palabra del cuento, con posición previa distinta de cero. El resto conserva el comportamiento original.

| Caso | Ventana | Ronda | Cortes con posición distinta | Aplicación de regla (audio s) | Final original | Final variante |
|---|---:|---:|---:|---|---:|---:|
| normal | 6 | 1 | 0 | [] | 56 | 56 |
| normal | 4 | 1 | 0 | [] | 56 | 56 |
| normal | 8 | 1 | 0 | [] | 56 | 56 |
| normal | 6 | 2 | 0 | [] | 56 | 56 |
| normal | 4 | 2 | 0 | [] | 56 | 56 |
| normal | 8 | 2 | 0 | [] | 56 | 56 |
| normal | 4 | 3 | 0 | [] | 56 | 56 |
| normal | 8 | 3 | 0 | [] | 56 | 56 |
| normal | 6 | 3 | 0 | [] | 56 | 56 |
| desviaciones | 8 | 1 | 0 | [] | 56 | 56 |
| desviaciones | 6 | 1 | 0 | [] | 56 | 56 |
| desviaciones | 4 | 1 | 0 | [] | 56 | 56 |
| desviaciones | 4 | 2 | 0 | [] | 56 | 56 |
| desviaciones | 6 | 2 | 0 | [] | 56 | 56 |
| desviaciones | 8 | 2 | 0 | [] | 56 | 56 |
| desviaciones | 8 | 3 | 0 | [] | 56 | 56 |
| desviaciones | 4 | 3 | 0 | [] | 56 | 56 |
| desviaciones | 6 | 3 | 0 | [] | 56 | 56 |
| pausa | 8 | 1 | 0 | [] | 56 | 56 |
| pausa | 4 | 1 | 0 | [] | 56 | 56 |
| pausa | 8 | 2 | 0 | [] | 56 | 56 |
| pausa | 4 | 2 | 0 | [] | 56 | 56 |
| pausa | 4 | 3 | 0 | [] | 56 | 56 |
| pausa | 8 | 3 | 0 | [] | 56 | 56 |
| lenta | 8 | 1 | 0 | [] | 55 | 55 |
| lenta | 4 | 1 | 2 | [62.0] | 53 | 53 |
| lenta | 8 | 2 | 0 | [] | 55 | 55 |
| lenta | 4 | 2 | 2 | [62.0] | 53 | 53 |
| lenta | 4 | 3 | 2 | [62.0] | 53 | 53 |
| lenta | 8 | 3 | 0 | [] | 55 | 55 |
| relectura | 8 | 1 | 0 | [] | 56 | 56 |
| relectura | 4 | 1 | 0 | [] | 56 | 56 |
| relectura | 8 | 2 | 0 | [] | 56 | 56 |
| relectura | 4 | 2 | 0 | [] | 56 | 56 |
| relectura | 4 | 3 | 0 | [] | 56 | 56 |
| relectura | 8 | 3 | 0 | [] | 56 | 56 |

Los JSON de resumen conservan las métricas humanas por variante y los cortes modificados. En desviaciones solo se compara el comportamiento; no se inventa una referencia temporal. Los registros originales permanecen intactos.
