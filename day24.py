"""Solution to day 24 of Advent of Code"""

from get_input import get_input, line_parser
from itertools import product, count
from collections import defaultdict
import sys


class ALU:
    def __init__(self, instructions):
        self.instructions = instructions
        self.digits = []
        self.reset()

    def run(self, digits):
        next(self.run_with_breakpoints(digits, set()), None)

    def run_with_breakpoints(self, digits, breakpoints):
        self.digits = digits.copy()
        while True:
            if self.lno in breakpoints:
                yield self
            if self.lno >= len(self.instructions):
                break
            func, *args = self.instructions[self.lno]
            self.lno += 1
            getattr(self, func)(*args)

    def reset(self, lno=0, registers=None):
        if registers is None:
            registers = {letter: 0 for letter in list("wxyz")}
        self.lno = lno
        self.registers = registers.copy()

    def inp(self, reg):
        self.registers[reg] = self.digits.pop(0)

    def mul(self, a, b):
        if not isinstance(b, int):
            b = self.registers[b]
        self.registers[a] *= b

    def add(self, a, b):
        if not isinstance(b, int):
            b = self.registers[b]
        self.registers[a] += b

    def mod(self, a, b):
        if not isinstance(b, int):
            b = self.registers[b]
        self.registers[a] %= b

    def div(self, a, b):
        if not isinstance(b, int):
            b = self.registers[b]
        assert b != 0
        self.registers[a] //= b

    def eql(self, a, b):
        if not isinstance(b, int):
            b = self.registers[b]
        self.registers[a] = 1 if self.registers[a] == b else 0


def test_alu():
    negator_prog = [
        ('inp', 'x'),
        ('mul', 'x', -1)
    ]
    negator = ALU(negator_prog)
    negator.run([1])
    assert negator.registers['x'] == -1
    negator.reset()
    negator.run([-10])
    assert negator.registers['x'] == 10

    three_times_prog = [
        ('inp', 'z'),
        ('inp', 'x'),
        ('mul', 'z', 3),
        ('eql', 'z', 'x'),
    ]
    three_times = ALU(three_times_prog)
    three_times.run([1, 3])
    assert three_times.registers['z'] == 1

    three_times = ALU(three_times_prog)
    three_times.run([2, 3])
    assert three_times.registers['z'] == 0

    binary_prog = [
        ('inp', 'w'),
        ('add', 'z', 'w'),
        ('mod', 'z', 2),
        ('div', 'w', 2),
        ('add', 'y', 'w'),
        ('mod', 'y', 2),
        ('div', 'w', 2),
        ('add', 'x', 'w'),
        ('mod', 'x', 2),
        ('div', 'w', 2),
        ('mod', 'w', 2)
    ]
    binary = ALU(binary_prog)
    binary.run([15])
    assert binary.registers == {'w': 1, 'x': 1, 'y': 1, 'z': 1}
    binary.reset()

    binary.run([10])
    assert binary.registers == {'w': 1, 'x': 0, 'y': 1, 'z': 0}
    binary.reset()

    binary.run([7])
    assert binary.registers == {'w': 0, 'x': 1, 'y': 1, 'z': 1}

    adder_prog = [
        ('inp', 'x'),
        ('inp', 'y'),
        ('add', 'x', 'y'),
        ('add', 'x', 1),
    ]
    adder = ALU(adder_prog)
    adder.run([3, 5])
    assert adder.registers['x'] == 9

def decompile(lines):
    # decompiled outline
    # 14 iterations of this
    # inp w
    # z /= (1|26) to push or pop the value
    # z += w+c

    # inp w
    # mul x 0
    # add x z
    # mod x 26
    # div z (1|26) # a
    # add x {b}
    # eql x w
    # eql x 0
    # mul y 0
    # add y 25
    # mul y x
    # add y 1
    # mul z y
    # mul y 0
    # add y w
    # add y {c}
    # mul y x
    # add z y
    inputs = []
    push_pop = []
    b_values = []
    c_values = []
    for lno, line in enumerate(lines):
        if line[0] == 'inp':
            assert line[1] == 'w'
            inputs.append(lno)
        elif lno == inputs[-1] + 4:
            assert line[0:2] == ('div', 'z') and line[2] in (1, 26)
            push_pop.append(line[2] == 1)  # 1 is push
        elif lno == inputs[-1] + 5:
            assert line[0:2] == ('add', 'x')
            b_values.append(line[2])
        elif lno == inputs[-1] + 15:
            assert line[0:2] == ('add', 'y')
            c_values.append(line[2])
    return tuple(zip(push_pop, b_values, c_values))


def part1(lines):
    values = decompile(lines)

    digit_stack = []
    digits = [9] * len(values)
    z_vals = [0] * (len(values) + 1)
    step = 0
    while step < len(values):
        push, b, c = values[step]
        if push:
            digit = digits[step]
            digit_stack.append((step, c))
        else:
            match_index, match_c = digit_stack.pop()
            # match_digit + match_c == digit - b
            digit = digits[match_index] + match_c + b
            if not 0 < digit <= 9:
                digits[match_index] -= 1
                step = match_index
                continue
        z = z_vals[step]
        x = 0 if (z % 26) + b == digit else 1
        z //= 1 if push else 26
        z *= 25*x+1
        z += (digit+c)*x
        z_vals[step+1] = z
        digits[step] = digit
        step += 1
    assert z_vals[-1] == 0
    monad = ALU(lines)
    breakpoints = [v[0] for v in values]
    breakpoints.append(len(lines))
    monad.run(digits)
    assert monad.registers['z'] == 0
    return ''.join(str(d) for d in digits)


def part2(lines):
    values = decompile(lines)

    digit_stack = []
    digits = [1] * len(values)
    z_vals = [0] * (len(values) + 1)
    step = 0
    while step < len(values):
        push, b, c = values[step]
        if push:
            digit = digits[step]
            digit_stack.append((step, c))
        else:
            match_index, match_c = digit_stack.pop()
            # match_digit + match_c == digit - b
            digit = digits[match_index] + match_c + b
            if not 0 < digit <= 9:
                digits[match_index] += 1
                step = match_index
                continue
        z = z_vals[step]
        x = 0 if (z % 26) + b == digit else 1
        z //= 1 if push else 26
        z *= 25*x+1
        z += (digit+c)*x
        z_vals[step+1] = z
        digits[step] = digit
        step += 1
    assert z_vals[-1] == 0
    monad = ALU(lines)
    breakpoints = [v[0] for v in values]
    breakpoints.append(len(lines))
    monad.run(digits)
    assert monad.registers['z'] == 0
    return ''.join(str(d) for d in digits)


def parse(line):
    func, *args = line.split(' ')
    processed = []
    for a in args:
        try:
            a = int(a)
        except ValueError:
            pass
        processed.append(a)
    return func, *processed


if __name__ == "__main__":
    LINES = line_parser(get_input(day=24, year=2021), parse=parse)

    test_alu()
    print(f"Part 1: {part1(LINES)}")
    print(f"Part 2: {part2(LINES)}")
