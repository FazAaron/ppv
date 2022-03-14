import uuid

from components.packet import Packet


class Application:
    def __init__(self,
                 ip: str,
                 name: str,
                 amount: int,
                 send_rate: int
                 ) -> None:
        self.ip:        str = ip
        self.name:      str = name
        self.amount:    int = amount
        self.send_rate: int = send_rate
        self.uuid:      str = uuid.uuid4
        self.curr_sent: int = 0

    def can_send(self) -> bool:
        return self.curr_sent != self.amount

    def send(self, target_ip: str, ppv: int) -> Packet:
        self.curr_sent += 1
        packet: Packet = Packet(self.ip, target_ip, ppv)
        return packet

    def receive(self, packet: Packet) -> None:
        print(f"Received packet on {self.name}:\n{packet}")
