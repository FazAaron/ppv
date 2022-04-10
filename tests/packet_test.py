from src.components.packet import Packet


def test_packet_init():
    """
    Test default init behaviour with proper parameters
    """
    source_ip = "192.168.1.1"
    target_ip = "192.168.0.1"
    ppv = 10
    p = Packet(source_ip, target_ip, ppv)
    assert p.source_ip == source_ip and \
        p.target_ip == target_ip and \
        p.ppv == ppv, "Packet field mismatch during initialization"


def test_packet_negative_ppv_init():
    """
    Test default init behaviour with negative PPV given\n
    PPV is set to 1 if the value given is below zero or is zero
    """
    source_ip = "192.168.1.1"
    target_ip = "192.168.0.1"
    ppv = -10
    p = Packet(source_ip, target_ip, ppv)
    assert p.source_ip == source_ip and \
        p.target_ip == target_ip and \
        p.ppv != ppv and \
        p.ppv == 1, \
        "Packet field mismatch during negative PPV initialization"


def test_packet_zero_ppv_init():
    """
    Test default init behaviour with negative PPV given\n
    PPV is set to 1 if the value given is below zero or is zero
    """
    source_ip = "192.168.1.1"
    target_ip = "192.168.0.1"
    ppv = 0
    p = Packet(source_ip, target_ip, ppv)
    assert p.source_ip == source_ip and \
        p.target_ip == target_ip and \
        p.ppv != ppv and \
        p.ppv == 1, \
        "Packet field mismatch during zero PPV initialization"
