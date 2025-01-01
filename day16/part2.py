"""AOC template file."""

import argparse
import heapq
import itertools
from pathlib import Path

import networkx as nx
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
EXPECTED = 45
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
EXPECTED1 = 64


def make_graph(s):
    walls = set()
    for x, line in enumerate(s.splitlines()):
        for y, c in enumerate(line):
            pos = x, y
            if c == 'S':
                start = pos
            if c == 'E':
                end = pos
            if c == '#':
                walls.add(pos)

    G = nx.DiGraph()

    # create all combination of nodes
    for x, y, direction in itertools.product(range(x), range(y), Direction4):
        if (x, y) not in walls:
            G.add_node(((x, y), direction))

    for pos, direction in G.nodes:
        # add straight look edges
        look = direction.apply(*pos)
        if (look, direction) in G.nodes:
            G.add_edge((pos, direction), (look, direction), weight=1)
        for next_direction in Direction4:
            if next_direction == direction:
                continue
            # add the turns to self position
            G.add_edge((pos, direction), (pos, next_direction), weight=1_000)

    # create single end node
    for direction in Direction4:
        G.add_edge((end, direction), ('end', 'whatev...'), weight=0)


    return G, start, end


def compute(s: str) -> int:  # noqa: ARG001
    """Compute the solution for given problem."""
    G, start, end = make_graph(s)
    shortest_paths = nx.all_shortest_paths(
        G,
        (start, Direction4.RIGHT),
        ('end', 'whatev...'),
        weight="weight",
    )
    paths_set = set(
        pos
        for path in shortest_paths
        for pos, direction in path
    )
    return len(paths_set) - 1


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
