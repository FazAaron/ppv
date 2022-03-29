from typing import List, Set

from application import Application
from interface import Interface
from link import Link
from node import Host, Node, Router


class Network:
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

    # TODO
    def update_routing_tables(self) -> None:
        pass

    # TODO helper for dijkstra + dijkstra
    def create_graph(self) -> str:
        for host in self.hosts:
            for interface in host.interfaces:
                pass

    def create_host(self, name: str, ip: str, send_rate: int,) -> None:
        self.hosts.append(Host(name, ip, send_rate))
        self.update_routing_tables()
        
    def create_router(self, 
                      name: str, 
                      ip: str, 
                      send_rate: int,
                      buffer_size: int
                      ) -> None:
        self.routers.append(Router(name, ip, send_rate, buffer_size))
        self.update_routing_tables()

    def add_interface(self, node: Node, interface_name: str) -> None:
        node.add_interface(interface_name)

    def delete_interface(self, node: Node, interface_name: str) -> None:
        node.delete_interface(node.get_interface(interface_name))

    def set_application(self, 
                        host: Host, 
                        name: str,
                        amount: int, 
                        send_rate: int,
                        app_type: str
                        ) -> None:
        host.set_application(name, amount, send_rate, app_type)        

    def connect_node_interfaces(self, 
                                node: Node, 
                                o_node: Node, 
                                node_interface: Interface, 
                                o_interface: Interface, 
                                speed: int, 
                                metrics: int
                                ) -> None:
        node.connect_to_interface(o_node, node_interface, 
                                  o_interface, speed, metrics)
        self.update_routing_tables()

    def disconnect_node_interfaces(self,
                                   node: Node,
                                   node_interface: Interface
                                   ) -> None:
        node.disconnect_interface(node_interface)
        self.update_routing_tables()

    def print_node(self, node: Node) -> None:
        node.print_details()

    # TODO
    def send_packet(self) -> None:
        pass
