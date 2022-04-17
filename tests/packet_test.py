from src.components.packet import Packet


def test_packet_init():
    """
    Test default init behaviour
    """
    # Setup the Packet object with proper parameters
    source_ip = "192.168.1.1"
    target_ip = "192.168.0.1"
    ppv = 10
    p_1 = Packet(source_ip, target_ip, ppv)

    # Setup the Packet object with negative PPV
    ppv_o = -10
    p_2 = Packet(source_ip, target_ip, ppv_o)

    # Setup the Packet object with zero PPV
    ppv_o = 0
    p_3 = Packet(source_ip, target_ip, ppv_o)

    assert p_1.source_ip == source_ip and \
        p_1.target_ip == target_ip and \
        p_1.ppv == ppv and \
        p_2.source_ip == source_ip and \
        p_2.target_ip == target_ip and \
        p_2.ppv == 1 and \
        p_3.source_ip == source_ip and \
        p_3.target_ip == target_ip and \
        p_3.ppv == 1, \
        "Packet field mismatch during initialization"
