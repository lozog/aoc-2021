import re

input_file = open('input/day21_full', 'r')
lines = input_file.read().splitlines()
input_file.close()

players = []
for line in lines:
    res = re.search("Player [0-9]+ starting position: ([0-9]+)", line)
    players.append(int(res.group(1)))

END_SCORE = 1000

print(players)
# array of players. values are the player's position
# players = [4, 8]
scores = [0 for player in players]

turn = 0
dice_roll_count = 0
player = 0
while not any( filter(lambda x: x >= END_SCORE, scores) ) :
    if player == len(players):
        player = 0
    # print(player)
    rolls = [dice_roll_count % 100 + i + 1 for i in range(3)]
    dice_roll_count += 3

    players[player] += sum(rolls)
    while players[player] > 10:
        players[player] -= 10
    # print(players[player])
    scores[player] += players[player]
    player += 1


print(players)
print(scores)
loser_score = list(filter(lambda x: x < END_SCORE, scores))[0]

res = loser_score * dice_roll_count
print(res)