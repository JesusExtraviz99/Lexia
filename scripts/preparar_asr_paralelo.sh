#!/usr/bin/env bash
# Solo instala/comprueba dependencias y descarga pesos; no ejecuta ASR.
set -euo pipefail
ROOT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"
for PROFILE in transformers whisper crisper vosk; do
    bash scripts/setup_env.sh "$PROFILE"
done
# La descarga no necesita importar el framework de cada modelo: usa HF del entorno Transformers.
export CUDA_VISIBLE_DEVICES=""
for MOTOR in xlsr parakeet whisper crisper vosk; do
    .venvs/servidor-transformers/bin/python -u scripts/evaluar_asr_externo.py descargar --motor "$MOTOR"
done
echo "Entornos y pesos preparados. Aún no se han transcrito audios."
echo "Consulta entornos/servidor/PRUEBA_PARALELA.md antes de lanzar."
