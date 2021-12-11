from collections import defaultdict
from copy import deepcopy
from dataclasses import dataclass
from functools import reduce
from pprint import pprint

def print_map(m):
    """
    prints a 2d array with None represented as: .
    ....
    .11.
    .22.
    ....
    """
    map_formatted = [[cell if cell is not None else "." for cell in row] for row in m]
    for row in map_formatted:
        print(''.join(map(str, row)))


@dataclass
class Point:
    x: int
    y: int

input_file = open('input/day11_test', 'r')
octopus_map = [[None, *[int(i) for i in line], None] for line in input_file.read().splitlines()]
input_file.close()
octopus_map = [
    [None for i in range(len(octopus_map[0]))],
    *octopus_map,
    [None for i in range(len(octopus_map[0]))],
] # pad octopus_map with a border of None
# this way we don't have to worry about edges or corners, there will be no IndexErrors
print_map(octopus_map)