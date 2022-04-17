from src.components.link import Channel, Link
from src.components.packet import Packet

#------------------------------------------------#
# CHANNEL TESTS
#------------------------------------------------#


def test_channel_init():
    """
    Test default init behaviour
    """
    # Setup a Channel object with proper parameters
    speed_1 = 10
    metrics_1 = 5
    channel_1 = Channel(speed_1, metrics_1)

    # Setup a Channel object with negative speed parameter
    speed_2 = -10
    metrics_2 = 5
    channel_2 = Channel(speed_2, metrics_2)

    # Setup a Channel object with zero speed parameter
    speed_3 = 0
    metrics_3 = 5
    channel_3 = Channel(speed_3, metrics_3)

    # Setup a Channel object with negative metrics parameter
    speed_4 = 10
    metrics_4 = -5
    channel_4 = Channel(speed_4, metrics_4)

    # Setup a Channel object with zero metrics parameter
    speed_5 = 10
    metrics_5 = 0
    channel_5 = Channel(speed_5, metrics_5)

    assert channel_1.speed == speed_1 and \
        channel_1.metrics == metrics_1 and \
        len(channel_1.payload) == 0 and \
        channel_2.speed == 1 and \
        channel_2.metrics == metrics_2 and \
        len(channel_2.payload) == 0 and \
        channel_3.speed == 1 and \
        channel_3.metrics == metrics_3 and \
        len(channel_3.payload) == 0 and \
        channel_4.speed == speed_4 and \
        channel_4.metrics == 1 and \
        len(channel_4.payload) == 0 and \
        channel_5.speed == speed_5 and \
        channel_5.metrics == 1 and \
        len(channel_5.payload) == 0, \
        "Channel field mismatch during initialization"


def test_channel_fill_payload():
    """
    Test the fill_payload() method of the Channel
    """
    # Setup a Channel object
    speed = 10
    metrics = 5
    channel = Channel(speed, metrics)

    # Get the initial length of the payload
    previous_len = len(channel.payload)

    # Add the Packet to the payload
    p = Packet("127.0.0.1", "127.1.1.1", 10)
    channel.fill_payload(p)

    assert channel.payload[0] == p and \
        len(channel.payload) != previous_len and \
        len(channel.payload) == 1, \
        "Channel.fill_payload() failure"


def test_channel_pop_payload():
    """
    Test the pop_payload() method of the Channel
    """
    # Setup the Channel object
    speed = 10
    metrics = 5
    channel_1 = Channel(speed, metrics)

    # Fill the payload of the Channel with Packets
    p_1 = Packet("127.0.0.1", "127.1.1.1", 10)
    p_2 = Packet("127.0.0.1", "127.1.1.1", 7)
    channel_1.fill_payload(p_1)
    channel_1.fill_payload(p_2)

    # Get the length of the Channel's payload and the item first added
    previous_len_1 = len(channel_1.payload)
    first_added_item = channel_1.pop_payload()

    # Setup the Channel object
    speed = 10
    metrics = 5
    channel_2 = Channel(speed, metrics)

    # Get the length of the Channel's payload and the item first added,
    # which is in this case None
    previous_len_2 = len(channel_2.payload)
    p_3 = channel_2.pop_payload()

    assert first_added_item == p_1 and \
        channel_1.payload[0] == p_2 and \
        len(channel_1.payload) != previous_len_1 and \
        len(channel_1.payload) == 1 and \
        p_3 is None and \
        len(channel_2.payload) == previous_len_2 and \
        len(channel_2.payload) == 0, \
        "Channel.pop_payload() failure"


#------------------------------------------------#
# LINK TESTS
#------------------------------------------------#


def test_link_init():
    """
    Test default init behaviour
    """
    # Setup the Link object
    speed = 10
    metrics = 10
    link = Link(speed, metrics)

    assert link.channels[0].speed == link.channels[1].speed and \
        link.channels[0].metrics == link.channels[1].metrics and \
        link.channels[0].speed == speed and \
        link.channels[0].metrics == metrics and \
        link.channels[0] != link.channels[1], \
        "Link field mismatch during initialization"
