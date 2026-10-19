# Evaluación de la pausa con anclas humanas

Tres anclas manuales revisadas por el lector; cobertura parcial, sin revisión independiente. La pausa se mide desde el final de flor hasta el inicio de Ana: intervalo sin lectura, no silencio acústico absoluto. Solo se conoce posición de referencia 27 dentro de ese intervalo. Las hipótesis de ventanas solapadas pueden contener habla anterior a la pausa. Una hipótesis no vacía no demuestra alucinación ni habla durante la pausa. La posición visible usa la última salida ya terminada en cada corte, según cola secuencial simulada, sin carga inicial del modelo ni latencia de pantalla. No se asignan tiempos a palabras no anotadas. El primer avance >=28 no mide reconocimiento exacto ni tiempo de detección de Ana. Se reutilizan registros existentes: no se han ejecutado nuevas inferencias.

Pausa anotada: 11.88–21.20 s; duración 9.32 s.

| Ventana | Ronda | Hipótesis en 27 durante pausa | Visible en 27 durante pausa | Primer avance tras retomar (audio s / posición) | Demora de avance simulada desde fin de Ana (s) | Demora final simulada (s) |
|---:|---:|---:|---:|---|---:|---:|
| 8 | 1 | 5/5 | 3/5 | 24.00 / 36 | 4.43 | 4.19 |
| 4 | 1 | 5/5 | 3/5 | 24.00 / 36 | 4.53 | 3.12 |
| 8 | 2 | 5/5 | 3/5 | 24.00 / 36 | 4.36 | 3.68 |
| 4 | 2 | 5/5 | 4/5 | 24.00 / 36 | 4.29 | 2.86 |
| 4 | 3 | 5/5 | 3/5 | 24.00 / 36 | 4.47 | 3.18 |
| 8 | 3 | 5/5 | 3/5 | 24.00 / 36 | 4.45 | 4.23 |

## Cortes dentro de la pausa

| Ventana | Ronda | Audio (s) | Referencia | Hipótesis | Visible simulado | Texto ASR |
|---:|---:|---:|---:|---:|---:|---|
| 8 | 1 | 12.0 | 27 | 27 | 20 | de su casa Cerca de un árbol encontró una mariposa azul La mariposa voló despacio y se posó sobre una flor |
| 8 | 1 | 14.0 | 27 | 27 | 20 | encontró una mariposa azul La mariposa voló despacio y se posó sobre una flor |
| 8 | 1 | 16.0 | 27 | 27 | 27 | La mariposa voló despacio y se posó sobre una flor |
| 8 | 1 | 18.0 | 27 | 27 | 27 | y se posó sobre una flor |
| 8 | 1 | 20.0 | 27 | 27 | 27 |  |
| 4 | 1 | 12.0 | 27 | 27 | 21 | La mariposa voló despacio y se posó sobre una flor |
| 4 | 1 | 14.0 | 27 | 27 | 21 | y se posó sobre una flor |
| 4 | 1 | 16.0 | 27 | 27 | 27 |  |
| 4 | 1 | 18.0 | 27 | 27 | 27 |  |
| 4 | 1 | 20.0 | 27 | 27 | 27 | Suscríbete |
| 8 | 2 | 12.0 | 27 | 27 | 17 | de su casa Cerca de un árbol encontró una mariposa azul La mariposa voló despacio y se posó sobre una flor |
| 8 | 2 | 14.0 | 27 | 27 | 20 | encontró una mariposa azul La mariposa voló despacio y se posó sobre una flor |
| 8 | 2 | 16.0 | 27 | 27 | 27 | La mariposa voló despacio y se posó sobre una flor |
| 8 | 2 | 18.0 | 27 | 27 | 27 | y se posó sobre una flor |
| 8 | 2 | 20.0 | 27 | 27 | 27 |  |
| 4 | 2 | 12.0 | 27 | 27 | 17 | La mariposa voló despacio y se posó sobre una flor |
| 4 | 2 | 14.0 | 27 | 27 | 27 | y se posó sobre una flor |
| 4 | 2 | 16.0 | 27 | 27 | 27 |  |
| 4 | 2 | 18.0 | 27 | 27 | 27 |  |
| 4 | 2 | 20.0 | 27 | 27 | 27 | Suscríbete |
| 4 | 3 | 12.0 | 27 | 27 | 17 | La mariposa voló despacio y se posó sobre una flor |
| 4 | 3 | 14.0 | 27 | 27 | 21 | y se posó sobre una flor |
| 4 | 3 | 16.0 | 27 | 27 | 27 |  |
| 4 | 3 | 18.0 | 27 | 27 | 27 |  |
| 4 | 3 | 20.0 | 27 | 27 | 27 | Suscríbete |
| 8 | 3 | 12.0 | 27 | 27 | 17 | de su casa Cerca de un árbol encontró una mariposa azul La mariposa voló despacio y se posó sobre una flor |
| 8 | 3 | 14.0 | 27 | 27 | 20 | encontró una mariposa azul La mariposa voló despacio y se posó sobre una flor |
| 8 | 3 | 16.0 | 27 | 27 | 27 | La mariposa voló despacio y se posó sobre una flor |
| 8 | 3 | 18.0 | 27 | 27 | 27 | y se posó sobre una flor |
| 8 | 3 | 20.0 | 27 | 27 | 27 |  |
