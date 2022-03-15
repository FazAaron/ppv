from typing import List, Set
from link import Link
from interface import Interface
from application import Application
from node import Node, Host, Router

class Network:
    # TODO building a network from the components
    """
    Abstract implementation of a Network, consisting of different components.
    """
    def __init__(self) -> None:
        self.hosts:   List[Host]   = []
        self.routers: List[Router] = []

    def get_nodes(self) -> List[Node]:
        return self.hosts + self.routers

    def get_applications(self) -> List[Application]:
        applications: List[Application] = []
        for host in self.hosts:
            applications.append(host.application)
        return applications

    def get_interfaces(self) -> List[Interface]:
        interfaces: List[Interface] = []
        for host in self.hosts:
            interfaces += host.interfaces
        for router in self.routers:
            interfaces += router.interfaces
        return interfaces

    def get_links(self) -> Set[Link]:
        links: Set[Link] = set()
        interfaces: List[Interface] = self.get_interfaces()
        for interface in interfaces:
            links.add(interface.link)
        return links

    def send_packet() -> None:
        pass