# Preparar Lexia en el servidor con uv

Configuración preparada el 30/10/2026 para Ubuntu 20.04 x86_64 y el controlador NVIDIA 525.147.05 observado. El Python compartido 3.8 no se modifica: uv usa Python administrado 3.12.15. No se utiliza sudo ni se instalan controladores o un CUDA Toolkit del sistema.

## Reserva previa de GPU

Antes de iniciar cualquier trabajo GPU, registrar el uso en el calendario compartido Outlook **Uso de los servidores**, según la indicación de la empresa confirmada por el usuario el 04/11/2026. Título: `Deeplearning NOMBRE (GPU: IDs)`, indicando los índices físicos de nvidia-smi y el intervalo previsto con margen. Comprobar la zona horaria y las reservas existentes; actualizar la reserva si cambia el uso. La disponibilidad momentánea mostrada por nvidia-smi no sustituye esta reserva. Registrar cada grupo de GPU con la franja correspondiente para no mantener ocupadas en calendario las que ya se liberaron.

## Archivos necesarios

Conservar esta estructura dentro de la carpeta del proyecto del servidor:

```text
scripts/setup_env.sh
scripts/comprobar_entorno_servidor.py
entornos/servidor/pyproject.toml
entornos/servidor/uv.lock
entornos/servidor/LEEME.md
```

El instalador original suministrado por el usuario sirve como referencia; sus extras detect/vlm/dev pertenecen a otro proyecto. No se reutiliza aquel lockfile. Aquí el lockfile se generó con uv 0.13.1 y fija dependencias/artefactos de Linux x86_64. El script utiliza uv 0.13.1: si falta, lo instala para el usuario; si encuentra otra versión, prepara la versión fijada aparte en .tools/uv-servidor, sin reemplazar la existente. La instalación consulta PyPI y el índice oficial de PyTorch; los pesos no están en este paquete.

## Instalación por perfil

Desde la raíz del proyecto en el SSH:

```bash
bash scripts/setup_env.sh transformers
```

Ese primer comando prepara XLSR y Parakeet y comprueba importaciones. Sin --gpu se ocultan las GPU durante la comprobación; no se ejecuta cálculo en ellas. Para comprobar una GPU que te hayan asignado:

```bash
bash scripts/setup_env.sh transformers --gpu NUMERO_ASIGNADO
```

Sustituir NUMERO_ASIGNADO por su índice. No seleccionar una GPU por aparecer momentáneamente libre. La GPU física elegida aparece como cuda:0 dentro del proceso. Se usa una operación mínima de tensores, no reconocimiento ni benchmark.

Perfiles independientes (cada uno crea su propia carpeta .venvs/servidor-PERFIL):

| Perfil | Uso | Dependencias principales |
|---|---|---|
| transformers | XLSR y Parakeet | PyTorch 2.7.1+cu118, Transformers 5.20.2, Accelerate 1.15.0 |
| crisper | CrisperWhisper Small, backend Transformers | CrisperWhisper 2.0.3 y las mismas versiones de PyTorch/Transformers |
| whisper | Faster-Whisper | Faster-Whisper 1.2.1, CTranslate2 4.4.0, cuBLAS 12.1.3.1 y cuDNN 8.9.7.29 |
| vosk | Vosk Small español, CPU | Vosk 0.3.45 |

Ejecutar otros perfiles:

```bash
bash scripts/setup_env.sh crisper
bash scripts/setup_env.sh whisper
bash scripts/setup_env.sh vosk
```

Cada uno usa uv sync --frozen solo con su extra, sin modificar el lock ni el entorno de otro perfil. Los metadatos de las opciones no activadas también figuran en uv.lock: no significa que se instalen todos los modelos o perfiles.

## Compatibilidad y alcance real

PyTorch 2.7.1 se selecciona por su distribución oficial CUDA 11.8; no es la misma versión de CPU instalada en el portátil. CTranslate2 4.4.0 corresponde a la alternativa documentada para CUDA 12/cuDNN 8; no equivale a nuestro backend local más reciente. Estas diferencias deben figurar en las comparaciones, no atribuir todos los cambios a la GPU. Las bibliotecas CUDA se instalan en los entornos, sin sustituir el driver. El cálculo mínimo en la GPU real y la inferencia de cada modelo siguen pendientes hasta ejecutar en el servidor. Una resolución correcta de dependencias no demuestra compatibilidad completa de todos los modelos con esa GPU.

Los informes de comprobación van a resultados/entornos_servidor con versiones, huella de uv.lock, estado y GPU solicitada. Un fallo se registra y detiene el instalador; no cambia silenciosamente a CPU. El perfil whisper comprueba carga de sus bibliotecas y tipos de cálculo de CTranslate2; necesita una inferencia posterior para validar cuDNN con audio real. Vosk se comprueba en CPU. Ninguna comprobación descarga pesos ni usa los audios de MLS o las voces privadas.

## Ejecutar programas después

Para el perfil Transformers, desde la raíz:

```bash
CUDA_VISIBLE_DEVICES=NUMERO_ASIGNADO PYTHONHASHSEED=42 .venvs/servidor-transformers/bin/python PROGRAMA.py
```

PROGRAMA.py es un marcador. Desde el 04/11/2026 existe scripts/evaluar_asr_externo.py, inicialmente XLSR/MLS y ampliado después a cinco motores. EVALUAR_MLS.md documenta la primera integración; PRUEBA_PARALELA.md contiene las instrucciones vigentes de preparación y lanzamiento concurrente. Instalar el entorno no lanza la evaluación. Los adaptadores nuevos siguen pendientes de primera inferencia real en el servidor.

Tras la cohorte corta comprobada, MLS_DEV_COMPLETO.md documenta la actualización para dev completo, progreso por audio e inicio con nohup. Los cinco motores han completado diez audios en servidor según la auditoría local de resultados del 04/11/2026; la evaluación completa sigue pendiente de lanzamiento. Usar el paquete más reciente y conservar el piloto.

Faster-Whisper necesita además cargar las bibliotecas de su propio entorno antes de iniciar Python, como exige su documentación. Una forma de hacerlo es:

```bash
PYTHON_BIN="$PWD/.venvs/servidor-whisper/bin/python"
NVIDIA_LIBS="$("$PYTHON_BIN" -c 'from pathlib import Path; import nvidia.cublas, nvidia.cudnn; print(":".join(str(Path(p.__path__[0])/"lib") for p in (nvidia.cublas,nvidia.cudnn)))')"
LD_LIBRARY_PATH="$NVIDIA_LIBS${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}" CUDA_VISIBLE_DEVICES=NUMERO_ASIGNADO PYTHONHASHSEED=42 "$PYTHON_BIN" PROGRAMA.py
```

No activar globalmente esas rutas de bibliotecas: las del perfil PyTorch y las del perfil CTranslate2 no deben mezclarse.

Fuentes consultadas:
- https://docs.astral.sh/uv/guides/projects/
- https://docs.astral.sh/uv/guides/integration/pytorch/
- https://pytorch.org/get-started/previous-versions/
- https://github.com/SYSTRAN/faster-whisper#gpu
- https://docs.nvidia.com/deploy/cuda-compatibility/610/minor-version-compatibility.html

Validación local: resolución de dependencias y lock, revisión de perfiles y sintaxis Bash/Python. No instalación Linux ni prueba de GPU desde Windows. No se ejecuta el script suministrado por el usuario.

Actualización 04/11/2026: el usuario muestra instalación/importaciones y cálculo mínimo correctos del perfil transformers en Ubuntu, Python 3.12.15, PyTorch 2.7.1+cu118 y RTX 3060 12 GB (GPU física 0). Estado dependencias_y_gpu_comprobadas en su informe remoto. También confirma 2.408 audios dev y 2.385 test con transcripts.txt. No implica todavía carga de XLSR/Parakeet, inferencia o comprobación individual remota de todos los hashes extraídos.
