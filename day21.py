from collections import defaultdict
from pprint import pprint
import re

input_file = open('input/day21_test', 'r')
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
END_SCORE = 3
rolls = defaultdict(int)
for i in range(3):
    for j in range(3):
        for k in range(3):
            rolls[i+j+k+3] += 1
rolls = dict(rolls)

print(players)

# 2d array of all possible positions and all possbile scores
# e.g. the value at all_p1_scores[x][y] is the # of universes where p1 has score y at position x after a certain number of turns
all_p0_scores = [[0 for i in range(END_SCORE)] for position in range(10+1)]
all_p1_scores = [[0 for i in range(END_SCORE)] for position in range(10+1)]

all_p0_scores[players[0]][0] = 1
all_p1_scores[players[1]][0] = 1
all_player_scores = all_p0_scores

num_winning_universes = [0 for player in players]
player = 0
while True :
    print(player)
    new_scores = [[0 for i in range(END_SCORE)] for position in range(10+1)]

    for position, scores in enumerate(all_player_scores):
        if position == 0:
            # the game starts counting positions from 1
            continue
        for score, num_at_score in enumerate(scores):
            if num_at_score > 0:
                # print(f"{position} {num_at_score}")
                for roll, roll_count in rolls.items():
                    new_tile = (position + roll - 1) % 10 + 1
                    new_score = score + new_tile
                    print(f"in {roll_count * num_at_score} universes, player {player} ends up on tile {new_tile} with score {new_score}")

                    if new_score >= END_SCORE:
                        # print(f"{position} {roll} {new_tile} {score}")
                        # print(f"player {player} has won in {roll_count * num_at_score} more universes. removing them from play")
                        num_winning_universes[player] += roll_count * num_at_score
                    else:
                        new_scores[new_tile][new_score] = roll_count * num_at_score
                # all_player_scores[position][score] -= num_at_score

    pprint(new_scores)
    if player == 0:
        all_p0_scores = new_scores
        player = 1
        all_player_scores = all_p1_scores
    else:
        all_p1_scores = new_scores
        player = 0
        all_player_scores = all_p0_scores

    if (
        all( [num_at_score == 0 for position in all_p0_scores for num_at_score in position] )
        and all( [num_at_score == 0 for position in all_p1_scores for num_at_score in position] )
    ):
        break
    print(num_winning_universes)


print(num_winning_universes)
# pprint(all_p1_scores)

# print(players)
# print(scores)
# loser_score = list(filter(lambda x: x < END_SCORE, scores))[0]

# res = loser_score * dice_roll_count
# print(res)
