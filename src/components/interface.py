import uuid

from link import Channel, Link
from packet import Packet


class Interface:
    """
    Abstract implementation of a Node interface.

    Data members:
    uuid                (str): Unique ID that helps distinguish Interfaces
    name                (str): String-based name given to the Interface
    link               (Link): Link connected to the Interface
    send_channel    (Channel): Sending Channel of the Link
    receive_channel (Channel): Receiving Channel of the Link
    """

    def __init__(self, name: str) -> None:
        self.uuid:            str     = uuid.uuid4().hex
        self.name:            str     = name
        self.link:            Link    = None
        self.send_channel:    Channel = None
        self.receive_channel: Channel = None

    def connect_link(self,
                     link: Link,
                     send_channel: Channel,
                     receive_channel: Channel
                     ) -> None:
        """
        Connects the Interface to a Link, and setting up sending and receiving

        Parameters:
        link               (Link): The Link to be connected to
        send_channel    (Channel): The Channel to set as the sending Channel
        receive_channel (Channel): The Channel to set as the receiving Channel
        """
        self.link            = link
        self.send_channel    = send_channel
        self.receive_channel = receive_channel

    def disconnect_link(self) -> None:
        """
        Disconnects from the Link and sets the Channels into a default state
        """
        self.link            = None
        self.send_channel    = None
        self.receive_channel = None

    def receive_from_link(self) -> Packet:
        """
        Gets a Packet from the receiving Channel, or if it is empty, nothing

        Returns:
        Packet: The first Packet in the payload of the Channel or None
        """
        if len(self.receive_channel.payload) != 0:
            print("Received packet from link")
            return self.receive_channel.pop_payload()
        return None

    def put_to_link(self, packet: Packet) -> None:
        """
        Puts a packet onto the sending Channel
        
        Parameters:
        packet (Packet): The Packet to send through the sending Channel
        """
        print("Put packet on link")
        self.send_channel.fill_payload(packet)

    def __str__(self) -> str:
        return (f"Interface name: {self.name}\nInterface UUID: {self.uuid}\n"
                f"Connected link:\n{self.link}")
