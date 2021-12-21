"""Solution to day 20 of Advent of Code"""

from get_input import get_input


def part1(header_and_mapping, iterations=2):
    header, mapping = header_and_mapping[:]
    assert not (header[0] == '#' and header[-1] == '#')
    toggle = header[0] == '#' and header[-1] == '.'
    image = {p for p, c in mapping.items() if c == '#'}
    # Order matters
    diffs = ((-1-1j), (-1+0j), (-1+1j), -1j, 0j, 1j, (1-1j), (1+0j), (1+1j))
    for r in range(iterations):
        to_update = set()
        record_light = not toggle or r % 2 == 0
        for p in image:
            to_update.update(p + d for d in diffs)
        new_image = set()
        if record_light:
            def get_bit(point):
                return '1' if point in image else '0'
        else:
            def get_bit(point):
                return '0' if point in image else '1'
        for point in to_update:
            total = ''.join(get_bit(point+d) for d in diffs)
            binary = int(total, 2)
            if toggle:
                if record_light and header[binary] == '.':
                    new_image.add(point)
                elif not record_light and header[binary] == '#':
                    new_image.add(point)
            else:
                if header[binary] == '#':
                    new_image.add(point)
        image = new_image
    return len(image)


def part2(lines):
    return part1(lines, iterations=50)


def parse(lines):
    lines = iter(lines.splitlines())
    header = tuple(next(lines))
    assert len(header) == 512
    assert '' == next(lines)
    mapping = {}
    for r, row in enumerate(lines):
        for c, char in enumerate(row):
            if char == '#':
                mapping[complex(r, c)] = char
    return header, mapping


test = """..#.#..#####.#.#.#.###.##.....###.##.#..###.####..#####..#....#..#..##..###..######.###...####..#..#####..##..#.#####...##.#.#..#.##..#.#......#.###.######.###.####...#.##.##..#..#..#####.....#.#....###..#.##......#.....#..#..#..##..#...##.######.####.####.#.#...#.......#..#.#.#...####.##.#......#..#...##.#.##..#...##.#.##..###.#......#.#.......#.#.#.####.###.##...#.....####.#..#..#.##.#....##..#.####....##...##..#...#......#.#.......#.......##..####..#...#.#.#...##..#.#..###..#####........#..####......#..#

#..#.
#....
##..#
..#..
..###"""


if __name__ == "__main__":
    lines = parse(get_input(day=20, year=2021))
    test = parse(test)

    assert part1(test) == 35
    # 5167 is to low, 5431 is to hight
    print(f"part 1: {part1(lines)}")

    assert part2(test) == 3351
    print(f"part 2: {part2(lines)}")
