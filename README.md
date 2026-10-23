# Bubble sort: see and hear

The script runs locally in its own pygame window. Your existing `algo.py` is preserved.

## Install and run on macOS

Open Terminal and paste these commands, one line at a time:

```sh
cd /Users/ben/Documents/sonify
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install pygame
python bubble_sort_visualizer.py
```

Use Python 3.10 or newer. If installation reports no compatible pygame distribution with a very new Python, use Python 3.12 to create the environment instead (`python3.12 -m venv .venv312`), then activate `.venv312/bin/activate` and repeat the install/run commands.

To run it again later:

```sh
cd /Users/ben/Documents/sonify
source .venv/bin/activate
python bubble_sort_visualizer.py
```

## Controls and colors

Click the pygame window so it receives keyboard input. It starts paused.

- **Space:** start, pause, or resume.
- **R:** generate a new shuffled set and pause; press Space to start it.
- **Up / Right:** faster (up to 40 visible actions per second).
- **Down / Left:** slower (down to 1 visible action per second).
- **Esc / close window:** quit.

Blue bars are unsorted; yellow marks a comparison; pink marks an exchange; green marks values in their final positions. The counters track comparisons and swaps separately. Bubble sort compares neighbors and exchanges them if they are out of order. Each pass moves the largest remaining value into place.

Taller bars produce higher pitched notes, from 220 to 880 Hz. A comparison plays the left value; a swap plays the larger value at its new right position. Each action schedules its note and screen update together. Actual audible timing depends on your audio device; wired or built-in speakers usually have less delay than Bluetooth. At high speeds, short notes can interrupt one another to stay aligned with the current action.

If audio cannot initialize, the animation continues silently and Terminal prints the reason. Check your output device and volume. There are no numpy, sounddevice, or external audio-file dependencies.

Each bar also plays its note as it turns green. At completion, the remaining bars turn green one at a time with a short descending note sweep, at the selected speed.
