# Primera revisión del lote por el asistente

Sin transcripción literal ni anclas temporales nuevas. No mide exactitud, WER ni latencia visible. No se activan reglas experimentales.

| Audio | Total medio ASR 4 s | Total medio ASR 8 s | Finales 4 s / 8 s | Mayor cola 4 s / 8 s |
|---|---:|---:|---|---|
| Lectura lenta - cuento 2 · 23/10/2026 | 68.25 s | 70.89 s | [56, 56, 56] / [56, 56, 56] | 7.18 / 3.42 s |
| Lectura rápida - cuento 2 · 23/10/2026 | 17.15 s | 23.72 s | [56, 56, 56] / [56, 56, 56] | 0.19 / 2.71 s |
| Lectura pausa con relectura barco rojo / el barco - cuento 2 · 23/10/2026 | 34.20 s | 47.68 s | [56, 56, 56] / [56, 56, 56] | 0.01 / 4.31 s |
| Lectura sustitución rojo por azul - cuento 2 · 23/10/2026 | 27.70 s | 40.38 s | [56, 56, 56] / [56, 56, 56] | 0.47 / 10.54 s |
| Lectura con ruido de fondo - cuento 2 · 23/10/2026 | 26.69 s | 35.42 s | [56, 56, 56] / [56, 56, 56] | 0.00 / 7.64 s |
| Lectura con muchas trabadas - cuento 2 · 23/10/2026 | 61.81 s | 63.05 s | [56, 56, 56] / [56, 56, 56] | 9.30 / 10.63 s |
| Lectura omisión abuelo - cuento 2 · 23/10/2026 | 27.42 s | 37.91 s | [56, 56, 56] / [56, 56, 56] | 1.26 / 9.70 s |

## Lectura de los resultados

- Revisar la trayectoria completa: llegar a 56 no demuestra transcripción correcta ni detección de disfluencias.
- Los totales incluyen llamadas sobre silencio: no son duración de habla ni latencia visual. Las colas son simuladas.
- Los máximos y la variación entre rondas se conservan en revision_asistente.json. Las rondas no añaden lectores ni grabaciones.
- Recursos de CPU/RAM/GPU: consultar recursos_computo.md y los JSON dentro de cada carpeta. ASR en CPU int8.
- Comparar con las confirmaciones del lector en pruebas/22_lote_segundo_cuento.md; la transcripción literal de las trabadas queda pendiente.
