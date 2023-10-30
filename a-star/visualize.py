"""
Visualize path finding on map data.
"""
import osmnx as ox
import networkx as nx
import geopandas as gpd
import matplotlib.pyplot as plt
import shapely
from functools import reduce
from collections import defaultdict

IMAGE_DIR = "./frames/"


def make_boundary_info_dict(boundaries, features_tags):
    """
    Get information about boundaries such as GDFs and buildings.
    """
    boundaries_info = defaultdict(dict)
    for place, color in boundaries.items():
        boundaries_info[place]["color"] = color
        boundaries_info[place]["gdf"] = ox.geocode_to_gdf(place)
        boundaries_info[place]["features"] = ox.features.features_from_place(
            place, features_tags
        )
    return boundaries_info


def make_combined_boundaries_gdf(boundaries_info):
    """
    Make a combined geodataframe from a boundaries info dict.
    """
    return reduce(
        lambda x, y: x.overlay(y, how="union"),
        (info["gdf"] for info in boundaries_info.values()),
    )


def make_graph_from_gdf(combined_gdf):
    """
    Make a road network graph from a geodataframe.
    """
    combined_polygon = shapely.unary_union(combined_gdf.geometry)

    # Get network graph
    graph = ox.graph.graph_from_polygon(combined_polygon)
    # Make undirectioned
    undirected = ox.utils_graph.get_undirected(graph)
    # Remove multi-edges
    # return ox.utils_graph.get_digraph(graph)
    return undirected


def get_unvisited(graph, start_node, algo="astar"):
    """
    Get set of unvisited nodes from a graph.

    Args:
        graph: A graph to get nodes from.
        start_node: Unvisited nodes are relative to this start point.

    Returns: A set of ints representing unvisited nodes.
    """
    param_visited = f"{algo}_visited_{start_node}"
    return {
        node
        for node, visited in dict(
            graph.nodes(data=param_visited, default=False)
        ).items()
        if not visited
    }


def get_tree_edges(graph, start_node, algo="astar"):
    """
    Get set of edges for the current Dijkstra tree.

    Args:
        graph: A graph to get Dijkstra tree edges from.
        start_node: Unvisited nodes are relative to this start point.
    """
    param_path = f"{algo}_path_{start_node}"
    paths = {
        path for _, path in dict(graph.nodes(data=param_path)).items() if path != None
    }

    edges = set()
    for path in paths:
        cur_edges = set(zip(path[:-1], path[1:]))
        edges = edges.union(cur_edges)
    return edges


def astar_get_current_node(graph, start_node, heuristic, algo="astar"):
    """
    Find next node to process.

    This node has the smallest combined known_path + heuristic score,
    where the heuristic function estimates the distance from a node to
    the destination.
    """
    param_dist = f"{algo}_distaince_{start_node}"

    def combined_score(node):
        known_distance = graph.nodes[node].get(param_dist, float("inf"))
        return known_distance + heuristic(node)

    unvisited = list(get_unvisited(graph, start_node, algo=algo))
    best_node = unvisited[0]
    for node in unvisited:
        if combined_score(node) < combined_score(best_node):
            best_node = node
    return best_node


def astar_init(graph, start_node, algo="astar"):
    """
    Initialize graph for A*
    """
    param_dist = f"{algo}_distaince_{start_node}"
    param_path = f"{algo}_path_{start_node}"

    graph.nodes[start_node][param_dist] = 0
    graph.nodes[start_node][param_path] = (start_node,)


def astar_iteration(graph, start_node, heuristic, algo="astar"):
    """
    Do one iteration of A* algorithm on a graph.

    Function is written in a way that stores A* paths and distances for
    different start nodes, so you don't need to use a fresh graph to find paths
    from a different start node.

    Args:
        graph: Graph representing road/path network.
        start_node: Start point for A* algorithm.
        heuristic: Heuristic function, needs to take a node as an argument and
            return an estimated distance.
        algo: A string to use for names in the node parameters. If using a
            heuristic function that always returns 0 for example, you can call
            this "dijkstra".

    Returns: True if no work was done (tree is solved). False otherwise.
    """
    param_dist = f"{algo}_distaince_{start_node}"
    param_path = f"{algo}_path_{start_node}"
    param_visited = f"{algo}_visited_{start_node}"

    unvisited = get_unvisited(graph, start_node, algo=algo)
    if len(unvisited) == 0:
        return True

    node_shortest = astar_get_current_node(graph, start_node, heuristic, algo=algo)
    len_shortest = graph.nodes[node_shortest].get(param_dist, float("inf"))

    # Process adjacent nodes
    for node_cur, avail_connections in graph.adj[node_shortest].items():
        if node_cur not in unvisited:
            continue

        # Unfortunately, the plot provided with osmnx doesn't work if it's not
        # a multigraph. So, we can deal with this by picking the shortest of
        # all available edges.
        edge_shortest_len = min(edge["length"] for edge in avail_connections.values())

        # Calculate distance to node through the current node, replace if shorter
        node_len_to = len_shortest + edge_shortest_len
        if node_len_to < graph.nodes[node_cur].get(param_dist, float("inf")):
            node_cur_dict = graph.nodes[node_cur]
            node_cur_dict[param_dist] = node_len_to
            node_cur_dict[param_path] = graph.nodes[node_shortest][param_path] + (
                node_cur,
            )
    # Mark node we are processing as visited
    graph.nodes[node_shortest][param_visited] = True
    return False


def visualize_map(graph, boundaries_info):
    """
    Visualize the graph.

    Args:
        graph: A networkx graph
        boundaries_info: A dict of string->dict, where strings represent areas
            defining network boundaries and the dict has information about it.

    Returns:
        Matplotlib fig and ax.
    """
    fig, ax = ox.plot_graph(graph, show=False, close=False)
    for place, info in boundaries_info.items():
        if "color" not in info:
            info["color"] = "blue"
        if "gdf" in info:
            ax = info["gdf"].plot(ax=ax, alpha=0.5, color=info["color"])

        if "features" in info:
            ax = info["features"].plot(ax=ax, color="gray")
    return fig, ax


def visualize_node(fig, ax, graph, node, size=25, color="red", zorder=10):
    """
    Plot node on map axis.
    """
    node_dict = graph.nodes[node]
    ax.scatter(node_dict["x"], node_dict["y"], color=color, s=size, zorder=zorder)
    return fig, ax


def visualize_tree(fig, ax, graph, tree_edges, color="red", weight=2, zorder=5):
    """
    Visualize the traversal tree of algorithm on map axis.
    """
    for n0, n1 in tree_edges:
        xs = (graph.nodes[n0]["x"], graph.nodes[n1]["x"])
        ys = (graph.nodes[n0]["y"], graph.nodes[n1]["y"])
        ax.plot(xs, ys, color=color, linewidth=weight, zorder=zorder)
    return fig, ax


def visualize_path_to_node(
    fig, ax, graph, start_node, end_node, algo="astar", color="red", weight=4, zorder=7
):
    """
    Visualize path up to node.
    """
    param_path = f"{algo}_path_{start_node}"
    path_nodes = graph.nodes[end_node][param_path]
    xs = [graph.nodes[n]["x"] for n in path_nodes]
    ys = [graph.nodes[n]["y"] for n in path_nodes]
    # That's a list of nodes...
    ax.plot(xs, ys, color=color, linewidth=weight, zorder=zorder)
    return fig, ax


def dist_to_node_func(graph, dest_node):
    """
    Make a function that takes a node as an argument, and returns the distance
    to dest_node passed in.

    Used to build heuristic for A*.
    """
    dest_dict = graph.nodes[dest_node]
    dest_x = dest_dict["x"]
    dest_y = dest_dict["y"]

    def distance_to_dest(node):
        n_dict = graph.nodes[node]
        nx = n_dict["x"]
        ny = n_dict["y"]
        return ox.distance.great_circle(dest_y, dest_x, ny, nx)

    return distance_to_dest


def animate_astar(
    graph, boundaries_info, start_node, dest_node, heuristic=None, algo="astar"
):
    """
    Animate A* algorithm.

    Dumps a bunch of PNG files into IMAGE_DIR.

    Args:
        graph: A road network as an NX object
        boundaries_info: Information about map boundaries to color.
        start_node: start node as a (y, x) tuple.
        dest_node: destination node as a (y, x) tuple.
        heuristic: Optional heuristic to use. If not specified, defaults
            great circle distance between two nodes.
    """

    def draw():
        fig, ax = visualize_map(graph, boundaries_info)

        edges = get_tree_edges(graph, start_node, algo=algo)
        fig, ax = visualize_tree(fig, ax, graph, edges, color="red")

        fig, ax = visualize_node(fig, ax, graph, start_node, color="orange", size=30)
        fig, ax = visualize_node(fig, ax, graph, dest_node, color="orange", size=30)

        current = astar_get_current_node(graph, start_node, heuristic, algo=algo)
        fig, ax = visualize_node(fig, ax, graph, current, color="pink", size=50)
        return fig, ax

    if heuristic is None:
        heuristic = dist_to_node_func(graph, dest_node)

    astar_init(graph, start_node, algo=algo)

    iteration = 0

    # Is this efficient, no. Does it work, yes.
    while dest_node in get_unvisited(graph, start_node, algo=algo):
        fig, ax = draw()
        fig_name = f"{algo}_{iteration:05}.png"
        fig_path = IMAGE_DIR + fig_name
        # plt.show()
        plt.savefig(fig_path)
        plt.close()
        astar_iteration(graph, start_node, heuristic, algo=algo)
        iteration += 1

    # Show final result
    fig, ax = draw()
    fig, ax = visualize_path_to_node(
        fig, ax, graph, start_node, dest_node, algo=algo, color="orange"
    )
    fig_name = f"{algo}_{iteration:05}.png"
    fig_path = IMAGE_DIR + fig_name
    plt.savefig(fig_path)


def animate_dijkstra(graph, boundaries_info, start_node, dest_node):
    animate_astar(
        graph,
        boundaries_info,
        start_node,
        dest_node,
        heuristic=lambda _: 0,
        algo="dijkstra",
    )


def animate_olin(animate_func):
    """
    Animate shortest path from Olin East Hall to Babson Olin Hall.
    """
    # All points in lat/lon, not lon/lat

    # East Hall, Olin College
    start_coords = (-71.262337, 42.292514)
    # Babson Olin Hall
    destination_coords = (-71.26717, 42.29967)

    # Areas to make map from (Olin, Babson, Needham, Wellesley, etc)
    # and highlight colors
    boundaries_colors = {"Olin College": "blue", "Babson College": "green"}
    features_tags = {"building": True}

    boundaries_info = make_boundary_info_dict(boundaries_colors, features_tags)
    combined_gdf = make_combined_boundaries_gdf(boundaries_info)
    graph = make_graph_from_gdf(combined_gdf)

    # Get nodes in graph closest to start and destination
    start_node, dest_node = ox.distance.nearest_nodes(
        graph, *zip(*(start_coords, destination_coords))
    )

    animate_func(graph, boundaries_info, start_node, dest_node)


def main():
    """
    Animate both Dijkstra's and A*
    """
    animate_olin(animate_dijkstra)
    animate_olin(animate_astar)


if __name__ == "__main__":
    main()
