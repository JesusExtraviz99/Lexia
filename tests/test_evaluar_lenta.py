import unittest
from scripts.evaluar_lenta import evaluate, position_bounds


class SparseBoundsTests(unittest.TestCase):
    def test_no_interpolation_between_anchors(self):
        anchors = [{'story_range': [46, 46], 'end': 61.42},
                   {'story_range': [53, 53], 'end': 72.73},
                   {'story_range': [55, 55], 'end': 75.01},
                   {'story_range': [56, 56], 'end': 77.34}]
        self.assertEqual(position_bounds(anchors, 62, 56), (46, 52))
        self.assertEqual(position_bounds(anchors, 74, 56), (53, 54))
        self.assertEqual(position_bounds(anchors, 76, 56), (55, 55))
        self.assertEqual(position_bounds(anchors, 77.34, 56), (56, 56))

    def test_reaching_end_does_not_hide_later_regression(self):
        anchors = [{'story_range': [i, i], 'end': end, 'reviewed': True}
                   for i, end in [(46, 61.42), (53, 72.73), (55, 75.01), (56, 77.34)]]
        annotation = {'audio_file': 'a.wav', 'duration_seconds': 90, 'words': anchors}
        data = {'audio_file': 'a.wav', 'audio_seconds': 90, 'story_words': ['cuento'],
                'updates': [{'audio_available_seconds': t, 'position': p,
                             'sequential_ready_seconds_simulated': t + 3, 'hypothesis': []}
                            for t, p in [(78, 56), (80, 55), (90, 55)]]}
        result = evaluate(data, annotation, ['cuento'])
        self.assertEqual(result['first_final_word']['audio_seconds'], 78)
        self.assertEqual(result['post_reading_positions'], [56, 55, 55])
        self.assertEqual(result['final_position'], 55)
        for u in data['updates']:
            u['position'] = 53
        self.assertIsNone(evaluate(data, annotation, ['cuento'])['first_final_word'])


if __name__ == '__main__':
    unittest.main()
