"""AOC template file."""

import argparse
import re
from pathlib import Path

import pytest
import support

INPUT_TXT = Path(__file__).parent / 'input.txt'

# NOTE: paste test text here
INPUT_S = """\
xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))
"""
EXPECTED = 48

MUL_RE = re.compile(r'mul\((\d+),(\d+)\)')
DO_RE = re.compile(r'do\(\)')
DONT_RE = re.compile(r'don\'t\(\)')


def compute(s: str) -> int:
    """Compute the solution for given problem."""

    do_starts = [m.start() for m in DO_RE.finditer(s)]
    dont_starts = [m.start() for m in DONT_RE.finditer(s)]

    muls = MUL_RE.finditer(s)
    mul_pos_to_result = {
        m.start(): int(m.group(1)) * int(m.group(2))
        for m in muls
    }  # fmt: skip

    result = 0
    enable = True

    for idx in range(len(s)):
        if idx in mul_pos_to_result:
            result += enable * mul_pos_to_result[idx]
        elif idx in do_starts:
            enable = True
        elif idx in dont_starts:
            enable = False

    return result


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
