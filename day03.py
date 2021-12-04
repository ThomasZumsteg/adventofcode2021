"""Solution to day 3 of Advent of Code"""

from get_input import get_input, line_parser
from collections import Counter


def part1(lines):
    gamma, epsilon = 0, 0
    assert all(len(line) == len(lines[0]) for line in lines)
    for col in range(len(lines[0])):
        count = Counter(line[col] for line in lines)
        assert count.keys() == set(('1', '0'))
        gamma <<= 1
        epsilon <<= 1
        if count['1'] >= count['0']:
            epsilon |= 1
        else:
            gamma |= 1
    return gamma * epsilon


def part2(lines):
    gamma_list = lines.copy()
    epsilon_list = lines.copy()
    for reverse, line_list in ((False, gamma_list), (True, epsilon_list)):
        col = 0
        while len(line_list) > 1:
            count = Counter(line[col] for line in line_list)
            assert set(count.keys()).issubset(set(('1', '0')))
            select = 1 if count['1'] >= count['0'] else 0
            if reverse:
                select = int(not select)
            select = str(select)
            line_list[:] = [line for line in line_list if line[col] == select]
            col += 1
    assert len(gamma_list) == 1 and len(epsilon_list) == 1
    return int(''.join(gamma_list[0]), 2) * int(''.join(epsilon_list[0]), 2)


TEST = """00100
11110
10110
10111
10101
01111
00111
11100
10000
11001
00010
01010
"""

if __name__ == "__main__":
    assert part2(line_parser(TEST, parse=tuple)) == 230
    LINES = line_parser(get_input(day=3, year=2021), parse=tuple)
    print(f"Part 1: {part1(LINES)}")
    print(f"Part 2: {part2(LINES)}")
