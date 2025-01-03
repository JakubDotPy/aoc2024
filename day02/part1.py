"""AOC template file."""

import argparse
import itertools
from pathlib import Path

import pytest

import support

INPUT_TXT = Path(__file__).parent / 'input.txt'

# NOTE: paste test text here
INPUT_S = """\
7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9
"""
EXPECTED = 2


def report_generator(input_s: str) -> tuple[int, ...]:
    """Parse the input string and generate the report."""
    yield from (tuple(map(int, line.split())) for line in input_s.splitlines())


def correct_diffs(a, b, c):
    """True, if a, b and c differ in at least one and at most three."""
    return abs(a - b) in (1, 2, 3) and abs(b - c) in (1, 2, 3)


def is_peak_or_valley(a, b, c):
    """True, if b is the peak of a, b, c."""
    return (a < b > c) or (a > b < c)


def tripple_wise(iterable):
    """Generate tripples from the iterable."""
    a, b, c = itertools.tee(iterable, 3)
    next(b, None)  # advance b by one
    next(c, None)  # advance c by two
    next(c, None)
    yield from zip(a, b, c)


def compute(s: str) -> int:  # noqa: ARG001
    """Compute the solution for given problem."""

    num_correct = 0
    for report in report_generator(s):
        safe = all(
            correct_diffs(a, b, c) and not is_peak_or_valley(a, b, c)
            for a, b, c in tripple_wise(report)
        )
        num_correct += safe

    return num_correct


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
