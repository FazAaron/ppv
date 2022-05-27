from src.components.packet import Packet


def test_packet_init():
    """
    Test default init behaviour
    """
    # Setup the Packet object with proper parameters
    source_ip = "192.168.1.1"
    target_ip = "192.168.0.1"
    ppv = 10
    size = 10
    p_1 = Packet(source_ip, target_ip, ppv, size)

    assert p_1.source_ip == source_ip and \
        p_1.target_ip == target_ip and \
        p_1.ppv == ppv and \
        p_1.size == size, \
        "Packet field mismatch during initialization"
