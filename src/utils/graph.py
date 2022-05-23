"""
This module makes Graph objects available for use when imported
"""

# Built-in modules
from math import inf
from typing import Dict, List, Tuple

# Self-written modules
from src.components.node import Node


class Graph:
    """
    A Graph representation of Network nodes and their connections

    Data members:
    vertices                       (List[str]): The vertices of the Graph
    edges    (List[(str, str, str, str, int)]): The edges of the Graph
    """

    def __init__(self) -> None:
        self.vertices: List[str] = []
        self.edges:    List[(str, str, str, str, int)] = []

    def update_graph(self, nodes: List[Node]) -> None:
        """
        Creates a Graph from a list of Nodes and their connections

        Parameters:
        nodes (List[Node]): The list of Nodes used to create the Graph
        """
        self.vertices = []
        self.edges = []

        # Go through all of the Nodes
        for node in nodes:
            # Get every vertex
            self.vertices.append(node.ip)

            # For every connection, add an edge to the vertex
            # An edge looks like this:
            # (ip - name) <- metrics -> (ip - name)
            for connection in node.connections:
                self.edges.append((connection[0][1].ip, connection[0][0].name,
                                   connection[1][1].ip, connection[1][0].name,
                                   connection[0][0].link.channels[0].metrics))

    def dijkstra(self,
                 source_ip: str,
                 destination_ip: str
                 ) -> Tuple[str, str, str, int]:
        """
        Dijkstra's algorithm used to set Routes in Nodes

        Parameters:
        source_ip      (str): The vertex the path starts from
        destination_ip (str): The vertex the path ends on

        Returns:
        (Tuple[str, str, str, int]): A tuple containing (destination_ip, \
                                     next_hop, interface, metrics) \
                                     to set as Route
        """
        # If the source_ip equals the destination_ip, we don't need to run Dijsktra's
        # algorithm
        if source_ip == destination_ip:
            return None

        # Dijkstra's algorithm
        # Create the variables to use
        # Distances for vertices, starting with an infinity value
        dist: Dict[str, int] = {vertex: inf for vertex in self.vertices}

        # The neighbour vertex for every vertex
        previous: Dict[str, int] = \
            {vertex: None for vertex in self.vertices}

        # Make the starting vertex's distance 0
        dist[source_ip] = 0

        # Create a set of neighbours for every vertex
        neighbours: Dict[str, set] = \
            {vertex: set() for vertex in self.vertices}

        # Fill them accordingly
        for start, s_interface, end, e_interface, cost in self.edges:
            # The neighbour to reach through the s_interface and it's cost
            neighbours[start].add((end, s_interface, cost))
            # The same, but backwards
            neighbours[end].add((start, e_interface, cost))

        # Run Dijkstra's algorithm
        q: List[str] = self.vertices.copy()
        while q:
            u: str = min(q, key=lambda vertex: dist[vertex])
            q.remove(u)
            if dist[u] == inf or u == destination_ip:
                break
            for v, interface, cost in neighbours[u]:
                if dist[u] + int(cost) < dist[v]:
                    previous[v] = u
                    dist[v] = dist[u] + int(cost)

        # Get the values to return
        next_hop: str = None
        for key, value in previous.items():
            if key == destination_ip:
                curr_val = value
                next_hop = key
                if curr_val is None:
                    break
                while curr_val != source_ip:
                    next_hop = curr_val
                    curr_val = previous[curr_val]
                break
        if next_hop is None:
            return None
        for neighbour in neighbours[source_ip]:
            if neighbour[0] == next_hop:
                interface = neighbour[1]
                return (destination_ip, next_hop,
                        interface, dist[destination_ip])
        return None
