import unittest

from scripts.evaluar_relectura_lejana import evaluate


class FarRereadingEvaluationTests(unittest.TestCase):
    def test_first_reading_alas_does_not_count_as_rereading_recovery(self):
        anchors = [{'end': 25}, {'start': 29}, {'end': 33}]
        def row(t, ready, position, movement):
            return {'audio_seconds': t, 'ready_seconds_simulated': ready,
                    'variants': {'new': {'position': position, 'movement': movement}}}
        rows = [row(22, 24, 45, 2), row(26, 28, 56, 11),
                row(32, 34, 43, -13), row(34, 36, 45, 2)]
        result = evaluate(rows, 'new', anchors)
        self.assertEqual(result['backward_cut_seconds'], 32)
        self.assertEqual(result['backward_ready_since_los_start_simulated'], 5)
        self.assertEqual(result['final_45_ready_delay_after_alas_end_simulated'], 3)
        self.assertEqual(result['first_56_ready_delay_after_cuaderno_end_simulated'], 3)

    def test_stuck_at_end_has_no_fabricated_recovery_or_delay(self):
        rows = [{'audio_seconds': 60, 'ready_seconds_simulated': 61,
                 'variants': {'old': {'position': 56, 'movement': 0}}}]
        result = evaluate(rows, 'old', [{'end': 25}, {'start': 29}, {'end': 33}])
        self.assertIsNone(result['backward_cut_seconds'])
        self.assertIsNone(result['final_45_ready_delay_after_alas_end_simulated'])
        self.assertEqual(result['final_position'], 56)
