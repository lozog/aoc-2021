from collections import defaultdict
from pprint import pprint

input_file = open('input/day12_full', 'r')

graph = defaultdict(lambda: [])
while True:
    edge = input_file.readline()
    if not edge:
        break
    edge = edge.split("-")

    # edge is between node_a and node_b
    node_a = edge[0]
    node_b = edge[1].strip() # strip newline
    graph[node_a].append(node_b)
    graph[node_b].append(node_a)
input_file.close()

graph = dict(graph)
# pprint(graph)

# adapted from https://www.python.org/doc/essays/graphs/
def find_all_paths_p1(graph, start, end, path=[]):
    path = path + [start]
    if start == end:
        return [path]
    if not start in graph:
        return []
    paths = []
    for node in graph[start]:
        if node.isupper() or node not in path: # ignore nodes we've already used
            newpaths = find_all_paths(graph, node, end, path)
            for newpath in newpaths:
                paths.append(newpath)
    return paths

# adapted from https://www.python.org/doc/essays/graphs/
def find_all_paths(graph, start, end, path=[]):
    path = path + [start]

    if start == end:
        return [path]
    if not start in graph:
        return []
    paths = []

    # print(",".join(path))
    small_caves = defaultdict(lambda: 0)
    for node in path:
        if node.islower():
            small_caves[node] += 1
    # print(dict(small_caves))

    for node in graph[start]:
        if (
            node.isupper()
            or node not in path
            or (
                2 not in small_caves.values()
                and small_caves[node] == 1
                and node != "start"
            )
        ):
            newpaths = find_all_paths(graph, node, end, path)
            for newpath in newpaths:
                paths.append(newpath)
    return paths

all_paths = find_all_paths(graph, "start", "end")
res = len(all_paths)
# for path in all_paths:
#     print(",".join(path))
print(f"{res} paths through cave")
