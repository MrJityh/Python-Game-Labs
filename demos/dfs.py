import sys

def dfs(neighbors, current_node, visited=None):
    if visited is None:
        visited = set()
    visited.add(current_node)

    print(current_node)  # This can be replaced with other processing logic

    for next_node in neighbors[current_node] - visited:
        dfs(neighbors, next_node, visited)
    return visited

if __name__ == '__main__':
    print(f'Name of the graph: {sys.argv[1]}')
    # Example usage
    neighbors = {
        'A': set(['B', 'C']),
        'B': set(['A', 'D', 'E']),
        'C': set(['A', 'F']),
        'D': set(['B']),
        'E': set(['B', 'F']),
        'F': set(['C', 'E'])
    }

    graph = neighbors

    dfs(graph, 'A')