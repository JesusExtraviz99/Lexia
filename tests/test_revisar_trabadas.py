from copy import deepcopy
import json
from pathlib import Path
import tempfile
import threading
import unittest

from scripts.revisar_trabadas import PLAN, Review, validate_reviews


def blank():
    return [dict(id=k, heard=[], asr4='', asr8='', notes='', reviewed=False) for k,*_ in PLAN]


class QualitativeReviewTests(unittest.TestCase):
    def test_doubt_is_valid_without_literal_transcription(self):
        rows = blank()
        rows[0].update(heard=['dudoso'], asr4='dudoso', asr8='dudoso', reviewed=True)
        self.assertTrue(validate_reviews(rows)[0]['reviewed'])
        self.assertNotIn('word_times', validate_reviews(rows)[0])

    def test_incomplete_review_and_changed_intervals_cannot_be_marked_complete(self):
        rows = blank()
        rows[0]['reviewed'] = True
        with self.assertRaises(ValueError):
            validate_reviews(rows)
        rows = blank()
        rows[0]['id'] = 'otro_audio'
        with self.assertRaises(ValueError):
            validate_reviews(rows)

    def test_contradictory_flags_are_rejected(self):
        rows = blank()
        rows[0]['heard'] = ['sin_trabadas','silabas_repetidas']
        with self.assertRaises(ValueError):
            validate_reviews(rows)

    def test_save_uses_server_metadata_and_preserves_previous_revision(self):
        with tempfile.TemporaryDirectory() as folder:
            review = Review.__new__(Review)
            review.root = Path(folder)
            review.path = review.root/'review.json'
            review.lock = threading.Lock()
            initial = dict(audio_sha256='original', intervals=[dict(id='inicio',start=0,end=8)], reviews=blank())
            review.current = lambda: deepcopy(initial)
            review.save(dict(reviews=blank(), audio_sha256='alterado', intervals=[]))
            first = review.path.read_bytes()
            stored = json.loads(first)
            self.assertEqual(stored['audio_sha256'],'original')
            self.assertEqual(stored['intervals'],initial['intervals'])
            review.save(dict(reviews=blank()))
            backups = list((review.root/'datos/anotaciones/copias').glob('*.json'))
            self.assertEqual(len(backups),1)
            self.assertEqual(backups[0].read_bytes(), first)


if __name__ == '__main__':
    unittest.main()
