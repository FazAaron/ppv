from src.components.routing_table import RoutingTable, Route

#------------------------------------------------#
# ROUTE TESTS
#------------------------------------------------#


def test_route_init():
    """
    Test default init behaviour
    """
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
    routing_table = RoutingTable()
    assert len(routing_table.routes) == 0, \
        "RoutingTable field mismatch during initialization"


def test_routing_table_set_route_new():
    """
    Test setting a new Route
    """
    routing_table = RoutingTable()
    previous_len = len(routing_table.routes)
    new_route = Route("192.168.1.1", "192.168.1.1", "eth1", 10)
    routing_table.set_route(new_route)
    assert len(routing_table.routes) == 1 and \
        routing_table.routes[0] == new_route and \
        len(routing_table.routes) != previous_len, \
        "RoutingTable.set_route() failure"


def test_routing_table_set_route_exact_match():
    """
    Test setting a new Route while an exact match is present\n
    This makes it so that the method call does not overwrite anything
    """
    routing_table = RoutingTable()
    previous_len = len(routing_table.routes)
    new_route = Route("192.168.1.1", "192.168.1.1", "eth1", 10)
    other_route = Route("192.168.1.1", "192.168.1.1", "eth1", 10)
    routing_table.set_route(new_route)
    routing_table.set_route(other_route)
    assert len(routing_table.routes) == 1 and \
        routing_table.routes[0] == new_route and \
        new_route == other_route and \
        len(routing_table.routes) != previous_len, \
        "RoutingTable.set_route() failure"


def test_routing_table_set_route_overwrite():
    """
    Test setting a new Route while there is a Route matching the new one's
    destination and interface\n
    This makes it so that the method call overwrites the previous Route
    """
    routing_table = RoutingTable()
    previous_len = len(routing_table.routes)
    new_route = Route("192.168.1.1", "192.168.0.1", "eth1", 7)
    other_route = Route("192.168.1.1", "192.168.1.1", "eth1", 10)
    routing_table.set_route(new_route)
    routing_table.set_route(other_route)
    assert len(routing_table.routes) == 1 and \
        routing_table.routes[0] == other_route and \
        new_route != other_route and \
        new_route.destination == other_route.destination and \
        new_route.gateway != other_route.gateway and \
        new_route.interface == other_route.interface and \
        new_route.metrics != other_route.metrics and \
        len(routing_table.routes) != previous_len, \
        "RoutingTable.set_route() failure"


def test_routing_table_get_routes_no_match():
    """
    Test getting Routes to a destination that don't match any of the
    Routes available in the RoutingTable
    """
    routing_table = RoutingTable()
    routing_table.set_route(Route("192.168.1.1", "192.168.0.1", "eth1", 7))
    routing_table.set_route(Route("192.168.0.1", "192.168.1.1", "eth2", 15))
    found_routes = routing_table.get_routes("127.0.0.1")
    assert len(found_routes) == 0 and \
        len(routing_table.routes) != 0, \
        "RoutingTable.get_routes() failure"


def test_routing_table_get_routes_single_match():
    """
    Test getting Routes to a destination that match a single one of the
    Routes available in the RoutingTable
    """
    routing_table = RoutingTable()
    routing_table.set_route(Route("192.168.1.1", "192.168.0.1", "eth1", 7))
    routing_table.set_route(Route("192.168.0.1", "192.168.1.1", "eth2", 15))
    found_routes = routing_table.get_routes("192.168.0.1")
    assert len(found_routes) == 1 and \
        len(routing_table.routes) != 0, \
        "RoutingTable.get_routes() failure"


def test_routing_table_get_routes_multiple_matches():
    """
    Test getting Routes to a destination that match multiple Routes 
    available in the RoutingTable
    """
    routing_table = RoutingTable()
    routing_table.set_route(Route("192.168.1.1", "192.168.0.1", "eth1", 7))
    routing_table.set_route(Route("192.168.0.1", "192.168.1.1", "eth2", 15))
    routing_table.set_route(Route("192.168.1.1", "192.168.1.1", "eth3", 20))
    routing_table.set_route(Route("192.168.0.1", "192.168.1.1", "eth4", 15))
    found_routes = routing_table.get_routes("192.168.0.1")
    assert len(found_routes) == 2 and \
        len(routing_table.routes) != 0, \
        "RoutingTable.get_routes() failure"


def test_routing_table_reset_routes():
    """
    Test resetting Routes in the RoutingTable
    This sets the routes to an empty state
    """
    routing_table = RoutingTable()
    routing_table.set_route(Route("192.168.1.1", "192.168.0.1", "eth1", 7))
    routing_table.set_route(Route("192.168.0.1", "192.168.1.1", "eth2", 15))
    routing_table.set_route(Route("192.168.1.1", "192.168.1.1", "eth3", 20))
    routing_table.set_route(Route("192.168.0.1", "192.168.1.1", "eth4", 15))
    previous_len = len(routing_table.routes)
    routing_table.reset_routes()
    assert len(routing_table.routes) != previous_len and \
        len(routing_table.routes) == 0
