# Próxima prueba: ritmo lento, pausa y relectura

Estado: prueba de pausa ejecutada por el usuario; lectura lenta y relectura pendientes. Los resultados de pausa se resumen al final.

## Pregunta

¿La ventana de 4 s conserva el seguimiento ante lectura lenta, silencio prolongado y retrocesos, o resulta útil el contexto de 8 s?

Usar el mismo cuento de 56 palabras, modelo Whisper small, CPU int8, VAD, bloque de 2 s y seguidor. Comparar únicamente ventanas de 4 y 8 s, tres rondas por audio. No introducir cambios de modelo en esta prueba.

## Grabaciones separadas

1. Ritmo lento: leer el cuento completo más despacio, sin errores deliberados, pausas extra ni relecturas.
2. Pausa: leer normalmente, parar unos 8 s después de flor y continuar con Ana llamó a su hermano. El indicador debería conservar la última posición respaldada durante la pausa y recuperar la lectura al continuar.
3. Relectura: leer normalmente; después de decir Los dos se quedaron en silencio, repetir esa misma frase y continuar con mirando sus alas. Revisar si el seguidor representa el retroceso y recupera la continuación; no exigir que el indicador solo avance.

Grabar una prueba y compararla antes de crear la siguiente para que el programa seleccione el WAV adecuado por defecto. Anotar la ruta del WAV y cualquier desviación no prevista. Son tres lecturas nuevas del mismo adulto; no una validación infantil.

```powershell
.\.venv\Scripts\python.exe scripts\grabar.py --segundos 60
.\.venv\Scripts\python.exe -u scripts\comparar_ventanas.py --ventanas 4 8 --repeticiones 3
```

Si la lectura lenta necesita más tiempo, usar --segundos 90. También se puede pasar la ruta de un WAV concreto al comparador para evitar seleccionar otro audio.

## Qué revisar

- Tiempo por inferencia y espera acumulada simulada.
- Posiciones por corte: no evaluar solo si alcanza cuaderno.
- Falsos avances durante silencio, retrocesos inesperados, bloqueos y recuperación.
- En la relectura, retorno al fragmento correcto y continuación posterior.
- Escucha humana de los tramos difíciles: anotar aproximadamente cuándo comienzan/terminan la pausa y la relectura, y las palabras en esos momentos. Estas marcas manuales iniciales no equivalen a una anotación temporal completa.
- Ventanas que no contienen voz: posición conservada esperable, no pérdida automática de seguimiento.

No considerar cada ventana solapada una lectura nueva, ni una diferencia ASR como error lector confirmado. No atribuir precisión temporal al sistema sin una referencia humana revisada.

## Resultado de pausa comunicado y comprobado

Audio: `datos/audio/lectura_20261014_111454_984161.wav`, 60 s. Registros en `resultados/comparaciones/20261014_111548_094194/`.

Tres rondas por ventana. En las seis ejecuciones: flor (27) se mantiene en cortes de 12 a 22 s; verla (36) aparece al corte de 24 s y cuaderno (56) al de 32 s. No hay retrocesos. No se ha anotado manualmente el inicio exacto de reanudación para medir recuperación.

Ventana 4: inferencia total media 32,01 s, 12/90 inferencias superiores a 2 s, cola máxima media simulada 0,15 s. Ventana 8: 39,60 s, 30/90, cola media 1,34 s. Los silencios prolongados afectan al total y a las medianas.

Se observa Suscríbete, ajeno al cuento, durante la pausa (ventana 4, corte de 20 s) y después de terminar (4: cortes 36/38 s; 8: 40/42 s). No provoca movimiento en estos registros. Su origen requiere escucha: si no fue pronunciado ni hubo voz de fondo, es una salida inventada del ASR. No afirmar que el VAD elimina todos estos casos.

Estado de publicación: el usuario autoriza subir el WAV de pausa, resultados y notas. Las próximas lecturas y resultados permanecerán locales hasta nueva revisión y autorización.

### Revisión humana del final

El usuario confirma, tras escuchar la grabación, que en el tramo final correspondiente a la salida Suscríbete solo se oye el trino de los pájaros, sin esa palabra pronunciada por una persona. Se registra por tanto una salida inventada del ASR sobre ambiente con pájaros, según referencia humana del usuario. No es una prueba aislada de causalidad del trino ni una escucha independiente del desarrollador.

Esta confirmación cubre el final (cortes 36/38 s para ventana 4 y 40/42 s para ventana 8). La aparición durante la pausa, en el corte de 20 s, queda pendiente de revisión. En todos estos registros la posición se mantuvo. Se conserva el caso para probar falsas detecciones sobre ruido ambiental.

### Próxima lectura: ritmo lento

Leer el mismo cuento más despacio, intentando una duración de unos 40–50 s, sin pausa larga ni errores deliberados y sin separar artificialmente cada palabra. Grabar 60 s y comparar ventanas 4 y 8 s, tres rondas, con los comandos anteriores. Si se necesita más tiempo, grabar 90 s. Anotar cualquier desviación real y revisar las posiciones intermedias, no únicamente el final.

La pregunta es si una ventana de 4 s mantiene suficientes palabras de contexto para seguir una lectura lenta, frente a una de 8 s. La prueba aún no está ejecutada.
