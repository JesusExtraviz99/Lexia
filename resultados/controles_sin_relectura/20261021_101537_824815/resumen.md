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

<!-- recursos-computo-inicio -->
## Recursos y coste computacional

Datos de la ejecución original. «No medido» no significa cero. RTF = suma de inferencias / duración del audio completo (incluye silencio); no es latencia visual ni mide captura, escritura o muestreo. Las rondas de una grabación no son lecturas independientes.

| Registro | Dispositivo ASR | Precisión | GPU para ASR | RTF | Máx. inferencia (s) | CPU/RAM/GPU instrumentadas |
|---|---|---|---|---:|---:|---|
| lectura_20261021_100814_321948_ventana_8s_r1.json | cpu | int8 | no (CPU) | 0.817 | 6.354 | no_medido_en_la_ejecucion_original |
| lectura_20261021_100814_321948_ventana_4s_r1.json | cpu | int8 | no (CPU) | 0.590 | 1.740 | no_medido_en_la_ejecucion_original |
| lectura_20261021_100814_321948_ventana_8s_r2.json | cpu | int8 | no (CPU) | 0.952 | 10.512 | no_medido_en_la_ejecucion_original |
| lectura_20261021_100814_321948_ventana_4s_r2.json | cpu | int8 | no (CPU) | 0.602 | 1.667 | no_medido_en_la_ejecucion_original |
| lectura_20261021_100814_321948_ventana_4s_r3.json | cpu | int8 | no (CPU) | 0.604 | 1.694 | no_medido_en_la_ejecucion_original |
| lectura_20261021_100814_321948_ventana_8s_r3.json | cpu | int8 | no (CPU) | 0.934 | 9.859 | no_medido_en_la_ejecucion_original |

Para comparar tablets habrá que medir en el dispositivo de destino: RAM máxima, tiempo de respuesta sostenido y consumo/batería. Este ordenador no permite deducir esos valores. No se cambia CPU por GPU automáticamente.
<!-- recursos-computo-fin -->

<!-- identidad-audio-inicio -->
## Audio utilizado

- **Lectura normal con lluvia · cuento 1 · 21/10/2026** — Lectura normal con lluvia - cuento 1 - 21-10-2026.wav
<!-- identidad-audio-fin -->
