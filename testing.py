from src.components.node import Host, Router
from src.components.routing_table import Route
from src.components.packet import Packet
from src.components.network import Network
from src.components.link import Link
from src.components.application import Application

#node1: Host = Host("sender", "192.168.1.1", 5)
#node1.set_application("sender-app", 2, node1.send_rate, "CONST")
#node2: Host = Host("receiver", "192.168.0.1", 3)
#node2.set_application("receiver-app", 0, node2.send_rate, "CONST")

#node3: Router = Router("first", "192.167.1.1", 3, 5)
#node4: Router = Router("second", "192.167.0.1", 4, 1)

#node1.add_interface("out_1")
##node1.add_interface("out_2")
##node2.add_interface("in_1")
#node2.add_interface("in_2")
##node1.connect_to_interface(node2, "out_1", "in_1", 10, 10)
##node1.connect_to_interface(node2, "out_2", "in_2", 15, 15)
##node1.delete_interface("out_2")
## node1.print_details()
## node2.print_details()

#node3.add_interface("in")
#node3.add_interface("out")

#node4.add_interface("in")
#node4.add_interface("out")

#node1.connect_to_interface(node3, "out_1", "in", 10, 100)
##node1.connect_to_interface(node4, "out_2", "in", 70, 15)
##node2.connect_to_interface(node3, "in_1", "out", 10, 100)
#node2.connect_to_interface(node4, "in_2", "out", 70, 15)
#node3.connect_to_interface(node4, "out", "in", 10, 10)

#node1.add_route(Route("192.168.0.1", "192.167.1.1", "out_1", 10))
##node1.add_route(Route("192.168.0.1", "192.167.0.1", "out_2", 15))

#node3.add_route(Route("192.168.0.1", "192.167.0.1", "out", 5))
#node3.add_route(Route("192.168.1.1", "192.168.1.1", "in", 10))
##node3.add_route(Route("192.168.1.1", "192.168.1.1", "in", 5))

#node4.add_route(Route("192.168.0.1", "192.168.0.1", "out", 20))
#node4.add_route(Route("192.168.1.1", "192.167.1.1", "in", 30))
##node4.add_route(Route("192.168.1.1", "192.168.1.1", "in", 20))

#destination: str = "192.168.0.1"
#node1.send_packet(destination)
#node3.receive_packet("in")
#node3.send_packet()
#node4.receive_packet("in")
#node4.send_packet()
#node2.receive_packet("in_2")
## while node1.application.can_send():
##    next_node: str = node1.send_packet(destination)
##    if next_node == node3.ip:
##        for connection in node1.connections:
##            if connection[1][0] in node3.interfaces:
##                node3.receive_packet(connection[1][0].name)
##        node3.send_packet()
##    elif next_node == node4.ip:
##        for connection in node1.connections:
##            if connection[1][0] in node4.interfaces:
##                node4.receive_packet(connection[1][0].name)
##        node4.send_packet()
##    node2.receive_packet("in_1")

## print(first)
## print(snd)
# node1: Host = Host("sender", "192.168.1.1", 5)
# node1.set_application("LOL", 10, 10, "AIMDA")
# node1.print_details()
# node2: Router = Router("LOL", "LOL", 10, 10)
# node2.print_details()

network: Network = Network()
network.create_host("first", "192.168.1.1", 10)
network.set_application("first", "first_app", 10, 10, "CONST")
network.add_interface("first", "eth1")

network.create_host("snd", "192.168.0.1", 10)
network.set_application("snd", "snd_app", 10, 10, "AIMD")
network.add_interface("snd", "eth2")

network.connect_node_interfaces("first", "snd", "eth1", "eth2", 10, 10)
# network.disconnect_node_interface("first", "eth1")

# network.create_router("third", "192.167.1.1", 10, 100)
# network.delete_interface("first", "eth1")
# network.print_hosts()

# network.print_routers()
network.update_routing_tables()
print(network.graph)