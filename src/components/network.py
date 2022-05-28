"""
This module serves as a way to interact with the components through an
API-like interface by allowing the users to create Network objects when
importing it, thus only being able to communicate with components in the
intended way
"""

# Built-in modules
from typing import List, Tuple

# Self-made modules
from src.components.interface import Interface
from src.components.node import Host, Node, Router
from src.components.routing_table import Route
from src.components.packet import Packet
from src.utils.graph import Graph


class Network:
    """
    Abstract implementation of a Network, consisting of different components

    Data members:
    hosts:       (List[Host]): Hosts available in the Network
    routers:     (List[Router]): Routers available in the Network
    graph:       (Graph): A Graph built up of the Nodes in the Network
    total_pack   (int): The total amount of Packets sent out
    dropped_pack (int): The total amount of Packets droped
    """

    def __init__(self) -> None:
        self.hosts:            List[Host] = []
        self.routers:          List[Router] = []
        self.graph:            Graph = Graph()
        self.total_pack:       int = 0
        self.dropped_pack:     int = 0
        self.received_pack:    int = 0
        self.avg_ppv_sent:     float = 0.0
        self.avg_ppv_dropped:  float = 0.0
        self.avg_ppv_received: float = 0.0

    def get_nodes(self) -> List[Node]:
        """
        Gets all the Nodes available in the Network

        Returns:
        List[Node]: All of the Nodes available in the Network
        """
        return self.hosts + self.routers

    def get_host(self, host_name_or_ip: str) -> Host:
        """
        Gets the Host corresponding to the name

        Parameters:
        host_name_or_ip (str): The name or IP of the Host to search for

        Returns:
        Host: The Host corresponding to the name or None
        """
        for host in self.hosts:
            if host_name_or_ip in (host.name, host.ip):
                return host
        return None

    def __refresh_avg_ppv(self) -> None:
        # Get the sum from Hosts
        self.avg_ppv_sent = 0.0
        self.avg_ppv_received = 0.0
        self.avg_ppv_dropped = 0.0
        for host in self.hosts:
            self.avg_ppv_sent += host.ppv_sent
            self.avg_ppv_received += host.ppv_received

        # Get the sum from Routers
        for router in self.routers:
            self.avg_ppv_dropped += router.ppv_dropped

        # Get the average
        self.avg_ppv_sent /= float(self.total_pack)
        if self.received_pack > 0:
            self.avg_ppv_received /= float(self.received_pack)
        if self.dropped_pack > 0:
            self.avg_ppv_dropped /= float(self.dropped_pack)

    def __update_routing_tables(self) -> bool:
        """
        Updates the RoutingTable of every single Node in the Network with the
        help of a Graph object

        Returns:
        bool: Whether the updating was successful or not
        """
        nodes: List[Node] = self.get_nodes()

        # Creates the Graph out of the Node components
        self.graph.update_graph(nodes)

        # Go through the Nodes
        for source in nodes:
            # Empty their Routes
            source.reset_routes()
            # Go through every single Node for every Node
            for destination in nodes:
                # This can only return False when an error occurs
                # Only done like this because there should always be a branch
                # whenever False is returned
                try:
                    # Run Dijkstra's algorithm on the source and destination
                    # IPs
                    route_tuple: Tuple[str, str, str, int] = \
                        self.graph.dijkstra(source.ip,
                                            destination.ip)
                    # If there is a Route between the two, then add it
                    if route_tuple is not None:
                        source.add_route(Route(route_tuple[0],
                                               route_tuple[1],
                                               route_tuple[2],
                                               route_tuple[3]))
                except:
                    return False
        return True

    def __is_duplicate_node(self, node_name: str, ip: str) -> bool:
        """
        Tells whether a Node with the given name or ip, or both, 
        is present in the Network, or not

        Parameters:
        node_name (str): The name of the Node to check
        ip        (str): The IP address of the Node to check

        Returns:
        bool: Whether the given Node is already part of the Network
        """
        for node in self.get_nodes():
            # A Node is a duplicate if there is already a Node with the given
            # IP or name present
            if node.ip == ip or node.name == node_name:
                return True

        return False

    def create_host(self, host_name: str, ip: str, send_rate: int) -> bool:
        """
        Creates a Host in the Network

        Parameters:
        host_name (str): The name of the new Host
        ip        (str): The IP of the new Host
        send_rate (int): The sending rate of the new Host

        Returns:
        bool: Whether the creation was a success or not
        """
        # Check if the Node would be a duplicate if created
        if self.__is_duplicate_node(host_name, ip):
            return False

        # If not, create it, and then update the RoutingTable of every Node
        self.hosts.append(Host(host_name, ip, send_rate))
        return self.__update_routing_tables()

    def delete_host(self, host_name_or_ip: str) -> bool:
        """
        Deletes a Host from the Network

        Parameters:
        host_name_or_ip (str): The name or IP of the Host to delete

        Returns:
        bool: Whether the deletion was a success or not
        """
        # Go through the Hosts to get the proper Host
        for host in self.hosts:
            # If either the IP or name matches
            if host_name_or_ip in (host.name, host.ip):
                # Go through all of its Interfaces
                for interface in host.interfaces:
                    # Disconnect them one by one
                    ret_val: Tuple[bool, int] = host.disconnect_interface(
                        interface.name)
                    # Get the amount of Packets dropped due to the disconnection
                    self.dropped_pack += ret_val[1]
                    # If the disconnect failed, return with False
                    if not ret_val[0]:
                        return ret_val[0]

                # If everything succeeded, remove the Host, and update the
                # RoutingTable of every Node
                self.hosts.remove(host)
                return self.__update_routing_tables()

        return False

    def get_router(self, router_name_or_ip: str) -> Router:
        """
        Gets the Router corresponding to the name

        Parameters:
        router_name_or_ip (str): The name or IP of the Router to search for

        Returns:
        Router: The Router corresponding to the name or None
        """
        for router in self.routers:
            # A Node is a duplicate if there is already a Node with the given
            # IP or name present
            if router_name_or_ip in (router.name, router.ip):
                return router
        return None

    def create_router(self,
                      router_name: str,
                      ip: str,
                      send_rate: int,
                      buffer_size: int
                      ) -> bool:
        """
        Creates a Router in the Network

        Parameters:
        Router_name (str): The name of the new Router
        ip          (str): The IP of the new Router
        send_rate   (int): The sending rate of the new Router

        Returns:
        bool: Whether the creation was a success or not
        """
        # Check if the Node would be a duplicate if created
        if self.__is_duplicate_node(router_name, ip):
            return False

        # If not, create it, and then update the RoutingTable of every Node
        self.routers.append(Router(router_name, ip, send_rate, buffer_size))
        return self.__update_routing_tables()

    def delete_router(self, router_name_or_ip: str) -> bool:
        """
        Deletes a Router from the Network

        Parameters:
        router_name_or_ip (str): The name or IP of the Router to delete

        Returns:
        bool: Whether the deletion was a success or not
        """
        # Go through the Hosts to get the proper Router
        for router in self.routers:
            # If either the IP or name matches
            if router_name_or_ip in (router.name, router.ip):
                # Go through all of its Interfaces
                for interface in router.interfaces:
                    # Disconnect them one by one
                    ret_val: Tuple[bool, int] = router.disconnect_interface(
                        interface.name)

                    # Get the amount of Packets dropped due to the disconnection
                    self.dropped_pack += ret_val[1]
                    # If the disconnect failed, return with False
                    if not ret_val[0]:
                        return ret_val[0]

                # Also take the buffer into consideration when counting dropped
                # packets
                self.dropped_pack += router.get_buffer_length()

                # If everything succeeded, remove the Router, and update the
                # RoutingTable of every Node
                self.routers.remove(router)
                return self.__update_routing_tables()

        return False

    def add_interface(self, node_name_or_ip: str, interface_name: str) -> bool:
        """
        Adds an Interface to an existing Node in the Network\n
        If that Interface is already present on the Node, this does not do
        anything\n
        If the Node does not exist, this does not do anything

        Parameters:
        node_name_or_ip (str): The name or IP of the Node
        interface_name  (str): The name of the Interface to add to the Node

        Returns:
        bool: Whether adding the Interface was a success or not
        """
        # Get the Node - either a Host or a Router
        node: Node = self.get_host(node_name_or_ip) or \
            self.get_router(node_name_or_ip)

        # If no such Node was found, return with False
        if node is None:
            return False

        # Else return with whether adding the Interface was successful or not
        return node.add_interface(interface_name)

    def delete_interface(self,
                         node_name_or_ip: str,
                         interface_name: str
                         ) -> bool:
        """
        Deletes an existing Interface from an existing Node\n
        If the Interface does not exist, this does not do anything\n
        If the Node does not exist, this does not do anything

        Parameters:
        node_name_or_ip (str): The name or IP of the Node to delete from
        interface_name  (str): The Interface's name to delete from the Node

        Returns:
        bool: Whether the deletion of the Interface was a success or not
        """
        # Get the Node - either a Host or a Router
        node: Node = self.get_host(node_name_or_ip) or \
            self.get_router(node_name_or_ip)

        # If no such Node was found, return with False
        if node is None:
            return False

        # Delete the Interface, and save if it failed or not, and the Packets
        # dropped into a variable
        ret_val: Tuple[bool, int] = node.delete_interface(interface_name)
        self.dropped_pack += ret_val[1]

        # If it succeeded, update RoutingTables, and return whether it happened
        # or not
        if ret_val[0]:
            return self.__update_routing_tables()

        # Else just return with False
        return ret_val[0]

    def set_application(self,
                        host_name_or_ip: str,
                        app_name: str,
                        amount: int,
                        send_rate: int,
                        app_type: str
                        ) -> bool:
        """
        Sets the Application on a Host type Node\n
        If the Host does not exist, this does not do anything

        Parameters:
        host_name_or_ip (str): The name or IP of the Host
        app_name        (str): The name of the Application to set on the Host
        amount          (int): Packet amount to send from the Application
        send_rate       (int): The sending rate of the application
        app_type        (str): The type of the Application - AIMD, or CONST

        Returns:
        bool: Whether setting the Application was a success or not
        """
        # Get the Host
        host: Host = self.get_host(host_name_or_ip)

        # If no such Host was found, return with False
        if host is None:
            return False

        # Set the Application, and in this case, it can't fail
        host.set_application(app_name, amount, send_rate, app_type)

        return True

    def can_send(self, host_name_or_ip: str) -> bool:
        """
        Gets whether the Host can send or not

        Parameters:
        host_name_or_ip (str): The name or IP of the Host

        Returns:
        bool: Whether the Host can send or not
        """
        # Get the Host
        host: Host = self.get_host(host_name_or_ip)

        # If no such Host was found, return with False
        if host is None or host.application is None:
            return False

        # Else return with whether it can send or not
        return host.application.can_send()

    def get_link_speed(self, node_name_or_ip: str, interface_name: str) -> int:
        """
        Gets the speed of the Link connected to the given Interface

        Parameters:
        node_name_or_ip (str): The name or IP of the Node
        interface_name  (str): The name of the Interface
        """
        # Get the Node
        node: Node = self.get_host(node_name_or_ip) or \
            self.get_router(node_name_or_ip)

        # If no such Node was found, return with 0
        if node is None:
            return 0

        # Get the Interface
        interface: Interface = node.get_interface(interface_name)

        # If no such Interface was found, or it's not connected, return with 0
        if interface is None or interface.link is None:
            return 0

        # Else, return the speed
        return interface.send_channel.speed

    def connect_node_interfaces(self,
                                node_name_or_ip: str,
                                o_node_name_or_ip: str,
                                interface_name: str,
                                o_interface_name: str,
                                speed: int,
                                metrics: int
                                ) -> bool:
        """
        Connects two Nodes on the given Interfaces

        Parameters:
        node_name_or_ip   (str): The name or IP of the first Node
        o_node_name_or_ip (str): The name or IP of the second Node
        interface_name    (str): The name of the Interface on the first Node
        o_interface_name  (str): The name of the Interface on the second Node
        speed             (int): The speed of the Link between the Nodes
        metrics           (int): The metrics of the Link between the nodes

        Returns:
        bool: Whether the creation of the connection was a success or not
        """
        # Get both Nodes - either of them can be either a Host or Router
        host_1: Host = self.get_host(node_name_or_ip)
        host_2: Host = self.get_host(o_node_name_or_ip)
        first_node: Node = host_1 or \
            self.get_router(node_name_or_ip)
        snd_node:   Node = host_2 or \
            self.get_router(o_node_name_or_ip)

        # If any of the two does not exist, return with False
        if (first_node and snd_node) is None:
            return False

        # Don't let Hosts get connected
        if (host_1 and host_2) is not None:
            return False

        # Try connecting the Interfaces
        ret_val: Tuple[bool, int] = first_node.connect_to_interface(snd_node,
                                                                    interface_name,
                                                                    o_interface_name,
                                                                    speed,
                                                                    metrics)

        # Since this also disconnects, we need to take dropped Packets into
        # consideration
        self.dropped_pack += ret_val[1]

        # If it succeeded, update RoutingTables, and return whether it happened
        # or not
        if ret_val[0]:
            return self.__update_routing_tables()

        # Else just return with False
        return ret_val[0]

    def disconnect_node_interface(self,
                                  node_name_or_ip: str,
                                  interface_name: str
                                  ) -> bool:
        """
        Disconnects a Node's interface from any connection\n
        This also disconnects the other Node which the Interface was connected
        to beforehand

        Parameters:
        node_name_or_ip (str): The Node's name or IP to disconnect from
        node_interface  (str): The Interface's name to disconnect the Link from

        Returns:
        bool: Whether the Interface was disconnected or not
        """
        # Get the Node - either a Host or a Router
        node: Node = self.get_host(node_name_or_ip) or \
            self.get_router(node_name_or_ip)

        # If no such Node was found, return with False
        if node is None:
            return False

        # Try disconnecting the Interface
        ret_val: Tuple[bool, int] = node.disconnect_interface(interface_name)

        # Take dropped Packets into consideration
        self.dropped_pack += ret_val[1]

        # If it succeeded, update RoutingTables, and return whether it happened
        # or not
        if ret_val[0]:
            return self.__update_routing_tables()

        # Else just return with False
        return ret_val[0]

    def send_packet(self,
                    node_name_or_ip: str,
                    destination_name_or_ip: str = ""
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
        # This needs to be done separately, because there is a branch that needs
        # checking the type of the Node
        host:   Host = self.get_host(node_name_or_ip)
        router: Router = self.get_router(node_name_or_ip)

        # Get the source Node
        node:   Node = host or router

        # Get the destination Node
        destination_node: Node = self.get_host(destination_name_or_ip) or \
            self.get_router(destination_name_or_ip)

        # If either of them is None, return with None
        # Needed to check like this, because Router does not require a destination
        # to send
        if ((host and destination_node) is None) and (router is None):
            return None

        # If the source Node is a Host, we need to add a parameter when using
        # the method
        if router is None:
            next_hop: Tuple[str, str] = node.send_packet(destination_node.ip)
            self.total_pack += 1
        # If it is a Router, it just pops a Packet from its buffer
        else:
            next_hop: Tuple[str, str] = node.send_packet()

        # Check if there is a Route (or in this case, a next hop), and if there
        # is none, then increase the dropped Packets and return None
        if next_hop is None:
            self.dropped_pack += 1
            self.__refresh_avg_ppv()
            return None

        # Else return the next hop, the next hop's receiver interface and the
        # actual destination of the Packet, for future use by other classes
        self.__refresh_avg_ppv()
        return (next_hop[0], next_hop[1], destination_name_or_ip)

    def receive_packet(self,
                       node_name_or_ip: str,
                       interface_name: str
                       ) -> bool:
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

        Returns:
        bool: Whether the Packet could be received or not
        """
        # Needs to be done separately, since the behaviour of Host and Router
        # differs
        router: Router = self.get_router(node_name_or_ip)
        node: Node = (self.get_host(node_name_or_ip) or router)

        # Check if the Node is present at all
        if node is None:
            return False

        # If the Node is a Host, we are done
        if router is None:
            self.received_pack += 1
            success: bool = node.receive_packet(interface_name)
            self.__refresh_avg_ppv()
            return success

        # In the other case, we need to handle the dropped Packet and the
        # success separately
        ret_val: Tuple[bool, bool] = node.receive_packet(interface_name)

        # If it dropped a Packet, increase the counter
        if ret_val[1]:
            self.dropped_pack += 1
        self.__refresh_avg_ppv()

        # Return the success / failure
        return ret_val[0]
