from copy import deepcopy
import json
from pathlib import Path
import tempfile
import threading
import unittest

from scripts.revisar_mls_web import Workspace, validate


class ReviewTests(unittest.TestCase):
    def template(self):
        return dict(id='1_2_3', audio_sha256='fixed', listened=False, completed=False,
                    reference_assessment='', asr_errors=[], notes='', heard_transcript='')

    def test_completion_requires_human_confirmation_and_preserves_identity(self):
        template = self.template()
        with self.assertRaises(ValueError):
            validate(dict(template, completed=True), template)
        payload = dict(template, listened=True, completed=True, reference_assessment='dudosa',
                       notes='No se entiende el final', id='otro', asr_errors=['crisper'])
        result = validate(payload, template)
        self.assertEqual(result['id'], template['id'])
        self.assertFalse(template['completed'])
        self.assertTrue(result['completed'])
        with self.assertRaises(ValueError):
            validate(dict(payload, audio_sha256='different'), template)

    def test_save_resume_and_backup_without_touching_audio(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            ws = Workspace.__new__(Workspace)
            ws.root, ws.lock = root, threading.Lock()
            ws.folder = root/'reviews'
            ws.templates = {'1_2_3': self.template()}
            original = root/'original.flac'
            original.write_bytes(b'original-content')
            a = ws.current('1_2_3')
            self.assertFalse(a['completed'])
            ws.save('1_2_3', dict(a, notes='Primer borrador'))
            ws.save('1_2_3', dict(a, listened=True, notes='Comprobado', reference_assessment='incompleta', completed=True))
            self.assertTrue(ws.current('1_2_3')['completed'])
            backups = list((root/'.descartados/revision_mls/copias').glob('*.json'))
            self.assertEqual(len(backups), 1)
            self.assertEqual(json.loads(backups[0].read_text(encoding='utf-8'))['notes'], 'Primer borrador')
            self.assertEqual(original.read_bytes(), b'original-content')

    def test_invalid_fields_do_not_count_as_review(self):
        template = self.template()
        for change in [dict(listened='sí'), dict(asr_errors=['inventado']),
                       dict(reference_assessment='corrected'), dict(asr_errors=['vosk','vosk'])]:
            with self.assertRaises(ValueError):
                validate(dict(deepcopy(template), **change), template)


if __name__ == '__main__':
    unittest.main()
