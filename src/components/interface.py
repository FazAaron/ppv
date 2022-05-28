"""
This module makes Interface objects available for use when imported
"""
# Self-made modules
from src.components.link import Channel, Link
from src.components.packet import Packet


class Interface:
    """
    Abstract implementation of a Node interface.

    Data members:
    name                (str): String-based name given to the Interface
    link               (Link): Link connected to the Interface
    send_channel    (Channel): Sending Channel of the Link
    receive_channel (Channel): Receiving Channel of the Link
    """

    def __init__(self, name: str) -> None:
        self.name:            str = name
        self.link:            Link = None
        self.send_channel:    Channel = None
        self.receive_channel: Channel = None

    def connect_link(self,
                     link: Link,
                     send_channel: Channel,
                     receive_channel: Channel
                     ) -> bool:
        """
        Connects the Interface to a Link, and setting up sending and receiving

        Parameters:
        link               (Link): The Link to be connected to
        send_channel    (Channel): The Channel to set as the sending Channel
        receive_channel (Channel): The Channel to set as the receiving Channel
        """
        # Checks if the Link given as a parameter has everything set up
        # This by default should not happen, but better to check it
        if (link and send_channel and receive_channel) is None:
            return False

        # Set the Link and the Channels
        self.link = link
        self.send_channel = send_channel
        self.receive_channel = receive_channel

        return True

    def disconnect_link(self) -> int:
        """
        Disconnects from the Link and sets the Channels into a default state

        Returns:
        int: The Packets contained inside the send_channel and receive_channel \
             before disconnecting the Link
        """
        # Get the amount of Packets dropped
        packets_dropped: int = len(self.receive_channel.payload)

        # Set the Link and Channels to the default state
        self.link = None
        self.send_channel = None
        self.receive_channel = None

        return packets_dropped

    def receive_from_link(self) -> Packet:
        """
        Gets a Packet from the receiving Channel, or if it is empty, nothing

        Returns:
        Packet: The first Packet in the payload of the Channel or None
        """
        # Only receive from the Link if its payload is not empty
        if len(self.receive_channel.payload) != 0:
            return self.receive_channel.pop_payload()

        return None

    def put_to_link(self, packet: Packet) -> None:
        """
        Puts a packet onto the sending Channel

        Parameters:
        packet (Packet): The Packet to send through the sending Channel
        """
        self.send_channel.fill_payload(packet)

    def __str__(self) -> str:
        return (f"Interface name: {self.name}\n"
                f"Connected Link:\n{self.link}\n")
