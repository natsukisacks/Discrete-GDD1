class Graph(object):
    def __init__(self, nodes, init_graph):
        self.nodes = nodes
        self.graph = self.construct_graph(nodes, init_graph)

    def construct_graph(self, nodes, init_graph):
        """
        This method makes sure that the graph is symmetrical.
        If there's a path from node A to B with a value V,
        there needs to be a path from node B to node A with a value V.

        Keys: cities
        Values: dictionaries containing distance to connected cities
        """

        graph = {}
        for node in nodes:
            graph[node] = {}

        graph.update(init_graph)

        for node, edges in graph.items():
            for adj_node, value in edges.items():
                if graph[adj_node].get(node, False) == False:
                    graph[adj_node][node] = value

        return graph

    def get_nodes(self):
        "Returns the nodes of the graph."
        return self.nodes

    def get_outgoing_edges(self, node):
        "Returns the neighbors of a node."
        connections = []
        for out_node in self.nodes:
            if self.graph[node].get(out_node, False) != False:
                connections.append(out_node)
        return connections

    def value(self, node1, node2):
        "Returns the value of an edge between two nodes."
        return self.graph[node1][node2]


def dijkstra_algorithm(graph, start_node):
    """
    Execute Dijkstra's algorithm.

    Parameters:
        graph: instance of the Graph class
        start_node: node from which calculations begin
    """
    # Get a list of all unvisited nodes
    unvisited_nodes = list(graph.get_nodes())

    # Store shortest distance of visiting each node, starting at inf
    shortest_path = {}

    # Store shortest known path to a node found so far
    # i.e. prev_nodes["Berlin"] -> "Oslo"
    prev_nodes = {}

    # Initialize distance inf for all nodes besides source node
    max_value = float("inf")  # sys.maxsize
    for node in unvisited_nodes:
        shortest_path[node] = max_value

    # Initialize starting node's value with 0
    shortest_path[start_node] = 0

    # Execute until all nodes have been visited
    while unvisited_nodes:
        # Find unvisited node with shortest distance
        current_min_node = None
        for node in unvisited_nodes:  # Iterate over the nodes
            if current_min_node == None:
                current_min_node = node
            elif shortest_path[node] < shortest_path[current_min_node]:
                current_min_node = node

        # Retrieve current node's neighbors and update their distances
        neighbors = graph.get_outgoing_edges(current_min_node)
        for neighbor in neighbors:
            new_dist = shortest_path[current_min_node] + graph.value(
                current_min_node, neighbor
            )
            if new_dist < shortest_path[neighbor]:
                shortest_path[neighbor] = new_dist
                # We also update the best path to the current node
                prev_nodes[neighbor] = current_min_node

        # After visiting its neighbors, we mark the node as "visited"
        unvisited_nodes.remove(current_min_node)

    return prev_nodes, shortest_path


def print_result(previous_nodes, shortest_path, start_node, target_node):
    """
    Helper function to print result nicely.
    """
    path = []
    node = target_node

    while node != start_node:
        path.append(node)
        node = previous_nodes[node]

    # Add the start node manually
    path.append(start_node)

    print(
        f"The best path from {start_node} to {target_node} has a value of {shortest_path[target_node]}"
    )
    print(" -> ".join(reversed(path)))


# Initialize nodes. This can be altered depending on the user.
nodes = [
    "New York",
    "Tokyo",
    "Cork",
    "London",
    "Rome",
    "Berlin",
    "Sicily",
    "Athens",
]

init_graph = {}
for node in nodes:
    init_graph[node] = {}

# Instantiate the edges. These inputs can be
# altered depending on what the user wants the graph to be of.
init_graph["New York"]["Tokyo"] = 5
init_graph["New York"]["London"] = 4
init_graph["Tokyo"]["Berlin"] = 1
init_graph["Tokyo"]["Cork"] = 3
init_graph["Cork"]["Sicily"] = 5
init_graph["Cork"]["Athens"] = 4
init_graph["Athens"]["Sicily"] = 1
init_graph["Rome"]["Berlin"] = 2
init_graph["Rome"]["Athens"] = 2

graph = Graph(nodes, init_graph)

# If you change the graph, you must also change the start_node name accordingly.
prev_nodes, shortest_path = dijkstra_algorithm(graph=graph, start_node="New York")

# Uncomment if you just want the shortest path to one node
# print_result(prev_nodes, shortest_path, start_node="New York", target_node="Boston")

for node in nodes:
    print_result(prev_nodes, shortest_path, start_node="New York", target_node=node)
