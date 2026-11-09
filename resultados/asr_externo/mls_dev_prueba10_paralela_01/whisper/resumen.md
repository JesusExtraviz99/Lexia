# MLS · whisper · prueba offline

Partición: dev. Seleccionados: 10; completados: 10; fallos: 0.

WER global: 0.08602150537634409; CER global: 0.021384928716904276; RTF ASR: 0.03788383146129162.

| Audio | Estado | Duración s | WER | CER | ASR s | RTF |
|---|---|---:|---:|---:|---:|---:|
| 133_1378_000042 | ok | 19.9600 | 0.0000 | 0.0000 | 0.7215 | 0.0361 |
| 1075_567_000050 | ok | 11.1000 | 0.0800 | 0.0219 | 0.3513 | 0.0317 |
| 6223_5079_000063 | ok | 15.0400 | 0.0444 | 0.0131 | 0.5895 | 0.0392 |
| 3719_1378_000015 | ok | 11.5900 | 0.0750 | 0.0284 | 0.4581 | 0.0395 |
| 133_1378_000052 | ok | 15.5900 | 0.0278 | 0.0051 | 0.5629 | 0.0361 |
| 10367_10282_000004 | ok | 19.1200 | 0.0625 | 0.0147 | 0.8258 | 0.0432 |
| 3719_1378_000088 | ok | 12.5000 | 0.0909 | 0.0169 | 0.4757 | 0.0381 |
| 6671_9310_000004 | ok | 10.6600 | 0.2000 | 0.0374 | 0.3288 | 0.0308 |
| 2592_1378_000079 | ok | 12.6900 | 0.4643 | 0.1104 | 0.5127 | 0.0404 |
| 3719_1378_000049 | ok | 13.8300 | 0.0244 | 0.0046 | 0.5562 | 0.0402 |

Normalización: NFC; minúsculas; puntuación Unicode sustituida por espacios; espacios colapsados; conserva tildes, ñ y números. CER incluye espacios.

Configuración exacta del motor en ejecucion.json. Una pasada por audio, batch 1. Sin VAD externo, remuestreo o reducción de ruido. Endpointing/segmentación internos dependen del motor. Calentamiento excluido y conservado por sesión.
RTF ASR incluye preparación de entradas, transferencia, forward y decodificación; excluye lectura, métricas, escritura y carga del modelo. CUDA sincronizada al medir.
Los fallos no reciben WER cero: se excluyen del cálculo y quedan contados. Reanudar no reintenta resultados fallidos.
Recursos por sesión en sesiones/*.json, con muestras y alcance. La primera ejecución se conserva separada; cachés de disco no controladas. No es latencia visual, prueba de literalidad ni medida de tablet.
Primera integración técnica; antes de evaluación completa, comprobar salida, cobertura de telemetría y comparabilidad con otros reconocedores.
