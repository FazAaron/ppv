"""
This module makes MainHandler objects available for use when imported
"""
# Built-in modules
from threading import Lock, Thread
import time
from tkinter import messagebox
from typing import Callable, List, Tuple

# Self-made modules
from src.components.node import Node
from src.components.network import Network
from src.components.node import Host, Router
from src.event_handlers.object_canvas_handler import ObjectCanvasHandler
from src.event_handlers.object_frame_handler import ObjectFrameHandler
from src.event_handlers.statistics_frame_handler import StatisticsFrameHandler
from src.graphic_handlers.main_window import MainWindow
from src.graphic_handlers.widget_container import WidgetContainer
from src.utils.logger import Logger


class MainHandler:
    """
    This class is used to connect together the handlers for every graphical \
    component, providing them with bindings to different events, creating \
    a user-interactive graphical interface

    Data members:
    main_window              (MainWindow): The main window of the GUI, \
                             containing everything
    network                  (Network): The main object of the components, \
                             containing everything
    object_canvas_handler    (ObjectCanvasHandler): The ObjectCanvas handling\
                             object
    object_frame_handler     (ObjectFrameHandler): The object frame handling \
                             object
    statistics_frame_handler (StatisticsFrameHandler): The statistics frame \
                             handling object
    logger                   (Logger): The logger object, logging neccessary \
                             actions
    hosts                    (List[Tuple[int, str]]): Host information stored
    routers                  (List[Tuple[int, str]]): Router information stored
    links                    (List[Tuple[int, str, str]]): Link information stored
    host_sending             (List[bool]): Which Host is currently sending
    statistics_lock          (Lock): Locks for the StatisticsFrameHandler's \
                             label updating
    network_lock             (Lock): Lock for the Network object's access
    message_lock             (Lock): Lock for the ObjectCanvasHandler's message \
                             showing
    sending_lock             (Lock): Lock for the host_sending object's access
    """

    def __init__(self, main_window: MainWindow, network: Network) -> None:
        self.main_window: MainWindow = main_window
        self.network: Network = network

        # Create the Handlers for every single GUI component
        content: WidgetContainer = self.main_window.content
        self.object_canvas_handler: ObjectCanvasHandler = ObjectCanvasHandler(
            content.object_canvas)
        self.object_frame_handler: ObjectFrameHandler = ObjectFrameHandler(
            content.object_frame)
        self.statistics_frame_handler: StatisticsFrameHandler = StatisticsFrameHandler(
            content.statistics_frame)

        # Create a Logger object
        self.logger = Logger("conf/logger_config.json")

        # Setup the List of Hosts, Routers and Links - needed to connect
        # the GUI and Network, storing information that helps identify them
        # in either
        self.hosts: List[Tuple[int, str]] = []
        self.routers: List[Tuple[int, str]] = []
        self.links: List[Tuple[int, str, str, str, str]] = []

        # Keeping track of which Host is sending
        self.host_sending: List[bool] = []

        # Locks for avoiding race conditions
        self.statistics_lock: Lock = Lock()
        self.network_lock: Lock = Lock()
        self.message_lock: Lock = Lock()
        self.sending_lock: Lock = Lock()

        # Setup the bindings for the Handlers
        self.__bind_to_object_frame_handler()
        self.__bind_to_object_canvas_handler()

    def __exit_prompt(self) -> None:
        """
        Opens a pop-up prompt asking a yes/no question for the user, whether \
        they want to exit or not
        """
        # Create a prompt asking for an answer
        answer: bool = messagebox.askyesno(title="Exit application",
                                           message="Are you sure you want to"
                                           "exit the application?")
        # If the answer was yes, exit the application
        if answer:
            self.main_window.exit()

    def __bind_to_object_frame_handler(self) -> None:
        """
        Bind events to the ObjectFrame's Button Widget, prompting a yes/no
        question when clicked
        """
        # Bind to the ObjectFrame's exit Button
        self.object_frame_handler.bind_to_exit(self.__exit_prompt)

    def __show_options_menu(self, event: str) -> None:
        """
        Shows a pop-up Menu at the given coordinates\n
        The Menu shown is based on whether the coordinates match a component's \
        coordinates or not

        Parameters:
        event (str): The event that happens
        """
        # This is going to be binded to the right-click on the Canvas
        self.object_canvas_handler.show_menu(event.x, event.y)

    def __show_and_log(self, comp: str, message: str, severity: str) -> None:
        """
        Shows a message on the right-hand side corner of the screen and then \
        logs to a file

        Parameters:
        comp     (str): The component the message is about
        message  (str): The message
        severity (str): The severity of the message, can be information or error
        """
        # Lock the ObjectCanvasHandler's message showing, to avoid race
        # conditions
        with self.message_lock:
            # Shows a message
            self.object_canvas_handler.show_message(message, 2000)
        # Logs the message to a file
        self.logger.write(comp, message, severity)

    def __handle_component_add_submit(self) -> None:
        """
        Handles the component placement Frame's submit Button event
        """
        # Used whenever we are in the Host or Router placement Frame, and
        # this handles pressing the submit Button
        self.object_canvas_handler.submit_input()

    def __handle_interface_add_submit(self) -> None:
        """
        Handles the add Interface Frame's submit Button event
        """
        # Get the coordinates where the Menu was opened before the Frame
        # This is needed to avoid having to use the event.x and event.y
        # coordinates
        x: int = self.object_canvas_handler.menu_x
        y: int = self.object_canvas_handler.menu_y

        # Check what intersects with the mouse (or the Menu in this case)
        intersection_details: Tuple[str, int] = \
            self.object_canvas_handler.intersects(x, y, 1, 1)

        # Get the user input from the Frame's Entries
        success: bool = self.object_canvas_handler.submit_input()
        user_input: List[str] = self.object_canvas_handler.input_data

        # If the regex failed, do nothing
        if not success:
            return

        # Logic based on whether the intersection happened on a Host or a
        # Router
        if intersection_details[0] == "HOST":
            for host in self.hosts:
                # If the item_id matches
                if host[0] == intersection_details[1]:
                    host_name = host[1]
                    interface_name = user_input[0]

                    # To avoid race conditions on the Network object
                    with self.network_lock:
                        # Try creating the Interface
                        created: bool = self.network.add_interface(
                            host_name, interface_name)

                    # If it was created / not created, show a message and log it
                    # accordingly
                    if created:
                        self.__show_and_log(f"Host {host_name} - Interface"
                                            f" {interface_name}",
                                            "Successfully created Interface "
                                            f"{interface_name} on Host {host_name}.",
                                            "Information")
                    else:
                        self.__show_and_log(f"Host {host_name} - Interface"
                                            f" {interface_name}",
                                            "Failed to create Interface "
                                            f"{interface_name} on Host "
                                            f"{host_name}: duplicate Interface"
                                            " name on Host.",
                                            "Information")
        elif intersection_details[0] == "ROUTER":
            for router in self.routers:
                # If the item_id matches
                if router[0] == intersection_details[1]:
                    router_name = router[1]
                    interface_name = user_input[0]

                    # To avoid race conditions on the Network object
                    with self.network_lock:
                        # Try creating the Interface
                        created: bool = self.network.add_interface(
                            router_name, interface_name)

                    # If it was created / not created, show a message and log it
                    # accordingly
                    if created:
                        self.__show_and_log(f"Router {router_name} - Interface"
                                            f" {interface_name}",
                                            "Successfully created Interface "
                                            f"{interface_name} on Router "
                                            f"{router_name}.",
                                            "Information")
                    else:
                        self.__show_and_log(f"Router {router_name} - Interface"
                                            f" {interface_name}",
                                            "Failed to create Interface "
                                            f"{interface_name} on Router "
                                            f"{router_name}: duplicate "
                                            "Interface name on Router.",
                                            "Information")

    def __update_statistics(self) -> None:
        """
        Updates the statistics inside the StatisticsFrame
        """
        # Gets the statistics - no locking needed, because this should be called
        # instantly after the Network's method was called, to provide 100% precision
        total_packets:   int = self.network.total_pack
        packets_dropped: int = self.network.dropped_pack

        # Lock the StatisticsFrame object's access to avoid race conditions
        with self.statistics_lock:
            # Updates the statistics in the StatisticsFrame
            self.statistics_frame_handler.update_labels(total_packets,
                                                        packets_dropped)

    def __handle_interface_delete_submit(self) -> None:
        """
        Handles the delete Interface Frame's submit Button event
        """
        # TODO: check sending
        # Get the coordinates where the Menu was opened before the Frame
        # This is needed to avoid having to use the event.x and event.y
        # coordinates
        x: int = self.object_canvas_handler.menu_x
        y: int = self.object_canvas_handler.menu_y

        # Check what intersects with the mouse (or the Menu in this case)
        intersection_details: Tuple[str, int] = self.object_canvas_handler.intersects(
            x, y, 1, 1)

        # Get the user input from the Frame's Entries
        success: bool = self.object_canvas_handler.submit_input()
        user_input: List[str] = self.object_canvas_handler.input_data

        # If the regex failed, do nothing
        if not success:
            return

        # Logic based on whether the intersection happened on a Host or a
        # Router
        if intersection_details[0] == "HOST":
            for host in self.hosts:
                # If the item_id matches
                if host[0] == intersection_details[1]:
                    host_name: str = host[1]
                    interface_name: str = user_input[0]

                    # To avoid race conditions on the Network object
                    with self.network_lock:
                        # Try deleting the Interface
                        deleted: bool = self.network.delete_interface(
                            host_name, interface_name)

                        # If deletion was successful, update the statistics
                        if deleted:
                            self.__update_statistics()

                    # If it was deleted / not deleted, show a message and log it
                    # accordingly, and delete the Link connected to it, if
                    # the deletion succeeded
                    if deleted:
                        for link in self.links:
                            if (host_name == link[1] and
                                interface_name == link[2]) \
                                or (host_name == link[3] and
                                    interface_name == link[4]):
                                self.links.remove(link)
                                self.object_canvas_handler.delete_link(
                                    link[0])
                                break
                        self.__show_and_log(f"Host {host_name} - Interface "
                                            f"{interface_name}",
                                            f"Successfully deleted Interface "
                                            f"{interface_name} on Host "
                                            f"{host_name}.",
                                            "Information")
                    else:
                        self.__show_and_log(f"Host {host_name} - Interface "
                                            f"{interface_name}",
                                            f"Failed to delete Interface "
                                            f"{interface_name} on Host "
                                            f"{host_name}: no such Interface on Host.",
                                            "Information")
        elif intersection_details[0] == "ROUTER":
            for router in self.routers:
                # If the item_id matches
                if router[0] == intersection_details[1]:
                    router_name: str = router[1]
                    interface_name: str = user_input[0]

                    # To avoid race conditions on the Network object
                    with self.network_lock:
                        # Try deleting the Interface
                        deleted: bool = self.network.delete_interface(
                            router_name, interface_name)

                        # If deletion was successful, we can update the statistics
                        if deleted:
                            self.__update_statistics()

                    # If it was deleted / not deleted, show a message and log it
                    # accordingly, and delete the Link connected to it, if
                    # the deletion succeeded
                    if deleted:
                        for link in self.links:
                            if (router_name == link[1] and
                                interface_name == link[2]) \
                                or (router_name == link[3] and
                                    interface_name == link[4]):
                                self.links.remove(link)
                                self.object_canvas_handler.delete_link(
                                    link[0])
                                break
                        self.__show_and_log(f"Router {router_name} - Interface"
                                            f" {interface_name}",
                                            f"Successfully deleted Interface "
                                            f"{interface_name} on Router "
                                            f"{router_name}.",
                                            "Information")
                    else:
                        self.__show_and_log(f"Router {router_name} - Interface"
                                            f" {interface_name}",
                                            f"Failed to delete Interface "
                                            f"{interface_name} on Router "
                                            f"{router_name}: no such Interface"
                                            " on Host.",
                                            "Information")

    def __handle_set_application_submit(self) -> None:
        """
        Handles the set Application Frame's submit Button event
        """
        # Get the coordinates where the Menu was opened before the Frame
        # This is needed to avoid having to use the event.x and event.y
        # coordinates
        x: int = self.object_canvas_handler.menu_x
        y: int = self.object_canvas_handler.menu_y

        # Check what intersects with the mouse (or the Menu in this case)
        intersection_details: Tuple[str, int] = self.object_canvas_handler.intersects(
            x, y, 1, 1)

        # Get the user input from the Frame's Entries
        success: bool = self.object_canvas_handler.submit_input()
        user_input: List[str] = self.object_canvas_handler.input_data

        # If the regex failed, do nothing
        if not success:
            return

        for host in self.hosts:
            # If the item_id matches
            if host[0] == intersection_details[1]:
                app_name: str = user_input[0]
                host_name: str = host[1]

                idx: int = self.hosts.index(host)

                # To avoid race conditions on the host_sending variables
                with self.sending_lock:
                    self.host_sending[idx] = False

                # To avoid race conditions on the Network object
                with self.network_lock:
                    # Set the Application
                    applied: bool = self.network.set_application(
                        host_name, app_name, user_input[1], 
                        user_input[2], user_input[3])

                # If it was set / not set, show a message and log it
                # accordingly
                # The else branch can only happen if some kind of error occurs
                if applied:
                    self.__show_and_log(f"Host {host_name} - Application "
                                        f"{app_name}",
                                        f"Successfully set Application "
                                        f"{app_name} on Host {host_name}.",
                                        "Information")
                else:
                    self.__show_and_log(f"Host {host_name} - Application "
                                        f"{app_name}",
                                        f"Failed to set Application "
                                        f"{app_name} on Host {host_name}.",
                                        "Error")

    def __link_thread(self, next_hop: str, interface: str) -> None:
        pass

    def __host_thread(self, host: Host, idx: int, target: Host) -> None:
        with self.sending_lock:
            self.host_sending[idx] = True
        is_sending: bool = True
        receiver_data: Tuple[str, str, str] = None
        sleep_time: float = 1 / host.send_rate
        while is_sending:

            with self.sending_lock:
                is_sending = self.host_sending[idx]

            if is_sending:
                with self.network_lock:
                    receiver_data = self.network.send_packet(host.name, target.name)
                    is_sending = self.network.can_send(host.name)

            time.sleep(sleep_time) 

    def __router_thread(self, router: Router) -> None:
        while True:
            if router.get_buffer_length() != 0:
                pass

    def __handle_send_submit(self) -> None:
        """
        Handles the start sending Frame's submit Button event
        """
        # Get the coordinates where the Menu was opened before the Frame
        # This is needed to avoid having to use the event.x and event.y
        # coordinates
        x: int = self.object_canvas_handler.menu_x
        y: int = self.object_canvas_handler.menu_y

        # Check what intersects with the mouse (or the Menu in this case)
        intersection_details: Tuple[str, int] = self.object_canvas_handler.intersects(
            x, y, 1, 1)

        # Get the user input from the Frame's Entries
        success: bool = self.object_canvas_handler.submit_input()
        user_input: List[str] = self.object_canvas_handler.input_data

        # If the regex failed, do nothing
        if not success:
            return

        # We can only start sending from Hosts
        for host in self.hosts:
            # If the item_id matches
            if host[0] == intersection_details[1]:
                host_name: str = host[1]
                target: str = user_input[0]

                # To avoid race conditions on the Network object
                with self.network_lock:
                    target_node: Host = self.network.get_host(target)

                if target_node is None:
                    self.__show_and_log(f"Host {host_name} <-> Host {target}",
                                        f"Failed to start sending from Host "
                                        f"{host_name} to Host {target}: "
                                        "invalid target Host.",
                                        "Information")
                    # Return, because there is no such Node
                    return
                elif host[1] == target_node.name or host[1] == target_node.ip:
                    self.__show_and_log(f"Host {host_name} <-> Host {target}",
                                        f"Failed to start sending from Host "
                                        f"{host_name} to Host {target}: "
                                        "can't send to self.",
                                        "Information")
                    # Return, because can't send to self
                    return

                # Get the index for the host_sending variable
                idx: int = self.hosts.index(host)

                # To avoid race conditions on the host_sending variable
                with self.sending_lock:
                    is_sending: bool = self.host_sending[idx]

                # If the Host is already sending, just return, and let it send
                if is_sending == True:
                    self.__show_and_log(f"Host {host_name} <-> Host {target}",
                                        f"Host {host_name} is already sending.",
                                        "Information")
                    return

                self.__show_and_log(f"Host {host_name} <-> Host {target}",
                                    f"Started sending from Host "
                                    f"{host_name} to Host {target}",
                                    "Information")
                # Sending process / Threading
                # If a Host is already sending, dont start sending again
                # If we can start sending, create a Thread that handles the sending, along with timings
                # If next_hop is None, refresh dropped packets and log
                self.__show_and_log(f"Host {host_name} <-> Host {target}",
                                    f"Stopped sending from Host "
                                    f"{host_name} to Host {target}",
                                    "Information")
                # Return, because we found our Host, and we are done
                return

    def __handle_connect_submit(self) -> None:
        """
        Handles the connect to Node Frame's submit Button event
        """
        # TODO check how sending is affected
        # Get the coordinates where the Menu was opened before the Frame
        # This is needed to avoid having to use the event.x and event.y
        # coordinates
        x: int = self.object_canvas_handler.menu_x
        y: int = self.object_canvas_handler.menu_y

        # Check what intersects with the mouse (or the Menu in this case)
        intersection_details: Tuple[str, int] = self.object_canvas_handler.intersects(
            x, y, 1, 1)

        # Get the user input from the Frame's Entries
        success: bool = self.object_canvas_handler.submit_input()
        user_input: List[str] = self.object_canvas_handler.input_data

        # If the regex failed, do nothing
        if not success:
            return

        # Setup the variables for the Node that the method was called on
        to_connect: Node = None
        to_connect_coords: Tuple[int, int] = None

        # Setup the variables for the other Node, and get the actual Node
        # To avoid race conditions on the Network object
        with self.network_lock:
            # Fetch the Node
            other_node: Node = self.network.get_host(user_input[0]) or \
                self.network.get_router(user_input[0])
        other_node_coords: Tuple[int, int] = None

        # Get the Nodes, combining Hosts and Routers
        nodes: List[Tuple[int, str]] = self.hosts + self.routers

        # Get the first Node and its coordinates
        for node in nodes:
            # If the item_id matches
            if node[0] == intersection_details[1]:
                # To avoid race conditions on the Network object
                with self.network_lock:
                    # Fetch the Node
                    to_connect = self.network.get_host(node[1]) or \
                        self.network.get_router(node[1])
                to_connect_coords = self.object_canvas_handler.get_node_coords(
                    node[0])
                break

        # If the second Node is not present in the Network, show a message
        # and log accordingly, and then return
        if other_node is None:
            # Get the name or the IP of the Node
            node_2_name_or_ip: str = user_input[0]

            self.__show_and_log(f"Node {to_connect.name} - {to_connect.ip}"
                                f" <-> Node {node_2_name_or_ip}",
                                f"Failed to connect {to_connect.name} - "
                                f"{to_connect.ip} to {node_2_name_or_ip}: no "
                                "such Node.",
                                "Information")

            return

        # Get the second Node's coordinates
        for node in nodes:
            # If the item_id matches
            if node[1] == other_node.name:
                other_node_coords = self.object_canvas_handler.get_node_coords(
                    node[0])
                break

        # Connect the Nodes using the given input
        interface_1_name: str = user_input[1]
        interface_2_name: str = user_input[2]

        # To avoid race conditions on the Network object
        with self.network_lock:
            # Try connecting the Interfaces
            connect_success: bool = self.network.connect_node_interfaces(
                to_connect.name, user_input[0], interface_1_name,
                interface_2_name, user_input[3], user_input[4])

            # If connecting was successful, we can update the statistics
            if connect_success:
                self.__update_statistics()

        # If connecting succeded
        if connect_success:
            # Delete the Link that was connected to either of the Interfaces
            for link in self.links:
                if (to_connect.name == link[1] and interface_1_name == link[2]) \
                        or (to_connect.name == link[3] and interface_1_name == link[4]) \
                        or (other_node.name == link[1] and interface_2_name == link[2]) \
                        or (other_node.name == link[3] and interface_2_name == link[4]):
                    self.links.remove(link)
                    self.object_canvas_handler.delete_link(link[0])
                    break

            # Draw the Link
            item_id: int = self.object_canvas_handler.draw(
                "LINK", to_connect_coords[0], to_connect_coords[1],
                other_node_coords[0], other_node_coords[1])

            # Add the new Link
            self.links.append((item_id, to_connect.name, interface_1_name,
                               other_node.name, interface_2_name))

            # Show a message and log accordingly
            self.__show_and_log(f"Node {to_connect.name} - {to_connect.ip} - "
                                f"{interface_1_name} <-> Node "
                                f"{other_node.name} - {other_node.ip} - "
                                f"{interface_2_name}",
                                f"Successfully connected {to_connect.name} - "
                                f"{to_connect.ip} - {interface_1_name} to "
                                f"{other_node.name} - {other_node.ip} - "
                                f"{interface_2_name}.",
                                "Information")
        # If it failed to connect
        else:
            # If the two Nodes are identical, show a message and log accordingly
            if to_connect == other_node:
                self.__show_and_log(f"Node {to_connect.name} - {to_connect.ip}"
                                    f" <-> Node {other_node.name} - "
                                    f"{other_node.ip}",
                                    f"Failed to connect {to_connect.name} - "
                                    f"{to_connect.ip} to {other_node.name} - "
                                    f"{other_node.ip}: can't connect to self.",
                                    "Information")
            # This occurs when there is an issue with the given Interfaces,
            # meaning that either of them does not exist on the given Node
            else:
                self.__show_and_log(f"Node {to_connect.name} - {to_connect.ip}"
                                    f" - {interface_1_name} <-> Node "
                                    f"{other_node.name} - {other_node.ip} - "
                                    f"{interface_2_name}",
                                    f"Failed to connect {to_connect.name} - "
                                    f"{to_connect.ip} - {interface_1_name} to "
                                    f"{other_node.name} - {other_node.ip} - "
                                    f"{interface_2_name}: invalid Interface(s).",
                                    "Information")

    def __handle_disconnect_submit(self) -> None:
        """
        Handles the disconnect Interface Frame's submit Button event
        """
        # TODO check how sending is affected
        # Get the coordinates where the Menu was opened before the Frame
        # This is needed to avoid having to use the event.x and event.y
        # coordinates
        x: int = self.object_canvas_handler.menu_x
        y: int = self.object_canvas_handler.menu_y

        # Check what intersects with the mouse (or the Menu in this case)
        intersection_details: Tuple[str, int] = self.object_canvas_handler.intersects(
            x, y, 1, 1)

        # Get the user input from the Frame's Entries
        success: bool = self.object_canvas_handler.submit_input()
        user_input: List[str] = self.object_canvas_handler.input_data

        # If the regex failed, do nothing
        if not success:
            return

        # Logic based on whether the intersection happened on a Host or a
        # Router
        if intersection_details[0] == "HOST":
            for host in self.hosts:
                # If the item_id matches
                if host[0] == intersection_details[1]:
                    host_name: str = host[1]
                    interface_name: str = user_input[0]

                    # To avoid race conditions on the Network object
                    with self.network_lock:
                        # Try disconnecting the given Interface
                        network_success: bool = \
                        self.network.disconnect_node_interface(host_name, 
                                                               interface_name)

                        # If disconnecting was successful, we can update the
                        # statistics
                        if network_success:
                            self.__update_statistics()

                    # If the disconnecting succeeded
                    if network_success:
                        # Delete the Link that was connected to the disconnected
                        # Interface - if there was any
                        for link in self.links:
                            if (link[1] == host_name and
                                link[2] == interface_name) or \
                               (link[3] == host_name and
                                    link[4] == interface_name):
                                self.object_canvas_handler.delete_link(link[0])
                                self.links.remove(link)
                                break

                        # Show a message and log accordingly
                        self.__show_and_log(f"Host {host_name} - Interface "
                                            f"{interface_name}",
                                            f"Successfully disconnected "
                                            f"Interface {interface_name} on "
                                            f"Host {host_name}.",
                                            "Information")
                    # If it failed, show a message and log accordingly
                    else:
                        self.__show_and_log(f"Host {host_name} - Interface "
                                            f"{interface_name}",
                                            f"Failed to disconnect Interface "
                                            f"{interface_name} on Host "
                                            f"{host_name}: no such Interface.",
                                            "Information")
        else:
            for router in self.routers:
                # If the item_id matches
                if router[0] == intersection_details[1]:
                    router_name: str = router[1]
                    interface_name: str = user_input[0]

                    # To avoid race conditions on the Network object
                    with self.network_lock:
                        # Try disconnecting the given Interface
                        network_success: bool = \
                            self.network.disconnect_node_interface(router_name,
                                                                   interface_name)

                        # If disconnecting was successful, we can update the
                        # statistics
                        if network_success:
                            self.__update_statistics()

                    # If the disconnecting succeeded
                    if network_success:
                        # Delete the Link that was connected to the disconnected
                        # Interface - if there was any
                        for link in self.links:
                            if (link[1] == router_name and
                                link[2] == interface_name) or \
                               (link[3] == router_name and
                                    link[4] == interface_name):
                                self.object_canvas_handler.delete_link(link[0])
                                self.links.remove(link)
                                break

                        # Show a message and log accordingly
                        self.__show_and_log(f"Router {router_name} - Interface "
                                            f" {interface_name}",
                                            f"Successfully disconnected "
                                            f"Interface {interface_name} on "
                                            f"Router {router_name}.",
                                            "Information")
                    # If it failed, show a message and log accordingly
                    else:
                        self.__show_and_log(f"Router {router_name} - Interface"
                                            f" {interface_name}",
                                            f"Failed to disconnect Interface"
                                            f" {interface_name} on Router "
                                            f"{router_name}: no such Interface.",
                                            "Information")

    def __get_handlers(self, menu_type: str) -> List[Callable]:
        """
        Gets the corresponding submit event handlers for the given pop-up Menu

        Parameters:
        menu_type (str): The type of the pop-up Menu, can be "NETWORK", "HOST" \
                  and "ROUTER"

        Returns:
        List[Callable]: The event handlers for the submit buttons
        """
        # Get the submit Button handlers for every single pop-up Menu type
        if menu_type.upper() == "NETWORK":
            return [self.__handle_component_add_submit,
                    self.__handle_component_add_submit]
        elif menu_type.upper() == "HOST":
            return [self.__handle_interface_add_submit,
                    self.__handle_interface_delete_submit,
                    self.__handle_set_application_submit,
                    self.__handle_send_submit,
                    self.__handle_connect_submit,
                    self.__handle_disconnect_submit]
        else:
            return [self.__handle_interface_add_submit,
                    self.__handle_interface_delete_submit,
                    self.__handle_connect_submit,
                    self.__handle_disconnect_submit]

    def __get_menu_frames(self, menu_type: str) -> List[str]:
        """
        Gets the corresponding Frame types for the given pop-up Menu

        Parameters:
        menu_type (str): The type of the pop-up Menu, can be "NETWORK", "HOST" \
                  and "ROUTER"

        Returns:
        List[str]: The Frame types for the given menu_type
        """
        # Get the Frame types for every single pop-up Menu type
        if menu_type.upper() == "ROUTER":
            return ["ADDINTERFACE", "DELETEINTERFACE",
                    "CONNECT", "DISCONNECT"]
        elif menu_type.upper() == "HOST":
            return ["ADDINTERFACE", "DELETEINTERFACE",
                    "SETAPPLICATION", "SEND", "CONNECT", "DISCONNECT"]
        else:
            return ["PLACEHOST", "PLACEROUTER"]

    def __handle_deletion_option(self) -> None:
        """
        The event handler for when the "delete component" Entry is pressed in \
        the pop-up Menu
        """
        # Get the coordinates where the Menu was opened before the Frame
        # This is needed to avoid having to use the event.x and event.y
        # coordinates
        x: int = self.object_canvas_handler.menu_x
        y: int = self.object_canvas_handler.menu_y

        # Check what intersects with the mouse (or the Menu in this case)
        intersection_details: Tuple[str, int] = self.object_canvas_handler.intersects(
            x, y, 1, 1)

        # Try deleting the component from the Canvas
        handler_success: bool = self.object_canvas_handler.delete_component(
            intersection_details[0], intersection_details[1])
        network_success: bool = False

        # Logic based on whether the intersection happened on a Host or a
        # Router
        if intersection_details[0] == "HOST":
            for host in self.hosts:
                # If the item_id matches
                if intersection_details[1] == host[0]:
                    host_name: str = host[1]

                    idx: int = self.hosts.index(host)

                    # To avoid race conditions on the host_sending variable
                    with self.sending_lock:
                        del self.host_sending[idx]

                    # To avoid race conditions on the Network object
                    with self.network_lock:
                        # Try deleting the Host
                        network_success = self.network.delete_host(host_name)

                        # If deletion was successful, we can update the statistics
                        if network_success:
                            self.__update_statistics()

                    # Create a List for the Links to remove
                    # This is needed because removing while iterating
                    # invalidates the iterator on the List
                    links_to_remove: List[int, str, str, str, str] = []

                    # Delete the Link from the Canvas
                    for link in self.links:
                        if host_name == link[1] or host_name == link[3]:
                            links_to_remove.append(link)
                            self.object_canvas_handler.delete_link(link[0])

                    # And also delete the Link from the storage used to connect
                    # together the network and handler / GUI components
                    for link in links_to_remove:
                        self.links.remove(link)

                    # If both succeeded, remove the Host, and show a message and
                    # log accordingly
                    if handler_success and network_success:
                        self.hosts.remove(host)
                        self.__show_and_log(f"Host {host_name}",
                                            f"Successfully deleted Host"
                                            f" {host_name}.",
                                            "Information")
                    # This can only happen if an error occurs
                    else:
                        self.__show_and_log(f"Host {host_name}",
                                            f"Failed to delete Host "
                                            f"{host_name}.",
                                            "Error")
                    # Return, because we found our Host
                    return
        elif intersection_details[0] == "ROUTER":
            for router in self.routers:
                # If the item_id matches
                if intersection_details[1] == router[0]:
                    router_name: str = router[1]

                    # To avoid race conditions on the Network object
                    with self.network_lock:
                        # Try deleting the Router
                        network_success = self.network.delete_router(router_name)

                        # If deletion was successful, we can update the statistics
                        if network_success:
                            self.__update_statistics()

                    # Create a List for the Links to remove
                    # This is needed because removing while iterating
                    # invalidates the iterator on the List
                    links_to_remove: List[int, str, str, str, str] = []

                    # Delete the Link from the Canvas
                    for link in self.links:
                        if router_name == link[1] or router_name == link[3]:
                            links_to_remove.append(link)
                            self.object_canvas_handler.delete_link(link[0])

                    # And also delete the Link from the storage used to connect
                    # together the network and handler / GUI components
                    for link in links_to_remove:
                        self.links.remove(link)

                    # If both succeeded, remove the Router, and show a message
                    # and log accordingly
                    if handler_success and network_success:
                        self.routers.remove(router)
                        self.__show_and_log(f"Router {router_name}",
                                            f"Successfully deleted Router "
                                            f"{router_name}.",
                                            "Information")
                    # This can only happen if an error occurs
                    else:
                        self.__show_and_log(f"Router {router_name}",
                                            f"Failed to delete Router "
                                            f"{router_name}.",
                                            "Error")
                    # Return, because we found our Router
                    return

    def __setup_cancel_button(self) -> None:
        """
        The event handler for when the "Cancel" Button is pressed in any of the \
        available Frames
        """
        self.object_canvas_handler.bind_to_cancel_button()

    def __setup_config_frames(self) -> None:
        """
        The event handler for when the "Cancel" Button is pressed in any of the \
        available Frames
        """
        # Get the specific handlers and Frames for the Network pop-up Menu
        network_frames: List[str] = self.__get_menu_frames("NETWORK")
        network_handlers: List[Callable] = self.__get_handlers("NETWORK")

        # Get the specific handlers and Frames for the Host pop-up Menu
        host_frames: List[str] = self.__get_menu_frames("HOST")
        host_handlers: List[Callable] = self.__get_handlers("HOST")

        # Get the specific handlers and Frames for the Router pop-up Menu
        router_frames: List[str] = self.__get_menu_frames("ROUTER")
        router_handlers: List[Callable] = self.__get_handlers("ROUTER")

        # Apply these to the entries, setting up what Frames to show, and what
        # behaviour has to be done when the submit Button is pressed
        self.object_canvas_handler.bind_to_options_menu_entries(
            (network_frames, network_handlers), (host_frames, host_handlers),
            (router_frames, router_handlers), self.__handle_deletion_option)

        # Also setup the cancel Button for every Frame - shares behaviour in
        # every Frame
        self.__setup_cancel_button()

    def __handle_is_placing_motion(self, event: str) -> None:
        """
        Event handler for placing motion, which only does anything, if \
        is_placing is equal to True

        Parameters:
        event (str): The event occuring, providing mouse coordinates
        """
        # If we are currently placing
        if self.object_canvas_handler.is_placing():
            # Draw the component, but don't save it for redraws
            item_id: int = self.object_canvas_handler.draw(
                self.object_canvas_handler.input_data[0],
                event.x, event.y, save=False)
            # If there was no intersection, save the coordinates, so that when
            # there is an actual intersection, we can use these coordinates
            if item_id != -1:
                self.object_canvas_handler.set_last_saved_pos(event.x, event.y)

    def __change_text(self, curr_showing: str, text: str) -> None:
        """
        Changes the text in the right-hand side Frame, the ObjectFrame

        Parameters:
        curr_showing (str): The currently shown component's type
        text         (str): The text to display, shown together with curr_showing
        """
        self.object_frame_handler.display_text(curr_showing, text)

    def __handle_show_details_left_click(self, event: str) -> None:
        """
        Event handler that shows the details of a component in the ObjectFrame

        Parameters:
        event (str): The event occuring, providing mouse coordinates
        """
        # Check what intersects with the mouse
        intersection_details: Tuple[str, int] = self.object_canvas_handler.intersects(
            event.x, event.y, 1, 1)

        # Logic based on whether the intersection happened on a Host, Router or
        # there was no intersection
        if intersection_details[0] == "HOST":
            for host in self.hosts:
                # If the item_id matches
                if intersection_details[1] == host[0]:

                    # To avoid race conditions on the Network object
                    with self.network_lock:
                        # Fetch the Host
                        item: Host = self.network.get_host(host[1])

                    # Show its attributes in the left-hand side Frame
                    self.__change_text(
                        "Host Details:\n", item.__str__())
        elif intersection_details[0] == "ROUTER":
            for router in self.routers:
                # If the item_id matches
                if intersection_details[1] == router[0]:

                    # To avoid race conditions on the Network object
                    with self.network_lock:
                        # Fetch the Router
                        item: Router = self.network.get_router(router[1])

                    # Show its attributes in the left-hand side Frame
                    self.__change_text(
                        "Router Details:\n", item.__str__())
        else:
            # If nothing intersected, show the starting text
            self.__change_text("", self.object_frame_handler.start_display)

    def __handle_is_placing_left_click(self, event: str) -> None:
        """
        Event handler that handles the permanent placing of a component

        Parameters:
        event (str): The event occuring
        """
        # If we are currently placing
        if self.object_canvas_handler.is_placing():
            # Fetch the data previously set from the Entries in the placing
            # Frame
            user_input: List[str] = self.object_canvas_handler.input_data

            # If there wasn't any set, return
            if len(user_input) == 0:
                return

            # created will be used to check if creating was successful or not
            # last_x and last_y is needed because event.x and event.y does
            # not provide the neccessary logic when trying to place
            created: bool = False
            last_x: int = self.object_canvas_handler.last_saved_x
            last_y: int = self.object_canvas_handler.last_saved_y

            # Logic based on whether the component we are placing is a Host or a
            # Router
            if user_input[0] == "COMPONENT/HOST":
                host_name: str = user_input[1]
                host_ip: str = user_input[2]

                # To avoid race conditions on the Network object
                with self.network_lock:
                    # Try creating the Host
                    created = self.network.create_host(
                        host_name, host_ip, int(user_input[3]))

                # If it succeeded
                if created:
                    # To avoid race conditions on the host_sending object
                    with self.sending_lock:
                        self.host_sending.append(False)

                    # Draw the component and save it for future redraws
                    item_id: int = self.object_canvas_handler.draw(
                        user_input[0], last_x, last_y)
                    self.hosts.append((item_id, host_name))

                    # Show a message and log accordingly
                    self.__show_and_log(f"Host {host_name} - {host_ip}",
                                        f"Successfully created Host "
                                        f"{host_name} - {host_ip}.",
                                        "Information")
                # If it was a duplicate name or IP, show a message and log
                # accordingly
                else:
                    self.__show_and_log(f"Host {host_name} - {host_ip}",
                                        f"Failed to create Host "
                                        f"{host_name} - {host_ip}: "
                                        "duplicate Node IP or Name.",
                                        "Information")
            else:
                router_name: str = user_input[1]
                router_ip: str = user_input[2]

                # To avoid race conditions on the Network object
                with self.network_lock:
                    # Try creating the Router
                    created = self.network.create_router(
                        router_name, router_ip,
                        int(user_input[3]), int(user_input[4]))

                # If it succeeded
                if created:
                    # Draw the component and save it for future redraws
                    item_id: int = self.object_canvas_handler.draw(
                        user_input[0], last_x, last_y)
                    self.routers.append((item_id, router_name))

                    # Show a message and log accordingly
                    self.__show_and_log(f"Router {router_name} - {router_ip}",
                                        f"Successfully created Router "
                                        f"{router_name} - {router_ip}.",
                                        "Information")
                # If it was a duplicate name or IP, show a message and log
                # accordingly
                else:
                    self.__show_and_log(f"Router {router_name} - {router_ip}",
                                        f"Failed to create Router "
                                        f"{router_name} - {router_ip}: "
                                        "duplicate Node IP or Name.",
                                        "Information")

            # Set the placing to False, indicating, that we are finished
            self.object_canvas_handler.placing = False

    def __bind_to_object_canvas_handler(self) -> None:
        """
        Binds event handlers to the ObjectCanvas, providing the needed \
        functionality for the simulation
        """
        # Bind to the right-click event of the Canvas, adding the option to
        # show pop-up Menus
        self.object_canvas_handler.bind("<Button-3>", self.__show_options_menu)

        # Configure the Entries of above mentioned Menus
        self.__setup_config_frames()

        # Add drawing the component to the Motion event if we are placing
        self.object_canvas_handler.bind(
            "<Motion>", self.__handle_is_placing_motion)

        # Add getting the details of a component to the left-click event
        self.object_canvas_handler.bind(
            "<Button-1>", self.__handle_show_details_left_click)

        # Add placing a component to the left-click event
        self.object_canvas_handler.bind(
            "<Button-1>", self.__handle_is_placing_left_click)
