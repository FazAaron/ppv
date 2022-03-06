class Packet:
    """
    A simplified network packet representation
    """
    def __init__(self, 
                 source_ip: str, 
                 target_ip: str, 
                 ppv: int, 
                 size: int
    ) -> None:
        self.source_ip: str = source_ip
        self.target_ip: str = target_ip
        self.ppv:       int = ppv
        self.size:      int = size
