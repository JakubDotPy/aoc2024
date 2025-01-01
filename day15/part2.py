"""AOC template file."""
import sys
from functools import cache
from functools import cached_property

from colorama import Fore
from colorama import Style
from colorama import init

init(autoreset=True)

import argparse
import collections
import itertools
from dataclasses import dataclass
from dataclasses import field
from pathlib import Path

import pytest

import support
from support import Direction4
from support import parse_coords_set

INPUT_TXT = Path(__file__).parent / 'input.txt'

# NOTE: paste test text here
INPUT_S = """\
#######
#...#.#
#.....#
#..OO@#
#..O..#
#.....#
#######

<vv<<^^<<^^
"""
INPUT_S1 = """\
######
#....#
#..#.#
#....#
#.O..#
#.OO@#
#.O..#
#....#
######

<vv<<^^^
"""
EXPECTED1 = 1216
EXPECTED = 618
INPUT_S2 = """\
##########
#..O..O.O#
#......O.#
#.OO..O.O#
#..O@..O.#
#O#..O...#
#O..O..O.#
#.OO.O.OO#
#....O...#
##########

<vv>^<v^>v>^vv^v>v<>v^v<v<^vv<<<^><<><>>v<vvv<>^v^>^<<<><<v<<<v^vv^v>^
vvv<<^>^v^^><<>>><>^<<><^vv^^<>vvv<>><^^v>^>vv<>v<<<<v<^v>^<^^>>>^<v<v
><>vv>v^v^<>><>>>><^^>vv>v<^^^>>v^v^<^^>v^^>v^<^v>v<>>v^v^<v>v^^<^^vv<
<<v<^>>^^^^>>>v^<>vvv^><v<<<>^^^vv^<vvv>^>v<^^^^v<>^>vvvv><>>v^<<^^^^^
^><^><>>><>^^<<^^v>>><^<v>^<vv>>v>>>^v><>^v><<<<v>>v<v<v>vvv>^<><<>^><
^>><>^v<><^vvv<^^<><v<<<<<><^v<<<><<<^^<v<^^^><^>>^<v^><<<^>>^v<v^v<v^
>^>>^v>vv>^<<^v<>><<><<v<<v><>v<^vv<<<>^^v^>^^>>><<^v>>v^v><^^>>^<>vv^
<><^^>^^^<><vvvvv^v<v<<>^v<v>v<<^><<><<><<<^^<<<^<<>><<><^^^>^^<>^>v<>
^^>vv<^v^v<vv>^<><v<^v>^^^>>>^^vvv^>vvv<>>>^<^>>>>>^<<^v>^vvv<>^<><<v>
v^^>>><<^^<>>^v^<v^vv<>v^<<>^<^v^v><^<<<><<^<v><v<>vv>>v><v^<vv<>v^<<^
"""
EXPECTED2 = 9021

class Blocked(Exception):
    pass


@dataclass
class Wall:
    x: int
    y: int

    def _for_registration(self):
        return {(self.x, self.y): self}

    def __hash__(self):
        return hash((self.x, self.y))

    def __str__(self):
        return '#'

@dataclass
class Box:
    x1: int
    y1: int
    x2: int
    y2: int
    map: 'Map' = field(init=False, repr=False)

    def __post_init__(self):
        self.char_gen = itertools.cycle('[]')

    def _for_registration(self):
        return {
            (self.x1, self.y1): self,
            (self.x2, self.y2): self,
        }

    @property
    def gps(self):
        return self.x1 + 100 * self.y1

    def move(self, direction):
        self.x1, self.y1 = direction.apply(self.x1, self.y1)
        self.x2, self.y2 = direction.apply(self.x2, self.y2)

    def look(self, direction):
        L = direction.apply(self.x1, self.y1)
        R = direction.apply(self.x2, self.y2)

        if direction in (Direction4.UP, Direction4.DOWN):
            return list({self.map.entities.get(L), self.map.entities.get(R)})

        if direction == Direction4.LEFT:
            return [self.map.entities.get(L)]

        if direction == Direction4.RIGHT:
            return [self.map.entities.get(R)]

    def __hash__(self):
        return hash((self.x1, self.y1, self.x2, self.y2))

    def __str__(self):
        return f"{Fore.GREEN}{next(self.char_gen)}{Style.RESET_ALL}"

@dataclass
class Robot:
    x: int
    y: int
    map: 'Map' = field(init=False, repr=False)

    def _for_registration(self):
        return {(self.x, self.y): self}

    def move(self, direction):
        self.x, self.y = direction.apply(self.x, self.y)

    def look(self, direction):
        return [self.map.entities.get(direction.apply(self.x, self.y))]

    def __hash__(self):
        return hash((self.x, self.y))

    def __str__(self):
        return f"{Fore.RED}@{Style.RESET_ALL}"

class Map:

    def __init__(self, walls, boxes, robot):
        self.walls = walls
        self.boxes = boxes
        self.robot = robot

        for entity in itertools.chain(walls, boxes, [robot]):
            self._register(entity)

    def _register(self, entity):
        entity.map = self

    @property
    def entities(self):
        return collections.ChainMap(*[
                entity._for_registration()
                for entity in itertools.chain(self.walls, self.boxes, [self.robot])
        ])

    def move(self, entity, direction, to_move=None):
        if to_move is None:
            to_move = set()

        if any(isinstance(see, Wall) for see in entity.look(direction)):
            raise Blocked

        if all(see is None for see in entity.look(direction)):
            to_move.add(entity)
            return to_move

        if any(isinstance(see, Box) for see in entity.look(direction)):
            for box in [see for see in entity.look(direction) if isinstance(see, Box)]:
                self.move(box, direction, to_move)

            to_move.add(entity)
            return to_move

    @cached_property
    def _map_limits(self):
        x, y = zip(*self.entities.keys())
        return min(x), max(x), min(y), max(y)

    def __str__(self):
        x_min, x_max, y_min, y_max = self._map_limits
        rows = []
        for y in range(y_min, y_max + 1):
            row = [str(self.entities.get((x, y), ' ')) for x in range(x_min, x_max + 1)]
            rows.append(''.join(row))
        return '\n'.join(rows)

def compute(s: str) -> int:  # noqa: ARG001
    map_s, moves = s.split('\n\n')

    # make map twice as big
    map_s = map_s.translate({
        ord('#'): '##',
        ord('.'): '..',
        ord('O'): '[]',
        ord('@'): '@.',
    })

    # parse map
    walls = [Wall(x, y) for (x, y) in parse_coords_set(map_s, '#')]
    robot, = [Robot(x, y) for (x, y) in parse_coords_set(map_s, '@')]
    boxes = [
        Box(x, y, x + 1, y)
        for y, line in enumerate(map_s.splitlines())
        for x, c in enumerate(line)
        if c == '['
    ]

    map = Map(walls, boxes, robot)

    # parse directions
    directions = [Direction4.from_chr(c) for c in ''.join(moves.split())]

    for direction in directions:
        try:
            to_move = map.move(robot, direction)
        except Blocked:
            pass
        else:
            for entity in to_move:
                entity.move(direction)

    return sum(box.gps for box in map.boxes)

@pytest.mark.solved
@pytest.mark.parametrize(
    ('input_s', 'expected'),
    [
        (INPUT_S, EXPECTED),
        (INPUT_S1, EXPECTED1),
        (INPUT_S2, EXPECTED2),
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
