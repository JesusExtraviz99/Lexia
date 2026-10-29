import unittest
from scripts.probar_final_vad_literal import prefix_samples,selected_numbers,SELECTION


class PrefixTests(unittest.TestCase):
    def test_custom_pause_selection_keeps_default_eight_unchanged(self):
        default=list(SELECTION)
        self.assertEqual(selected_numbers([3,13],17),[3,13])
        self.assertEqual(selected_numbers(None,17),default)
        self.assertEqual(SELECTION,default)

    def test_invalid_selection_is_rejected_instead_of_silently_skipping(self):
        for numbers in [[],[3,3],[0],[18]]:
            with self.subTest(numbers=numbers),self.assertRaises(ValueError):
                selected_numbers(numbers,17)

    def test_vad_margin_is_not_added_twice(self):
        self.assertEqual(prefix_samples(23.312,40*16000),372992)

    def test_no_voice_is_not_silently_transcribed_as_empty(self):
        for end in [None,0,-1]:
            with self.subTest(end=end),self.assertRaises(ValueError):
                prefix_samples(end,640000)

    def test_prefix_cannot_extend_past_original_audio(self):
        with self.assertRaises(ValueError):
            prefix_samples(41,40*16000)


if __name__=='__main__':
    unittest.main()
