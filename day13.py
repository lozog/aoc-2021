from dataclasses import dataclass
from copy import deepcopy
from pprint import pprint

@dataclass
class Point:
    x: int
    y: int
    def __repr__(self):
        return f"{self.x}, {self.y}"

@dataclass
class Fold:
    dim: str
    value: int
    def __repr__(self):
        return f"{self.dim}={self.value}"

def transpose(matrix):
    return list(map(list, zip(*matrix)))

def parse_file(file: str):
    input_file = open(file, 'r')
    # data = input_file.read()

    dots = []
    folds = []
    dot_coord_section = True
    max_x = 0
    max_y = 0
    while True:
        line = input_file.readline()
        if not line:
            break
        line = line.strip()
        if line == "":
            dot_coord_section = False
            continue

        if dot_coord_section:
            coords = line.split(",")
            # y,x
            dot = Point(x=int(coords[0]), y=int(coords[1]))
            max_x = max(dot.x, max_x)
            max_y = max(dot.y, max_y)
            dots.append(dot)
        else:
            fold_input = line.split()[2].split("=")
            fold = Fold(dim = fold_input[0], value = int(fold_input[1]))
            folds.append(fold)
            

    input_file.close()
    return dots, folds, max_x, max_y

def print_matrix(matrix):
    for row in transpose(matrix):
        for dot in row:
            char = "."
            if dot is not None:
                char = "#"
            print(char, end="")
        print()

# print_matrix(dot_map)
# print()

def merge_matrices(matrix1, matrix2):
    # assumes matrices are same size
    for x, row in enumerate(matrix1):
        for y, dot in enumerate(row):
            if matrix2[x][y] is None:
                matrix2[x][y] = dot
    return matrix2


dots, folds, max_x, max_y = parse_file("input/day13_full")

# pprint(dots)
# pprint(folds)
# print(max_x)
# print(max_y)

dot_map = [
    [None for y in range(max_y+1)]
    for x in range(max_x+1)
]

for dot in dots:
    dot_map[dot.x][dot.y] = dot

for fold in folds:
    value = fold.value
    # print(fold)
    if fold.dim == "x":
        left = dot_map[:value]
        right = dot_map[value+1:]
        right = right[::-1]
        # right=dot_map[value+1:]
        # print_matrix(left)
        # print()
        # print_matrix(right)
        dot_map = merge_matrices(left, deepcopy(right))
    else:
        transposed_map = transpose(dot_map)
        top = transposed_map[:value]
        bottom = reversed(transposed_map[value+1:])
        top = transpose(top)
        bottom = transpose(bottom)
        
        dot_map = merge_matrices(top, deepcopy(bottom))

        # print_matrix(top)
        # print()
        # print_matrix(bottom)
        # print()
        # print_matrix(dot_map)
    # break # uncomment for p1
print_matrix(dot_map)

res = sum([sum([1 for dot in row if dot is not None]) for row in dot_map])
print(res)