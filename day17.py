from dataclasses import dataclass
from pprint import pprint
import re
from scipy.optimize import minimize

@dataclass
class Point:
    x: int
    y: int

input_file = open("input/day17_full", 'r')
target = input_file.readline().strip()
input_file.close()
res = re.search("target area: x=(-?[0-9]+)\.\.(-?[0-9]+), y=(-?[0-9]+)\.\.(-?[0-9]+)", target)

x_min = int(res.group(1))
x_max = int(res.group(2))
y_min = int(res.group(3))
y_max = int(res.group(4))

# print(x_min, x_max, y_min, y_max)

def probe(x_vel, y_vel):
    # print(f"{x_vel} {y_vel}")
    
    pos = Point(0, 0)
    max_height = -1

    while True:
        pos.x += x_vel
        pos.y += y_vel
        max_height = max(max_height, pos.y)
        x_vel = max(0, x_vel - 1)
        y_vel -= 1
        # print(f"{pos.x} {pos.y}")

        if (
            pos.x >= x_min
            and pos.x <= x_max
            and pos.y >= y_min
            and pos.y <= y_max
        ):
            # print("hit!")
            break
        
        if (
            pos.x > x_max
            or pos.y < y_min
        ):
            # print("miss!")
            return -1
            break
    return max_height

# brute force
# range of guesses to find max height within
x_vel_min = -50
x_vel_max = 200
y_vel_min = -200
y_vel_max = 200

max_heights = []
for x_vel in range(x_vel_min, x_vel_max):
    for y_vel in range(y_vel_min, y_vel_max):
        res = probe(x_vel, y_vel)
        # print(f"{x_vel} {y_vel} {res}")
        max_heights.append([res, x_vel, y_vel])

print(max([i[0] for i in max_heights]))
