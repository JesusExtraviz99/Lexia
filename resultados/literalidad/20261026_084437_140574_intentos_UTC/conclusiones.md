# Conclusiones del contraste de intentos

26/10/2026. Siete inferencias nuevas: tres ablaciones sobre dos entradas de desarrollo idénticas a sus prefijos VAD anteriores, más un diagnóstico acústico separado.

- Desactivar por separado reparación de repeticiones, temperaturas alternativas o recuperación de cierre deja el texto exactamente igual al de referencia en las tomas 2 y 3 (seis comparaciones exactas).
- Las cuatro repeticiones de palabras de toma 2 siguen presentes; los intentos regres- re- de toma 3 siguen ausentes.
- El último bloque nativo anterior (52–70,32 s) ya escribe regresar: la omisión no aparece solo al unir los textos para mostrarlos.
- Reconocer ese tramo aislado sin contexto textual previo y con ajustes originales también escribe Antes de regresar. No recupera los intentos. Su principio Piedra y encontró... puede corresponder al solapamiento acústico que la continuación anterior gestionaba con contexto; no se declara invención por comparar cadenas distintas.
- Estos resultados no identifican el mecanismo interno de la omisión. Tampoco prueban que las funciones desactivadas se hubieran ejecutado en la referencia. No hay base aquí para adoptar esos cambios.
- El recorte conserva el límite final VAD, pero cambia inicio, contexto y ruta corta/larga. No es un experimento causal puro de contexto ni evidencia contra toda posible mejora por segmentación.
- No se ha ajustado nada con tomas 5/6 reservadas. No se han descargado modelos ni cambiado el seguidor.

Inferencia total de siete propuestas: 108,46 s; carga única 6,05 s; pico de vida del proceso 4.403,49 MiB. CPU, RAM/GPU global y detalle por propuesta en resultados.json. Las referencias antiguas se reutilizan: no comparar velocidades como benchmark pareado, ni inferir rendimiento en tablet.

## Revisión de escucha

Visor http://127.0.0.1:8782/ con toma 3, control toma 2 y último bloque aislado; 0,4× disponible. El objetivo se oye aproximadamente a los 8 s del fragmento según marca automática del ASR; empezar unos segundos antes para escuchar también los intentos. No es una marca humana validada.

Confirmación previa del lector: regres- re- regresar. Falta establecer sus límites humanos y contrastar con las distintas salidas. El texto no basta para contar intentos. Decisión del usuario (26/10/2026): conservar ajustes originales + VAD de final y dejar esta omisión como observación pendiente para el cambio de entorno. Retomar entonces con el mismo WAV/fragmento y los controles conservados, sin continuar ahora con más ajustes o reconocedores.
