# MLS · xlsr · prueba offline

Partición: dev. Seleccionados: 10; completados: 10; fallos: 0.

WER global: 0.11290322580645161; CER global: 0.024439918533604887; RTF ASR: 0.008230404034235958.

| Audio | Estado | Duración s | WER | CER | ASR s | RTF |
|---|---|---:|---:|---:|---:|---:|
| 133_1378_000042 | ok | 19.9600 | 0.0536 | 0.0069 | 0.1688 | 0.0085 |
| 1075_567_000050 | ok | 11.1000 | 0.0800 | 0.0073 | 0.0873 | 0.0079 |
| 6223_5079_000063 | ok | 15.0400 | 0.0444 | 0.0044 | 0.1373 | 0.0091 |
| 3719_1378_000015 | ok | 11.5900 | 0.0750 | 0.0227 | 0.0931 | 0.0080 |
| 133_1378_000052 | ok | 15.5900 | 0.2222 | 0.0457 | 0.1338 | 0.0086 |
| 10367_10282_000004 | ok | 19.1200 | 0.1458 | 0.0368 | 0.1600 | 0.0084 |
| 3719_1378_000088 | ok | 12.5000 | 0.0909 | 0.0169 | 0.0957 | 0.0077 |
| 6671_9310_000004 | ok | 10.6600 | 0.2000 | 0.0467 | 0.0857 | 0.0080 |
| 2592_1378_000079 | ok | 12.6900 | 0.2500 | 0.0613 | 0.0955 | 0.0075 |
| 3719_1378_000049 | ok | 13.8300 | 0.0732 | 0.0139 | 0.1122 | 0.0081 |

Normalización: NFC; minúsculas; puntuación Unicode sustituida por espacios; espacios colapsados; conserva tildes, ñ y números. CER incluye espacios.

Configuración exacta del motor en ejecucion.json. Una pasada por audio, batch 1. Sin VAD externo, remuestreo o reducción de ruido. Endpointing/segmentación internos dependen del motor. Calentamiento excluido y conservado por sesión.
RTF ASR incluye preparación de entradas, transferencia, forward y decodificación; excluye lectura, métricas, escritura y carga del modelo. CUDA sincronizada al medir.
Los fallos no reciben WER cero: se excluyen del cálculo y quedan contados. Reanudar no reintenta resultados fallidos.
Recursos por sesión en sesiones/*.json, con muestras y alcance. La primera ejecución se conserva separada; cachés de disco no controladas. No es latencia visual, prueba de literalidad ni medida de tablet.
Primera integración técnica; antes de evaluación completa, comprobar salida, cobertura de telemetría y comparabilidad con otros reconocedores.
