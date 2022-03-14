import uuid
from link import Channel, Link
from packet import Packet


class Interface:
    """
    Abstract implementation of a Node interface.
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
        self.link = link
        self.send_channel = send_channel
        self.receive_channel = receive_channel

    def disconnect_link(self) -> None:
        self.link = None
        self.send_channel = None
        self.receive_channel = None

    def receive_from_link(self) -> Packet:
        if len(self.receive_channel.payload) != 0:
            return self.receive_channel.pop_payload()
        return None

    def put_to_link(self, packet: Packet) -> None:
        self.send_channel.fill_payload(packet)

    def __str__(self) -> str:
        return (f"Interface name: {self.name}\nInterface UUID: {self.uuid}\n"
                f"Connected link:\n{self.link}")
