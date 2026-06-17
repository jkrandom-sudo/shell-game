import unittest

import shell_game as core


class FixedRng:
    def __init__(self, values):
        self.values = list(values)

    def randrange(self, stop):
        return self.values.pop(0) % stop


class TestCore(unittest.TestCase):
    def test_config_fallback(self):
        self.assertEqual(core.config("bad"), core.config("normal"))

    def test_new_round(self):
        self.assertEqual(core.new_round("easy", FixedRng([2])), 2)

    def test_make_swaps_avoids_same_cup(self):
        swaps = core.make_swaps("easy", FixedRng([0, 0, 1, 2, 2, 0, 1, 1, 2, 0, 2, 1]))
        self.assertEqual(len(swaps), 4)
        self.assertTrue(all(a != b for a, b in swaps))

    def test_apply_swaps(self):
        self.assertEqual(core.apply_swaps(0, [(0, 1), (1, 2)]), 2)
        self.assertEqual(core.apply_swaps(2, [(0, 1)]), 2)

    def test_parse_guess(self):
        self.assertEqual(core.parse_guess("1", 3), 0)
        self.assertEqual(core.parse_guess("3", 3), 2)
        self.assertIsNone(core.parse_guess("0", 3))
        self.assertIsNone(core.parse_guess("4", 3))
        self.assertIsNone(core.parse_guess("x", 3))

    def test_cups_text(self):
        self.assertEqual(core.cups_text(3), "[1] [2] [3]")
        self.assertEqual(core.cups_text(3, 1), "[1] [2*] [3]")

    def test_swaps_text(self):
        self.assertEqual(core.swaps_text([(0, 1), (2, 0)]), "1<->2 3<->1")

    def test_score_for(self):
        self.assertEqual(core.score_for("easy", 2), 40)
        self.assertEqual(core.score_for("normal", 2), 80)
        self.assertEqual(core.score_for("easy", 2, correct=False), 0)

    def test_final_rating(self):
        self.assertEqual(core.final_rating(5, 5), "perfect")
        self.assertEqual(core.final_rating(4, 6), "sharp")
        self.assertEqual(core.final_rating(2, 6), "lucky")
        self.assertEqual(core.final_rating(0, 6), "lost")


if __name__ == "__main__":
    unittest.main()
