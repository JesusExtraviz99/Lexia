import unittest

from scripts.evaluar_seguimiento import evaluate, position_at


class HumanEvaluationTests(unittest.TestCase):
    def setUp(self):
        self.annotation = {'audio_file': 'datos/audio/a.wav', 'duration_seconds': 10,
                           'words': [{'word': 'Una', 'start': 1, 'end': 2, 'reviewed': True},
                                     {'word': 'mañana', 'start': 3, 'end': 5, 'reviewed': True}]}
        self.data = {'audio_file': 'a.wav', 'audio_seconds': 10,
                     'story_words': ['Una', 'mañana'], 'audio_window_seconds': 4,
                     'updates': [{'audio_available_seconds': t, 'position': p,
                                  'sequential_ready_seconds_simulated': ready}
                                 for t, p, ready in [(2, 1, 4.5), (4, 1, 6), (6, 2, 8), (8, 2, 9)]]}

    def test_word_end_and_pause_convention(self):
        self.assertEqual([position_at(self.annotation['words'], t) for t in [1, 2, 3, 5]], [0, 1, 1, 2])

    def test_queue_and_final_silence_are_separate(self):
        result = evaluate(self.data, self.annotation)
        self.assertEqual(result['hypothesis_at_audio_cutoff']['mean_absolute_words'], 0)
        self.assertEqual(result['visible_at_audio_cutoff_simulated']['mean_absolute_words'], 1)
        self.assertEqual(result['hypothesis_at_audio_cutoff']['samples'], 2)
        self.assertEqual(result['final_word_delay_seconds_simulated'], 3)

    def test_reject_other_audio_or_unreviewed_reference(self):
        self.data['audio_file'] = 'otro.wav'
        with self.assertRaises(ValueError):
            evaluate(self.data, self.annotation)
        self.data['audio_file'] = 'a.wav'
        self.annotation['words'][0]['reviewed'] = False
        with self.assertRaises(ValueError):
            evaluate(self.data, self.annotation)


if __name__ == '__main__':
    unittest.main()
