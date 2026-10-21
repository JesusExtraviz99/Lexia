# Relectura lejana: comparación de seguidores

Reproducción de hipótesis fijas, sin nuevas inferencias. Cortes de audio y salida lista simulada son distintos. Sin referencia humana temporal: no se calcula latencia respecto a la lectura ni precisión. Reglas sin modificar ni activar.

| Ventana | Ronda | Final original / combinada / nueva | Cortes distintos combinada–nueva | Recuperación exacta (corte s) |
|---:|---:|---|---|---|
| 8 | 1 | 45 / 45 / 45 | [34.0, 36.0] | [34.0] |
| 4 | 1 | 56 / 56 / 45 | [32.0, 34.0, 36.0, 38.0, 40.0, 42.0, 44.0, 46.0, 48.0, 50.0, 52.0, 54.0, 56.0, 58.0, 60.0] | [32.0] |
| 8 | 2 | 45 / 45 / 45 | [34.0, 36.0] | [34.0] |
| 4 | 2 | 56 / 56 / 45 | [32.0, 34.0, 36.0, 38.0, 40.0, 42.0, 44.0, 46.0, 48.0, 50.0, 52.0, 54.0, 56.0, 58.0, 60.0] | [32.0] |
| 4 | 3 | 56 / 56 / 45 | [32.0, 34.0, 36.0, 38.0, 40.0, 42.0, 44.0, 46.0, 48.0, 50.0, 52.0, 54.0, 56.0, 58.0, 60.0] | [32.0] |
| 8 | 3 | 45 / 45 / 45 | [34.0, 36.0] | [34.0] |
