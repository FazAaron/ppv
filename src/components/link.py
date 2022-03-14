from packet import Packet
from typing import List
import uuid


class Channel:
    def __init__(self,
                 speed: int,
                 metrics: int
                 ) -> None:
        self.speed:   int          = speed
        self.metrics: int          = metrics
        self.payload: List[Packet] = []

    def fill_payload(self, packet: Packet) -> None:
        self.payload.append(packet)

    def pop_payload(self) -> Packet:
        return self.payload.pop()

    def __str__(self) -> str:
        return (f"Speed: {self.speed} packet / second\n"
                f"Metrics: {self.metrics}\n"
                f"Payload: {len(self.payload)} packets")


class Link:
    """
    Abstract representation of a duplex link in the network, connecting 
    different Node objects.
    """

    def __init__(self, speed: int, metrics: int):
        self.uuid:     str = uuid.uuid4()
        self.channels: List[Channel] = \
            [Channel(speed, metrics), Channel(speed, metrics)]

    def __str__(self) -> str:
        return f"Link UUID: {self.uuid}\n{self.channels[0].__str__()}"
