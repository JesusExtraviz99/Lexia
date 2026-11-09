import unittest
from scripts.revisar_lectores import validate_review


class ReaderReviewTests(unittest.TestCase):
    def setUp(self):
        self.template = dict(audio_sha256='abc', recording_id='fixed')

    def test_partial_review_can_be_saved_without_inventing_transcript(self):
        result = validate_review(dict(audio_sha256='abc', notes='Duda al final.'), self.template)
        self.assertFalse(result['literal_reviewed'])
        self.assertEqual(result['transcript_literal'], '')

    def test_wrong_audio_and_unknown_flags_are_rejected(self):
        for payload in [dict(audio_sha256='other'), dict(audio_sha256='abc',flags=['inventado'])]:
            with self.assertRaises(ValueError):
                validate_review(payload,self.template)

    def test_literal_completion_requires_general_review_and_text(self):
        with self.assertRaises(ValueError):
            validate_review(dict(audio_sha256='abc',literal_reviewed=True),self.template)

    def test_preserves_actual_partials_and_immutable_identity(self):
        result=validate_review(dict(audio_sha256='abc',recording_id='different',general_reviewed=True,
            completion='completa',quality='revisable',literal_reviewed=True,
            transcript_literal='Regres- re- regresaron. [otra voz: bien]',flags=['trabadas','otras_voces']),self.template)
        self.assertEqual(result['recording_id'],'fixed')
        self.assertEqual(result['transcript_literal'],'Regres- re- regresaron. [otra voz: bien]')

    def test_general_completion_requires_explicit_quality_and_completion(self):
        with self.assertRaises(ValueError):
            validate_review(dict(audio_sha256='abc',general_reviewed=True),self.template)
