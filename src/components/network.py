from typing import List, Tuple, Any

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
        for node in self.get_nodes():
            interfaces += node.interfaces
        return interfaces

    def get_connections(self, node: Node) -> Any:
        connections: List[Tuple(Node, Link, Node)] = []
        for node in self.get_nodes():
            node_1: Node = node.connections[0][1]
            link: Link = node.connections[0][0].link
            node_2: Node = node.connections[1][1]
            to_add: Tuple(Node, Link, Node) = (node_1, link, node_2)
            connections.append(to_add)
        return connections

    # TODO
    def update_routing_tables(self) -> None:
        pass

    def is_duplicate_node(self, name: str, ip: str) -> bool:
        for node in self.get_nodes():
            if node.ip == ip or node.name == name:
                return True

    def get_host(self, name: str) -> Host:
        for host in self.hosts:
            if host.name == name:
                return host
        return None

    def create_host(self, name: str, ip: str, send_rate: int) -> None:
        if (self.is_duplicate_node(name, ip)):
            return
        self.hosts.append(Host(name, ip, send_rate))
        self.update_routing_tables()

    def delete_host(self, name: str) -> None:
        for host in self.hosts:
            if host.name == name:
                self.hosts.remove(host)

    def get_router(self, name: str) -> Router:
        for router in self.routers:
            if router.name == name:
                return router
        return None
    
    def create_router(self, 
                      name: str, 
                      ip: str, 
                      send_rate: int,
                      buffer_size: int
                      ) -> None:
        if (self.is_duplicate_node(name, ip)):
            return
        self.routers.append(Router(name, ip, send_rate, buffer_size))
        self.update_routing_tables()
                
    def delete_router(self, name: str) -> None:
        for router in self.routers:
            if router.name == name:
                self.routers.remove(router)

    def add_interface(self, node_name: str, interface_name: str) -> None:
        node: Node = self.get_host(node_name) or self.get_router(node_name)
        if node is None:
            return
        for interface in node.interfaces:
            if interface.name == interface_name:
                return
        node.add_interface(interface_name)

    def delete_interface(self, node_name: str, interface_name: str) -> None:
        node: Node = self.get_host(node_name) or self.get_router(node_name)
        if node is None:
            return
        node.delete_interface(interface_name)

    def set_application(self, 
                        host_name: str, 
                        name: str,
                        amount: int, 
                        send_rate: int,
                        app_type: str
                        ) -> None:
        host: Host = self.get_host(host_name)
        if host is None:
            return
        host.set_application(name, amount, send_rate, app_type)        

    def connect_node_interfaces(self, 
                                node_name: str, 
                                o_node_name: str, 
                                interface_name: str, 
                                o_interface_name: str, 
                                speed: int, 
                                metrics: int
                                ) -> None:
        first_node: Node = self.get_host(node_name) or \
                           self.get_router(node_name)
        snd_node: Node = self.get_host(o_node_name) or \
                         self.get_router(o_node_name)
        if (first_node and snd_node) is None:
            return
        first_node.connect_to_interface(snd_node, interface_name, 
                                        o_interface_name, speed, metrics)
        self.update_routing_tables()

    def disconnect_node_interfaces(self,
                                   node_name: str,
                                   node_interface: Interface
                                   ) -> None:
        node: Node = self.get_host(node_name) or self.get_router(node_name)
        node.disconnect_interface(node_interface)
        self.update_routing_tables()

    # TODO returns (next_node, target_node), so that the event handler can handle future events
    def send_packet(self) -> None:
        pass

    # TODO 
    def receive_packet(self) -> None:
        pass
    
    def print_node(self, node: Node) -> None:
        node.print_details()

    def print_nodes(self) -> None:
        for node in self.get_nodes():
            self.print_node(node)

    def print_hosts(self) -> None:
        for host in self.hosts:
            self.print_node(host)

    def print_routers(self) -> None:
        for router in self.routers:
            self.print_node(router)

    def print_connections(self) -> None:
        for connection in self.get_connections():
            print(f"{connection[0]}\n{connection[1]}\n{connection[2]}\n---")

    def print_applications(self) -> None:
        for host in self.hosts:
            print(host.application)