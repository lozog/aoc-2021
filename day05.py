from dataclasses import dataclass
from functools import reduce
from pprint import pprint
import re

MAP_LENGTH = 1000 # assuming the grid is MAP_LENGTH x MAP_LENGTH


@dataclass
class Point:
    x: int
    y: int


@dataclass
class Line:
    start: Point
    end: Point


def transpose(matrix):
    return list(zip(*matrix))


def read_vents_from_file(file: str):
    input_file = open(file, 'r')
    data = input_file.read().splitlines()

    vents = []

    for line_input in data:
        # regex for x,y -> x2,y2
        res = re.search("([0-9]+\,[0-9]+)\ \-\>\ ([0-9]+\,[0-9]+)", line_input)

        start_coords = res.group(1).split(",")
        start_point = Point(x=int(start_coords[0]), y=int(start_coords[1]))
        end_coords = res.group(2).split(",")
        end_point = Point(x=int(end_coords[0]), y=int(end_coords[1]))

        line = Line(start=start_point, end=end_point)
        vents.append(line)

    input_file.close()
    return vents


def print_matrix(matrix):
    for row in transpose(matrix):
        for char in row:
            if char == 0:
                char = "."
            print(char, end="")
        print()


def is_diagonal(line: Line):
    return not (line.start.x == line.end.x or line.start.y == line.end.y)


def find_points_in_line(line):
    points_in_line = []

    if line.start.x == line.end.x:
        # horizontal
        start_y = min(line.start.y, line.end.y)
        end_y = max(line.start.y, line.end.y)
        points_in_line = [*points_in_line, *[Point(line.start.x, y) for y in range(start_y, end_y + 1)]]

    if line.start.y == line.end.y:
        # vertical
        start_x = min(line.start.x, line.end.x)
        end_x = max(line.start.x, line.end.x)
        points_in_line = [*points_in_line, *[Point(x, line.start.y) for x in range(start_x, end_x + 1)]]

    return points_in_line


vents = read_vents_from_file('input/day05_test')
# pprint(vents)

vent_map = [
    [0 for i in range(0, MAP_LENGTH)]
    for i in range(0, MAP_LENGTH)
]

for vent in vents:
    if not(is_diagonal(vent)):
        points_in_line = find_points_in_line(vent)

        for point in points_in_line:
            vent_map[point.x][point.y] += 1


# print_matrix(vent_map)

dangerous_points = sum(
    [
        sum([1 for item in row if item >= 2]) 
        for row in vent_map
    ]
)
print(f"p1: {dangerous_points}")