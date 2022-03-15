from __future__ import annotations
from application import Application
from packet import Packet
from routing_table import RoutingTable, Route
from interface import Interface
from typing import List
from link import Link
import random

# TODO implement discover_routes to be a proper routing table population algorithm


class Node:
    def __init__(self, name: str, ip: str, send_rate: int) -> None:
        self.name:          str = name
        self.ip:            str = ip
        self.send_rate:     int = send_rate
        self.interfaces:    List[Interface] = []
        self.connections:   List[(Interface, Interface)] = []
        self.routing_table: RoutingTable = RoutingTable()

    def add_route(self, route: Route) -> None:
        self.routing_table.set_route(route)

    # TODO
    def discover_routes(self) -> None:
        pass

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
        for (ownx, owny), (otherx, othery) in \
                zip(self.connections, __o.connections):
            if ownx is self_interface and owny is other_interface and \
                    otherx is other_interface and othery is self_interface:
                return
        connection: Link = Link(speed, metrics)
        self_interface.connect_link(connection,
                                    connection.channels[0],
                                    connection.channels[1])
        other_interface.connect_link(connection,
                                     connection.channels[1],
                                     connection.channels[0])
        self.connections.append((self_interface, other_interface))
        __o.connections.append((other_interface, self_interface))

    def disconnect_from_interface(self,
                                  self_interface: Interface,
                                  other_interface: Interface
                                  ) -> None:
        for item in self.connections:
            if item[0] is self_interface and item[1] is other_interface:
                self_interface.disconnect_link()
                other_interface.disconnect_link()
                self.connections.remove(item)
                return

    def send_packet(self) -> None:
        raise NotImplementedError("Base class method call.")

    def receive_packet(self) -> None:
        raise NotImplementedError("Base class method call.")


class Host(Node):
    def __init__(self,
                 name: str,
                 ip: str,
                 send_rate: int,
                 ) -> None:
        super().__init__(name, ip, send_rate)
        self.application = None

    def set_application(self, name: str, amount: int) -> None:
        self.application: Application = \
            Application(name, self.ip, amount, self.send_rate)

    def set_ip(self, ip: str) -> None:
        self.ip = ip
        self.application.ip = ip

    def set_send_rate(self, send_rate: int) -> None:
        self.send_rate = send_rate
        self.application.send_rate = send_rate

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
                print(f"\n{same_node}\n---\nCONNECTED TO\n---\n{other_node}")


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
                print(f"\n{same_node}\n---\nCONNECTED TO\n---\n{other_node}")
