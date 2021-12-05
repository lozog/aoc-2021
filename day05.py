from dataclasses import dataclass
from functools import reduce
from pprint import pprint
import re

MAP_LENGTH = 1000 # assuming the grid is MAP_LENGTH x MAP_LENGTH


@dataclass
class Point:
    x: int
    y: int
    def __str__(self):
        return f"{self.x}, {self.y}"


@dataclass
class Line:
    start: Point
    end: Point
    def __str__(self):
        return f"{self.start} -> {self.end}"


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


def find_y_on_line(start: Point, end: Point, x: int):
    return int( ((x - start.x) * ((end.y - start.y)/(end.x - start.x))) + start.y )

def find_points_in_line(line: Line):
    points_in_line = []

    if line.start.x == line.end.x:
        # horizontal
        direction = 1 if line.start.y < line.end.y else -1
        new_points = [Point(line.start.x, y) for y in range(line.start.y, line.end.y + direction, direction)]
    elif line.start.y == line.end.y:
        # vertical
        direction = 1 if line.start.x < line.end.x else -1
        new_points = [Point(x, line.start.y) for x in range(line.start.x, line.end.x + direction, direction)]
    else:
        # diagonal
        direction = 1 if line.start.x < line.end.x else -1
        new_points = [Point(x, find_y_on_line(line.start, line.end, x)) for x in range(line.start.x, line.end.x + direction, direction)]
    
    points_in_line = [*points_in_line, *new_points]
    return points_in_line


vents = read_vents_from_file('input/day05_full')
# pprint(vents)

vent_map = [
    [0 for i in range(0, MAP_LENGTH)]
    for i in range(0, MAP_LENGTH)
]

def find_dangerous_points_count(dont_check_for_diagonals):
    for vent in vents:

        if (is_diagonal(vent) and dont_check_for_diagonals):
            continue

        points_in_line = find_points_in_line(vent)

        for point in points_in_line:
            vent_map[point.x][point.y] += 1

    print_matrix(vent_map)

    return sum(
        [
            sum([1 for item in row if item >= 2])
            for row in vent_map
        ]
    )

# print(f"p1: {find_dangerous_points_count(True)}")
print(f"p2: {find_dangerous_points_count(False)}")