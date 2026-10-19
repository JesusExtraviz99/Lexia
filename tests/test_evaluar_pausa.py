from copy import deepcopy
import unittest

from scripts.evaluar_pausa import evaluate


class PauseEvaluationTests(unittest.TestCase):
    def setUp(self):
        self.annotation = {'audio_file': 'datos/audio/a.wav', 'duration_seconds': 40,
                           'words': [{'story_range': [27, 27], 'start': 9, 'end': 10, 'reviewed': True},
                                     {'story_range': [28, 28], 'start': 19, 'end': 20, 'reviewed': True},
                                     {'story_range': [56, 56], 'start': 29, 'end': 30, 'reviewed': True}]}
        self.data = {'audio_file': 'a.wav', 'audio_seconds': 40, 'story_words': ['cuento'],
                     'updates': [{'audio_available_seconds': t, 'position': p,
                                  'sequential_ready_seconds_simulated': t + 3,
                                  'hypothesis': [{'word': 'flor'}]}
                                 for t, p in [(10, 27), (12, 27), (18, 27), (20, 36), (30, 56), (32, 56)]]}

    def test_pause_edges_and_visible_output_are_distinct(self):
        r = evaluate(self.data, self.annotation, ['cuento'])
        self.assertEqual(r['pause_duration_seconds'], 9)
        self.assertEqual([s['audio_seconds'] for s in r['pause_samples']], [10, 12, 18])
        self.assertEqual(r['hypothesis_exact_27_samples'], 3)
        self.assertEqual(r['visible_exact_27_samples'], 1)
        self.assertEqual(r['first_advance_after_resume']['position'], 36)
        self.assertEqual(r['first_advance_after_resume']['delay_from_ana_end_seconds_simulated'], 3)
        self.assertEqual(r['first_final_word']['delay_from_cuaderno_end_seconds_simulated'], 3)

    def test_no_advance_and_no_final_word_remain_missing(self):
        data = deepcopy(self.data)
        for u in data['updates']:
            u['position'] = 27
        r = evaluate(data, self.annotation, ['cuento'])
        self.assertIsNone(r['first_advance_after_resume'])
        self.assertIsNone(r['first_final_word'])

    def test_reject_mismatched_or_unreviewed_reference(self):
        for key, value in [('audio_file', 'otro.wav'), ('audio_seconds', 60), ('story_words', ['otro'])]:
            data = deepcopy(self.data)
            data[key] = value
            with self.assertRaises(ValueError):
                evaluate(data, self.annotation, ['cuento'])
        self.annotation['words'][1]['reviewed'] = False
        with self.assertRaises(ValueError):
            evaluate(self.data, self.annotation, ['cuento'])


if __name__ == '__main__':
    unittest.main()
