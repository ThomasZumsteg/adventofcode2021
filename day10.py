"""Solution to day 10 of Advent of Code"""

from get_input import get_input, line_parser
from collections import defaultdict, deque


def part1(lines):
    counts = defaultdict(int)
    brackets = {
        '{': '}',
        '(': ')',
        '[': ']',
        '<': '>',
    }
    for line in lines:
        stack = deque()
        for char in line:
            if char in brackets:
                stack.append(char)
            elif char in brackets.values():
                last = stack.pop()
                if char != brackets[last]:
                    counts[char] += 1
                    break
            else:
                raise NotImplementedError
    return counts[')'] * 3 + counts[']'] * 57 +\
        counts['}'] * 1197 + counts['>'] * 25137


def part2(lines):
    counts = defaultdict(int)
    brackets = {
        '{': '}',
        '(': ')',
        '[': ']',
        '<': '>',
    }
    scores = []
    for line in lines:
        stack = deque()
        for char in line:
            if char in brackets:
                stack.append(char)
            elif char in brackets.values():
                last = stack.pop()
                if char != brackets[last]:
                    counts[char] += 1
                    break
            else:
                raise NotImplementedError
        else:
            score = 0
            values = {"(": 1, "[": 2, "{": 3, "<": 4}
            for char in reversed(stack):
                score *= 5
                score += values[char]
            scores.append(score)
    scores.sort()
    return scores[len(scores)//2]


if __name__ == "__main__":
    LINES = line_parser(get_input(day=10, year=2021), parse=tuple)
    print(f"Part 1: {part1(LINES)}")
    print(f"Part 2: {part2(LINES)}")
