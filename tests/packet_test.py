from src.components.packet import Packet

def test_proper_init():
    """
    Creation of a Packet with proper parameters
    """
    source_ip: str    = "192.168.1.1"
    target_ip: str    = "192.168.0.1"
    ppv:       int    = 10
    p:         Packet = Packet(source_ip, target_ip, ppv)
    assert p.source_ip == source_ip and \
           p.target_ip == target_ip and \
           p.ppv       == ppv, "packet field mismatch during initialization"

def test_negative_ppv_init():
    """
    PPV is set to 1 if the value given is below zero or is zero
    """
    source_ip: str    = "192.168.1.1"
    target_ip: str    = "192.168.0.1"
    ppv:       int    = -10
    p:         Packet = Packet(source_ip, target_ip, ppv)
    assert p.source_ip == source_ip and \
           p.target_ip == target_ip and \
           p.ppv       == 1, \
           "packet field mismatch during negative PPV initialization"
