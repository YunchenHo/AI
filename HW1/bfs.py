import csv # read edges.csv
from collections import deque

from tracemalloc import start

edgeFile = 'edges.csv'
_graph = None


def _load_graph():
    global _graph
    if _graph is not None:
        return _graph

    graph = {}
    # graph is adjacency list
    with open(edgeFile, newline='') as f:
        reader = csv.DictReader(f)
         # DictReader will return a dict for each row
         # key is the column name and value is the corresponding value
        for row in reader:
            start = int(row['start'])
            end = int(row['end'])
            distance = float(row['distance'])
            graph.setdefault(start, []).append((end, distance))
            graph.setdefault(end, [])
            # make sure the node end is in the graph 
            # even if it has no outgoing edges, it should still have empty list of neighbors

    _graph = graph
    return _graph


# BFS assures to find the path with the fewest edges
# but not necessarily the shortest total distance
def bfs(start, end):
    
    if start == end:
            return [start], 0.0, 1
    
    graph = _load_graph() # import graph（read from file first, then use cache）
    
    queue = deque() # BFS queue: FIFO
    visited = set() # record visited nodes to avoid repeated cycles
    parent = {} # parent[child] = parent_node, to reconstruct the path at the end

    path_reversed = []
    path = []

    total_distance = 0.0
    num_visited = 0 # record the number of nodes actually dequeued and processed

    queue.append(start)
    visited.add(start)
    parent[start] = None

    while queue:  # keep doing BFS until queue is empty
        current = queue.popleft()
        num_visited += 1
        
        if current == end:  # once we pop the end node from the queue, we can stop BFS
            break

        for neighbor, distance in graph.get(current, []): # sweep all current's neighbors
            if neighbor not in visited:
                visited.add(neighbor)
                parent[neighbor] = current
                # record that neighbor is reached from current
                # this can be used later to reconstruct the path
                queue.append(neighbor) 
                # add neighbor to queue for processing in BFS order
       
    if end in parent: # if end is found (meaning it has a parent record)           
        while current is not None: # from current(= end) to reconstruct the path
            path_reversed.append(current) # first put current node into reversed path
            previous = parent[current] # find current's parent node
            if previous is not None: # if it's not the start node, add the distance of the edge to the total
                for neighbor, distance in graph.get(previous, []):
                    if neighbor == current:
                        total_distance += distance
                        break
            current = previous
        # because parent only records the previous node, not the distance of the edge,
        # so we have to look up the graph to find the distance from previous to current
        
        # make the reverse path into the correct order
        while path_reversed:
            node = path_reversed.pop()
            path.append(node) 
    
    elif end not in parent:
        return [], float("inf"), num_visited 
    
    return path, total_distance, num_visited

def execution_time(a, start, end):
    import time
    start_time = time.perf_counter()
    path, cost, num_visited = a(start, end)
    end_time = time.perf_counter()
    return end_time - start_time

if __name__ == '__main__':
    # Public case 1 in current dataset.
    path, dist, num_visited = bfs(2773409914, 1079387396)
    exec_time = execution_time(bfs, 2773409914, 1079387396)
    # path, dist, num_visited = bfs(2773409914, 2773409914)
    print(f'The number of path nodes: {len(path)}')
    print(f'Total distance of path: {dist}')
    print(f'The number of visited nodes: {num_visited}')
    print(f'Execution time: {exec_time}')