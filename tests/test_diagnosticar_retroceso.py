import unittest
from scripts.alinear import tokens
from scripts.seguir import Tracker, locate


class RegressionMechanismTests(unittest.TestCase):
    def test_wrong_last_word_leaves_previous_exact_match(self):
        story = tokens('mariposa en un cuaderno')
        tracker = Tracker(story)
        self.assertEqual(tracker.update(tokens('mariposa en un cuaderno'))['position'], 4)
        result = tracker.update(tokens('en un jugaderno'))
        self.assertEqual(result['position'], 3)
        self.assertEqual(result['movement'], -1)
        self.assertEqual(result['evidence']['exact_matches'], 2)
        self.assertEqual(result['evidence']['hypothesis_words'], 3)
        self.assertEqual(result['evidence']['edit_cost'], 1)
        self.assertEqual(tracker.update(tokens('un jugaderno'))['position'], 3)
        self.assertEqual(tracker.update([])['position'], 3)

    def test_correct_last_word_preserves_end(self):
        story = tokens('mariposa en un cuaderno')
        self.assertEqual(locate(story, tokens('en un cuaderno'), previous=4)['position'], 4)


if __name__ == '__main__':
    unittest.main()
