"""AOC template file."""

import argparse
from pathlib import Path

import pytest

import support

INPUT_TXT = Path(__file__).parent / 'input.txt'

# NOTE: paste test text here
INPUT_S = """\
....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#...
"""
EXPECTED = 41


def compute(s: str) -> int:  # noqa: ARG001
    """Compute the solution for given problem."""
    grid = support.Grid.from_string(s)
    # add pointer
    coords = next(coord for coord, char in grid.items() if char == '^')
    pointer = support.Pointer(*coords, direction=support.Direction4.UP)
    grid.add_pointers(pointer)

    main_path = set()

    while True:
        try:
            main_path.add(pointer.coords)
            if pointer.look() == '#':
                pointer.direction = pointer.direction.cw
            pointer.move()
        except support.OutOfBounds:
            print(grid)
            return len(main_path)


@pytest.mark.solved
@pytest.mark.parametrize(
    ('input_s', 'expected'),
    [(INPUT_S, EXPECTED)],
)
def test(input_s: str, expected: int) -> None:
    """Test the compute function."""
    print()  # newline for better readability
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
