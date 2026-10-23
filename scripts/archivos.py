"""Guardado de texto por sustitución, con reintentos limitados de errores de acceso."""
import errno
import os
from pathlib import Path
import tempfile
import time


def _write_once(path, text):
    descriptor, name = tempfile.mkstemp(prefix=f'.{path.name}.', suffix='.tmp', dir=path.parent)
    temporary = Path(name)
    try:
        with os.fdopen(descriptor, 'w', encoding='utf-8', newline='') as stream:
            stream.write(text)
        # El temporal está cerrado antes de sustituir el destino en Windows.
        os.replace(temporary, path)
    finally:
        try:
            temporary.unlink(missing_ok=True)
        except OSError:
            pass


def write_text_atomic(path, text):
    """Conservar el destino anterior si no se puede completar la sustitución.

    Cuatro intentos como máximo. No reintentar errores de disco lleno/ruta ausente.
    El llamador recibe el último error si el problema persiste.
    """
    path = Path(path)
    for attempt in range(4):
        try:
            _write_once(path, text)
            return
        except OSError as exc:
            retryable = exc.errno in (errno.EINVAL, errno.EACCES, errno.EPERM, errno.EBUSY)
            if not retryable or attempt == 3:
                raise
            time.sleep(0.1 * 2**attempt)
