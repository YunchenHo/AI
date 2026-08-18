import csv
import sys # to avoid hitting recursion limit, but I use iterative DFS with stack

from bfs import execution_time

edgeFile = 'edges.csv'
_graph = None


def _load_graph():
    global _graph
    if _graph is not None:
        return _graph

    graph = {}
    with open(edgeFile, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            start = int(row["start"])
            end = int(row["end"])
            distance = float(row["distance"])
            graph.setdefault(start, []).append((end, distance))
            graph.setdefault(end, [])

    _graph = graph
    return _graph


# DFS is a pathfinding algorithm that explores as far as possible along each branch
# but it does not guarantee to find the path with the fewest edges or the shortest total distance
def dfs(start, end):

    if start == end:
            return [start], 0.0, 1

    graph = _load_graph()
    sys.setrecursionlimit(max(sys.getrecursionlimit(), len(graph) + 100))
    # increase recursion limit, but my DFS is iterative (using stack)

    stack = []  # DFS uses stack (LIFO)
    visited = set()
    parent = {}
    
    path = []
    path_reversed = []

    total_distance = 0.0
    num_visited = 0

    stack.append(start)
    visited.add(start)
    parent[start] = None

    while stack: # stack is not empty, keep doing DFS
        current = stack.pop() # LIFO
        num_visited += 1
        
        if current == end: # found the end node, stop DFS, it may not be the optimal path
            break

        for neighbor, distance in graph.get(current, []):
            if neighbor not in visited:
                visited.add(neighbor)
                parent[neighbor] = current
                stack.append(neighbor) 
       
    if end in parent:           
        while current is not None:
            path_reversed.append(current)
            previous = parent[current]
            if previous is not None:
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


if __name__ == "__main__":
    # Public case 1 in current dataset.
    path, dist, num_visited = dfs(2773409914, 1079387396)
    exec_time = execution_time(dfs, 2773409914, 1079387396)
    # path, dist, num_visited = dfs(2773409914, 2773409914)
    print(f'The number of path nodes: {len(path)}')
    print(f'Total distance of path: {dist}')
    print(f'The number of visited nodes: {num_visited}')
    print(f'Execution time: {exec_time}')
