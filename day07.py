"""Solution to day 7 of Advent of Code"""

from get_input import get_input, line_parser


def part1(lines):
    positions = sorted(lines)
    mid = positions[len(positions) // 2]
    return sum(abs(mid - p) for p in positions)


def part2(lines):
    def find_fuel(position):
        total = 0
        for line in lines:
            diff = abs(line - position)
            total += diff * (diff + 1) // 2
        return total
    left = min(lines)
    right = max(lines)
    while left < right:
        left_third = left + max(1, (right - left) // 3)
        right_third = right - max(1, (right - left) // 3)
        left_result = find_fuel(left_third)
        right_result = find_fuel(right_third)
        if left_result > right_result:
            left = left_third
        elif left_result < right_result:
            right = right_third
        else:
            left, right = left_third, right_third
    return find_fuel(left)


TEST = "16,1,2,0,4,2,7,1,2,14"


if __name__ == "__main__":
    assert part1(line_parser(TEST, parse=int, seperator=',')) == 37
    assert part2(line_parser(TEST, parse=int, seperator=',')) == 168
    LINES = line_parser(get_input(day=7, year=2021), parse=int, seperator=',')
    print(f"Part 1: {part1(LINES)}")
    print(f"Part 2: {part2(LINES)}")
