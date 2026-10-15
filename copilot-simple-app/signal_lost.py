"""SIGNAL LOST: a small terminal survival adventure."""

from __future__ import annotations

import argparse
import json
import os
import random
import sys
import time
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

RESET = "\033[0m"
DIM = "\033[2m"
CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
MAGENTA = "\033[95m"
WHITE = "\033[97m"
HIGH_SCORE_PATH = Path(__file__).with_name("highscores.json")
HIGH_SCORE_LIMIT = 10

TITLE_ART = r"""
    ##### ##### ##### #   #  ###  #
    #       #   #     ##  # #   # #
    #####   #   # ### # # # ##### #
        #   #   #   # #  ## #   # #
    ##### ##### ##### #   # #   # #####

    #     ##### ##### #####
    #     #   # #       #  
    #     #   # #####   #  
    #     #   #     #   #  
    ##### ##### #####   #  

           S I G N A L   L O S T
"""


SCENES = {
    "crash_site": {
        "art": r"""
          .  *       .       *
              _.-^^---....,,--
          _--                  --_
         <   CARGO SHIP  //     >
          \._                _.-'
             `--.________.--'
                 /|  |\
                /_|__|_\
          _____/  WRECK  \_____
""",
        "text": "The impact has stopped. Your cargo ship is split open beneath a black sky. The emergency beacon is silent, and your suit reports a dwindling oxygen reserve.",
        "choices": [
            {"label": "Search the cargo hold", "target": "cargo_hold"},
            {"label": "Step onto the moon", "target": "moon_plain"},
        ],
    },
    "cargo_hold": {
        "art": r"""
          ______________________
         /  CARGO BAY  / / /    \
        | [##]  [##]  [##]       |
        |   ____       _____     |
        |  |____|     |_____||   |
        |        \___/            |
        |   EMERGENCY LOCKER      |
        |________________________|
""",
        "text": "The cargo hold is buckled but pressurized enough to search. A marked emergency locker hangs open near the airlock.",
        "choices": [
            {"label": "Take the plasma cutter", "add_item": "plasma_cutter", "not_has": "plasma_cutter"},
            {"label": "Take the O2 canister", "add_item": "oxygen_canister", "not_has": "oxygen_canister"},
            {"label": "Climb out to the moon", "target": "moon_plain"},
            {"label": "Return to the cockpit", "target": "crash_site"},
        ],
    },
    "moon_plain": {
        "art": r"""
                 .       *          .
           *          .       .        *
                  .-'----'-.
                .'  .--.  '.
          _____/___/____\___\_____
         /  .   .   .   .   .      \
        /____.____.____.____.________\
            /  /             \  \
""",
        "text": "A gray plain stretches between the wreck, a split in the moon's crust, and a ridge crowned by a blinking red light. Geometric stones glimmer farther east.",
        "choices": [
            {"label": "Descend into the fissure", "target": "fissure"},
            {"label": "Follow the shallow gully", "target": "gully"},
            {"label": "Investigate the alien ruins", "target": "ruin_gate"},
            {"label": "Climb toward the beacon ridge", "target": "ridge"},
            {"label": "Give up and wait in the dark", "target": "ending_stranded"},
        ],
    },
    "fissure": {
        "art": r"""
             .  .       .  .
          ___/ \_________/ \___
         /                       \
        |       MOON FISSURE       |
        |          .  *             |
        |         / \               |
        |        /   \               |
        |_______/     \______________|
                \     /
                 \___/
""",
        "text": "A narrow fissure cuts through the basalt. Cold air drifts up from somewhere below, carrying a faint blue glow.",
        "choices": [
            {"label": "Squeeze down into the cave", "target": "cave", "cost": 2},
            {"label": "Climb back to the plain", "target": "moon_plain"},
        ],
    },
    "cave": {
        "art": r"""
             __________________
          .-'                  '-.
         /     /\       /\        \
        |     /  \  *  /  \         |
        |    /____\   /____\    .   |
        |       .      _____        |
        |      / \    /     \       |
         \____/___\__/_______\_____/
""",
        "text": "The cave walls are veined with luminous mineral. An alien mechanism is embedded in a crystal seam; something key-shaped shines inside it.",
        "choices": [
            {"label": "Cut the crystal and take the alien key", "requires": ["plasma_cutter"], "add_item": "alien_key", "not_has": "alien_key"},
            {"label": "Follow the markings toward the ruins", "target": "ruin_gate"},
            {"label": "Climb back through the fissure", "target": "fissure"},
        ],
    },
    "gully": {
        "art": r"""
          _..---.._
       .-'         '-.
      /   .-----.     \
     /   /       \     \
    |   |  GULLY  |     |
    |    \_______/   *  |
     \      ____       /
      '.___/    \___.-'
         /        \
""",
        "text": "The gully shields you from the wind. A trail leads toward the ship's scattered equipment, while another narrows into the glowing cave fissure.",
        "choices": [
            {"label": "Search the scattered wreckage", "target": "wreckage"},
            {"label": "Enter the glowing fissure", "target": "fissure"},
            {"label": "Return to the open plain", "target": "moon_plain"},
        ],
    },
    "ruin_gate": {
        "art": r"""
              .-----------.
             /  _  _  _    \
            |  |_| |_| |_|   |
            |  |  ALIEN  |   |
            |  |  GATE   |   |
            |  |_________|   |
            |   /       \    |
         ___|__/_________\___|___
""",
        "text": "A gate of dark stone rises from the plain. Its surface is seamless except for a key-shaped recess surrounded by unfamiliar symbols.",
        "choices": [
            {"label": "Use the alien key to open the archive", "requires": ["alien_key"], "target": "alien_archive"},
            {"label": "Return to the moon plain", "target": "moon_plain"},
        ],
    },
    "alien_archive": {
        "art": r"""
          _______________________
         /  *   *   *   *   *     \
        |   .-----------------.   |
        |   |  /\/\  /\  /\/\ |   |
        |   |  ancient signal |   |
        |   |  /\  \/  \/  /\  |   |
        |   '-----------------'   |
         \___________*___________/
""",
        "text": "The gate opens onto a silent archive. A living pattern pulses across the walls, answering the alien key in your glove.",
        "choices": [
            {"label": "Answer the signal and join the archive", "target": "ending_alien"},
            {"label": "Copy the tower's coordinates and leave", "target": "ridge"},
            {"label": "Return to the stone gate", "target": "ruin_gate"},
        ],
    },
    "wreckage": {
        "art": r"""
          \  .  .  .  .  .  .  /
        ___\__________________/___
       /   /   BROKEN HULL    \   \
      |   |  [KIT]       [O2]  |   |
      |    \____       _______/   |
      |         \_____/            |
       \__________________________/
""",
        "text": "A cargo pod lies half-buried in dust. Its emergency kit is intact, and a spare canister is wedged beside it.",
        "choices": [
            {"label": "Take the spare O2 canister", "add_item": "oxygen_canister", "not_has": "oxygen_canister"},
            {"label": "Take the first-aid kit", "add_item": "medkit", "not_has": "medkit"},
            {"label": "Use the first-aid kit", "requires": ["medkit"], "action": "use_medkit"},
            {"label": "Return through the gully", "target": "gully"},
            {"label": "Head back to the crash site", "target": "crash_site"},
        ],
    },
    "ridge": {
        "art": r"""
                   /\        /\
             /\   /  \  /\  /  \
            /  \_/    \/  \/    \
           /         BEACON       \
          /   .          |          \
         /_______________|___________\
                  /      |      \
                 /_______|_______\
""",
        "text": "From the ridge, you can see the beacon tower stuttering against the stars. A steep path descends to its sealed service hatch.",
        "choices": [
            {"label": "Approach the tower", "target": "tower_base"},
            {"label": "Descend to the moon plain", "target": "moon_plain"},
            {"label": "Follow the ridge back to the ruins", "target": "ruin_gate"},
        ],
    },
    "tower_base": {
        "art": r"""
                  |  /\
                  | /  \
                __|/____\__
               |  /  []  \  |
               | | SIGNAL | |
               | | TOWER  | |
               | |___  ___| |
               |_|__|__|__|_|
                 / SERVICE \
""",
        "text": "The beacon tower's service hatch is fused shut. A control panel flashes once, then goes dark. The signal needs a manual restart from inside.",
        "choices": [
            {"label": "Cut through the service hatch", "requires": ["plasma_cutter"], "target": "tower_interior"},
            {"label": "Return to the ridge", "target": "ridge"},
        ],
    },
    "tower_interior": {
        "art": r"""
             .----------------.
             |  .----. .----. |
             |  | 00 | | 00 | |
             |  '----' '----' |
             |   BEACON CORE  |
             |    \  ||  /    |
             |  ___\_||_/___  |
             '----------------'
""",
        "text": "The tower is cold and dark. At its center, the beacon's security console waits for a four-digit override code.",
        "choices": [
            {"label": "Hack the beacon console", "action": "hack"},
            {"label": "Leave the tower", "target": "tower_base"},
        ],
    },
    "ending_rescued": {
        "art": r"""
             *       .       *
          .     \    |    /      .
             ----\  |  /----
          .       \ | /          *
          ==========*==========
             RESCUE INBOUND
          .       / | \          .
             ----/  |  \----
""",
        "text": "The beacon catches. A reply crackles through your helmet: rescue craft inbound. You made it.",
        "choices": [],
        "ending": "rescued",
    },
    "ending_stranded": {
        "art": r"""
              .       *       .
           .      _______        *
                .'       '.
               /  NO      \
              |   SIGNAL   |
               \_________/
          .       .   .       .
""",
        "text": "The silence settles in. No rescue is coming, and the moon keeps your secret.",
        "choices": [],
        "ending": "stranded",
    },
    "ending_alien": {
        "art": r"""
           .       /\       .
              *   /  \   *
           _____ / /\ \ _____
          /     / /  \ \     \
         |  *  | | () | |  *  |
          \_____\ \__/ /_____/
             YOU ARE THE SIGNAL
""",
        "text": "The archive recognizes you as its missing voice. Your distress call becomes something older, wider, and no longer human.",
        "choices": [],
        "ending": "alien",
    },
    "ending_oxygen": {
        "art": r"""
             .----------------.
             | O2: 00%         |
             |      .----.     |
             |     / X  X \    |
             |     \  __  /    |
             |      '----'     |
             '----------------'
                  ... ...
""",
        "text": "Your oxygen reaches zero. The beacon is still out there, but you cannot go on.",
        "choices": [],
        "ending": "oxygen",
    },
}

ITEM_LABELS = {
    "plasma_cutter": "Plasma cutter",
    "oxygen_canister": "O2 canister",
    "alien_key": "Alien key",
    "medkit": "Medkit",
}

SCENE_COLORS = {
    "crash_site": RED,
    "cargo_hold": YELLOW,
    "moon_plain": CYAN,
    "fissure": MAGENTA,
    "cave": MAGENTA,
    "gully": YELLOW,
    "ruin_gate": GREEN,
    "alien_archive": MAGENTA,
    "wreckage": RED,
    "ridge": CYAN,
    "tower_base": YELLOW,
    "tower_interior": GREEN,
}


def mastermind_feedback(code: str, guess: str) -> tuple[int, int]:
    """Return (exact-position matches, correct digits in other positions)."""
    exact = sum(secret_digit == guess_digit for secret_digit, guess_digit in zip(code, guess))
    shared = sum((Counter(code) & Counter(guess)).values())
    return exact, shared - exact


def load_high_scores(path: Path = HIGH_SCORE_PATH) -> list[dict]:
    try:
        with path.open(encoding="utf-8") as score_file:
            data = json.load(score_file)
    except FileNotFoundError:
        return []

    if not isinstance(data, dict) or not isinstance(data.get("scores"), list):
        raise ValueError(f"Invalid high-score file format: {path}")
    scores = data["scores"]
    if any(
        not isinstance(entry, dict)
        or not isinstance(entry.get("score"), int)
        or isinstance(entry.get("score"), bool)
        for entry in scores
    ):
        raise ValueError(f"Invalid high-score entry in {path}")
    return scores


def save_high_score(entry: dict, path: Path = HIGH_SCORE_PATH) -> list[dict]:
    scores = load_high_scores(path)
    scores.append(entry)
    scores.sort(key=lambda saved_score: saved_score["score"], reverse=True)
    scores = scores[:HIGH_SCORE_LIMIT]
    with path.open("w", encoding="utf-8") as score_file:
        json.dump({"scores": scores}, score_file, indent=2)
        score_file.write("\n")
    return scores


class SignalLost:
    def __init__(self, seed: int | None = None, fast: bool = False):
        self.rng = random.Random(seed)
        self.fast = fast
        self.scene_id = "crash_site"
        self.oxygen = 70
        self.max_oxygen = 100
        self.hp = 3
        self.items: set[str] = set()
        self.items_found: set[str] = set()
        self.ending: str | None = None
        self.message = ""
        self.secret_code = f"{self.rng.randrange(10_000):04d}"

    @property
    def score(self) -> int:
        secret_bonus = 100 if self.ending == "alien" else 0
        return max(0, self.oxygen) + len(self.items_found) + secret_bonus

    def clear_screen(self) -> None:
        os.system("cls" if os.name == "nt" else "clear")

    def type_text(self, text: str) -> None:
        if self.fast:
            print(text)
            return
        for character in text:
            print(character, end="", flush=True)
            if character not in "\n\r":
                time.sleep(0.008)
        print()

    def hud(self) -> str:
        filled = max(0, min(10, round(self.oxygen / self.max_oxygen * 10)))
        oxygen_bar = "█" * filled + "░" * (10 - filled)
        hearts = "♥" * max(0, self.hp) + "♡" * max(0, 3 - self.hp)
        item_list = ", ".join(ITEM_LABELS[item] for item in sorted(self.items)) or "none"
        return f"O2 {oxygen_bar} {self.oxygen}% | HP {hearts} | Items: {item_list}"

    def render(self) -> None:
        self.clear_screen()
        scene = SCENES[self.scene_id]
        color = SCENE_COLORS.get(self.scene_id, WHITE)
        print(self.hud())
        print(f"{color}{scene['art']}{RESET}")
        self.type_text(scene["text"])
        if self.message:
            print(f"{YELLOW}{self.message}{RESET}")
            self.message = ""

    def render_title(self) -> None:
        self.clear_screen()
        print(self.hud())
        print(f"{CYAN}{TITLE_ART}{RESET}")
        self.type_text("LAST CREW MEMBER. DEAD MOON. ONE BEACON. DON'T LET THE LIGHT GO OUT.")
        input("\nPress Enter to begin...")

    def available_choices(self) -> list[dict]:
        available = []
        for choice in SCENES[self.scene_id]["choices"]:
            if all(item in self.items for item in choice.get("requires", [])):
                if choice.get("not_has") and choice["not_has"] in self.items:
                    continue
                available.append(choice)
        return available

    def show_choices(self, available: list[dict]) -> None:
        for number, choice in enumerate(available, start=1):
            cost = choice.get("cost", 1)
            suffix = f" ({cost} O2)" if cost > 1 else ""
            print(f"  {number}. {choice['label']}{suffix}")
        for choice in SCENES[self.scene_id]["choices"]:
            missing = [ITEM_LABELS[item] for item in choice.get("requires", []) if item not in self.items]
            if missing:
                print(f"  {DIM}-- {choice['label']} [requires {', '.join(missing)}]{RESET}")

    def take_turn(self, cost: int, before_event=None) -> bool:
        self.oxygen -= cost
        if before_event:
            before_event()

        event_roll = self.rng.random()
        if event_roll < 0.04:
            self.oxygen -= 2
            self.message = "RANDOM EVENT: An O2 line ruptures! You lose 2 additional oxygen."
        elif event_roll < 0.08:
            self.hp -= 1
            self.message = "RANDOM EVENT: A meteor shower clips your suit. You lose 1 HP."

        if self.oxygen <= 0:
            self.scene_id = "ending_oxygen"
            self.ending = "oxygen"
            return False
        if self.hp <= 0:
            self.scene_id = "ending_stranded"
            self.ending = "stranded"
            self.message = "Your suit fails after the impact. You cannot continue."
            return False
        return True

    def apply_choice(self, choice: dict) -> None:
        action = choice.get("action")

        def apply_item_action() -> None:
            if choice.get("add_item"):
                item = choice["add_item"]
                self.items.add(item)
                self.items_found.add(item)
                self.message = f"Added: {ITEM_LABELS[item]}."
            elif action == "use_oxygen":
                self.items.remove("oxygen_canister")
                self.oxygen = min(self.max_oxygen, self.oxygen + 4)
                self.message = "The canister hisses open. Oxygen reserve restored by 4%."
            elif action == "use_medkit":
                self.items.remove("medkit")
                self.hp = min(3, self.hp + 1)
                self.message = "You patch the suit and steady your breathing. HP restored by 1."

        if not self.take_turn(choice.get("cost", 1), apply_item_action):
            return

        if action == "hack":
            self.play_hacking_puzzle()
            return

        target = choice.get("target")
        if target:
            self.scene_id = target
            ending = SCENES[target].get("ending")
            if ending:
                self.ending = ending

    def use_inventory_item(self) -> bool:
        options = []
        if "oxygen_canister" in self.items:
            options.append(("oxygen_canister", "Use O2 canister", "use_oxygen"))
        if "medkit" in self.items and self.hp < 3:
            options.append(("medkit", "Use medkit", "use_medkit"))
        if not options:
            return False

        print("\n  I. Inventory")
        for number, (_, label, _) in enumerate(options, start=1):
            print(f"     {number}. {label}")
        print("     0. Cancel")
        selected = input("Use item (or press Enter to cancel): ").strip()
        if not selected or selected == "0":
            return True
        if not selected.isdigit() or not 1 <= int(selected) <= len(options):
            self.message = "That item selection is not available."
            return True

        item, _, action = options[int(selected) - 1]
        choice = {"action": action}
        if item == "oxygen_canister":
            choice["cost"] = 1
        self.apply_choice(choice)
        return True

    def play_hacking_puzzle(self) -> None:
        history: list[str] = []
        attempt = 1
        while attempt <= 6:
            self.clear_screen()
            print(self.hud())
            print(f"{GREEN}{SCENES['tower_interior']['art']}{RESET}")
            print(f"BEACON OVERRIDE — attempt {attempt}/6")
            for line in history:
                print(line)
            guess = input("Enter a four-digit code: ").strip()
            if len(guess) != 4 or not guess.isdigit():
                history.append("Invalid entry. Enter exactly four digits; no oxygen spent.")
                continue

            if not self.take_turn(1):
                return

            exact, misplaced = mastermind_feedback(self.secret_code, guess)
            if exact == 4:
                self.scene_id = "ending_rescued"
                self.ending = "rescued"
                return

            history.append(
                f"{guess}: {exact} correct position(s), {misplaced} correct digit(s) misplaced."
            )
            attempt += 1

        self.scene_id = "ending_stranded"
        self.ending = "stranded"
        self.message = "The console locks you out. The beacon remains silent."

    def run(self) -> None:
        self.render_title()
        while self.ending is None:
            self.render()
            available = self.available_choices()
            self.show_choices(available)
            if self.items and ("oxygen_canister" in self.items or "medkit" in self.items):
                print("  I. Use an inventory item")
            selected = input("\nChoose an action: ").strip().lower()
            if selected == "i" and self.use_inventory_item():
                continue
            if not selected.isdigit() or not 1 <= int(selected) <= len(available):
                self.message = "Choose one of the listed options."
                continue
            self.apply_choice(available[int(selected) - 1])

        self.render()
        score_entry = {
            "score": self.score,
            "oxygen_left": max(0, self.oxygen),
            "items_found": len(self.items_found),
            "ending": self.ending,
            "played_at": datetime.now(timezone.utc).isoformat(),
        }
        scores = save_high_score(score_entry)
        print(f"\nFINAL SCORE: {self.score}")
        print("HIGH SCORES")
        for position, entry in enumerate(scores[:5], start=1):
            print(f"  {position:>2}. {entry['score']:>3}  ({entry['ending']})")
        input("\nPress Enter to exit...")


def main() -> None:
    parser = argparse.ArgumentParser(description="Play SIGNAL LOST, a terminal survival adventure.")
    parser.add_argument("--seed", type=int, help="Seed random events for reproducible runs.")
    parser.add_argument("--fast", action="store_true", help="Skip the typewriter text effect.")
    args = parser.parse_args()
    os.system("")
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    SignalLost(seed=args.seed, fast=args.fast).run()


if __name__ == "__main__":
    main()
