# Prueba 02: lectura adulta con desviaciones deliberadas

Audio: `datos/audio/lectura_20261014_082953_219058.wav`.
Resultado revisado: `resultados/lectura_20261014_082953_219058_20261014_083013_046227.json`.
Modelo: Whisper small, faster-whisper 1.2.1, CPU int8.
Audio: 30 s. Procesamiento: 3,85 s. Carga: 0,84 s.

Referencia de los intentos: descripción del lector. No se ha realizado una escucha ni una anotación temporal humana del audio en esta revisión.

| Evento comunicado por el lector | Resultado en el JSON | Interpretación inicial |
|---|---|---|
| Dos apariciones consecutivas de Ana al inicio | Dos entradas: Ana, de 2,32 a 3,06 s; Ana de 3,66 a 4,08 s | Conserva la repetición. |
| Omisión de despacio | Secuencia voló y se posó, sin despacio | Respeta la omisión en la transcripción; todavía no existe un detector automático de omisiones. |
| mari… mariposa en dibujaron la mariposa en un cuaderno | Una única entrada mariposa, de 20,98 a 22,86 s | No representa por separado el intento truncado. El intervalo estimado puede abarcar el intento y la corrección, pero debe revisarse escuchando el audio. |
| El lector indica haber dicho silencio | Salida cinesio, de 16,48 a 16,96 s | Posible sustitución del ASR según la referencia del lector; no etiquetar como error lector. |

Los intervalos son estimaciones del ASR. La duración de mariposa (1,88 s) no demuestra por sí sola una autocorrección. La probabilidad del modelo tampoco es una puntuación calibrada de lectura correcta.

## Consecuencias para el desarrollo

- Conservar el audio y la salida original sin corregirla automáticamente contra el cuento.
- Separar diferencias textuales, errores del ASR y errores lectores confirmados.
- El seguidor deberá tolerar una sustitución local como silencio/cinesio y continuar con mirando sus alas.
- Comparar cuento y transcripción puede localizar repetición, omisión y sustitución candidatas, pero no recuperar un fragmento borrado por el reconocedor.
- Siguiente hito: alineamiento textual posterior con índices del cuento, antes de implementar seguimiento incremental.
