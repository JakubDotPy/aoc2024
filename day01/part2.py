import argparse
import itertools
from functools import cache
from pathlib import Path

import pytest

import support

INPUT_TXT = Path(__file__).parent / 'input.txt'

# NOTE: paste test text here
INPUT_S = """\
3   4
4   3
2   5
1   3
3   9
3   3
"""
EXPECTED = 31

@cache
def get_similarity(num: int, right_list: tuple[int, ...]) -> int:
    return num * right_list.count(num)

def compute(s: str) -> int:
    # separate the two columns into left and right
    left, right = zip(*itertools.batched(map(int, s.split()), 2))
    return sum(
        get_similarity(num, right)
        for num in left
    )


@pytest.mark.solved
@pytest.mark.parametrize(
    ('input_s', 'expected'),
    [(INPUT_S, EXPECTED)],
)
def test(input_s: str, expected: int) -> None:
    """Test the compute function."""
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
