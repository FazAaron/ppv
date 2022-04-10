from src.components.node import Node, Host, Router

#------------------------------------------------#
# NODE TESTS
#------------------------------------------------#


def test_node_init():
    pass


def test_node_get_best_route_no_match():
    pass


def test_node_get_best_route_found_match():
    pass


def test_node_get_interface():
    pass


def test_node_add_interface():
    pass


def test_node_delete_interface():
    pass


def test_node_connect_to_interface():
    pass


def test_node_disconnect_interface():
    pass

#------------------------------------------------#
# HOST TESTS
#------------------------------------------------#


def test_host_init():
    pass


def test_host_set_application():
    pass


def test_host_send_packet():
    pass


def test_host_receive_packet():
    pass


def test_host_handle_feedback():
    pass


def test_host_receive_feedback():
    pass

# TODO: Test PPV generation properly
def test_host_something_ppv(): pass

#------------------------------------------------#
# ROUTER TESTS
#------------------------------------------------#


def test_router_init():
    pass


def test_router_lowest_buffer_ppv():
    pass


def test_router_send_packet():
    pass


def test_router_receive_packet():
    pass


def test_router_send_feedback():
    pass


def test_router_receive_feedback():
    pass
