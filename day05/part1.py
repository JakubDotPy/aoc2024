"""AOC template file."""

import argparse
from itertools import chain
from itertools import tee
from pathlib import Path
from typing import Iterable
from typing import List
from typing import Tuple
from typing import Tuple
from typing import Tuple

import networkx as nx
import pytest

import support

INPUT_TXT = Path(__file__).parent / 'input.txt'

# NOTE: paste test text here
INPUT_S = """\
47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13

75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47
"""
EXPECTED = 143


def parse_data(s: str) -> tuple[list[tuple[int, ...]], list[list[int]]]:
    """Parse the input data into orders and updates."""
    orders_raw, updates_raw = s.split('\n\n')
    orders = [tuple(map(int, line.split('|'))) for line in orders_raw.splitlines()]
    updates = [list(map(int, line.split(','))) for line in updates_raw.splitlines()]
    return orders, updates

def is_valid_toposort(update: list[int], toposort: list[int]) -> bool:
    """Check if the update order matches the topological sort."""
    filtered = [x for x in toposort if x in update]
    return update == filtered

def compute(s: str) -> int:
    """Compute the solution for the given problem."""
    orders, updates = parse_data(s)
    total = 0

    for update in updates:
        relevant_orders = [
            (a, b)
            for a, b in orders
            if a in update and b in update
        ]
        graph = nx.DiGraph(relevant_orders)
        toposort = list(nx.topological_sort(graph))

        if is_valid_toposort(update, toposort):
            total += update[len(update) // 2]

    return total


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
