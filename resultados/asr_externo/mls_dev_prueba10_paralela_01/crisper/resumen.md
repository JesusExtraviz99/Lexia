# MLS · crisper · prueba offline

Partición: dev. Seleccionados: 10; completados: 10; fallos: 0.

WER global: 0.10752688172043011; CER global: 0.026476578411405296; RTF ASR: 0.22501249919301483.

| Audio | Estado | Duración s | WER | CER | ASR s | RTF |
|---|---|---:|---:|---:|---:|---:|
| 133_1378_000042 | ok | 19.9600 | 0.0000 | 0.0000 | 3.9999 | 0.2004 |
| 1075_567_000050 | ok | 11.1000 | 0.0800 | 0.0219 | 2.4468 | 0.2204 |
| 6223_5079_000063 | ok | 15.0400 | 0.0667 | 0.0175 | 3.2937 | 0.2190 |
| 3719_1378_000015 | ok | 11.5900 | 0.1250 | 0.0511 | 2.8160 | 0.2430 |
| 133_1378_000052 | ok | 15.5900 | 0.0556 | 0.0102 | 3.1729 | 0.2035 |
| 10367_10282_000004 | ok | 19.1200 | 0.0625 | 0.0110 | 3.4642 | 0.1812 |
| 3719_1378_000088 | ok | 12.5000 | 0.1818 | 0.0282 | 2.9433 | 0.2355 |
| 6671_9310_000004 | ok | 10.6600 | 0.2000 | 0.0374 | 2.4333 | 0.2283 |
| 2592_1378_000079 | ok | 12.6900 | 0.4643 | 0.1104 | 3.5226 | 0.2776 |
| 3719_1378_000049 | ok | 13.8300 | 0.0488 | 0.0185 | 3.8771 | 0.2803 |

Normalización: NFC; minúsculas; puntuación Unicode sustituida por espacios; espacios colapsados; conserva tildes, ñ y números. CER incluye espacios.

Configuración exacta del motor en ejecucion.json. Una pasada por audio, batch 1. Sin VAD externo, remuestreo o reducción de ruido. Endpointing/segmentación internos dependen del motor. Calentamiento excluido y conservado por sesión.
RTF ASR incluye preparación de entradas, transferencia, forward y decodificación; excluye lectura, métricas, escritura y carga del modelo. CUDA sincronizada al medir.
Los fallos no reciben WER cero: se excluyen del cálculo y quedan contados. Reanudar no reintenta resultados fallidos.
Recursos por sesión en sesiones/*.json, con muestras y alcance. La primera ejecución se conserva separada; cachés de disco no controladas. No es latencia visual, prueba de literalidad ni medida de tablet.
Primera integración técnica; antes de evaluación completa, comprobar salida, cobertura de telemetría y comparabilidad con otros reconocedores.
