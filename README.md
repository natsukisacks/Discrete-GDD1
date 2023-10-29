# Shortest Path Algorithms
This repository contains all code files for the Discrete Math Group Deep Dive 1. Our group delved deeper into three of the most popular shortest-path algorithms: Dijkstra's, A*, and Bellman-Ford. 

## **1. Introducing the algorithms**
### **1.1 Dijkstra's Algorithm**
Dijkstra's algorithm is arguably the most well-known shortest path algorithm, working well with graphs that are not too complex, not bidirectional, and do not have negative weights.It is often used in network routing protocols.

Dijkstra's was conceived in 1956 by Edsger W. Dijkstra as a thought experiment on the fastest way to get to a certain location. It has many variants; the original algorithm found the shortest path between two given nodes, while other implementations chooses a single "source node" and finds the shortest path to all other nodes, effectively creating a shortest-path tree.

Explore our Dijkstra's implementation in [this subfolder.](./dijkstra)

### **1.2 A\***
A downside of A\* is its $O(b^d)$ space complexity, due to the fact that it stores all generated nodes in memory instead of pre-processing the graph. It is built off of Dijkstra's algorithm, with the addition of a heuristic. The heuristic function $h(t)$ estimates the distance of any given node to the destination node. Instead of producing a shortest-path tree like Dijkstra's, A* finds the shortest path from a specific source to a specific goal.

### **1.3 Bellman-Ford**
Bellman-Ford is similar to Dijkstra's in that it finds all shortest paths to each node from a defined source node (In fact, it runs Dijkstra's as a subroutine for the actual shortest path implementations). Although this algorithm is slower than Dijkstra's, it's more versatile since it's able to handle graphs with negative weights.

This algorithm states that all edges of an N vertex graph should be relaxed N-1 times to compute the shortest path from the source node. Relaxation works by continuously shortening the calculated distance between vertices comparing that distance with other known distances.

## Navigating the Repo
`dijkstras_GDD1.py`: Python script that takes in a graph by instantiating nodes and edges, defines a start and target node, runs Dijkstra's algorithm, and returns the shortest path to that specific node. Note that this is a different implementation than what is described in the final Python notebook; that one produces a shortest-path tree to all nodes from the start node. 

`discrete_GDD1.ipynb`: Python notebook that goes through each algorithm, providing varying types of visualizations and context for each algorithm. 
