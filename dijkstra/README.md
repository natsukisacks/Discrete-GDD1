# Introduction to Dijkstra's Algorithm
Dijkstra's shortest-path algorithm can be implemented in many ways. For example, it could find the shortest path from a source node to all nodes or find the shortest path from a defined source node to a target node.

The most common use of Dijkstra's is finding the shortest path from the source to all nodes, producing a shortest-path tree. This notebook will delve deeper into this specific implementation. 

You can find the code implementation of Dijkstra's in `dijkstra.py`. 

## Overview of implementation
Dijkstra's keeps track of a few things:

*   Univisited nodes (list)
*   Visited nodes (list)
*   Shortest distance to source (adjacency list/dictionary)
*   Previous node (list)

For the visualization below, the shortest distance and previous node for each node is stored in a table. The distances are the equivalent of the edge weights. 

The following is the general steps that this algorithm takes. 

1. Starting at the source node, the algorithm looks at all connected nodes to determine the shortest path to them. To determine the shortest path, the algorithm compares newfound distances with those already stored. Since the start node is distance 0 away from itself, it receives an immediate shortest distance of 0. All other nodes start with an unknown distance of ∞, making distance comparison very simple. If the distance to the next nodes is shorter than the current distance (which is bound to be true when we’re starting with distance ∞), the distance to that vertex is updated accordingly.

2. Once the distances have been updated, we can remove the source from our list of unvisited nodes to our visited nodes. The current node we're searching from will become the closest node to the source. 

3. Next, we analyze the distances to the adjacent nodes from our new current node and update the distance accordingly. Once we have updated the distances and found our new shortest path, we can move the current node to our list of visited nodes and continue on to the shortest path.

4. This continues until our unvisited nodes list is empty. 

### Setup
In simpler terms...
* Label all nodes as having a distance of ∞, except for the starting node having a distance of 0.
* All nodes are placed in a list of ”unvisited” nodes.
* The starting node is labeled as the current node.

Algorithm:
1. Check if the unvisited nodes set is empty. If so, stop.
2. Look at all edges adjacent to the current node. For each adjacent node,
let distance from current = current distance + weight of current edge if distance from current < recorded distance. Update distance to be that from current node.
3. Remove current from the unvisited set.
4. Look at all unvisited nodes v. Find the node with the smallest labeled distance.
5. Set the current node to that node.
6. Repeat until there are no more unvisited nodes. 

The following is a walkthrough of the algorithm described below, using arbitrary times for driving between states in the Northeast. 

### Dijkstra's Algorithm Example
To make it easier to understand, let's walk through what Dijkstra's algorithm does on a graph. Although this implementation is kind of drawn-out, I think it's helpful to see the step-by-step process. 

**Original Graph**

<img src="https://drive.google.com/uc?export=view&id=183r0qADAp29XkRwgYKETw4Sdu7g8dZW3" width="700px">

We have defined MD as our source node, so we'll highlight that and it's respective edges that connect to an unvisited node. We also must keep track of the unvisited and visited nodes. This algorithm will run until all nodes have been visited, or unvisited = [].

Keeping track of the previous node allows us to create a shortest-path tree.

**Current node = MD**

<img src="https://drive.google.com/uc?export=view&id=1XFF0PwHLnKEfHrcmui4AFinKmLRtlxOP" width="700px">

Since NJ and RI are in the unvisited node list and both of their distances from MD are less than infinity, we update the shortest distance from the source and the previous node.

Now, we can remove MD from the unvisited node list and add it to the visited list.

**Current node = NJ**

<img src="https://drive.google.com/uc?export=view&id=1gDfscfOh55Jed7XcwX6eUSmQ4_R1yw87" width="700px">

Since MD has already been visited, we ignore the edge between NJ and MD. We look at all connected unvisited edges (RI and CT). The distance of RI will not be updated because the distance $3 + 5 > 5$. Distance CT is updated because $3 + 4 < ∞$.

Now, the previous node for CT is updated to NJ and the unvisited and visited lists are updated accordingly.

**Current node = RI**

<img src="https://drive.google.com/uc?export=view&id=1_i8Oi2MvjJtRhqnK1YQxP6lQpKVmeI8-" width="700px">

Since NJ and MD have already been visited, we ignore those connected edges. MA and NY have not yet been visited, so we update those values if the new found distance is less than what was there before.

Now, the previous nodes for NY and MA are updated to RI and the unvisited and visited lists are updated accordingly.

**Current node = NY**

<img src="https://drive.google.com/uc?export=view&id=14_i4tQEQZRjvKVcVXW9-vDVTNnP2QE2t" width="700px">

The only connected, unvisited node is CT. Since the current shortest distance for CT is 7, which is less than NY + 2 = 8, we don't update anything in our table. We update unvisited and visited nodes.

**Current node = CT**

<img src="https://drive.google.com/uc?export=view&id=1SuSy_0PZnDC-xrSLEghOpfC559aFbN2I" width="700">

The only connected, unvisited node is DE. Since the current shortest distance for DE is ∞, we update our shortest distance table to CT + 3 = 10. We update previous node for DE and the unvisited and visited nodes lists.

**Current node = DE**

<img src="https://drive.google.com/uc?export=view&id=1WmrTAFabA5LPOtfxLkolRLdSmwIacqHO" width="700px">

The only connected, unvisited node is MA. Since the current shortest distance for MA is 13, we won't update anything because that is shorter than DE + 7 = 17. We update the unvisited and visited nodes lists accordingly.

**Current node = MA**

<img src="https://drive.google.com/uc?export=view&id=1lqdcS1prORuxCoDE6OREtmKp73VfgaUo" width="700px">

There are no more unvisited nodes, so we are all done!

# Resources
[NetworkX library](https://networkx.org/documentation/stable/tutorial.html)

Brilliant. Dijkstra's Short Path Finder. https://brilliant.org/wiki/dijkstras-short-path-finder/

freeCodeCamp. Dijkstra's Shortest Path Algorithm: A Visual Introduction. https://www.freecodecamp.org/news/dijkstras-shortest-path-algorithm-visual-introduction/

Wikipedia. (n.d.). Dijkstra's Algorithm. https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm

Udacity. (2021, October). Implementing Dijkstra's Algorithm in Python. https://www.udacity.com/blog/2021/10/implementing-dijkstras-algorithm-in-python.html
