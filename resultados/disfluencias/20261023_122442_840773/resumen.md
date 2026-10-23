# Piloto de VAD y transcripción literal

Cuatro fragmentos completos de 8 s. Una pasada por condición; orden alternado. Sin referencias exhaustivas ni tasas de eventos. Un solo modelo compartido; tiempos no comparables directamente con rondas históricas. No modifica el seguidor, sus registros ni anotaciones humanas.

| Fragmento | VAD | Texto bruto del modelo | Palabras guardadas |
|---|---|---|---|
| inicio | True |  Una tarde Lucía paseaba por el parque. | Una tarde Lucía paseaba por el parque |
| inicio | False |  Una tarde Lucía paseaba por el parque. | Una tarde Lucía paseaba por el parque |
| medio_1 | False |  descubrió un pequeño barco rojo, el barco... | descubrió un pequeño barco rojo el barco |
| medio_1 | True |  descubrió un pequeño barco rojo, el barco... | descubrió un pequeño barco rojo el barco |
| medio_2 | True |  para acercarlo a la orilla.  Su abuelo la ayudó y junto... | para acercarlo a la orilla Su abuelo la ayudó y junto |
| medio_2 | False |  para acercarlo a la orilla.  Su abuelo la ayudó y junto... | para acercarlo a la orilla Su abuelo la ayudó y junto |
| final | False |  pues regresaron a casa y lo colocaron sobre una estantería. | pues regresaron a casa y lo colocaron sobre una estantería |
| final | True |  pues regresaron a casa y lo colocaron sobre una estantería. | pues regresaron a casa y lo colocaron sobre una estantería |
