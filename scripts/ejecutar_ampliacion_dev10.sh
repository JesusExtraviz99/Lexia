#!/usr/bin/env bash
set -euo pipefail
ROOT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"
[[ $# -gt 0 ]] || { echo "Indica GPU autorizadas: 0 1 2 3" >&2; exit 2; }
for GPU_ID in "$@"; do
    [[ "$GPU_ID" =~ ^[0-3]$ ]] || { echo "GPU fuera de 0–3" >&2; exit 2; }
done
COHORT_NAME="${LEXIA_AMPLIACION_COHORTE:-mls_dev_nuevos_prueba10_01}"
[[ "$COHORT_NAME" =~ ^mls_dev_nuevos_prueba10_[0-9]+$ ]] || { echo "Nombre de cohorte no permitido" >&2; exit 2; }
OUTPUT_DIR="$ROOT_DIR/resultados/asr_externo/$COHORT_NAME"
[[ ! -e "$OUTPUT_DIR" && ! -e "$OUTPUT_DIR.lanzador.log" && ! -e "$OUTPUT_DIR.pid" ]] || { echo "Salida previa: no sobrescribir" >&2; exit 1; }
mkdir -p "$ROOT_DIR/resultados/asr_externo"
nohup "$ROOT_DIR/.venvs/servidor-ampliacion/bin/python" -u scripts/lanzar_ampliacion_asr.py \
    --dataset "$HOME/datasets_mls_evaluacion/mls_es" --gpus "$@" --limite 10 --salida "$OUTPUT_DIR" \
    > "$OUTPUT_DIR.lanzador.log" 2>&1 < /dev/null &
printf '%s\n' "$!" > "$OUTPUT_DIR.pid"
echo "Iniciado lanzador; comprobar log/progreso. Nuevos ASR, sin literales."
echo "python3 scripts/estado_asr_externo.py resultados/asr_externo/$COHORT_NAME"
