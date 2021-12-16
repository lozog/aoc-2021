from queue import PriorityQueue
from pprint import pprint

input_file = open('input/day15_test', 'r')
lines = input_file.read().splitlines()
input_file.close()

graph = dict()
line_length = None
for x, line in enumerate(lines):
    line_length = len(line) # assume square grid
    for y, char in enumerate(line):
        cur_node_index = x*line_length + y
        # print(x, y, char, cur_node_index)
        graph[cur_node_index] = [int(char)]
        if x+1 < line_length:
            graph[cur_node_index].append((x+1)*line_length + y)
        if y+1 < line_length:
            graph[cur_node_index].append(x*line_length + (y+1))

grid_size = len(graph.keys())
# pprint(graph)

# adapted from https://stackabuse.com/dijkstras-algorithm-in-python/
def dijkstra(graph, start_vertex):
    num_vertices = len(graph.keys())
    visited = []

    # D will hold the lowest risk from start_vertex to every other node
    D = {v:float('inf') for v in range(num_vertices)}
    D[start_vertex] = 0

    pq = PriorityQueue()
    pq.put((0, start_vertex))

    while not pq.empty():
        (dist, current_vertex) = pq.get()
        visited.append(current_vertex)
        # print(len(visited))
        for neighbor in graph[current_vertex][1:]:
            risk = graph[neighbor][0]
            if neighbor not in visited:
                old_cost = D[neighbor]
                new_cost = D[current_vertex] + risk
                if new_cost < old_cost:
                    pq.put((new_cost, neighbor))
                    D[neighbor] = new_cost
    return D

# p1
# end = grid_size - 1
# res = dijkstra(graph, 0)[end]
# print(res)

def print_graph(graph, line_length, full_map_factor):
    for j in range(full_map_factor):
        for row in range(line_length):
            for i in range(full_map_factor):
                for col in range(line_length):
                    print(graph[row*line_length*full_map_factor + col+(line_length*i) + grid_size*full_map_factor*j][0], end="")
            print()

# p2 attempt 1
# full_graph = dict()
# full_map_factor = 5
# full_line_length = line_length * full_map_factor

# for j in range(full_map_factor):
#     for x, line in enumerate(lines):
#         for i in range(full_map_factor):
#             for y, risk in enumerate(line):
#                 cur_node_index = x*(line_length*(full_map_factor)) + y+(line_length*i) + grid_size*full_map_factor*j
#                 full_graph[cur_node_index] = []
#                 new_risk = (int(risk) + i + j) 
#                 if new_risk > 9:
#                     new_risk -= 9
#                 full_graph[cur_node_index].append(new_risk)
#                 # print(x, y, i, j, risk, full_graph[cur_node_index], cur_node_index)
#                 if line_length * j + (x+1) <= full_line_length - 1:
#                     full_graph[cur_node_index].append((x+1)*(line_length*(full_map_factor)) + y+(line_length*i) + grid_size*full_map_factor*j)
#                 if line_length * i + (y+1) <= full_line_length - 1:
#                     full_graph[cur_node_index].append(x*(line_length*(full_map_factor)) + (y+1)+(line_length*i) + grid_size*full_map_factor*j)

# print_graph(full_graph, line_length, full_map_factor)
# pprint(full_graph)

# end = len(full_graph.keys()) - 1
# res = dijkstra(full_graph, 0)[end]
# print(res)

# p2 attempt 2

import numpy as np
import sys
from skimage.graph import route_through_array

np.set_printoptions(linewidth=np.inf, threshold=sys.maxsize)
input_file = open('input/day15_full', 'r')

graph = []
line_length = 0
for line in input_file.read().splitlines():
    line_length = len(line) # assume square
    graph.append([int(char) for char in line])

input_file.close()

graph = np.array(graph)
grid_size = (line_length+1)**2
factor = 5

def f(x, i):
    x += i
    if x > 9:
        x -= 9
    return x

vfunc = np.vectorize(f)

first_tile_row = graph.copy()
for i in range(1, factor):
    new_tile = vfunc(graph, i)
    # print(new_tile)
    first_tile_row = np.concatenate((first_tile_row,new_tile),axis=1)
# print(first_tile_row)

full_graph = first_tile_row.copy()
for j in range(1, factor):
    new_tile = vfunc(first_tile_row, j)
    # print(new_tile)
    full_graph = np.concatenate((full_graph,new_tile),axis=0)

# print(full_graph)

full_length = line_length * factor
res = route_through_array(full_graph, [0, 0], [full_length-1, full_length-1], fully_connected=False)
path = res[0]
# pprint(res[0])
cost = sum([full_graph[node[0]][node[1]] for node in path]) - full_graph[0][0]
print(cost)
# print(res[1])
