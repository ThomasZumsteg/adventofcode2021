"""Solution to day 13 of Advent of Code"""

from common import letters
from get_input import get_input
from itertools import islice


class Dots(set):
    def fold(self, axis, value):
        def transform(dot):
            if axis == 'y' and dot.imag > value:
                return complex(dot.real, 2 * value - dot.imag)
            elif axis == 'x' and dot.real > value:
                return complex(2 * value - dot.real, dot.imag)
            return dot
        return Dots(transform(dot) for dot in self)

    def display(self):
        left = int(min(p.real for p in self))
        right = int(max(p.real for p in self))
        upper = int(min(p.imag for p in self))
        lower = int(max(p.imag for p in self))
        lines = []
        for y in range(upper, lower+1):
            line = []
            lines.append(line)
            for x in range(left, right+1):
                char = '.'
                if complex(x, y) in self:
                    char = '#'
                line.append(char)
        return '\n'.join(''.join(line) for line in lines)


def part1(lines):
    folds, dots = lines[:]
    dots = dots.fold(*folds[0])
    return len(dots)


def part2(lines):
    folds, dots = lines[:]
    for fold in folds:
        dots = dots.fold(*fold)

    return ''.join(islice(letters(dots.display()), 8))


def parse(lines):
    lines = iter(lines.splitlines())
    points = Dots()
    for line in lines:
        if line == '':
            break
        x, y = line.split(',')
        points.add(complex(int(x), int(y)))
    folds = []
    for line in lines:
        assert line.startswith('fold along ')
        axis, value = line[len('fold along '):].split('=')
        folds.append((axis, int(value)))
    return (folds, points)


TEST = """6,10
0,14
9,10
0,3
10,4
4,11
6,0
6,12
4,1
0,13
10,12
3,4
3,0
8,4
1,10
2,14
8,10
9,0

fold along y=7
fold along x=5"""


if __name__ == "__main__":
    assert part1(parse(TEST)) == 17
    LINES = parse(get_input(day=13, year=2021))
    print(f"Part 1: {part1(LINES)}")
    print(f"Part 2: {part2(LINES)}")
