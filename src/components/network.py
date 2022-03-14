from typing import List
from link import Link
from node import Node

class Network:
    # TODO building a network from the components
    """
    Abstract implementation of a Network, consisting of different components.
    """
    def __init__(self) -> None:
        self.links: List[Link] = []
        self.nodes: List[Node] = []
