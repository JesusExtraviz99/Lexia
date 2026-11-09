# MLS · whisper_turbo · prueba offline

Partición: dev. Seleccionados: 1; completados: 1; fallos: 0.

WER global: 0.0; CER global: 0.0; RTF ASR: 0.7512580510975423.

| Audio | Estado | Duración s | WER | CER | ASR s | RTF |
|---|---|---:|---:|---:|---:|---:|
| 133_1378_000042 | ok | 19.9600 | 0.0000 | 0.0000 | 14.9951 | 0.7513 |

Normalización: NFC; minúsculas; puntuación Unicode sustituida por espacios; espacios colapsados; conserva tildes, ñ y números. CER incluye espacios.

Configuración exacta del motor en ejecucion.json. Una pasada por audio, batch 1. Sin VAD externo, remuestreo o reducción de ruido. Endpointing/segmentación internos dependen del motor. Calentamiento excluido y conservado por sesión.
RTF ASR incluye preparación de entradas, transferencia, forward y decodificación; excluye lectura, métricas, escritura y carga del modelo. CUDA sincronizada al medir.
Los fallos no reciben WER cero: se excluyen del cálculo y quedan contados. Reanudar no reintenta resultados fallidos.
Recursos por sesión en sesiones/*.json, con muestras y alcance. La primera ejecución se conserva separada; cachés de disco no controladas. No es latencia visual, prueba de literalidad ni medida de tablet.
Revisar cobertura, avisos y comparabilidad; ejecución concurrente y medición de rendimiento aislado son condiciones diferentes.
