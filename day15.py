from pprint import pprint

input_file = open('input/day15_test', 'r')

graph = dict()
line_length = None
for x, line in enumerate(input_file.read().splitlines()):
    line_length = len(line) # assume square grid
    for y, char in enumerate(line):
        cur_node_index = x*line_length + y
        # print(x, y, char, cur_node_index)
        graph[cur_node_index] = [int(char)]
        if x+1 < line_length:
            graph[cur_node_index].append((x+1)*line_length + y)
        if y+1 < line_length:
            graph[cur_node_index].append(x*line_length + (y+1))

input_file.close()
# pprint(graph)
# print()

def lowest_risk_path(start, end, graph):
    if start == end:
        return [end], 0
    
    path_a, risk_a = lowest_risk_path(graph[start][1], end, graph)
    risk_b = None
    if len(graph[start]) > 2:
        path_b, risk_b = lowest_risk_path(graph[start][2], end, graph)

    if risk_b is None or risk_a < risk_b:
        return [start, *path_a], risk_a + graph[start][0]
    else:
        return [start, *path_b], risk_b + graph[start][0]

path, risk = lowest_risk_path(0, (line_length**2)-1, graph)
# print()
# print(f"path: {path}")
print(f"risk: {risk}")
# print()

# for node in path:
#     # print(node)
#     print(graph[node][0])