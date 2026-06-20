"""Console game for Shell Game."""
import score as score_mod
import settings as settings_mod
import shell_game as core
from i18n import t
from sound import Sound


class QuitGame(Exception):
    pass


def _print(text=""):
    print(text)


def show_header(settings):
    _print("=" * 32)
    _print(t(settings["lang"], "title"))
    _print("=" * 32)


def show_help(settings):
    show_header(settings)
    _print(t(settings["lang"], "help_title"))
    _print(t(settings["lang"], "help_text"))
    input(t(settings["lang"], "press_enter"))


def show_scores(settings):
    show_header(settings)
    _print(t(settings["lang"], "scores"))
    scores = score_mod.load()
    if not scores:
        _print(t(settings["lang"], "no_scores"))
    for idx, item in enumerate(scores, 1):
        _print(f"{idx}. {item.get('name', '?')} {item.get('score', 0)} ({item.get('difficulty', '?')})")
    input(t(settings["lang"], "press_enter"))


def settings_menu(settings):
    while True:
        show_header(settings)
        _print(t(settings["lang"], "settings"))
        _print(f"{t(settings['lang'], 'lang')}: {settings['lang']}")
        _print(f"{t(settings['lang'], 'sound')}: {t(settings['lang'], 'on' if settings['sound'] else 'off')}")
        _print(f"{t(settings['lang'], 'volume')}: {settings['volume']}")
        _print(f"{t(settings['lang'], 'difficulty')}: {settings['difficulty']}")
        choice = input(t(settings["lang"], "settings_menu") + "\n" + t(settings["lang"], "choice")).strip().lower()
        if choice == "1":
            settings_mod.cycle_lang(settings)
        elif choice == "2":
            settings_mod.toggle_sound(settings)
        elif choice == "3":
            settings_mod.cycle_volume(settings)
        elif choice == "4":
            settings_mod.cycle_difficulty(settings)
        elif choice == "b":
            settings_mod.save(settings)
            return
        else:
            _print(t(settings["lang"], "unknown"))


def play_round(settings):
    lang = settings["lang"]
    difficulty = settings["difficulty"]
    cfg = core.config(difficulty)
    snd = Sound(settings["sound"], settings["volume"])
    total_score = 0
    correct_count = 0
    streak = 0

    bracket_fmt = t(lang, "cup_brackets")
    swap_sym = t(lang, "swap_symbol")

    show_header(settings)
    for round_index in range(1, cfg["rounds"] + 1):
        start = core.new_round(difficulty)
        swaps = core.make_swaps(difficulty)
        end = core.apply_swaps(start, swaps)
        _print(t(lang, "round", round=round_index, total=cfg["rounds"]))
        _print(t(lang, "cups", cups=core.cups_text(cfg["cups"], start, bracket_fmt)))
        _print(t(lang, "start", cup=start + 1))
        _print(t(lang, "swaps", swaps=core.swaps_text(swaps, swap_sym)))
        guess_text = input(t(lang, "guess_prompt")).strip().lower()
        if guess_text == "q":
            raise QuitGame()
        guess = core.parse_guess(guess_text, cfg["cups"])
        if guess is None:
            _print(t(lang, "invalid_with_range", max=cfg["cups"]))
            streak = 0
            snd.incorrect()
            continue
        if guess == end:
            streak += 1
            correct_count += 1
            points = core.score_for(difficulty, streak)
            total_score += points
            _print(t(lang, "correct", points=points))
            snd.correct()
        else:
            _print(t(lang, "wrong", cup=end + 1))
            streak = 0
            snd.incorrect()

    rating_key = core.final_rating(correct_count, cfg["rounds"])
    _print(t(lang, "finished", correct=correct_count, total=cfg["rounds"], rating=t(lang, rating_key), score=total_score))
    if correct_count:
        snd.win()
    else:
        snd.lose()
    return total_score


def main_menu():
    settings = settings_mod.load()
    while True:
        show_header(settings)
        choice = input(t(settings["lang"], "main_menu") + "\n" + t(settings["lang"], "choice")).strip().lower()
        if choice == "p":
            try:
                result = play_round(settings)
            except QuitGame:
                result = 0
            if result > 0:
                name = input(t(settings["lang"], "name_prompt")).strip()
                if name:
                    score_mod.add(name, result, settings["difficulty"])
                    _print(t(settings["lang"], "saved"))
                else:
                    _print(t(settings["lang"], "not_saved"))
            input(t(settings["lang"], "press_enter"))
        elif choice == "h":
            show_help(settings)
        elif choice == "s":
            settings_menu(settings)
        elif choice == "c":
            show_scores(settings)
        elif choice == "q":
            _print(t(settings["lang"], "bye"))
            return
        else:
            _print(t(settings["lang"], "unknown"))


if __name__ == "__main__":
    main_menu()
