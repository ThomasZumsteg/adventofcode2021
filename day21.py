"""Solution to day 21 of Advent of Code"""

from get_input import get_input
from collections import defaultdict
from itertools import product


class Dice:
    def __init__(self, size):
        self.rolls = 0
        self.size = size

    def roll(self):
        value = (self.rolls % self.size) + 1
        self.rolls += 1
        return value


def part1(players):
    players = list(players)
    scores = [0, 0]
    dice = Dice(100)
    board_size = 10
    done = False
    while not done:
        for p, player in enumerate(players):
            player += dice.roll() + dice.roll() + dice.roll()
            player = ((player - 1) % board_size) + 1
            players[p] = player
            scores[p] += player
            if scores[p] >= 1000:
                done = True
                break
    scores.sort()
    return scores[0] * dice.rolls


def part2(players):
    possible_roles = defaultdict(int)
    for rolls in product(range(1, 4), repeat=3):
        possible_roles[sum(rolls)] += 1
    board_size = 10
    max_score = 21
    outcomes = defaultdict(lambda: {
        0: defaultdict(int),
        1: defaultdict(int),
    })
    for player, position in enumerate(players):
        # Times this statue occured, number of rolls, score, player position
        queue = [(1, 0, 0, position)]
        while queue:
            times, n_rolls, score, position = queue.pop()
            outcomes[n_rolls][player][score] += times
            if score >= max_score:
                continue
            for roll, count in possible_roles.items():
                next_position = ((position + roll - 1) % board_size) + 1
                queue.append((
                    times * count,
                    n_rolls + 3,
                    score + next_position,
                    next_position
                ))
    wins = [0, 0]
    for rolls, games in outcomes.items():
        for player, scores in games.items():
            opponent = 0 if player == 1 else 1
            for score, times in scores.items():
                if score < max_score:
                    continue
                opponent_states = games[opponent]
                if player == 0:
                    opponent_states = outcomes[rolls-3][1]
                for opponent_score, count in opponent_states.items():
                    if opponent_score < max_score:
                        wins[player] += count * times
    return max(wins)


def parse(lines):
    lines = lines.splitlines()
    prefix = "Player 1 starting position: "
    assert lines[0].startswith('Player 1 starting position: ')
    assert lines[1].startswith('Player 2 starting position: ')
    assert len(lines) == 2
    return (int(lines[0][len(prefix):]), int(lines[1][len(prefix):]))


TEST = """Player 1 starting position: 4
Player 2 starting position: 8
"""


if __name__ == "__main__":
    LINES = parse(get_input(day=21, year=2021))
    test = parse(TEST)

    assert part1(test) == 739785
    print(f"Part 1: {part1(LINES)}")

    assert part2(test) == 444356092776315
    print(f"Part 2: {part2(LINES)}")
