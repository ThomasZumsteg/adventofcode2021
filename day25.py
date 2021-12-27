"""Solution to day 25 of Advent of Code"""

from get_input import get_input


def part1(lines):
    cucumbers, seafloor = lines[:]
    last = {1: set(), 1j: set()}
    step = 0
    while last != cucumbers:
        last = cucumbers
        cucumbers = {1: set(), 1j: set()}
        for heard, cross_check in ((1j, last[1]), (1, cucumbers[1j])):
            for position in last[heard]:
                update = position + heard
                # print(f"Moving {update} = {position} + {heard}")
                if update not in seafloor:
                    update = complex(0, position.imag) if heard == 1\
                        else complex(position.real, 0)
                blocked = update in last[heard]
                blocked_by_cross = update in cross_check
                if not blocked_by_cross and not blocked:
                    cucumbers[heard].add(update)
                else:
                    cucumbers[heard].add(position)
        step += 1
        # print(step)
        # print(show_seafloor(cucumbers, seafloor), end='\n\n')
    return step


def show_seafloor(cucumbers, seafloor):
    max_row = max(p.real for p in seafloor)
    min_row = min(p.real for p in seafloor)
    max_col = max(p.imag for p in seafloor)
    min_col = min(p.imag for p in seafloor)
    result = []
    for r in range(int(min_row), int(max_row+1)):
        result.append([])
        for c in range(int(min_col), int(max_col+1)):
            point = complex(r, c)
            char = '.'
            if point in cucumbers[1]:
                char = 'v'
            elif point in cucumbers[1j]:
                char = '>'
            result[-1].append(char)
    return ''.join(''.join(row) + '\n' for row in result)


def parse(lines):
    cucumbers = {1: set(), 1j: set()}
    seafloor = set()
    for r, row in enumerate(lines.splitlines()):
        for c, char in enumerate(row):
            point = complex(r, c)
            seafloor.add(point)
            if char == 'v':
                cucumbers[1].add(point)
            elif char == '>':
                cucumbers[1j].add(point)
            else:
                assert char == '.'
    return cucumbers, seafloor


TEST = """v...>>.vv>
.vv>>.vv..
>>.>v>...v
>>v>>.>.v.
v>v.vv.v..
>.>>..v...
.vv..>.>v.
v.v..>>v.v
....v..v.>"""


if __name__ == "__main__":
    LINES = parse(get_input(day=25, year=2021))
    assert part1(parse(TEST)) == 58
    print(f"Part 1: {part1(LINES)}")
