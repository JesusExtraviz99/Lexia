import errno
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from scripts.archivos import write_text_atomic


class AtomicWriteTests(unittest.TestCase):
    def test_successful_write_replaces_content_and_cleans_temporary(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder)/'registro.json'
            path.write_text('anterior', encoding='utf-8')
            write_text_atomic(path, '{"texto":"Lucía"}')
            self.assertEqual(path.read_text(encoding='utf-8'), '{"texto":"Lucía"}')
            self.assertEqual(list(Path(folder).iterdir()), [path])

    def test_transient_replace_failure_retries_without_truncating_previous_file(self):
        import os
        replace = os.replace
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder)/'registro.json'
            path.write_text('anterior', encoding='utf-8')
            calls = []
            def sometimes(source, destination):
                calls.append(destination)
                self.assertEqual(path.read_text(encoding='utf-8'), 'anterior')
                if len(calls) == 1:
                    raise OSError(errno.EINVAL, 'fallo simulado')
                replace(source, destination)
            with patch('scripts.archivos.os.replace', side_effect=sometimes), patch('scripts.archivos.time.sleep'):
                write_text_atomic(path, 'nuevo')
            self.assertEqual(len(calls), 2)
            self.assertEqual(path.read_text(encoding='utf-8'), 'nuevo')
            self.assertEqual(list(Path(folder).iterdir()), [path])

    def test_persistent_failure_preserves_previous_file_and_is_reported(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder)/'registro.json'
            path.write_text('anterior', encoding='utf-8')
            with patch('scripts.archivos.os.replace', side_effect=PermissionError(errno.EACCES, 'ocupado')) as replace, \
                    patch('scripts.archivos.time.sleep'):
                with self.assertRaises(PermissionError):
                    write_text_atomic(path, 'nuevo')
            self.assertEqual(replace.call_count, 4)
            self.assertEqual(path.read_text(encoding='utf-8'), 'anterior')
            self.assertEqual(list(Path(folder).iterdir()), [path])
