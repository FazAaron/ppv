"""
This module makes MainHandler objects available for use when imported
"""
# Built-in modules
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
    main_window              (MainWindow): The main window of the GUI, containing everything
    network                  (Network): The main object of the components, containing everything
    object_canvas_handler    (ObjectCanvasHandler): The object canvas handling object
    object_frame_handler     (ObjectFrameHandler): The object frame handling object
    statistics_frame_handler (StatisticsFrameHandler): The statistics frame handling object
    logger                   (Logger): The logger object, logging neccessary actions
    hosts                    (List[Tuple[int, str]]): Host information stored
    routers                  (List[Tuple[int, str]]): Router information stored
    links                    (List[Tuple[int, str, str]]): Link information stored
    """

    def __init__(self, main_window: MainWindow, network: Network) -> None:
        self.main_window: MainWindow = main_window
        self.network: Network = network

        content: WidgetContainer = self.main_window.content
        self.object_canvas_handler: ObjectCanvasHandler = ObjectCanvasHandler(
            content.object_canvas)
        self.object_frame_handler: ObjectFrameHandler = ObjectFrameHandler(
            content.object_frame)
        self.statistics_frame_handler: StatisticsFrameHandler = StatisticsFrameHandler(
            content.statistics_frame)

        self.logger = Logger("conf/logger_config.json")

        self.hosts: List[Tuple[int, str]] = []
        self.routers: List[Tuple[int, str]] = []
        self.links: List[Tuple[int, str, str, str, str]] = []

        # Setup the bindings to the Handlers
        self.__bind_to_object_frame_handler()
        self.__bind_to_object_canvas_handler()

    def __exit_prompt(self) -> None:
        """
        Opens a pop-up prompt asking a yes/no question for the user, whether \
        they want to exit or not
        """
        answer: bool = messagebox.askyesno(title="Exit application",
                                           message="Are you sure you want to exit the application?")
        if answer:
            self.main_window.exit()

    def __bind_to_object_frame_handler(self) -> None:
        """
        Bind events to the ObjectFrame's Button Widget, prompting a yes/no
        question when clicked
        """
        self.object_frame_handler.bind_to_exit(self.__exit_prompt)

    def __set_mouse_pos(self, event: str) -> None:
        self.object_canvas_handler.mouse_pos_x = event.x
        self.object_canvas_handler.mouse_pos_y = event.y

    def __show_options_menu(self, event: str) -> None:
        self.object_canvas_handler.show_menu()

    def __show_and_log(self, comp: str, message: str, severity: str) -> None:
        self.object_canvas_handler.show_message(message, 2000)
        while not self.logger.write(comp, message, severity):
            pass

    def __handle_component_add_submit(self) -> None:
        self.object_canvas_handler.submit_input()

    def __handle_interface_add_submit(self) -> None:
        x: int = self.object_canvas_handler.menu_x
        y: int = self.object_canvas_handler.menu_y
        intersection_details: Tuple[str, int] = self.object_canvas_handler.intersects(
            x, y, 1, 1)
        self.object_canvas_handler.submit_input()
        user_input: List[str] = self.object_canvas_handler.input_data
        if len(user_input) == 0:
            return
        if intersection_details[0] == "HOST":
            for host in self.hosts:
                if host[0] == intersection_details[1]:
                    created = self.network.add_interface(
                        host[1], user_input[0])
                    host_name = host[1]
                    interface_name = user_input[0]
                    if created:
                        self.__show_and_log(f"Host {host_name} - Interface {interface_name}",
                                            f"Successfully created Interface {interface_name} on Host {host_name}.", "Information")
                    else:
                        self.__show_and_log(f"Host {host_name} - Interface {interface_name}",
                                            f"Failed to create Interface {interface_name} on Host {host_name}: duplicate Interface name on Host.", "Information")
        elif intersection_details[0] == "ROUTER":
            for router in self.routers:
                if router[0] == intersection_details[1]:
                    created = self.network.add_interface(
                        router[1], user_input[0])
                    router_name = router[1]
                    interface_name = user_input[0]
                    if created:
                        self.__show_and_log(f"Router {router_name} - Interface {interface_name}",
                                            f"Successfully created Interface {interface_name} on Router {router_name}", "Information")
                    else:
                        self.__show_and_log(f"Router {router_name} - Interface {interface_name}",
                                            f"Failed to create Interface {interface_name} on Router {router_name}: duplicate Interface name on Router.", "Information")

    def __handle_interface_delete_submit(self) -> None:
        # TODO: check if any packets were lost / what happens with connections, application, sending, etc
        x: int = self.object_canvas_handler.menu_x
        y: int = self.object_canvas_handler.menu_y
        details = self.object_canvas_handler.intersects(x, y, 1, 1)
        self.object_canvas_handler.submit_input()
        user_input: List[str] = self.object_canvas_handler.input_data
        if len(user_input) == 0:
            return
        if details[0] == "HOST":
            for host in self.hosts:
                if host[0] == details[1]:
                    deleted = self.network.delete_interface(
                        host[1], user_input[0])
                    host_name = host[1]
                    interface_name = user_input[0]
                    for link in self.links:
                        if (host_name == link[1] and interface_name == link[2]) or (host_name == link[3] and interface_name == link[4]):
                            self.links.remove(link)
                            self.object_canvas_handler.delete_link(
                                link[0])
                            break
                    if deleted:
                        self.object_canvas_handler.show_message(
                            f"Successfully deleted Interface {interface_name} on Host {host_name}.", 2000)
                        while not self.logger.write(f"Host {host_name} -> Interface {interface_name}", "Successful deletion", "Information"):
                            pass
                    else:
                        self.object_canvas_handler.show_message(
                            f"Failed to delete Interface {interface_name} on {host_name}: no such Interface on Host.", 2000)
                        while not self.logger.write(f"Host {host_name} -> Interface {interface_name}", "Failed deletion: no such Interface on Host", "Information"):
                            pass
        elif details[0] == "ROUTER":
            for router in self.routers:
                if router[0] == details[1]:
                    deleted = self.network.delete_interface(
                        router[1], user_input[0])
                    router_name = router[1]
                    interface_name = user_input[0]
                    for link in self.links:
                        if (router_name == link[1] and interface_name == link[2]) or (router_name == link[3] and interface_name == link[4]):
                            self.links.remove(link)
                            self.object_canvas_handler.delete_link(
                                link[0])
                            break
                    if deleted:
                        self.object_canvas_handler.show_message(
                            f"Successfully deleted Interface {interface_name} on Router {router_name}.", 2000)
                        while not self.logger.write(f"Router {router_name} -> Interface {interface_name}", "Successful deletion", "Information"):
                            pass
                    else:
                        self.object_canvas_handler.show_message(
                            f"Failed to delete Interface {interface_name} on {router_name}: no such Interface on Router.", 2000)
                        while not self.logger.write(f"Router {router_name} -> Interface {interface_name}", "Failed creation: no such Interface on Router", "Information"):
                            pass

    def __handle_set_application_submit(self) -> None:
        # TODO: keep sending if it was sending or just stop?
        x: int = self.object_canvas_handler.menu_x
        y: int = self.object_canvas_handler.menu_y
        details = self.object_canvas_handler.intersects(x, y, 1, 1)
        self.object_canvas_handler.submit_input()
        user_input: List[str] = self.object_canvas_handler.input_data
        if len(user_input) == 0:
            return
        for host in self.hosts:
            if host[0] == details[1]:
                applied = self.network.set_application(
                    host[1], user_input[0], user_input[1], user_input[2], user_input[3])
                if applied:
                    self.object_canvas_handler.show_message(
                        f"Successfully set Application {user_input[0]} on Host {host[1]}.", 2000)
                    while not self.logger.write(f"Host {host[1]} -> Application {user_input[0]}", "Set successfully", "Information"):
                        pass
                else:
                    # This can't happen by default, only if there is a logical error in the code
                    self.object_canvas_handler.show_message(
                        f"Failed to set Application {user_input[0]} on Host {host[1]}.", 2000)
                    while not self.logger.write(f"Host {host[1]} -> Application {user_input[0]}", "Failed to set", "Error"):
                        pass

    def __handle_send_submit(self) -> None:
        print("Sending")
        self.object_canvas_handler.submit_input()
        print(self.object_canvas_handler.input_data)

    def __handle_connect_submit(self) -> None:
        # TODO check packets dropped / how sending is affected, etc. when connecting (since this disconnects then connects the links)
        details: Tuple[str, int] = self.object_canvas_handler.intersects(
            self.object_canvas_handler.menu_x, self.object_canvas_handler.menu_y, 1, 1)
        self.object_canvas_handler.submit_input()
        user_input: List[str] = self.object_canvas_handler.input_data
        if len(user_input) == 0:
            return
        node_1: Node = None  # The Node to connect
        node_1_coords: Tuple[int, int] = None
        node_2: Node = self.network.get_host(user_input[0]) or self.network.get_router(
            user_input[0])  # The Node to connect to
        node_2_coords: Tuple[int, int] = None
        nodes: List[Tuple[int, str]] = self.hosts + self.routers
        for node in nodes:
            if node[0] == details[1]:
                node_1 = self.network.get_host(
                    node[1]) or self.network.get_router(node[1])
                node_1_coords = self.object_canvas_handler.get_node_coords(
                    node[0])
                break
        if node_2 is None:
            self.object_canvas_handler.show_message(
                f"Failed to connect {node_1.name} - {node_1.ip} to {user_input[0]}: no such Node.", 2000)
            self.logger.write(f"Node {node_1.name} - {node_1.ip} <-> Node {user_input[0]}",
                              "Failed to connect: no such Node", "Information")
            return
        for node in nodes:
            if node[1] == node_2.name:
                node_2_coords = self.object_canvas_handler.get_node_coords(
                    node[0])
                break
        connect_success: bool = self.network.connect_node_interfaces(
            node_1.name, user_input[0], user_input[1], user_input[2], user_input[3], user_input[4])
        link_success: bool = True
        if connect_success:
            for link in self.links:
                if (node_1.name == link[1] and user_input[1] == link[2]) or (node_1.name == link[3] and user_input[1] == link[4]) or \
                        (node_2.name == link[1] and user_input[2] == link[2]) or (node_2.name == link[3] and user_input[2] == link[4]):
                    self.links.remove(link)
                    link_success = self.object_canvas_handler.delete_link(
                        link[0])
                    break
            if link_success:
                coords: Tuple[int, int, int, int] = self.object_canvas_handler.get_link_endpoints(
                    node_1_coords[0], node_1_coords[1], node_2_coords[0], node_2_coords[1])
                item_id: int = self.object_canvas_handler.draw(
                    "LINK", coords[0], coords[1], coords[2], coords[3])
                self.links.append(
                    (item_id, node_1.name, user_input[1], node_2.name, user_input[2]))
                self.object_canvas_handler.show_message(
                    f"Successfully connected {node_1.name} - {node_1.ip} - {user_input[1]} to {node_2.name} - {node_2.ip} - {user_input[2]}.", 2000)
                self.logger.write(
                    f"Node {node_1.name} - {node_1.ip} - {user_input[1]} <-> Node {node_2.name} - {node_2.ip} - {user_input[2]}", "Successfully connected", "Information")
        else:
            if node_1 == node_2:
                self.object_canvas_handler.show_message(
                    f"Failed to connect {node_1.name} - {node_1.ip} to {node_2.name} - {node_2.ip}: can't connect to self.", 2000)
                self.logger.write(f"Node {node_1.name} - {node_1.ip} <-> Node {node_2.name} - {node_2.ip}",
                                  "Failed to connect: can't connect to self", "Information")
            else:
                self.object_canvas_handler.show_message(
                    f"Failed to connect {node_1.name} - {node_1.ip} - {user_input[1]} to {node_2.name} - {node_2.ip} - {user_input[2]}: invalid Interface.", 2000)
                self.logger.write(
                    f"Node {node_1.name} - {node_1.ip} - {user_input[1]} <-> Node {node_2.name} - {node_2.ip} - {user_input[2]}", "Failed to connect: invalid Interface", "Information")

    def __handle_disconnect_submit(self) -> None:
        # TODO check packets dropped / how sending is affected, etc.
        details: Tuple[str, int] = self.object_canvas_handler.intersects(
            self.object_canvas_handler.menu_x, self.object_canvas_handler.menu_y, 1, 1)
        self.object_canvas_handler.submit_input()
        user_input: List[str] = self.object_canvas_handler.input_data
        if len(user_input) == 0:
            return
        if details[0] == "HOST":
            for host in self.hosts:
                if host[0] == details[1]:
                    network_success: bool = self.network.disconnect_node_interface(
                        host[1], user_input[0])
                    link_success: bool = False
                    if network_success:
                        for link in self.links:
                            if (link[1] == host[1] and link[2] == user_input[0]) or \
                                    (link[3] == host[1] and link[4] == user_input[0]):
                                link_success = self.object_canvas_handler.delete_link(
                                    link[0])
                                if link_success:
                                    self.links.remove(link)
                                    self.object_canvas_handler.show_message(
                                        f"Successfully disconnected Interface {user_input[0]}.", 2000)
                                    self.logger.write(
                                        f"Host {host[1]} - Interface {user_input[0]}", "Successfully disconnected", "Information")
                                else:
                                    self.object_canvas_handler.show_message(
                                        f"Failed to disconnect Interface {user_input[0]}: no corresponding Link.", 2000)
                                    self.logger.write(
                                        f"Host {host[1]} - Interface {user_input[0]}", "Failed to disconnect: no corresponding Link", "Error")
                    else:
                        self.object_canvas_handler.show_message(
                            f"Failed to disconnect Interface {user_input[0]}: no such Interface on Host {host[1]}.", 2000)
                        self.logger.write(
                            f"Host {host[1]} - Interface {user_input[0]}", f"Failed to disconnect: no such Interface on Host {host[1]}", "Error")
        else:
            for router in self.routers:
                if router[0] == details[1]:
                    network_success: bool = self.network.disconnect_node_interface(
                        router[1], user_input[0])
                    link_success: bool = False
                    if network_success:
                        for link in self.links:
                            if (link[1] == router[1] and link[2] == user_input[0]) or \
                                    (link[3] == router[1] and link[4] == user_input[0]):
                                link_success = self.object_canvas_handler.delete_link(
                                    link[0])
                                if link_success:
                                    self.links.remove(link)
                                    self.object_canvas_handler.show_message(
                                        f"Successfully disconnected Interface {user_input[0]}.", 2000)
                                    self.logger.write(
                                        f"Router {router[1]} - Interface {user_input[0]}", "Successfully disconnected", "Information")
                                else:
                                    self.object_canvas_handler.show_message(
                                        f"Failed to disconnect Interface {user_input[0]}: no corresponding Link.", 2000)
                                    self.logger.write(
                                        f"Router {router[1]} - Interface {user_input[0]}", "Failed to disconnect: no corresponding Link", "Error")
                    else:
                        self.object_canvas_handler.show_message(
                            f"Failed to disconnect Interface {user_input[0]}: no such Interface on Router {router[1]}.", 2000)
                        self.logger.write(
                            f"Router {router[1]} - Interface {user_input[0]}", f"Failed to disconnect: no such Interface on Router {router[1]}", "Error")

    def __get_handlers(self, menu_type: str) -> List[Callable]:
        if menu_type.upper() == "NETWORK":
            return [self.__handle_component_add_submit, self.__handle_component_add_submit]
        elif menu_type.upper() == "HOST":
            return [self.__handle_interface_add_submit, self.__handle_interface_delete_submit,
                    self.__handle_set_application_submit, self.__handle_send_submit,
                    self.__handle_connect_submit, self.__handle_disconnect_submit]
        else:
            return [self.__handle_interface_add_submit, self.__handle_interface_delete_submit,
                    self.__handle_connect_submit, self.__handle_disconnect_submit]

    def __get_menu_frames(self, menu_type: str) -> List[str]:
        if menu_type.upper() == "ROUTER":
            return ["ADDINTERFACE", "DELETEINTERFACE", "CONNECT", "DISCONNECT"]
        elif menu_type.upper() == "HOST":
            return ["ADDINTERFACE", "DELETEINTERFACE", "SETAPPLICATION", "SEND", "CONNECT", "DISCONNECT"]
        else:
            return ["PLACEHOST", "PLACEROUTER"]

    def __handle_deletion_option(self) -> None:
        # TODO: check if any packets were lost / what happens with connections, application, sending, etc
        x: int = self.object_canvas_handler.menu_x
        y: int = self.object_canvas_handler.menu_y
        details: Tuple[str, int] = self.object_canvas_handler.intersects(
            x, y, 1, 1)
        handler_success: bool = self.object_canvas_handler.delete_component(
            details[0], details[1])
        network_success: bool = False
        link_success: bool = True
        if details[0] == "ROUTER":
            for router in self.routers:
                if details[1] == router[0]:
                    network_success = self.network.delete_router(router[1])
                    for link in self.links:
                        if router[1] == link[1] or router[1] == link[3]:
                            self.links.remove(link)
                            link_success = link_success and self.object_canvas_handler.delete_link(
                                link[0])
                    if handler_success and network_success and link_success:
                        self.routers.remove(router)
                        self.object_canvas_handler.show_message(
                            f"Successfully deleted Router {router[1]}.", 2000)
                        self.logger.write(
                            f"Router {router[1]}", "Successful deletion", "Information")
                    else:
                        self.object_canvas_handler.show_message(
                            f"Failed to delete Router {router[1]}.", 2000)
                        self.logger.write(
                            f"Router {router[1]}", "Failed deletion", "Error")
        elif details[0] == "HOST":
            for host in self.hosts:
                if details[1] == host[0]:
                    network_success = self.network.delete_host(host[1])
                    for link in self.links:
                        if host[1] == link[1] or host[1] == link[3]:
                            self.links.remove(link)
                            link_success = link_success and self.object_canvas_handler.delete_link(
                                link[0])
                    if handler_success and network_success and link_success:
                        self.hosts.remove(host)
                        self.object_canvas_handler.show_message(
                            f"Successfully deleted Host {host[1]}.", 2000)
                        self.logger.write(
                            f"Host {host[1]}", "Successful deletion", "Information")
                    else:
                        self.object_canvas_handler.show_message(
                            f"Failed to delete Host {host[1]}.", 2000)
                        self.logger.write(
                            f"Host {host[1]}", "Failed deletion", "Error")

    def __setup_cancel_button(self) -> None:
        self.object_canvas_handler.bind_to_cancel_button()

    def __setup_config_frames(self) -> None:
        network_frames: List[str] = self.__get_menu_frames("NETWORK")
        network_handlers: List[Callable] = self.__get_handlers("NETWORK")

        host_frames: List[str] = self.__get_menu_frames("HOST")
        host_handlers: List[Callable] = self.__get_handlers("HOST")

        router_frames: List[str] = self.__get_menu_frames("ROUTER")
        router_handlers: List[Callable] = self.__get_handlers("ROUTER")

        self.object_canvas_handler.bind_to_options_menu_entries(
            (network_frames, network_handlers), (host_frames, host_handlers), (router_frames, router_handlers), self.__handle_deletion_option)
        self.__setup_cancel_button()

    def __handle_is_placing_motion(self, event: str) -> None:
        if self.object_canvas_handler.is_placing():
            item_id: int = self.object_canvas_handler.draw(
                self.object_canvas_handler.input_data[0], event.x, event.y, save=False)
            if item_id != -1:
                self.object_canvas_handler.set_last_saved_pos(event.x, event.y)

    def __change_text(self, curr_showing: str, text: str) -> None:
        self.object_frame_handler.display_text(curr_showing, text)

    def __handle_show_details_left_click(self, event: str) -> None:
        details: Tuple[str, int] = self.object_canvas_handler.intersects(
            event.x, event.y, 1, 1)
        if details[1] > 0:
            if details[0] == "ROUTER":
                for router in self.routers:
                    if details[1] == router[0]:
                        item: Router = self.network.get_router(router[1])
                        self.__change_text(
                            "Router Details:\n", item.__str__())
            else:
                for host in self.hosts:
                    if details[1] == host[0]:
                        item: Host = self.network.get_host(host[1])
                        self.__change_text(
                            "Host Details:\n", item.__str__())
        else:
            self.__change_text("", self.object_frame_handler.start_display)

    def __handle_is_placing_left_click(self, event: str) -> None:
        if self.object_canvas_handler.is_placing():
            user_input: List[str] = self.object_canvas_handler.input_data
            if len(user_input) == 0:
                return
            created: bool = False
            last_x: int = self.object_canvas_handler.last_saved_x
            last_y: int = self.object_canvas_handler.last_saved_y
            if user_input[0] == "COMPONENT/HOST":
                created = self.network.create_host(
                    user_input[1], user_input[2], int(user_input[3]))
                if created:
                    item_id: int = self.object_canvas_handler.draw(
                        user_input[0], last_x, last_y)
                    self.hosts.append((item_id, user_input[1]))
                    self.object_canvas_handler.show_message(
                        "Successfully created the Host.", 2000)
                    while not self.logger.write(f"Host {user_input[1]} - {user_input[2]}", "Successful creation", "Information"):
                        pass
                else:
                    self.object_canvas_handler.show_message(
                        "Failed to create the Host: duplicate Node IP or Name.", 2000)
                    while not self.logger.write(f"Host {user_input[1]} - {user_input[2]}", "Failed creation: duplicate Node IP or Name", "Information"):
                        pass
            else:
                created = self.network.create_router(
                    user_input[1], user_input[2], int(user_input[3]), int(user_input[4]))
                if created:
                    item_id: int = self.object_canvas_handler.draw(
                        user_input[0], last_x, last_y)
                    self.routers.append((item_id, user_input[1]))
                    self.object_canvas_handler.show_message(
                        "Successfully created the Router.", 2000)
                    while not self.logger.write(f"Router {user_input[1]} - {user_input[2]}", "Successful creation", "Information"):
                        pass
                else:
                    self.object_canvas_handler.show_message(
                        "Failed to create the Router: duplicate Node IP or Name.", 2000)
                    while not self.logger.write(f"Router {user_input[1]} - {user_input[2]}", "Failed creation: duplicate Node IP or Name", "Information"):
                        pass
            self.object_canvas_handler.placing = False

    def __bind_to_object_canvas_handler(self) -> None:
        self.object_canvas_handler.bind("<Motion>", self.__set_mouse_pos)
        self.object_canvas_handler.bind("<Button-3>", self.__show_options_menu)
        self.__setup_config_frames()
        self.object_canvas_handler.bind(
            "<Motion>", self.__handle_is_placing_motion)
        self.object_canvas_handler.bind(
            "<Button-1>", self.__handle_show_details_left_click)
        self.object_canvas_handler.bind(
            "<Button-1>", self.__handle_is_placing_left_click)
