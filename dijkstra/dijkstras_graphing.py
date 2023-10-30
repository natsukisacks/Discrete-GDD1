# Visualizing with code from Sohum
import matplotlib.pyplot as plt
import networkx as nx

# Create a sample graph using networkx
G = nx.Graph()

# Adding nodes (locations)
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
G.add_nodes_from(nodes)

# Adding edges with weights (paths and their costs)
edges = [
    ("New York", "Tokyo", 5),
    ("New York", "London", 4),
    ("Tokyo", "Berlin", 1),
    ("Tokyo", "Cork", 3),
    ("Cork", "Sicily", 5),
    ("Cork", "Athens", 4),
    ("Athens", "Sicily", 1),
    ("Rome", "Berlin", 2),
    ("Rome", "Athens", 2),
]

G.add_weighted_edges_from(edges)

color_map = [
    "green",
    "lightblue",
    "lightblue",
    "lightblue",
    "lightblue",
    "lightblue",
    "lightblue",
    "lightblue",
]
edges_color_map = [
    "black",
    "black",
    "black",
    "black",
    "black",
    "black",
    "black",
    "black",
    "black",
]


# Drawing the graph
pos = nx.circular_layout(G, scale=1)
nx.draw(
    G,
    pos,
    with_labels=True,
    node_size=2000,
    node_color=color_map,
    edge_color=edges_color_map,
    font_size=15,
)
labels = nx.get_edge_attributes(G, "weight")
nx.draw_networkx_edge_labels(G, pos, edge_labels=labels, font_size=12)

plt.title("Traveling the Northeast")
plt.show()
