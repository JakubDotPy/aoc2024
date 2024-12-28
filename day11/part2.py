"""AOC template file."""

import argparse
import collections
from dataclasses import dataclass
from pathlib import Path
from shlex import split
from typing import Optional

import pytest

import support

INPUT_TXT = Path(__file__).parent / 'input.txt'

# NOTE: paste test text here
INPUT_S = """\
125 17
"""
EXPECTED = 55312


def compute(s: str) -> int:  # noqa: ARG001
    """Compute the solution for given problem."""

    stones = collections.Counter(map(int, s.split()))

    for blink in range(75):
        new_stones = collections.Counter()
        for num, count in stones.items():

            if num == 0:
                new_stones[1] += count

            elif (l := len(str(num))) % 2 == 0:
                split = l // 2
                left = int(str(num)[:split])
                right = int(str(num)[split:])
                new_stones[left] += count
                new_stones[right] += count

            else:
                new_stones[num * 2024] += count

        stones = new_stones

    return sum(stones.values())


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
