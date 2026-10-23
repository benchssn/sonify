#!/usr/bin/env python3
"""Bubble sort you can see and hear (macOS, Python 3.10+).

Setup in Terminal:
    cd /Users/ben/Documents/sonify
    python3 -m venv .venv
    source .venv/bin/activate
    python -m pip install pygame
    python bubble_sort_visualizer.py

Space: pause/resume | R: reshuffle | Up/Right: faster | Down/Left: slower
Escape or close window: quit. Starts paused so you can read the controls.
Only pygame is required; tones use Python's standard library, not audio files.
"""

import math
import random
from array import array

BAR_COUNT = 32
SAMPLE_RATE = 44100


def bubble_steps(values):
    """Yield one visible action at a time; sort the supplied list in place.

    Each result is (action, active_indices, first_sorted_index).
    The green suffix contains values already in their final positions.
    """
    sorted_from = len(values)
    for end in range(len(values) - 1, 0, -1):
        changed = False
        for j in range(end):
            yield "compare", (j, j + 1), end + 1
            if values[j] > values[j + 1]:
                values[j], values[j + 1] = values[j + 1], values[j]
                changed = True
                yield "swap", (j, j + 1), end + 1
        sorted_from = end
        yield "settled", (end,), end
        if not changed:
            break
    # Sound each remaining bar as the green region expands to the left.
    for index in range(sorted_from - 1, -1, -1):
        yield "settled", (index,), index
    yield "done", (), 0


def tone_samples(value, count=BAR_COUNT):
    """Map bar height to two octaves, 220–880 Hz, with a soft envelope."""
    frequency = 220 * 2 ** (2 * (value - 1) / max(1, count - 1))
    length = int(SAMPLE_RATE * 0.055)
    return array("h", (
        int(0.18 * 32767 * math.sin(2 * math.pi * frequency * i / SAMPLE_RATE)
            * math.sin(math.pi * i / (length - 1)) ** 2)
        for i in range(length)
    ))


def main():
    try:
        import pygame
    except ImportError:
        raise SystemExit("pygame is missing. Activate your virtual environment, then run:\n"
                         "python -m pip install pygame")

    # Initialize display separately: lack of an audio device must not stop the app.
    pygame.display.init()
    pygame.font.init()
    screen = pygame.display.set_mode((1000, 680))
    pygame.display.set_caption("Bubble Sort — See and Hear")
    font = pygame.font.Font(None, 27)
    small = pygame.font.Font(None, 23)
    clock = pygame.time.Clock()
    sounds = {}
    channel = None
    audio_status = "Sound on: taller bars play higher notes"
    try:
        pygame.mixer.init(frequency=SAMPLE_RATE, size=-16, channels=1, buffer=512)
        channel = pygame.mixer.Channel(0)
        sounds = {v: pygame.mixer.Sound(buffer=tone_samples(v))
                  for v in range(1, BAR_COUNT + 1)}
    except pygame.error as error:
        audio_status = "Audio unavailable — visual mode (see Terminal)"
        print(f"Audio unavailable: {error}. Continuing with visuals.")

    def reset():
        values = list(range(1, BAR_COUNT + 1))
        random.shuffle(values)
        return values, bubble_steps(values)

    values, steps = reset()
    paused, finished, running = True, False, True
    action, active, sorted_from = "ready", (), BAR_COUNT
    comparisons = swaps = 0
    speed = 12.0  # Visible actions per second, not frames per second.
    elapsed = 0.0

    def label(text, x, y, color=(220, 227, 240), compact=False):
        screen.blit((small if compact else font).render(text, True, color), (x, y))

    try:
        while running:
            dt = clock.tick(60) / 1000
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    elif event.key == pygame.K_SPACE and not finished:
                        paused = not paused
                        elapsed = 0.0
                        if paused and channel:
                            channel.stop()
                    elif event.key == pygame.K_r:
                        values, steps = reset()
                        action, active, sorted_from = "ready", (), BAR_COUNT
                        comparisons = swaps = 0
                        paused, finished, elapsed = True, False, 0.0
                        if channel:
                            channel.stop()
                    elif event.key in (pygame.K_UP, pygame.K_RIGHT):
                        speed = min(40.0, speed * 1.25)
                    elif event.key in (pygame.K_DOWN, pygame.K_LEFT):
                        speed = max(1.0, speed / 1.25)

            if not running:
                break
            if not paused and not finished:
                elapsed += dt
                if elapsed >= 1 / speed:
                    # Never catch up with a burst: every action gets a visible frame.
                    elapsed = 0.0
                    action, active, sorted_from = next(steps)
                    comparisons += action == "compare"
                    swaps += action == "swap"
                    if active and channel:
                        # A comparison sounds the left bar; a swap sounds the
                        # right bar after the exchange (the larger value).
                        # Settled bars sound as they turn green.
                        index = active[1] if action == "swap" else active[0]
                        channel.play(sounds[values[index]])
                    if action == "done":
                        finished = True

            screen.fill((17, 22, 34))
            label("BUBBLE SORT  /  SEE + HEAR", 30, 24)
            label("Space: pause/resume    R: reshuffle    Arrows: speed    Esc: quit",
                  30, 65, compact=True)
            status = "SORTED! Press R to start again" if finished else (
                "PAUSED — press Space" if paused else "SORTING")
            label(f"{status}    |    {speed:.1f} actions/sec", 30, 105)
            label(f"Comparisons: {comparisons}     Swaps: {swaps}     Action: {action}",
                  30, 140, compact=True)
            baseline, max_height = 565, 350
            width = 940 / BAR_COUNT
            for i, value in enumerate(values):
                color = (79, 163, 230)
                if i >= sorted_from:
                    color = (87, 207, 145)
                if i in active:
                    if action == "settled":
                        color = (145, 255, 185)
                    else:
                        color = (255, 199, 77) if action == "compare" else (246, 113, 144)
                height = max_height * value / BAR_COUNT
                pygame.draw.rect(screen, color,
                                 (30 + i * width, baseline - height, width - 4, height),
                                 border_radius=3)
                label(str(value), int(31 + i * width), baseline + 9, compact=True)
            label("Blue: unsorted    Yellow: comparing    Pink: swapped    Green: final position",
                  30, 612, compact=True)
            label(audio_status, 30, 643, compact=True)
            # Sound is scheduled with the action immediately before its frame.
            pygame.display.flip()
    finally:
        pygame.quit()


if __name__ == "__main__":
    main()
