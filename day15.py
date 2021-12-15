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

# p2
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

# attempt 2:
full_map_factor = 5
i = 4
j = 4
new_tile = dict()
for position, node in graph.items():
    new_node = node
    new_risk = node[0] + i + j
    if new_risk > 9:
        new_risk -= 9
    new_node[0] = new_risk
    new_tile[position] = new_node

pprint(new_tile)
print_graph(graph, line_length, 1)

# do this for each of top row and left col
cur_min = float('inf')
end = grid_size - 1
for start_candidate in range(line_length): # each of first row
    res = dijkstra(new_tile, start_candidate)[end]
    if res < cur_min:
        cur_min = res
for row in range(line_length): # first of each col
    res = dijkstra(new_tile, line_length * row)[end]
    if res < cur_min:
        cur_min = res
print(cur_min)
print(2 + 5 + 3 + 2 + 2 + 4 + 1 + 4 + 3 + 1 + 2 + 3 + 3 + 4 + 7 + 9)

res = dijkstra(new_tile, 30)[end]
print(res)
"""
approach 2:
1. take input graph
2. transform it into the bottom right tile
3. calculate the lowest risk path from every position in the first row & col to the end position
4. find the tile adjacent to that. e.g. if lowest path is from a position in the first col, take the tile to the left
5. find the lowest risk path from any position in the first row & col to the position next to the start of the next tile
  5a. ignore the first col if the tile is all the way on the left, ditto the first row if the tile is at the top
6. once you get to the first tile, calculate path from start position
7. add all these together

# this assumes that the shortest path for the last tile will be the same as the shortest path
# when starting from the entire grid, which is not true!
"""
