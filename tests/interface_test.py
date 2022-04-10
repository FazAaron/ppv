from src.components.interface import Interface
from src.components.link import Link
from src.components.packet import Packet


def test_interface_init():
    """
    Test default init behaviour
    """
    name = "eth1"
    interface = Interface(name)
    assert interface.name == name and \
        interface.link == None and \
        interface.send_channel == None and \
        interface.receive_channel == None, \
        "Interface field mismatch during initialization"


def test_interface_connect_link_success():
    """
    Test successful Interface connection creation
    """
    name = "eth1"
    interface = Interface(name)
    link = Link(10, 10)
    send_channel = link.channels[0]
    receive_channel = link.channels[1]
    success = interface.connect_link(link, send_channel, receive_channel)
    assert success and \
        interface.name == name and \
        interface.link == link and \
        interface.send_channel == send_channel and \
        interface.receive_channel == receive_channel, \
        "Interface.connect_link() failure"


def test_interface_connect_link_failure():
    """
    Test failing Interface connection creation
    """
    name = "eth1"
    interface = Interface(name)
    link = None
    send_channel = None
    receive_channel = None
    success = interface.connect_link(link, send_channel, receive_channel)
    assert not success and \
        interface.name == name and \
        interface.link == None and \
        interface.send_channel == None and \
        interface.receive_channel == None, \
        "Interface.connect_link() failure"


def test_interface_disconnect_link():
    """
    Test disconnecting the Link from the Interface
    """
    name = "eth1"
    interface = Interface(name)
    link = Link(10, 10)
    send_channel = link.channels[0]
    receive_channel = link.channels[1]
    success = interface.connect_link(link, send_channel, receive_channel)
    interface.disconnect_link()
    assert success and \
        interface.name == name and \
        interface.link == None and \
        interface.send_channel == None and \
        interface.receive_channel == None and \
        send_channel != None and \
        receive_channel != None, \
        "Interface.disconnect_link() failure"


def test_interface_receive_from_link_success():
    """
    Test successful receival of a Packet from the receive_channel on the Interface
    """
    name = "eth1"
    interface = Interface(name)
    link = Link(10, 10)
    send_channel = link.channels[0]
    receive_channel = link.channels[1]
    interface.connect_link(link, send_channel, receive_channel)
    p = Packet("192.168.1.1", "192.168.0.1", 10)
    interface.receive_channel.fill_payload(p)
    packet = interface.receive_from_link()
    assert packet is not None and \
        packet == p and \
        len(interface.receive_channel.payload) == 0, \
        "Interface.receive_from_link() failure"


def test_interface_receive_from_link_failure():
    """
    Test failing receival of a Packet from the receive_channel on the Interface
    """
    name = "eth1"
    interface = Interface(name)
    link = Link(10, 10)
    send_channel = link.channels[0]
    receive_channel = link.channels[1]
    interface.connect_link(link, send_channel, receive_channel)
    packet = interface.receive_from_link()
    assert packet is None and\
        len(interface.receive_channel.payload) == 0, \
        "Interface.receive_from_link() failure"


def test_interface_single_put_to_link():
    """
    Test putting a single Packet to the send_channel of the Link
    """
    name = "eth1"
    interface = Interface(name)
    link = Link(10, 10)
    send_channel = link.channels[0]
    receive_channel = link.channels[1]
    interface.connect_link(link, send_channel, receive_channel)
    packet = Packet("192.168.1.1", "192.168.0.1", 10)
    interface.put_to_link(packet)
    assert len(interface.send_channel.payload) == 1 and \
        interface.send_channel.payload[0] == packet, \
        "Interface.put_to_link() failure"


def test_interface_multiple_put_to_link():
    """
    Test putting multiple Packets to the send_channel of the Link
    """
    name = "eth1"
    interface = Interface(name)
    link = Link(10, 10)
    send_channel = link.channels[0]
    receive_channel = link.channels[1]
    interface.connect_link(link, send_channel, receive_channel)
    steps = 10
    packet = None
    for _ in range(steps):
        packet = Packet("192.168.1.1", "192.168.0.1", 10)
        interface.put_to_link(packet)
    payload_length = len(interface.send_channel.payload)
    last_packet = interface.send_channel.payload[payload_length - 1]
    assert len(interface.send_channel.payload) == steps and \
        last_packet is not None and \
        packet is not None and \
        last_packet == packet, \
        "Interface.put_to_link() failure"
