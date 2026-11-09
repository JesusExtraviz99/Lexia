#!/usr/bin/env bash
# Ejecuta el lote ya autorizado con los cinco candidatos; no instala/descarga pesos.
# Uso: bash scripts/ejecutar_mls_dev_completo.sh 0 1 2 3
set -euo pipefail
ROOT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"
[[ $# -gt 0 ]] || { echo "Indica los índices GPU que puedes utilizar: 0 1 2 3" >&2; exit 2; }
for GPU_INDEX in "$@"; do
    [[ "$GPU_INDEX" =~ ^[0-9]+$ ]] || { echo "Índice GPU no válido." >&2; exit 2; }
done
[[ -f "$HOME/datasets_mls_evaluacion/mls_es/dev/transcripts.txt" ]] || {
    echo "No se encuentra MLS dev en la ruta prevista." >&2; exit 1;
}
COHORT_NAME="mls_dev_completo_paralela_01"
OUTPUT_DIR="$ROOT_DIR/resultados/asr_externo/$COHORT_NAME"
[[ ! -e "$OUTPUT_DIR" && ! -e "$OUTPUT_DIR.lanzador.log" && ! -e "$OUTPUT_DIR.pid" ]] || {
    echo "Ya existe salida/log/PID de este lote; no se sobrescribe ni se inicia otra copia." >&2; exit 1;
}
mkdir -p "$ROOT_DIR/resultados/asr_externo"
# nohup ignora SIGHUP; stdin cerrado y salida redirigida para no depender de SSH.
nohup "$ROOT_DIR/.venvs/servidor-transformers/bin/python" -u "$ROOT_DIR/scripts/lanzar_asr_paralelo.py" \
    --dataset "$HOME/datasets_mls_evaluacion/mls_es" \
    --gpus "$@" --limite 0 --completo --salida "$OUTPUT_DIR" \
    > "$OUTPUT_DIR.lanzador.log" 2>&1 < /dev/null &
LAUNCHER_PID=$!
printf '%s\n' "$LAUNCHER_PID" > "$OUTPUT_DIR.pid"
echo "Lanzador iniciado con PID $LAUNCHER_PID. Comprueba el progreso:"
echo "python3 scripts/estado_asr_externo.py resultados/asr_externo/$COHORT_NAME"
echo "Registro: $OUTPUT_DIR.lanzador.log"
echo "El PID solo confirma inicio del proceso; verifica el registro y los estados."
