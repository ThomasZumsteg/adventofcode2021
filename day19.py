"""Solution to day 19 of Advent of Code"""

from collections import defaultdict
from get_input import get_input
import re
from itertools import combinations, permutations, product


def apply_rotation(rot_vec, point):
    assert len(rot_vec) == 3

    def rotate_x(point):
        return (point[0], -point[2], point[1])

    def rotate_y(point):
        return (point[2], point[1], -point[0])

    def rotate_z(point):
        return (-point[1], point[0], point[2])

    for count, rotation in zip(rot_vec, (rotate_x, rotate_y, rotate_z)):
        for _ in range(count):
            point = rotation(point)
    return point


def apply_translation(translation, point):
    assert len(translation) == len(point)
    return tuple(t+p for t, p in zip(translation, point))


def part1(scanners, common=12):
    distances = defaultdict(lambda: defaultdict(set))
    for scanner, beacons in scanners.items():
        for beacon_a, beacon_b in combinations(beacons, 2):
            diff = tuple(a - b for a, b in zip(beacon_a, beacon_b))
            distance = frozenset(abs(d) for d in diff)
            distances[distance][scanner].add((beacon_a, beacon_b))
    overlaps = defaultdict(lambda: defaultdict(set))
    for matches in distances.values():
        if len(matches) < 2:
            continue
        for scanner_a, scanner_b in permutations(matches, 2):
            pair_a = list(matches[scanner_a])
            pair_b = list(matches[scanner_b])
            assert len(pair_a) == len(pair_b) == 1
            overlaps[scanner_a][scanner_b].add((pair_a[0], pair_b[0]))

    offsets = {
        0: ((0, 0, 0), (0, 0, 0)),
    }
    beacon_remap = {0: {b: b for b in scanners[0]}}
    while not all(s in offsets for s in scanners.keys()):
        keys = list(offsets.keys())
        for scanner in keys:
            for overlap, pair_keys in overlaps.get(scanner, {}).items():
                if overlap in offsets:
                    continue
                diffs = defaultdict(int)
                for rotation in product(range(4), repeat=3):
                    if overlap in offsets:
                        break
                    for anchor_pair, map_pair in pair_keys:
                        anchor_pair = (
                            beacon_remap[scanner][anchor_pair[0]],
                            beacon_remap[scanner][anchor_pair[1]],
                        )
                        anchor_diff = tuple(a-b for a, b in zip(*anchor_pair))
                        map_diff = tuple(a-b for a, b in zip(*map_pair))
                        map_diff = apply_rotation(rotation, map_diff)
                        if map_diff == anchor_diff:
                            map_pair = tuple(
                                apply_rotation(rotation, pair)
                                for pair in map_pair
                            )
                            translation = tuple(
                                a-b for a, b in
                                zip(anchor_pair[0], map_pair[0])
                            )
                            alt = tuple(a-b for a, b in
                                        zip(anchor_pair[1], map_pair[1]))
                            assert alt == translation
                            diffs[translation] += 1
                    for translation, value in diffs.items():
                        if value > 12:
                            print(f"{scanner} - {overlap} : {translation}")
                            offsets[overlap] = (translation, rotation)
                            beacon_remap[overlap] = {}
                            for beacon in scanners[overlap]:
                                real = apply_rotation(rotation, beacon)
                                real = apply_translation(translation, real)
                                beacon_remap[overlap][beacon] = real
    return len(set(
        b for remap in beacon_remap.values()
        for b in remap.values()
    ))


def part2(scanners, common=12):
    distances = defaultdict(lambda: defaultdict(set))
    for scanner, beacons in scanners.items():
        for beacon_a, beacon_b in combinations(beacons, 2):
            diff = tuple(a - b for a, b in zip(beacon_a, beacon_b))
            distance = frozenset(abs(d) for d in diff)
            distances[distance][scanner].add((beacon_a, beacon_b))
    overlaps = defaultdict(lambda: defaultdict(set))
    for matches in distances.values():
        if len(matches) < 2:
            continue
        for scanner_a, scanner_b in permutations(matches, 2):
            pair_a = list(matches[scanner_a])
            pair_b = list(matches[scanner_b])
            assert len(pair_a) == len(pair_b) == 1
            overlaps[scanner_a][scanner_b].add((pair_a[0], pair_b[0]))

    offsets = {
        0: ((0, 0, 0), (0, 0, 0)),
    }
    beacon_remap = {0: {b: b for b in scanners[0]}}
    while not all(s in offsets for s in scanners.keys()):
        keys = list(offsets.keys())
        for scanner in keys:
            for overlap, pair_keys in overlaps.get(scanner, {}).items():
                if overlap in offsets:
                    continue
                diffs = defaultdict(int)
                for rotation in product(range(4), repeat=3):
                    if overlap in offsets:
                        break
                    for anchor_pair, map_pair in pair_keys:
                        anchor_pair = (
                            beacon_remap[scanner][anchor_pair[0]],
                            beacon_remap[scanner][anchor_pair[1]],
                        )
                        anchor_diff = tuple(a-b for a, b in zip(*anchor_pair))
                        map_diff = tuple(a-b for a, b in zip(*map_pair))
                        map_diff = apply_rotation(rotation, map_diff)
                        if map_diff == anchor_diff:
                            map_pair = tuple(
                                apply_rotation(rotation, pair)
                                for pair in map_pair
                            )
                            translation = tuple(
                                a-b for a, b in
                                zip(anchor_pair[0], map_pair[0])
                            )
                            alt = tuple(a-b for a, b in
                                        zip(anchor_pair[1], map_pair[1]))
                            assert alt == translation
                            diffs[translation] += 1
                    for translation, value in diffs.items():
                        if value > 12:
                            print(f"{scanner} - {overlap} : {translation}")
                            offsets[overlap] = (translation, rotation)
                            beacon_remap[overlap] = {}
                            for beacon in scanners[overlap]:
                                real = apply_rotation(rotation, beacon)
                                real = apply_translation(translation, real)
                                beacon_remap[overlap][beacon] = real
    translations = [off[0] for off in offsets.values()]
    breakpoint()
    distances = tuple(
        sum(abs(a-b) for a, b in zip(a_vec, b_vec))
        for a_vec, b_vec in permutations(translations, 2)
    )

    return max(distances)


def parse(lines):
    scanners = {}
    for line in lines.splitlines():
        m = re.match(r'--- scanner (\d+) ---$', line)
        if line == "":
            continue
        elif m:
            scanner = int(m.group(1))
            beacons = set()
            scanners[scanner] = beacons
        else:
            x, y, z = line.split(',')
            beacons.add((int(x), int(y), int(z)))
    return scanners


TEST = """--- scanner 0 ---
404,-588,-901
528,-643,409
-838,591,734
390,-675,-793
-537,-823,-458
-485,-357,347
-345,-311,381
-661,-816,-575
-876,649,763
-618,-824,-621
553,345,-567
474,580,667
-447,-329,318
-584,868,-557
544,-627,-890
564,392,-477
455,729,728
-892,524,684
-689,845,-530
423,-701,434
7,-33,-71
630,319,-379
443,580,662
-789,900,-551
459,-707,401

--- scanner 1 ---
686,422,578
605,423,415
515,917,-361
-336,658,858
95,138,22
-476,619,847
-340,-569,-846
567,-361,727
-460,603,-452
669,-402,600
729,430,532
-500,-761,534
-322,571,750
-466,-666,-811
-429,-592,574
-355,545,-477
703,-491,-529
-328,-685,520
413,935,-424
-391,539,-444
586,-435,557
-364,-763,-893
807,-499,-711
755,-354,-619
553,889,-390

--- scanner 2 ---
649,640,665
682,-795,504
-784,533,-524
-644,584,-595
-588,-843,648
-30,6,44
-674,560,763
500,723,-460
609,671,-379
-555,-800,653
-675,-892,-343
697,-426,-610
578,704,681
493,664,-388
-671,-858,530
-667,343,800
571,-461,-707
-138,-166,112
-889,563,-600
646,-828,498
640,759,510
-630,509,768
-681,-892,-333
673,-379,-804
-742,-814,-386
577,-820,562

--- scanner 3 ---
-589,542,597
605,-692,669
-500,565,-823
-660,373,557
-458,-679,-417
-488,449,543
-626,468,-788
338,-750,-386
528,-832,-391
562,-778,733
-938,-730,414
543,643,-506
-524,371,-870
407,773,750
-104,29,83
378,-903,-323
-778,-728,485
426,699,580
-438,-605,-362
-469,-447,-387
509,732,623
647,635,-688
-868,-804,481
614,-800,639
595,780,-596

--- scanner 4 ---
727,592,562
-293,-554,779
441,611,-461
-714,465,-776
-743,427,-804
-660,-479,-426
832,-632,460
927,-485,-438
408,393,-506
466,436,-512
110,16,151
-258,-428,682
-393,719,612
-211,-452,876
808,-476,-593
-575,615,604
-485,667,467
-680,325,-822
-627,-443,-432
872,-547,-609
833,512,582
807,604,487
839,-516,451
891,-625,532
-652,-548,-490
30,-46,-14"""


if __name__ == "__main__":
    # assert part1(line_parser(TEST, parse=parse)) == None
    # assert part2(line_parser(TEST, parse=parse)) == None
    LINES = parse(get_input(day=19, year=2021))
    test = parse(TEST)
    assert part1(test) == 79
    print(f"Part 1: {part1(LINES)}")

    assert part2(test) == 3621
    print(f"Part 2: {part2(LINES)}")
