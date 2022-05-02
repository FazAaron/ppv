from src.components.network import Network
from src.components.node import Host, Router
from src.components.routing_table import Route
from src.components.packet import Packet


def test_network_init():
    """
    Test default init behaviour
    """
    # Setup the Network object
    network = Network()
    
    assert len(network.hosts) == 0 and \
        len(network.routers) == 0 and \
        len(network.graph.vertices) == 0 and \
        len(network.graph.edges) == 0, \
        "Network field mismatch during initialization"


def test_network_get_nodes():
    """
    Test getting all the Nodes (Hosts and Routers combined)
    """
    # Setup the Network object
    network = Network()

    # Get the number of initial Nodes
    init_nodes = network.get_nodes()

    # Add Nodes to the Network
    network.hosts.append(Host("host_1", "192.168.1.1", 10))
    network.routers.append(Router("router_1", "192.167.1.1", 10, 10))

    # Get the number of final Nodes
    final_nodes = network.get_nodes()

    assert len(init_nodes) == 0 and \
        len(final_nodes) == len(network.hosts) + len(network.routers), \
        "Network.get_nodes() failure"


def test_network_get_applications():
    """
    Test getting all the Applications on Hosts
    """
    # Setup the Network object
    network = Network()

    # Get the number of initial Applications
    init_apps = network.get_applications()

    # Add Hosts to the Network    
    network.hosts.append(Host("host_1", "192.168.1.1", 10))
    network.hosts.append(Host("host_2", "192.167.1.1", 10))

    # Set the Application of the Hosts
    network.hosts[0].set_application("app_1", 10, 10, "CONST")
    network.hosts[1].set_application("app_2", 10, 10, "AIMD")

    # Get the number of final Applications
    final_apps = network.get_applications()

    assert len(init_apps) == 0 and len(final_apps) == len(network.hosts), \
        "Network.get_applications() failure"


def test_network_get_interfaces():
    """
    Test getting all the Interfaces on Nodes
    """
    # Setup the Network object
    network = Network()

    # Get the number of initial Interfaces
    init_interfaces = network.get_interfaces()

    # Add Nodes to the Network
    network.hosts.append(Host("host_1", "192.168.1.1", 10))
    network.routers.append(Router("router_1", "192.167.1.1", 10, 10))

    # Add Interfaces to the Nodes
    network.hosts[0].add_interface("eth1")
    network.routers[0].add_interface("eth2")

    # Get the number of final Interfaces
    final_interfaces = network.get_interfaces()

    assert len(init_interfaces) == 0 and \
        len(final_interfaces) == len(network.get_nodes()), \
        "Network.get_interfaces() failure"


def test_network_get_connections():
    """
    Test getting every connection between Nodes
    """
    # Setup the Network object
    network = Network()

    # Get initial connections in the empty Network
    init_connections = network.get_connections()

    # Add Nodes to the Network
    network.hosts.append(Host("host_1", "192.168.1.1", 10))
    network.routers.append(Router("router_1", "192.167.1.1", 10, 10))

    # Setup Interfaces and connections between Nodes
    network.hosts[0].add_interface("eth1")
    network.routers[0].add_interface("eth2")
    network.hosts[0].connect_to_interface(
        network.routers[0], "eth1", "eth2", 10, 10)

    # Get connections after connecting Nodes
    final_connections = network.get_connections()

    assert len(init_connections) == 0 and len(final_connections) == 2, \
        "Network.get_connections() failure"


def test_network_update_routing_tables():
    """
    Test updating the RoutingTable on every Node
    The same logic is done on both Hosts and Routers, since Nodes are being used
    """
    # Setup an empty Network
    network = Network()

    # Setup a Host without any Interface present
    host_without_interface = Host("host_0", "127.0.0.1", 10)

    # Setup a Host that is not connected to any other Node in the Network
    host_not_connected = Host("host_12930", "127.0.1.1", 10)
    host_not_connected.add_interface("eth0")

    # Setup host_1
    host_1 = Host("host_1", "192.168.1.1", 10)
    host_1.add_interface("eth1_1")
    host_1.add_interface("eth1_2")

    # Setup host_2
    host_2 = Host("host_2", "192.167.1.1", 10)
    host_2.add_interface("eth2_1")
    host_2.add_interface("eth2_2")

    # Setup host_3
    host_3 = Host("host_3", "192.169.1.1", 10)
    host_3.add_interface("eth3_1")
    host_3.add_interface("eth3_2")

    # Connect the Nodes
    host_1.connect_to_interface(host_2, "eth1_1", "eth2_1", 10, 5)
    host_1.connect_to_interface(host_3, "eth1_2", "eth3_1", 10, 7)

    host_2.connect_to_interface(host_3, "eth2_2", "eth3_2", 10, 1)

    # Add the newly created Hosts to the Network
    network.hosts.append(host_not_connected)
    network.hosts.append(host_without_interface)
    network.hosts.append(host_1)
    network.hosts.append(host_2)
    network.hosts.append(host_3)

    # Update the RoutingTable
    success = network.update_routing_tables()

    # Create the expected Routes as comparison
    route1_1 = Route("192.167.1.1", "192.167.1.1", "eth1_1", 5)
    route1_2 = Route("192.169.1.1", "192.167.1.1", "eth1_1", 6)

    route2_1 = Route("192.168.1.1", "192.168.1.1", "eth2_1", 5)
    route2_2 = Route("192.169.1.1", "192.169.1.1", "eth2_2", 1)

    route3_1 = Route("192.168.1.1", "192.167.1.1", "eth3_2", 6)
    route3_2 = Route("192.167.1.1", "192.167.1.1", "eth3_2", 1)

    assert success and \
        len(host_not_connected.routing_table.routes) == 0 and \
        len(host_without_interface.routing_table.routes) == 0 and \
        host_1.routing_table.routes[0] == route1_1 and \
        host_1.routing_table.routes[1] == route1_2 and \
        host_2.routing_table.routes[0] == route2_1 and \
        host_2.routing_table.routes[1] == route2_2 and \
        host_3.routing_table.routes[0] == route3_1 and \
        host_3.routing_table.routes[1] == route3_2, \
        "Network.update_routing_tables() failure"


def test_network_is_duplicate_node():
    """
    Test checking if the Node is a duplicate Node \
    (a Node already exists with the given name or IP)
    """
    # Setup the Network object
    network = Network()

    # Check for duplicate name / IP in an empty Network
    is_first_duplicate = network.is_duplicate_node("first_host", "192.168.1.1")

    # Add Nodes to the Network
    network.hosts.append(Host("host_1", "192.168.1.1", 10))
    network.routers.append(Router("router_1", "192.167.1.1", 10, 10))

    # Check duplicate the following way:
    # - the IP is a duplicate
    # - the name is a duplicate
    ip_duplicate = network.is_duplicate_node("host_2", "192.168.1.1")
    name_duplicate = network.is_duplicate_node("router_1", "192.169.1.1")

    assert not is_first_duplicate and ip_duplicate and name_duplicate, \
        "Network.is_duplicate_node() failure"


def test_network_get_host():
    """
    Test getting Hosts
    """
    # Setup the Network object
    network = Network()

    # Add Hosts to the Network
    network.hosts.append(Host("host_1", "192.168.1.1", 10))
    network.hosts.append(Host("host_2", "192.167.1.1", 10))
    network.hosts.append(Host("host_3", "192.169.1.1", 10))

    # Get a Host the following way:
    # - no Host with such name exists
    # - no Host with such IP exists
    name_null_value = network.get_host("host_4")
    ip_null_value = network.get_host("192.170.1.1")

    # Successfully get a Host
    host_value = network.get_host("192.168.1.1")

    assert len(network.hosts) == 3 and \
        name_null_value is None and \
        ip_null_value is None and \
        host_value == network.hosts[0], \
        "Network.get_host() failure"


def test_network_create_host():
    """
    Test creating a Host on the Network
    """
    # Setup the Network object
    network = Network()

    # Successfully create a Host
    empty_success = network.create_host("host_1", "192.168.1.1", 5)

    # Create a Host with the same name / IP already present in the Network
    duplicate_success = network.create_host("host_1", "192.168.1.1", 4)

    assert empty_success and \
        not duplicate_success and \
        len(network.hosts) == 1, \
        "Network.create_host() failure"


def test_network_delete_host():
    """
    Test deleting a Host on the Network
    """
    # Setup the Network object
    network = Network()

    # Delete a Host from an empty Network
    empty_success = network.delete_host("host_9123")

    # Create Hosts to add to the Network
    creation_success_1 = network.create_host("host_1", "192.168.1.1", 4)
    creation_success_2 = network.create_host("host_2", "192.167.1.1", 4)
    prev_len = len(network.hosts)

    # Setup a connection to check whether deletion disconnects it or not
    router = Router("router", "127.0.0.1", 10, 10)
    network.routers.append(router)
    network.hosts[0].add_interface("eth1")
    router.add_interface("eth2")
    router.connect_to_interface(network.hosts[0], "eth2", "eth1", 10, 10)
    prev_connections_len = len(router.connections)

    # Delete Hosts the following way:
    # - no such Host is present in the Network
    # - a Host's IP address matches the deletion parameter
    not_present_success = network.delete_host("192.169.1.1")
    deletion_ip_success = network.delete_host("192.168.1.1")

    # Successfully delete a Host
    deletion_name_success = network.delete_host("host_2")

    # Get the number of Hosts and connections
    final_len = len(network.hosts)
    final_connections_len = len(router.connections)

    assert not empty_success and \
        creation_success_1 and \
        creation_success_2 and \
        prev_len == 2 and \
        not not_present_success and \
        deletion_ip_success and \
        deletion_name_success and \
        final_len == 0 and \
        prev_connections_len == 1 and \
        final_connections_len == 0, \
        "Network.delete_host() failure"


def test_network_get_router():
    """
    Test getting Routers
    """
    # Setup the Network object
    network = Network()

    # Add Routers to the Network
    network.routers.append(Router("router_1", "192.168.1.1", 10, 8))
    network.routers.append(Router("router_2", "192.167.1.1", 10, 9))
    network.routers.append(Router("router_3", "192.169.1.1", 10, 7))

    # Get routers the following way:
    # - the Router with that name is not present in the Network
    # - the Router with that IP is not present in the Network
    name_null_value = network.get_router("router_4")
    ip_null_value = network.get_router("192.170.1.1")

    # Successfully getting a Router
    router_value = network.get_router("192.168.1.1")

    assert len(network.routers) == 3 and \
        name_null_value is None and \
        ip_null_value is None and \
        router_value == network.routers[0], \
        "Network.get_router() failure"


def test_network_create_router():
    """
    Test creating a Router on the Network
    """
    # Setup the Network object
    network = Network()

    # Successfully create a Router
    empty_success = network.create_router("host_1", "192.168.1.1", 5, 20)

    # Create a Router with the same name / IP already present in the Network
    duplicate_success = network.create_router("host_1", "192.168.1.1", 4, 30)

    assert empty_success and \
        not duplicate_success and \
        len(network.routers) == 1, \
        "Network.create_router() failure"


def test_network_delete_router():
    """
    Test deleting a Router on the Network
    """
    # Setup the Network object
    network = Network()

    # Delete a Router from an empty Network
    empty_success = network.delete_router("router_9123")

    # Create Routers to add to the Network
    creation_success_1 = network.create_router(
        "router_1", "192.168.1.1", 4, 10)
    creation_success_2 = network.create_router(
        "router_2", "192.167.1.1", 4, 10)
    prev_len = len(network.routers)

    # Setup a connection to check whether deletion disconnects it or not
    router = Router("router", "127.0.0.1", 10, 10)
    network.routers.append(router)
    network.routers[0].add_interface("eth1")
    router.add_interface("eth2")
    router.connect_to_interface(network.routers[0], "eth2", "eth1", 10, 10)
    prev_connections_len = len(router.connections)

    # Delete a Router with a parameter that doesn't match any in the Network
    not_present_success = network.delete_router("192.169.1.1")

    # Successfully delete a Router based on name / IP address
    deletion_ip_success = network.delete_router("192.168.1.1")
    deletion_name_success = network.delete_router("router_2")

    # Get the number of Routers and connections
    final_len = len(network.routers)
    final_connections_len = len(router.connections)

    assert not empty_success and \
        creation_success_1 and \
        creation_success_2 and \
        prev_len == 2 and \
        not not_present_success and \
        deletion_ip_success and \
        deletion_name_success and \
        final_len == 1 and \
        prev_connections_len - final_connections_len == prev_connections_len, \
        "Network.delete_router() failure"


def test_network_add_interface():
    """
    Test adding an Interface to a Node
    """
    # Setup the Network object
    network = Network()

    # Try adding an Interface to a non-existing Node
    non_existing_success = network.add_interface("host_8213", "eth1")

    # Create Nodes
    network.create_host("host_123", "192.168.1.1", 10)
    network.create_router("router_123", "192.167.1.1", 10, 10)

    # Add an Interface to a Node by specifying the Node's name
    add_by_name_success = network.add_interface("host_123", "eth1")

    # Add an Interface to a Node by specifying the Node's IP address
    add_by_ip_success = network.add_interface("192.167.1.1", "eth2")

    # Try adding a duplicate Interface
    already_existing_success = network.add_interface("router_123", "eth2")

    assert not non_existing_success and \
        add_by_name_success and \
        add_by_ip_success and \
        not already_existing_success, \
        "Network.add_interface() failure"


def test_network_delete_interface():
    """
    Test deleting an Interface on a Node
    """
    # Setup the Network object
    network = Network()

    # Try deleting an Interface on a non-existing Node
    non_existing_success = network.delete_interface("router_81923", "eth3")

    # Create Nodes
    network.create_host("host_123", "192.168.1.1", 10)
    network.create_router("router_123", "192.167.1.1", 10, 10)

    # Add Interfaces to Nodes
    network.add_interface("host_123", "eth1_1")
    network.add_interface("host_123", "eth2_1")
    network.add_interface("host_123", "eth3_1")
    network.add_interface("host_123", "eth4_1")
    network.add_interface("router_123", "eth1_2")
    network.add_interface("router_123", "eth2_2")
    network.add_interface("router_123", "eth3_2")
    network.add_interface("router_123", "eth4_2")

    # Delete an Interface from a Node by specifying the Node's name
    delete_by_name_success = network.delete_interface("host_123", "eth1_1")

    # Delete an Interface from a Node by specifying the Node's IP address
    delete_by_ip_success = network.delete_interface("192.167.1.1", "eth1_2")

    # Delete an Interface from a Node that does not exist on that Node
    interface_not_present_success = network.delete_interface(
        "host_123", "eth1_1")

    # Delete an Interface from a Node that is connected to an other Node
    network.hosts[0].connect_to_interface(
        network.routers[0], "eth2_1", "eth2_2", 10, 10)

    # Get the connected Nodes' number of connections
    prev_connection_len_host = len(network.hosts[0].connections)
    prev_connection_len_router = len(network.routers[0].connections)

    # Delete a connected Interface
    network.get_router("router_123").get_interface("eth2_2").receive_channel.fill_payload(Packet("127.0.0.1", "127.1.1.1", 10))
    connected_interface_success = network.delete_interface(
        "router_123", "eth2_2")

    # Get the disconnected Nodes' number of connections
    final_connection_len_host = len(network.hosts[0].connections)
    final_connection_len_router = len(network.routers[0].connections)

    assert not non_existing_success and \
        delete_by_name_success and \
        delete_by_ip_success and \
        not interface_not_present_success and \
        prev_connection_len_host + prev_connection_len_router == 2 and \
        connected_interface_success and \
        network.dropped_pack == 1 and \
        final_connection_len_host + final_connection_len_router == 0, \
        "Network.delete_interface() failure"


def test_network_set_application():
    """
    Test setting Application on a Host
    """
    # Setup the Network object
    network = Network()

    # Create a Host
    network.create_host("host_123", "192.168.1.1", 10)

    # Set the Application on a Host that does not exist
    non_existant_success = network.set_application(
        "host_456", "app_123", 11, 11, "AIMD")

    # Set the Application by different methods
    application_set_by_name_success = network.set_application(
        "host_123", "app_123", 11, 11, "AIMD")
    application_set_by_ip_success = network.set_application(
        "192.168.1.1", "app_123", 12, 12, "CONST")

    assert not non_existant_success and \
        application_set_by_name_success and \
        application_set_by_ip_success and \
        network.get_host("host_123").application.send_rate == 12 and \
        network.get_host("host_123").application.app_type == "CONST", \
        "Network.set_application() failure"


def test_network_connect_node_interfaces():
    """
    Test connecting Node Interfaces
    """
    # Setup the Network object
    network = Network()

    # Create Nodes
    network.create_host("host_1", "192.168.1.1", 10)
    network.create_router("router_1", "192.169.1.1", 10, 10)

    network.create_host("host_2", "192.170.1.1", 10)
    network.create_router("router_2", "192.171.1.1", 10, 10)

    # Add Interfaces
    network.add_interface("host_1", "eth1_1")
    network.add_interface("router_1", "eth1_2")
    network.add_interface("host_2", "eth1_3")
    network.add_interface("router_2", "eth1_4")

    # Connect Nodes that on either or both side(s) are non-existant
    first_non_existant_node_success = network.connect_node_interfaces(
        "host_123", "router_1", "eth1_1", "eth1_2", 10, 10)
    second_non_existant_node_success = network.connect_node_interfaces(
        "host_1", "router_123", "eth1_1", "eth1_2", 10, 10)
    both_non_existant_node_success = network.connect_node_interfaces(
        "host_123", "router_123", "eth1_1", "eth1_2", 10, 10)

    # Connect Nodes using Interfaces on either or both side(s) that are non-existant
    first_non_existant_interface_success = network.connect_node_interfaces(
        "host_1", "router_1", "eth1", "eth1_2", 10, 10)
    second_non_existant_interface_success = network.connect_node_interfaces(
        "host_1", "router_1", "eth1_1", "eth1_234", 10, 10)
    both_non_existant_interface_success = network.connect_node_interfaces(
        "host_1", "router_1", "eth1_231", "eth1_2234", 10, 10)

    # Connect Nodes using different methods
    connect_by_name_success = network.connect_node_interfaces(
        "host_1", "router_1", "eth1_1", "eth1_2", 10, 10)

    connect_by_ip_success = network.connect_node_interfaces(
        "192.170.1.1", "192.171.1.1", "eth1_3", "eth1_4", 10, 10)

    assert not first_non_existant_node_success and \
        not second_non_existant_node_success and \
        not both_non_existant_node_success and \
        not first_non_existant_interface_success and \
        not second_non_existant_interface_success and \
        not both_non_existant_interface_success and \
        connect_by_name_success and \
        len(network.hosts[0].connections) != 0 and \
        len(network.routers[0].connections) != 0 and \
        connect_by_ip_success and \
        len(network.hosts[1].connections) != 0 and \
        len(network.routers[1].connections) != 0 and \
        len(network.get_nodes()) == 4, \
        "Network.connect_node_interfaces() failure"


def test_network_disconnect_node_interfaces():
    """
    Test disconnecting Node Interfaces
    """
    # Setup the Network object
    network = Network()

    # Create Nodes
    network.create_host("host_1", "192.168.1.1", 10)
    network.create_router("router_1", "192.169.1.1", 10, 10)

    network.create_host("host_2", "192.170.1.1", 10)
    network.create_router("router_2", "192.171.1.1", 10, 10)

    # Add Interfaces
    network.add_interface("host_1", "eth1_1")
    network.add_interface("router_1", "eth1_2")
    network.add_interface("host_2", "eth1_3")
    network.add_interface("router_2", "eth1_4")

    # Connect Nodes
    network.connect_node_interfaces(
        "host_1", "router_1", "eth1_1", "eth1_2", 10, 10)

    network.connect_node_interfaces(
        "192.170.1.1", "192.171.1.1", "eth1_3", "eth1_4", 10, 10)

    # Disconnect Node that is non-existant
    non_existant_node_success = network.disconnect_node_interface(
        "host_32423", "eth2")

    # Disconnect an Interface on the Node that is not present
    non_existant_interface_success = network.disconnect_node_interface(
        "host_1", "eth2_2")

    # Disconnect using multiple methods
    network.get_host("host_1").get_interface("eth1_1").receive_channel.fill_payload(Packet("127.0.0.1", "127.1.1.1", 10))
    disconnect_by_name_success = network.disconnect_node_interface(
        "host_1", "eth1_1")
    disconnect_by_ip_success = network.disconnect_node_interface(
        "192.171.1.1", "eth1_4")

    assert not non_existant_node_success and \
        not non_existant_interface_success and \
        disconnect_by_name_success and \
        len(network.hosts[0].connections) == 0 and \
        len(network.routers[0].connections) == 0 and \
        disconnect_by_ip_success and \
        len(network.hosts[1].connections) == 0 and \
        len(network.routers[1].connections) == 0 and \
        len(network.get_nodes()) == 4 and \
        network.dropped_pack == 1, \
        "Network.disconnect_node_interface() failure"


def test_network_send_packet():
    """
    Test sending Packets between Nodes
    """
    # Setup the Network object
    network = Network()

    # Create Nodes
    network.create_host("host_1", "192.168.1.1", 10)
    network.create_router("router_1", "192.169.1.1", 10, 10)

    network.create_host("host_2", "192.170.1.1", 10)
    network.create_router("router_2", "192.171.1.1", 10, 10)

    # Set Application on Hosts
    network.set_application("host_1", "app_1", 10, 10, "AIMD")
    network.set_application("host_2", "app_2", 0, 10, "AIMD")

    # Add Interfaces
    network.add_interface("host_1", "eth1_1")
    network.add_interface("router_1", "eth1_2")
    network.add_interface("host_2", "eth1_3")
    network.add_interface("router_2", "eth1_4")

    # Connect Nodes
    network.connect_node_interfaces(
        "host_1", "router_1", "eth1_1", "eth1_2", 10, 10)
    network.connect_node_interfaces(
        "192.170.1.1", "192.171.1.1", "eth1_3", "eth1_4", 10, 10)

    # Send from a Node that is non-existant,
    # or send to a Node that is non-existant, or both
    first_non_existant_success = network.send_packet("host_1234", "router_1")
    second_non_existant_success = network.send_packet("router_1", "host_23425")

    # Send in a way that next_hop is None:
    # - the Application can't send (if Host)
    # - the destination is same as the source
    # - there is no Route between the two Nodes
    app_cant_send_success = network.send_packet("host_2", "router_2")
    same_ip_success = network.send_packet("192.168.1.1", "host_1")
    no_route_success = network.send_packet("host_1", "192.171.1.1")

    # Send successfully
    send_success = network.send_packet("host_1", "router_1")

    assert not first_non_existant_success and \
        not second_non_existant_success and \
        not app_cant_send_success and \
        not same_ip_success and \
        not no_route_success and \
        send_success[0] == "192.169.1.1" and \
        send_success[1] == "eth1_2" and \
        send_success[2] == "router_1", \
        "Network.send_packet() failure"


def test_network_receive_packet():
    """
    Test receiving Packets on Nodes
    """
    # Setup the Network object
    network = Network()

    # Create Nodes
    network.create_host("host_1", "192.168.1.1", 10)
    network.create_router("router_1", "192.169.1.1", 10, 10)

    network.create_host("host_2", "192.170.1.1", 10)
    network.create_router("router_2", "192.171.1.1", 10, 10)

    # Set Application on Hosts
    network.set_application("host_1", "app_1", 10, 10, "AIMD")
    network.set_application("host_2", "app_2", 0, 10, "AIMD")

    # Add Interfaces
    network.add_interface("host_1", "eth1_1")
    network.add_interface("router_1", "eth1_2")
    network.add_interface("host_2", "eth1_3")
    network.add_interface("router_2", "eth1_4")

    # Connect Nodes
    network.connect_node_interfaces(
        "host_1", "router_1", "eth1_1", "eth1_2", 10, 10)

    network.connect_node_interfaces(
        "192.170.1.1", "192.171.1.1", "eth1_3", "eth1_4", 10, 10)

    # Receive on a Node that is non-existant
    non_existant_node_success = network.receive_packet("host_12341", "eth1")

    # Receive on a Node Interface that is not present on the Node
    non_existant_interface_success = network.receive_packet("host_1", "eth1_2")

    # Receive on a Node Interface that does not have any incoming Packet(s)
    no_packet_success = network.receive_packet("host_1", "eth1_1")

    # Receive successfully
    next_hop = network.send_packet("host_1", "router_1")
    receive_success = network.receive_packet(next_hop[0], next_hop[1])

    assert not non_existant_node_success and \
        not non_existant_interface_success and \
        not no_packet_success and \
        receive_success and \
        len(network.get_router("router_1").buffer) == 1, \
        "Network.receive_packet() failure"
