"""Métricas/recursos originales con despacho a cada adaptador sin cambiar sus parámetros."""
from pathlib import Path
import sys
if __package__ in (None,''):
    sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from scripts import evaluar_asr_externo as evaluator
from scripts import motores_test_todos
if __name__=='__main__':
    evaluator.motors=motores_test_todos
    evaluator.main()
