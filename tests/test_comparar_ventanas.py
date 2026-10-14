import unittest
from scripts.comparar_ventanas import experiment_plan, summarize


class ComparisonTests(unittest.TestCase):
    def test_plan_balanced_and_reproducible(self):
        windows = [0, 4, 6, 8, 10, 12]
        plan = experiment_plan(windows, 2, 20261014)
        self.assertEqual(plan, experiment_plan(windows, 2, 20261014))
        for repeat in (1, 2):
            self.assertEqual(sorted(w for r, w in plan if r == repeat), windows)

    def test_summary_includes_slow_updates_and_backward_moves(self):
        data = {"story_words": ["el", "gato"], "block_seconds":2, "updates": []}
        for t, p, movement, cost in [(2, 1, 1, 1), (4, 2, 1, 3), (6, 1, -1, 2)]:
            data["updates"].append({"audio_available_seconds":t, "position":p, "movement":movement,
                                    "processing_seconds":cost, "audio_reprocessed_seconds":t,
                                    "backlog_seconds_simulated":1, "sequential_ready_seconds_simulated":t+cost})
        out = summarize(data)
        self.assertEqual(out["processing_total_seconds"],6)
        self.assertEqual(out["over_block_updates"],1)
        self.assertEqual(out["backward_moves"],1)
        self.assertEqual(out["first_final_position_audio_seconds"],4)
        self.assertEqual(out["final_position"],1)


if __name__ == "__main__":
    unittest.main()
