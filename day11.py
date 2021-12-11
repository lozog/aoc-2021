from collections import defaultdict
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
    map_formatted = [[octo.energy if octo is not None else "." for octo in row] for row in m]
    # map_formatted = [[octo.last_flash if octo is not None and octo.last_flash else "." for octo in row] for row in m]
    for row in map_formatted:
        print(''.join(map(str, row)))


@dataclass
class Octo:
    x: int
    y: int
    energy: int
    last_flash: int
    def __str__(self):
        return f"{self.x} {self.y} {self.energy} {self.last_flash}"

input_file = open('input/day11_full', 'r')
octopus_map = [
    [None, *[
        Octo(x=i+1, y=j+1, energy=int(energy), last_flash=None) for j, energy in enumerate(line)
    ], None] 
    for i, line in enumerate(input_file.read().splitlines())
]
input_file.close()
octopus_map = [
    [None for i in range(len(octopus_map[0]))],
    *octopus_map,
    [None for i in range(len(octopus_map[0]))],
] # pad octopus_map with a border of None
# this way we don't have to worry about edges or corners, there will be no IndexErrors
print_map(octopus_map)
print()

def flash(octo, step, octo_map):
    octo.last_flash = step
    octo.energy = 0
    # print(f"{octo} flashes")
    i = octo.x
    j = octo.y
    neighbour_coords = [
        octo_map[i-1][j-1],
        octo_map[i-1][j],
        octo_map[i-1][j+1],

        octo_map[i][j-1],
        octo_map[i][j+1],

        octo_map[i+1][j-1],
        octo_map[i+1][j],
        octo_map[i+1][j+1],
    ]

    # increment all neighbours, flashing if necessary
    flash_count = 0
    for n in neighbour_coords:
        if (
            n is not None
            and n.last_flash != step
        ):
            n.energy += 1
            if n.energy > 9:
                flash_count += flash(n, step, octo_map)
    return flash_count + 1
            

def day11(num_steps, octo_map):
    flash_count = 0
    for step in range(num_steps):

        # increment every octo
        for row in octo_map:
            for octo in row:
                if octo is not None:
                    octo.energy += 1


        # every octo over 9 flashes
        for i, row in enumerate(octo_map):
            for j, octo in enumerate(row):
                if octo is not None and octo.energy > 9:
                    flash_count += flash(octo, step, octo_map)

        num_flashing_octos = sum(
            [
                1
                for row in octo_map
                for octo in row
                if octo is not None and octo.last_flash == step
            ]
        )
        # print(f"step {step+1} # flashing: {num_flashing_octos}")

        if num_flashing_octos == 100:
            print(f"all octopus flash on step {step+1}")
            break

        # print(f"step {step+1}")
        # print_map(octo_map)
    print(f"flash count: {flash_count}")
    return    

day11(1000, octopus_map)