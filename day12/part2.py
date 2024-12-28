"""AOC template file."""

import argparse
from pathlib import Path

import pytest
from mypyc.ir.ops import Unreachable

import support

INPUT_TXT = Path(__file__).parent / 'input.txt'

# NOTE: paste test text here
INPUT_S = """\
AAAA
BBCD
BBCC
EEEC
"""
EXPECTED = 80
INPUT_S2 = """\
EEEEE
EXXXX
EEEEE
EXXXX
EEEEE
"""
EXPECTED2 = 236
INPUT_S3 = """\
OOOOO
OXOXO
OOOOO
OXOXO
OOOOO
"""
EXPECTED3 = 436
INPUT_S4 = """\
AAAAAA
AAABBA
AAABBA
ABBAAA
ABBAAA
AAAAAA
"""
EXPECTED4 = 368
INPUT_S5 = """\
RRRRIICCFF
RRRRIICCCF
VVRRRCCFFF
VVRCCCJFFF
VVVVCJJCFE
VVIVCCJJEE
VVIIICJJEE
MIIIIIJJEE
MIIISIJEEE
MMMISSJEEE
"""
EXPECTED5 = 1206


def check_corners(char, around) -> int:
    """check neighbors

    top row, left, right, bottom row
    0 1 2
    3 c 4
    5 6 7
    """
    corners = 0

    exterior_indices = [
        (1, 3),  # top-left L
        (1, 4),  # top-right L
        (3, 6),  # bottom-left L
        (6, 4),  # bottom-right L
    ]
    interior_indices = [
        (1, 3, 0),  # top-left L
        (1, 4, 2),  # top-right L
        (3, 6, 5),  # bottom-left L
        (4, 6, 7),  # bottom-right L
    ]

    # check for exterior corner
    corners += sum(
        around[i] != char and around[j] != char
        for i, j in exterior_indices
    )

    # check for interior corner
    corners += sum(
        around[i] == char
        and around[j] == char
        and around[k] != char
        for i, j, k in interior_indices
    )

    return corners


def flood_fill(coord, char, grid, visited):
    stack = [coord]
    area = 0
    corners = 0  # same as sides

    while stack:
        current = stack.pop()
        if current in visited or grid.get(current) != char:
            continue

        visited.add(current)
        area += 1

        chars_around = [grid.get(n, 'x') for n in support.adjacent_8(*current)]
        corners += check_corners(char, chars_around)

        for neighbor in support.adjacent_4(*current):
            if neighbor in grid and neighbor not in visited:
                stack.append(neighbor)

    return area, corners


def compute(s: str) -> int:  # noqa: ARG001
    """Compute the solution for given problem."""
    grid = support.parse_coords_char(s)
    visited = set()
    areas = []

    for coord, char in grid.items():
        if coord in visited:
            continue
        area, sides = flood_fill(coord, char, grid, visited)
        areas.append((char, area, sides))

    result = sum(
        area * sides
        for _, area, sides in areas
    )

    return result


# @pytest.mark.solved
@pytest.mark.parametrize(
    ('input_s', 'expected'),
    [
        (INPUT_S, EXPECTED),
        (INPUT_S2, EXPECTED2),
        (INPUT_S3, EXPECTED3),
        (INPUT_S4, EXPECTED4),
        (INPUT_S5, EXPECTED5),
    ],
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
