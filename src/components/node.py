from __future__ import annotations
from application import Application
from packet import Packet
from routing_table import RoutingTable, Route
from interface import Interface
from typing import List, Tuple
from link import Link
import random


class Node:
    def __init__(self, name: str, ip: str, send_rate: int) -> None:
        self.name:          str = name
        self.ip:            str = ip
        self.send_rate:     int = send_rate
        self.interfaces:    List[Interface] = []
        self.connections:   List[(Interface, Node), (Interface, Node)] = []
        self.routing_table: RoutingTable = RoutingTable()

    def add_route(self, route: Route) -> None:
        self.routing_table.set_route(route)

    def get_best_route(self, destination: str) -> Route:
        best_route: Route = None
        for route in self.routing_table.routes:
            if route.destination == destination:
                if best_route is None:
                    best_route = route
                elif best_route.metrics > route.metrics:
                    best_route = route
        return best_route

    def get_interface(self, name: str) -> Interface:
        for interface in self.interfaces:
            if interface.name == name:
                return interface
        return None

    def add_interface(self, name: str) -> None:
        for interface in self.interfaces:
            if interface.name == name:
                return
        self.interfaces.append(Interface(name))

    def delete_interface(self, name: str) -> None:
        for connection in self.connections:
            if connection[0][0].name == name:
               self.disconnect_from_interface(connection[1][1],
                                              connection[0][0],
                                              connection[1][0]) 
        for interface in self.interfaces:
            if interface.name == name:
                self.interfaces.remove(interface)

    def connect_to_interface(self,
                             __o: Node,
                             self_interface: Interface,
                             other_interface: Interface,
                             speed: int,
                             metrics: int
                             ) -> None:
        for connection in self.connections:
            if connection[0][0] is self_interface and \
               connection[1][0] is other_interface:
                   for o_connection in __o.connections:
                       if o_connection[0][0] is other_interface and \
                          o_connection[1][0] is self_interface:
                              self.connections.remove(connection)
                              __o.connections.remove(o_connection)
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

    def disconnect_from_interface(self,
                                  __o: Node,
                                  self_interface: Interface,
                                  other_interface: Interface
                                  ) -> None:
        for item in self.connections:
            if item[0][0] is self_interface and item[1][0] is other_interface:
                self_interface.disconnect_link()
                self.connections.remove(item)
                other_interface.disconnect_link()
                for connection in __o.connections:
                    if connection[0][0] is item[1][0]:
                        __o.connections.remove(connection)
                return

    def send_packet(self) -> None:
        raise NotImplementedError("Base class method call.")

    def receive_packet(self) -> None:
        raise NotImplementedError("Base class method call.")

    def print_details(self) -> None:
        raise NotImplementedError("Base class method call.")


class Host(Node):
    def __init__(self,
                 name: str,
                 ip: str,
                 send_rate: int,
                 ) -> None:
        super().__init__(name, ip, send_rate)
        self.application = None

    def set_application(self, name: str, amount: int, send_rate: int) -> None:
        self.application: Application = \
            Application(name, self.ip, amount, send_rate)
        self.send_rate = send_rate

    def send_packet(self, destination: str) -> str:
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
        packet: Packet = interface.receive_from_link()
        if packet is not None:
            print(f"Received packet on {self.name}")
            self.application.receive(packet)

    # TODO make it so that packages' PPV are not randomly generated
    def calculate_ppv(self) -> int:
        return random.randint(1, 10)

    def print_details(self) -> None:
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
        min_packet: Packet = None
        for packet in self.buffer:
            if min_packet is None or packet.ppv < min_packet.ppv:
                min_packet = packet
        return min_packet

    def send_packet(self) -> str:
        if len(self.buffer) > 0:
            print(f"Sent packet from {self.name}")
            packet: Packet = self.buffer.pop()
            route: Route = self.get_best_route(packet.target_ip)
            for interface in self.interfaces:
                if route.interface == interface.name:
                    interface.put_to_link(packet)
                    return route.gateway

    def receive_packet(self, interface: Interface) -> None:
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

    def print_details(self) -> None:
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
