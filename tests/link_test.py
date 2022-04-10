from src.components.link import Channel, Link
from src.components.packet import Packet

#------------------------------------------------#
# CHANNEL TESTS
#------------------------------------------------#


def test_channel_init():
    """
    Test default init behaviour
    """
    speed = 10
    metrics = 5
    channel = Channel(speed, metrics)
    assert channel.speed == speed and \
        channel.metrics == metrics and \
        len(channel.payload) == 0


def test_channel_negative_speed_init():
    """
    Test default init behaviour
    """
    speed = -10
    metrics = 5
    channel = Channel(speed, metrics)
    assert channel.speed == 1 and \
        channel.metrics == metrics and \
        len(channel.payload) == 0


def test_channel_zero_speed_init():
    """
    Test default init behaviour
    """
    speed = 0
    metrics = 5
    channel = Channel(speed, metrics)
    assert channel.speed == 1 and \
        channel.metrics == metrics and \
        len(channel.payload) == 0


def test_channel_negative_metrics_init():
    """
    Test default init behaviour
    """
    speed = 10
    metrics = -5
    channel = Channel(speed, metrics)
    assert channel.speed == speed and \
        channel.metrics == 1 and \
        len(channel.payload) == 0


def test_channel_zero_metrics_init():
    """
    Test default init behaviour
    """
    speed = 10
    metrics = 0
    channel = Channel(speed, metrics)
    assert channel.speed == speed and \
        channel.metrics == 1 and \
        len(channel.payload) == 0


def test_channel_fill_payload():
    """
    Test adding a Packet to the payload of the Channel
    """
    speed = 10
    metrics = 5
    channel = Channel(speed, metrics)
    previous_len = len(channel.payload)
    p = Packet("127.0.0.1", "127.1.1.1", 10)
    channel.fill_payload(p)
    assert channel.payload[0] == p and \
        len(channel.payload) != previous_len and \
        len(channel.payload) == 1


def test_channel_pop_payload_non_empty():
    """
    Test getting the first added Packet from the payload
    """
    speed = 10
    metrics = 5
    channel = Channel(speed, metrics)
    p = Packet("127.0.0.1", "127.1.1.1", 10)
    p_1 = Packet("127.0.0.1", "127.1.1.1", 7)
    channel.fill_payload(p)
    channel.fill_payload(p_1)
    previous_len = len(channel.payload)
    first_added_item = channel.pop_payload()
    assert first_added_item == p and \
        channel.payload[0] == p_1 and \
        len(channel.payload) != previous_len and \
        len(channel.payload) == 1


def test_channel_pop_payload_empty():
    """
    Test getting the first added Packet from an empty payload
    """
    speed = 10
    metrics = 5
    channel = Channel(speed, metrics)
    previous_len = len(channel.payload)
    p = channel.pop_payload()
    assert p is None and \
        len(channel.payload) == previous_len and \
        len(channel.payload) == 0


#------------------------------------------------#
# LINK TESTS
#------------------------------------------------#


def test_link_init():
    """
    Test default init behaviour
    """
    speed = 10
    metrics = 10
    link = Link(speed, metrics)
    assert link.channels[0].speed == link.channels[1].speed and \
        link.channels[0].metrics == link.channels[1].metrics and \
        link.channels[0].speed == speed and \
        link.channels[0].metrics == metrics and \
        link.channels[0] != link.channels[1]
