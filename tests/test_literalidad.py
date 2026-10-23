"""El informe debe admitir audio completo y rechazar resultados incompletos."""
import json
from pathlib import Path
import tempfile
import unittest

from scripts.comparar_literalidad import summarize


class LiteralidadTests(unittest.TestCase):
    def fixture(self, root):
        manifest={'notice':'Audio completo, ensayo offline.',
                  'samples':[{'id':'completa','start':0,'end':60,'human_note':'Sin conteos validados.'}]}
        (root/'manifest.json').write_text(json.dumps(manifest),encoding='utf-8')
        result={'status':'completo','runs':[{'id':'completa','raw_text':'Texto literal.','processing_seconds':3}],
                'resources':{'final_memory':{'process_lifetime_peak_working_set_bytes':1048576}},
                'backend':'prueba','compute_type':'prueba','model_load_seconds':1}
        for engine in ['baseline','candidato']:
            (root/(engine+'.json')).write_text(json.dumps(result),encoding='utf-8')
        return result

    def test_summary_uses_actual_duration_for_one_complete_recording(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);self.fixture(root)
            summarize(root)
            text=(root/'resumen.md').read_text(encoding='utf-8')
            self.assertIn('60.00 s por motor',text)
            self.assertIn('Texto literal.',text)
            self.assertNotIn('56 s',text)

    def test_summary_rejects_missing_or_duplicate_runs(self):
        for runs in [[], [{'id':'completa'},{'id':'completa'}]]:
            with self.subTest(runs=runs),tempfile.TemporaryDirectory() as tmp:
                root=Path(tmp);result=self.fixture(root);result['runs']=runs
                (root/'candidato.json').write_text(json.dumps(result),encoding='utf-8')
                with self.assertRaises(ValueError):
                    summarize(root)


if __name__=='__main__':
    unittest.main()
