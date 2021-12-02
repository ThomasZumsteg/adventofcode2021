"""Solution to day 2 of Advent of Code"""

from get_input import get_input, line_parser


def part1(lines):
    position = 0+0j
    diffs = {
        'up': 0-1j,
        'down': 0+1j,
        'forward': 1+0j,
    }
    for (command, size) in lines:
        position += diffs[command] * size
    return int(position.real) * int(position.imag)


def part2(lines):
    position = 0+0j
    aim = 0
    for (command, size) in lines:
        if command == "up":
            aim -= size
        elif command == 'down':
            aim += size
        elif command == 'forward':
            position += complex(size, aim * size)
        else:
            raise NotImplementedError
    return int(position.real) * int(position.imag)


def parse(line):
    command, depth = line.split(' ')
    return (command, int(depth))


if __name__ == "__main__":
    LINES = line_parser(get_input(day=2, year=2021), parse=parse)
    print(f"Part 1: {part1(LINES)}")
    print(f"Part 2: {part2(LINES)}")
