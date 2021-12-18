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
            return True # p2
            break
        
        if (
            pos.x > x_max
            or pos.y < y_min
        ):
            # print("miss!")
            return False # p2
            break
    return max_height

# brute force
x_vel_min = 0
x_vel_max = 700
y_vel_min = -500
y_vel_max = 500

max_heights = []
for x_vel in range(x_vel_min, x_vel_max+1):
    for y_vel in range(y_vel_min, y_vel_max+1):
        res = probe(x_vel, y_vel)
        # if res != -1: # p1
        if res == True: # p2
            print(f"{x_vel} {y_vel} {res}")
            max_heights.append([res, x_vel, y_vel])

# print(max([i[0] for i in max_heights]))
pprint(len(max_heights))

