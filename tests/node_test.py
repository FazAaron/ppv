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
    # Setup the Node object
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


def test_node_add_interface():
    """
    Test the add_interface() method of the Node
    """
    # Setup the Node object
    name = "node"
    ip = "192.168.1.1"
    send_rate = 10
    node = Node(name, ip, send_rate)

    # Setup the Interface, and add it - first with success, secondly with failure
    interface_name = "eth1"
    success_1 = node.add_interface(interface_name)
    success_2 = node.add_interface(interface_name)

    assert len(node.interfaces) == 1 and \
        node.interfaces[0].name == interface_name and \
        success_1 and \
        not success_2, \
        "Node.add_interface() failure"


def test_node_get_interface():
    """
    Test the get_interface() method of the Node
    """
    # Setup the Node object
    name = "node"
    ip = "192.168.1.1"
    send_rate = 10
    node = Node(name, ip, send_rate)

    # Get an Interface, and get the number of Interfaces on the Node
    # No match will be found, since there are no Interfaces on the Node
    to_find = "eth1"
    found_interface_1 = node.get_interface(to_find)
    init_len = len(node.interfaces)

    # Add an Interface
    node.add_interface("eth2")

    # Get an Interface, and get the number of Interfaces on the Node
    # No match will be found, since there is no such Interface on the Node
    found_interface_2 = node.get_interface(to_find)
    new_len = len(node.interfaces)

    # Get an Interface, and get the number of Interfaces on the Node
    # A match will be found, since there is such an Interface on the Node
    found_interface_3 = node.get_interface("eth2")

    assert init_len == 0 and \
        new_len != 0 and \
        not found_interface_1 and \
        not found_interface_2 and \
        found_interface_3, \
        "Node.get_interface() failure"


def test_node_connect_to_interface():
    """
    Test the connect_to_interface() method of the Node
    """
    # Setup the Node object
    name = "node1"
    ip = "192.168.1.1"
    send_rate = 10
    node = Node(name, ip, send_rate)

    # Add an Interface to the Node
    node.add_interface("eth1")

    # Connect the Node to itself, failing
    success_1 = node.connect_to_interface(node, "eth1", "eth1", 10, 10)
    init_connections = len(node.connections)

    # Setup a second Node object
    name = "node2"
    ip = "192.168.0.1"
    send_rate = 3
    node_2 = Node(name, ip, send_rate)

    # Add an Interface to the Node
    node_2.add_interface("eth2")

    # Connect the Nodes the following way:
    # - first Interface being invalid
    # - the second Interface being invalid
    # - both Interfaces being invalid
    success_2 = node.connect_to_interface(node_2, "eth34", "eth2", 10, 10)
    success_3 = node.connect_to_interface(node_2, "eth1", "eth24312", 10, 10)
    success_4 = node.connect_to_interface(node_2, "eth34", "eth2432", 10, 10)

    # Connect the Nodes successfully
    success_5 = node.connect_to_interface(node_2, "eth1", "eth2", 10, 10)

    assert not success_1[0] and \
        success_1[1] == 0 and \
        not success_2[0] and \
        success_2[1] == 0 and \
        not success_3[0] and \
        success_3[1] == 0 and \
        not success_4[0] and \
        success_4[1] == 0 and \
        success_5[0] and \
        success_5[1] == 0 and \
        init_connections == 0 and \
        len(node.connections) != 0 and \
        len(node_2.connections) != 0 and \
        node.connections[0][0][1] == node_2.connections[0][1][1] and \
        node.connections[0][0][0] == node_2.connections[0][1][0] and \
        node.connections[0][1][1] == node_2.connections[0][0][1] and \
        node.connections[0][1][0] == node_2.connections[0][0][0], \
        "Node.connect_to_interface() failure"


def test_node_disconnect_interface():
    """
    Test the disconnect_interface() method of the Node
    """
    # Setup the Node object
    name = "node1"
    ip = "192.168.1.1"
    send_rate = 10
    node_1 = Node(name, ip, send_rate)

    # Add an Interface to it
    node_1.add_interface("eth1")
    node_1.add_interface("eth2")

    # Setup an other Node object
    name = "node2"
    ip = "192.168.0.1"
    send_rate = 10
    node_2 = Node(name, ip, send_rate)

    # Add an Interface to it
    node_2.add_interface("eth2")

    # Connect the Nodes
    node_1.connect_to_interface(node_2, "eth1", "eth2", 10, 10)
    init_connections = len(node_1.connections)
    prev_connected = node_1.connections[0][0][1] == node_2.connections[0][1][1] and \
        node_1.connections[0][0][0] == node_2.connections[0][1][0] and \
        node_1.connections[0][1][1] == node_2.connections[0][0][1] and \
        node_1.connections[0][1][0] == node_2.connections[0][0][0]
    node_1.get_interface("eth1").receive_channel.fill_payload(
        Packet("127.0.0.1", "127.1.1.1", 10))

    # Disconnect an Interface the following ways:
    # - the Interface is invalid
    # - the Interface is not connected
    success_1 = node_1.disconnect_interface("eth3")
    success_2 = node_1.disconnect_interface("eth2")

    # Disconnect the Interface successfully, which is connected
    success_3 = node_1.disconnect_interface("eth1")

    assert not success_1[0] and \
        success_1[1] == 0 and \
        success_2[0] and \
        success_2[1] == 0 and \
        success_3[0] and \
        success_3[1] == 1 and \
        init_connections != 0 and \
        prev_connected and \
        len(node_1.connections) == 0 and \
        len(node_2.connections) == 0 and \
        node_1.get_interface("eth1").link is None and \
        node_2.get_interface("eth2").link is None, \
        "Node.disconnect_interface() failure"


def test_node_delete_interface():
    """
    Test the delete_interface() method
    """
    # Setup the Node object
    name = "node"
    ip = "192.168.1.1"
    send_rate = 10
    node = Node(name, ip, send_rate)

    # Delete the Interface, failing, since there are no Interfaces on the Node
    success_1 = node.delete_interface("eth1")
    init_len = len(node.interfaces)

    # Add an Interface to the Node
    node.add_interface("eth1")

    # Delete the Interface that is not present on the Node, failing
    success_2 = node.delete_interface("eth2")
    len_2 = len(node.interfaces)

    # Delete the Interface, that is not connected
    success_3 = node.delete_interface("eth1")
    len_3 = len(node.interfaces)

    # Add an Interface back
    node.add_interface("eth1")

    # Setup an other Node object
    name = "node1"
    ip = "192.168.0.1"
    send_rate = 10
    node_2 = Node(name, ip, send_rate)

    # Add an Interface to the new Node
    node_2.add_interface("eth2")

    # Connect the Nodes
    conn_succ = node.connect_to_interface(node_2, "eth1", "eth2", 10, 10)

    # Delete the Interface
    node.get_interface("eth1").receive_channel.fill_payload(
        Packet("127.0.0.1", "127.1.1", 10))
    success_4 = node.delete_interface("eth1")

    assert not success_1[0] and \
        success_1[1] == 0 and \
        not success_2[0] and \
        success_2[1] == 0 and \
        success_3[0] and \
        success_3[1] == 0 and \
        conn_succ[0] and \
        conn_succ[1] == 0 and \
        success_4[0] and \
        success_4[1] == 1 and \
        init_len == 0 and \
        len_2 != 0 and \
        len_3 == 0 and \
        len(node.interfaces) == 0 and \
        len(node.connections) == 0 and \
        len(node_2.interfaces) != 0 and \
        len(node_2.connections) == 0, \
        "Node.delete_interface() failure"


#------------------------------------------------#
# HOST TESTS
#------------------------------------------------#


def test_host_init():
    """
    Test default init behaviour
    """
    # Setup the Host object
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
    Test the set_application() method of the Host
    """
    # Setup the Host object
    name = "host"
    ip = "192.166.1.1"
    send_rate = 10
    host = Host(name, ip, send_rate)

    # Setup the Application object
    app_name = "host_app"
    amount = 15
    app_send_rate = 11
    app_type = "AIMD"

    # Set the Application
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
    Test the send_packet() method of the Host
    """
    # Setup the Host object
    name = "host_1"
    ip = "192.166.1.1"
    send_rate = 10
    host_1 = Host(name, ip, send_rate)
    host_1.add_interface("eth1")

    # Setup the Application object
    app_name = "host_app_1"
    amount = 15
    app_send_rate = 11
    app_type = "AIMD"

    # Set the Application
    host_1.set_application(app_name, amount, app_send_rate, app_type)

    # Setup an other Host object
    name = "host_2"
    ip = "192.166.0.1"
    send_rate = 10
    host_2 = Host(name, ip, send_rate)
    host_2.add_interface("eth2")

    # Setup an other Application object
    app_name = "host_app_2"
    amount = 15
    app_send_rate = 11
    app_type = "AIMD"

    # Set the Application on the other Host
    host_2.set_application(app_name, amount, app_send_rate, app_type)

    # Connect the Hosts
    connected = host_1.connect_to_interface(host_2, "eth1", "eth2", 10, 10)

    # Send a Packet to the same IP address as the source, failing
    success_1 = host_1.send_packet(host_1.ip)

    # Send a Packet when the Application can't send, failing
    host_1.set_application(app_name, 0, app_send_rate, app_type)
    success_2 = host_1.send_packet(host_2.ip)

    # Set the Application to the previous state
    host_1.set_application(app_name, amount, app_send_rate, app_type)

    # Send a Packet when there is no Route to the destination set
    success_3 = host_1.send_packet(host_2.ip)

    # Add Routes to the Hosts
    host_1.add_route(Route("192.166.0.1", "192.166.0.1", "eth1", 5))
    host_2.add_route(Route("192.166.1.1", "192.166.1.1", "eth2", 5))

    # Send a Packet successfully
    success_4 = host_1.send_packet(host_2.ip)

    assert success_1 is None and \
        success_2 is None and \
        success_3 is None and \
        success_4 and \
        connected and \
        len(host_1.routing_table.routes) != 0 and \
        len(host_2.routing_table.routes) != 0, \
        "Host.send_packet() failure"


def test_host_receive_packet_invalid_interface():
    """
    Test the receive_packet() method of the Host
    """
    # Setup the Host object
    name = "host_1"
    ip = "192.167.1.1"
    send_rate = 10
    host_1 = Host(name, ip, send_rate)
    host_1.add_interface("eth1")

    # Setup the Application object
    app_name = "host_app_1"
    amount = 10
    app_send_rate = 11
    app_type = "AIMD"

    # Set the Application
    host_1.set_application(app_name, amount, app_send_rate, app_type)

    # Setup an other Host object
    name = "host_2"
    ip = "192.166.1.1"
    send_rate = 10
    host_2 = Host(name, ip, send_rate)
    host_2.add_interface("eth2")

    # Setup an other Application object
    app_name = "host_app_2"
    amount = 15
    app_send_rate = 11
    app_type = "AIMD"

    # Set the Application
    host_2.set_application(app_name, amount, app_send_rate, app_type)

    # Connect the Hosts
    connected = host_1.connect_to_interface(host_2, "eth1", "eth2", 10, 10)

    # receive the Packet when there are no Packets to receive
    received_packet_1 = host_1.receive_packet("eth1")

    # Setup the Packet object
    p = Packet("192.166.1.1", "192.167.1.1", 10)

    # Fill the receiving channel of every single Interface
    for interface in host_1.interfaces:
        interface.receive_channel.fill_payload(p)

    # Receive the Packet on an Interface that is not present on the Host
    received_packet_2 = host_1.receive_packet("eth2")

    # Receive the Packet sucessfully
    received_packet_3 = host_1.receive_packet("eth1")

    assert not received_packet_1 and \
        not received_packet_2 and \
        received_packet_3 and \
        host_1.get_interface("eth2") is None and \
        len(host_1.interfaces) != 0 and \
        connected, \
        "Host.receive_packet() failure"


# TODO: Test PPV generation properly
def test_host_something_ppv(): pass


#------------------------------------------------#
# ROUTER TESTS
#------------------------------------------------#


def test_router_init():
    """
    Test the default init behaviour
    """
    # Setup the Router object with positive buffer size
    name = "router"
    ip = "192.168.1.1"
    send_rate = 10
    pos_buffer_size = 5
    router_1 = Router(name, ip, send_rate, pos_buffer_size)

    # Setup an other Router object with negative buffer size
    neg_buffer_size = -1
    router_2 = Router(name, ip, send_rate, neg_buffer_size)
    assert router_1.name == name and \
        router_1.ip == ip and \
        router_1.send_rate == send_rate and \
        router_1.buffer_size == pos_buffer_size and \
        len(router_1.buffer) == 0 and \
        router_2.name == name and \
        router_2.ip == ip and \
        router_2.send_rate == send_rate and \
        router_2.buffer_size == 0 and \
        len(router_2.buffer) == 0, \
        "Router field mismatch during buffer_size initialization"


def test_router_lowest_buffer_ppv():
    """
    Test the lowest_buffer_ppv() method of the Router
    """
    # Setup the Router object
    name = "router"
    ip = "192.168.1.1"
    send_rate = 10
    buffer_size = 10
    router = Router(name, ip, send_rate, buffer_size)

    # Get the Packet from an empty buffer, giving a None, and get the buffer
    # length as well
    packet_1 = router.lowest_buffer_ppv()
    init_len = len(router.buffer)

    # Add Packets to the buffer
    for _ in range(buffer_size - 1):
        router.buffer.append(Packet("192.167.1.1", "192.169.1.1", 10))
    min_packet = Packet("192.167.1.1", "192.169.1.1", 5)
    router.buffer.append(min_packet)

    # Get the lowest PPV Packet from the buffer, with a single match, and get
    # the buffer length as well
    packet_2 = router.lowest_buffer_ppv()
    next_len_2 = len(router.buffer)

    # Reset the buffer, and fill it with Packets, but with differently
    # distributed PPV
    router.buffer = []
    for _ in range(buffer_size - 3):
        router.buffer.append(Packet("192.167.1.1", "192.169.1.1", 10))
    for _ in range(3):
        router.buffer.append(Packet("192.167.1.1", "192.169.1.1", 5))

    # Get the lowest PPV packet from the buffer, with multiple matches,
    # getting only the first one, and get the buffer length as well
    packet_3 = router.lowest_buffer_ppv()
    next_len_3 = len(router.buffer)

    assert packet_1 is None and \
        init_len == 0 and \
        packet_2 is min_packet and \
        next_len_2 != 0 and \
        packet_3 is router.buffer[buffer_size - 3] and \
        next_len_3 != 0, \
        "Router.lowest_buffer_ppv() failure"


def test_router_send_packet():
    """
    Test the send_packet() method of the Router
    """
    # Setup the Router object
    name = "router"
    ip = "192.168.1.1"
    send_rate = 10
    buffer_size = 10
    router_1 = Router(name, ip, send_rate, buffer_size)

    # Send the Packet, getting the next hop - None, in this case, because the
    # buffer is empty
    next_hop_1 = router_1.send_packet()

    # Add a Packet to the buffer
    router_1.buffer.append(Packet("192.166.1.1", "192.167.1.1", 5))
    prev_buffer_len = len(router_1.buffer)

    # Send the Packet, getting the next hop - None, in this case, because the
    # Route to the destination is not set
    next_hop_2 = router_1.send_packet()
    after_buffer_len = len(router_1.buffer)

    # Setup an other Router object
    name = "router_2"
    ip = "192.168.1.1"
    send_rate = 10
    buffer_size = 10
    router_2 = Router(name, ip, send_rate, buffer_size)

    # Setup the Interfaces on the Routers
    router_1.add_interface("eth1")
    router_2.add_interface("eth2")

    # Connect the Routers
    router_1.connect_to_interface(router_2, "eth1", "eth2", 10, 10)

    # Add Route to be able to send the Packet
    router_1.add_route(Route("192.168.1.1", "192.168.1.1", "eth1", 10))

    # Add a Packet to the Router's buffer
    packet = Packet("192.167.1.1", "192.168.1.1", 10)
    router_1.buffer.append(packet)

    # Send the Packet, succeeding, and get the next hop and the sending and
    # receiving channels of the corresponding Routers
    next_hop_3 = router_1.send_packet()
    r1_send_channel = router_1.connections[0][0][0].send_channel
    r2_receive_channel = router_2.connections[0][0][0].receive_channel

    assert next_hop_1 is None and \
        next_hop_2 is None and \
        next_hop_3[0] == "192.168.1.1" and \
        next_hop_3[1] == "eth2" and \
        r1_send_channel.payload[0] == packet and \
        r2_receive_channel.payload[0] == packet and \
        prev_buffer_len != 0 and \
        after_buffer_len == 0, \
        "Router.send_packet() failure"


def test_router_receive_packet():
    """
    Test the receive_packet() method of the Router
    """
    # Setup the Router object
    name = "router"
    ip = "192.167.1.1"
    send_rate = 10
    buffer_size = 10
    router_1 = Router(name, ip, send_rate, buffer_size)

    # Add an Interface to the Router
    router_1.add_interface("eth1")

    # Receive Packet on an invalid Interface name, failing
    success_1 = router_1.receive_packet("eth2")

    # Setup an other Router object
    name = "router_2"
    ip = "192.168.1.1"
    send_rate = 10
    buffer_size = 1
    router_2 = Router(name, ip, send_rate, buffer_size)

    # Add an Interface to the other Router
    router_2.add_interface("eth2")

    # Connect the Routers
    router_1.connect_to_interface(router_2, "eth1", "eth2", 10, 10)

    # Receive a Packet whenever there is no Packet to receive, failing
    success_2 = router_1.receive_packet("eth1")

    # Setup the Host object
    name = "host_1"
    ip = "192.167.1.1"
    send_rate = 10
    host_1 = Host(name, ip, send_rate)

    # Set the Application of the Host
    host_1.set_application("host_app", 10, 10, "CONST")

    # Add an Interface to the Host
    host_1.add_interface("eth1")

    # Add a Packet to the Router's buffer with maximum PPV
    router_2.buffer.append(Packet("192.167.1.1", "192.168.1.1", 8))

    # Connect the Host and the Router
    host_1.connect_to_interface(router_2, "eth1", "eth2", 10, 10)

    # Add Routes to the Host and the Router
    host_1.add_route(Route("192.168.1.1", "192.168.1.1", "eth1", 10))
    router_2.add_route(Route("192.167.1.1", "192.167.1.1", "eth2", 8))

    # Put a Packet with lower PPV than the one in the buffer to the receiving
    # Channel of the Router
    packet_1 = Packet("192.167.1.1", "192.168.1.1", 7)
    router_2.get_interface("eth2").receive_channel.fill_payload(packet_1)

    # Receive the Packet successfully, dropping the incoming Packet
    success_3 = router_2.receive_packet("eth2")

    # Get the content of the buffer
    pack_1 = router_2.buffer[0]

    # Put a Packet with higher PPV than the one in the buffer to the receiving
    # Channel of the Router
    packet_2 = Packet("192.167.1.1", "192.168.1.1", 9)
    router_2.get_interface("eth2").receive_channel.fill_payload(packet_2)

    # Receive the Packet successfully, dropping the Packet from the Buffer
    success_4 = router_2.receive_packet("eth2")

    # Get the content of the buffer
    pack_2 = router_2.buffer[0]

    # Empty the buffer
    router_2.buffer = []

    # Put a Packet to the receiving Channel of the Router
    next_hop = host_1.send_packet("192.168.1.1")

    # Receive the Packet, succeeding
    success_5 = router_2.receive_packet(next_hop[1])

    assert not success_1[0] and \
        success_1[1] == 0 and \
        not success_2[0] and \
        success_1[1] == 0 and \
        success_3[0] and \
        success_3[1] == 1 and \
        success_4[0] and \
        success_4[1] == 1 and \
        success_5[0] and \
        success_5[1] == 0 and \
        pack_1 != packet_1 and \
        pack_1.ppv == 8 and \
        pack_2 == packet_2 and \
        pack_2.ppv == 9 and \
        len(router_1.interfaces) != 0 and \
        len(router_2.interfaces) != 0 and \
        len(router_2.buffer) != 0, \
        "Router.receive_packet() failure"
