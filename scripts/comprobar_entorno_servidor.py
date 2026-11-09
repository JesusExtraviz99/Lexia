"""Comprobar dependencias y cálculo mínimo; no carga reconocedores ni audios."""
import argparse
from datetime import datetime, timezone
import hashlib
import importlib
import importlib.metadata
import json
import os
from pathlib import Path
import platform
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--perfil', required=True, choices=['transformers','crisper','whisper','vosk'])
    parser.add_argument('--gpu', type=int)
    parser.add_argument('--uv-version', required=True)
    args = parser.parse_args()
    result = dict(created_at_utc=datetime.now(timezone.utc).isoformat(), profile=args.perfil,
        python=sys.version, executable=sys.executable, platform=platform.platform(),
        uv_version=args.uv_version, packages={}, gpu_requested=args.gpu,
        cuda_visible_devices=os.environ.get('CUDA_VISIBLE_DEVICES'),
        lock_sha256=hashlib.sha256((ROOT/'entornos/servidor/uv.lock').read_bytes()).hexdigest(),
        scope='Importación y prueba mínima de dependencias; sin modelos, audios, inferencias ASR o medidas de rendimiento.')
    pairs = [('numpy','numpy'),('soundfile','soundfile'),('psutil','psutil'),('jiwer','jiwer')]
    if args.perfil in ('transformers','crisper'):
        pairs += [('torch','torch'),('transformers','transformers'),('accelerate','accelerate'),('librosa','librosa')]
    if args.perfil == 'crisper':
        pairs += [('crisperwhisper','crisperwhisper')]
    if args.perfil == 'whisper':
        pairs += [('faster-whisper','faster_whisper'),('ctranslate2','ctranslate2'),('av','av')]
    if args.perfil == 'vosk':
        pairs += [('vosk','vosk')]
    folder = ROOT/'resultados/entornos_servidor'
    folder.mkdir(parents=True, exist_ok=True)
    output = folder/f'{datetime.now(timezone.utc):%Y%m%d_%H%M%S_%f}_{args.perfil}.json'
    try:
        for package, module in pairs:
            importlib.import_module(module)
            result['packages'][package] = importlib.metadata.version(package)
        if args.perfil in ('transformers','crisper'):
            import torch
            from transformers import AutoModelForCTC, AutoModelForTDT, AutoProcessor
            result['torch_cuda_build'] = torch.version.cuda
            if args.gpu is not None:
                if not torch.cuda.is_available():
                    raise RuntimeError('PyTorch no puede utilizar la GPU seleccionada.')
                if torch.cuda.device_count() != 1:
                    raise RuntimeError('Se esperaba una sola GPU visible.')
                result['gpu_name'] = torch.cuda.get_device_name(0)
                values = torch.arange(4, dtype=torch.float32, device='cuda')
                if (values @ values).item() != 14:
                    raise RuntimeError('La prueba de cálculo GPU no coincide.')
                torch.cuda.synchronize()
        if args.perfil == 'crisper':
            from crisperwhisper import CrisperWhisperModel
        if args.perfil == 'whisper' and args.gpu is not None:
            import ctypes
            for library in ('libcublas.so.12','libcudnn.so.8'):
                ctypes.CDLL(library)
            import ctranslate2
            result['supported_compute_types'] = sorted(ctranslate2.get_supported_compute_types('cuda',0))
            if not result['supported_compute_types']:
                raise RuntimeError('CTranslate2 no reconoce tipos de cálculo GPU.')
        if args.gpu is not None:
            result['nvidia_smi'] = subprocess.check_output(['nvidia-smi','-i',str(args.gpu),
                '--query-gpu=index,name,driver_version,memory.total','--format=csv,noheader'],text=True).strip()
        result['status'] = 'dependencias_y_gpu_comprobadas' if args.gpu is not None else 'dependencias_comprobadas_gpu_pendiente'
        if args.perfil == 'vosk':
            result['status'] = 'dependencias_cpu_comprobadas'
    except Exception as exc:
        result['status'] = 'error'
        result['error'] = f'{type(exc).__name__}: {exc}'
        raise
    finally:
        output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        print(json.dumps(result,ensure_ascii=False,indent=2),flush=True)
        print('Comprobación guardada:',output,flush=True)


if __name__ == '__main__':
    main()
