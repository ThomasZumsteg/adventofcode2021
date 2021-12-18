"""Solution to day 17 of Advent of Code"""

from get_input import get_input
import re
from itertools import product


def make_target_func(target):
    upper_left, lower_right = target[:]

    def wrapped(velocity, position=0+0j):
        while position.imag >= lower_right.imag:
            if (upper_left.real <= position.real <= lower_right.real) and \
               (upper_left.imag >= position.imag >= lower_right.imag):
                return True
            position += velocity
            vel_x = velocity.real
            if vel_x > 0:
                vel_x -= 1
            elif vel_x < 0:
                vel_x += 1
            velocity = complex(vel_x, velocity.imag - 1)
        return False
    return wrapped


def part1(target):
    assert target[1].imag < 0
    diff = abs(target[1].imag) - 1
    return int(diff * (diff+1) / 2)


def part2(target):
    _, lower_right = target[:]

    assert lower_right.imag < 0
    big_y = abs(lower_right.imag) - 1
    y_range = range(int(lower_right.imag), int(big_y)+1)

    assert lower_right.real > 0
    x_range = range(1, int(lower_right.real)+1)

    target_func = make_target_func(target)
    hits_target = set()
    for x_vel, y_vel in product(x_range, y_range):
        vel = complex(x_vel, y_vel)
        if target_func(vel):
            hits_target.add(vel)
    return len(hits_target)


def parse(line):
    m = re.match(r"target area: x=(-?\d+)..(-?\d+), y=(-?\d+)..(-?\d+)", line)
    left, right = int(m.group(1)), int(m.group(2))
    assert left < right
    lower, upper = int(m.group(3)), int(m.group(4))
    assert upper > lower
    return (
        complex(left, upper),
        complex(right, lower)
    )


TEST = "target area: x=20..30, y=-10..-5"


if __name__ == "__main__":
    LINES = parse(get_input(day=17, year=2021))
    assert part1(parse(TEST)) == 45
    print(f"Part 1: {part1(LINES)}")

    assert part2(parse(TEST)) == 112
    print(f"Part 2: {part2(LINES)}")
