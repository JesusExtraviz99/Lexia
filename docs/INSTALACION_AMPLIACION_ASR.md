# Nuevos ASR instalados y pruebas preparadas · 06/11/2026

Descargados y cotejados diez checkpoints oficiales (~18,96 GB), revisiones completas y SHA256/LFS en resultados/instalacion_asr/ampliacion_20261106 y modelos/ampliacion_20261106. El usuario aclara que el requisito es gratuidad actual, no permiso comercial futuro. Crisper medium/turbo/large son gratuitos para investigación/no comercial: solo descarga, sin inferencias. Scribe/Speechmatics excluidos, sin cuenta/API/pagos. No se borra el Crisper histórico ni sus resultados.

Nuevo entorno local .tools/asr-ampliacion-env: Python 3.12.15, Torch/torchaudio 2.7.1 CPU y Transformers 5.20.2, dependencias fijadas en requirements_local_cpu_lock.txt. Los anteriores no se modifican.

## Qué está comprobado

Seis ASR cargan y transcriben un clip público MLS dev de 19,96 s, secuencialmente en CPU: Moonshine Tiny/Small español, Granite TurboCTC, Qwen0.6B-hf, Canary1Bv2 y Whisper large-v3-turbo. Es una comprobación funcional (incluye calentamiento), no un benchmark ni evidencia de generalización. Qwen1.7B-hf agotó memoria al cargar float32 en el ordenador de 15,7 GiB; queda pendiente para GPU del servidor, sin fallback o cambio silencioso de precisión. Intentos fallidos conservados y correcciones de integración (plantillas oficiales, dependencia de audio y límite del decodificador) registradas en el código final. Veintitrés pruebas simuladas correctas de adaptadores/evaluador/coordinador; sintaxis Bash verificada.

## Servidor aislado

El paquete se extrae bajo $HOME/lexia/experimentos/ampliacion_20261106. Lleva copias del evaluador/coordinador y scripts propios, entornos/lock nuevos y protocolo fijado. No sobrescribe los scripts o entornos del MLS test anterior. No incluye pesos/datasets/voces; la instalación descarga directamente de Hugging Face solo los siete ASR a ese directorio aislado (~12,7 GB). Las variantes literales permanecen descargadas localmente y no se lanzan en servidor.

PowerShell local:

```powershell
cd 'C:\Users\PC\OneDrive\Documentos\ChatGPT\Practicas y TFG'
scp '.\.descartados\servidor\lexia_ampliacion_asr.tar' '.\.descartados\servidor\lexia_ampliacion_asr.tar.sha256' jextraviz@192.168.22.24:/opt/qaisc/home/jextraviz/
```

SSH (se necesita autenticación del usuario, no enviar la contraseña al chat):

```bash
cd "$HOME"
sha256sum -c lexia_ampliacion_asr.tar.sha256 && tar -xf lexia_ampliacion_asr.tar -C "$HOME/lexia"
cd "$HOME/lexia/experimentos/ampliacion_20261106"
bash scripts/setup_ampliacion_asr.sh --descargar-asr
```

Se conserva uv 0.13.1 previamente instalado. Nuevo entorno .venvs/servidor-ampliacion con Torch/torchaudio cu118 y Transformers 5.20.2; sin tocar driver/Python compartido. GPU oculta durante instalación/importación. Revisar espacio disponible antes: pesos+entorno necesitan espacio adicional al proyecto anterior.

Después, reservar las GPU en Uso de los servidores y comprobar disponibilidad con nvidia-smi. No ocupar tarjetas de trabajos anteriores todavía activos; el coordinador solo toma libres de la lista autorizada y espera el resto, sin cancelar otros procesos.

```bash
nvidia-smi
bash scripts/ejecutar_ampliacion_dev10.sh 0 1 2 3
python3 scripts/estado_asr_externo.py resultados/asr_externo/mls_dev_nuevos_prueba10_01
```

Siete ASR, una tarea propia por GPU, cola para los restantes. Primeros diez dev reproducibles, mismos IDs que piloto anterior, batch1 float32, semilla42, sin VAD/limpieza/cuento proporcionado. Qwen fuerza español, Canary transcribe es→es; Whisper utiliza Transformers, no CT2, y sin tiempos de palabra: backend/configuración distintos deben constar al comparar coste. Las arquitecturas llamadas streaming se prueban aquí offline por clip, no mide latencia real.

Crisper no aparece en el registro de candidatos de prueba. El nuevo lote no usa test. Tras revisar carga GPU, límites de generación, cobertura y salidas se decidirá el lote grande; no lanzar todo automáticamente tras errores. Misma instrumentación de precisión, tiempos y recursos que el evaluador original, con versiones nuevas registradas. No se afirma aún que exista una ejecución GPU remota ni se publica nada.
