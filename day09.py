from collections import defaultdict
from copy import deepcopy
from dataclasses import dataclass
from functools import reduce
from pprint import pprint

@dataclass
class Point:
    x: int
    y: int

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
    
def p1():
    local_mins = []
    local_mins_coords = []
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
                local_mins_coords.append(Point(x=i, y=j))

    res = sum(local_mins) + len(local_mins)
    print(f"p1: {res}")
    return local_mins_coords


def flood_fill(i, j, basin_num, height_map, basins):
    if height_map[i][j] is None:
        return
    if basins[i][j] != '':
        return
    if height_map[i][j] < 9:
        basins[i][j] = basin_num
        flood_fill(i+1, j, basin_num, height_map, basins )
        flood_fill(i-1, j, basin_num, height_map, basins )
        flood_fill(i, j-1, basin_num, height_map, basins )
        flood_fill(i, j+1, basin_num, height_map, basins )

def p2():
    local_mins = p1()
    # print(local_mins)
    basins = [["" if cell is not None else None for cell in row] for row in height_map]
    for basin_num, local_min in enumerate(local_mins):
        flood_fill(local_min.x, local_min.y, basin_num, height_map, basins)
    # pprint(basins)

    # flatten, remove all Nones, count each unique 
    basins = [val for row in basins for val in row if val is not None and val != '']
    # print(basins)
    basin_sizes = defaultdict(lambda: 0)
    for point in basins:
        basin_sizes[point] += 1
    basin_sizes = list(basin_sizes.values())
    # print(basin_sizes)

    top_3_basin_sizes = sorted(basin_sizes, reverse=True)[:3]
    # print(top_3_basin_sizes)
    res = reduce(lambda a, b: a*b, top_3_basin_sizes)
    print(f"p2: {res}")


p2()
