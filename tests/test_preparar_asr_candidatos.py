import unittest
from pathlib import Path
from scripts.preparar_asr_candidatos import zip_target


class ModelArchivePathTests(unittest.TestCase):
    def test_expected_model_path_is_preserved(self):
        root=Path.cwd()/'modelos'
        result=zip_target('vosk-model-small-es-0.42/am/final.mdl',root,'vosk-model-small-es-0.42')
        self.assertEqual(result,root.resolve()/'vosk-model-small-es-0.42/am/final.mdl')

    def test_unsafe_paths_and_other_model_roots_are_rejected(self):
        root=Path.cwd()/'modelos'
        for value in ['../escape','/absolute','C:/escape','vosk-model-small-es-0.42/../../escape',
                      'vosk-model-small-es-0.42\\escape','other/am/final.mdl']:
            with self.subTest(value=value),self.assertRaises(ValueError):
                zip_target(value,root,'vosk-model-small-es-0.42')


if __name__=='__main__':unittest.main()
