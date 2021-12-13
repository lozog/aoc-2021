from dataclasses import dataclass
from pprint import pprint

@dataclass
class Point:
    x: int
    y: int
    def __repr__(self):
        return f"{self.x}, {self.y}"

@dataclass
class Fold:
    dim: int
    value: int
    def __repr__(self):
        return f"{self.dim}={self.value}"

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
            dot = Point(x=int(coords[0]), y=int(coords[1]))
            max_x = max(dot.x, max_x)
            max_y = max(dot.y, max_y)
            dots.append(dot)
        else:
            fold_input = line.split()[2].split("=")
            fold = Fold(dim = fold_input[0], value = fold_input[1])
            folds.append(fold)
            

    input_file.close()
    return dots, folds, max_x, max_y

dots, folds, max_x, max_y = parse_file("input/day13_test")

pprint(dots)
pprint(folds)
print(max_x)
print(max_y)