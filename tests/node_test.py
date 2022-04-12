from src.components.node import Host, Node, Router
from src.components.packet import Packet
from src.components.routing_table import Route

#------------------------------------------------#
# NODE TESTS
#------------------------------------------------#


def test_node_init():
    """
    Test default init behaviour
    """
    name = "node"
    ip = "192.168.1.1"
    send_rate = 10
    node = Node(name, ip, send_rate)
    assert node.name == name and \
        node.ip == ip and \
        node.send_rate == send_rate and \
        node.interfaces == [] and \
        node.connections == [] and \
        node.routing_table.routes == [], \
        "Node field mismatch during initialization"


def test_node_get_best_route_empty_routing_table():
    """
    Test getting the best route for a destination, but the RoutingTable is empty
    """
    name = "node"
    ip = "192.168.1.1"
    send_rate = 10
    node = Node(name, ip, send_rate)
    route = node.get_best_route("192.167.1.1")
    assert route is None and \
        len(node.routing_table.routes) == 0, \
        "Node.get_best_route() failure"


def test_node_get_best_route_no_match():
    """
    Test getting the best route for a destination, but finding no match
    """
    name = "node"
    ip = "192.168.1.1"
    send_rate = 10
    node = Node(name, ip, send_rate)
    route_1 = Route("192.168.1.1", "192.168.1.1", "eth1", 10)
    route_2 = Route("192.168.0.1", "192.168.1.1", "eth2", 10)
    node.add_route(route_1)
    node.add_route(route_2)
    route = node.get_best_route("192.167.1.1")
    assert route is None and \
        len(node.routing_table.routes) != 0, \
        "Node.get_best_route() failure"


def test_node_get_best_route_single_match():
    """
    Test getting the best route for a destination, but finding one match
    """
    name = "node"
    ip = "192.168.1.1"
    send_rate = 10
    node = Node(name, ip, send_rate)
    route_1 = Route("192.168.1.1", "192.168.1.1", "eth1", 10)
    route_2 = Route("192.168.0.1", "192.168.1.1", "eth2", 10)
    node.add_route(route_1)
    node.add_route(route_2)
    route = node.get_best_route("192.168.1.1")
    assert route is route_1 and \
        len(node.routing_table.routes) != 0, \
        "Node.get_best_route() failure"


def test_node_get_best_route_multiple_matches():
    """
    Test getting the best route for a destination, but finding multiple matches
    """
    name = "node"
    ip = "192.168.1.1"
    send_rate = 10
    node = Node(name, ip, send_rate)
    route_1 = Route("192.168.1.1", "192.168.1.1", "eth1", 10)
    route_2 = Route("192.168.1.1", "192.168.1.1", "eth2", 7)
    node.add_route(route_1)
    node.add_route(route_2)
    route = node.get_best_route("192.168.1.1")
    assert route is route_2 and \
        len(node.routing_table.routes) != 0, \
        "Node.get_best_route() failure"


def test_node_add_interface_new_name():
    """
    Test adding a new Interface with a name that does not already exist
    """
    name = "node"
    ip = "192.168.1.1"
    send_rate = 10
    node = Node(name, ip, send_rate)
    interface_name = "eth1"
    success = node.add_interface(interface_name)
    assert len(node.interfaces) == 1 and \
        node.interfaces[0].name == interface_name and \
        success, \
        "Node.add_interface() failure"


def test_node_add_interface_existing_name():
    """
    Test adding a new Interface with a name that already exists on the Node\n
    In this case the already existing will be kept
    """
    name = "node"
    ip = "192.168.1.1"
    send_rate = 10
    node = Node(name, ip, send_rate)
    interface_name = "eth1"
    node.add_interface(interface_name)
    success = node.add_interface(interface_name)
    assert len(node.interfaces) == 1 and \
        node.interfaces[0].name == interface_name and \
        not success, \
        "Node.add_interface() failure"


def test_node_get_interface_no_interfaces():
    """
    Test getting a Node Interface based on name, but having no Interfaces on \
    the Node
    """
    name = "node"
    ip = "192.168.1.1"
    send_rate = 10
    node = Node(name, ip, send_rate)
    to_find = "eth1"
    found_interface = node.get_interface(to_find)
    assert len(node.interfaces) == 0 and \
        not found_interface, \
        "Node.get_interface() failure"


def test_node_get_interface_no_match():
    """
    Test getting a Node Interface based on name, but having no matching \
    Interfaces on the Node
    """
    name = "node"
    ip = "192.168.1.1"
    send_rate = 10
    node = Node(name, ip, send_rate)
    interface_1 = "eth2"
    interface_2 = "eth3"
    node.add_interface(interface_1)
    node.add_interface(interface_2)
    to_find = "eth1"
    found_interface = node.get_interface(to_find)
    assert len(node.interfaces) != 0 and \
        found_interface is None, \
        "Node.get_interface() failure"


def test_node_get_interface_found_match():
    """
    Test getting a Node Interface based on name, and having a matching \
    Interface on the Node
    """
    name = "node"
    ip = "192.168.1.1"
    send_rate = 10
    node = Node(name, ip, send_rate)
    interface_1 = "eth1"
    interface_2 = "eth2"
    node.add_interface(interface_1)
    node.add_interface(interface_2)
    to_find = "eth1"
    found_interface = node.get_interface(to_find)
    assert len(node.interfaces) != 0 and \
        found_interface.name == to_find, \
        "Node.get_interface() failure"


def test_node_connect_to_interface_same_nodes():
    """
    Test connecting two Nodes' Interfaces, the two Nodes being the same object
    """
    name = "node1"
    ip = "192.168.1.1"
    send_rate = 10
    node = Node(name, ip, send_rate)
    node.add_interface("eth1")
    success = node.connect_to_interface(node, "eth1", "eth1", 10, 10)
    assert not success and \
        len(node.connections) == 0, \
        "Node.connect_to_interface() failure"


def test_node_connect_to_interface_invalid_interface_first():
    """
    Test connecting two Nodes' Interfaces, the two Nodes being different objects, \
    but the first Interface's name is a name that is not present
    """
    name = "node1"
    ip = "192.168.1.1"
    send_rate = 10
    node_1 = Node(name, ip, send_rate)
    node_1.add_interface("eth1")
    name = "node2"
    ip = "192.168.0.1"
    send_rate = 10
    node_2 = Node(name, ip, send_rate)
    node_2.add_interface("eth1")
    connect_1 = "eth2"
    connect_2 = "eth1"
    success = node_1.connect_to_interface(node_2, connect_1, connect_2, 10, 10)
    assert not success and \
        node_1.get_interface(connect_1) is None and \
        node_2.get_interface(connect_2) is not None and \
        len(node_1.connections) == 0 and \
        len(node_2.connections) == 0, \
        "Node.connect_to_interface() failure"


def test_node_connect_to_interface_invalid_interface_second():
    """
    Test connecting two Nodes' Interfaces, the two Nodes being different objects, \
    but the second Interface's name is a name that is not present
    """
    name = "node1"
    ip = "192.168.1.1"
    send_rate = 10
    node_1 = Node(name, ip, send_rate)
    node_1.add_interface("eth1")
    name = "node2"
    ip = "192.168.0.1"
    send_rate = 10
    node_2 = Node(name, ip, send_rate)
    node_2.add_interface("eth1")
    connect_1 = "eth1"
    connect_2 = "eth2"
    success = node_1.connect_to_interface(node_2, connect_1, connect_2, 10, 10)
    assert not success and \
        node_1.get_interface(connect_1) is not None and \
        node_2.get_interface(connect_2) is None and \
        len(node_1.connections) == 0 and \
        len(node_2.connections) == 0, \
        "Node.connect_to_interface() failure"


def test_node_connect_to_interface_invalid_interface_both():
    """
    Test connecting two Nodes' Interfaces, the two Nodes being different objects, \
    but both Interfaces' name is a name that is not present
    """
    name = "node1"
    ip = "192.168.1.1"
    send_rate = 10
    node_1 = Node(name, ip, send_rate)
    node_1.add_interface("eth1")
    name = "node2"
    ip = "192.168.0.1"
    send_rate = 10
    node_2 = Node(name, ip, send_rate)
    node_2.add_interface("eth1")
    connect_1 = "eth2"
    connect_2 = "eth2"
    success = node_1.connect_to_interface(node_2, connect_1, connect_2, 10, 10)
    assert not success and \
        node_1.get_interface(connect_1) is None and \
        node_2.get_interface(connect_2) is None and \
        len(node_1.connections) == 0 and \
        len(node_2.connections) == 0, \
        "Node.connect_to_interface() failure"


def test_node_connect_to_interface_success():
    """
    Test connecting two Nodes' Interfaces and succeeding
    """
    name = "node1"
    ip = "192.168.1.1"
    send_rate = 10
    node_1 = Node(name, ip, send_rate)
    node_1.add_interface("eth1")
    name = "node2"
    ip = "192.168.0.1"
    send_rate = 10
    node_2 = Node(name, ip, send_rate)
    node_2.add_interface("eth1")
    connect_1 = "eth1"
    connect_2 = "eth1"
    success = node_1.connect_to_interface(node_2, connect_1, connect_2, 10, 10)
    print(node_1.connections[0][0][1].name)
    assert success and \
        node_1.get_interface(connect_1).name == connect_1 and \
        node_2.get_interface(connect_2).name == connect_2 and \
        len(node_1.connections) != 0 and \
        len(node_2.connections) != 0 and \
        node_1.connections[0][0][1] == node_2.connections[0][1][1] and \
        node_1.connections[0][0][0] == node_2.connections[0][1][0] and \
        node_1.connections[0][1][1] == node_2.connections[0][0][1] and \
        node_1.connections[0][1][0] == node_2.connections[0][0][0], \
        "Node.connect_to_interface() failure"


def test_node_disconnect_interface_invalid_interface():
    """
    Test disconnecting an Interface that is not present on the Node
    """
    name = "node1"
    ip = "192.168.1.1"
    send_rate = 10
    node_1 = Node(name, ip, send_rate)
    node_1.add_interface("eth1")
    name = "node2"
    ip = "192.168.0.1"
    send_rate = 10
    node_2 = Node(name, ip, send_rate)
    node_2.add_interface("eth1")
    connect_1 = "eth1"
    connect_2 = "eth1"
    node_1.connect_to_interface(node_2, connect_1, connect_2, 10, 10)
    disconnect = "eth2"
    success = node_1.disconnect_interface(disconnect)
    assert not success and \
        len(node_1.connections) != 0 and \
        len(node_2.connections) != 0 and \
        node_1.connections[0][0][1] == node_2.connections[0][1][1] and \
        node_1.connections[0][0][0] == node_2.connections[0][1][0] and \
        node_1.connections[0][1][1] == node_2.connections[0][0][1] and \
        node_1.connections[0][1][0] == node_2.connections[0][0][0], \
        "Node.disconnect_interface() failure"


def test_node_disconnect_interface_not_connected_interface():
    """
    Test disconnecting an Interface that is not connected to anything on the Node
    """
    name = "node1"
    ip = "192.168.1.1"
    send_rate = 10
    node_1 = Node(name, ip, send_rate)
    node_1.add_interface("eth1")
    node_1.add_interface("eth2")
    name = "node2"
    ip = "192.168.0.1"
    send_rate = 10
    node_2 = Node(name, ip, send_rate)
    node_2.add_interface("eth1")
    connect_1 = "eth1"
    connect_2 = "eth1"
    node_1.connect_to_interface(node_2, connect_1, connect_2, 10, 10)
    disconnect = "eth2"
    success = node_1.disconnect_interface(disconnect)
    assert not success and \
        len(node_1.connections) != 0 and \
        len(node_2.connections) != 0 and \
        node_1.connections[0][0][1] == node_2.connections[0][1][1] and \
        node_1.connections[0][0][0] == node_2.connections[0][1][0] and \
        node_1.connections[0][1][1] == node_2.connections[0][0][1] and \
        node_1.connections[0][1][0] == node_2.connections[0][0][0], \
        "Node.disconnect_interface() failure"


def test_node_disconnect_interface_success():
    """
    Test disconnecting an Interface successfully
    """
    name = "node1"
    ip = "192.168.1.1"
    send_rate = 10
    node_1 = Node(name, ip, send_rate)
    node_1.add_interface("eth1")
    node_1.add_interface("eth2")
    name = "node2"
    ip = "192.168.0.1"
    send_rate = 10
    node_2 = Node(name, ip, send_rate)
    node_2.add_interface("eth1")
    connect_1 = "eth1"
    connect_2 = "eth1"
    node_1.connect_to_interface(node_2, connect_1, connect_2, 10, 10)
    disconnect = "eth1"
    success = node_1.disconnect_interface(disconnect)
    assert success and \
        len(node_1.connections) == 0 and \
        len(node_2.connections) == 0, \
        "Node.disconnect_interface() failure"


def test_node_delete_interface_no_interfaces():
    """
    Test deleting a Node Interface based on name, and having no Interfaces \
    on the Node
    """
    name = "node"
    ip = "192.168.1.1"
    send_rate = 10
    node = Node(name, ip, send_rate)
    to_delete = "eth1"
    success = node.delete_interface(to_delete)
    assert len(node.interfaces) == 0 and \
        not success, \
        "Node.delete_interface() failure"


def test_node_delete_interface_no_match():
    """
    Test deleting a Node Interface based on name, and having no matching \
    Interfaces on the Node
    """
    name = "node"
    ip = "192.168.1.1"
    send_rate = 10
    node = Node(name, ip, send_rate)
    node.add_interface("eth1")
    to_delete = "eth2"
    success = node.delete_interface(to_delete)
    assert len(node.interfaces) != 0 and \
        not success, \
        "Node.delete_interface() failure"


def test_node_delete_interface_not_connected_success():
    """
    Test deleting a Node Interface based on name, and succeeding at it
    """
    name = "node"
    ip = "192.168.1.1"
    send_rate = 10
    node = Node(name, ip, send_rate)
    node.add_interface("eth1")
    to_delete = "eth1"
    success = node.delete_interface(to_delete)
    assert len(node.interfaces) == 0 and \
        success, \
        "Node.delete_interface() failure"


def test_node_delete_interface_connected_success():
    """
    Test deleting a Node Interface based on name which is connected to an other
    Node's interface, and succeeding at it
    """
    name = "node1"
    ip = "192.168.1.1"
    send_rate = 10
    node_1 = Node(name, ip, send_rate)
    name = "node1"
    ip = "192.168.1.1"
    send_rate = 10
    node_2 = Node(name, ip, send_rate)
    node_1.add_interface("eth1")
    node_2.add_interface("eth1")
    node_1.connect_to_interface(node_2, "eth1", "eth1", 10, 10)
    to_delete = "eth1"
    success = node_1.delete_interface(to_delete)
    assert len(node_1.interfaces) == 0 and \
        len(node_1.connections) == 0 and \
        len(node_2.interfaces) != 0 and \
        len(node_2.connections) == 0 and \
        success, \
        "Node.delete_interface() failure"


#------------------------------------------------#
# HOST TESTS
#------------------------------------------------#


def test_host_init():
    """
    Test default init behaviour
    """
    name = "host"
    ip = "192.166.1.1"
    send_rate = 10
    host = Host(name, ip, send_rate)
    assert host.name == name and \
        host.ip == ip and \
        host.send_rate == send_rate and \
        host.application == None, \
        "Host field mismatch during initialization"


def test_host_set_application():
    """
    Test setting the Application, which changes the Host's send_rate as well
    """
    name = "host"
    ip = "192.166.1.1"
    send_rate = 10
    host = Host(name, ip, send_rate)
    app_name = "host_app"
    amount = 15
    app_send_rate = 11
    app_type = "AIMD"
    host.set_application(app_name, amount, app_send_rate, app_type)
    assert host.application.name == app_name and \
        host.application.ip == host.ip and \
        host.application.amount == amount and \
        host.application.send_rate == app_send_rate and \
        host.application.send_rate == host.send_rate and \
        host.application.send_rate != send_rate and \
        host.application.app_type == app_type, \
        "Host.set_application() failure"


def test_host_send_packet_self_ip():
    """
    Test sending a Packet to the same IP as the Host
    """
    name = "host_1"
    ip = "192.166.1.1"
    send_rate = 10
    host_1 = Host(name, ip, send_rate)
    host_1.add_interface("eth1")
    app_name = "host_app_1"
    amount = 15
    app_send_rate = 11
    app_type = "AIMD"
    host_1.set_application(app_name, amount, app_send_rate, app_type)
    name = "host_2"
    ip = "192.166.1.1"
    send_rate = 10
    host_2 = Host(name, ip, send_rate)
    host_2.add_interface("eth2")
    app_name = "host_app_2"
    amount = 15
    app_send_rate = 11
    app_type = "AIMD"
    host_2.set_application(app_name, amount, app_send_rate, app_type)
    connected = host_1.connect_to_interface(host_2, "eth1", "eth2", 10, 10)
    host_1.add_route(Route("192.166.1.1", "192.166.1.1", "eth1", 5))
    host_2.add_route(Route("192.166.1.1", "192.166.1.1", "eth2", 5))
    return_val = host_1.send_packet(host_2.ip)
    assert return_val is None and \
        connected and \
        len(host_1.routing_table.routes) != 0 and \
        len(host_2.routing_table.routes) != 0, \
        "Host.send_packet() failure"


def test_host_send_packet_app_cant_send():
    """
    Test sending a Packet to a Node in such a way that the Application can't \
    send anymore
    """
    name = "host_1"
    ip = "192.167.1.1"
    send_rate = 10
    host_1 = Host(name, ip, send_rate)
    host_1.add_interface("eth1")
    app_name = "host_app_1"
    amount = 0
    app_send_rate = 11
    app_type = "AIMD"
    host_1.set_application(app_name, amount, app_send_rate, app_type)
    name = "host_2"
    ip = "192.166.1.1"
    send_rate = 10
    host_2 = Host(name, ip, send_rate)
    host_2.add_interface("eth2")
    app_name = "host_app_2"
    amount = 15
    app_send_rate = 11
    app_type = "AIMD"
    host_2.set_application(app_name, amount, app_send_rate, app_type)
    connected = host_1.connect_to_interface(host_2, "eth1", "eth2", 10, 10)
    host_1.add_route(Route("192.166.1.1", "192.166.1.1", "eth1", 5))
    host_2.add_route(Route("192.167.1.1", "192.167.1.1", "eth2", 5))
    return_val = host_1.send_packet(host_2.ip)
    assert return_val is None and \
        connected and \
        len(host_1.routing_table.routes) != 0 and \
        len(host_2.routing_table.routes) != 0 and \
        not host_1.application.can_send(), \
        "Host.send_packet() failure"


def test_host_send_packet_no_route():
    """
    Test sending a Packet to an other Node in such a way that there is no Route \
    between the two
    """
    name = "host_1"
    ip = "192.167.1.1"
    send_rate = 10
    host_1 = Host(name, ip, send_rate)
    host_1.add_interface("eth1")
    app_name = "host_app_1"
    amount = 15
    app_send_rate = 11
    app_type = "AIMD"
    host_1.set_application(app_name, amount, app_send_rate, app_type)
    name = "host_2"
    ip = "192.166.1.1"
    send_rate = 10
    host_2 = Host(name, ip, send_rate)
    host_2.add_interface("eth2")
    app_name = "host_app_2"
    amount = 15
    app_send_rate = 11
    app_type = "AIMD"
    host_2.set_application(app_name, amount, app_send_rate, app_type)
    connected = host_1.connect_to_interface(host_2, "eth1", "eth2", 10, 10)
    return_val = host_1.send_packet(host_2.ip)
    assert return_val is None and \
        connected and \
        len(host_1.routing_table.routes) == 0 and \
        len(host_2.routing_table.routes) == 0 and \
        host_1.application.can_send(), \
        "Host.send_packet() failure"


def test_host_send_packet_success():
    name = "host_1"
    ip = "192.167.1.1"
    send_rate = 10
    host_1 = Host(name, ip, send_rate)
    host_1.add_interface("eth1")
    app_name = "host_app_1"
    amount = 10
    app_send_rate = 11
    app_type = "AIMD"
    host_1.set_application(app_name, amount, app_send_rate, app_type)
    name = "host_2"
    ip = "192.166.1.1"
    send_rate = 10
    host_2 = Host(name, ip, send_rate)
    host_2.add_interface("eth2")
    app_name = "host_app_2"
    amount = 15
    app_send_rate = 11
    app_type = "AIMD"
    host_2.set_application(app_name, amount, app_send_rate, app_type)
    connected = host_1.connect_to_interface(host_2, "eth1", "eth2", 10, 10)
    host_1.add_route(Route("192.166.1.1", "192.166.1.1", "eth1", 5))
    host_2.add_route(Route("192.167.1.1", "192.167.1.1", "eth2", 5))
    return_val = host_1.send_packet(host_2.ip)
    assert return_val[0] == host_2.ip and \
        return_val[1] == host_2.interfaces[0].name and \
        connected, \
        "Host.send_packet() failure"


def test_host_receive_packet_invalid_interface():
    """
    Test receiving a Packet on an Interface that does not exist
    """
    name = "host_1"
    ip = "192.167.1.1"
    send_rate = 10
    host_1 = Host(name, ip, send_rate)
    host_1.add_interface("eth1")
    app_name = "host_app_1"
    amount = 10
    app_send_rate = 11
    app_type = "AIMD"
    host_1.set_application(app_name, amount, app_send_rate, app_type)
    name = "host_2"
    ip = "192.166.1.1"
    send_rate = 10
    host_2 = Host(name, ip, send_rate)
    host_2.add_interface("eth2")
    app_name = "host_app_2"
    amount = 15
    app_send_rate = 11
    app_type = "AIMD"
    host_2.set_application(app_name, amount, app_send_rate, app_type)
    p = Packet("192.166.1.1", "192.167.1.1", 10)
    connected = host_1.connect_to_interface(host_2, "eth1", "eth2", 10, 10)
    for interface in host_1.interfaces:
        interface.receive_channel.fill_payload(p)
    received_packet = host_1.receive_packet("eth2")
    assert not received_packet and \
        host_1.get_interface("eth2") is None and \
        len(host_1.interfaces) != 0 and \
        connected, \
        "Host.receive_packet() failure"


def test_host_receive_packet_no_packet():
    """
    Test trying to receive a Packet on an Interface that does not have any \
    incoming packets
    """
    name = "host_1"
    ip = "192.167.1.1"
    send_rate = 10
    host_1 = Host(name, ip, send_rate)
    host_1.add_interface("eth1")
    app_name = "host_app_1"
    amount = 10
    app_send_rate = 11
    app_type = "AIMD"
    host_1.set_application(app_name, amount, app_send_rate, app_type)
    name = "host_2"
    ip = "192.166.1.1"
    send_rate = 10
    host_2 = Host(name, ip, send_rate)
    host_2.add_interface("eth2")
    app_name = "host_app_2"
    amount = 15
    app_send_rate = 11
    app_type = "AIMD"
    host_2.set_application(app_name, amount, app_send_rate, app_type)
    connected = host_1.connect_to_interface(host_2, "eth1", "eth2", 10, 10)
    received_packet = host_1.receive_packet("eth1")
    assert not received_packet and \
        host_1.get_interface("eth1") is not None and \
        len(host_1.interfaces) != 0 and \
        connected, \
        "Host.receive_packet() failure"


def test_host_receive_packet_success():
    """
    Test successfully receiving a packet
    """
    name = "host_1"
    ip = "192.167.1.1"
    send_rate = 10
    host_1 = Host(name, ip, send_rate)
    host_1.add_interface("eth1")
    app_name = "host_app_1"
    amount = 10
    app_send_rate = 11
    app_type = "AIMD"
    host_1.set_application(app_name, amount, app_send_rate, app_type)
    name = "host_2"
    ip = "192.166.1.1"
    send_rate = 10
    host_2 = Host(name, ip, send_rate)
    host_2.add_interface("eth2")
    app_name = "host_app_2"
    amount = 15
    app_send_rate = 11
    app_type = "AIMD"
    host_2.set_application(app_name, amount, app_send_rate, app_type)
    connected = host_1.connect_to_interface(host_2, "eth1", "eth2", 10, 10)
    p = Packet("192.166.1.1", "192.167.1.1", 10)
    host_1.get_interface("eth1").receive_channel.fill_payload(p)
    received_packet = host_1.receive_packet("eth1")
    assert received_packet and \
        host_1.get_interface("eth1") is not None and \
        len(host_1.interfaces) != 0 and \
        connected, \
        "Host.receive_packet() failure"


def test_host_handle_feedback_positive():
    """
    Test handling a postitive feedback value
    """
    name = "host_1"
    ip = "192.167.1.1"
    send_rate = 10
    host_1 = Host(name, ip, send_rate)
    host_1.add_interface("eth1")
    app_name = "host_app_1"
    amount = 10
    app_send_rate = 11
    app_type = "AIMD"
    host_1.set_application(app_name, amount, app_send_rate, app_type)
    host_1.handle_feedback(1)
    assert host_1.send_rate == app_send_rate + 1 and \
        host_1.application.send_rate == app_send_rate + 1, \
        "Host.handle_feedback() failure"


def test_host_handle_feedback_negative():
    """
    Test handling a negative feedback value
    """
    name = "host_1"
    ip = "192.167.1.1"
    send_rate = 10
    host_1 = Host(name, ip, send_rate)
    host_1.add_interface("eth1")
    app_name = "host_app_1"
    amount = 10
    app_send_rate = 11
    app_type = "AIMD"
    host_1.set_application(app_name, amount, app_send_rate, app_type)
    host_1.handle_feedback(-1)
    assert host_1.send_rate == app_send_rate // 2 and \
        host_1.application.send_rate == app_send_rate // 2, \
        "Host.handle_feedback() failure"


def test_host_receive_feedback_const_negative():
    """
    Test receiving a negative value feedback on a CONST app_type Host
    """
    name = "host_1"
    ip = "192.167.1.1"
    send_rate = 10
    host_1 = Host(name, ip, send_rate)
    host_1.add_interface("eth1")
    app_name = "host_app_1"
    amount = 10
    app_send_rate = 11
    app_type = "CONST"
    host_1.set_application(app_name, amount, app_send_rate, app_type)
    host_1.receive_feedback("192.166.1.1", -1)
    assert host_1.send_rate == app_send_rate and \
        host_1.application.send_rate == app_send_rate, \
        "Host.handle_feedback() failure"


def test_host_receive_feedback_const_positive():
    """
    Test receiving a positive feedback value on a CONST app_type Host
    """
    name = "host_1"
    ip = "192.167.1.1"
    send_rate = 10
    host_1 = Host(name, ip, send_rate)
    host_1.add_interface("eth1")
    app_name = "host_app_1"
    amount = 10
    app_send_rate = 11
    app_type = "CONST"
    host_1.set_application(app_name, amount, app_send_rate, app_type)
    host_1.receive_feedback("192.166.1.1", 1)
    assert host_1.send_rate == app_send_rate and \
        host_1.application.send_rate == app_send_rate, \
        "Host.handle_feedback() failure"


def test_host_receive_feedback_aimd_negative():
    """
    Test receiving a negative feedback value on an AIMD app_type Host
    """
    name = "host_1"
    ip = "192.167.1.1"
    send_rate = 10
    host_1 = Host(name, ip, send_rate)
    host_1.add_interface("eth1")
    app_name = "host_app_1"
    amount = 10
    app_send_rate = 11
    app_type = "AIMD"
    host_1.set_application(app_name, amount, app_send_rate, app_type)
    host_1.receive_feedback("192.167.1.1", -1)
    assert host_1.send_rate == app_send_rate // 2 and \
        host_1.application.send_rate == app_send_rate // 2, \
        "Host.handle_feedback() failure"


def test_host_receive_feedback_aimd_positive():
    """
    Test receiving a positive feedback value on an AIMD app_type Host
    """
    name = "host_1"
    ip = "192.167.1.1"
    send_rate = 10
    host_1 = Host(name, ip, send_rate)
    host_1.add_interface("eth1")
    app_name = "host_app_1"
    amount = 10
    app_send_rate = 11
    app_type = "AIMD"
    host_1.set_application(app_name, amount, app_send_rate, app_type)
    host_1.receive_feedback("192.167.1.1", 1)
    assert host_1.send_rate == app_send_rate + 1 and \
        host_1.application.send_rate == app_send_rate + 1, \
        "Host.handle_feedback() failure"

# TODO: Test PPV generation properly
def test_host_something_ppv(): pass


#------------------------------------------------#
# ROUTER TESTS
#------------------------------------------------#


def test_router_init_positive_buffer_size():
    """
    Test initialization with positive (>=0) buffer_size
    """
    name = "router"
    ip = "192.168.1.1"
    send_rate = 10
    buffer_size = 5
    router = Router(name, ip, send_rate, buffer_size)
    assert router.name == name and \
        router.ip == ip and \
        router.send_rate == send_rate and \
        router.buffer_size == buffer_size and \
        len(router.buffer) == 0, \
        "Router field mismatch during positive buffer_size initialization"


def test_router_init_positive_buffer_size():
    """
    Test initialization with negative (<0) buffer_size
    """
    name = "router"
    ip = "192.168.1.1"
    send_rate = 10
    buffer_size = -1
    router = Router(name, ip, send_rate, buffer_size)
    assert router.name == name and \
        router.ip == ip and \
        router.send_rate == send_rate and \
        router.buffer_size == 0 and \
        len(router.buffer) == 0, \
        "Router field mismatch during negative buffer_size initialization"


def test_router_lowest_buffer_ppv_empty_buffer():
    """
    Test getting the lowest PPV Packet from the buffer while it is empty
    """
    name = "router"
    ip = "192.168.1.1"
    send_rate = 10
    buffer_size = 10
    router = Router(name, ip, send_rate, buffer_size)
    packet = router.lowest_buffer_ppv()
    assert packet is None and \
        len(router.buffer) == 0, \
        "Router.lowest_buffer_ppv() failure"


def test_router_lowest_buffer_ppv_single_lowest():
    """
    Test getting the lowest PPV Packet with a single Packet having the lowest \
    out of all of them
    """
    name = "router"
    ip = "192.168.1.1"
    send_rate = 10
    buffer_size = 10
    router = Router(name, ip, send_rate, buffer_size)
    for _ in range(buffer_size - 1):
        router.buffer.append(Packet("192.167.1.1", "192.169.1.1", 10))
    min_packet = Packet("192.167.1.1", "192.169.1.1", 5)
    router.buffer.append(min_packet)
    packet = router.lowest_buffer_ppv()
    assert packet is min_packet and \
        packet is router.buffer[buffer_size - 1] and \
        len(router.buffer) == buffer_size, \
        "Router.lowest_buffer_ppv() failure"


def test_router_lowest_buffer_ppv_multiple_lowest():
    """
    Test getting the lowest PPV Packet with multiple Packets having the lowest \
    out of all of them, essentially getting the first one with such PPV
    """
    name = "router"
    ip = "192.168.1.1"
    send_rate = 10
    buffer_size = 10
    router = Router(name, ip, send_rate, buffer_size)
    for _ in range(buffer_size - 3):
        router.buffer.append(Packet("192.167.1.1", "192.169.1.1", 10))
    for _ in range(3):
        router.buffer.append(Packet("192.167.1.1", "192.169.1.1", 5))
    packet = router.lowest_buffer_ppv()
    assert packet is router.buffer[buffer_size - 3] and \
        len(router.buffer) == buffer_size, \
        "Router.lowest_buffer_ppv() failure"


def test_router_send_packet_empty_buffer():
    pass


def test_router_send_packet_no_route():
    pass


def test_router_send_packet_success():
    pass


def test_router_receive_packet_invalid_interface():
    pass


def test_router_receive_packet_no_packet():
    pass


def test_router_receive_packet_success():
    pass


def test_router_send_feedback():
    pass


def test_router_receive_feedback():
    pass
