# Built-in modules
from collections import deque
from math import inf
from typing import List

# Self-written modules
from src.components.interface import Interface
from src.components.node import Node


class Graph:

    def __init__(self) -> None:
        self.vertices: List[Node]                                    = []
        self.edges:    List[(Node, Interface, Node, Interface, int)] = []

    def update_graph(self, nodes: List[Node]) -> None:
        self.vertices = []
        self.edges    = []
        for node in nodes:
            self.vertices.append(node.ip)
            for connection in node.connections:
                self.edges.append((connection[0][1].ip, connection[0][0].name,
                                   connection[1][1].ip, connection[1][0].name,
                                   connection[0][0].link.channels[0].metrics))

    def dijkstra(self, source_ip: str, destination_ip: str) -> None:
        if not source_ip in self.vertices:
            pass
