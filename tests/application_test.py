from src.components.application import Application
from src.components.packet import Packet


def test_application_init():
    """
    Test default init behaviour
    """
    # Setup an AIMD type Application object
    name = "test_app"
    ip = "127.0.0.1"
    amount = 10
    send_rate = 10
    app_type = "AIMD"
    app_1 = Application(name, ip, amount, send_rate, app_type)

    assert app_1.name == "test_app" and \
        app_1.ip == "127.0.0.1" and \
        app_1.amount == 10 and \
        app_1.send_rate == 10 and \
        app_1.app_type == "AIMD" and \
        app_1.curr_sent == 0 and \
        "Application field mismatch during initialization"


def test_application_send():
    """
    Test the send() method of the Application
    """
    # Setup the Application object
    name = "test_app"
    ip = "127.0.0.1"
    amount = 10
    send_rate = 10
    app_type = "CONST"
    app = Application(name, ip, amount, send_rate, app_type)

    # Send while it can send (while the curr_sent is less than amount)
    while app.curr_sent < app.amount:
        app.send("127.0.0.1", 1, 10)

    assert app.curr_sent == app.amount and \
        app.send("127.0.0.1", 1, 10) is None, \
        "Application.send() failure"


def test_application_can_send():
    """
    Test the can_send() method of the Application
    """
    # Setup the Application object
    name = "test_app"
    ip = "127.0.0.1"
    amount = 10
    send_rate = 10
    app_type = "CONST"
    app_1 = Application(name, ip, amount, send_rate, app_type)

    # Send amount - 1 amount of Packets, still making sending available
    for _ in range(amount - 1):
        app_1.send("127.0.0.1", 1, 10)

    # Setup the Application object
    name = "test_app"
    ip = "127.0.0.1"
    amount = 10
    send_rate = 10
    app_type = "CONST"
    app_2 = Application(name, ip, amount, send_rate, app_type)

    # Send amount of Packets, making sending not available
    for _ in range(amount):
        app_2.send("127.0.0.1", 1, 10)

    assert app_1.can_send() and app_1.curr_sent < amount and \
        not app_2.can_send() and app_2.curr_sent == amount, \
        "Application.can_send() failure"


def test_application_receive(capsys):
    """
    Test the receive() method of the Application
    """
    # Setup the Application object
    name = "test_app"
    ip = "127.0.0.1"
    amount = 10
    send_rate = 10
    app_type = "CONST"
    app = Application(name, ip, amount, send_rate, app_type)

    # Create the Packet to "receive"
    p = Packet("127.0.1.1", "127.0.0.1", 10, 10)

    # Receive the Packet and capture the output
    app.receive(p)
    captured = capsys.readouterr()

    assert captured.out == f"Received packet on {app.name}:\n{p}\n", \
        "Application.receive() failure - expected different output"
