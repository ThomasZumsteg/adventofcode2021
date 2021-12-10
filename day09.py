"""Solution to day 9 of Advent of Code"""

from get_input import get_input


def part1(mapping):
    return sum(h+1 for _, h in find_low_points(mapping))


def part2(mapping):
    low_points = find_low_points(mapping)
    basins = []
    for start in low_points:
        basin = set()
        boundary = set((start,))
        while boundary:
            new_boundary = set()
            for point, height in boundary:
                if height < 9:
                    basin.add(point)
                for adjacent in (point + d for d in (1j, -1j, 1, -1)):
                    adjacent_height = mapping.get(adjacent)
                    if adjacent_height is not None and\
                       adjacent_height > height and\
                       adjacent not in basin:
                        new_boundary.add((adjacent, adjacent_height))
            boundary = new_boundary
        basins.append(basin)
    check_result(mapping, basins)
    sizes = sorted((len(b) for b in basins), reverse=True)
    return sizes[0] * sizes[1] * sizes[2]


def find_low_points(mapping):
    for point, height in mapping.items():
        adjacent = (mapping.get(point + diff) for diff in (1j, -1j, 1, -1))
        if all(adj is None or adj > height for adj in adjacent):
            yield (point, height)


def check_result(lines, basins):
    all_points = set()
    for b, basin in enumerate(basins):
        all_points.update(basin)
        for compare in basins[b+1:]:
            assert basin.isdisjoint(compare)
    for nine in (set(lines.keys()) - all_points):
        assert lines[nine] == 9


def visualize(mapping, basin):
    max_rows = max(p.real for p in mapping.keys())
    max_cols = max(p.imag for p in mapping.keys())
    for r in range(int(max_rows)+1):
        for c in range(int(max_cols)+1):
            point = complex(r, c)
            if point in basin:
                print(mapping.get(point), end='')
            else:
                print(' ', end='')
        print()


def parse(lines):
    result = {}
    for r, line in enumerate(lines.splitlines()):
        for c, char in enumerate(line.strip()):
            result[complex(r, c)] = int(char)
    return result


TEST = """2199943210
3987894921
9856789892
8767896789
9899965678"""


if __name__ == "__main__":
    assert part1(parse(TEST)) == 15
    assert part2(parse(TEST)) == 1134
    # Low 561946
    LINES = parse(get_input(day=9, year=2021))
    print(f"Part 1: {part1(LINES)}")
    print(f"Part 2: {part2(LINES)}")
