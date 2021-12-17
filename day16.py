"""Solution to day 16 of Advent of Code"""

from get_input import get_input


def read_packet(bits):
    version, packet_type = int(bits[:3], 2), int(bits[3:6], 2)
    bits = bits[6:]
    if packet_type == 4:
        data = 0
        cont = '1'
        while cont != '0':
            cont, word, bits = bits[0], bits[1:5], bits[5:]
            data <<= 4
            data += int(word, 2)
    elif bits[0] == '0':
        # total length in bits
        length, bits = int(bits[1:16], 2), bits[16:]
        subpackets, bits = bits[:length], bits[length:]
        data = []
        while subpackets and not all(b == '0' for b in subpackets):
            packet, subpackets = read_packet(subpackets)
            data.append(packet)
    elif bits[0] == '1':
        n_subpackets, bits = int(bits[1:12], 2), bits[12:]
        data = []
        for _ in range(n_subpackets):
            packet, bits = read_packet(bits)
            data.append(packet)
    else:
        raise NotImplementedError
    return (version, packet_type, data), bits


def part1(packet):
    root, _ = read_packet(packet)
    count_queue = [root]
    total = 0
    while count_queue:
        version, _, sub = count_queue.pop()
        total += version
        if isinstance(sub, list):
            count_queue.extend(sub)
    return total


def eval_packet(packet):
    version, packet_type, value = packet[:]
    assert packet_type == 4 or isinstance(value, list)
    if packet_type == 0:
        return sum(eval_packet(p) for p in value)
    if packet_type == 1:
        assert len(value) > 0
        total = 1
        for p in value:
            total *= eval_packet(p)
        return total
    if packet_type == 2:
        return min(eval_packet(p) for p in value)
    if packet_type == 3:
        return max(eval_packet(p) for p in value)
    if packet_type == 4:
        return value
    if packet_type == 5:
        assert len(value) == 2
        return 1 if eval_packet(value[0]) > eval_packet(value[1]) else 0
    if packet_type == 6:
        assert len(value) == 2
        return 1 if eval_packet(value[0]) < eval_packet(value[1]) else 0
    if packet_type == 7:
        assert len(value) == 2
        return 1 if eval_packet(value[0]) == eval_packet(value[1]) else 0


def part2(packet):
    root, _ = read_packet(packet)
    return eval_packet(root)


def parse(lines):
    lines = lines.splitlines()
    assert len(lines) == 1
    return ''.join('{:04b}'.format(int(char, 16)) for char in lines[0])


if __name__ == "__main__":
    LINES = parse(get_input(day=16, year=2021))
    assert part1(parse("D2FE28")) == 6
    assert part1(parse("EE00D40C823060")) == 14
    assert part1(parse("8A004A801A8002F478")) == 16
    assert part1(parse("620080001611562C8802118E34")) == 12
    assert part1(parse("C0015000016115A2E0802F182340")) == 23
    assert part1(parse("A0016C880162017C3686B18A3D4780")) == 31
    print(f"Part 1: {part1(LINES)}")

    assert part2(parse("C200B40A82")) == 3
    assert part2(parse("04005AC33890")) == 54
    assert part2(parse("880086C3E88112")) == 7
    assert part2(parse("CE00C43D881120")) == 9
    assert part2(parse("D8005AC2A8F0")) == 1
    assert part2(parse("F600BC2D8F")) == 0
    assert part2(parse("9C005AC2F8F0")) == 0
    assert part2(parse("9C0141080250320F1802104A08")) == 1
    print(f"Part 2: {part2(LINES)}")
