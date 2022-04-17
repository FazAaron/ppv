from src.components.interface import Interface
from src.components.link import Link
from src.components.packet import Packet


def test_interface_init():
    """
    Test default init behaviour
    """
    # Setup the Interface object
    name = "eth1"
    interface = Interface(name)

    assert interface.name == name and \
        interface.link == None and \
        interface.send_channel == None and \
        interface.receive_channel == None, \
        "Interface field mismatch during initialization"


def test_interface_connect_link():
    """
    Test the connect_link() method of the Interface
    """
    # Setup a connection failure
    name = "eth1"
    interface_1 = Interface(name)
    link = None
    send_channel = None
    receive_channel = None
    none_success = interface_1.connect_link(
        link, send_channel, receive_channel)

    # Setup a successful connection
    name = "eth2"
    interface_2 = Interface(name)
    link = Link(10, 10)
    send_channel = link.channels[0]
    receive_channel = link.channels[1]
    success = interface_2.connect_link(link, send_channel, receive_channel)

    assert not none_success and \
        interface_1.name == "eth1" and \
        interface_1.link == None and \
        interface_1.send_channel == None and \
        interface_1.receive_channel == None and \
        success and \
        interface_2.name == "eth2" and \
        interface_2.link == link and \
        interface_2.send_channel == send_channel and \
        interface_2.receive_channel == receive_channel, \
        "Interface.connect_link() failure"


def test_interface_disconnect_link():
    """
    Test the disconnect_link() method of the Interface
    """
    # Setup the Interface object
    name = "eth1"
    interface = Interface(name)

    # Connect the Link to the Interface
    link = Link(10, 10)
    send_channel = link.channels[0]
    receive_channel = link.channels[1]
    success = interface.connect_link(link, send_channel, receive_channel)

    # Disconnect the Link from the Interface
    interface.disconnect_link()

    assert success and \
        interface.name == name and \
        interface.link == None and \
        interface.send_channel == None and \
        interface.receive_channel == None and \
        send_channel != None and \
        receive_channel != None, \
        "Interface.disconnect_link() failure"


def test_interface_receive_from_link():
    """
    Test the receive_from_link() method of the Interface
    """
    # Setup an Interface object
    name = "eth1"
    interface_1 = Interface(name)

    # Connect the Link to the Interface
    link = Link(10, 10)
    send_channel = link.channels[0]
    receive_channel = link.channels[1]
    interface_1.connect_link(link, send_channel, receive_channel)

    # Add a Packet to the receiving Channel of the Interface
    p = Packet("192.168.1.1", "192.168.0.1", 10)
    interface_1.receive_channel.fill_payload(p)

    # Receive the Packet from the receiving Channel successfully
    packet_1 = interface_1.receive_from_link()

    # Setup an Interface object
    name = "eth1"
    interface_2 = Interface(name)

    # Connect the Link to the Interface
    link = Link(10, 10)
    send_channel = link.channels[0]
    receive_channel = link.channels[1]
    interface_2.connect_link(link, send_channel, receive_channel)

    # Receive the Packet from the receiving Channel with a failure
    packet_2 = interface_2.receive_from_link()

    assert packet_1 is not None and \
        packet_1 == p and \
        len(interface_1.receive_channel.payload) == 0 and \
        packet_2 is None and \
        len(interface_2.receive_channel.payload) == 0, \
        "Interface.receive_from_link() failure"


def test_interface_put_to_link():
    """
    Test the put_to_linK() method of the Interface
    """
    # Setup an Interface object
    name = "eth1"
    interface_1 = Interface(name)

    # Connect the Link to the Interface
    link = Link(10, 10)
    send_channel = link.channels[0]
    receive_channel = link.channels[1]
    interface_1.connect_link(link, send_channel, receive_channel)

    # Put a single to the Link
    packet_1 = Packet("192.168.1.1", "192.168.0.1", 10)
    interface_1.put_to_link(packet_1)

    # Setup the Interface object
    name = "eth1"
    interface_2 = Interface(name)

    # Connect the Link to the Interface
    link = Link(10, 10)
    send_channel = link.channels[0]
    receive_channel = link.channels[1]
    interface_2.connect_link(link, send_channel, receive_channel)

    # Put steps amount of Packets on the Link
    steps = 10
    packet_2 = None
    for _ in range(steps):
        packet_2 = Packet("192.168.1.1", "192.168.0.1", 10)
        interface_2.put_to_link(packet_2)

    # Get the length of the sending Channel's payload and the last Packet
    payload_length = len(interface_2.send_channel.payload)
    last_packet = interface_2.send_channel.payload[payload_length - 1]

    assert len(interface_1.send_channel.payload) == 1 and \
        interface_1.send_channel.payload[0] == packet_1 and \
        len(interface_2.send_channel.payload) == steps and \
        last_packet is not None and \
        packet_2 is not None and \
        last_packet == packet_2, \
        "Interface.put_to_link() failure"
