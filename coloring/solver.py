import random

# Function to add an edge between two nodes in the graph
def add_edge(graph, edge):
    if edge[0] not in graph:
        graph[edge[0]] = []
    if edge[1] not in graph:
        graph[edge[1]] = []
    # Add the second node as a neighbor of the first node and vice versa
    graph[edge[0]].append(edge[1])
    graph[edge[1]].append(edge[0])

# Function to generate a graph from a list of edges
def get_graph(edges):
    graph = {}
    # Add all edges to the graph
    for edge in edges:
        add_edge(graph, edge)
    return graph

# Function to find the next available color for a node
def find_next_color(used):
    color = 0
    # Increment color value until an unused color is found
    while color in used:
        color += 1
    return color

# Function to solve the graph coloring problem randomly
def solve_random(graph, nodes, node_colors):
    Q = nodes.copy()
    random.shuffle(Q)
    while Q:
        node = Q.pop(0)  # Get the next node from the list
        used_colors = set()  # Set to store the colors used by neighbors
        # Check all neighbors of the current node
        for temp in graph[node]:
            if node_colors[temp] != -1:  # If the neighbor has a color
                used_colors.add(node_colors[temp])  # Add the color to the used set
        # Assign the next available color to the current node
        node_colors[node] = find_next_color(used_colors)

# Function to solve the graph coloring problem using a more strategic approach
def solve(graph, nodes, node_colors):
    temp = nodes.copy()  # Create a copy of the nodes list
    while temp:
        array = []
        # Iterate over all nodes in the temp list
        for node in temp:
            used = set()
            # Find the colors used by the neighbors of the node
            for neigh in graph[node]:
                if node_colors[neigh] != -1:
                    used.add(node_colors[neigh])
            # Add the node, number of used colors, and number of neighbors to the array
            array.append((node, len(used), len(graph[node])))
        # Sort nodes by the number of used colors and neighbors (in descending order)
        array.sort(key=lambda x: (x[1], x[2]), reverse=True)
        # Choose the node with the highest number of used colors and neighbors
        node = array[0][0]
        temp.remove(node)  
        # Find the colors used by the neighbors of the node
        used_colors = set(node_colors[neighbor] for neighbor in graph[node] if node_colors[neighbor] != -1)
        # Assign the next available color to the selected node
        node_colors[node] = find_next_color(used_colors)        


def solve_it(input_data):

    lines = input_data.split('\n')
    first_line = lines[0].split()
    node_count = int(first_line[0])
    edge_count = int(first_line[1])

    edges = []
    for i in range(1, edge_count + 1):
        parts = lines[i].split()
        edges.append((int(parts[0]), int(parts[1])))

    nodes = list(set(node for edge in edges for node in edge))
    graph = get_graph(edges)
    node_colors = {node: -1 for node in nodes}

    if len(nodes) < 100:
        best_solution = []
        for _ in range(1000):
            node_colors = {node: -1 for node in nodes}
            solve_random(graph, nodes, node_colors)
            solution = list(node_colors.values())
            if not best_solution or len(set(solution)) < len(set(best_solution)):
                best_solution = solution
        solution = best_solution
    else:
        solve(graph, nodes, node_colors)
        solution = list(node_colors.values())

    output_data = f"{len(set(solution))} 0\n"
    output_data += ' '.join(map(str, solution))

    return output_data

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        with open(file_location, 'r') as input_data_file:
            input_data = input_data_file.read()
        print(solve_it(input_data))
    else:
        print('This test requires an input file. Please select one from the data directory. (i.e. python solver.py ./data/gc_4_1)')
