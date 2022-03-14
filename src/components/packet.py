import uuid


class Packet:
    """
    A simplified network packet representation
    """

    def __init__(self,
                 source_ip: str,
                 target_ip: str,
                 ppv: int,
                 ) -> None:
        self.uuid:      str = uuid.uuid4()
        self.source_ip: str = source_ip
        self.target_ip: str = target_ip
        self.ppv:       int = ppv

    def __str__(self) -> str:
        """
        Overriding the default behaviour of the string representation for
        Packet objects
        """
        return (f"ID: {self.uuid}\n"
                f"Source IP: {self.source_ip}\nTarget IP: {self.target_ip}\n"
                f"PPV: {self.ppv}")
