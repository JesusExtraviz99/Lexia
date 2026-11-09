# Prueba corta concurrente de los cinco reconocedores

04/11/2026. Diez audios de MLS dev, semilla 42, una pasada por motor y un calentamiento excluido por sesión. No se usa test ni voces privadas. Los cinco reciben IDs, referencias y archivos idénticos; el lanzador comprueba igualdad de los manifiestos al terminar. No se considera aún evaluación completa ni selección final de candidatos.

## Estado comprobado y límites

El usuario ha descargado/verificado XLSR y ha mostrado la prueba mínima GPU correcta del entorno Transformers en la RTX 3060. Los otros adaptadores y el coordinador tienen comprobaciones locales con modelos/procesos simulados; la inferencia real remota de los cinco sigue pendiente. No se afirma que ya funcionen todos en Linux. No se ha ejecutado reconocimiento local sobre ninguna grabación.

El nuevo paquete sustituye código y documentación del evaluador, conserva los pesos descargados y añade los módulos necesarios. No reextraer posteriormente el TAR inicial lexia_mls_evaluador.tar de dos archivos: contiene el evaluador anterior. Los resultados de versiones distintas no se mezclan.

## 1. Transferir paquete completo

PowerShell local:

```powershell
cd 'C:\Users\PC\OneDrive\Documentos\ChatGPT\Practicas y TFG'
scp '.\.descartados\servidor\lexia_asr_paralelo.tar' '.\.descartados\servidor\lexia_asr_paralelo.tar.sha256' jextraviz@192.168.22.24:/opt/qaisc/home/jextraviz/
```

Terminal SSH:

```bash
cd "$HOME"
sha256sum -c lexia_asr_paralelo.tar.sha256 && tar -xf lexia_asr_paralelo.tar -C "$HOME/lexia"
cd "$HOME/lexia"
bash scripts/preparar_asr_paralelo.sh
```

La preparación es secuencial: comprueba/instala los cuatro perfiles con uv y descarga pesos verificados. Puede descargar varios GB de dependencias y unos 5,3 GB de modelos en total. XLSR ya descargado se reutiliza/verifica, no se elimina. Sin micrófono, ASR ni uso GPU durante la preparación. No cambia Python, driver, lock ni dependencias del sistema. Crea un entorno por perfil.

## 2. Comprobar plan y GPU antes del ensayo

El usuario debe disponer de autorización/asignación para las GPU que enumere. El lanzador no reserva recursos en el servicio de la empresa. Si existe una cola institucional, coordinar con ella; no competir por una tarjeta por aparecer momentáneamente libre.

```bash
cd "$HOME/lexia"
nvidia-smi
.venvs/servidor-transformers/bin/python scripts/lanzar_asr_paralelo.py \
  --dataset "$HOME/datasets_mls_evaluacion/mls_es" \
  --gpus 0 1 2 3 --limite 10 \
  --salida resultados/asr_externo/mls_dev_prueba10_paralela_01 --plan
```

--plan solo muestra configuración. Omitir --plan inicia el ensayo. Usar carpeta de salida nueva. Puede limitarse --gpus a una o varias GPU asignadas: encola los motores restantes y reutiliza las plazas al terminar sus propios procesos. Antes de cada lanzamiento comprueba que no aparecen procesos de cómputo en la tarjeta; esto no es reserva atómica frente a otros usuarios.

Con cuatro plazas disponibles, normalmente XLSR/Parakeet/Whisper/Crisper ocupan 0/1/2/3. Vosk usa CPU del mismo servidor en paralelo, con CUDA oculta. El orden cambia si alguna plaza está ocupada: el índice realmente usado se guarda siempre. No se sustituyen automáticamente backends GPU por CPU.

Mantener SSH abierto durante esta prueba corta. Ctrl+C solicita interrupción únicamente a los procesos hijos del lanzador, dándoles oportunidad de guardar; si requieren terminación forzada, el último audio o la telemetría final pueden quedar incompletos. Los archivos por audio ya guardados permanecen. Repetir la prueba con carpeta nueva; reanudación individual requiere mismo código/configuración/huellas y no reintenta errores guardados.

## Modelos y configuración inicial

| Motor | Perfil | Pesos fijados | Configuración |
|---|---|---|---|
| XLSR español | transformers | 96d7e9b4e4a78af515a3c6d3cee7c0826045d276 | float32, CTC greedy sin LM |
| Parakeet TDT v3 | transformers | 541d1f99c6b0c3cd0b11a95167540bb8edefd82b | float32, generate, máximo 512 tokens, idioma automático |
| Faster-Whisper Small | whisper | 536b0662742c02347bc0e980a01041f333bce120 | float32, español, beam 5, temperatura 0, sin texto previo, tiempos de palabra |
| CrisperWhisper2 Small | crisper | bcaecf0a584a1f600d8897fe6032b9e2e56429a7 | Transformers float32, verbatim/es, reparaciones/fallback nativos y tiempos de palabra, máximo 256 tokens |
| Vosk Small es 0.42 | vosk | ZIP SHA256 09b239888f633ef2f0b4e09736e3d9936acfd810bc65d53fad45261762c6511f | CPU, grafo nativo, PCM16, conserva resultados intermedios y final |

Las precisiones y decodificadores son propios de cada implementación; esta comparación no aísla arquitectura ni entrenamiento. Vosk CPU y modelos GPU se etiquetan por separado. Crisper conserva licencia de investigación no comercial y soporte declarado principalmente en inglés/alemán; no asumir optimización para español. Su modo verbatim forma parte del candidato, sin evaluar aún métricas específicas de disfluencia. Sin cuento, transcripción de referencia ni hotwords en el reconocedor.

Faster-Whisper utiliza solo las bibliotecas CUDA de su entorno, mediante LD_LIBRARY_PATH del proceso. No mezcla esas rutas con Torch ni las exporta globalmente. CT2 consume por completo el generador de segmentos antes de finalizar el cronómetro. XLSR/Parakeet sincronizan CUDA; Crisper sincroniza su llamada completa. Se conserva segmentación interna de cada motor y detalles de salida; no hay VAD/limpieza externos ni ventanas deslizantes 4/8 s. MLS se procesa archivo a archivo sin concatenarlos. Batch 1, cuatro hilos solicitados, límites OMP/MKL/OpenBLAS/NumExpr registrados; hilos nativos Vosk no se garantizan.

## Datos recogidos

- Por audio: hash, ID, lector/libro MLS, referencia, duración, bytes/frames/frecuencia, pico, RMS/dBFS e indicador de amplitud límite; texto original, normalizado y salidas nativas cuando existen. WER/CER bruto y normalizado, alineamiento, aciertos, sustituciones, omisiones, inserciones, MER/WIL/WIP, coincidencia exacta y salida vacía.
- Tiempos: carga/importación y calentamiento separados; lectura de audio, preparación/transferencia, forward, decodificación si el backend expone esas etapas, llamada nativa completa y ASR total. Métricas y CPU hasta evaluación. Etapas internas inseparables se guardan como null: no se inventa tiempo de forward en CT2/Crisper/Vosk. El tiempo global de sesión incluye muestreo y escritura; RTF ASR no los incluye.
- Proceso: CPU de usuario/sistema, hilos, afinidad cuando disponible, RSS/VMS; USS/PSS/compartida según sistema, pico de vida Linux, cambios de contexto, contadores de E/S. Fotos antes/después de carga y cada audio; muestras CPU/RAM cada 0,25 s solicitado, intervalos reales conservados. Memoria de Torch asignada/reservada y máximos por audio cuando utiliza Torch.
- GPU seleccionada: UUID/modelo/controlador/memoria total; muestras de VRAM global, utilización, utilización de memoria, potencia, temperatura y frecuencias. VRAM atribuida al PID si está disponible y número de otros procesos de cómputo; no se guardan sus comandos. Detalle NVIDIA antes/después de la sesión sobre estado de rendimiento, límites y motivos de reducción reportados. Consulta GPU aproximadamente cada segundo, tiempo de consulta e intervalos reales guardados.
- Servidor: modelo CPU, núcleos, CPU global, RAM, swap, carga del sistema, espacio libre del dataset, E/S global, frecuencia CPU y sensores disponibles. Instantáneas globales se etiquetan como compartidas, no consumo exclusivo del reconocedor. Tamaño lógico del entorno, tamaño de pesos y cantidad de parámetros cuando el adaptador puede obtenerla sin duplicar carga.
- Energía GPU estimada solo entre muestras válidas próximas, con cobertura temporal. Se conserva por sesión e intervalo observado de audio; para clips cortos puede ser null. Sin extrapolar extremos ni atribuirlo al ASR/CPU/equipo completo. Máximos muestreados no son picos garantizados. Frecuencia de sensores y overhead limitan la precisión.
- Reproducibilidad: versiones de todos los paquetes, huellas de scripts/modelos, configuración, semilla, precisión, GPU física, UTC de inicio/final, PID propio y cohorte. El coordinador permite reconstruir solapamientos. Resultados, fallos y logs independientes; no se ocultan audios fallidos.

Se guardan referencias humanas externas tal como vienen del dataset: integridad del archivo no certifica exactitud de referencia. No se calculan eventos del lector/seguimiento con estos datos externos. No se mide batería/tablet, FLOPs ni energía CPU. SNR, tiempos humanos y métricas de silencio requieren referencias/métodos adicionales; quedan no disponibles. Precisión y recursos concurrentes son un primer control técnico, no resultados definitivos de rendimiento aislado.

## Resultados y revisión compartida

Carpeta de cohorte: cohorte.json con procesos, GPU, inicio/final/estado, selección y resumen; un .log por motor. Subcarpetas xlsr/parakeet/whisper/crisper/vosk con ejecucion.json, audios/*.json, sesiones/*.json, resumen.json, audios.csv y resumen.md. Las muestras también se escriben incrementalmente y se vacía el búfer en sesiones/*.jsonl: permite conservar observaciones previas a un cierre inesperado, aunque no garantiza la última muestra ante fallo de disco/sistema. Verificar completados=10, fallos=0, misma selección, transcripciones plausibles, GPU realmente utilizada y telemetría presente antes de ampliar. Un fallo de un reconocedor no convierte sus resultados en cero ni impide que terminen los otros; revisar su log.

El objetivo actual es comprobar el circuito de los cinco motores, no elegir un ganador con diez audios. Después realizar desarrollo completo y una selección fija de mediciones aisladas para separar interferencia de CPU/RAM/disco. Se conserva test sin ajustar configuraciones contra él.

Validación local: trece pruebas con entradas sintéticas, módulos/procesos simulados y sin reconocimiento real; sintaxis Python y Bash comprobada al empaquetar. Fuentes de APIs: documentación instalada de Crisper 2.0.3, https://huggingface.co/docs/transformers/model_doc/wav2vec2 , https://huggingface.co/docs/huggingface_hub/en/package_reference/file_download , https://github.com/SYSTRAN/faster-whisper , https://github.com/alphacep/vosk-api y https://docs.nvidia.com/deploy/nvidia-smi/index.html .
