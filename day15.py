"""Solution to day 15 of Advent of Code"""

from get_input import get_input
import itertools
import heapq


class CustomHeap(list):
    def __init__(self, items):
        super().__init__()
        self._mapping = {}
        for value, key in items:
            self.push(value, key)

    def push(self, value, point):
        rep = hash(point)
        self._mapping[rep] = point
        heapq.heappush(self, (value, rep))

    def pop(self):
        value, rep = heapq.heappop(self)
        return (value, self._mapping[rep])


def part1(mapping):
    queue = CustomHeap([(0, 0+0j)])
    lower = max(k.real for k in mapping.keys())
    right = max(k.imag for k in mapping.keys())
    end = complex(lower, right)
    seen = set()
    while queue:
        value, point = queue.pop()
        if point in seen:
            continue
        seen.add(point)
        if point == end:
            return value
        for step in (point+diff for diff in (1j, -1j, 1, -1)):
            if step not in mapping:
                continue
            queue.push(value+mapping[step], step)
    raise NotImplementedError


def part2(mapping):
    new_mapping = {}
    height = max(k.real for k in mapping.keys())+1
    width = max(k.imag for k in mapping.keys())+1
    for diff in itertools.product(range(5), range(5)):
        panel = complex(diff[0] * height, diff[1] * width)
        for key, value in mapping.items():
            new_value = (diff[0] + diff[1] + value - 1) % 9 + 1
            point = key + panel
            new_mapping[point] = new_value
    return part1(new_mapping)


def parse(lines):
    lines = iter(lines.splitlines())
    mapping = {}
    for r, row in enumerate(lines):
        for c, char in enumerate(row):
            mapping[complex(r, c)] = int(char)
    return mapping

TEST = """1163751742
1381373672
2136511328
3694931569
7463417111
1319128137
1359912421
3125421639
1293138521
2311944581"""

if __name__ == "__main__":
    LINES = parse(get_input(day=15, year=2021))
    test = parse(TEST)

    assert part1(test) == 40
    print(f"Part 1: {part1(LINES)}")

    assert part2(test) == 315
    print(f"Part 2: {part2(LINES)}")
