# MLS · parakeet · prueba offline

Partición: dev. Seleccionados: 10; completados: 10; fallos: 0.

WER global: 0.06720430107526881; CER global: 0.017311608961303463; RTF ASR: 0.017619048725595478.

| Audio | Estado | Duración s | WER | CER | ASR s | RTF |
|---|---|---:|---:|---:|---:|---:|
| 133_1378_000042 | ok | 19.9600 | 0.0000 | 0.0000 | 0.3024 | 0.0151 |
| 1075_567_000050 | ok | 11.1000 | 0.0000 | 0.0000 | 0.1975 | 0.0178 |
| 6223_5079_000063 | ok | 15.0400 | 0.0222 | 0.0087 | 0.2439 | 0.0162 |
| 3719_1378_000015 | ok | 11.5900 | 0.0250 | 0.0057 | 0.2252 | 0.0194 |
| 133_1378_000052 | ok | 15.5900 | 0.0278 | 0.0051 | 0.2614 | 0.0168 |
| 10367_10282_000004 | ok | 19.1200 | 0.0208 | 0.0037 | 0.3242 | 0.0170 |
| 3719_1378_000088 | ok | 12.5000 | 0.0909 | 0.0169 | 0.2277 | 0.0182 |
| 6671_9310_000004 | ok | 10.6600 | 0.3500 | 0.1028 | 0.2333 | 0.0219 |
| 2592_1378_000079 | ok | 12.6900 | 0.3571 | 0.0859 | 0.2433 | 0.0192 |
| 3719_1378_000049 | ok | 13.8300 | 0.0244 | 0.0046 | 0.2444 | 0.0177 |

Normalización: NFC; minúsculas; puntuación Unicode sustituida por espacios; espacios colapsados; conserva tildes, ñ y números. CER incluye espacios.

Configuración exacta del motor en ejecucion.json. Una pasada por audio, batch 1. Sin VAD externo, remuestreo o reducción de ruido. Endpointing/segmentación internos dependen del motor. Calentamiento excluido y conservado por sesión.
RTF ASR incluye preparación de entradas, transferencia, forward y decodificación; excluye lectura, métricas, escritura y carga del modelo. CUDA sincronizada al medir.
Los fallos no reciben WER cero: se excluyen del cálculo y quedan contados. Reanudar no reintenta resultados fallidos.
Recursos por sesión en sesiones/*.json, con muestras y alcance. La primera ejecución se conserva separada; cachés de disco no controladas. No es latencia visual, prueba de literalidad ni medida de tablet.
Primera integración técnica; antes de evaluación completa, comprobar salida, cobertura de telemetría y comparabilidad con otros reconocedores.
