# Recuperación global exacta

Variante experimental sobre la combinación. Mismos ASR, cortes y tiempos guardados; sin nuevas inferencias, grabaciones ni medición real de latencia. Se usan anclas humanas solo para evaluar. Regla de al menos tres palabras elegida provisionalmente sobre datos de desarrollo. Seguidor habitual sin activar variantes.

Si falla la búsqueda local: cola completa de 3 a 8 palabras exactas consecutivas, aparición única en todo el cuento, destino anterior, tiempos ordenados y frase situada después del apoyo temporal aceptado. El resto conserva la combinación y la política de texto idéntico.

| Caso | Ventana | Ronda | Cambios de posición respecto a combinación | Final combinación | Final nuevo |
|---|---:|---:|---:|---:|---:|
| normal | 6 | 1 | 0 | 56 | 56 |
| normal | 4 | 1 | 0 | 56 | 56 |
| normal | 8 | 1 | 0 | 56 | 56 |
| normal | 6 | 2 | 0 | 56 | 56 |
| normal | 4 | 2 | 0 | 56 | 56 |
| normal | 8 | 2 | 0 | 56 | 56 |
| normal | 4 | 3 | 0 | 56 | 56 |
| normal | 8 | 3 | 0 | 56 | 56 |
| normal | 6 | 3 | 0 | 56 | 56 |
| desviaciones | 8 | 1 | 0 | 56 | 56 |
| desviaciones | 6 | 1 | 0 | 56 | 56 |
| desviaciones | 4 | 1 | 0 | 56 | 56 |
| desviaciones | 4 | 2 | 0 | 56 | 56 |
| desviaciones | 6 | 2 | 0 | 56 | 56 |
| desviaciones | 8 | 2 | 0 | 56 | 56 |
| desviaciones | 8 | 3 | 0 | 56 | 56 |
| desviaciones | 4 | 3 | 0 | 56 | 56 |
| desviaciones | 6 | 3 | 0 | 56 | 56 |
| pausa | 8 | 1 | 0 | 56 | 56 |
| pausa | 4 | 1 | 0 | 56 | 56 |
| pausa | 8 | 2 | 0 | 56 | 56 |
| pausa | 4 | 2 | 0 | 56 | 56 |
| pausa | 4 | 3 | 0 | 56 | 56 |
| pausa | 8 | 3 | 0 | 56 | 56 |
| lenta | 8 | 1 | 0 | 56 | 56 |
| lenta | 4 | 1 | 0 | 53 | 53 |
| lenta | 8 | 2 | 0 | 56 | 56 |
| lenta | 4 | 2 | 0 | 53 | 53 |
| lenta | 4 | 3 | 0 | 53 | 53 |
| lenta | 8 | 3 | 0 | 56 | 56 |
| relectura | 8 | 1 | 0 | 56 | 56 |
| relectura | 4 | 1 | 0 | 56 | 56 |
| relectura | 8 | 2 | 0 | 56 | 56 |
| relectura | 4 | 2 | 0 | 56 | 56 |
| relectura | 4 | 3 | 0 | 56 | 56 |
| relectura | 8 | 3 | 0 | 56 | 56 |

## Controles sintéticos

- A. Texto y tiempos repetidos: [14, 14, 14] → [3, 3, 3]; recuperaciones nuevas 1.
- B. Mismo texto, tiempos posteriores: [14, 14, 14] → [3, 3, 3]; recuperaciones nuevas 1.
- C. La frase va creciendo: [14, 14, 5] → [3, 4, 5]; recuperaciones nuevas 1.
- D. Textos distintos respaldan el mismo candidato: [14, 14, 3] → [3, 3, 3]; recuperaciones nuevas 1.
- E. Frase exacta de audio antiguo: [14] → [14]; recuperaciones nuevas 0.
- F. Solo dos palabras: [14] → [14]; recuperaciones nuevas 0.
- G. Una palabra no coincide: [14] → [14]; recuperaciones nuevas 0.
- H. Frase que empieza antes del apoyo aceptado: [14] → [14]; recuperaciones nuevas 0.
- I. Texto antiguo seguido de igual texto con tiempos nuevos: [14, 14] → [14, 14]; recuperaciones nuevas 0.
- J. Frase con dos apariciones en el cuento (estado sintetico): [61] → [61]; recuperaciones nuevas 0.

No se cambia la política de texto idéntico. El control I conserva esa limitación. Exactitud y unicidad no prueban nueva habla: los tiempos ASR pueden fallar o el reconocedor inventar texto del cuento. No se mide generalización ni latencia real.
