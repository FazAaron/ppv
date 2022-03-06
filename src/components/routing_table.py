from typing import List
from route import Route

class RoutingTable:
    """
    Abstract representation of routing tables used by Node objects
    """
    def __init__(self) -> None:
        self.routes: List[Route] = []
    
    def get_routes(self, destination : str) -> List[Route]:
        """
        Returns the list of routes corrseponding to the destination
        """
        found: List[Route] = []
        for route in self.routes:
            if destination == route.destination:
                found.append(route)
        return found

    def list_routes(self) -> None:
        """
        Prints routes in a formatted way
        """
        curr_line: int = 1
        for route in self.routes:
            print(f"\nRoute {curr_line}")
            first_row_len: int = len(route.destination) + len("Destination: ")
            print("-" * first_row_len)
            print(route)
            curr_line += 1

    def set_route(self, to_set: Route) -> bool:
        """
        Overrides the corresponding Route with the one passed as an argument.
        The Route with the same destination and interface is going to be the
        one overwritten. If no such Route exists, this adds it.
        If the exact Route is present in the table, nothing will change.
        """
        for route in self.routes:
            if to_set == route:
                return False
            elif to_set.destination == route.destination and\
                 to_set.interface == route.interface:
                route = to_set
                return True
        self.routes.append(to_set)
        return True    
                            

    def del_route(self, to_delete) -> None:
        """
        Deletes a route from the list of routes
        """
        self.routes.remove(to_delete)
