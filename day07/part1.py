"""AOC template file."""

import argparse
import re
from pathlib import Path

import pytest

import support

INPUT_TXT = Path(__file__).parent / 'input.txt'

# NOTE: paste test text here
INPUT_S = """\
190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20
"""
EXPECTED = 3749


def evaluate_eq_combinations(result, numbers):

    def dfs(index, current_value):
        """Perform DFS to explore all operator combinations.

        index: current position in right hand side
        current_value: accumulated result
        """

        # we overshot
        if current_value > result:
            return False

        # we reach the last number
        if index == len(numbers):
            return current_value == result

        # addition
        if dfs(index + 1, current_value + numbers[index]):
            return True

        # multiplication
        if dfs(index + 1, current_value * numbers[index]):
            return True

        return False

    # DFS from the first number
    return result if dfs(1, numbers[0]) else 0


def compute(s: str) -> int:  # noqa: ARG001
    """Compute the solution for given problem."""

    total_result = 0

    for line in s.splitlines():
        result, *numbers = map(int, re.findall(r'\d+', line))
        total_result += evaluate_eq_combinations(result, numbers)

    return total_result



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
