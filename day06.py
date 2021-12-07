"""Solution to day 6 of Advent of Code"""

from get_input import get_input
from collections import defaultdict, Counter


def part1(lines, days=80):
    fishes = Counter(lines)
    for _ in range(days):
        next_fishes = defaultdict(int)
        for fish, count in fishes.items():
            if fish == 0:
                fish = 7
                next_fishes[8] = count
            fish -= 1
            next_fishes[fish] += count
        fishes = next_fishes
    return sum(fishes.values())


def part2(lines):
    return part1(lines, days=256)


def parse(line):
    return tuple(int(n) for n in line.split(','))


TEST = '3,4,3,1,2'

if __name__ == "__main__":
    assert part1(parse(TEST), days=18) == 26, part1(parse(TEST), days=18)
    LINES = parse(get_input(day=6, year=2021))
    print(f"Part 1: {part1(LINES)}")
    print(f"Part 2: {part2(LINES)}")
