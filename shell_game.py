"""Core logic for Shell Game."""
import random

DIFFICULTY_CONFIG = {
    "easy": {"cups": 3, "swaps": 4, "rounds": 5, "bonus": 1},
    "normal": {"cups": 4, "swaps": 6, "rounds": 6, "bonus": 2},
    "hard": {"cups": 5, "swaps": 8, "rounds": 7, "bonus": 3},
}


def config(difficulty):
    return DIFFICULTY_CONFIG.get(difficulty, DIFFICULTY_CONFIG["normal"])


def new_round(difficulty, rng=None):
    rng = rng or random
    cups = config(difficulty)["cups"]
    return rng.randrange(cups)


def make_swaps(difficulty, rng=None):
    rng = rng or random
    cfg = config(difficulty)
    swaps = []
    for _ in range(cfg["swaps"]):
        a = rng.randrange(cfg["cups"])
        b = rng.randrange(cfg["cups"])
        while b == a:
            b = rng.randrange(cfg["cups"])
        swaps.append((a, b))
    return swaps


def apply_swaps(ball_pos, swaps):
    for a, b in swaps:
        if ball_pos == a:
            ball_pos = b
        elif ball_pos == b:
            ball_pos = a
    return ball_pos


def parse_guess(text, cups):
    text = text.strip()
    if not text.isdigit():
        return None
    value = int(text)
    if 1 <= value <= cups:
        return value - 1
    return None


def cups_text(cups, reveal=None, bracket_fmt="[{num}]"):
    parts = []
    for idx in range(cups):
        label = str(idx + 1)
        if reveal == idx:
            label += "*"
        parts.append(bracket_fmt.format(num=label))
    return " ".join(parts)


def swaps_text(swaps, swap_symbol="<->"):
    return " ".join(f"{a + 1}{swap_symbol}{b + 1}" for a, b in swaps)


def score_for(difficulty, streak, correct=True):
    if not correct:
        return 0
    return (20 + streak * 10) * config(difficulty)["bonus"]


def final_rating(correct, rounds):
    if correct == rounds:
        return "perfect"
    if correct >= max(1, rounds * 2 // 3):
        return "sharp"
    if correct >= max(1, rounds // 3):
        return "lucky"
    return "lost"
