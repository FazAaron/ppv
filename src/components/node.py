"""
This module makes Node, Host and Router objects available for use when imported
"""

# Built-in modules
from __future__ import annotations # Needed to be able to store
                                   # the same object as the class itself
import random
from typing import List, Tuple

# Self-made modules
from src.components.application import Application
from src.components.interface import Interface
from src.components.link import Link
from src.components.packet import Packet
from src.components.routing_table import Route, RoutingTable


class Node:
    """
    Abstract implementation of a Node in a Network\n
    This being the main component, handles most of the logic\n
    Base class for Host and Router

    Data members:
    name                            (str): Name of the Node
    ip                              (str): IP address of the Node
    send_rate                       (int): Sending rate (Packets / second)
    interfaces          (List[Interface]): Interfaces available on the Node
    connections  (List[(Interface, Node), \
                      (Interface, Node)]): Node - Node connections
    routing_table          (RoutingTable): Routing table on the Node
    """

    def __init__(self, name: str, ip: str, send_rate: int) -> None:
        self.name:          str = name
        self.ip:            str = ip
        self.send_rate:     int = send_rate
        self.interfaces:    List[Interface] = []
        self.connections:   List[Tuple[Tuple[Interface, Node],
                                 Tuple[Interface, Node]]] = []
        self.routing_table: RoutingTable = RoutingTable()

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

        # Check for the best possible Route, comparing metrics
        # The first Route with the lowest metrics will be the best Route
        for route in self.routing_table.routes:
            if route.destination == destination:
                if best_route is None:
                    best_route = route
                elif best_route.metrics > route.metrics:
                    best_route = route

        return best_route

    def reset_routes(self):
        """
        Resets the Node's RoutingTable to a default state - making it empty
        """
        self.routing_table.reset_routes()

    def add_interface(self, name: str) -> bool:
        """
        Adds an Interface to the Node if it does not match an already existing
        Interface's name

        Parameters:
        name (str): The name of the new Interface to add

        Returns:
        bool: Whether adding the Interface was successful or not
        """
        # Check if there is already an Interface with the given name
        for interface in self.interfaces:
            if interface.name == name:
                return False

        self.interfaces.append(Interface(name))
        return True

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

    def delete_interface(self, name: str) -> Tuple[bool, int]:
        """
        Deletes an Interface on the Node\n
        Before deletion, the Interface is disconnected and is removed from all
        connections

        Parameters:
        name (str): The Interface's name to delete

        Returns:
        Tuple[bool, int]: Whether deleting the interface was successful or not \
                          and the amount of Packets dropped
        """
        interface: Interface = self.get_interface(name)
        pack_dropped: int = 0

        # Check if the given Interface is actually present on the Node
        if interface is None:
            return (False, pack_dropped)

        # Disconnect the Interface, if it is connected
        for connection in self.connections:
            if connection[0][0] == interface:
                # Check if any Packets were dropped
                # No need to check the first (0) index of the return, since
                # we already checked whether the Interface exists or not
                pack_dropped = self.disconnect_interface(name)[1]
                break

        self.interfaces.remove(interface)
        return (True, pack_dropped)

    def connect_to_interface(self,
                             __o: Node,
                             self_name: str,
                             other_name: str,
                             speed: int,
                             metrics: int
                             ) -> Tuple[bool, int]:
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

        Returns:
        Tuple[bool, int]: Whether creating the connection was successful or not \
                          and how many Packets were dropped
        """
        pack_dropped: int = 0

        # Check if the __o Node is equal to the Node itself
        if self is __o:
            return (False, pack_dropped)

        # Checks whether the given Interfaces are actually present on the Nodes
        self_interface:  Interface = self.get_interface(self_name)
        other_interface: Interface = __o.get_interface(other_name)
        if (self_interface and other_interface) is None:
            return (False, pack_dropped)

        # Check if any Packets were dropped
        # No need to check the first (0) index of the return, since
        # we already checked whether the Interface exists or not
        pack_dropped = self.disconnect_interface(self_name)[1]
        __o.disconnect_interface(other_name)

        # Connect the Interfaces
        connection: Link = Link(speed, metrics)
        self_success: bool = self_interface.connect_link(connection,
                                                         connection.channels[0],
                                                         connection.channels[1])
        other_success: bool = other_interface.connect_link(connection,
                                                           connection.channels[1],
                                                           connection.channels[0])

        # Check if connection was successful, if yes, add the new connection to
        # both Nodes' connection table
        if (self_success and other_success):
            self_connection:  Tuple(Interface, Node) = (self_interface, self)
            other_connection: Tuple(Interface, Node) = (other_interface, __o)
            self.connections.append((self_connection,
                                    other_connection))
            __o.connections.append((other_connection,
                                    self_connection))
            return (True, pack_dropped)

        return (False, pack_dropped)

    def disconnect_interface(self, name: str) -> Tuple[bool, int]:
        """
        Disconnects an Interface and also disconnects the corresponding
        Interface on the other Node

        Parameters:
        name (str): The Interface's name to disconnect

        Returns:
        Tuple[bool, int]: Whether disconnecting the Interface was successful or not, \
                          and how many Packets were dropped
        """
        self_interface: Interface = self.get_interface(name)
        pack_dropped: int = 0

        # Check if the given Interface is actually present on the Node
        if self_interface is None:
            return (False, pack_dropped)

        # Check if the Interface is connected
        for item in self.connections:
            if item[0][0] is self_interface:
                # Get the other Node's information
                other_interface: Interface = item[1][0]
                other_node:      Node = item[1][1]

                # Check if any Packets were dropped, and remove the connection
                pack_dropped = self_interface.disconnect_link()
                self.connections.remove(item)

                # Check if any Packets were dropped, and remove the connection
                # on the other Node as well
                pack_dropped += other_interface.disconnect_link()
                for connection in other_node.connections:
                    if connection[0][0] is other_interface:
                        other_node.connections.remove(connection)
                        return (True, pack_dropped)

        return (True, pack_dropped)

    def receive_feedback(self, packet_source: str, feedback: int) -> None:
        """
        Receives feedback - should not be called, only used
        because of polymorphism's sake
        """
        raise NotImplementedError("Base class method call.")


class Host(Node):
    """
    Abstract Host in the Network\n
    These are the Nodes in the Network that handle creating Packets and
    setting PPV

    Data members:
    name                            (str): Name of the Host
    ip                              (str): IP address of the Host
    send_rate                       (int): Sending rate (Packets / second)
    interfaces          (List[Interface]): Interfaces available on the Host
    connections (List[(Interface, Node), \
                      (Interface, Node)]): Host - Node connections
    routing_table          (RoutingTable): Routing table on the Host
    application             (Application): The Application on the Host
    ppv_received            (int): The PPV sum of the Packets received
    ppv_sent                (int): The PPV sum of the Packets sent
    """

    def __init__(self,
                 name: str,
                 ip: str,
                 send_rate: int,
                 ) -> None:
        super().__init__(name, ip, send_rate)
        self.application: Application = None
        self.ppv_received: int = 0
        self.ppv_sent:     int = 0

    def set_application(self,
                        name: str,
                        amount: int,
                        send_rate: int,
                        app_type: str) -> None:
        """
        Sets the Application and the send_rate accordingly in the Host

        Parameters:
        name      (str): Name of the Application
        amount    (int): Amount of Packets to send
        send_rate (int): Send rate of the Application
        app_type  (str): Type of the Application - AIMD or CONST
        """
        self.application = \
            Application(name, self.ip, amount, send_rate, app_type)
        # The Application and Host send rate should always be equal
        self.send_rate = send_rate

    def send_packet(self, destination: str) -> Tuple[str, str]:
        """
        Leverages the Application to send a Packet

        Parameters:
        destination (str): IP address of the destination Node

        Returns:
        Tuple[str, str]: The next hop in the Route and the receiving Interface
        """
        # Check if the destination we would like to send to is equal to this Host
        if destination == self.ip:
            return None

        # Only send, if the Application still have Packets to send
        if self.application.can_send():
            # Get the PPV, and get the corresponding Packet
            # Also fetch the best possible Route to the destination
            # Currently, the size of a Packet does not matter, because
            # there is no policy enforced that could use it
            ppv: int = self.calculate_ppv()
            packet: Packet = self.application.send(destination, ppv,
                                                   random.randint(1, 10))
            route: Route = self.get_best_route(destination)

            # Check if the destination can be reached, and the Packet was created
            if (route and packet) is None:
                return None

            # Go through the Interfaces until we find the one that matches the
            # one given by the Route
            for interface in self.interfaces:
                if route.interface == interface.name:
                    # Go through the connections, so that we can actually get
                    # the Interface the Packet will be received on for future use
                    for connection in self.connections:
                        if connection[0][0].name == interface.name:
                            receiver_interface = connection[1][0].name
                            break

                    # Put the Packet to the Link
                    interface.put_to_link(packet)

                    # Save the PPV for statistics in Network
                    self.ppv_sent += ppv

                    # Return the next hop and it's corresponding receiver Interface
                    return route.gateway, receiver_interface

        return None

    def receive_packet(self, name: str) -> bool:
        """
        Handles an incoming Packet accordingly - consumes it in this case

        Parameters:
        name (str): The Interface's name the Packet came from

        Returns:
        bool: Whether receiving the Packet was a success or not
        """
        interface: Interface = self.get_interface(name)

        # Check if the Interface actually exists on the Host
        if interface is None:
            return False

        # Get the Packet from the Link connected to the Interface
        packet: Packet = interface.receive_from_link()

        # Check if there was actually a Packet to receive
        if packet is not None:
            # Pass the Packet to the Application
            self.application.receive(packet)

            # Save the PPV for statistics in Network
            self.ppv_received += packet.ppv
            return True

        return False

    def __handle_feedback(self, feedback: int) -> None:
        """
        Adjusts sending rate on the Node and Application based on feedback

        Parameters:
        feedback (int): The feedback received from the Router
        """
        # If the feedback was positive (the buffer was not full), we can increase
        # the speed
        if feedback == 1:
            self.send_rate += 1
            self.application.send_rate += 1
            if self.send_rate > 9:
                self.send_rate = 9
                self.application.send_rate = 9
        # If the feedback was negative (the buffer was full), we need to decrease
        # the speed the Host is sending at
        elif feedback == -1:
            self.send_rate //= 2
            self.application.send_rate //= 2
            if self.send_rate == 0:
                self.send_rate = 1
                self.application.send_rate = 1

    def receive_feedback(self, packet_source: str, feedback: int) -> None:
        """
        Gets a feedback from the receiving Node in the Network,
        and adjusts the sending rate according to that (if needed)

        Parameters:
        packet_source (str): This Node's IP address
        feedback      (int): The feedback data being sent back
        """
        # Check if the Host's type is equal to AIMD or not - only that type of
        # Host has an use for the feedback mechanism
        if self.application.app_type == "AIMD":
            # Only handle the feedback when the Packet was sent from here
            # (should always be the case, unless some logical error occurs)
            if packet_source == self.ip:
                self.__handle_feedback(feedback)

    def __nine_color_gold(self) -> int:
        """
        Gives a random PPV based on what the actual send_rate is
        """
        return random.randint(10 - self.send_rate, 9)

    def calculate_ppv(self) -> int:
        """
        Calculates the PPV for the next Packet \n
        This is a specific, simple policy, and thus new policies can be
        easily added for future use

        Returns:
        int: The calculated PPV value for the next Packet
        """
        return self.__nine_color_gold()

    def __str__(self) -> str:
        to_return: str = ""
        to_return += (f"\nHOST {self.name} - {self.ip}:\n\n"
                      f"Send rate: {self.send_rate} Packet(s) / s\n\n"
                      f"Running Application:\n{self.application}\n\n")
        to_return += self.routing_table.__str__()
        to_return += "\n\nAvailable Interfaces on Node:\n"
        if len(self.interfaces) == 0:
            to_return += ("There are no Interfaces on the Node.")
        else:
            for interface in self.interfaces:
                to_return += interface.__str__()
        to_return += "\n\nAvailable connections to other Nodes:\n"
        if len(self.connections) == 0:
            to_return += "There are no connections to other Nodes."
        else:
            for same_node, other_node in self.connections:
                to_return += f"{same_node[0]}\n-\nCONNECTED TO\n-\n{other_node[0]}\n"
        return to_return


class Router(Node):
    """
    Abstract Routes in the Network\n
    These are the Nodes in the Network that handle Packets marked with PPV

    Data members:
    name          (str): Name of the Host
    ip            (str): IP address of the Host
    send_rate     (int): Sending rate (Packets / second)
    interfaces    (List[Interface]): Interfaces available on the Host
    connections   (List[(Interface, Node), \
                        (Interface, Node)]): Host - Node connections
    routing_table (RoutingTable): Routing table on the Host
    buffer        (List[Packet]): Buffer for Packets to send out
    buffer_size   (int): Maximum buffer size available
    ppv_dropped   (int): The PPV sum of Packets dropped, only accounted for \
                  when the algorithm drops it
    """

    def __init__(self,
                 name: str,
                 ip: str,
                 send_rate: int,
                 buffer_size: int,
                 ) -> None:
        super().__init__(name, ip, int(send_rate))
        self.buffer:      List[Packet] = []
        self.buffer_size: int = 0 if buffer_size < 0 else buffer_size
        self.ppv_dropped: int = 0

    def get_buffer_length(self) -> int:
        """
        Gets the total amount of Packets inside the Buffer

        Returns:
        int: The Packets inside the buffer
        """
        return len(self.buffer)

    def lowest_buffer_ppv(self) -> Packet:
        """
        Gets the lowest PPV Packet in the buffer if there is any

        Returns:
        Packet: The lowest PPV Packet or None
        """
        min_packet: Packet = None

        # Go through the buffer to check for the lowest PPV Packet
        for packet in self.buffer:
            if min_packet is None or packet.ppv < min_packet.ppv:
                min_packet = packet

        return min_packet

    def send_packet(self) -> Tuple[str, str]:
        """
        Takes a Packet from the buffer, or nothing

        Returns:
        Tuple[str, str]: The next hop in the Route and the receiving Interface
        """
        # Check if the buffer has any Packet to send
        if len(self.buffer) > 0:
            # Get the next Packet to send, and the best Route for it to send it
            # through
            packet: Packet = self.buffer.pop()
            route: Route = self.get_best_route(packet.target_ip)

            # Check if the destination can be reached, and the Packet was popped
            if (route and packet) is None:
                return None

            # Go through the Interfaces until we find the one that matches the
            # one given by the Route
            for interface in self.interfaces:
                if route.interface == interface.name:
                    for connection in self.connections:
                        # Go through the connections, so that we can actually get
                        # the Interface the Packet will be received on for future use
                        if connection[0][0].name == interface.name:
                            receiver_interface = connection[1][0].name
                            break

                    # Put the Packet to the Link
                    interface.put_to_link(packet)

                    # Return the next hop and it's corresponding receiver Interface
                    return route.gateway, receiver_interface

        return None

    def receive_packet(self, name: str) -> Tuple[bool, bool]:
        """
        Handles an incoming Packet accordingly\n
        Puts it in the buffer, or throws it away, since this is the step that
        compares PPV in Packets (lowest_buffer_ppv vs. incoming_ppv)\n
        Also sends a feedback to the source of the Packet

        Parameters:
        name (str): The Interface's name the Packet came from

        Returns:
        Tuple[bool, bool]: Whether receiving the Packet was a success or not \
                           and whether the incoming Packet or one from the \
                           buffer was dropped
        """
        dropped_pack: bool = False
        interface: Interface = self.get_interface(name)

        # Check if the Interface actually exists on the Router
        if interface is None:
            return (False, dropped_pack)

        # Get the Packet from the Link connected to the Interface
        packet: Packet = interface.receive_from_link()

        # Check if there was actually a Packet to receive
        if packet is not None:
            # Check if there is still space in the buffer
            if len(self.buffer) < self.buffer_size:
                # If there is, simply just add it to the buffer, and send a
                # positive feedback
                self.buffer.append(packet)
                self.__send_feedback(packet.source_ip, 1)
                return (True, dropped_pack)
            if len(self.buffer) == self.buffer_size:
                # If there is none, get the lowest PPV Packet from the Buffer
                buffer_packet: Packet = self.lowest_buffer_ppv()

                # Drop the Packet from the buffer or the incoming one, based on
                # which one has a lower PPV
                if buffer_packet.ppv < packet.ppv:
                    self.buffer.remove(buffer_packet)
                    self.buffer.append(packet)
                    self.ppv_dropped += buffer_packet.ppv
                else:
                    self.ppv_dropped += packet.ppv

                dropped_pack = True

                # Send a negative feedback to the source of the Packet
                self.__send_feedback(packet.source_ip, -1)
                return (True, dropped_pack)

        return (False, dropped_pack)

    def __send_feedback(self, packet_source: str, feedback: int) -> None:
        """
        Sends feedback data to the Node the Packet was received from

        Parameters:
        packet (Packet): The received Packet's source IP
        feedback  (int): The feedback data being sent back
        """
        route: Route = self.get_best_route(packet_source)
        if route is None:
            return
        from_ip: str = route.gateway

        # Send the feedback to a neighbouring Node, so that it can keep passing
        # it on, or handle it
        for connection in self.connections:
            if connection[1][1].ip == from_ip:
                connection[1][1].receive_feedback(packet_source, feedback)

    def receive_feedback(self, packet_source: str, feedback: int) -> None:
        """
        Receives feedback data, sending it to the intended Node

        Parameters:
        packet_source (str): The source to send feedback to
        feedback      (int): The feedback data being sent back
        """
        self.__send_feedback(packet_source, feedback)

    def __str__(self) -> str:
        to_return: str = ""
        to_return += (f"\nROUTER {self.name} - {self.ip}:\n\n"
                      f"Send rate: {self.send_rate} Packet(s) / s\n\n"
                      f"Buffer: {len(self.buffer)} / {self.buffer_size}\n\n")
        to_return += self.routing_table.__str__()
        to_return += "\n\nAvailable Interfaces on Node:\n"
        if len(self.interfaces) == 0:
            to_return += ("There are no Interfaces on the Node.")
        else:
            for interface in self.interfaces:
                to_return += interface.__str__()
        to_return += "\n\nAvailable connections to other Nodes:\n"
        if len(self.connections) == 0:
            to_return += "There are no connections to other Nodes."
        else:
            for same_node, other_node in self.connections:
                to_return += f"{same_node[0]}\n-\nCONNECTED TO\n-\n{other_node[0]}\n"
        return to_return
