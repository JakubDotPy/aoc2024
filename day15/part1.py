"""AOC template file."""

import argparse
import itertools
from dataclasses import dataclass
from pathlib import Path

import pytest
from six import moves

import support
from support import Direction4
from support import Pointer

INPUT_TXT = Path(__file__).parent / 'input.txt'

# NOTE: paste test text here
INPUT_S = """\
########
#..O.O.#
##@.O..#
#...O..#
#.#.O..#
#...O..#
#......#
########

<^^>>>vv<v>>v<<
"""
EXPECTED = 2028
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
EXPECTED2 = 10092

class Blocked(Exception):
    pass

class Box(Pointer):
    pass

class Robot(Pointer):
    pass


def move_in_grid(pointer: Pointer, direction, grid, boxes, walls):
    # pointer faces wall
    if pointer.look(direction) == '#':
        raise Blocked

    pointer.direction = direction

    # pointer faces empty space
    if pointer.look(direction) == '.':
        grid.move(pointer.coords, direction)
        pointer.move()
        return

    # pointer faces a box
    if pointer.look(direction) == 'O':
        # recursive call
        try:  # to move the box
            box_there = next(
                box
                for box in boxes
                if box.coords == direction.apply(*pointer.coords)
            )
            move_in_grid(box_there, direction, grid, boxes, walls)
        except Blocked:
            raise
        else:
            # move self behind the box
            move_in_grid(pointer, direction, grid, boxes, walls)


def compute(s: str) -> int:  # noqa: ARG001
    map, moves = s.split('\n\n')

    # parse map

    grid = support.Grid.from_string(map)
    boxes = set()
    walls = set()
    for y, line in enumerate(map.splitlines()):
        for x, c in enumerate(line):
            if c == '#':
                walls.add((x, y))
            elif c == 'O':
                boxes.add(Box(x, y))
            elif c == '@':
                robot = Robot(x, y)

    grid.add_pointers(*boxes)
    grid.add_pointers(robot)

    # parse directions
    directions = [
        Direction4.from_chr(c)
        for c in itertools.chain.from_iterable(moves.splitlines())
    ]

    for direction in directions:
        try:
            move_in_grid(robot, direction, grid, boxes, walls)
        except Blocked:
            pass

    return sum(box.x + box.y * 100 for box in boxes)


@pytest.mark.solved
@pytest.mark.parametrize(
    ('input_s', 'expected'),
    [
        (INPUT_S, EXPECTED),
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
