# Control sin relectura: comparación de seguidores

Reproducción de hipótesis fijas, sin nuevas inferencias. Cortes de audio y salida lista simulada son distintos. Sin referencia humana temporal: no se calcula latencia respecto a la lectura ni precisión. Reglas sin modificar ni activar.

| Ventana | Ronda | Final original / combinada / nueva | Cortes distintos combinada–nueva | Recuperación exacta (corte s) |
|---:|---:|---|---|---|
| 8 | 1 | 56 / 56 / 56 | [] | [] |
| 4 | 1 | 56 / 56 / 56 | [] | [] |
| 8 | 2 | 56 / 56 / 56 | [] | [] |
| 4 | 2 | 56 / 56 / 56 | [] | [] |
| 4 | 3 | 56 / 56 / 56 | [] | [] |
| 8 | 3 | 56 / 56 / 56 | [] | [] |

## Retrocesos y conservación del final

Los retrocesos son movimientos registrados, no falsos positivos confirmados sin revisión del contenido.
- Ventana 8, ronda 1: retrocesos {'original': [], 'combinada': [], 'nueva': []}; posiciones distintas del final tras alcanzarlo {'original': [], 'combinada': [], 'nueva': []}.
- Ventana 4, ronda 1: retrocesos {'original': [], 'combinada': [], 'nueva': []}; posiciones distintas del final tras alcanzarlo {'original': [], 'combinada': [], 'nueva': []}.
- Ventana 8, ronda 2: retrocesos {'original': [], 'combinada': [], 'nueva': []}; posiciones distintas del final tras alcanzarlo {'original': [], 'combinada': [], 'nueva': []}.
- Ventana 4, ronda 2: retrocesos {'original': [], 'combinada': [], 'nueva': []}; posiciones distintas del final tras alcanzarlo {'original': [], 'combinada': [], 'nueva': []}.
- Ventana 4, ronda 3: retrocesos {'original': [], 'combinada': [], 'nueva': []}; posiciones distintas del final tras alcanzarlo {'original': [], 'combinada': [], 'nueva': []}.
- Ventana 8, ronda 3: retrocesos {'original': [], 'combinada': [], 'nueva': []}; posiciones distintas del final tras alcanzarlo {'original': [], 'combinada': [], 'nueva': []}.
