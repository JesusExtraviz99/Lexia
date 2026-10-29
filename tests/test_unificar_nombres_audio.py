import unittest
from scripts.unificar_nombres_audio import description, reader_id


class NamingTests(unittest.TestCase):
    def test_preserves_condition_and_removes_batch_prefix(self):
        row = {'audio_file': 'Biblioteca 08 - mezcla dificil larga - lectura_05 - 26-10-2026.wav'}
        self.assertEqual(description(row), 'Mezcla dificil larga')

    def test_new_names_are_stable_and_story_alias_removed(self):
        self.assertEqual(description({'audio_file': 'Lectura normal - lectura_03 - 28-10-2026 - lector_02.wav'}), 'Lectura normal')
        self.assertEqual(description({'audio_file': 'Lectura lenta - cuento 2 - lectura_02 - 23-10-2026.wav'}), 'Lectura lenta')

    def test_reader_identity_normalization(self):
        self.assertEqual(reader_id('adulto_01'), 'lector_01')
        self.assertEqual(reader_id('lector_2'), 'lector_02')
        self.assertEqual(reader_id('lector_02'), 'lector_02')
        with self.assertRaises(ValueError):
            reader_id(None)
