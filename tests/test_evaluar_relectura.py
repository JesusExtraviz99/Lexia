from copy import deepcopy
import unittest
from scripts.evaluar_relectura import evaluate, phase_at


class RereadingEvaluationTests(unittest.TestCase):
    def setUp(self):
        self.anchors = [{'story_range': span, 'attempt': attempt, 'start': start, 'end': end, 'reviewed': True}
                        for span, attempt, start, end in [([37, 42], 1, 17.54, 19.84),
                                                         ([37, 42], 2, 20.36, 22.77),
                                                         ([43, 43], 1, 22.91, 23.29)]]
        self.annotation = {'audio_file': 'a.wav', 'duration_seconds': 60, 'words': self.anchors}
        self.data = {'audio_file': 'a.wav', 'audio_seconds': 60, 'story_words': ['cuento'], 'block_seconds': 2,
                     'updates': [{'audio_available_seconds': t, 'position': p, 'movement': m,
                                  'sequential_ready_seconds_simulated': t + 1.7, 'hypothesis': []}
                                 for t, p, m in [(18, 36, 2), (20, 42, 6), (22, 41, -1), (24, 45, 4)]]}

    def test_only_one_cut_in_second_attempt_and_output_arrives_later(self):
        result = evaluate(self.data, self.annotation, ['cuento'])
        self.assertEqual(result['second_attempt_cut_samples'], 1)
        self.assertEqual(result['backward_hypotheses_with_cut_in_second_attempt'], 1)
        self.assertEqual(result['backward_outputs_ready_during_second_attempt_simulated'], 0)
        self.assertEqual(result['samples'][2]['visible_position_simulated'], 42)
        self.assertAlmostEqual(result['gap_seconds'], .52)

    def test_phase_boundaries(self):
        self.assertEqual(phase_at(self.anchors, 19.84), 'entre_intentos')
        self.assertEqual(phase_at(self.anchors, 20.36), 'segundo_intento')
        self.assertEqual(phase_at(self.anchors, 22.77), 'frase_repetida_terminada')
        self.assertEqual(phase_at(self.anchors, 23.29), 'mirando_terminada')

    def test_reject_other_audio_and_unreviewed_attempt(self):
        data = deepcopy(self.data)
        data['audio_file'] = 'otro.wav'
        with self.assertRaises(ValueError):
            evaluate(data, self.annotation, ['cuento'])
        self.anchors[1]['reviewed'] = False
        with self.assertRaises(ValueError):
            evaluate(self.data, self.annotation, ['cuento'])


if __name__ == '__main__':
    unittest.main()
