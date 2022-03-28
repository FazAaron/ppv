from multiprocessing.sharedctypes import Value
from typing import List


class Route:
    """
    Abstract representation of Routes

    Data members:
    destination (str): What is the destination the given Route leads to
    gateway     (str): The next hop in the Network to go to
    interface   (str): The Interface's name to go through to get to the gateway
    metrics     (int): The Route's metrics which are specified in a Link object
    """

    def __init__(self,
                 destination: str,
                 gateway:     str,
                 interface:   str,
                 metrics:     int
                 ) -> None:
        self.destination: str = destination
        self.gateway:     str = gateway
        self.interface:   str = interface
        self.metrics:     int = metrics

    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, self.__class__):
            return __o.destination == self.destination and \
                   __o.gateway     == self.gateway and \
                   __o.interface   == self.interface and \
                   __o.metrics     == self.metrics
        return False

    def __str__(self) -> str:
        return (f"Destination: {self.destination}\n"
                f"Gateway: {self.gateway}\n"
                f"Interface: {self.interface}\n"
                f"Metrics: {self.metrics}")


class RoutingTable:
    """
    Abstract representation of RoutingTables

    Data members:
    routes (List[Route]): List of Route objects
    """

    def __init__(self) -> None:
        self.routes: List[Route] = []

    def get_routes(self, destination: str) -> List[Route]:
        """
        Find the Routes that match the argument

        Parameters:
        destination (str): The destination IP to match against

        Returns:
        List[Route]: The Routes that match the destination
        """
        found: List[Route] = []
        for route in self.routes:
            if destination == route.destination:
                found.append(route)
        return found

    def list_routes(self) -> None:
        """
        Prints Routes contained in the RoutingTable in a formatted way
        """
        if len(self.routes) == 0:
            print("The routing table is empty.")
            return
        curr_line: int = 1
        for route in self.routes:
            print(f"\nRoute {curr_line}")
            first_row_len: int = len(route.destination) + len("Destination: ")
            print("-" * first_row_len)
            print(route)
            curr_line += 1

    def set_route(self, to_set: Route) -> bool:
        """
        Overrides the corresponding Route with the one passed as an argument\n
        The Route with the same destination and interface is going to be the
        one overwritten\n
        If no such Route exists, this adds it instead of overwriting it\n
        If the exact Route is present, nothing changes in the RoutingTable\n

        Parameters:
        to_set (Route): New Route to add or set

        Returns:
        bool: Whether the new Route was added / set or not
        """
        for route in self.routes:
            if to_set == route:
                return False
            elif to_set.destination == route.destination and\
                 to_set.interface   == route.interface:
                self.routes.remove(route)
                self.routes.append(to_set)
                return True
        self.routes.append(to_set)
        return True

    def del_route(self, to_delete: Route) -> None:
        """
        Deletes a route from the RoutingTable

        Parameters:
        to_delete (Route): The Route object to delete from the RoutingTable
        """
        try:
            self.routes.remove(to_delete)
        except ValueError:
            print("The given route was not found during deletion.")
