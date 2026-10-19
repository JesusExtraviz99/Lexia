from copy import deepcopy
import unittest

from scripts.alinear import tokens
from scripts.comparar_seguidores import TemporalBacktrackTracker, replay
from scripts.seguir import locate


def timed(text, start, step=1):
    return [{'word': w, 'start': start + i * step, 'end': start + (i + 1) * step}
            for i, w in enumerate(tokens(text))]


class TemporalGuardTests(unittest.TestCase):
    def setUp(self):
        self.story = tokens('mariposa en un cuaderno')
        self.tracker = TemporalBacktrackTracker(self.story)
        self.tracker.update_timed(timed('mariposa en un cuaderno', 70))

    def test_old_support_does_not_erase_final_position(self):
        result = self.tracker.update_timed(timed('en un jugaderno', 71))
        self.assertEqual(result['position'], 4)
        self.assertEqual(result['mode'], 'retroceso_sin_tiempo_nuevo')
        self.assertEqual(result['evidence']['rejected_position'], 3)
        self.assertEqual(result['evidence']['matched_asr_end_seconds'], 73)
        self.assertEqual(self.tracker.latest_support_end, 74)
        self.assertEqual(self.tracker.update_timed([])['position'], 4)

    def test_new_support_can_still_move_backwards(self):
        self.tracker.update_timed(timed('en un jugaderno', 71))
        result = self.tracker.update_timed(timed('mariposa en un', 80))
        self.assertEqual(result['position'], 3)
        self.assertEqual(result['movement'], -1)
        self.assertNotEqual(result['mode'], 'retroceso_sin_tiempo_nuevo')
        self.assertEqual(self.tracker.latest_support_end, 83)

    def test_alignment_index_preserves_full_hypothesis_offset(self):
        story = tokens('Después volvieron a casa y dibujaron la mariposa en un cuaderno')
        heard = tokens('extra anterior otra mas casa y dibujaron la mariposa en un cuaderno')
        evidence = locate(story, heard, previous=11, include_match_index=True)
        self.assertEqual(evidence['matched_hypothesis_index'], 11)
        self.assertNotIn('matched_hypothesis_index', locate(story, heard, previous=11))
        # La última palabra errónea no se usa como apoyo temporal de un.
        evidence = locate(self.story, tokens('en un jugaderno'), previous=4, include_match_index=True)
        self.assertEqual(evidence['matched_hypothesis_index'], 1)

    def test_replay_preserves_input_and_does_not_reconfirm_identical_text(self):
        first = timed('mariposa en un cuaderno', 70)
        old = timed('en un jugaderno', 71)
        data = {'story_words': self.story, 'updates': [{'hypothesis': h} for h in [first, old, old]]}
        original = deepcopy(data)
        result = replay(data, TemporalBacktrackTracker)
        self.assertEqual(data, original)
        self.assertEqual([u['position'] for u in result['updates']], [4, 4, 4])
        self.assertEqual(result['updates'][-1]['mode'], 'hipotesis_sin_cambios')

    def test_missing_or_invalid_timing_cannot_silently_drive_guard(self):
        for hypothesis in [[{'word': 'un'}], [{'word': 'un', 'start': 4, 'end': 3}],
                           [{'word': 'un', 'start': 0, 'end': float('nan')}]]:
            with self.assertRaises(ValueError):
                self.tracker.update_timed(hypothesis)


if __name__ == '__main__':
    unittest.main()
