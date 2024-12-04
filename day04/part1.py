"""AOC template file."""

import argparse
from pathlib import Path

import pytest
import support

INPUT_TXT = Path(__file__).parent / 'input.txt'

# NOTE: paste test text here
INPUT_S = """\
....XXMAS.
.SAMXMS...
...S..A...
..A.A.MS.X
XMASAMX.MM
X.....XA.A
S.S.S.S.SS
.A.A.A.A.A
..M.M.M.MM
.X.X.XMASX
"""
EXPECTED = 18


def get_surround_coord_difs(x: int, y: int):
    yield (x, y), (x + 1, y), (x + 2, y), (x + 3, y)  # right
    yield (x, y), (x - 1, y), (x - 2, y), (x - 3, y)  # left
    yield (x, y), (x, y - 1), (x, y - 2), (x, y - 3)  # up
    yield (x, y), (x, y + 1), (x, y + 2), (x, y + 3)  # down
    # bottom right
    yield (x, y), (x + 1, y + 1), (x + 2, y + 2), (x + 3, y + 3)
    # bottom left
    yield (x, y), (x - 1, y + 1), (x - 2, y + 2), (x - 3, y + 3)
    # top right
    yield (x, y), (x + 1, y - 1), (x + 2, y - 2), (x + 3, y - 3)
    # top left
    yield (x, y), (x - 1, y - 1), (x - 2, y - 2), (x - 3, y - 3)


def apply_coord_diff(x, y, diff):
    return [(x + dx, y + dy) for (dx, dy) in diff]


def get_word(grid, coords):
    return ''.join(grid[coord] for coord in coords)


def get_surround_words(grid, x, y):
    for coords in get_surround_coord_difs(x, y):
        if all(coord in grid for coord in coords):
            yield get_word(grid, coords)


def compute(s: str) -> int:
    """Compute the solution for given problem."""
    grid = support.parse_coords_char(s)
    xmas_count = 0
    for (x, y), char in grid.items():
        if char != 'X':
            continue
        xmas_count += sum(word == 'XMAS' for word in get_surround_words(grid, x, y))

    return xmas_count


@pytest.mark.solved
@pytest.mark.parametrize(
    ('input_s', 'expected'),
    [(INPUT_S, EXPECTED)],
)
def test(input_s: str, expected: int) -> None:
    """Test the compute function."""
    assert compute(input_s) == expected


def main() -> int:
    """Execute the main routine.

    Parse input data, compute the solution, and print the result.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('data_file', nargs='?', default=INPUT_TXT)
    args = parser.parse_args()

    with Path.open(args.data_file) as f, support.timing():
        print(compute(f.read()))

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
