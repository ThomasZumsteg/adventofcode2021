"""Solution to day 14 of Advent of Code"""

from get_input import get_input
from collections import defaultdict


def part1(lines, steps=10):
    start, translations = lines[:]
    pairs = defaultdict(int)
    for pair in zip(start, start[1:]):
        pairs[pair] += 1
    for _ in range(steps):
        next_pairs = defaultdict(int)
        for pair, value in pairs.items():
            middle = translations.get(pair)
            if middle is not None:
                next_pairs[(pair[0], middle)] += value
                next_pairs[(middle, pair[1])] += value
            else:
                next_pairs[pair] += value
        pairs = next_pairs
    counts = defaultdict(int)
    counts[start[0]] += 1
    counts[start[-1]] += 1
    for pair, value in pairs.items():
        counts[pair[0]] += value
        counts[pair[1]] += value
    return (max(counts.values()) - min(counts.values())) // 2


def part2(lines):
    return part1(lines, steps=40)


def parse(lines):
    lines = iter(lines.splitlines())
    start = next(lines)
    translations = {}
    assert next(lines) == ""
    for line in lines:
        pair, result = line.split(" -> ")
        assert tuple(pair) not in translations
        translations[tuple(pair)] = result
    return start, translations


TEST = """NNCB

CH -> B
HH -> N
CB -> H
NH -> C
HB -> C
HC -> B
HN -> C
NN -> C
BH -> H
NC -> B
NB -> B
BN -> B
BB -> N
BC -> B
CC -> N
CN -> C
"""

if __name__ == "__main__":
    LINES = parse(get_input(day=14, year=2021))

    assert part1(parse(TEST)) == 1588
    print(f"Part 1: {part1(LINES)}")

    assert part2(parse(TEST)) == 2188189693529
    print(f"Part 2: {part2(LINES)}")
