
import numpy as np
import sounddevice as sd
import random

SAMPLE_RATE = 44100

def play_note(value, duration=0.07):
    # Map a number to a musical frequency
    frequency = 220 * 2 ** (value / 12)

    t = np.linspace(
        0, duration,
        int(SAMPLE_RATE * duration),
        endpoint=False
    )

    # Sine wave with fade-in and fade-out
    envelope = np.sin(np.pi * t / duration) ** 2
    wave = 0.2 * np.sin(2 * np.pi * frequency * t)
    wave *= envelope

    sd.play(wave, SAMPLE_RATE)
    sd.wait()


def bubble_sort_sonified(numbers):
    a = numbers.copy()

    for i in range(len(a)):
        for j in range(len(a) - i - 1):

            # Sonify the comparison
            play_note(a[j])

            if a[j] > a[j + 1]:
                a[j], a[j + 1] = a[j + 1], a[j]

    return a


numbers = list(range(1, 25))
random.shuffle(numbers)

print("Before:", numbers)
sorted_numbers = bubble_sort_sonified(numbers)
print("After:", sorted_numbers)