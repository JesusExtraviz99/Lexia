#!/usr/bin/env bash
set -euo pipefail
ROOT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"
[[ $# -gt 0 ]] || { echo "Indica GPU autorizadas: 0 1 2 3" >&2; exit 2; }
for GPU_ID in "$@"; do
    [[ "$GPU_ID" =~ ^[0-3]$ ]] || { echo "GPU fuera de 0–3" >&2; exit 2; }
done
OUTPUT_DIR="$ROOT_DIR/resultados/asr_externo/mls_test_todos_01"
[[ ! -e "$OUTPUT_DIR" && ! -e "$OUTPUT_DIR.lanzador.log" && ! -e "$OUTPUT_DIR.pid" && ! -e "$OUTPUT_DIR.preparacion.json" ]] || { echo "Salida/log/PID previos; no se sobrescribe" >&2; exit 1; }
mkdir -p "$ROOT_DIR/resultados/asr_externo"
PYTHON_BIN="$HOME/lexia/.venvs/servidor-transformers/bin/python"
nohup "$PYTHON_BIN" -u scripts/lanzar_test_todos.py \
    --root-anteriores "$HOME/lexia" --root-nuevos "$HOME/lexia/experimentos/ampliacion_20261106" \
    --dataset "$HOME/datasets_mls_evaluacion/mls_es" --gpus "$@" --salida "$OUTPUT_DIR" \
    > "$OUTPUT_DIR.lanzador.log" 2>&1 < /dev/null &
printf '%s\n' "$!" > "$OUTPUT_DIR.pid"
echo "Lanzador con nohup iniciado; verificar log y progreso. PID no garantiza arranque correcto."
echo "python3 scripts/estado_asr_externo.py resultados/asr_externo/mls_test_todos_01"
echo "Registro: $OUTPUT_DIR.lanzador.log"
