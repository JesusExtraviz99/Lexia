"""Descarga explícita del modelo; no procesa grabaciones."""
from pathlib import Path
from huggingface_hub import snapshot_download

ROOT = Path(__file__).resolve().parents[1]
snapshot_download(
    repo_id="Systran/faster-whisper-small",
    local_dir=ROOT / "modelos" / "faster-whisper-small",
    allow_patterns=["config.json", "model.bin", "tokenizer.json", "vocabulary.*", "preprocessor_config.json"],
)
print("Modelo preparado en modelos/faster-whisper-small")
