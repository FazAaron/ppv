from typing import List, Tuple
from packet import Packet
from interface import Interface
import uuid

class Link:
    """
    Abstract representation of a duplex link in the network, connecting 
    different Node objects.
    """
    def __init__(self, speed: str) -> None:
        self.uuid:       str             = uuid.uuid4().hex
        self.speed:      str             = speed
        self.channels:   List[Packet]    = [None, None]
        self.interfaces: List[Interface] = [None, None]
        # TODO: creating (interface, channel) tuples, and store them like that
        # TODO: connect to interface(s) / disconnect from interface(s)

    def get_availability(self, interface: Interface) -> bool:
        """
        Checks if sending from that interface is possible, meaning that the
        link's corresponding channel is not occupied with sending.
        """
        send_channel_idx: int = self.get_corresponding_channel(interface)
        return self.channels[send_channel_idx] is not None

    def deliver_packet(self, interface: Interface) -> None:
        """
        Hand over the packet traveling on the channel which corresponds
        to the receiving interface
        """
        send_channel_idx: int = self.get_corresponding_channel(interface)
        rec_channel_idx: int = (send_channel_idx + 1) % 2
        # TODO: give it to the interface - self.interfaces[rec_channel_idx].receive_packet(channels[send_channel_idx])
        self.channels[send_channel_idx] = None
        pass
    
    def receive_packet(self, interface: Interface, packet: Packet) -> None:
        """
        Puts the received packet from the interface to it's corresponding
        sending channel.
        """
        send_channel_idx: int = self.get_corresponding_channel(interface)
        self.channels[send_channel_idx] = packet

    def get_corresponding_channel(self, interface: Interface) -> int:
        return self.interfaces.index(interface)
