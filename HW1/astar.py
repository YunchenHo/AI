import csv
import heapq

from bfs import execution_time

edgeFile = 'edges.csv'
heuristicFile = 'heuristic.csv'
_graph = None
_heuristics = None
# _graph is the cache of graph data read from edges.csv
# _heuristics is the cache of heuristic data read from heuristic.csv

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


def _load_heuristics():
    global _heuristics
    if _heuristics is not None:
        return _heuristics

    heuristics = {} # heuristics[node][goal] = h(node)
    with open(heuristicFile, newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            node = int(row['node']) # the row is the heuristic data for which node
            heuristics[node] = {int(k): float(v) for k, v in row.items() if k != 'node' and v}

    _heuristics = heuristics
    return _heuristics


# A* use f(n) = g(n) + h(n) to decide which node to expand first
# g(n) = the real distance(start, n)
# h(n) = the estimated distance(n, goal) from heuristic.csv
# f(n) = the total estimated cost of the path from start through n to the goal
# A* guarantees to find the shortest distance path if the heuristic is admissible
def astar(start, end):

    if start == end:
        return [start], 0.0, 1

    graph = _load_graph()
    heuristics = _load_heuristics()
    minheap = []  # put (f_cost, g_cost, node), when f are equal, compare g, then node to find the smallest one 
    parent = {}
    g = {}
    h = {}
    f = {}
    
    path = []
    path_reversed = []
    
    total_distance = 0.0
    num_visited = 0

    parent[start] = None
    g[start] = 0.0
    h[start] = heuristics[start][end]
    f[start] = g[start] + h[start]
    heapq.heappush(minheap, (f[start], g[start], start)) # put start in min-heap

    while minheap:
        f_cost, g_cost, current = heapq.heappop(minheap)
        # will first pop up the smallest f_cost entry
        
        # if this heap entry's g cost is bigger than the known best g[current]
        # this is an old entry, just skip
        if g_cost > g[current]: 
            continue
        
        num_visited += 1
        
        if current == end:
            break

        for neighbor, distance in graph.get(current, []):
            new_cost = g_cost + distance # the new actual cost from start to neighbor through current
            if neighbor in g and new_cost >= g[neighbor]:
                continue
            else:
                g[neighbor] = new_cost
                h[neighbor] = heuristics[neighbor][end]
                f[neighbor] = g[neighbor] + h[neighbor]
                parent[neighbor] = current
                heapq.heappush(minheap, (f[neighbor], g[neighbor], neighbor)) 
                #put the new state into heap, the order of expansion will be decided by f, then g, then node

    if end in parent:           
        while current is not None:
            path_reversed.append(current)
            previous = parent[current]
            current = previous
        
        while path_reversed:
            node = path_reversed.pop()
            path.append(node) 
        
        total_distance = g[end] 
        # the shortest distance is g[end]
        # as f[end] = g[end] + h[end], and h[end] = 0, so f[end] = g[end]
    
    elif end not in parent:
        return [], float("inf"), num_visited 

    return path, total_distance, num_visited

if __name__ == '__main__':
    # Public case 1 in current dataset.
    path, dist, num_visited = astar(2773409914, 1079387396)
    exec_time = execution_time(astar, 2773409914, 1079387396)
    # path, dist, num_visited = astar(2773409914, 2773409914)
    print(f'The number of path nodes: {len(path)}')
    print(f'Total distance of path: {dist}')
    print(f'The number of visited nodes: {num_visited}')
    print(f'Execution time: {exec_time}')
