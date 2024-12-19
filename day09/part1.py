"""AOC template file."""

import argparse
import itertools
from dataclasses import dataclass
from dataclasses import field
from email.policy import default
from itertools import filterfalse
from mimetypes import inited
from pathlib import Path
from typing import Optional

import pytest

import support

INPUT_TXT = Path(__file__).parent / 'input.txt'

# NOTE: paste test text here
INPUT_S = """\
2333133121414131402
"""
EXPECTED = 1928


def skip_ids_gen():
    """Generate numbers and Nones repeatedly"""
    counter = itertools.count()
    while True:
        yield next(counter)
        yield None


@dataclass
class Partition:
    """Hold info about a disc space."""
    file_id: int | None
    next: Optional['Partition'] = None
    prev: Optional['Partition'] = None

    def __bool__(self):
        return self.file_id is not None

    def __str__(self):
        if self.file_id is None:
            return '.'
        if len(str(self.file_id)) == 1:
            return f'{self.file_id}'
        return f'[{self.file_id}]'

    def __repr__(self):
        return f'Partition({self.file_id})'


class LinkedList:
    """A doubly linked list."""
    def __init__(self):
        self.head = None
        self.tail = None

    def append(self, file_id):
        """Append a new node to the list."""
        if self.head is None:
            self.head = self.tail = Partition(
                file_id=file_id,
                next=None,
                prev=None,
            )
        else:
            self.tail.next = Partition(
                file_id=file_id,
                next=None,
                prev=self.tail,
            )
            self.tail = self.tail.next

    def __iter__(self):
        """Iterate over the list."""
        node = self.head
        while node is not None:
            yield node
            node = node.next

    def __reversed__(self):
        """Iterate over the list in reverse order."""
        node = self.tail
        while node is not None:
            yield node
            node = node.prev

    def __str__(self):
        """Return a string representation of the list."""
        return ''.join(str(node) for node in self)


def compute(s: str) -> int:  # noqa: ARG001
    """Compute the solution for given problem."""

    sizes = map(int, s.strip())
    id_gen = skip_ids_gen()

    partitions = LinkedList()
    for file_id, size in zip(id_gen, sizes):
        for _ in range(size):
            partitions.append(file_id)

    # consume partitions from the end
    # fill in the empty spaces from the beginning

    empties = filterfalse(bool, partitions)
    fulls = filter(bool, reversed(partitions))
    for empty, full in zip(empties, fulls):
        if empty.prev == full:
            # the two partitions are adjacent
            break
        empty.file_id = full.file_id
        full.file_id = None

    return sum(
        pos * partition.file_id
        for pos, partition in enumerate(filter(bool, partitions))
    )


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
