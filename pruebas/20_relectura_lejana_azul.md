# Segunda relectura lejana: destino azul

21/10/2026. WAV datos/audio/lectura_20261021_103917_243241.wav, 45 s. Consigna: cuento completo y después Cerca de un árbol encontró una mariposa azul, final 17. Contenido confirmado por el usuario, sin marcas temporales humanas nuevas.

El usuario comparte resultados/comparaciones/20261021_104005_265730 (ventanas 4/8, tres rondas). Contrastar sin nuevas inferencias ni modificar reglas:

```powershell
.\.venv\Scripts\python.exe -m scripts.comparar_relectura_lejana resultados/comparaciones/20261021_104005_265730
```

Ejecución del asistente: resultados/relectura_lejana/20261021_104431_582794. Ventana 4 s: original/combinación final 56; nueva vuelve a 12 en corte 28 con Cerca de un, avanza a 13/15/17 en 30/32/34. Ventana 8 s: nueva vuelve directamente a 17 en 34; las otras recuperan en 36. Repetido en tres rondas de una sola grabación. El mínimo de tres palabras se conserva provisionalmente: este caso favorable no valida su seguridad general. Sin anclas no se mide demora respecto a la lectura. El usuario comparte resultados/relectura_lejana/20261021_104703_885196: los seis registros completos coinciden con los del asistente. Se prepara anotador --caso relectura_azul para cuaderno, Cerca y azul; tiempos manuales pendientes. No se activa ni publica automáticamente.

## Evaluación con marcas humanas

Anclas revisadas: cuaderno 21,79–22,51 s, Cerca 25,73–26,84, azul 33,32–34,32. Para contrastar:

```powershell
.\.venv\Scripts\python.exe -m scripts.evaluar_relectura_lejana resultados/relectura_lejana/20261021_104703_885196 --caso relectura_azul
```

Primera hipótesis en azul: nueva corte 34 (antes del final audible 34,32), original/combinación 8 s corte 36. Primera salida lista respecto al final humano: nueva 4 s media 1,26 s, nueva 8 s 1,39, original/combinación 8 s 3,25; original/combinación 4 s sin recuperación. Con criterio de corte posterior al final humano completo todas las versiones que recuperan lo apoyan en 36. No confundir primera identificación parcial con disponer de la palabra completa. Tiempos de salida simulados reutilizados, sin pantalla ni coste de variantes. El usuario ejecuta el evaluador y comparte las 18 filas, coincidentes con las del asistente. Revisión conjunta completada, manteniendo la distinción entre primera hipótesis parcial y actualización posterior al final humano. No se activa ni publica automáticamente.
