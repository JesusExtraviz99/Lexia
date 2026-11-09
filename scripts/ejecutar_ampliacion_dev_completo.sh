#!/usr/bin/env bash
set -euo pipefail
ROOT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"
[[ $# -gt 0 ]] || { echo "Indica GPU autorizadas: 0 1 2 3" >&2; exit 2; }
for GPU_ID in "$@"; do
    [[ "$GPU_ID" =~ ^[0-3]$ ]] || { echo "GPU fuera de 0–3" >&2; exit 2; }
done
PILOT_NAME="${LEXIA_PILOTO_COHORTE:-mls_dev_nuevos_prueba10_02}"
[[ "$PILOT_NAME" =~ ^mls_dev_nuevos_prueba10_[0-9]+$ ]] || { echo "Piloto no permitido" >&2; exit 2; }
PYTHON_BIN="$ROOT_DIR/.venvs/servidor-ampliacion/bin/python"
"$PYTHON_BIN" -m scripts.validar_piloto_ampliacion "resultados/asr_externo/$PILOT_NAME"
OUTPUT_DIR="$ROOT_DIR/resultados/asr_externo/mls_dev_nuevos_completo_01"
[[ ! -e "$OUTPUT_DIR" && ! -e "$OUTPUT_DIR.lanzador.log" && ! -e "$OUTPUT_DIR.pid" ]] || { echo "Salida previa: no sobrescribir" >&2; exit 1; }
mkdir -p "$ROOT_DIR/resultados/asr_externo"
nohup "$PYTHON_BIN" -u scripts/lanzar_ampliacion_asr.py \
    --dataset "$HOME/datasets_mls_evaluacion/mls_es" --gpus "$@" --limite 0 --completo --salida "$OUTPUT_DIR" \
    > "$OUTPUT_DIR.lanzador.log" 2>&1 < /dev/null &
printf '%s\n' "$!" > "$OUTPUT_DIR.pid"
echo "Lanzador iniciado. Verificar log y progreso; el PID no garantiza ejecución correcta."
echo "python3 scripts/estado_asr_externo.py resultados/asr_externo/mls_dev_nuevos_completo_01"
