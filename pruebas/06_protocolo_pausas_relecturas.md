# Próxima prueba: ritmo lento, pausa y relectura

Estado: protocolo propuesto; no ejecutado. No contiene resultados.

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
