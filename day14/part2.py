"""AOC template file."""

import argparse
import collections
import itertools
import re
from pathlib import Path
from turtledemo.forest import start

import pytest

import support

INPUT_TXT = Path(__file__).parent / 'input.txt'

# NOTE: paste test text here
INPUT_S = """\
p=0,4 v=3,-3
p=6,3 v=-1,-3
p=10,3 v=-1,2
p=2,0 v=2,-1
p=0,0 v=1,3
p=3,0 v=-2,-2
p=7,6 v=-1,-3
p=3,0 v=-1,-2
p=9,3 v=2,3
p=7,3 v=-1,2
p=2,4 v=2,-3
p=9,5 v=-3,-3
"""
EXPECTED = 12


class Robot:

    def __init__(self, pos: tuple[int, int], vel: tuple[int, int]) -> None:
        self.pos = pos
        self.vel = vel

        self.x, self.y = pos
        self.vx, self.vy = vel

    @classmethod
    def from_line(cls, line: str) -> 'Robot':
        x, y, vx, vy = map(int, re.findall(r'-?\d+', line))
        return cls((x, y), (vx, vy))

    def move(self, world_bounds: tuple[int, int], t: int = 1) -> None:
        wx, wy = world_bounds
        self.x = (self.x + t * self.vx) % wx
        self.y = (self.y + t * self.vy) % wy

    def __str__(self):
        return f'Robot(pos=({self.x}, {self.y}), vel=({self.vx}, {self.vy}))'

    __repr__ = __str__

def compute(s: str) -> int:  # noqa: ARG001
    """Compute the solution for given problem."""

    world_size = 101, 103
    robots = [Robot.from_line(line) for line in s.splitlines()]

    for step in itertools.count():
        # assume the Christmas tree is symmetric
        min_tree_width = 20  # another assumption

        positions = set((robot.x, robot.y) for robot in robots)

        # most of them should be centered
        for midpoint in range(min_tree_width // 2, world_size[0] - min_tree_width // 2):
            centered_count = 0
            for curr_x, curr_y in positions:
                new_x = midpoint - (curr_x - midpoint)
                has_opposite = (new_x, curr_y) in positions
                centered_count += has_opposite

            if centered_count > len(robots) // 2:
                support.print_coords_hash(positions)
                return step

        for robot in robots:
            robot.move(world_size)

    return step


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
