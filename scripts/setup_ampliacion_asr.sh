#!/usr/bin/env bash
set -euo pipefail
ROOT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"
[[ $# -eq 0 || ( $# -eq 1 && "$1" == --descargar-asr ) ]] || { echo "Uso: bash scripts/setup_ampliacion_asr.sh [--descargar-asr]" >&2; exit 2; }
DOWNLOAD_ASR="${1:-}"
[[ "$(uname -s)" == Linux && "$(uname -m)" == x86_64 ]] || { echo "Solo Linux x86_64" >&2; exit 2; }
if [[ -x "$ROOT_DIR/.tools/uv-servidor/uv" ]]; then
    UV_BIN="$ROOT_DIR/.tools/uv-servidor/uv"
elif command -v uv >/dev/null 2>&1; then
    UV_BIN="$(command -v uv)"
else
    UV_BIN="$HOME/.local/bin/uv"
fi
[[ -x "$UV_BIN" ]] || { echo "Falta uv previamente preparado" >&2; exit 1; }
[[ "$("$UV_BIN" --version | awk '{print $2}')" == 0.13.1 ]] || { echo "Se requiere uv 0.13.1" >&2; exit 1; }
export UV_PROJECT_ENVIRONMENT="$ROOT_DIR/.venvs/servidor-ampliacion"
export CUDA_VISIBLE_DEVICES=""
"$UV_BIN" sync --project entornos/ampliacion --python 3.12.15 --managed-python --frozen --no-default-groups
"$UV_PROJECT_ENVIRONMENT/bin/python" -c 'import torch,transformers; print("Dependencias importadas:",torch.__version__,transformers.__version__,"sin inferencia GPU")'
echo "Entorno nuevo preparado. Los entornos previos no se modifican."
echo "Descarga/verificación solo de ASR nuevos:"
echo '.venvs/servidor-ampliacion/bin/python -m scripts.preparar_ampliacion_asr descargar --modelos moonshine_tiny_es moonshine_small_es granite_turboctc qwen_asr_06b qwen_asr_17b canary_v2 whisper_turbo'
if [[ "$DOWNLOAD_ASR" == --descargar-asr ]]; then
    "$UV_PROJECT_ENVIRONMENT/bin/python" -u -m scripts.preparar_ampliacion_asr descargar \
        --modelos moonshine_tiny_es moonshine_small_es granite_turboctc qwen_asr_06b qwen_asr_17b canary_v2 whisper_turbo
fi
