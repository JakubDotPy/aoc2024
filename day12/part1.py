"""AOC template file."""

import argparse
from pathlib import Path

import pytest

import support

INPUT_TXT = Path(__file__).parent / 'input.txt'

# NOTE: paste test text here
INPUT_S = """\
AAAA
BBCD
BBCC
EEEC
"""
EXPECTED = 140
INPUT_S2 = """\
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
EXPECTED2 = 1930
INPUT_S3 = """\
OOOOO
OXOXO
OOOOO
OXOXO
OOOOO
"""
EXPECTED3 = 772


def flood_fill(coord, char, grid, visited):
    stack = [coord]
    area = 0
    perimeter = 0

    while stack:
        current = stack.pop()
        if current in visited or grid.get(current) != char:
            continue

        visited.add(current)
        area += 1

        # check neighbors and count boundary transitions
        for neighbor in support.adjacent_4(*current):
            if neighbor not in grid or grid.get(neighbor) != char:
                # if neighbor is out of bounds or a different character, it's a boundary
                perimeter += 1
            elif neighbor not in visited:
                stack.append(neighbor)

    return area, perimeter


def compute(s: str) -> int:  # noqa: ARG001
    """Compute the solution for given problem."""
    grid = support.parse_coords_char(s)
    visited = set()
    areas = []

    for coord, char in grid.items():
        if coord in visited:
            continue
        area, perimeter = flood_fill(coord, char, grid, visited)
        areas.append((char, area, perimeter))

    result = sum(
        area * perimeter
        for _, area, perimeter in areas
    )

    return result


# @pytest.mark.solved
@pytest.mark.parametrize(
    ('input_s', 'expected'),
    [
        (INPUT_S, EXPECTED),
        (INPUT_S2, EXPECTED2),
        (INPUT_S3, EXPECTED3),
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
