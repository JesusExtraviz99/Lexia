"""Coordinador de nuevos ASR; nunca ejecuta variantes literales ni modifica scripts previos."""
from pathlib import Path
import sys
if __package__ in (None, ''):
    sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from scripts import lanzar_asr_paralelo as launcher
from scripts import ampliacion_motores

if __name__=='__main__':
    if '--particion' in sys.argv and sys.argv[sys.argv.index('--particion')+1]!='dev':
        raise SystemExit('Nuevos candidatos: primero desarrollo en dev, no test.')
    original_job_command=launcher.job_command
    def command(*args,**kwargs):
        result=original_job_command(*args,**kwargs)
        result[2]=str(launcher.ROOT/'scripts/evaluar_ampliacion_asr.py')
        return result
    launcher.motors=ampliacion_motores
    launcher.job_command=command
    launcher.main()
