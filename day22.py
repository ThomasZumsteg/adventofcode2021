"""Solution to day 22 of Advent of Code"""

from get_input import get_input, line_parser
import re


def part1(steps):
    filtered = []
    for state, x_range, y_range, z_range in steps:
        rngs = (x_range, y_range, z_range)
        if not all(-50 <= rng[0] < rng[1] <= 51 for rng in rngs):
            continue
        filtered.append((state, x_range, y_range, z_range))
    return part2(filtered)


def subtract(left_cube, right_cube):
    """Subtract two hypercubes returing resultant cubes of the same dimention
    that represent what remains of the left cube

    Not recommended for dimentions higher then 3, it hurts my brain"""
    # left_cube - right_cube = what_remains_of_left
    cube = list(left_cube)
    result = set()
    for axis, (left, right) in enumerate(zip(left_cube, right_cube)):
        if left[0] < right[0] < right[1] < left[1]:
            # |<left   |<right    right>|   left>|
            for value in ((left[0], right[0]), (right[1], left[1])):
                copy = cube.copy()
                copy[axis] = value
                result.add(tuple(copy))
            cube[axis] = right
        elif left[0] < right[0] <= left[1] <= right[1]:
            # |<left    |<right    left>|    right>|
            copy = cube.copy()
            copy[axis] = (left[0], right[0])
            result.add(tuple(copy))
            if right[0] == left[1]:
                break
            cube[axis] = (right[0], left[1])
        elif right[0] <= left[0] <= right[1] < left[1]:
            # |<right   |<left    right>|     left>|
            copy = cube.copy()
            copy[axis] = (right[1], left[1])
            result.add(tuple(copy))
            if left[0] == right[1]:
                break
            cube[axis] = (left[0], right[1])
        elif left[1] <= right[0] or right[1] <= left[0]:
            # |<left    left>|   |<right   right>|
            # or
            # |<right  right>|   |<left     left>|
            result.add(tuple(cube.copy()))
            break
        else:
            #    |<right     |<left      left>|     right>|
            assert right[0] <= left[0] < left[1] <= right[1]
    return result


def test_intersections():
    assert subtract(
        ((0, 10), (0, 10), (0, 10)),
        ((0, 10), (0, 10), (0, 10)),
    ) == set()

    assert subtract(
        ((10, 30), (0, 10), (0, 10)),
        ((0, 20), (0, 10), (0, 10)),
    ) == set([((20, 30), (0, 10), (0, 10))])

    assert subtract(
        ((11, 14), (11, 14), (11, 14)),  # 27
        ((10, 13), (10, 13), (10, 13)),  # 27
    ) == set([
        ((13, 14), (11, 14), (11, 14)),  # 9
        ((11, 13), (13, 14), (11, 14)),  # 6
        ((11, 13), (11, 13), (13, 14)),  # 4  # 19
    ])

    assert subtract(
        ((1, 3), (1, 3), (1, 3)),  # 8
        ((0, 4), (0, 4), (0, 4)),  # 64
    ) == set()

    assert subtract(
        ((0, 4), (0, 4), (0, 4)),  # 64
        ((1, 3), (1, 3), (1, 3)),  # 8
    ) == set([
            ((0, 1), (0, 4), (0, 4)),  # 16
            ((3, 4), (0, 4), (0, 4)),  # 16
            ((1, 3), (0, 1), (0, 4)),  # 8
            ((1, 3), (3, 4), (0, 4)),  # 8
            ((1, 3), (1, 3), (0, 1)),  # 4
            ((1, 3), (1, 3), (3, 4)),  # 4
    ])

    assert subtract(
        ((11, 12), (11, 12), (9, 10)),
        ((10, 11), (10, 13), (10, 13))
    ) == set([((11, 12), (11, 12), (9, 10)), ])

    assert subtract(
        ((10, 11), (10, 13), (10, 13)),
        ((11, 12), (11, 12), (9, 10)),
    ) == set([((10, 11), (10, 13), (10, 13)), ])

    assert subtract(
        ((1, 3), (1, 3), (0, 8)),
        ((0, 4), (0, 4), (2, 6)),
    ) == set([
        ((1, 3), (1, 3), (0, 2)),
        ((1, 3), (1, 3), (6, 8)),
    ])

    # Test 2d
    assert subtract(
        ((0, 8), (0, 8)),
        ((2, 6), (2, 6)),
    ) == set([
        ((0, 2), (0, 8)),
        ((6, 8), (0, 8)),
        ((2, 6), (0, 2)),
        ((2, 6), (6, 8)),
    ])

    # Test 1d
    assert subtract(
        ((0, 8),),
        ((2, 6),),
    ) == set([
        ((0, 2),),
        ((6, 8),),
    ])


def size(cubes):
    total = 0
    for cube in cubes:
        total += (cube[0][1] - cube[0][0]) *\
            (cube[1][1] - cube[1][0]) *\
            (cube[2][1] - cube[2][0])
    return total


def part2(steps):
    on_cubes = set()  # non intersection on cubes
    for state, x_range, y_range, z_range in steps:
        # print(f"{state}: {x_range},{y_range},{z_range} - {len(on_cubes)}")
        cube = (x_range, y_range, z_range)
        next_on_cubes = set()
        if state == 'on':
            next_on_cubes.add(cube)
        for on in on_cubes:
            on_set = subtract(on, cube)
            next_on_cubes.update(on_set)
        on_cubes = next_on_cubes
    return size(on_cubes)


def parse(line):
    m = re.match(
        r"(on|off) x=(-?\d+)..(-?\d+),y=(-?\d+)..(-?\d+),z=(-?\d+)..(-?\d+)$",
        line
    )
    return (
        m.group(1),
        (int(m.group(2)), int(m.group(3))+1),
        (int(m.group(4)), int(m.group(5))+1),
        (int(m.group(6)), int(m.group(7))+1)
    )


TEST = """on x=-20..26,y=-36..17,z=-47..7
on x=-20..33,y=-21..23,z=-26..28
on x=-22..28,y=-29..23,z=-38..16
on x=-46..7,y=-6..46,z=-50..-1
on x=-49..1,y=-3..46,z=-24..28
on x=2..47,y=-22..22,z=-23..27
on x=-27..23,y=-28..26,z=-21..29
on x=-39..5,y=-6..47,z=-3..44
on x=-30..21,y=-8..43,z=-13..34
on x=-22..26,y=-27..20,z=-29..19
off x=-48..-32,y=26..41,z=-47..-37
on x=-12..35,y=6..50,z=-50..-2
off x=-48..-32,y=-32..-16,z=-15..-5
on x=-18..26,y=-33..15,z=-7..46
off x=-40..-22,y=-38..-28,z=23..41
on x=-16..35,y=-41..10,z=-47..6
off x=-32..-23,y=11..30,z=-14..3
on x=-49..-5,y=-3..45,z=-29..18
off x=18..30,y=-20..-8,z=-3..13
on x=-41..9,y=-7..43,z=-33..15
on x=-54112..-39298,y=-85059..-49293,z=-27449..7877
on x=967..23432,y=45373..81175,z=27513..53682"""


TEST2 = """on x=-5..47,y=-31..22,z=-19..33
on x=-44..5,y=-27..21,z=-14..35
on x=-49..-1,y=-11..42,z=-10..38
on x=-20..34,y=-40..6,z=-44..1
off x=26..39,y=40..50,z=-2..11
on x=-41..5,y=-41..6,z=-36..8
off x=-43..-33,y=-45..-28,z=7..25
on x=-33..15,y=-32..19,z=-34..11
off x=35..47,y=-46..-34,z=-11..5
on x=-14..36,y=-6..44,z=-16..29
on x=-57795..-6158,y=29564..72030,z=20435..90618
on x=36731..105352,y=-21140..28532,z=16094..90401
on x=30999..107136,y=-53464..15513,z=8553..71215
on x=13528..83982,y=-99403..-27377,z=-24141..23996
on x=-72682..-12347,y=18159..111354,z=7391..80950
on x=-1060..80757,y=-65301..-20884,z=-103788..-16709
on x=-83015..-9461,y=-72160..-8347,z=-81239..-26856
on x=-52752..22273,y=-49450..9096,z=54442..119054
on x=-29982..40483,y=-108474..-28371,z=-24328..38471
on x=-4958..62750,y=40422..118853,z=-7672..65583
on x=55694..108686,y=-43367..46958,z=-26781..48729
on x=-98497..-18186,y=-63569..3412,z=1232..88485
on x=-726..56291,y=-62629..13224,z=18033..85226
on x=-110886..-34664,y=-81338..-8658,z=8914..63723
on x=-55829..24974,y=-16897..54165,z=-121762..-28058
on x=-65152..-11147,y=22489..91432,z=-58782..1780
on x=-120100..-32970,y=-46592..27473,z=-11695..61039
on x=-18631..37533,y=-124565..-50804,z=-35667..28308
on x=-57817..18248,y=49321..117703,z=5745..55881
on x=14781..98692,y=-1341..70827,z=15753..70151
on x=-34419..55919,y=-19626..40991,z=39015..114138
on x=-60785..11593,y=-56135..2999,z=-95368..-26915
on x=-32178..58085,y=17647..101866,z=-91405..-8878
on x=-53655..12091,y=50097..105568,z=-75335..-4862
on x=-111166..-40997,y=-71714..2688,z=5609..50954
on x=-16602..70118,y=-98693..-44401,z=5197..76897
on x=16383..101554,y=4615..83635,z=-44907..18747
off x=-95822..-15171,y=-19987..48940,z=10804..104439
on x=-89813..-14614,y=16069..88491,z=-3297..45228
on x=41075..99376,y=-20427..49978,z=-52012..13762
on x=-21330..50085,y=-17944..62733,z=-112280..-30197
on x=-16478..35915,y=36008..118594,z=-7885..47086
off x=-98156..-27851,y=-49952..43171,z=-99005..-8456
off x=2032..69770,y=-71013..4824,z=7471..94418
on x=43670..120875,y=-42068..12382,z=-24787..38892
off x=37514..111226,y=-45862..25743,z=-16714..54663
off x=25699..97951,y=-30668..59918,z=-15349..69697
off x=-44271..17935,y=-9516..60759,z=49131..112598
on x=-61695..-5813,y=40978..94975,z=8655..80240
off x=-101086..-9439,y=-7088..67543,z=33935..83858
off x=18020..114017,y=-48931..32606,z=21474..89843
off x=-77139..10506,y=-89994..-18797,z=-80..59318
off x=8476..79288,y=-75520..11602,z=-96624..-24783
on x=-47488..-1262,y=24338..100707,z=16292..72967
off x=-84341..13987,y=2429..92914,z=-90671..-1318
off x=-37810..49457,y=-71013..-7894,z=-105357..-13188
off x=-27365..46395,y=31009..98017,z=15428..76570
off x=-70369..-16548,y=22648..78696,z=-1892..86821
on x=-53470..21291,y=-120233..-33476,z=-44150..38147
off x=-93533..-4276,y=-16170..68771,z=-104985..-24507"""


SHORT = """on x=10..12,y=10..12,z=10..12
on x=11..13,y=11..13,z=11..13
off x=9..11,y=9..11,z=9..11
on x=10..10,y=10..10,z=10..10"""

if __name__ == "__main__":
    LINES = line_parser(get_input(day=22, year=2021), parse=parse)

    assert part1(line_parser(TEST, parse=parse)) == 590784
    print(f"Part 1: {part1(LINES)}")

    test_intersections()

    assert part2(line_parser(SHORT, parse=parse)) == 27 + 19 - 8 + 1
    assert part2(line_parser(TEST, parse=parse)[:-2]) == 590784
    result = part2(line_parser(TEST2, parse=parse))
    assert result == 2758514936282235, result
    print(f"Part 2: {part2(LINES)}")
