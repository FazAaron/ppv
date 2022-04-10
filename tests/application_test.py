from src.components.application import Application
from src.components.packet import Packet


def test_application_aimd_app_type_init():
    """
    Test default init behaviour with AIMD app_type
    """
    name = "test_app"
    ip = "127.0.0.1"
    amount = 10
    send_rate = 10
    app_type = "AIMD"
    app = Application(name, ip, amount, send_rate, app_type)
    assert app.name == name and \
        app.ip == ip and \
        app.amount == amount and \
        app.send_rate == send_rate and \
        app.app_type == app_type and \
        app.curr_sent == 0, \
        "Application field mismatch during AIMD app_type initialization"


def test_application_const_app_type_init():
    """
    Test default init behaviour with CONST app_type
    """
    name = "test_app"
    ip = "127.0.0.1"
    amount = 10
    send_rate = 10
    app_type = "CONST"
    app = Application(name, ip, amount, send_rate, app_type)
    assert app.name == name and \
        app.ip == ip and \
        app.amount == amount and \
        app.send_rate == send_rate and \
        app.app_type == app_type and \
        app.curr_sent == 0, \
        "Application field mismatch during CONST app_type initialization"


def test_application_other_app_type_init():
    """
    Test default init behaviour with any app_type other than AIMD and CONST\n
    The Application's type will be set to CONST in this case
    """
    name = "test_app"
    ip = "127.0.0.1"
    amount = 10
    send_rate = 10
    app_type = "OTHER"
    app = Application(name, ip, amount, send_rate, app_type)
    assert app.name == name and \
        app.ip == ip and \
        app.amount == amount and \
        app.send_rate == send_rate and \
        app.app_type != app_type and \
        app.app_type == "CONST" and \
        app.curr_sent == 0, \
        "Application field mismatch during OTHER app_type initialization"


def test_application_negative_amount_init():
    """
    Test default init behaviour with negative amount given\n
    The Application's amount will be set to 0 in this case
    """
    name = "test_app"
    ip = "127.0.0.1"
    amount = -10
    send_rate = 10
    app_type = "CONST"
    app = Application(name, ip, amount, send_rate, app_type)
    assert app.name == name and \
        app.ip == ip and \
        app.amount != amount and \
        app.amount == 0 and \
        app.send_rate == send_rate and \
        app.app_type == app_type and \
        app.curr_sent == 0, \
        "Application field mismatch during negative amount initialization"


def test_application_send():
    """
    Test the send() method of the Application\n
    Every call to send increases curr_sent by 1\n
    Returns None if the can_send() returns False
    """
    name = "test_app"
    ip = "127.0.0.1"
    amount = 10
    send_rate = 10
    app_type = "CONST"
    app = Application(name, ip, amount, send_rate, app_type)
    while app.can_send():
        app.send("127.0.0.1", 1)
    assert not app.can_send() and \
        app.curr_sent == amount and \
        app.send("127.0.0.1", 1) is None, \
        "Application.send() failure"


def test_application_can_send():
    """
    Test the can_send() method of the Application\n
    Returns True if the curr_sent is lower than the amount
    """
    name = "test_app"
    ip = "127.0.0.1"
    amount = 10
    send_rate = 10
    app_type = "CONST"
    app = Application(name, ip, amount, send_rate, app_type)
    for _ in range(amount - 1):
        app.send("127.0.0.1", 1)
    assert app.can_send() and app.curr_sent < amount, \
        "Application.can_send() failure - should be able to send"


def test_application_cant_send():
    """
    Test the can_send() method of the Application\n
    Returns False if the curr_sent is equal or greater than the amount
    """
    name = "test_app"
    ip = "127.0.0.1"
    amount = 10
    send_rate = 10
    app_type = "CONST"
    app = Application(name, ip, amount, send_rate, app_type)
    for _ in range(amount):
        app.send("127.0.0.1", 1)
    assert not app.can_send() and app.curr_sent == amount, \
        "Application.can_send() failure - shouldn't be able to send"


def test_application_receive(capsys):
    """
    Test receiving a Packet on the Application
    Prints to stdout if a Packet was received
    """
    name = "test_app"
    ip = "127.0.0.1"
    amount = 10
    send_rate = 10
    app_type = "CONST"
    app = Application(name, ip, amount, send_rate, app_type)
    p = Packet("127.0.1.1", "127.0.0.1", 10)
    app.receive(p)
    captured = capsys.readouterr()
    assert captured.out == f"Received packet on {app.name}:\n{p}\n", \
        "Application.receive() failure - expected different output"
