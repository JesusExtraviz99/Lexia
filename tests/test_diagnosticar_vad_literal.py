import unittest
from scripts.diagnosticar_vad_literal import covered_seconds


class CoverageTests(unittest.TestCase):
    def test_disjoint_voice_has_zero_overlap_with_silent_tail(self):
        self.assertEqual(covered_seconds(26,40,[(0,23.4)]),0)

    def test_overlap_is_merged_before_comparing_a_human_anchor(self):
        self.assertAlmostEqual(covered_seconds(1,3,[(0,2),(1.5,4)]),2)

    def test_partial_coverage_does_not_look_like_full_coverage(self):
        self.assertAlmostEqual(covered_seconds(1,3,[(0,1.25),(2.75,4)]),.5)
        with self.assertRaises(ValueError):
            covered_seconds(3,1,[])


if __name__=='__main__':
    unittest.main()
