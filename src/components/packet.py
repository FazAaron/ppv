"""
This module makes Packet objects available for use when imported
"""

class Packet:
    """
    A simplified network packet representation

    Data members:
    source_ip (str): What Node IP the Packet was created at
    target_ip (str): What is the Node destination IP of the Packet
    ppv       (int): Per-packet value, used by aggregate points in the Network
                     Used by the proposed algorithm's logic to handle Packets
    """

    def __init__(self,
                 source_ip: str,
                 target_ip: str,
                 ppv: int,
                 ) -> None:
        self.source_ip: str = source_ip
        self.target_ip: str = target_ip
        self.ppv:       int = ppv if ppv > 0 else 1

    def __str__(self) -> str:
        return (f"Source IP: {self.source_ip}\nTarget IP: {self.target_ip}\n"
                f"PPV: {self.ppv}")
