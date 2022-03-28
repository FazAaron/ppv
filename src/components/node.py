from __future__ import annotations

import random
from typing import List, Tuple

from application import Application
from interface import Interface
from link import Link
from packet import Packet
from routing_table import Route, RoutingTable


class Node:
    """
    Abstract implementation of a Node in a Network\n
    This being the main component, handles most of the logic
    Base class for Host and Router

    Data members:
    name                            (str): Name of the Node
    ip                              (str): IP address of the Node
    send_rate                       (int): Sending rate (Packets / second)
    interfaces          (List[Interface]): Interfaces available on the Node
    connections (List[(Interface, Node), \
                      (Interface, Node)]): Node - Node connections
    routing_table          (RoutingTable): Routing table on the Node
    """
    def __init__(self, name: str, ip: str, send_rate: int) -> None:
        self.name:          str                     = name
        self.ip:            str                     = ip
        self.send_rate:     int                     = send_rate
        self.interfaces:    List[Interface]         = []
        self.connections:   List[(Interface, Node), 
                                 (Interface, Node)] = []
        self.routing_table: RoutingTable            = RoutingTable()

    def add_route(self, route: Route) -> None:
        """
        Adds a Route to the RoutingTable

        Parameters:
        route (Route): The route to add
        """
        self.routing_table.set_route(route)

    def get_best_route(self, destination: str) -> Route:
        """
        Get the best Route that matches the destination's IP address or nothing

        Parameters:
        destination (str): The IP address of the destination Node
        
        Returns:
        Route: The best route that matches the destination IP address or None
        """
        best_route: Route = None
        for route in self.routing_table.routes:
            if route.destination == destination:
                if best_route is None:
                    best_route = route
                elif best_route.metrics > route.metrics:
                    best_route = route
        return best_route

    def get_interface(self, name: str) -> Interface:
        """
        Get an interface based on it's name or nothing

        Parameters:
        name (str): The name of the interface to find

        Returns:
        Interface: The corresponding interface or None (if not present)
        """
        for interface in self.interfaces:
            if interface.name == name:
                return interface
        return None

    def add_interface(self, name: str) -> None:
        """
        Adds an Interface to the Node if it does not match an already existing
        Interface's name

        Parameters:
        name (str): The name of the new Interface to add
        """
        for interface in self.interfaces:
            if interface.name == name:
                return
        self.interfaces.append(Interface(name))

    def delete_interface(self, name: str) -> None:
        """
        Deletes an Interface on the Node\n
        Before deletion, the Interface is disconnected and is removed from all
        connections

        Parameters:
        name (str): The Interface's name to delete
        """
        interface: Interface = self.get_interface(name)
        if interface is None:
            return
        for connection in self.connections:
            if connection[0][0] == interface:
                self.disconnect_interface(name)
                self.interfaces.remove(interface)
                return
            
    def connect_to_interface(self,
                             __o: Node,
                             self_name: str,
                             other_name: str,
                             speed: int,
                             metrics: int
                             ) -> None:
        """
        Connects an Interface of the Node to another Node's Interface\n
        This creates a Link between the two Interfaces\n
        Before connecting the two Interfaces, it also disconnects them from any
        other connection

        Parameters:
        __o                  (Node): Other Node
        self_name             (str): This Node's Interface's name to connect
        other_name            (str): Other Node's Interface's name to connect
        speed                 (int): Speed of the Link between the Interfaces
        metrics               (int): Metrics of Link between the Interfaces
        """
        if self is __o:
            return
        self_interface:  Interface = self.get_interface(self_name)
        other_interface: Interface = __o.get_interface(other_name)
        if self_interface is None or other_interface is None:
            return
        for connection in self.connections:
            if connection[0][0] is self_interface and \
               connection[1][0] is other_interface:
                   self.disconnect_interface(connection[0][0])
        connection: Link = Link(speed, metrics)
        self_interface.connect_link(connection,
                                    connection.channels[0],
                                    connection.channels[1])
        other_interface.connect_link(connection,
                                     connection.channels[1],
                                     connection.channels[0])
        self_connection:  Tuple(Interface, Node) = (self_interface, self)
        other_connection: Tuple(Interface, Node) = (other_interface, __o)
        self.connections.append((self_connection, 
                                 other_connection))
        __o.connections.append((other_connection, 
                                self_connection))

    def disconnect_interface(self, name: str) -> None:
        """
        Disconnects an Interface and also disconnects the corresponding
        Interface on the other Node

        Parameters:
        name (str): The Interface's name to disconnect
        """
        self_interface: Interface = self.get_interface(name)
        if self_interface is None:
            return
        for item in self.connections:
            if item[0][0] is self_interface:
                other_interface: Interface = item[1][0]
                other_node:      Node      = item[1][1]
                self_interface.disconnect_link()
                self.connections.remove(item)
                other_interface.disconnect_link()
                for connection in other_node.connections:
                    if connection[0][0] is other_interface:
                        other_node.connections.remove(connection)
                        return

    def print_details(self) -> None:
        """
        Prints the details of the Node object - should not be called, only used
        because of the Python language server wouldn't help out with the method
        signature
        """
        raise NotImplementedError("Base class method call.")


class Host(Node):
    """
    Abstract Host in the Network
    These are the Nodes in the Network that handle sending and setting PPV

    Data members:
    name                            (str): Name of the Host
    ip                              (str): IP address of the Host
    send_rate                       (int): Sending rate (Packets / second)
    interfaces          (List[Interface]): Interfaces available on the Host
    connections (List[(Interface, Node), \
                      (Interface, Node)]): Host - Node connections
    routing_table          (RoutingTable): Routing table on the Host
    application             (Application): The Application on the Host
    """
    def __init__(self,
                 name: str,
                 ip: str,
                 send_rate: int,
                 ) -> None:
        super().__init__(name, ip, send_rate)
        self.application: Application = None

    def set_application(self, name: str, amount: int, send_rate: int) -> None:
        """
        Sets the Application and the send_rate accordingly in the Host

        Parameters:
        name      (str): Name of the Application
        amount    (int): Amount of Packets to send
        send_rate (int): Send rate of the Application
        """
        self.application = Application(name, self.ip, amount, send_rate)
        self.send_rate   = send_rate

    def send_packet(self, destination: str) -> str:
        """
        Leverages the Application to send a Packet

        Parameters:
        destination (str): IP address of the destination Node

        Returns:
        str: The next hop in the Route
        """
        # TODO check the Application's send rate, and adjust if needed
        if self.application.can_send():
            ppv: int = self.calculate_ppv()
            packet: Packet = self.application.send(destination, ppv)
            route: Route = self.get_best_route(destination)
            for interface in self.interfaces:
                if route.interface == interface.name:
                    print(f"Sent packet from {self.name}")
                    interface.put_to_link(packet)
                    return route.gateway

    def receive_packet(self, interface: Interface) -> None:
        """
        Handles an incoming Packet accordingly - consumes it in this case

        Parameters:
        interface (Interface): The Interface the Packet came from
        """
        packet: Packet = interface.receive_from_link()
        if packet is not None:
            print(f"Received packet on {self.name}")
            self.application.receive(packet)

    def receive_all_packets(self) -> None:
        """
        Receives all Packets on all Interfaces by going through all of them
        """
        # TODO Iterate over all interfaces and get all packets
        pass

    # TODO make it so that packages' PPV are not randomly generated
    def calculate_ppv(self) -> int:
        """
        Calculates the PPV for the next Packet.

        Returns:
        int: The calculated PPV value for the next Packet
        """
        return random.randint(1, 10)

    def print_details(self) -> None:
        """
        Prints details of the Host, listing every attribute of it
        """
        print(f"\nNODE {self.name} - {self.ip}:\n"
              f"Send rate: {self.send_rate} packets / s\n"
              f"Running application:\n{self.application}")
        self.routing_table.list_routes()
        print("---\nAvailable Interfaces on Node:")
        if len(self.interfaces) == 0:
            print("None")
        else:
            for interface in self.interfaces:
                print(interface)
        print("---\nAvailable connections to other Nodes:")
        if len(self.connections) == 0:
            print("None")
        else:
            for same_node, other_node in self.connections:
                print(f"{same_node[0]}\n-\nCONNECTED TO\n-\n{other_node[0]}\n")


class Router(Node):
    """
    Abstract Routes in the Network
    These are the Nodes in the Network that handle Packets marked with PPV

    Data members:
    name                            (str): Name of the Host
    ip                              (str): IP address of the Host
    send_rate                       (int): Sending rate (Packets / second)
    interfaces          (List[Interface]): Interfaces available on the Host
    connections (List[(Interface, Node), \
                      (Interface, Node)]): Host - Node connections
    routing_table          (RoutingTable): Routing table on the Host
    buffer                 (List[Packet]): Buffer for Packets to send out
    buffer_size                     (int): Maximum buffer size available
    """
    def __init__(self,
                 name: str,
                 ip: str,
                 send_rate: int,
                 buffer_size: int,
                 ) -> None:
        super().__init__(name, ip, send_rate)
        self.buffer:      List[Packet] = []
        self.buffer_size: int = buffer_size

    def lowest_buffer_ppv(self) -> Packet:
        """
        Gets the lowest PPV Packet in the buffer, or nothing

        Returns:
        Packet: The lowest PPV Packet or None
        """
        min_packet: Packet = None
        for packet in self.buffer:
            if min_packet is None or packet.ppv < min_packet.ppv:
                min_packet = packet
        return min_packet

    def send_packet(self) -> str:
        """
        Takes a Packet from the buffer, or nothing

        Returns:
        str: The next hop in the Route, or None
        """
        if len(self.buffer) > 0:
            print(f"Sent packet from {self.name}")
            packet: Packet = self.buffer.pop()
            route: Route = self.get_best_route(packet.target_ip)
            for interface in self.interfaces:
                if route.interface == interface.name:
                    interface.put_to_link(packet)
                    return route.gateway
        return None

    def receive_packet(self, interface: Interface) -> None:
        """
        Handles an incoming Packet accordingly
        Puts it in the buffer, or throws it away, since this is the step that
        compares PPV in Packets (lowest_buffer_ppv vs. incoming_ppv)

        Parameters:
        interface (Interface): The Interface the Packet came from
        """
        packet: Packet = interface.receive_from_link()
        if packet is not None:
            print(f"Received packet on {self.name}")
            if len(self.buffer) < self.buffer_size:
                self.buffer.append(packet)
            elif self.buffer_size != 0:
                buffer_packet: Packet = self.lowest_buffer_ppv()
                if buffer_packet.ppv < packet.ppv:
                    self.buffer.remove(buffer_packet)
                    print(f"Dropped from buffer:\n{buffer_packet}")
                else:
                    print(f"Dropped incoming packet:\n{packet}.")

    def receive_all_packets(self) -> None:
        """
        Receives all Packets on all Interfaces by going through all of them
        """
        pass

    def print_details(self) -> None:
        """
        Prints details of the Router, listing every attribute of it
        """
        print(f"\nNODE {self.name} - {self.ip}:\n"
              f"Send rate: {self.send_rate} packets / s\n"
              f"Buffer: {len(self.buffer)} / {self.buffer_size}")
        self.routing_table.list_routes()
        print("---\nAvailable Interfaces on Node:")
        if len(self.interfaces) == 0:
            print("None")
        else:
            for interface in self.interfaces:
                print(interface)
        print("---\nAvailable connections to other Nodes:")
        if len(self.connections) == 0:
            print("None")
        else:
            for same_node, other_node in self.connections:
                print(f"\n{same_node[0]}\n-\nCONNECTED TO\n-\n{other_node[0]}")
