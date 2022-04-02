# Built-in modules
from typing import List, Tuple

# Self written modules
from src.components.application import Application
from src.components.interface import Interface
from src.components.link import Link
from src.components.node import Host, Node, Router
from src.utils.graph import Graph


class Network:
    """
    Abstract implementation of a Network, consisting of different components

    Data members:
    hosts:     List[Host]: Hosts available in the Network
    routers: List[Router]: Routers available in the Network
    graph:          Graph: A Graph built up of the Nodes in the Network
    """

    def __init__(self) -> None:
        self.hosts:   List[Host]   = []
        self.routers: List[Router] = []
        self.graph:   Graph        = Graph()

    def get_nodes(self) -> List[Node]:
        """
        Gets all the Nodes available in the Network

        Returns:
        List[Node]: All of the Nodes available in the Network
        """
        return self.hosts + self.routers

    def get_applications(self) -> List[Application]:
        """
        Gets the Application on every Host in the Network

        Returns:
        List[Application]: The Applications running in the Network
        """
        applications: List[Application] = []
        for host in self.hosts:
            applications.append(host.application)
        return applications

    def get_interfaces(self) -> List[Interface]:
        """
        Gets the Interface(s) on every Node in the Network

        Returns:
        List[Interface]: Every available Interface in the network
        """
        interfaces: List[Interface] = []
        for node in self.get_nodes():
            interfaces += node.interfaces
        return interfaces

    def get_connections(self) -> List[Tuple[Node, Link, Node]]:
        """
        Gets the connections between Nodes in the Network

        Returns:
        List[Tuple[Node, Link, Node]]: Every connection in the Network, which \
                                       corresponds to a (Node, Link, Node) trio
        """
        connections: List[Tuple[Node, Link, Node]] = []
        for node in self.get_nodes():
            node_1: Node = node.connections[0][1]
            link: Link = node.connections[0][0].link
            node_2: Node = node.connections[1][1]
            to_add: Tuple(Node, Link, Node) = (node_1, link, node_2)
            connections.append(to_add)
        return connections

    # TODO pass Routes to Nodes
    def update_routing_tables(self) -> None:
        """
        Updates the RoutingTable of every single Node in the Network with the
        help of a Graph object
        """
        self.graph.update_graph(self.get_nodes())

    def is_duplicate_node(self, node_name: str, ip: str) -> bool:
        """
        A helper method, which tells whether a Node with the given name or ip,
        or both, is present in the Network, or not

        Parameters:
        node_name (str): The name of the Node to check
        ip        (str): The IP address of the Node to check

        Returns:
        bool: Whether the given Node is already part of the Network
        """
        for node in self.get_nodes():
            if node.ip == ip or node.name == node_name:
                return True

    def get_host(self, host_name_or_ip: str) -> Host:
        """
        A helper method which returns the Host corresponding to the name

        Parameters:
        host_name_or_ip (str): The name or IP of the Host to search for

        Returns:
        Host: The Host corresponding to the name or None
        """
        for host in self.hosts:
            if host.name == host_name_or_ip or host.ip == host_name_or_ip:
                return host
        return None

    def create_host(self, host_name: str, ip: str, send_rate: int) -> None:
        """
        Creates a Host in the Network

        Parameters:
        host_name (str): The name of the new Host
        ip        (str): The IP of the new Host
        send_rate (int): The sending rate of the new Host
        """
        if (self.is_duplicate_node(host_name, ip)):
            return
        self.hosts.append(Host(host_name, ip, send_rate))
        self.update_routing_tables()

    def delete_host(self, host_name_or_ip: str) -> None:
        """
        Deletes a Host from the Network

        Parameters:
        host_name_or_ip (str): The name or IP of the Host to delete
        """
        for host in self.hosts:
            if host.name == host_name_or_ip or host.ip == host_name_or_ip:
                for interface in host.interfaces:
                    host.disconnect_interface(interface.name)
                self.hosts.remove(host)
                self.update_routing_tables()
                return

    def get_router(self, router_name_or_ip: str) -> Router:
        """
        A helper method which returns the Router corresponding to the name

        Parameters:
        router_name_or_ip (str): The name or IP of the Router to search for

        Returns:
        Router: The Router corresponding to the name or None
        """
        for router in self.routers:
            if router.name == router_name_or_ip or \
               router.ip   == router_name_or_ip:
                return router
        return None

    def create_router(self,
                      router_name: str,
                      ip: str,
                      send_rate: int,
                      buffer_size: int
                      ) -> None:
        """
        Creates a Router in the Network

        Parameters:
        Router_name (str): The name of the new Router
        ip          (str): The IP of the new Router
        send_rate   (int): The sending rate of the new Router
        """
        if (self.is_duplicate_node(router_name, ip)):
            return
        self.routers.append(Router(router_name, ip, send_rate, buffer_size))
        self.update_routing_tables()

    def delete_router(self, router_name_or_ip: str) -> None:
        """
        Deletes a Router from the Network

        Parameters:
        router_name_or_ip (str): The name or IP of the Router to delete
        """
        for router in self.routers:
            if router.name == router_name_or_ip or \
               router.ip   == router_name_or_ip:
                for interface in router.interfaces:
                    router.disconnect_interface(interface.name)
                self.routers.remove(router)
                self.update_routing_tables()
                return

    def add_interface(self, node_name_or_ip: str, interface_name: str) -> None:
        """
        Adds an Interface to an existing Node in the Network\n
        If that Interface is already present on the Node, this does not do
        anything\n
        If the Node does not exist, this does not do anything

        Parameters:
        node_name_or_ip (str): The name or IP of the Node
        interface_name  (str): The name of the Interface to add to the Node
        """
        node: Node = self.get_host(node_name_or_ip) or \
                     self.get_router(node_name_or_ip)
        if node is None:
            return
        for interface in node.interfaces:
            if interface.name == interface_name:
                return
        node.add_interface(interface_name)

    def delete_interface(self,
                         node_name_or_ip: str,
                         interface_name: str
                         ) -> None:
        """
        Deletes an existing Interface from an existing Node\n
        If the Interface does not exist, this does not do anything\n
        If the Node does not exist, this does not do anything

        Parameters:
        node_name_or_ip (str): The name or IP of the Node to delete from
        interface_name  (str): The Interface's name to delete from the Node
        """
        node: Node = self.get_host(node_name_or_ip) or \
                     self.get_router(node_name_or_ip)
        if node is None:
            return
        node.delete_interface(interface_name)
        self.update_routing_tables()

    def set_application(self,
                        host_name_or_ip: str,
                        app_name: str,
                        amount: int,
                        send_rate: int,
                        app_type: str
                        ) -> None:
        """
        Sets the Application on a Host type Node\n
        If the Host does not exist, this does not do anything

        Parameters:
        host_name_or_ip (str): The name of the Host
        app_name        (str): The name of the Application to set on the Host
        amount          (int): Packet amount to send from the Application
        send_rate       (int): The sending rate of the application
        app_type        (str): The type of the Application - AIMD, or CONST
        """
        host: Host = self.get_host(host_name_or_ip)
        if host is None:
            return
        host.set_application(app_name, amount, send_rate, app_type)

    def connect_node_interfaces(self,
                                node_name_or_ip: str,
                                o_node_name_or_ip: str,
                                interface_name: str,
                                o_interface_name: str,
                                speed: int,
                                metrics: int
                                ) -> None:
        """
        Connects two Nodes on the given Interfaces

        Parameters:
        node_name_or_ip   (str): The name or IP of the first Node
        o_node_name_or_ip (str): The name or IP of the second Node
        interface_name    (str): The name of the Interface on the first Node
        o_interface_name  (str): The name of the Interface on the second Node
        speed             (int): The speed of the Link between the Nodes
        metrics           (int): The metrics of the Link between the nodes
        """
        first_node: Node = self.get_host(node_name_or_ip) or \
                           self.get_router(node_name_or_ip)
        snd_node: Node = self.get_host(o_node_name_or_ip) or \
                         self.get_router(o_node_name_or_ip)
        if (first_node and snd_node) is None:
            return
        first_node.connect_to_interface(snd_node, interface_name,
                                        o_interface_name, speed, metrics)
        self.update_routing_tables()

    def disconnect_node_interface(self,
                                  node_name_or_ip: str,
                                  interface_name: str
                                  ) -> None:
        """
        Disconnects a Node's interface from any connection\n
        This also disconnects the other Node which the Interface was connected
        to beforehand

        Parameters:
        node_name_or_ip (str): The Node's name or IP to disconnect from
        node_interface  (str): The Interface's name to disconnect the Link from
        """
        node: Node = self.get_host(node_name_or_ip) or \
                     self.get_router(node_name_or_ip)
        node.disconnect_interface(interface_name)
        self.update_routing_tables()

    def send_packet(self,
                    node_name_or_ip: str,
                    destination_name_or_ip: str
                    ) -> Tuple[str, str, str]:
        """
        Starts sending a Packet to the given destination from the given Node\n
        If the Node is a Host, it creates a new Packet to send, because they
        are by default not set up to forward Packets\n
        If the Node is a Router, it gets a Packet from their buffer, and
        forwards that\n
        This describes one step of the sending process, so calling this method
        multiple times, until the current Node's IP is equal to the destination
        is needed for it to function properly

        Parameters:
        node_name_or_ip        (str): The Node's name or IP to send from
        destination_name_or_ip (str): The name or IP address of the goal Node

        Returns:
        Tuple[str, str, str]: A (gateway, receiver_interface, destination) trio
        """
        host:           Host = self.get_host(node_name_or_ip)
        router:         Router = self.get_router(node_name_or_ip)
        node:           Node = host or router
        destination_ip: str = (self.get_host(destination_name_or_ip) or
                               self.get_router(destination_name_or_ip)).ip
        if router is None:
            next_hop: Tuple[str, str] = node.send_packet(destination_ip)
        else:
            next_hop: Tuple[str, str] = node.send_packet()
        return (next_hop[0], next_hop[1], destination_name_or_ip)

    def receive_packet(self,
                       node_name_or_ip: str,
                       interface_name: str
                       ) -> None:
        """
        Receives a Packet on the Node on the given Interface\n
        If the Node is a Host, it consumes the Packet, because they are by
        default not set up to handle forwarding Packets\n
        If the Node is a Router, it puts the incoming Packet into it's 
        buffer.\n
        This describes one step of the sending process, so calling this method
        multiple times, until the current Node's IP is equal to the destination
        is needed for it to function properly

        Parameters:
        node_name_or_ip (str): The name or IP of the Node receiving a Packet
        interface_name  (str): The name of the Interface the Packet goes to
        """
        node: Node = (self.get_host(node_name_or_ip) or
                      self.get_router(node_name_or_ip))
        node.receive_packet(interface_name)

    def print_node(self, node: Node) -> None:
        """
        Prints a Node's configuration

        Parameters:
        node (Node): The Node to print the configuration of
        """
        node.print_details()

    def print_nodes(self) -> None:
        """
        Prints every Node's configuration in the Network
        """
        for node in self.get_nodes():
            self.print_node(node)

    def print_hosts(self) -> None:
        """
        Prints every Host's configuration in the Network
        """
        for host in self.hosts:
            self.print_node(host)

    def print_routers(self) -> None:
        """
        Prints every Router's configuration in the Network
        """
        for router in self.routers:
            self.print_node(router)

    def print_connections(self) -> None:
        """
        Prints every Connection (back and forth) in the Network
        """
        for connection in self.get_connections():
            print(f"{connection[0]}\n{connection[1]}\n{connection[2]}\n---")

    def print_applications(self) -> None:
        """
        Prints every Application running in the Network
        """
        for host in self.hosts:
            print(host.application)
