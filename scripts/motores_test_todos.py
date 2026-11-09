"""Despacho de los doce candidatos fijados; no incorpora nuevas variantes literales."""
from scripts import asr_motores_externos as previous
from scripts import ampliacion_motores as new

SPECS={key:dict(value) for key,value in {**previous.SPECS,**new.SPECS}.items()}
PACKAGES={**previous.PACKAGES,**new.PACKAGES}


def parameters(motor):
    return (new if motor in new.SPECS else previous).parameters(motor)


def check(folder,motor,sha):
    return (new if motor in new.SPECS else previous).check(folder,motor,sha)


def load(motor,folder,gpu,threads):
    return (new if motor in new.SPECS else previous).load(motor,folder,gpu,threads)
