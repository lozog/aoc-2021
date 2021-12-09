from functools import reduce
from pprint import pprint

input_file = open('input/day09_full', 'r')
height_map = [[None, *[int(i) for i in line], None] for line in input_file.read().splitlines()]
input_file.close()
height_map = [
    [None for i in range(len(height_map[0]))],
    *height_map,
    [None for i in range(len(height_map[0]))],
] # pad height_map with a border of None
# this way we don't have to worry about edges or corners, there will be no IndexErrors
# pprint(height_map)

def is_cell_local_min(i, j, cell, height_map):
    neighbours = [
        height_map[i-1][j],
        height_map[i][j-1],
        height_map[i][j+1],
        height_map[i+1][j],
    ]
    neighbours = [n for n in neighbours if n is not None]

    return cell < min(neighbours)
    

local_mins = []
for i, row in enumerate(height_map):
    if i == 0 or i == len(height_map) - 1:
        # skip first and last row, that's just the None border
        continue
    for j, cell in enumerate(row):
        if j == 0 or j == len(row) - 1:
            # skip first and last column
            continue
        if is_cell_local_min(i, j, cell, height_map):
            local_mins.append(cell)

res = sum(local_mins) + len(local_mins)
print(res)