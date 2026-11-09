#!/usr/bin/env bash
# Test oficial con configuraciones fijadas; no modifica modelos/datos/entornos.
set -euo pipefail
ROOT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"
[[ $# -gt 0 ]] || { echo "Indica GPU autorizadas: 0 1 2 3" >&2; exit 2; }
for GPU_INDEX in "$@"; do
    [[ "$GPU_INDEX" =~ ^[0-3]$ ]] || { echo "Solo GPU 0, 1, 2 o 3 explícitas." >&2; exit 2; }
done
[[ -f "$HOME/datasets_mls_evaluacion/mls_es/test/transcripts.txt" ]] || {
    echo "No se encuentra MLS test en la ruta prevista." >&2; exit 1;
}
COHORT_NAME="mls_test_completo_paralela_01"
OUTPUT_DIR="$ROOT_DIR/resultados/asr_externo/$COHORT_NAME"
[[ ! -e "$OUTPUT_DIR" && ! -e "$OUTPUT_DIR.lanzador.log" && ! -e "$OUTPUT_DIR.pid" ]] || {
    echo "Salida/log/PID existentes; no se sobrescribe ni se inicia otra copia." >&2; exit 1;
}
mkdir -p "$ROOT_DIR/resultados/asr_externo"
nohup "$ROOT_DIR/.venvs/servidor-transformers/bin/python" -u "$ROOT_DIR/scripts/lanzar_asr_paralelo.py" \
    --dataset "$HOME/datasets_mls_evaluacion/mls_es" --particion test --confirmar-test \
    --gpus "$@" --motores xlsr parakeet whisper crisper vosk --limite 0 --completo --salida "$OUTPUT_DIR" \
    > "$OUTPUT_DIR.lanzador.log" 2>&1 < /dev/null &
LAUNCHER_PID=$!
printf '%s\n' "$LAUNCHER_PID" > "$OUTPUT_DIR.pid"
echo "Lanzador iniciado: PID $LAUNCHER_PID. Verifica estado y log; el PID solo confirma el inicio."
echo "python3 scripts/estado_asr_externo.py resultados/asr_externo/$COHORT_NAME"
echo "Registro: $OUTPUT_DIR.lanzador.log"
