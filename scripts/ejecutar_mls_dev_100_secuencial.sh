#!/usr/bin/env bash
# Cuatro candidatos para alimentar al seguidor; no ejecuta reglas del seguidor.
set -euo pipefail
ROOT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"
[[ $# -eq 1 && ( "$1" == 0 || "$1" == 1 ) ]] || {
    echo "Uso: bash scripts/ejecutar_mls_dev_100_secuencial.sh 0 (o 1, solo GPU autorizadas)" >&2; exit 2;
}
[[ -f "$HOME/datasets_mls_evaluacion/mls_es/dev/transcripts.txt" ]] || {
    echo "No se encuentra MLS dev en la ruta prevista." >&2; exit 1;
}
COHORT_NAME="mls_dev_100_secuencial_sin_crisper_01"
OUTPUT_DIR="$ROOT_DIR/resultados/asr_externo/$COHORT_NAME"
[[ ! -e "$OUTPUT_DIR" && ! -e "$OUTPUT_DIR.lanzador.log" && ! -e "$OUTPUT_DIR.pid" ]] || {
    echo "Salida/log/PID existentes; no se sobrescribe ni se inicia otra copia." >&2; exit 1;
}
mkdir -p "$ROOT_DIR/resultados/asr_externo"
nohup "$ROOT_DIR/.venvs/servidor-transformers/bin/python" -u "$ROOT_DIR/scripts/lanzar_asr_paralelo.py" \
    --dataset "$HOME/datasets_mls_evaluacion/mls_es" --gpus "$1" --secuencial \
    --motores xlsr parakeet whisper vosk --limite 100 --salida "$OUTPUT_DIR" \
    > "$OUTPUT_DIR.lanzador.log" 2>&1 < /dev/null &
LAUNCHER_PID=$!
printf '%s\n' "$LAUNCHER_PID" > "$OUTPUT_DIR.pid"
echo "Lanzador iniciado: PID $LAUNCHER_PID. Verifica el estado; el PID solo confirma el inicio."
echo "python3 scripts/estado_asr_externo.py resultados/asr_externo/$COHORT_NAME"
echo "Registro: $OUTPUT_DIR.lanzador.log"
