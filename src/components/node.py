from queue import Queue
import uuid
from application import Application
from packet import Packet
from routing_table import RoutingTable, Route
from interface import Interface
from typing import List
from link import Link
import sys


# TODO implement discover_routes to be a proper routing table population algorithm
class Node:
    def __init__(self, name: str, ip: str, send_rate: int) -> None:
        self.uuid:          str = uuid.uuid4()
        self.name:          str = name
        self.ip:            str = ip
        self.send_rate:     int = send_rate
        self.interfaces:    List[Interface] = []
        self.connections:   List[(Interface, Interface)] = []
        self.routing_table: RoutingTable = RoutingTable()

    def add_route(self, route: Route) -> None:
        self.routing_table.set_route(route)

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
                             self_interface: Interface,
                             other_interface: Interface,
                             speed: int,
                             metrics: int
                             ) -> None:
        for own, other in self.connections:
            if own is self_interface and other is other_interface:
                return
        connection: Link = Link(speed, metrics)
        self_interface.connect_link(connection[0], connection[1])
        other_interface.connect_link(connection[1], connection[0])
        self.connections.append((self_interface, other_interface))

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
    def __init__(self, name: str, ip: str, application: Application) -> None:
        super().__init__(name, ip)
        self.application = application

    def set_application(self, application: Application) -> None:
        self.application = application

    def send_packet(self, destination: str, ppv: int) -> None:
        if self.application.can_send():
            packet: Packet = self.application.send(destination, ppv)
            route: Route = self.get_best_route(destination)
            for interface in self.interfaces:
                if route.interface == interface.name:
                    interface.put_to_link(packet)
                    return

    def receive_packet(self, interface: Interface) -> None:
        packet: Packet = interface.receive_from_link()
        if packet is not None:
            self.application.receive(packet)

    def calculate_ppv(self) -> None:
        pass


class Router(Node):
    def __init__(self,
                 name: str,
                 ip: str,
                 buffer_size: int,
                 send_rate: int) -> None:
        super().__init__(name, ip)
        self.buffer:      List[Packet] = []
        self.buffer_size: int = buffer_size
        self.send_rate:   int = send_rate

    def lowest_buffer_ppv(self) -> Packet:
        min_packet: Packet = None
        for packet in self.buffer:
            if min_packet is None or packet.ppv < min_packet.ppv:
                min_packet = packet

    def send_packet(self) -> None:
        packet: Packet = self.buffer.pop()
        route: Route = self.get_best_route(packet.target_ip)
        for interface in self.interfaces:
            if route.interface == interface.name:
                interface.put_to_link(packet)
                return

    def receive_packet(self, interface: Interface) -> None:
        packet: Packet = interface.receive_from_link()
        if packet is not None:
            if len(self.buffer) < self.buffer_size:
                self.buffer.append(packet)
            elif self.buffer_size != 0:
                buffer_packet: Packet = self.lowest_buffer_ppv()
                if buffer_packet.ppv < packet.ppv:
                    self.buffer.remove(buffer_packet)
                    print(f"Dropped {buffer_packet} from buffer.")
                else:
                    print(f"Dropped incoming {packet}.")