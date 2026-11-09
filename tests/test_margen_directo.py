import unittest
from scripts.alinear import tokens
from scripts.comparar_margen_directo import MarginTracker, replay
from scripts.seguir import Tracker


class MarginTests(unittest.TestCase):
    def setUp(self):
        self.story=tokens('uno dos tres cuatro cinco seis siete ocho nueve diez once doce trece catorce quince dieciseis diecisiete dieciocho diecinueve veinte')

    def test_short_rereading_still_allowed(self):
        traces=replay(self.story, ['ocho nueve diez', 'nueve diez once'], initial=12)
        for positions in traces.values():
            self.assertEqual(positions,[10,11])

    def test_far_rereading_needs_global_fallback(self):
        traces=replay(self.story, ['uno dos tres','uno dos dos tres','uno uno dos tres'], initial=20)
        self.assertEqual(traces['local5_global'][-1],3)
        self.assertEqual(traces['local5_sin_global'][-1],20)

    def test_exact_unchanged_text_does_not_confirm_recovery(self):
        traces=replay(self.story, ['uno dos tres']*3, initial=20)
        self.assertEqual(traces['local5_global'],[20,20,20])

    def test_baseline_matches_existing_tracker_on_changed_hypotheses(self):
        expected=Tracker(self.story)
        actual=MarginTracker(self.story)
        for phrase in ['uno dos tres','dos tres cuatro','palabras sin coincidencias','cinco seis siete','uno dos tres','uno uno dos tres','uno dos dos tres']:
            self.assertEqual(actual.update(tokens(phrase)), expected.update(tokens(phrase))['position'] or 0)


if __name__=='__main__':unittest.main()
