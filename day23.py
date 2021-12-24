"""Solution to day 23 of Advent of Code"""

from collections import namedtuple, defaultdict
from enum import Enum
from get_input import get_input
from itertools import product
from queue import PriorityQueue
import os


class AmphException(Exception):
    pass


class State(Enum):
    START = "START"
    IN_HALLWAY = "IN_HALLWAY"
    DONE = "DONE"


class Species(Enum):
    AMBER = 1
    BRONZE = 10
    COPPER = 100
    DESERT = 1000

    @staticmethod
    def get_species(letter):
        if letter == 'A':
            return Species.AMBER
        if letter == 'B':
            return Species.BRONZE
        if letter == 'C':
            return Species.COPPER
        if letter == 'D':
            return Species.DESERT

    def get_letter(self):
        if self.name == 'AMBER':
            return 'A'
        if self.name == 'BRONZE':
            return 'B'
        if self.name == 'COPPER':
            return 'C'
        if self.name == 'DESERT':
            return 'D'
        raise NotImplementedError


class Amphipod(namedtuple('Amphipod',
                          ['position', 'species', 'state', 'goal_room'])):
    def __lt__(self, other):
        return (self.species, self.goal_room) < \
               (other.species, other.goal_room)

    def in_room(self):
        return self.position.real > 1 and self.position.imag == self.goal_room


def move_to_room(amp, board):
    position = amp.position
    for row in range(2, 6):
        point = complex(row, amp.goal_room)
        if point not in board.open_spaces:
            break
        if point in board.amps and not board.amps[point].in_room():
            raise AmphException("Room full")
    horiz = 1j if amp.goal_room > position.imag else -1j
    used = 0
    while position.imag != amp.goal_room:
        position += horiz
        used += amp.species.value
        if position in board.amps:
            raise AmphException("No path")
    while board.is_open(position + 1):
        position += 1
        used += amp.species.value
    if position not in board.open_spaces:
        raise NotImplementedError
    return (used, Amphipod(
        position, amp.species, State.DONE, amp.goal_room))


def move_to_hallway(amp, board):
    used, position = 0, amp.position
    # Move to hallway
    while position.real > 1:
        position -= 1
        used += amp.species.value
        if not board.is_open(position):
            # Blocked in
            return
    # move left and right
    queue = [(used, -1j, position), (used, 1j, position)]
    while queue:
        used, step, position = queue.pop()
        if not board.is_open(position):
            continue
        if board.in_hallway(position):
            yield used, Amphipod(
                position, amp.species, State.IN_HALLWAY, amp.goal_room)
        queue.append((used+amp.species.value, step, position+step))


class Board:
    def __init__(self, open_spaces):
        self.open_spaces = open_spaces
        self.room_map = defaultdict(list)
        self.hallway = set()
        for space in open_spaces:
            if space.real > 1:
                self.room_map[space.imag].append(space)
            else:
                self.hallway.add(space)
        self.hallway.difference_update(
            complex(1, rid) for rid in self.room_map.keys()
        )
        for room in self.room_map.values():
            room.sort(key=lambda p: p.real)

    def add_amps(self, amps):
        self.amps = {a.position: a for a in amps}

    def remove_amps(self):
        self.amps.clear()

    @property
    def room(self):
        rooms = {}
        for rid, room in self.room_map.items():
            rooms[rid] = []
            for depth in range(2, 5):
                if complex(depth, rid) in self.amps:
                    rooms[rid].append(self.amps[complex(depth, rid)])
        return rooms

    def is_open(self, position):
        if position not in self.open_spaces:
            return False
        return position not in self.amps

    def in_hallway(self, position):
        return position in self.hallway

    def __str__(self):
        lines = []
        for r in range(7):
            lines.append([])
            for c in range(13):
                point = complex(r, c)
                char = '#'
                if point in self.amps:
                    char = self.amps[point].species.get_letter()
                elif point in self.open_spaces:
                    char = '.'
                lines[-1].append(char)
        return '\n'.join(''.join(line) for line in lines)


def part1(lines):
    amphipods, spaces = lines[:]
    board = Board(spaces)

    room_ids = tuple(sorted(set(p.imag for p in spaces if p.real > 1)))
    assignments = dict(zip(tuple(s for s in Species), room_ids))

    state = [Amphipod(position, species, State.START, assignments[species])
             for species, position in amphipods]
    queue = PriorityQueue()
    queue.put((0, 0, tuple(state)))
    seen = set()
    while not queue.empty():
        energy, steps, state = queue.get()
        board.add_amps(state)
        if state in seen:
            continue
        seen.add(state)
        if all(amp.position.imag == amp.goal_room for amp in state):
            print(' ' * os.get_terminal_size().columns, end='\r')
            return energy
        print(energy, steps, end='\r')
        for a, amp in enumerate(state):
            if amp.state == State.DONE:
                continue
            if amp.state == State.IN_HALLWAY:
                try:
                    used, moved_amp = move_to_room(amp, board)
                except AmphException:
                    pass
                else:
                    moved_state = list(state)
                    moved_state[a] = moved_amp
                    queue.put((energy+used, steps+1, tuple(moved_state)))
            elif amp.state == State.START:
                for used, moved_amp in move_to_hallway(amp, board):
                    moved_state = list(state)
                    moved_state[a] = moved_amp
                    queue.put((energy+used, steps+1, tuple(moved_state)))
        board.remove_amps()

    raise NotImplementedError


def part2(lines):
    amphipods, spaces = lines[:]
    unfolded = list()
    for species, position in amphipods:
        if position.real > 2:
            unfolded.append((species, position+2))
        else:
            unfolded.append((species, position))
    additional = (
        (Species.DESERT, 3+3j),
        (Species.DESERT, 4+3j),
        (Species.COPPER, 3+5j),
        (Species.BRONZE, 4+5j),
        (Species.BRONZE, 3+7j),
        (Species.AMBER, 4+7j),
        (Species.AMBER, 3+9j),
        (Species.COPPER, 4+9j),
    )
    unfolded.extend(additional)
    for c, r in product((3, 5, 7, 9), (4, 5)):
        spaces.add(complex(r, c))
    return part1((unfolded, spaces))


def parse(lines):
    spaces = set()
    amphipods = []
    for r, row in enumerate(lines.splitlines()):
        for c, char in enumerate(row):
            if char == '#' or char == ' ':
                continue
            point = complex(r, c)
            spaces.add(point)
            if char in ('A', 'B', 'C', 'D'):
                amphipods.append((Species.get_species(char), point))
    return amphipods, spaces


TEST = """#############
#...........#
###B#C#B#D###
  #A#D#C#A#
  #########"""

SIMPLE = """#############
#...........#
###B#A#C#D###
  #A#B#C#D#
  #########"""

if __name__ == "__main__":
    LINES = parse(get_input(day=23, year=2021))
    test = parse(TEST)

    assert part1(parse(SIMPLE)) == 46
    assert part1(test) == 12521
    print(f"Part 1: {part1(LINES)}")

    assert part2(test) == 44169
    print(f"Part 2: {part2(LINES)}")
