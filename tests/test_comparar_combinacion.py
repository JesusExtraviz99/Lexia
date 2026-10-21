import unittest

from scripts.alinear import tokens
from scripts.comparar_combinacion import interaction_changes
from scripts.comparar_seguidores import CombinedTracker, SingleWordTracker, TemporalBacktrackTracker, replay
from scripts.seguir import Tracker


def timed(text, start, step=1):
    return [{'word': w, 'start': start + i * step, 'end': start + (i + 1) * step}
            for i, w in enumerate(tokens(text))]


class CombinedRulesTests(unittest.TestCase):
    def test_both_rules_and_synthetic_rereading_in_one_sequence(self):
        story = tokens('mirando sus alas después volvieron a casa y dibujaron la mariposa en un cuaderno')
        data = {'story_words': story, 'updates': [{'hypothesis': h} for h in [
            timed('mirando sus alas', 0), timed('Después', 3),
            timed('y dibujaron la mariposa en un cuaderno', 8),
            timed('en un jugaderno', 12), timed('después volvieron', 20)]]}
        positions = {name: [u['position'] for u in replay(data, cls)['updates']]
                     for name, cls in [('original', Tracker), ('single', SingleWordTracker),
                                       ('temporal', TemporalBacktrackTracker), ('combined', CombinedTracker)]}
        self.assertEqual(positions['original'], [3, 3, 14, 13, 5])
        self.assertEqual(positions['single'], [3, 4, 14, 13, 5])
        self.assertEqual(positions['temporal'], [3, 3, 14, 14, 5])
        self.assertEqual(positions['combined'], [3, 4, 14, 14, 5])

    def test_single_word_advance_updates_temporal_support(self):
        tracker = CombinedTracker(tokens('mirando sus alas después volvieron'))
        tracker.update_timed(timed('mirando sus alas', 0))
        state = tracker.update_timed(timed('Después', 5))
        self.assertEqual(state['position'], 4)
        self.assertEqual(tracker.latest_support_end, 6)
        # Respaldo 4,5: posterior al apoyo inicial de alas, pero anterior a Después.
        state = tracker.update_timed(timed('mirando sus alas digo', 1.5))
        self.assertEqual(state['position'], 4)
        self.assertEqual(state['mode'], 'retroceso_sin_tiempo_nuevo')

    def test_interaction_report_does_not_hide_new_combined_position(self):
        def trace(position):
            return {'updates': [{'audio_available_seconds': 2, 'position': position}]}
        self.assertEqual(interaction_changes(trace(3), trace(4), trace(3), trace(4)), [])
        rows = interaction_changes(trace(3), trace(4), trace(3), trace(5))
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]['combinada'], 5)


if __name__ == '__main__':
    unittest.main()
