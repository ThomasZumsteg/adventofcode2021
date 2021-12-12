"""Solution to day 11 of Advent of Code"""

from get_input import get_input
from collections import deque


def flash_octopi(mapping):
    mapping = mapping.copy()
    directions = (1, -1, 1j, -1j, 1+1j, -1+1j, 1-1j, -1-1j)
    while True:
        flashed = set()
        queue = deque(mapping.keys())
        while queue:
            position = queue.pop()
            if position not in mapping:
                continue
            mapping[position] += 1
            if mapping[position] > 9 and position not in flashed:
                flashed.add(position)
                queue.extend(position + d for d in directions)
        for position in flashed:
            mapping[position] = 0
        yield flashed


def part1(mapping, steps=100):
    total = 0
    for step, flashed in enumerate(flash_octopi(mapping)):
        if step == steps:
            return total
        total += len(flashed)


def part2(mapping):
    ALL = set(mapping.keys())
    for step, flashed in enumerate(flash_octopi(mapping), start=1):
        if flashed == ALL:
            return step


def display(mapping):
    text = []
    last_row = 0
    for p in sorted(mapping.keys(), key=lambda p: (p.real, p.imag)):
        if p.real != last_row:
            text.append('\n')
        last_row = p.real
        text.append(str(mapping[p]))
    print(''.join(text))


def parse(rows):
    mapping = {}
    for r, row in enumerate(rows.splitlines()):
        for c, char in enumerate(row.strip()):
            mapping[complex(r, c)] = int(char)
    return mapping


TEST = """5483143223
2745854711
5264556173
6141336146
6357385478
4167524645
2176841721
6882881134
4846848554
5283751526"""


if __name__ == "__main__":
    assert part1(parse(TEST), steps=10) == 204
    assert part2(parse(TEST)) == 195
    LINES = parse(get_input(day=11, year=2021))
    print(f"Part 1: {part1(LINES)}")
    print(f"Part 2: {part2(LINES)}")
