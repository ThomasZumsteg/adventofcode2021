"""Solution to day 8 of Advent of Code"""

from get_input import get_input, line_parser
from collections import defaultdict


def part1(lines):
    count = 0
    for _, outputs in lines:
        for output in outputs:
            if len(output) in {7, 2, 4, 3}:
                count += 1
    return count


def part2(lines):
    total = 0
    for inputs, outputs in lines:
        mapping = solve_line(inputs)
        outputs = [mapping[frozenset(output)] for output in outputs]
        total += int(''.join(str(d) for d in outputs))
    return total


def solve_line(inputs):
    # Mapping
    #  111
    # 2   3
    # 2   3
    # 2   3
    #  444
    # 5   6
    # 5   6
    # 5   6
    #  777
    values = set(frozenset(v) for v in inputs)
    digit_segments = {
        0: {1, 2, 3, 5, 6, 7},
        1: {3, 6},
        2: {1, 3, 4, 5, 7},
        3: {1, 3, 4, 6, 7},
        4: {2, 3, 4, 6},
        5: {1, 2, 4, 6, 7},
        6: {1, 2, 4, 5, 6, 7},
        7: {1, 3, 6},
        8: {1, 2, 3, 4, 5, 6, 7},
        9: {1, 2, 3, 4, 6, 7},
    }
    possable = {digit: [v for v in values if len(v) == len(segments)]
                for digit, segments in digit_segments.items()}
    segment_mapping = {segment: set("abcdefg") for segment in range(1, 8)}
    mapping = {}
    while len(possable) > 0:
        next_possable = {}
        for digit, poss in possable.items():
            if len(poss) == 1:
                mapping[poss[0]] = digit
                for segment, segment_map in segment_mapping.items():
                    if segment in digit_segments[digit]:
                        segment_map.intersection_update(poss[0])
                    else:
                        segment_map.difference_update(poss[0])
            else:
                def has_letters(letters):
                    counter = defaultdict(int)
                    for segment in digit_segments[digit]:
                        counter[frozenset(segment_mapping[segment])] += 1
                    for items, count in counter.items():
                        if len(letters.intersection(items)) != count:
                            return False
                    return True
                next_possable[digit] = [p for p in poss if has_letters(p)]
        possable = next_possable
    return mapping


def parse(line):
    signals, outputs = line.split(' | ')
    signals = tuple(signals.split(' '))
    outputs = tuple(outputs.split(' '))
    return (signals, outputs)


TEST = """be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb | fdgacbe cefdb cefbgd gcbe
edbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec | fcgedb cgb dgebacf gc
fgaebd cg bdaec gdafb agbcfd gdcbef bgcad gfac gcb cdgabef | cg cg fdcagb cbg
fbegcd cbd adcefb dageb afcb bc aefdc ecdab fgdeca fcdbega | efabcd cedba gadfec cb
aecbfdg fbg gf bafeg dbefa fcge gcbea fcaegb dgceab fcbdga | gecf egdcabf bgf bfgea
fgeab ca afcebg bdacfeg cfaedg gcfdb baec bfadeg bafgc acf | gebdcfa ecba ca fadegcb
dbcfg fgd bdegcaf fgec aegbdf ecdfab fbedc dacgb gdcebf gf | cefg dcbef fcge gbcadfe
bdfegc cbegaf gecbf dfcage bdacg ed bedf ced adcbefg gebcd | ed bcgafe cdgba cbgef
egadfb cdbfeg cegd fecab cgb gbdefca cg fgcdab egfdb bfceg | gbdfcae bgc cg cgb
gcafb gcf dcaebfg ecagb gf abcdeg gaef cafbge fdbac fegbdc | fgae cfgab fg bagce"""


SMALL = "acedgfb cdfbe gcdfa fbcad dab cefabd cdfgeb eafb cagedb ab | cdfeb fcadb cdfeb cdbaf"
if __name__ == "__main__":
    assert part1(line_parser(TEST, parse=parse)) == 26
    assert part2(line_parser(SMALL, parse=parse)) == 5353
    assert part2(line_parser(TEST, parse=parse)) == 61229
    LINES = line_parser(get_input(day=8, year=2021), parse=parse)
    print(f"Part 1: {part1(LINES)}")
    print(f"Part 2: {part2(LINES)}")
