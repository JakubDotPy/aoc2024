"""AOC template file."""

import argparse
import copy
from itertools import count
from pathlib import Path
from pydoc import resolve
from tokenize import group

import pytest
from mypy.memprofile import defaultdict

import support
from support import Direction4

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
EXPECTED = 6
wrong = [
    2096,
    2151,
]


def get_simple_path(pointer):
    main_path = set()

    while True:
        try:
            main_path.add(pointer.coords)
            while pointer.look() == '#':
                pointer.direction = pointer.direction.cw
            pointer.move()
        except support.OutOfBounds:
            return main_path


def run_loop(pointer, start_coords):
    main_path = set()
    pointer.place_at(*start_coords)
    pointer.direction = Direction4.UP
    while True:
        try:
            if pointer.state in main_path:
                return False
            main_path.add(pointer.state)
            while pointer.look() == '#':
                pointer.direction = pointer.direction.cw
            pointer.move()
        except support.OutOfBounds:
            return main_path



def compute(s: str) -> int:  # noqa: ARG001
    """Compute the solution for given problem."""
    grid = support.Grid.from_string(s)
    # add pointer
    start_coords = next(coord for coord, char in grid.items() if char == '^')
    pointer = support.Pointer(*start_coords, direction=support.Direction4.UP)
    grid.add_pointers(pointer)

    main_path = get_simple_path(pointer)
    main_path.remove(start_coords)

    total_loops = 0

    for coord in main_path:
        grid[coord] = '#'
        if not run_loop(pointer, start_coords):
            total_loops += 1
        grid[coord] = '.'

    return total_loops


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
