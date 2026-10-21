import unittest

from scripts.evaluar_relectura_lejana import evaluate


class FarRereadingEvaluationTests(unittest.TestCase):
    def test_other_destination_distinguishes_partial_word_from_post_end_update(self):
        anchors = [{'end': 22.51}, {'start': 25.73}, {'end': 34.32}]
        def row(cut, ready, position, movement):
            return {'audio_seconds': cut, 'ready_seconds_simulated': ready,
                    'variants': {'new': {'position': position, 'movement': movement}}}
        rows = [row(8, 10, 17, 2), row(24, 26, 56, 11), row(28, 29.5, 12, -44),
                row(34, 35.6, 17, 2), row(36, 37.5, 17, 0)]
        result = evaluate(rows, 'new', anchors, (10, 17))
        self.assertEqual(result['backward_cut_seconds'], 28)
        self.assertEqual(result['first_target_cut_seconds'], 34)
        self.assertTrue(result['first_target_cut_before_human_end'])
        self.assertAlmostEqual(result['first_target_ready_minus_human_end_simulated'], 1.28)
        self.assertEqual(result['post_end_target_cut_seconds'], 36)
        self.assertAlmostEqual(result['post_end_target_ready_delay_simulated'], 3.18)
        self.assertNotIn('final_45_cut_seconds', result)

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
