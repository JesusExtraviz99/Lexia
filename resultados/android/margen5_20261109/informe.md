> PRELIMINAR: aquí las cinco posiciones incluyen la actual. La interpretación final con cinco palabras anteriores más la actual está en margen5_inclusivo_20261109 (offset 6).

# Margen de cinco palabras · reproducción

Cambios de posición no equivalen a mejoras sin referencia humana. Mismos textos ASR: no mide aceleración del modelo ni nueva latencia. El cuento no se introduce en el ASR.

Se aísla reducir el contexto local de 12 a 5 palabras y, por separado, desactivar la recuperación global. Se mantienen 24 palabras por delante, hipótesis de ocho palabras y umbrales originales.

| Sesión | Versión | Final | Retrocesos | Avances >1 | Cortes distintos |
|---|---|---:|---:|---:|---:|
| lexia_1794219519555.json | original | 56 | 0 | 9 | 0 |
| lexia_1794219519555.json | local5_global | 56 | 0 | 9 | 0 |
| lexia_1794219519555.json | local5_sin_global | 56 | 0 | 9 | 0 |
| lexia_1794219667177.json | original | 56 | 1 | 9 | 0 |
| lexia_1794219667177.json | local5_global | 56 | 0 | 8 | 1 |
| lexia_1794219667177.json | local5_sin_global | 56 | 0 | 8 | 1 |
| lexia_1794220857455.json | original | 56 | 0 | 3 | 0 |
| lexia_1794220857455.json | local5_global | 56 | 0 | 3 | 0 |
| lexia_1794220857455.json | local5_sin_global | 56 | 0 | 3 | 0 |
| lexia_1794220954773.json | original | 56 | 2 | 5 | 0 |
| lexia_1794220954773.json | local5_global | 56 | 0 | 5 | 4 |
| lexia_1794220954773.json | local5_sin_global | 56 | 0 | 5 | 4 |

## Controles construidos

Son propuestas textuales, no grabaciones ni segundos de demora.

- avance normal: destino construido 12; {'original': [11, 12], 'local5_global': [11, 12], 'local5_sin_global': [11, 12]}.

- relectura corta: destino construido 11; {'original': [10, 11], 'local5_global': [10, 11], 'local5_sin_global': [10, 11]}.

- relectura lejana: destino construido 3; {'original': [20, 20, 3], 'local5_global': [20, 20, 3], 'local5_sin_global': [20, 20, 20]}.

- ocho palabras antiguas sin avance: destino construido 12; {'original': [12], 'local5_global': [12], 'local5_sin_global': [12]}.

## Interpretación

Un margen de cinco palabras no prohíbe retroceder dentro de ese margen ni garantiza eliminar oscilaciones. Quitar la recuperación global sí impide resolver ciertos regresos lejanos; el resaltado no demuestra que nunca ocurrirán. Acortar el cuento buscado no acelera por sí mismo la inferencia acústica. Un avance de varias palabras puede ser la llegada de una frase reconocida; no demuestra omisión lectora ni pérdida de todas esas palabras.

Ninguna de estas variantes queda activada en la app.
