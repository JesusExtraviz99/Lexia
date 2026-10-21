from copy import deepcopy
import unittest

from scripts.comparar_recuperacion import ExactRecoveryTracker, unique_exact_tail
from scripts.comparar_seguidores import CombinedTracker, replay
from scripts.diagnosticar_recuperacion import PREFIX, STORY, timed


def seed(cls=ExactRecoveryTracker):
    tracker = cls(STORY)
    for hypothesis in PREFIX:
        tracker.update_timed(hypothesis)
    return tracker


class ExactRecoveryTests(unittest.TestCase):
    def test_new_exact_unique_phrase_recovers_on_first_proposal(self):
        tracker = seed()
        result = tracker.update_timed(timed('mirando sus alas', 20))
        self.assertEqual(result['position'], 3)
        self.assertEqual(result['mode'], 'recuperacion_global_exacta')
        self.assertEqual(tracker.failures, 0)
        self.assertIsNone(tracker.recovery_candidate)
        self.assertEqual(tracker.latest_support_end, 23)
        self.assertEqual(seed(CombinedTracker).update_timed(timed('mirando sus alas', 20))['position'], 14)

    def test_old_overlapping_or_unordered_times_do_not_get_shortcut(self):
        bad_order = timed('mirando sus alas', 20)
        bad_order[1].update(start=20.5, end=21.5)
        for hypothesis in [timed('mirando sus alas', 0), timed('mirando sus alas', 14), bad_order]:
            state = seed().update_timed(hypothesis)
            self.assertNotEqual(state['mode'], 'recuperacion_global_exacta')
            self.assertEqual(state['position'], 14)

    def test_requires_entire_tail_exact_at_least_three_and_unique(self):
        for text in ['mirando sus', 'mirando sus alax', 'ruido mirando sus alas']:
            self.assertIsNone(unique_exact_tail(STORY, timed(text, 20)))
        ambiguous = STORY + STORY[:3]
        self.assertIsNone(unique_exact_tail(ambiguous, timed('mirando sus alas', 20)))
        self.assertEqual(unique_exact_tail(STORY, timed('Mirando sus alas', 20))['position'], 3)

    def test_replay_preserves_data_and_old_to_new_identical_text_limit(self):
        data = {'story_words': STORY, 'updates': [{'hypothesis': h} for h in
                PREFIX + [timed('mirando sus alas', 0), timed('mirando sus alas', 20)]]}
        snapshot = deepcopy(data)
        result = replay(data, ExactRecoveryTracker)
        self.assertEqual(data, snapshot)
        self.assertEqual([u['position'] for u in result['updates'][-2:]], [14, 14])
        self.assertEqual(result['updates'][-1]['mode'], 'hipotesis_sin_cambios')

    def test_local_match_keeps_existing_path(self):
        tracker = seed()
        state = tracker.update_timed(timed('después volvieron', 20))
        self.assertEqual(state['position'], 5)
        self.assertEqual(state['mode'], 'local')
        cold = ExactRecoveryTracker(STORY)
        self.assertNotEqual(cold.update_timed(timed('mirando sus alas', 20))['mode'], 'recuperacion_global_exacta')

    def test_invalid_timestamps_cannot_drive_shortcut(self):
        for value in [float('nan'), True, '20']:
            hypothesis = timed('mirando sus alas', 20)
            hypothesis[0]['start'] = value
            with self.assertRaises(ValueError):
                seed().update_timed(hypothesis)


if __name__ == '__main__':
    unittest.main()
