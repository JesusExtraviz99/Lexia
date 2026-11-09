"""Punto de entrada aislado: reutiliza métricas y telemetría, solo nuevos ASR."""
from pathlib import Path
import sys

if __package__ in (None, ''):
    sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from scripts import evaluar_asr_externo as evaluator
from scripts import ampliacion_motores

if __name__=='__main__':
    evaluator.motors=ampliacion_motores
    evaluator.main()
