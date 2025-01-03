"""AOC template file."""

import argparse
import re
from dataclasses import dataclass
from dataclasses import field
from pathlib import Path
from typing import Any

import pytest

import support

INPUT_TXT = Path(__file__).parent / 'input.txt'

# NOTE: paste test text here
INPUT_S = """\
Register A: 729
Register B: 0
Register C: 0

Program: 0,1,5,4,3,0
"""
EXPECTED = "4,6,3,5,6,3,5,2,1,0"

class InstructionSet:

    def __init__(self):
        self.computer = None
        self.opcode_map = {
            0: self.adv,
            1: self.bxl,
            2: self.bst,
            3: self.jnz,
            4: self.bxc,
            5: self.out,
            6: self.bdv,
            7: self.cdv,
        }

    def adv(self, arg):
        """The adv instruction (opcode 0) performs division.
        The numerator is the value in the A register.
        The denominator is found by raising 2 to the power of the instruction's combo operand.
        (So, an operand of 2 would divide A by 4 (2^2); an operand of 5 would divide A by 2^B.)
        The result of the division operation is truncated to an integer
        and then written to the A register.
        """
        result = self.computer.A // (2 ** self.computer.combo_operand_map[arg]())
        self.computer.A = result

    def bxl(self, arg):
        """The bxl instruction (opcode 1) calculates the bitwise XOR
        of register B and the instruction's literal operand,
        then stores the result in register B.
        """
        result = self.computer.B ^ arg
        self.computer.B = result

    def bst(self, arg):
        """The bst instruction (opcode 2) calculates the value of its combo operand modulo 8
        (thereby keeping only its lowest 3 bits), then writes that value to the B register.
        """
        result = self.computer.combo_operand_map[arg]() % 8
        self.computer.B = result

    def jnz(self, arg):
        """The jnz instruction (opcode 3) does nothing if the A register is 0.
        However, if the A register is not zero, it jumps by setting the instruction pointer
        to the value of its literal operand; if this instruction jumps,
        the instruction pointer is not increased by 2 after this instruction.
        """
        if self.computer.A == 0:
            return
        return arg

    def bxc(self, arg):
        """The bxc instruction (opcode 4) calculates the bitwise XOR of register B and register C,
        then stores the result in register B.
        (For legacy reasons, this instruction reads an operand but ignores it.)
        """
        result = self.computer.B ^ self.computer.C
        self.computer.B = result

    def out(self, arg):
        """The out instruction (opcode 5) calculates the value of its combo operand modulo 8,
        then outputs that value.
        (If a program outputs multiple values, they are separated by commas.)
        """
        result = self.computer.combo_operand_map[arg]() % 8
        self.computer.output.append(result)

    def bdv(self, arg):
        """The bdv instruction (opcode 6) works exactly like the adv instruction
        except that the result is stored in the B register.
        (The numerator is still read from the A register.)
        """
        result = self.computer.A // (2 ** self.computer.combo_operand_map[arg]())
        self.computer.B = result

    def cdv(self, arg):
        """The cdv instruction (opcode 7) works exactly like the adv instruction
        except that the result is stored in the C register.
        (The numerator is still read from the A register.)
        """
        result = self.computer.A // (2 ** self.computer.combo_operand_map[arg]())
        self.computer.C = result


@dataclass
class Computer:
    # registers
    A: int
    B: int
    C: int
    program: list[int]
    instruction_set: InstructionSet = field(init=False)

    output: list[int] = field(init=False, default_factory=list)

    def __post_init__(self):
        self.combo_operand_map: dict[int, Any] = {
            0: lambda: 0,
            1: lambda: 1,
            2: lambda: 2,
            3: lambda: 3,
            4: lambda: self.A,
            5: lambda: self.B,
            6: lambda: self.C,
            7: lambda: None
        }

    def _add_instruction_set(self, instruciont_set: InstructionSet):
        instruciont_set.computer = self
        self.instruction_set = instruciont_set


    @classmethod
    def from_string(cls, s):
        a, b, c, *program = map(int, re.findall(r'\d+', s))
        return cls(a, b, c, list(program))

    def run(self):
        pointer = 0

        while pointer < len(self.program) - 1:
            opcode, operand = self.program[pointer:pointer + 2]
            fn = self.instruction_set.opcode_map[opcode]
            fn_result = fn(operand)

            if fn_result is None:
                pointer += 2
            else:
                pointer = fn_result

        return self.output

    def formatted_output(self):
        return ','.join(map(str, self.output))


def compute(s: str) -> int:  # noqa: ARG001
    """Compute the solution for given problem."""

    computer = Computer.from_string(s)
    instruction_set = InstructionSet()
    computer._add_instruction_set(instruction_set)
    computer.run()

    return computer.formatted_output()

# @pytest.mark.solved
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
