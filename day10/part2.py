"""AOC template file."""

import argparse
import itertools
from pathlib import Path
import matplotlib.pyplot as plt
import networkx as nx
import pytest
from networkx.algorithms.dag import descendants

import support
from support import OutOfBounds
from support import adjacent_4

INPUT_TXT = Path(__file__).parent / 'input.txt'

# NOTE: paste test text here
INPUT_S = """\
.....0.
..4321.
..5..2.
..6543.
..7..4.
..8765.
..9....
"""
EXPECTED = 3

INPUT_S2 = """\
..90..9
...1.98
...2..7
6543456
765.987
876....
987....
"""
EXPECTED2 = 13

INPUT_S3 = """\
012345
123456
234567
345678
4.6789
56789.
"""
EXPECTED3 = 227

INPUT_S4 = """\
89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732
"""
EXPECTED4 = 81


def create_graph(s: str):
    """Create a networkx graph from the given string."""

    G = nx.DiGraph()

    grid = support.Grid.from_string(s)
    # filter out dots
    grid = {pos: val for pos, val in grid.items() if val != '.'}

    for pos, val in grid.items():
        # add node
        if val == '.':
            continue
        G.add_node(pos, weight=int(val))
        # add edges
        for npos in adjacent_4(*pos):
            try:
                if int(grid[npos]) == int(grid[pos]) + 1:
                    G.add_edge(pos, npos)
            except KeyError:
                pass
    return G


def compute(s: str) -> int:  # noqa: ARG001
    """Compute the solution for given problem."""

    G = create_graph(s)
    # nx.draw_networkx(G)
    # plt.show()

    trailheads = [
        node
        for node in G.nodes(data=True)
        if node[1]['weight'] == 0
    ]
    targets = [
        node
        for node in G.nodes(data=True)
        if node[1]['weight'] == 9
    ]

    score = 0

    for head, tail in itertools.product(trailheads, targets):
        score += sum(1 for _ in nx.all_simple_paths(G, head[0], tail[0]))

    return score


@pytest.mark.solved
@pytest.mark.parametrize(
    ('input_s', 'expected'),
    [
        (INPUT_S, EXPECTED),
        (INPUT_S2, EXPECTED2),
        (INPUT_S3, EXPECTED3),
        (INPUT_S4, EXPECTED4),
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
