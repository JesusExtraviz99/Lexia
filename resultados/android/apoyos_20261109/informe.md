# Apoyo de avances y texto reciente · experimento

Reproducción de las mismas hipótesis. No corrige el ASR, no prueba que una frase se pronunciara ni mide latencia acústica nueva. Las reglas NO están activadas en la APK. Un sufijo inventado que coincida con el cuento todavía puede engañarlas.

Se conserva el ASR y el margen de cada sesión. Variante1: para avanzar, la última palabra propuesta debe coincidir con el destino; un avance de más de una posición requiere además las dos últimas palabras consecutivas exactas. Variante2 añade una salida del atasco: sufijo reciente de al menos tres palabras consecutivas exactas, una de al menos cinco caracteres, aparición única en el cuento y destino dentro de las 24 posiciones siguientes. No cambia retrocesos, ni acepta una palabra aislada, ni limita artificialmente todo avance a una posición.

| Registro | Versión del seguidor | Final | Retrocesos | Callbacks distintos | Primer callback en final (s) |
|---|---|---:|---:|---:|---:|
| lexia_1794219519555.json | original | 56 | 0 | 0 | 68.119 |
| lexia_1794219519555.json | terminal_support | 56 | 0 | 14 | 68.119 |
| lexia_1794219519555.json | terminal_and_recent | 56 | 0 | 14 | 68.119 |
| lexia_1794219667177.json | original | 56 | 1 | 0 | 89.834 |
| lexia_1794219667177.json | terminal_support | 56 | 0 | 8 | 89.834 |
| lexia_1794219667177.json | terminal_and_recent | 56 | 0 | 14 | 83.823 |
| lexia_1794220857455.json | original | 56 | 0 | 0 | 56.385 |
| lexia_1794220857455.json | terminal_support | 56 | 0 | 4 | 56.385 |
| lexia_1794220857455.json | terminal_and_recent | 56 | 0 | 4 | 56.385 |
| lexia_1794220954773.json | original | 56 | 2 | 0 | 52.201 |
| lexia_1794220954773.json | terminal_support | 56 | 0 | 9 | 52.201 |
| lexia_1794220954773.json | terminal_and_recent | 56 | 0 | 9 | 52.201 |
| lexia_1794224052924.json | original | 56 | 3 | 0 | 110.312 |
| lexia_1794224052924.json | terminal_support | 56 | 0 | 14 | 110.312 |
| lexia_1794224052924.json | terminal_and_recent | 56 | 0 | 23 | 99.452 |

## Límites y decisión

El apoyo terminal evita ciertos saltos basados en coincidencias interiores antiguas. Puede retrasar avances correctos cuando el ASR añade una terminación errónea. La recuperación exacta por texto reciente puede superar contaminación anterior, pero es más permisiva que el alineamiento completo y requiere controles negativos. Las dos variantes están diseñadas a partir de estos mismos registros: son desarrollo, no validación independiente. No se elige por llegar al final antes.

Mantener 0,125 y 0,25 s como rango de futuras lecturas. La nueva toma usa Small, 0,125 s y contexto original, no el margen de cinco. Su diferencia respecto a otras tomas no prueba que la cadencia cause los errores: cambian lectura, segmentación y condiciones. No hay aquí escucha independiente ni referencia humana por palabra.
