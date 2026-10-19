from copy import deepcopy
import unittest

from scripts.alinear import tokens
from scripts.seguir import Tracker
from scripts.comparar_seguidores import SingleWordTracker, replay


class SingleWordExperimentTests(unittest.TestCase):
    def test_exact_consecutive_unique_word_can_advance(self):
        story = tokens('mirando sus alas después volvieron a casa')
        original, variant = Tracker(story), SingleWordTracker(story)
        for tracker in (original, variant):
            tracker.update(tokens('mirando sus alas'))
        self.assertEqual(original.update(['después'])['position'], 3)
        self.assertEqual(variant.update(['después'])['position'], 4)
        self.assertEqual(variant.update(['Después'])['position'], 4)

    def test_reject_short_ambiguous_unrelated_skipped_and_backward_words(self):
        tracker = SingleWordTracker(tokens('inicio jardín casa y jardín después final'))
        tracker.position = 1
        for heard in ['jardín', 'casa', 'después', 'suscríbete', 'inicio']:
            self.assertEqual(tracker.update([heard])['position'], 1)
        empty = SingleWordTracker(tokens('jardín después'))
        self.assertIsNone(empty.update(['jardín'])['position'])

    def test_multiword_rereading_is_still_allowed(self):
        tracker = SingleWordTracker(tokens('una mañana Ana salió al jardín'))
        tracker.update(tokens('Ana salió al jardín'))
        self.assertEqual(tracker.update(tokens('una mañana Ana'))['position'], 3)

    def test_replay_preserves_inputs_timing_and_unchanged_policy(self):
        data = {'story_words': tokens('mirando sus alas después'), 'updates': [
            {'hypothesis': [{'word': w} for w in tokens('mirando sus alas')], 'processing_seconds': .5},
            {'hypothesis': [{'word': 'después'}], 'processing_seconds': .7},
            {'hypothesis': [{'word': 'después'}], 'processing_seconds': .8}]}
        snapshot = deepcopy(data)
        result = replay(data, SingleWordTracker)
        self.assertEqual(data, snapshot)
        self.assertEqual([u['position'] for u in result['updates']], [3, 4, 4])
        self.assertEqual(result['updates'][-1]['mode'], 'hipotesis_sin_cambios')
        self.assertEqual([u['processing_seconds'] for u in result['updates']], [.5, .7, .8])


if __name__ == '__main__':
    unittest.main()
