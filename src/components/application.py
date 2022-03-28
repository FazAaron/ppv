from packet import Packet


class Application:
    def __init__(self,
                 name: str,
                 ip: str,
                 amount: int,
                 send_rate: int
                 ) -> None:
        self.name:      str = name
        self.ip:        str = ip
        self.amount:    int = amount
        self.send_rate: int = send_rate
        self.curr_sent: int = 0

    def can_send(self) -> bool:
        return self.curr_sent < self.amount

    def send(self, target_ip: str, ppv: int) -> Packet:
        self.curr_sent += 1
        packet: Packet = Packet(self.ip, target_ip, ppv)
        return packet

    def receive(self, packet: Packet) -> None:
        print(f"Received packet on {self.name}:\n{packet}")

    def __str__(self) -> str:
        return (f"APP {self.name} - {self.ip}:\n"
                f"Sent packets: {self.curr_sent} / {self.amount}\n"
                f"Send rate: {self.send_rate}")

class ConstantApplication(Application):
    pass

class AIMDApplication(Application):
    pass