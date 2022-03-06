class Route:
    """
    Abstract representation of routes in a routing table
    """
    def __init__(self, 
                 destination: str, 
                 gateway:     str, 
                 subnet_mask: str, 
                 interface:   str, 
                 metrics:     int
    ) -> None:
        self.destination: str = destination
        self.gateway:     str = gateway
        self.subnet_mask: str = subnet_mask # might be removed in the future
        self.interface:   str = interface
        self.metrics:     int = metrics

    def __eq__(self, __o: object) -> bool:
        """
        Overriding the behaviour of the = operator on Route objects
        """
        if isinstance(__o, self.__class__):
            return __o.destination == self.destination and\
                   __o.gateway == self.gateway and\
                   __o.subnet_mask == self.subnet_mask and\
                   __o.interface == self.interface and\
                   __o.metrics == self.metrics
        return False

    def __str__(self) -> str:
        """
        Overriding the behaviour of the string representation of
        Route objects
        """
        return (f"Destination: {self.destination}\n"
                f"Gateway: {self.gateway}\n"
                f"Subnet Mask: {self.subnet_mask}\n"
                f"Interface: {self.interface}\n"
                f"Metrics: {self.metrics}")
