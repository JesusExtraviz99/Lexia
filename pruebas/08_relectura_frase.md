# Prueba 08: relectura de una frase

Fecha: 16/10/2026. Ejecutada por el usuario; salida y JSON locales revisados. Sin cambios de código ni publicación.

Audio: `datos/audio/lectura_20261016_104151_933317.wav`, duración 60 s. Registros: `resultados/comparaciones/20261016_104206_415649/`. Ventanas de 4 y 8 s, bloque de 2 s, tres rondas, Whisper small CPU int8, VAD y seguidor sin cambios. La consigna era repetir Los dos se quedaron en silencio y continuar con mirando sus alas. Las hipótesis conservan esa repetición; falta anotación humana literal y temporal del audio.

## Resultados

| Ventana | Inferencia total media (s) | Rango (s) | Inferencias >2 s | Cola máxima simulada | Final |
|---|---:|---|---:|---:|---|
| 4 s | 26,21 | 26,09–26,46 | 0/90 | 0 s | 56, cuaderno |
| 8 s | 31,49 | 30,89–31,80 | 0/90 | 0 s | 56, cuaderno |

Las seis ejecuciones alcanzan 56 al corte de 30 s y lo mantienen. Los tiempos incluyen silencio final; no son latencia visual. Cada ventana reproduce su secuencia de posiciones en las tres rondas.

## Qué ocurre durante la repetición

| Corte de audio disponible | Ventana 4 s | Ventana 8 s |
|---|---|---|
| 20 s | 42, silencio | 42, silencio |
| 22 s | Retrocede a 41, en | Conserva 42, silencio |
| 24 s | Avanza a 45, alas | Avanza a 45, alas |

Las hipótesis incluyen las dos apariciones del fragmento. En ventana 8, al corte de 22 s se rechaza la nueva posición: las últimas ocho palabras tienen cuatro coincidencias y coste de edición cuatro. El estado conserva la posición anterior. En ventana 4, la nueva hipótesis permite aceptar 41; no representa necesariamente el retorno completo al principio de la frase.

Conservar la repetición en ASR, representarla con un indicador y evaluarla como evento son capacidades diferentes. La prueba confirma continuidad tras este caso; no demuestra seguimiento preciso de todo el retroceso. La actualización cada 2 s puede omitir posiciones intermedias; falta referencia humana para comprobar cuáles ocurrieron entre cortes.

## Relación con la lectura lenta

La repetición real prevista provoca un pequeño retroceso con 4 s y una espera con 8 s. En la lectura lenta, 8 s retrocedía al cambiar cuaderno por en un jugaderno. Un recuento de retrocesos por sí solo no distingue estos escenarios. No resolver la regresión imponiendo avance exclusivamente hacia delante sin comparar con relecturas.

## Decisión

Se completa el primer recorrido de casos adultos: lectura normal, desviaciones deliberadas, pausa, lectura lenta y relectura. Se conservan fallos y configuraciones sin ajustes posteriores a este caso. El siguiente trabajo es organizar el banco de pruebas, asociar cada WAV con su caso y añadir transcripciones literales y marcas temporales humanas antes de comparar reconocedores o ayudas de audio. El conjunto actual es pequeño, con un adulto y un cuento; no valida uso infantil.
