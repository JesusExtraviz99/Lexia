import unittest
from scripts.exportar_catalogo_publico import public_catalog


class PublicCatalogTests(unittest.TestCase):
    def test_excludes_other_speakers_without_mutating_private_catalog(self):
        source = {'recordings': [{'speaker_id': s} for s in ['adulto_01', 'lector_01', 'lector_02', 'lector_10', None]]}
        result = public_catalog(source)
        self.assertEqual([r['speaker_id'] for r in result['recordings']], ['adulto_01', 'lector_01'])
        self.assertEqual(len(source['recordings']), 5)
