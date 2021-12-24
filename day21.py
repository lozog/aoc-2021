from collections import defaultdict
from functools import lru_cache
import itertools
from pprint import pprint
import re

input_file = open('input/day21_full', 'r')
lines = input_file.read().splitlines()
input_file.close()

# array of players. values are the player's position
players = []
for line in lines:
    res = re.search("Player [0-9]+ starting position: ([0-9]+)", line)
    players.append(int(res.group(1)))

# p1
# END_SCORE = 1000

# print(players)
# scores = [0 for player in players]

# turn = 0
# dice_roll_count = 0
# player = 0
# while not any( filter(lambda x: x >= END_SCORE, scores) ) :
#     if player == len(players):
#         player = 0
#     # print(player)
#     rolls = [dice_roll_count % 100 + i + 1 for i in range(3)]
#     dice_roll_count += 3

#     players[player] += sum(rolls)
#     players[player] = (players[player] - 1) % 10 + 1
#     # print(players[player])
#     scores[player] += players[player]
#     player += 1


# print(players)
# print(scores)
# loser_score = list(filter(lambda x: x < END_SCORE, scores))[0]

# res = loser_score * dice_roll_count
# print(res)


# p2
rolls = defaultdict(int)
for i in range(3):
    for j in range(3):
        for k in range(3):
            rolls[i+j+k+3] += 1
rolls = dict(rolls)

# mostly stolen from reddit
@lru_cache(maxsize=None)
def dirac(p1, p2, p1_score, p2_score, win_score):
    num_wins = [0, 0]
    for roll1 in itertools.product([1,2,3], repeat=3):
        for roll2 in itertools.product([1,2,3], repeat=3):
            p1_ = (p1 + sum(roll1) - 1 ) % 10 + 1
            p1_score_ = p1_score + p1_
            if p1_score_ >= win_score:
                num_wins[0] += 1
                break
            p2_ = (p2 + sum(roll2) - 1) % 10 + 1
            p2_score_ = p2_score + p2_
            if p2_score_ >= win_score:
                num_wins[1] += 1
                continue
            subsequent_wins = dirac(p1_, p2_, p1_score_, p2_score_, win_score)
            num_wins[0] += subsequent_wins[0]
            num_wins[1] += subsequent_wins[1]
    return num_wins

res = dirac(players[0], players[1], 0, 0, 21)

print(res)
