# Primera prueba MLS en el servidor

Preparada el 04/11/2026. Este documento describe la primera integración XLSR/MLS. La ampliación a los cinco motores y el paquete completo vigente se documentan en PRUEBA_PARALELA.md; usar ese paquete, que incluye asr_motores_externos.py. Los comandos XLSR siguen disponibles, pero el TAR inicial de dos archivos conserva la versión anterior y no debe reextraerse sobre la ampliación.

## Modelo y protocolo

- XLSR: jonatasgrosman/wav2vec2-large-xlsr-53-spanish, revisión 96d7e9b4e4a78af515a3c6d3cee7c0826045d276. Apache-2.0; declara entrenamiento en Common Voice 6.1: no asumir independencia de todos los datasets externos.
- CPU o una GPU física explícita, float32, batch 1, CTC greedy sin modelo de lenguaje adicional. Semilla 42, cuatro hilos Torch, cudnn.benchmark desactivado; no se garantiza determinismo bit a bit entre dispositivos.
- Diez IDs de dev elegidos por orden inicial ordenado y mezcla pseudoaleatoria con semilla 42. Referencias, IDs, rutas relativas, huellas y orden se conservan en ejecucion.json. No es muestra estratificada ni evaluación final.
- Audios originales mono a 16 kHz, completos: sin VAD, denoising, concatenación, fragmentación o remuestreo. No se consulta el cuento ni se proporciona la referencia al ASR.
- Calentamiento con el primer audio seleccionado, repetido una vez por sesión y excluido de las métricas comparativas; su salida y tiempo se conservan. Modelo y carga medidos por separado. Cachés de disco no controladas.

## Transferir los archivos desde Windows

En una ventana **PowerShell local**, sin cerrar el SSH:

```powershell
cd 'C:\Users\PC\OneDrive\Documentos\ChatGPT\Practicas y TFG'
scp '.\.descartados\servidor\lexia_mls_evaluador.tar' '.\.descartados\servidor\lexia_mls_evaluador.tar.sha256' jextraviz@192.168.22.24:/opt/qaisc/home/jextraviz/
```

En **SSH**:

```bash
cd "$HOME"
sha256sum -c lexia_mls_evaluador.tar.sha256
tar -xf "$HOME/lexia_mls_evaluador.tar" -C "$HOME/lexia"
cd "$HOME/lexia"
```

El paquete contiene solo scripts/evaluar_asr_externo.py y este documento. No contiene voces, audios externos, pesos, entornos ni credenciales. No sustituye los archivos del instalador anterior. Comprobar OK antes de extraer.

## Descargar XLSR (~1,3 GB)

```bash
cd "$HOME/lexia"
CUDA_VISIBLE_DEVICES="" .venvs/servidor-transformers/bin/python -u scripts/evaluar_asr_externo.py descargar
```

Es una descarga oficial con revisión fijada. No utiliza GPU ni ejecuta ASR. La descarga se reanuda mediante Hugging Face; se contrastan hashes LFS cuando existen y se genera modelos/wav2vec2-xlsr-53-spanish/lexia_modelo.json. La evaluación usa exclusivamente archivos locales verificados; no ejecuta código remoto del modelo.

## Ejecutar diez audios de desarrollo

Comprobar disponibilidad/asignación de la GPU 0 antes de iniciar. En SSH:

```bash
cd "$HOME/lexia"
CUDA_VISIBLE_DEVICES=0 PYTHONHASHSEED=42 .venvs/servidor-transformers/bin/python -u scripts/evaluar_asr_externo.py evaluar \
  --dataset "$HOME/datasets_mls_evaluacion/mls_es" \
  --gpu 0 --particion dev --limite 10 --semilla 42 \
  --salida resultados/asr_externo/mls_dev_xlsr_prueba10
```

El índice --gpu es físico. Dentro del proceso solo queda visible esa tarjeta como cuda:0; se exige una GPU disponible y no se cambia automáticamente a CPU. Para una ejecución CPU omitir --gpu y usar otra carpeta de salida, evitando mezclar dispositivos. No dejar un ensayo largo dependiente de una sesión SSH que vaya a cerrarse; esta primera prueba corta permanece en primer plano.

Guardar la salida y revisar resumen.md antes de ampliar. Dev completo se solicitará con --limite 0 en otra carpeta tras la comprobación compartida. Test requiere --confirmar-test y configuración ya fijada; no se usa en esta prueba.

## Qué se guarda

- ejecucion.json: modelo/revisión/huellas, versiones, hardware disponible, configuración, selección exacta y firma de ejecución.
- audios/ID.json: referencia original, salida original, textos normalizados, alineamiento de palabras, WER/CER bruto y normalizado, aciertos, sustituciones, omisiones, inserciones, MER/WIL/WIP, coincidencia completa y salida vacía. IDs de frames CTC conservados, sin afirmar tiempos de palabra.
- Duración, tamaño, frames, frecuencia, pico, RMS/dBFS e indicador de amplitud próxima al límite. SNR, VAD y habla/silencios no medidos en este protocolo inicial.
- Por audio: lectura, preparación/transferencia, forward sincronizado CUDA, decodificación, ASR total, RTF, métricas y CPU hasta evaluación. Ventana temporal de cada audio en las muestras; RAM inicial/final y máximos de memoria del allocator Torch cuando hay GPU. No confundir la memoria de Torch con VRAM total.
- sesiones/*.json: importación/carga y calentamiento; CPU/RAM del proceso, hilos y RAM libre del sistema; muestras de la GPU física seleccionada (VRAM, utilización, utilización de memoria, potencia, temperatura y frecuencias si están disponibles). RAM solicitada cada 0,25 s y GPU aproximadamente cada segundo; se conservan intervalos reales y errores de lectura. El muestreo tiene coste y puede perder picos. La ampliación añade memoria privada/compartida cuando esté disponible, E/S, contexto del sistema, VRAM del PID y desgloses temporales por audio; consultar PRUEBA_PARALELA.md.
- Energía: integración trapezoidal de potencia solo entre muestras válidas cercanas. Se guarda cobertura temporal. Es energía estimada de la GPU completa durante ese intervalo, sin extrapolar extremos ni atribuirla exclusivamente al ASR. No se mide energía CPU/equipo/tablet.
- resumen.json, audios.csv y resumen.md: métricas globales ponderadas por palabras/caracteres y distribuciones por audio (media, mediana, desviación, p90/p95/p99/extremos), cobertura/fallos, velocidad. Fallos excluidos de precisión y siempre contados, sin WER ficticio de cero.

No se incluyen métricas específicas de literalidad o seguimiento: requieren nuestro dataset y referencias humanas. Tampoco se calculan todavía intervalos de confianza, desgloses por grupos ni energía por audio: las salidas detalladas permiten añadir análisis posteriores cuando estén definidas las comparaciones y haya cobertura suficiente. La prueba del servidor no determina consumo o rendimiento de tablet.

## Reanudar y errores

Los resultados se guardan atómicamente por audio y el resumen se actualiza tras cada uno. Al interrumpir con Ctrl+C, los completados permanecen. Repetir el mismo comando con --reanudar omite los archivos ya registrados y comprueba la firma: mismos datos, hashes, software, hardware y configuración. No admite cambios silenciosos ni reintenta fallos guardados; una ejecución con fallos conserva estado fallido. Corregir su causa y usar otra carpeta para repetir el ensayo. Un audio interrumpido puede tener que repetirse.

Una salida cuyo calentamiento/carga falla tendrá informe de sesión pero no transcripciones completadas. No presentar ese caso como evaluación de precisión. Revisar errores de memoria antes de intentar lotes más grandes.

## Fuentes y comprobaciones

- https://huggingface.co/jonatasgrosman/wav2vec2-large-xlsr-53-spanish/tree/96d7e9b4e4a78af515a3c6d3cee7c0826045d276
- https://huggingface.co/docs/huggingface_hub/en/package_reference/file_download
- https://huggingface.co/docs/transformers/model_doc/wav2vec2
- https://jitsi.github.io/jiwer/reference/process/
- https://docs.nvidia.com/deploy/nvidia-smi/index.html

Validación local con FLAC de ceros creados en carpeta temporal y ASR simulado: selección/IDs, normalización y errores, ponderación del corpus, energía sin extrapolación, guardado/reanudación y fallo persistido. No usa micrófono ni voces del banco, no ejecuta modelos ni acredita todavía inferencia en Linux. La comprobación GPU del instalador sí fue mostrada por el usuario el 04/11/2026 (RTX 3060, PyTorch 2.7.1+cu118); no sustituye esta primera inferencia.
