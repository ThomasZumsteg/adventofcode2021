"""Solution to day 1 of Advent of Code"""

from get_input import get_input, line_parser


def part1(lines, offset=1):
    return sum(1 for a, b in zip(lines, lines[offset:]) if a < b)


def part2(lines):
    return part1(lines, offset=3)


if __name__ == "__main__":
    LINES = line_parser(get_input(day=1, year=2021))
    print(f"Part 1: {part1(LINES)}")
    print(f"Part 2: {part2(LINES)}")
