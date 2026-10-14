import unittest
from scripts.seguir import Tracker, locate, audio_bounds
from scripts.alinear import tokens


class TrackingTests(unittest.TestCase):
    def test_window_limits_and_overlap(self):
        self.assertEqual(audio_bounds(4*16000, 6), (0, 4*16000))
        self.assertEqual(audio_bounds(12*16000, 6), (6*16000, 12*16000))
        self.assertEqual(audio_bounds(14*16000, 6), (8*16000, 14*16000))
        self.assertEqual(audio_bounds(12*16000, 0), (0, 12*16000))

    def test_omission_and_substitution_do_not_block(self):
        story = tokens("la mariposa voló despacio y se posó sobre una flor")
        result = locate(story, tokens("la mariposa voló y se posó sobre una flor"))
        self.assertEqual(result["position"], 10)
        story = tokens("los dos se quedaron en silencio mirando sus alas")
        result = locate(story, tokens("los dos se quedaron en cinesio mirando sus alas"))
        self.assertEqual(result["position"], 9)

    def test_repetition_and_backward_reading(self):
        tracker = Tracker(tokens("una mañana Ana salió al jardín de su casa"))
        self.assertEqual(tracker.update(tokens("una mañana Ana Ana salió"))["position"], 4)
        self.assertEqual(tracker.update(tokens("una mañana Ana"))["position"], 3)

    def test_unrelated_speech_holds_position(self):
        tracker = Tracker(tokens("el gato duerme en casa"))
        tracker.update(tokens("el gato duerme"))
        self.assertEqual(tracker.update(tokens("quiero beber agua ahora"))["position"], 3)

    def test_two_word_minimum(self):
        self.assertIsNone(locate(tokens("el gato duerme"), ["el"])["position"])

    def test_locality_of_repeated_phrase(self):
        story = tokens("el gato duerme en casa y el gato corre por fuera")
        self.assertEqual(locate(story, tokens("el gato"), previous=8)["position"], 8)


if __name__ == "__main__":
    unittest.main()
