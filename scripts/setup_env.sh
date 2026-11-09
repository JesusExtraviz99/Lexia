#!/usr/bin/env bash
# Entornos de Lexia en Ubuntu; no modifica Python ni controladores del sistema.
# bash scripts/setup_env.sh transformers
# bash scripts/setup_env.sh transformers --gpu NUMERO_ASIGNADO
# Otros perfiles: whisper, crisper, vosk. Un perfil por entorno.
set -euo pipefail

ROOT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
PROJECT_DIR="$ROOT_DIR/entornos/servidor"
UV_VERSION="0.13.1"
PROFILE="${1:-}"
GPU_ID=""

usage() {
    echo "Uso: bash scripts/setup_env.sh {transformers|crisper|whisper|vosk} [--gpu N]"
    echo "Sin --gpu instala y comprueba importaciones; no hace la prueba de cálculo GPU."
}
case "$PROFILE" in
    transformers|crisper|whisper|vosk) shift ;;
    -h|--help|"") usage; exit 0 ;;
    *) usage; exit 2 ;;
esac
if [[ $# -gt 0 ]]; then
    [[ $# -eq 2 && "$1" == "--gpu" && "$2" =~ ^[0-9]+$ ]] || { usage; exit 2; }
    GPU_ID="$2"
fi
[[ "$(uname -s)" == "Linux" && "$(uname -m)" == "x86_64" ]] || {
    echo "Este archivo está preparado para Ubuntu/Linux x86_64." >&2; exit 1;
}
[[ -f "$PROJECT_DIR/uv.lock" ]] || { echo "Falta entornos/servidor/uv.lock; copia también esa carpeta." >&2; exit 1; }
[[ "$PROFILE" != "vosk" || -z "$GPU_ID" ]] || { echo "El perfil Vosk usa CPU." >&2; exit 2; }
if [[ -n "$GPU_ID" ]]; then
    command -v nvidia-smi >/dev/null || { echo "No se encuentra nvidia-smi." >&2; exit 1; }
    echo "GPU elegida; confirma que te ha sido asignada:"
    nvidia-smi -i "$GPU_ID" --query-gpu=index,name,driver_version,memory.used,memory.total --format=csv
fi

if command -v uv >/dev/null 2>&1; then
    UV_BIN="$(command -v uv)"
elif [[ -x "$HOME/.local/bin/uv" ]]; then
    UV_BIN="$HOME/.local/bin/uv"
else
    echo "Instalando uv $UV_VERSION solo para este usuario, sin modificar el PATH…"
    curl -LsSf "https://astral.sh/uv/$UV_VERSION/install.sh" | env UV_NO_MODIFY_PATH=1 sh
    UV_BIN="$HOME/.local/bin/uv"
fi
ACTUAL_UV="$("$UV_BIN" --version | awk '{print $2}')"
if [[ "$ACTUAL_UV" != "$UV_VERSION" ]]; then
    echo "uv existente: $ACTUAL_UV. Preparando uv $UV_VERSION aparte, sin sustituirlo…"
    curl -LsSf "https://astral.sh/uv/$UV_VERSION/install.sh" | env UV_UNMANAGED_INSTALL="$ROOT_DIR/.tools/uv-servidor" sh
    UV_BIN="$ROOT_DIR/.tools/uv-servidor/uv"
    ACTUAL_UV="$("$UV_BIN" --version | awk '{print $2}')"
    [[ "$ACTUAL_UV" == "$UV_VERSION" ]] || { echo "No se pudo preparar la versión de uv requerida." >&2; exit 1; }
fi

export UV_PROJECT_ENVIRONMENT="$ROOT_DIR/.venvs/servidor-$PROFILE"
export PYTHONHASHSEED=42
export TOKENIZERS_PARALLELISM=false
# Ningún perfil selecciona una GPU automáticamente ni modifica el driver.
if [[ -n "$GPU_ID" ]]; then export CUDA_VISIBLE_DEVICES="$GPU_ID"; else export CUDA_VISIBLE_DEVICES=""; fi

"$UV_BIN" sync --project "$PROJECT_DIR" --python 3.12.15 --managed-python --frozen --no-default-groups --extra "$PROFILE"
PYTHON_BIN="$UV_PROJECT_ENVIRONMENT/bin/python"
if [[ "$PROFILE" == "whisper" ]]; then
    NVIDIA_LIBS="$("$PYTHON_BIN" - <<'PY'
import nvidia.cublas, nvidia.cudnn
from pathlib import Path
print(':'.join(str(Path(p.__path__[0])/'lib') for p in (nvidia.cublas,nvidia.cudnn)))
PY
)"
    export LD_LIBRARY_PATH="$NVIDIA_LIBS${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"
fi
CHECK_ARGS=(--perfil "$PROFILE" --uv-version "$ACTUAL_UV")
if [[ -n "$GPU_ID" ]]; then CHECK_ARGS+=(--gpu "$GPU_ID"); fi
"$PYTHON_BIN" "$ROOT_DIR/scripts/comprobar_entorno_servidor.py" "${CHECK_ARGS[@]}"
echo "Entorno preparado: $UV_PROJECT_ENVIRONMENT"
echo "No se han descargado pesos ni ejecutado reconocimiento."
echo "Consulta entornos/servidor/LEEME.md para ejecutar después desde este entorno."
