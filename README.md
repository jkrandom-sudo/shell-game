# Shell Game / 猜杯子

A bilingual console shell-game memory tracker written with the Python standard library.

一个使用 Python 标准库编写的双语控制台猜杯子小游戏。

## Features / 功能

- Track a hidden ball under numbered cups.
- Watch swap instructions and pick the final cup.
- Three difficulty levels with more cups, swaps, and rounds.
- Bilingual UI: English and Chinese.
- Persistent JSON settings and top scores.
- Optional terminal bell sound with adjustable volume.
- Automated tests for core logic, persistence modules, sound, and menu gameplay.

## Requirements / 环境要求

- Python 3.9+
- No third-party dependencies.

## Run / 启动

```bash
python3 game.py
```

## Test / 测试

```bash
python3 -m py_compile game.py shell_game.py i18n.py settings.py score.py sound.py
python3 tests/run_tests.py
```

## How to Play / 玩法

1. Choose Play from the main menu.
2. Note which cup starts with the hidden ball.
3. Follow each displayed swap such as `1<->2`.
4. Enter the final cup number.
5. Score increases with correct streaks.
6. Type `q` to quit the current round.

## Difficulty / 难度

| Difficulty | Cups | Swaps per round | Rounds | Score bonus |
| --- | ---: | ---: | ---: | ---: |
| easy | 3 | 4 | 5 | 1x |
| normal | 4 | 6 | 6 | 2x |
| hard | 5 | 8 | 7 | 3x |

## Files / 文件

- `game.py` — console UI and menus.
- `shell_game.py` — core cup, swap, scoring, and rating logic.
- `i18n.py` — bilingual strings.
- `settings.py` — JSON settings persistence.
- `score.py` — JSON score persistence.
- `sound.py` — terminal bell sound helper.
- `tests/` — automated unit tests.
