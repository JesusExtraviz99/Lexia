import hashlib
import json
from pathlib import Path
import tempfile
from types import SimpleNamespace
import unittest

from scripts.comparar_literalidad import resource_interval
from scripts.lote_literalidad import select_recordings,select_story


class LiteralBatchTests(unittest.TestCase):
    def test_story_selection_rejects_changed_text_and_unknown_story(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            story=root/'new.txt';story.write_bytes(b'new')
            rows=[dict(id='new',story_file='new.txt',story_sha256=hashlib.sha256(b'new').hexdigest()),
                  dict(id='old',story_file='old.txt',story_sha256='old')]
            self.assertEqual([r['id'] for r in select_story(rows,story,root)],['new'])
            with self.assertRaises(ValueError):
                select_story(rows,root/'unknown.txt',root)
            story.write_bytes(b'changed')
            with self.assertRaises(ValueError):
                select_story(rows,story,root)

    def test_resource_interval_excludes_other_audios_and_lifetime_peak(self):
        monitor=SimpleNamespace(
            samples=[{'elapsed_seconds':t,'memory':{'working_set_bytes':ram}} for t,ram in [(0,9000),(2,300),(4,400),(6,8000)]],
            gpu_samples=[{'elapsed_seconds':t,'gpus':[]} for t in [0,3,6]])
        result=resource_interval(monitor,1,5,2,{'working_set_bytes':200},{'working_set_bytes':250,'process_lifetime_peak_working_set_bytes':9000})
        self.assertEqual(result['working_set_max_sampled_bytes'],400)
        self.assertEqual([s['elapsed_seconds'] for s in result['samples']],[2,4])
        self.assertEqual([s['elapsed_seconds'] for s in result['gpu_global_samples']],[3])
        self.assertEqual(result['cpu_percent_one_logical_core'],50)

    def test_resource_interval_missing_memory_is_not_zero(self):
        result=resource_interval(SimpleNamespace(samples=[],gpu_samples=[]),0,1,0,{}, {})
        self.assertIsNone(result['working_set_max_sampled_bytes'])

    def test_selection_covers_every_wav_and_skips_only_declared_history(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);(root/'datos/audio').mkdir(parents=True);(root/'datos/referencias').mkdir()
            (root/'datos/audio/actual.wav').write_bytes(b'actual')
            rows=[dict(id='actual',audio_file='datos/audio/actual.wav',audio_sha256=hashlib.sha256(b'actual').hexdigest()),
                  dict(id='anterior',audio_file='datos/audio/actual.wav',audio_sha256=hashlib.sha256(b'viejo').hexdigest(),availability_status='historico_sin_wav_coincidente')]
            (root/'datos/referencias/catalogo.json').write_text(json.dumps({'recordings':rows}),encoding='utf-8')
            selected,skipped=select_recordings(root)
            self.assertEqual([r['id'] for r in selected],['actual'])
            self.assertEqual([r['id'] for r in skipped],['anterior'])
            (root/'datos/audio/sin_catalogar.wav').write_bytes(b'otro')
            with self.assertRaises(ValueError):
                select_recordings(root)


if __name__=='__main__':
    unittest.main()
