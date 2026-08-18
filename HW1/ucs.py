import csv
import heapq
# heapq: Python's min-heap implementation
# used for priority queue in UCS
from turtle import distance

from bfs import execution_time

edgeFile = 'edges.csv'
_graph = None


def _load_graph():
    global _graph
    if _graph is not None:
        return _graph

    graph = {}
    with open(edgeFile, newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            start = int(row['start'])
            end = int(row['end'])
            distance = float(row['distance'])
            graph.setdefault(start, []).append((end, distance))
            graph.setdefault(end, [])

    _graph = graph
    return _graph


# UCS will expand the node with the smallest total cost so far
# if all edge weights are non-negative, UCS guarantees to find the shortest distance path
def ucs(start, end):

    if start == end:
        return [start], 0.0, 1

    graph = _load_graph()
    minheap = [] # minheap will store (cost, node)
    parent = {}
    g = {}
    
    path = []
    path_reversed = []
    
    total_distance = 0.0
    num_visited = 0

    heapq.heappush(minheap, (0.0, start))
     # start in min-heap，the cost is 0
    parent[start] = None
    g[start] = 0.0

    while minheap: # if min-heap is not empty, keep doing UCS
        cost, current = heapq.heappop(minheap) # pop the entry with the smallest cost now
        
        if cost > g[current]: # if this heap entry's cost is bigger than the known best g[current]
            continue # just skip (because we already have a cheaper path to current)
        # Because the same node might be pushed into the heap multiple times,
        # and later we find a shorter path, so the old entry becomes invalid
        
        num_visited += 1
        
        if current == end:
            break

        for neighbor, distance in graph.get(current, []): # sweep all current's neighbors
            new_cost = cost + distance # the new cost from start to reach neighbor through current
            if neighbor in g and new_cost >= g[neighbor]: 
            # if neighbor already has a better or equal path, don't update
                continue
            else:
                g[neighbor] = new_cost
                parent[neighbor] = current
                heapq.heappush(minheap, (new_cost, neighbor)) # put the updated state into heap
                # as the old data won't be removed
                # we need the cost > g[current] check to skip the invalid heap entry
      
    if end in parent:           
        while current is not None:
            path_reversed.append(current)
            previous = parent[current]
            current = previous
        
        while path_reversed:
            node = path_reversed.pop()
            path.append(node) 

        total_distance = g[end] # UCS's shortest distance is g[end]
    
    elif end not in parent:
        return [], float("inf"), num_visited 

    return path, total_distance, num_visited


if __name__ == '__main__':
    # Public case 1 in current dataset.
    path, dist, num_visited = ucs(2773409914, 1079387396)
    exec_time = execution_time(ucs, 2773409914, 1079387396)
    # path, dist, num_visited = ucs(2773409914, 2773409914)
    print(f'The number of path nodes: {len(path)}')
    print(f'Total distance of path: {dist}')
    print(f'The number of visited nodes: {num_visited}')
    print(f'Execution time: {exec_time}')