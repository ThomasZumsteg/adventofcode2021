"""Solution to day 4 of Advent of Code"""

from get_input import get_input


class Board:
    def __init__(self, board):
        self._map = dict()
        self._marked = set()
        for r, row in enumerate(board):
            for c, num in enumerate(row):
                pos = complex(r, c)
                assert num not in self._map
                self._map[num] = pos

    def mark(self, num):
        if num in self._map:
            self._marked.add(self._map[num])

    def is_winner(self):
        for n in range(5):
            if all(complex(n, c) in self._marked for c in range(5)):
                return True
            elif all(complex(r, n) in self._marked for r in range(5)):
                return True
        return False

    def unmarked(self):
        unmarked_nums = set()
        for num, pos in self._map.items():
            if pos not in self._marked:
                unmarked_nums.add(num)
        return unmarked_nums

    def __str__(self):
        reverse = {p: n for n, p in self._map.items()}
        result = ""
        for r in range(5):
            for c in range(5):
                pos = complex(r, c)
                num = reverse[pos]
                if pos in self._marked:
                    result += f"({num:2})"
                else:
                    result += f" {num:2} "
            result += '\n'
        return result


def part1(lines):
    leader, boards = lines
    boards = [Board(b) for b in boards]
    for num in leader:
        for b in boards:
            b.mark(num)
            if b.is_winner():
                return num * sum(b.unmarked())


def part2(lines):
    leader, boards = lines
    boards = [Board(b) for b in boards]
    for num in leader:
        next_iter = []
        for b in boards:
            b.mark(num)
            if not b.is_winner():
                next_iter.append(b)
        if len(boards) == 1:
            return num * sum(boards[0].unmarked())
        boards = next_iter


def parse(lines):
    lines = iter(lines.splitlines())
    leader = [int(n) for n in next(lines).split(',')]
    boards = []
    done = False
    assert next(lines).strip() == ''
    while not done:
        board = []
        while True:
            try:
                line = next(lines).strip()
            except StopIteration:
                done = True
                break
            if line == '':
                break
            board.append(tuple(int(n) for n in line.split()))
        boards.append(board)
    return leader, boards


TEST = """7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,3,26,1

22 13 17 11  0
 8  2 23  4 24
21  9 14 16  7
 6 10  3 18  5
 1 12 20 15 19

 3 15  0  2 22
 9 18 13 17  5
19  8  7 25 23
20 11 10 24  4
14 21 16 12  6

14 21 17 24  4
10 16 15  9 19
18  8 23 26 20
22 11 13  6  5
 2  0 12  3  7"""

if __name__ == "__main__":
    assert part1(parse(TEST)) == 4512
    assert part2(parse(TEST)) == 1924
    LINES = parse(get_input(day=4, year=2021))
    print(f"Part 1: {part1(LINES)}")
    print(f"Part 2: {part2(LINES)}")
