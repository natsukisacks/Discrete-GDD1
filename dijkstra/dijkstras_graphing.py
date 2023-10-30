# Visualizing with code from Sohum
import matplotlib.pyplot as plt
import networkx as nx

# Create a sample graph using networkx
G = nx.Graph()

# Adding nodes (locations)
nodes = ["MD", "NJ", "CT", "NY", "RI", "MA", "DE"]
G.add_nodes_from(nodes)

# Adding edges with weights (paths and their costs)
edges = [
    ("MD", "NJ", 3),
    ("NJ", "RI", 6),
    ("MD", "RI", 5),
    ("NJ", "CT", 4),
    ("RI", "NY", 1),
    ("NY", "CT", 2),
    ("RI", "MA", 8),
    ("MA", "DE", 7),
    ("CT", "DE", 3),
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
