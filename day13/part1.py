"""AOC template file."""

import argparse
import re
from functools import cached_property
from pathlib import Path

import numpy as np
import pytest
from numpy import ndarray

import support

INPUT_TXT = Path(__file__).parent / 'input.txt'

# NOTE: paste test text here
INPUT_S = """\
Button A: X+94, Y+34
Button B: X+22, Y+67
Prize: X=8400, Y=5400

Button A: X+26, Y+66
Button B: X+67, Y+21
Prize: X=12748, Y=12176

Button A: X+17, Y+86
Button B: X+84, Y+37
Prize: X=7870, Y=6450

Button A: X+69, Y+23
Button B: X+27, Y+71
Prize: X=18641, Y=10279
"""
EXPECTED = 480


class ClawMachine:

    A_PRESS = 3
    B_PRESS = 1

    def __init__(
        self, a_diff: tuple[int, int], b_diff: tuple[int, int], prize: tuple[int, int]
    ) -> None:
        self.a_diff = a_diff
        self.b_diff = b_diff
        self.prize = prize

        # helper variables
        self.a_dx, self.a_dy = a_diff
        self.b_dx, self.b_dy = b_diff
        self.prize_x, self.prize_y = prize

    @classmethod
    def from_input(cls, s: str) -> 'ClawMachine':
        a_dx, a_dy, b_dx, b_dy, prize_x, prize_y = map(
            int,
            re.findall(r'\d+', s),
        )
        return cls((a_dx, a_dy), (b_dx, b_dy), (prize_x, prize_y))

    @cached_property
    def solution(self) -> ndarray[int, int] | None:
        # solve the system of equations
        # a_dx * x + a_dy * y = prize_x
        # b_dx * x + b_dy * y = prize_y
        a = np.array(
            [
                [self.a_dx, self.b_dx],
                [self.a_dy, self.b_dy],
            ]
        )
        b = np.array(
            [
                self.prize_x,
                self.prize_y,
            ]
        )
        solution = np.linalg.solve(a, b)
        if np.allclose(solution, solution.round(), atol=1e-10):
            return solution
        return None

    @property
    def cost(self):
        if self.solution is None:
            return 0
        press_a, press_b = self.solution
        return self.A_PRESS * press_a + self.B_PRESS * press_b

    def __str__(self):
        return f'ClawMachine({self.a_diff}, {self.b_diff}, {self.prize})'

    __repr__ = __str__


def compute(s: str) -> int:  # noqa: ARG001
    """Compute the solution for given problem."""
    machines = [ClawMachine.from_input(block) for block in s.strip().split('\n\n')]
    return int(sum(machine.cost for machine in machines))


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
