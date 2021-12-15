from queue import PriorityQueue
from pprint import pprint

input_file = open('input/day15_full', 'r')

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
        for neighbor in graph[current_vertex][1:]:
            risk = graph[neighbor][0]
            if neighbor not in visited:
                old_cost = D[neighbor]
                new_cost = D[current_vertex] + risk
                if new_cost < old_cost:
                    pq.put((new_cost, neighbor))
                    D[neighbor] = new_cost
    return D

end = len(graph.keys()) - 1
res = dijkstra(graph, 0)[end]
print(res)