"""AOC template file."""

import argparse
import heapq
from pathlib import Path

import pytest

import support
from support import Direction4

INPUT_TXT = Path(__file__).parent / 'input.txt'

# NOTE: paste test text here
INPUT_S = """\
###############
#.......#....E#
#.#.###.#.###.#
#.....#.#...#.#
#.###.#####.#.#
#.#.#.......#.#
#.#.#####.###.#
#...........#.#
###.#.#####.#.#
#...#.....#.#.#
#.#.#.###.#.#.#
#.....#...#.#.#
#.###.#.#.#.#.#
#S..#.....#...#
###############
"""
EXPECTED = 7036
INPUT_S1 = """\
#################
#...#...#...#..E#
#.#.#.#.#.#.#.#.#
#.#.#.#...#...#.#
#.#.#.#.###.#.#.#
#...#.#.#.....#.#
#.#.#.#.#.#####.#
#.#...#.#.#.....#
#.#.#####.#.###.#
#.#.#.......#...#
#.#.###.#####.###
#.#.#...#.....#.#
#.#.#.#####.###.#
#.#.#.........#.#
#.#.#.#########.#
#S#.............#
#################
"""
EXPECTED1 = 11048


def compute(s: str) -> int:  # noqa: ARG001
    """Compute the solution for given problem."""

    start = end = None
    walls = set()

    for y, line in enumerate(s.splitlines()):
        for x, c in enumerate(line):
            pos = (x, y)
            if c == '#':
                walls.add(pos)
            elif c == 'S':
                start = pos
            elif c == 'E':
                end = pos

    pq = [(0, start, Direction4.RIGHT)]
    visited = set()

    while pq:
        cost, pos, direction = heapq.heappop(pq)

        if pos == end:
            return cost

        if (pos, direction) in visited:
            continue

        visited.add((pos, direction))

        look_forward = direction.apply(*pos)
        if look_forward not in walls:
            heapq.heappush(pq, (cost + 1, look_forward, direction))
        heapq.heappush(pq, (cost + 1000, pos, direction.cw))
        heapq.heappush(pq, (cost + 1000, pos, direction.ccw))

    raise RuntimeError('unreachable')


@pytest.mark.solved
@pytest.mark.parametrize(
    ('input_s', 'expected'),
    [
        (INPUT_S, EXPECTED),
        (INPUT_S1, EXPECTED1),
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
