import csv
import heapq

from bfs import execution_time

edgeFile = 'edges.csv'
heuristicFile = 'heuristic.csv'
_graph = None
_heuristics = None
_max_speed_mps = None


def _load_graph():
    global _graph, _max_speed_mps
    if _graph is not None:
        return _graph

    graph = {}
    max_speed_mps = 0.0
    with open(edgeFile, newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            start = int(row['start'])
            end = int(row['end'])
            distance = float(row['distance'])
            speed_kmh = float(row['speed limit'])
            speed_mps = speed_kmh * 1000.0 / 3600.0 # turn to m/s

            if speed_mps > 0.0:
                travel_time = distance / speed_mps  
                # the cost is changed to time instead of distance, cost = time = distance / speed
                graph.setdefault(start, []).append((end, travel_time))
                if speed_mps > max_speed_mps:
                    max_speed_mps = speed_mps
            graph.setdefault(end, [])

    _graph = graph
    _max_speed_mps = max_speed_mps  # save global max speed for heuristic 
    return _graph


def _load_heuristics():
    global _heuristics
    if _heuristics is not None:
        return _heuristics

    heuristics = {}
    with open(heuristicFile, newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            node = int(row['node'])
            heuristics[node] = {int(k): float(v) for k, v in row.items() if k != 'node' and v}

    _heuristics = heuristics
    return _heuristics


def astar_time(start, end):
    
    if start == end:
            return [start], 0.0, 1
    
    graph = _load_graph()
    heuristics = _load_heuristics()
    minheap = []
    parent = {}
    g = {}
    h = {}
    f = {}
    
    path = []
    path_reversed = []
    
    total_time = 0.0
    num_visited = 0

    parent[start] = None
    g[start] = 0.0
    h[start] = heuristics[start][end] / _max_speed_mps 
    # the global highest speed → the shortest possible time from n to goal, ensures h(n) is admissible
    f[start] = g[start] + h[start]
    heapq.heappush(minheap, (f[start], g[start], start))

    while minheap:
        f_cost, g_cost, current = heapq.heappop(minheap)
        # first pop up the smallest f_cost entry
        
        if g_cost > g[current]:
            continue

        num_visited += 1
        
        if current == end:
            break

        for neighbor, travel_time in graph.get(current, []):
            new_cost = g_cost + travel_time # the new actual time cost
            if neighbor in g and new_cost >= g[neighbor]: 
                # if this path to neighbor is worse than the known best, skip
                continue
            else:
                g[neighbor] = new_cost
                h[neighbor] = heuristics[neighbor][end] / _max_speed_mps
                f[neighbor] = g[neighbor] + h[neighbor]
                parent[neighbor] = current
                heapq.heappush(minheap, (f[neighbor], g[neighbor], neighbor))

    if end in parent:           
        while current is not None:
            path_reversed.append(current)
            previous = parent[current]
            current = previous
        
        while path_reversed:
            node = path_reversed.pop()
            path.append(node) 
        
        total_time = g[end] # the shortest time is g[end]
    
    elif end not in parent:
        return [], float("inf"), num_visited 

    return path, total_time, num_visited


if __name__ == '__main__':
    # Public case 1 in current dataset.
    path, time, num_visited = astar_time(2773409914, 1079387396)
    exec_time = execution_time(astar_time, 2773409914, 1079387396)
    # path, time, num_visited = astar_time(2773409914, 2773409914)
    print(f'The number of path nodes: {len(path)}')
    print(f'Total second of path: {time}')
    print(f'The number of visited nodes: {num_visited}')
    print(f'Execution time: {exec_time}')
