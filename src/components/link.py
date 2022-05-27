"""
This module makes Channel and Link objects available for use when imported
"""
# Built-in modules
from typing import List

# Self-made modules
from src.components.packet import Packet


class Channel:
    """
    Abstract representation of a one-directional dataflow in a duplex Link

    Data members:
    speed           (int): 1 / speed is the time needed for the Packet to pass \
                    through the Channel
    metrics         (int): Abstract immutable metric number set upon creation
    payload: List[Packet]: Packets currently traveling through the Channel
    """

    def __init__(self,
                 speed: int,
                 metrics: int
                 ) -> None:
        self.speed:   int = speed
        self.metrics: int = metrics
        self.payload: List[Packet] = []

    def fill_payload(self, packet: Packet) -> None:
        """
        Adds a Packet to the payload to send it to the receiving side

        Parameters:
        packet (Packet): The packet to send through the Channel
        """
        self.payload.append(packet)

    def pop_payload(self) -> Packet:
        """
        Removes and returns the first element from the payload

        Returns:
        Packet: The Packet added first or None if the payload is empty
        """
        # The try-except block is needed in case there is no item present in the
        # payload, because the List default behaviour throws an exception in that
        # case
        try:
            return self.payload.pop(0)
        except IndexError:
            return None

    def __str__(self) -> str:
        return (f"Speed: {1 / self.speed} second(s) / Packet\n"
                f"Metrics: {self.metrics}\n")


class Link:
    """
    Abstract representation of a duplex link in the network, connecting
    different Node objects.

    Data members:
    speed   (int): 1 / speed is the time needed for the Packet to pass through \
            the Link
    metrics (int): Abstract immutable metric number set upon creation
    """

    def __init__(self, speed: int, metrics: int):
        self.channels: List[Channel] = \
            [Channel(speed, metrics), Channel(speed, metrics)]

    def __str__(self) -> str:
        return f"Link:\n---\n{self.channels[0]}"
