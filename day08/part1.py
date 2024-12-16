"""AOC template file."""

import argparse
import itertools
from pathlib import Path

import pytest
import support
from mypy.memprofile import defaultdict

INPUT_TXT = Path(__file__).parent / 'input.txt'

# NOTE: paste test text here
INPUT_S = """\
T....#....
...T......
.T....#...
.........#
..#.......
..........
...#......
..........
....#.....
..........
"""
EXPECTED = 9
INPUT_S2 = """
............
........0...
.....0......
.......0....
....0.......
......A.....
............
............
........A...
.........A..
............
............
"""
EXPECTED2 = 34


def compute(s: str) -> int:
    """Compute the solution for given problem."""
    antinodes = set()

    antennas = defaultdict(set)
    for y, line in enumerate(s.splitlines()):
        for x, c in enumerate(line):
            if c != '.':
                antennas[c].add((x, y))

    for freq, positions in antennas.items():
        for (x1, y1), (x2, y2) in itertools.combinations(positions, 2):
            x_diff, y_diff = x2 - x1, y2 - y1
            n1x, n1y = x1 - x_diff, y1 - y_diff
            n2x, n2y = x2 + x_diff, y2 + y_diff

            if (0 <= n1x <= x) and (0 <= n1y <= y):
                antinodes.add((n1x, n1y))
            if (0 <= n2x <= x) and (0 <= n2y <= y):
                antinodes.add((n2x, n2y))

    return len(antinodes)


@pytest.mark.solved
@pytest.mark.parametrize(
    ('input_s', 'expected'),
    [
        (INPUT_S, EXPECTED),
        (INPUT_S2, EXPECTED2),
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
