"""
This module makes MainHandler objects available for use when imported
"""
# Built-in modules
from tkinter import messagebox
from typing import List, Tuple

# Self-made modules
from src.components.network import Network
from src.event_handlers.object_canvas_handler import ObjectCanvasHandler
from src.event_handlers.object_frame_handler import ObjectFrameHandler
from src.event_handlers.statistics_frame_handler import StatisticsFrameHandler
from src.graphic_handlers.main_window import MainWindow
from src.graphic_handlers.widget_container import WidgetContainer
from src.utils.logger import Logger
from src.components.node import Host, Router


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
        self.interfaces: List[Tuple[int, str, str]] = []
        self.links: List[Tuple[int, str, str]] = []

        # Setup the bindings to the Handlers
        self.__bind_to_object_frame_handler()
        self.__bind_to_object_canvas_handler()

    # Bindings to Handlers
    # ObjectFrameHandler specific bindings
    def __bind_to_object_frame_handler(self) -> None:
        self.object_frame_handler.bind_to_exit(self.__exit_prompt)

    # ObjectCanvasHandler specific bindings
    def __bind_to_object_canvas_handler(self) -> None:
        self.object_canvas_handler.bind("<Motion>", self.__set_mouse_pos)
        self.object_canvas_handler.bind("<Button-3>", self.__show_options_menu)
        self.__setup_config_frames()
        self.__setup_config_buttons()
        self.object_canvas_handler.bind(
            "<Motion>", self.__handle_is_placing_motion)
        self.object_canvas_handler.bind(
            "<Button-1>", self.__handle_show_details_left_click)
        self.object_canvas_handler.bind(
            "<Button-1>", self.__handle_is_placing_left_click)
        #self.object_canvas_handler.bind("<Motion>", self.__placing_motion_handler)
        #self.object_canvas_handler.bind("<Button-1>", self.__placing_left_click_handdler)

    # Private methods
    # ObjectFrame handlers
    def __exit_prompt(self) -> None:
        """
        Opens a pop-up prompt asking a yes/no question for the user, whether \
        they want to exit or not
        """
        answer: bool = messagebox.askyesno(title="Exit application",
                                           message="Are you sure you want to exit the application?")
        if answer:
            self.main_window.exit()

    def __change_text(self, curr_showing: str, text: str) -> None:
        self.object_frame_handler.display_text(curr_showing, text)

    # ObjectCanvas handlers
    def __set_mouse_pos(self, event: str) -> None:
        self.object_canvas_handler.mouse_pos_x = event.x
        self.object_canvas_handler.mouse_pos_y = event.y

    # ----
    def __show_options_menu(self, event: str) -> None:
        self.object_canvas_handler.show_menu()

    # ----
    def __setup_config_frames(self) -> None:
        network: List[str] = self.object_canvas_handler.get_network_config_menu_frames()
        host: List[str] = self.object_canvas_handler.get_host_config_menu_frames()
        router: List[str] = self.object_canvas_handler.get_router_config_menu_frames()
        self.object_canvas_handler.bind_to_options_menu_entries(
            network, host, router, self.__handle_deletion_option)

    # ----
    def __setup_config_buttons(self) -> None:
        self.object_canvas_handler.bind_to_frame_buttons(
            self.object_canvas_handler.submit_input)

    # ----
    def __handle_is_placing_motion(self, event: str) -> None:
        if self.object_canvas_handler.is_placing():
            self.object_canvas_handler.draw(
                self.object_canvas_handler.placing_data[0], event.x, event.y, save=False)

    # ----
    def __handle_is_placing_left_click(self, event: str) -> None:
        if self.object_canvas_handler.is_placing():
            to_create: List[str] = self.object_canvas_handler.placing_data
            created: bool = False
            if to_create[0] == "COMPONENT/HOST":
                created = self.network.create_host(
                    to_create[1], to_create[2], int(to_create[3]))
                if created:
                    item_id: int = self.object_canvas_handler.draw(
                        self.object_canvas_handler.placing_data[0], event.x, event.y)
                    self.hosts.append((item_id, to_create[1]))
                    self.object_canvas_handler.show_message(
                        "Successfully created the Host.", 2000)
                    while not self.logger.write(f"Host {to_create[1]} - {to_create[2]}", "Successful creation", "Information"):
                        pass
                else:
                    self.object_canvas_handler.show_message(
                        "Failed to create the Host: duplicate Node IP or Name.")
                    while not self.logger.write(f"Host {to_create[1]} - {to_create[2]}", "Failed creation: duplicate Node IP or Name", "Information"):
                        pass
            else:
                created = self.network.create_router(
                    to_create[1], to_create[2], int(to_create[3]), int(to_create[4]))
                if created:
                    item_id: int = self.object_canvas_handler.draw(
                        self.object_canvas_handler.placing_data[0], event.x, event.y)
                    self.routers.append((item_id, to_create[1]))
                    self.object_canvas_handler.show_message(
                        "Successfully created the Router.", 2000)
                    while not self.logger.write(f"Router {to_create[1]} - {to_create[2]}", "Successful creation", "Information"):
                        pass
                else:
                    self.object_canvas_handler.show_message(
                        "Failed to create the Router: duplicate Node IP or Name.", 2000)
                    while not self.logger.write(f"Router {to_create[1]} - {to_create[2]}", "Failed creation: duplicate Node IP or Name", "Information"):
                        pass
            self.object_canvas_handler.placing_data = []
            self.object_canvas_handler.redraw()

    # ----
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
            elif details[0] == "HOST":
                for host in self.hosts:
                    if details[1] == host[0]:
                        item: Host = self.network.get_host(host[1])
                        self.__change_text(
                            "Host Details:\n", item.__str__())
            else:
                # INTERFACE DETAILS
                pass
        else:
            self.__change_text("", self.object_frame_handler.start_display)

    def __handle_deletion_option(self) -> None:
        x: int = self.object_canvas_handler.mouse_pos_x
        y: int = self.object_canvas_handler.mouse_pos_y
        details: Tuple[str, int] = self.object_canvas_handler.intersects(
            x, y, 1, 1)
        handler_success: bool = self.object_canvas_handler.delete_component(
            details[0], details[1])
        network_success: bool = False
        if details[0] == "ROUTER":
            for router in self.routers:
                if details[1] == router[0]:
                    network_success = self.network.delete_router(router[1])
                    self.routers.remove(router)
                    if handler_success and network_success:
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
                    self.hosts.remove(host)
                    if handler_success and network_success:
                        self.object_canvas_handler.show_message(
                            f"Successfully deleted Router {host[1]}.", 2000)
                        self.logger.write(
                            f"Host {host[1]}", "Successful deletion", "Information")
                    else:
                        self.object_canvas_handler.show_message(
                            f"Failed to delete Host {host[1]}.", 2000)
                        self.logger.write(
                            f"Host {host[1]}", "Failed deletion", "Error")

    # def __right_click_event(self, event) -> None:
        #self.object_canvas_handler.show_menu(event.x, event.y)
        ##self.object_canvas_handler.bind_to_options_menu_entries(lambda x=event.x, y=event.y: self.__place_host_frame(x, y))
        #self.object_canvas_handler.show_frame("PLACEHOST", event.x, event.y)
        #self.__place_host_frame(event.x, event.y)

    # def __place_host_frame(self, x: int, y: int) -> None:
       ##frame = self.object_canvas_handler.show_frame(x, y)
       # for widget in frame.winfo_children():
        # if widget == self.object_canvas_handler.object_canvas.cancel_button:
        # widget.configure(command=self.object_canvas_handler.object_canvas.hide_frame)
        # elif widget == self.object_canvas_handler.object_canvas.submit_button:
        # widget.configure(command=self.testing)
        # self.object_canvas_handler.bind_to_frame_buttons(self.object_canvas_handler.submit_input)

    # def testing(self) -> None:
        #new_object_details: List[str] = self.object_canvas_handler.fetch_entry_content()
        #self.object_canvas_handler.placing = "COMPONENT/ROUTER", True

    # def __placing_motion_handler(self, event) -> None:
        # if self.object_canvas_handler.is_placing:
        #comp_type: str = self.object_canvas_handler.placing[0]
        #self.object_canvas_handler.draw(comp_type, event.x, event.y, save=False)

    # def __placing_left_click_handdler(self, event) -> None:
        # if self.object_canvas_handler.is_placing:
        #comp_type: str = self.object_canvas_handler.placing[0]
        #self.object_canvas_handler.draw(comp_type, event.x, event.y)
        #self.object_canvas_handler.placing = ("", False)

    # def __object_details_left_click_handler(self, event) -> None:
        # pass

    # def __move_left_drag_handler(self, event) -> None:
        # pass
