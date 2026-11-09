# MLS · vosk · prueba offline

Partición: dev. Seleccionados: 10; completados: 10; fallos: 0.

WER global: 0.13172043010752688; CER global: 0.03920570264765784; RTF ASR: 0.0894560009688936.

| Audio | Estado | Duración s | WER | CER | ASR s | RTF |
|---|---|---:|---:|---:|---:|---:|
| 133_1378_000042 | ok | 19.9600 | 0.0714 | 0.0172 | 1.6172 | 0.0810 |
| 1075_567_000050 | ok | 11.1000 | 0.0800 | 0.0146 | 0.9240 | 0.0832 |
| 6223_5079_000063 | ok | 15.0400 | 0.1778 | 0.0742 | 1.4110 | 0.0938 |
| 3719_1378_000015 | ok | 11.5900 | 0.0750 | 0.0227 | 1.1382 | 0.0982 |
| 133_1378_000052 | ok | 15.5900 | 0.0278 | 0.0051 | 1.4281 | 0.0916 |
| 10367_10282_000004 | ok | 19.1200 | 0.0417 | 0.0110 | 1.6056 | 0.0840 |
| 3719_1378_000088 | ok | 12.5000 | 0.1818 | 0.0395 | 1.0785 | 0.0863 |
| 6671_9310_000004 | ok | 10.6600 | 0.3000 | 0.1121 | 0.9553 | 0.0896 |
| 2592_1378_000079 | ok | 12.6900 | 0.4643 | 0.1288 | 1.4221 | 0.1121 |
| 3719_1378_000049 | ok | 13.8300 | 0.0976 | 0.0231 | 1.1299 | 0.0817 |

Normalización: NFC; minúsculas; puntuación Unicode sustituida por espacios; espacios colapsados; conserva tildes, ñ y números. CER incluye espacios.

Configuración exacta del motor en ejecucion.json. Una pasada por audio, batch 1. Sin VAD externo, remuestreo o reducción de ruido. Endpointing/segmentación internos dependen del motor. Calentamiento excluido y conservado por sesión.
RTF ASR incluye preparación de entradas, transferencia, forward y decodificación; excluye lectura, métricas, escritura y carga del modelo. CUDA sincronizada al medir.
Los fallos no reciben WER cero: se excluyen del cálculo y quedan contados. Reanudar no reintenta resultados fallidos.
Recursos por sesión en sesiones/*.json, con muestras y alcance. La primera ejecución se conserva separada; cachés de disco no controladas. No es latencia visual, prueba de literalidad ni medida de tablet.
Primera integración técnica; antes de evaluación completa, comprobar salida, cobertura de telemetría y comparabilidad con otros reconocedores.
