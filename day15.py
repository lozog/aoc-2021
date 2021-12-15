from pprint import pprint

input_file = open('input/day15_test', 'r')

graph = dict()
line_length = None
for x, line in enumerate(input_file.read().splitlines()):
    line_length = len(line) # assume square grid
    for y, char in enumerate(line):
        cur_node_index = x*line_length + y
        print(x, y, char, cur_node_index)
        graph[cur_node_index] = []
        if x+1 < line_length:
            graph[cur_node_index].append((x+1)*line_length + y)
        if y+1 < line_length:
            graph[cur_node_index].append(x*line_length + (y+1))

input_file.close()
pprint(graph)
