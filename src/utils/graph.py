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
        for node in nodes:
            self.vertices.append(node.ip)
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
        if source_ip == destination_ip:
            return None
        if source_ip in self.vertices:
            # Dijkstra's algorithm
            dist: Dict[str, int] = {vertex: inf for vertex in self.vertices}
            previous: Dict[str, int] = \
                {vertex: None for vertex in self.vertices}
            dist[source_ip] = 0
            neighbours: Dict[str, set] = \
                {vertex: set() for vertex in self.vertices}
            for start, s_interface, end, e_interface, cost in self.edges:
                neighbours[start].add((end, s_interface, cost))
                neighbours[end].add((start, e_interface, cost))

            q: List[Node] = self.vertices.copy()
            while q:
                u: str = min(q, key=lambda vertex: dist[vertex])
                q.remove(u)
                if dist[u] == inf or u == destination_ip:
                    break
                for v, interface, cost in neighbours[u]:
                    if dist[u] + cost < dist[v]:
                        previous[v] = u
                        dist[v] = dist[u] + cost

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
