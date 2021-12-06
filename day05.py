"""Solution to day 5 of Advent of Code"""

from get_input import get_input, line_parser
from collections import defaultdict


def get_gridwise_unit(vector):
    """
    Create a girdwise unit vector that preserves sign, but reduces to a
    unit length
    Examples:
       10+3j ->  1+1j
        0-3j ->  0-1j
       -3+0j -> -1-0j
       -3+0j -> -1-0j
    """
    if vector.real != 0:
        vector = complex(vector.real / abs(vector.real), vector.imag)
    if vector.imag != 0:
        vector = complex(vector.real, vector.imag / abs(vector.imag))
    return vector


def part1(lines, skip=True):
    grid = defaultdict(int)
    for start, end in lines:
        step = get_gridwise_unit(end - start)
        if skip and step.real != 0 and step.imag != 0:
            # Skip diagonals
            continue
        pos = start
        while pos != end:
            grid[pos] += 1
            pos += step
        grid[end] += 1
    return sum(1 for v in grid.values() if v >= 2)


def part2(lines):
    return part1(lines, skip=False)


def parse(line):
    points = []
    for point in line.split(' -> '):
        x, y = point.split(',')
        points.append(complex(int(x), int(y)))
    return tuple(points)


if __name__ == "__main__":
    LINES = line_parser(get_input(day=5, year=2021), parse=parse)
    print(f"Part 1: {part1(LINES)}")
    print(f"Part 2: {part2(LINES)}")
