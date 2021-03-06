"""
This module makes Application objects available for use when imported
"""
from src.components.packet import Packet


class Application:
    """
    Abstract implementation of an Application running on a Host machine\n

    Data members:
    name      (str): Name of the Application
    ip        (str): IP address of the Application (matches the Host's)
    amount    (int): Total Packets to send
    send_rate (int): How many Packets to send per second
    curr_sent (int): Total number of Packets sent since initialization
    app_type  (str): The type of the application (AIMD, CONST)
    """

    def __init__(self,
                 name: str,
                 ip: str,
                 amount: int,
                 send_rate: int,
                 app_type: str
                 ) -> None:
        self.name:      str = name
        self.ip:        str = ip
        self.amount:    int = amount
        self.send_rate: int = send_rate
        self.app_type:  str = app_type.upper()
        self.curr_sent: int = 0

    def can_send(self) -> bool:
        """
        Checks whether the Application still can (or wants to) send or not

        Returns:
        bool: Whether the Application can send or not (sent < max)
        """
        return self.curr_sent < self.amount

    def send(self, target_ip: str, ppv: int, size: int) -> Packet:
        """
        Creates a Packet that will be sent through the Network if the
        Application can send

        Parameters:
        target_ip (str): Destination to send the Packet to
        ppv       (int): The PPV to set (how valuable the Packet is)

        Returns:
        Packet: The Packet to send through the Network or None
        """
        # Check if the Application can actually send
        if self.can_send():
            # If yes, increase the sent Packets by 1, and return the Packet
            self.curr_sent += 1
            packet: Packet = Packet(self.ip, target_ip, ppv, size)
            return packet

        return None

    def receive(self, packet: Packet) -> None:
        """
        Handles a Packet coming in from the Node

        Parameters:
        packet (Packet): The Packet to handle
        """
        print(f"Received packet on {self.name}:\n{packet}")

    def __str__(self) -> str:
        return (f"{self.name} - {self.ip}:\n"
                f"Application type: {self.app_type}\n"
                f"Sent packets: {self.curr_sent} / {self.amount}\n"
                f"Send rate: {self.send_rate} Packet(s) / s")
