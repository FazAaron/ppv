# Built-in modules
from typing import List

# Self-written modules
from src.components.interface import Interface
from src.components.node import Node


class Graph:

    def __init__(self) -> None:
        self.vertices: List[Node]                                    = []
        self.edges:    List[(Node, Interface, Node, Interface, int)] = []

    def update_graph(self, nodes: List[Node]) -> None:
        for node in nodes:
            self.vertices.append(node)
            for connection in node.connections:
                self.edges.append((connection[0][1], connection[0][0], \
                                   connection[1][1], connection[0][1], \
                                   connection[0][0].link.channels[0].metrics))

    def dijkstra(self) -> None:
        pass
