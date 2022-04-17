from src.components.routing_table import RoutingTable, Route

#------------------------------------------------#
# ROUTE TESTS
#------------------------------------------------#


def test_route_init():
    """
    Test default init behaviour
    """
    # Setup the Route object
    destination = "192.168.1.1"
    gateway = "192.168.1.1"
    interface = "eth1"
    metrics = 10
    route = Route(destination, gateway, interface, metrics)

    assert route.destination == destination and \
        route.gateway == gateway and \
        route.interface == interface and \
        route.metrics == metrics, \
        "Route field mismatch during initialization"

#------------------------------------------------#
# ROUTINGTABLE TESTS
#------------------------------------------------#


def test_routing_table_init():
    """
    Test default init behaviour
    """
    # Setup the RoutingTable object
    routing_table = RoutingTable()

    assert len(routing_table.routes) == 0, \
        "RoutingTable field mismatch during initialization"


def test_routing_table_set_route():
    """
    Test the set_route() method of the RoutingTable
    """
    # Setup the RoutingTable object
    routing_table_1 = RoutingTable()

    # Get the initial number of the Routes
    previous_len_1 = len(routing_table_1.routes)

    # Add a new Route to the empty RoutingTable
    new_route_1 = Route("192.168.1.1", "192.168.1.1", "eth1", 10)
    routing_table_1.set_route(new_route_1)

    # Setup the RoutingTable object
    routing_table_2 = RoutingTable()

    # Get the initial number of the Routes
    previous_len_2 = len(routing_table_2.routes)

    # Add routes in such a wawy that they are duplicates, meaning that only the
    # first one is gonna be added, the second one is going to be ignored
    new_route_2 = Route("192.168.1.1", "192.168.1.1", "eth1", 10)
    other_route_2 = Route("192.168.1.1", "192.168.1.1", "eth1", 10)
    routing_table_2.set_route(new_route_2)
    routing_table_2.set_route(other_route_2)

    # Setup the RoutingTable object
    routing_table_3 = RoutingTable()

    # Get the initial number of the Routes
    previous_len_3 = len(routing_table_3.routes)
    new_route_3 = Route("192.168.1.1", "192.168.0.1", "eth1", 7)
    other_route_3 = Route("192.168.1.1", "192.168.1.1", "eth1", 10)
    routing_table_3.set_route(new_route_3)
    routing_table_3.set_route(other_route_3)

    assert len(routing_table_1.routes) == 1 and \
        routing_table_1.routes[0] == new_route_1 and \
        len(routing_table_1.routes) != previous_len_1 and \
        len(routing_table_2.routes) == 1 and \
        routing_table_2.routes[0] == new_route_2 and \
        new_route_2 == other_route_2 and \
        len(routing_table_2.routes) != previous_len_2 and \
        len(routing_table_3.routes) == 1 and \
        routing_table_3.routes[0] == other_route_3 and \
        new_route_3 != other_route_3 and \
        new_route_3.destination == other_route_3.destination and \
        new_route_3.gateway != other_route_3.gateway and \
        new_route_3.interface == other_route_3.interface and \
        new_route_3.metrics != other_route_3.metrics and \
        len(routing_table_3.routes) != previous_len_3, \
        "RoutingTable.set_route() failure"


def test_routing_table_get_routes():
    """
    Test the get_routes() method of the RoutingTable
    """
    # Setup the RoutingTable object
    routing_table_1 = RoutingTable()

    # Add Routes to the RoutingTable
    routing_table_1.set_route(Route("192.168.1.1", "192.168.0.1", "eth1", 7))
    routing_table_1.set_route(Route("192.168.0.1", "192.168.1.1", "eth2", 15))

    # Get the Route(s) matching the IP address (no match in this case)
    found_routes_1 = routing_table_1.get_routes("127.0.0.1")

    # Setup the RoutingTable object
    routing_table_2 = RoutingTable()

    # Add Routes to the RoutingTable
    routing_table_2.set_route(Route("192.168.1.1", "192.168.0.1", "eth1", 7))
    routing_table_2.set_route(Route("192.168.0.1", "192.168.1.1", "eth2", 15))

    # Get the Route(s) matching the IP address (single match in this case)
    found_routes_2 = routing_table_2.get_routes("192.168.0.1")

    # Setup the RoutingTable object
    routing_table_3 = RoutingTable()

    # Add Routes to the RoutingTable
    routing_table_3.set_route(Route("192.168.1.1", "192.168.0.1", "eth1", 7))
    routing_table_3.set_route(Route("192.168.0.1", "192.168.1.1", "eth2", 15))
    routing_table_3.set_route(Route("192.168.1.1", "192.168.1.1", "eth3", 20))
    routing_table_3.set_route(Route("192.168.0.1", "192.168.1.1", "eth4", 15))

    # Get the Route(s) matching the IP address (multiple matches in this case)
    found_routes_3 = routing_table_3.get_routes("192.168.0.1")

    assert len(found_routes_1) == 0 and \
        len(routing_table_1.routes) != 0 and \
        len(found_routes_2) == 1 and \
        len(routing_table_2.routes) != 0 and \
        len(found_routes_3) == 2 and \
        len(routing_table_3.routes) != 0, \
        "RoutingTable.get_routes() failure"


def test_routing_table_reset_routes():
    """
    Test the reset_routes() method of the RoutingTable
    """
    # Setup the RoutingTable object
    routing_table = RoutingTable()

    # Add Routes to the RoutingTable
    routing_table.set_route(Route("192.168.1.1", "192.168.0.1", "eth1", 7))
    routing_table.set_route(Route("192.168.0.1", "192.168.1.1", "eth2", 15))
    routing_table.set_route(Route("192.168.1.1", "192.168.1.1", "eth3", 20))
    routing_table.set_route(Route("192.168.0.1", "192.168.1.1", "eth4", 15))

    # Get the number of Routes present
    previous_len = len(routing_table.routes)

    # Reset the RoutingTable to a default state
    routing_table.reset_routes()

    assert len(routing_table.routes) != previous_len and \
        len(routing_table.routes) == 0, \
        "RoutingTable.reset_routes() failure"
