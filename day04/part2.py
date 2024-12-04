"""AOC template file."""

import argparse
from pathlib import Path

import pytest
import support

INPUT_TXT = Path(__file__).parent / 'input.txt'

# NOTE: paste test text here
INPUT_S = """\
.M.S......
..A..MSMS.
.M.S.MAA..
..A.ASMSM.
.M.S.M....
..........
S.S.S.S.S.
.A.A.A.A..
M.M.M.M.M.
..........
"""
EXPECTED = 9


def get_surround_coord_difs(x: int, y: int):
    yield (x - 1, y - 1), (x, y), (x + 1, y + 1)  # left diag
    yield (x - 1, y + 1), (x, y), (x + 1, y - 1)  # right diag


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
        if char != 'A':
            continue
        words = tuple(get_surround_words(grid, x, y))
        if not words:
            continue
        w1, w2 = words
        xmas_count += w1 in 'SAMMAS' and w2 in 'SAMMAS'

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
