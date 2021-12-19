"""Solution to day 18 of Advent of Code"""

from get_input import get_input, line_parser
import itertools


class Node:
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return str(self.value)

    def __add__(self, other):
        if isinstance(other, Node):
            other = other.value
        self.value += other
        return self

    def __lt__(self, other):
        if isinstance(other, Node):
            other = other.value
        return self.value < other

    def __le__(self, other):
        if isinstance(other, Node):
            other = other.value
        return self.value <= other

    def __gt__(self, other):
        if isinstance(other, Node):
            other = other.value
        return self.value > other

    def __ge__(self, other):
        if isinstance(other, Node):
            other = other.value
        return self.value >= other


class Pair:
    def __init__(self, left, right, parent=None):
        if isinstance(left, list):
            assert len(left) == 2
            left = Pair(left[0], left[1])
        if isinstance(left, Pair):
            left.parent = self
        if isinstance(right, list):
            assert len(right) == 2
            right = Pair(right[0], right[1])
        if isinstance(right, Pair):
            right.parent = self
        self.left = left
        self.right = right
        self.parent = parent

    def resolved(self):
        for node in self.pairs():
            if node.depth > 4:
                node.explode()
                return False
        for node in self.pairs():
            if isinstance(node.left, int) and node.left >= 10:
                div, mod = divmod(node.left, 2)
                node.left = Pair(div, div+mod, parent=node)
                return False
            elif isinstance(node.right, int) and node.right >= 10:
                div, mod = divmod(node.right, 2)
                node.right = Pair(div, div+mod, parent=node)
                return False
        return True

    def __repr__(self):
        return f"[{repr(self.left)},{repr(self.right)}]"

    def pairs(self):
        if isinstance(self.left, Pair):
            yield from self.left.pairs()
        yield self
        if isinstance(self.right, Pair):
            yield from self.right.pairs()

    @property
    def depth(self):
        node = self
        depth = 0
        while node is not None:
            node = node.parent
            depth += 1
        return depth

    def get_cw_node(self):
        last, node = self, self.parent
        while node is not None:
            if node.left is not last:
                if isinstance(node.left, int):
                    return node, 'left'
                node = node.left
                break
            last, node = node, node.parent
        if node is None:
            return None
        while not isinstance(node.right, int):
            node = node.right
        return node, 'right'

    def get_ccw_node(self):
        last, node = self, self.parent
        while node is not None:
            if node.right is not last:
                if isinstance(node.right, int):
                    return node, 'right'
                node = node.right
                break
            last, node = node, node.parent
        if node is None:
            return None
        while not isinstance(node.left, int):
            node = node.left
        return node, 'left'

    def explode(self):
        assert isinstance(self.left, int)
        assert isinstance(self.right, int)

        left_node = self.get_cw_node()
        right_node = self.get_ccw_node()
        if left_node:
            setattr(left_node[0], left_node[1],
                    getattr(left_node[0], left_node[1])+self.left)
        if right_node:
            setattr(right_node[0], right_node[1],
                    getattr(right_node[0], right_node[1])+self.right)

        if self is self.parent.right:
            self.parent.right = 0
        if self is self.parent.left:
            self.parent.left = 0

    def __eq__(self, other):
        assert isinstance(other, Pair)
        return self.left == other.left and self.right == other.right

    def magnitude(self):
        left = self.left
        if isinstance(left, Pair):
            left = left.magnitude()
        right = self.right
        if isinstance(right, Pair):
            right = right.magnitude()
        return left * 3 + right * 2


def part1(lines):
    root = None
    for line in lines:
        if root is None:
            root = Pair(*line)
        else:
            root = Pair(root, Pair(*line))
        while True:
            # print("\t"+str(root))
            if root.resolved():
                break
        # print(root)
    return root.magnitude()


def part2(lines):
    def get_magnitude(pair_a, pair_b):
        pair = Pair(pair_a, pair_b)
        while True:
            if pair.resolved():
                break
        return pair.magnitude()
    max_magnitude = 0
    assert get_magnitude(
        [[2,[[7,7],7]],[[5,8],[[9,3],[0,2]]]],
        [[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]]
    ) == 3993
    for pair_a, pair_b in itertools.product(iter(lines), iter(lines)):
        max_magnitude = max(
            max_magnitude,
            get_magnitude(pair_a, pair_b)
        )
    return max_magnitude


def parse(line):
    stack = []
    for char in line:
        if char == '[':
            stack.append([])
            digits = ''
        elif char == ']' or char == ',':
            if digits != '':
                stack[-1].append(int(digits))
            else:
                child = stack.pop()
                stack[-1].append(child)
            digits = ''
        else:
            digits += char
    return stack[0]


TEST = """[[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]]
[[[5,[2,8]],4],[5,[[9,9],0]]]
[6,[[[6,2],[5,6]],[[7,6],[4,7]]]]
[[[6,[0,7]],[0,9]],[4,[9,[9,0]]]]
[[[7,[6,4]],[3,[1,3]]],[[[5,5],1],9]]
[[6,[[7,3],[3,2]]],[[[3,8],[5,7]],4]]
[[[[5,4],[7,7]],8],[[8,3],8]]
[[9,3],[[9,9],[6,[4,9]]]]
[[2,[[7,7],7]],[[5,8],[[9,3],[0,2]]]]
[[[[5,2],5],[8,[3,7]]],[[5,[7,5]],[4,4]]]
"""

# TEST = """[[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]]
# [7,[[[3,7],[4,3]],[[6,3],[8,8]]]]
# [[2,[[0,8],[3,4]]],[[[6,7],1],[7,[1,6]]]]
# [[[[2,4],7],[6,[0,5]]],[[[6,8],[2,8]],[[2,1],[4,5]]]]
# [7,[5,[[3,8],[1,4]]]]
# [[2,[2,2]],[8,[8,1]]]
# [2,9]
# [1,[[[9,3],9],[[9,0],[0,7]]]]
# [[[5,[7,4]],7],1]
# [[[[4,2],2],6],[8,7]]"""


# TEST = """[1,1]
# [2,2]
# [3,3]
# [4,4]
# [5,5]
# """


if __name__ == "__main__":
    pair = Pair([[[[9, 8], 1], 2], 3],  4)
    assert not pair.resolved()
    assert pair.resolved()
    assert pair == Pair([[[0, 9], 2], 3], 4)

    pair = Pair(7,[6,[5,[4,[3,2]]]])
    assert not pair.resolved()
    assert pair.resolved()
    assert pair == Pair(7,[6,[5,[7,0]]])

    pair = Pair([6,[5,[4,[3,2]]]],1)
    assert not pair.resolved()
    assert pair.resolved()
    assert pair == Pair([6,[5,[7,0]]],3)

    assert parse('[5,5]') == [5, 5]
    assert parse('[[1,5],5]') == [[1, 5], 5]
    assert parse('[1,[2,3]]') == [1, [2, 3]]

    LINES = line_parser(get_input(day=18, year=2021), parse=parse)
    assert part1(line_parser(TEST, parse=parse)) == 4140
    print(f"Part 1: {part1(LINES)}")

    assert part2(line_parser(TEST, parse=parse)) == 3993
    print(f"Part 2: {part2(LINES)}")
