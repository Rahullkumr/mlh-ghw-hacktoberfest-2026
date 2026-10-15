import unittest
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from signal_lost import SCENES, SignalLost, load_high_scores, mastermind_feedback, save_high_score


class SignalLostTests(unittest.TestCase):
    def test_scene_data_has_twelve_explorable_scenes_and_four_endings(self):
        endings = {key for key, scene in SCENES.items() if scene.get("ending")}
        self.assertEqual(len(endings), 4)
        self.assertGreaterEqual(len(SCENES) - len(endings), 12)
        for scene in SCENES.values():
            self.assertTrue(scene["art"].strip())
            self.assertIn("text", scene)
            self.assertIn("choices", scene)

    def test_mastermind_feedback_accounts_for_duplicate_digits(self):
        self.assertEqual(mastermind_feedback("1123", "1211"), (1, 2))
        self.assertEqual(mastermind_feedback("1234", "5678"), (0, 0))

    def test_oxygen_depletion_routes_to_oxygen_ending(self):
        game = SignalLost(seed=7, fast=True)
        game.oxygen = 1
        self.assertFalse(game.take_turn(1))
        self.assertEqual(game.ending, "oxygen")
        self.assertEqual(game.scene_id, "ending_oxygen")

    def test_inventory_unlocks_the_archive_and_tower(self):
        game = SignalLost(seed=7, fast=True)
        game.scene_id = "ruin_gate"
        self.assertFalse(any(choice.get("target") == "alien_archive" for choice in game.available_choices()))
        game.items.add("alien_key")
        self.assertTrue(any(choice.get("target") == "alien_archive" for choice in game.available_choices()))

        game.scene_id = "tower_base"
        self.assertFalse(any(choice.get("target") == "tower_interior" for choice in game.available_choices()))
        game.items.add("plasma_cutter")
        self.assertTrue(any(choice.get("target") == "tower_interior" for choice in game.available_choices()))

    def test_invalid_hacking_input_does_not_consume_a_guess(self):
        game = SignalLost(seed=7, fast=True)
        game.scene_id = "tower_interior"
        output = StringIO()
        with patch("builtins.input", side_effect=["abcd", game.secret_code]), redirect_stdout(output):
            game.play_hacking_puzzle()

        self.assertEqual(game.ending, "rescued")
        self.assertEqual(output.getvalue().count("BEACON OVERRIDE — attempt 1/6"), 2)

    def test_score_counts_remaining_oxygen_items_found_and_secret_bonus(self):
        game = SignalLost(seed=7, fast=True)
        game.oxygen = 42
        game.items_found.update({"plasma_cutter", "alien_key"})
        game.ending = "rescued"
        self.assertEqual(game.score, 44)

        game.ending = "alien"
        self.assertEqual(game.score, 144)

    def test_high_scores_are_persisted_and_limited_to_ten(self):
        with TemporaryDirectory() as temporary_directory:
            path = Path(temporary_directory) / "highscores.json"
            for score in range(12):
                save_high_score({"score": score, "ending": "rescued"}, path)

            scores = load_high_scores(path)
            self.assertEqual(len(scores), 10)
            self.assertEqual([entry["score"] for entry in scores], list(range(11, 1, -1)))


if __name__ == "__main__":
    unittest.main()
