import re

input_file = open("input/day17_full", 'r')
target = input_file.readline().strip()
input_file.close()
# line = "target area: x=20..30, y=-10..-5"
res = re.search("target area: x=(-?[0-9]+)\.\.(-?[0-9]+), y=(-?[0-9]+)\.\.(-?[0-9]+)", target)

x_min = int(res.group(1))
x_max = int(res.group(2))
y_min = int(res.group(3))
y_max = int(res.group(4))

print(x_min, x_max, y_min, y_max)