# Three more sorting visualizers

Each script is standalone and needs only pygame. Your bubble sort script is unchanged.

## Run on macOS

If you already installed pygame in `.venv`, open Terminal and run:

```sh
cd /Users/ben/Documents/sonify
source .venv/bin/activate
python selection_sort_visualizer.py
```

Or replace the last line with either:

```sh
python insertion_sort_visualizer.py
python quick_sort_visualizer.py
```

Run one at a time; close its window before running the next command.

For a fresh installation, create the environment first:

```sh
cd /Users/ben/Documents/sonify
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install pygame
```

Python 3.10+ is supported; Python 3.12 is a convenient choice with available pygame wheels.

## Controls

Click the window to give it keyboard focus. Space starts/pauses/resumes; R reshuffles and pauses; Up/Right speeds up; Down/Left slows down; Esc quits.

Yellow bars are compared; pink bars have just swapped; green bars are in their final positions. Every bar sounds once as it turns green. Taller bars play higher notes. Comparisons play the first highlighted bar and swaps play the value at the second highlighted position. High speeds can interrupt short notes. Audio device latency may affect perceived synchronization. If audio initialization fails, visuals continue and Terminal explains the failure.

## What to watch for

- **Selection sort** scans the unsorted area for its smallest value, then puts it into place. The green region grows from the left.
- **Insertion sort** moves each new value left through its already ordered neighbors. This version uses adjacent swaps to keep every value visible. Ordered bars can still move later, so the green notes play in a final left-to-right sweep.
- **Quicksort** compares values to a pivot (the rightmost bar of the current section), partitions them, then works on the two sides. Each pivot turns green when placed. This simple pivot choice can be slow for already sorted inputs.
