import unittest
from scripts.alinear import tokens
from scripts.diagnosticar_apoyos_android import SupportedTracker


class SupportTests(unittest.TestCase):
    def test_interior_common_word_does_not_justify_skipping_phrase(self):
        story=tokens('Ana llamó a su hermano para que pudiera verla los dos se quedaron')
        tracker=SupportedTracker(story)
        tracker.position=8
        self.assertEqual(tracker.update_recent('hermano para que pudiera y lo que se','y lo que se'),8)
        self.assertEqual(tracker.event['kind'],'advance_rejected_missing_terminal_support')

    def test_fast_correct_phrase_may_advance_several_words(self):
        tracker=SupportedTracker(tokens('Una mañana Ana salió al jardín de su casa'))
        tracker.position=3
        self.assertEqual(tracker.update_recent('Ana salió al jardín','Ana salió al jardín'),6)

    def test_recent_clear_phrase_can_escape_old_unrelated_text(self):
        tracker=SupportedTracker(tokens('Después volvieron a casa y dibujaron la mariposa en un cuaderno'),suffix_recovery=True)
        tracker.position=8
        self.assertEqual(tracker.update_recent('en el sector de la pesca en un cuaderno','en un cuaderno'),11)
        self.assertEqual(tracker.event['kind'],'recent_exact_unique_suffix')

    def test_ambiguous_phrase_does_not_trigger_suffix_recovery(self):
        tracker=SupportedTracker(tokens('un barco rojo allí un barco rojo'),suffix_recovery=True)
        tracker.position=1
        tracker.update_recent('ruido extraño sin relación un barco rojo','un barco rojo')
        self.assertNotEqual((tracker.event or {}).get('kind'),'recent_exact_unique_suffix')

    def test_two_words_alone_do_not_trigger_suffix_recovery(self):
        tracker=SupportedTracker(tokens('Después volvieron a casa y dibujaron la mariposa en un cuaderno'),suffix_recovery=True)
        tracker.position=8
        tracker.update_recent('en el sector de la pesca un cuaderno','un cuaderno')
        self.assertNotEqual((tracker.event or {}).get('kind'),'recent_exact_unique_suffix')

    def test_limit_exact_hallucinated_phrase_cannot_be_distinguished_from_speech(self):
        # Control adverso conocido: sin audio, el texto exacto inventado es indistinguible.
        tracker=SupportedTracker(tokens('Después volvieron a casa y dibujaron la mariposa en un cuaderno'),suffix_recovery=True)
        tracker.position=8
        tracker.update_recent('en el sector de la pesca en un cuaderno','en un cuaderno')
        self.assertEqual(tracker.position,11)

    def test_limit_incomplete_trailing_word_can_delay_valid_earlier_words(self):
        tracker=SupportedTracker(tokens('una mariposa azul la mariposa voló despacio'))
        tracker.position=3
        tracker.update_recent('azul la mariposa voló des','azul la mariposa voló des')
        self.assertEqual(tracker.position,3)
        self.assertEqual(tracker.event['kind'],'advance_rejected_missing_terminal_support')


if __name__=='__main__':unittest.main()
