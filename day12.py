"""Solution to day 12 of Advent of Code"""

from get_input import get_input
from collections import defaultdict, deque


def part1(mapping):
    queue = deque()
    queue.append(('start',))
    result = 0
    while queue:
        nodes = queue.pop()
        if nodes[-1] == 'end':
            result += 1
            continue
        for step in mapping[nodes[-1]]:
            if step.islower() and step in nodes:
                continue
            queue.append(nodes + (step,))
    return result


def part2(mapping):
    queue = deque()
    queue.append((False, ('start',)))
    result = 0
    while queue:
        double, nodes = queue.pop()
        if nodes[-1] == 'end':
            result += 1
            continue
        for step in mapping[nodes[-1]]:
            if step.islower() and step in nodes:
                if not double:
                    queue.append((True, (nodes + (step,))))
            else:
                queue.append((double, nodes + (step,)))
    return result


def parse(lines):
    mapping = defaultdict(set)
    for line in lines.splitlines():
        start, end = line.split('-')
        mapping[start].add(end)
        if start != 'start' and end != 'end':
            mapping[end].add(start)
    return mapping


TEST = """start-A
start-b
A-c
A-b
b-d
A-end
b-end"""


if __name__ == "__main__":
    assert part1(parse(TEST)) == 10
    assert part2(parse(TEST)) == 36
    LINES = parse(get_input(day=12, year=2021))
    print(f"Part 1: {part1(LINES)}")
    print(f"Part 2: {part2(LINES)}")
