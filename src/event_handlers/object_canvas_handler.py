"""
This module makes ObjectCanvasHandler objects available for use when imported
"""
# Built-in modules
from tkinter import Menu
from typing import Callable, List, Tuple

# Self-made modules
from src.graphic_handlers.object_canvas import ObjectCanvas
from src.utils.regex_checker import regex_matches


class ObjectCanvasHandler:
    """
    The class handling any access to the ObjectCanvas class, and also handling \
    specific actions using the methods binded to them by the MainHandler class

    Data members:
    object_canvas (ObjectCanvas): The Frame itself to access
    """

    def __init__(self, object_canvas: ObjectCanvas) -> None:
        self.object_canvas: ObjectCanvas = object_canvas
        self.input_data: List[str] = []
        self.placing: bool = False
        self.hosts: List[Tuple[int, int, int]] = []
        self.routers: List[Tuple[int, int, int]] = []
        #self.interfaces: List[Tuple[int, int, int]] = []
        self.links: List[Tuple[int, int, int, int, int]] = []
        self.shown_message: Tuple[int, int, str] = ()
        self.mouse_pos_x: int = 0
        self.mouse_pos_y: int = 0
        self.menu_x: int = 0
        self.menu_y: int = 0
        self.node_width: int = 60
        self.node_height: int = 60

    def bind(self, event: str, func: Callable) -> None:
        self.object_canvas.bind(event, func)

    def bind_to_options_menu_entries(self,
                                     network_conf_options: Tuple[List[str], List[Callable]],
                                     host_conf_options: Tuple[List[str], List[Callable]],
                                     router_conf_options: Tuple[List[str], List[Callable]],
                                     deletion_option: Callable
                                     ) -> None:
        for i in range(len(network_conf_options[0])):
            self.object_canvas.network_config_menu.entryconfigure(
                i, command=lambda i=i: self.show_frame(network_conf_options[0][i], network_conf_options[1][i]))

        for i in range(len(host_conf_options[0])):
            self.object_canvas.host_config_menu.entryconfigure(
                i, command=lambda i=i: self.show_frame(host_conf_options[0][i], host_conf_options[1][i]))
        last_index = len(host_conf_options[0])
        self.object_canvas.host_config_menu.entryconfigure(
            last_index, command=deletion_option)

        for i in range(len(router_conf_options[0])):
            self.object_canvas.router_config_menu.entryconfigure(
                i, command=lambda i=i: self.show_frame(router_conf_options[0][i], router_conf_options[1][i]))

        last_index = len(router_conf_options[0])
        self.object_canvas.router_config_menu.entryconfigure(
            last_index, command=deletion_option)

    def bind_to_submit_button(self, submit_command: Callable) -> None:
        self.object_canvas.submit_button.config(command=submit_command)

    def bind_to_cancel_button(self) -> None:
        self.object_canvas.cancel_button.config(command=self.hide_frame)

    def is_placing(self) -> bool:
        return self.placing

    def show_message(self, text: str, time: int) -> None:
        x: int = self.object_canvas.get_geometry()[0] - 3
        y: int = self.object_canvas.get_geometry()[1] - 10
        self.shown_message = (x, y, text)
        self.redraw()
        self.object_canvas.after(time, self.hide_message)

    def hide_message(self) -> None:
        self.shown_message = ()
        self.redraw()

    def draw(self, comp_type: str, x1: int, y1: int, x2: int = 0, y2: int = 0, save: bool = True) -> int:
        item_id: int = -1
        aligned_coords: Tuple[int, int] = (x1, y1)

        if comp_type.upper() == "COMPONENT/ROUTER" or comp_type.upper() == "COMPONENT/HOST":
            aligned_coords = self.re_align_coords(
                x1, y1, self.node_width, self.node_width)
            if aligned_coords is None or self.intersects(aligned_coords[0], aligned_coords[1], self.node_width, self.node_height)[1] != -1:
                return item_id
        # elif comp_type.upper() == "INTERFACE":
            #aligned_coords = self.re_align_coords(x1, y1, 10, 10)
            # if aligned_coords is None or self.intersects(aligned_coords[0], aligned_coords[1], 10, 10)[1] != -1:
                # return item_id

        self.redraw()
        if comp_type.upper() == "COMPONENT/ROUTER":
            item_id: int = self.object_canvas.draw_component(
                aligned_coords[0], aligned_coords[1], self.node_width, self.node_height, "ROUTER")
            if save:
                self.routers.append(
                    (item_id, aligned_coords[0], aligned_coords[1]))
        elif comp_type.upper() == "COMPONENT/HOST":
            item_id: int = self.object_canvas.draw_component(
                aligned_coords[0], aligned_coords[1], self.node_width, self.node_height, "HOST")
            if save:
                self.hosts.append(
                    (item_id, aligned_coords[0], aligned_coords[1]))
        elif comp_type.upper() == "LINK":
            item_id: int = self.object_canvas.draw_link(x1, y1, x2, y2)
            self.links.append((item_id, x1, y1, x2, y2))
        # elif comp_type.upper() == "INTERFACE":
            # item_id: int = self.object_canvas.draw_interface(
            # aligned_coords[0], aligned_coords[1])
            # if save:
            # self.interfaces.append(
            # (item_id, aligned_coords[0], aligned_coords[1]))

        return item_id

    def redraw(self) -> None:
        self.object_canvas.clear_canvas()
        for _, x1, y1, x2, y2 in self.links:
            self.object_canvas.draw_link(x1, y1, x2, y2)
        for _, x, y in self.hosts:
            self.object_canvas.draw_component(
                x, y, self.node_width, self.node_height, "HOST")
        for _, x, y in self.routers:
            self.object_canvas.draw_component(
                x, y, self.node_width, self.node_height, "ROUTER")
        # for _, x, y in self.interfaces:
            #self.object_canvas.draw_interface(x, y)
        if (self.shown_message != ()):
            self.object_canvas.draw_string(
                self.shown_message[0], self.shown_message[1], self.shown_message[2])

    def intersects(self, x, y, width, height) -> Tuple[str, int]:
        for host in self.hosts:
            if (host[1] <= x + width and host[2] <= y + height and host[1] + self.node_width >= x and host[2] + self.node_height >= y):
                return ("HOST", host[0])
        for router in self.routers:
            if (router[1] <= x + width and router[2] <= y + height and router[1] + self.node_width >= x and router[2] + self.node_height >= y):
                return ("ROUTER", router[0])
        # for interface in self.interfaces:
            # if (interface[1] <= x + width and interface[2] <= y + height and interface[1] + 10 >= x and interface[2] + 10 >= y):
                # return ("INTERFACE", interface[0])
        return ("", -1)

    def delete_component(self, comp_type: str, item_id: int) -> bool:
        if comp_type == "HOST":
            for host in self.hosts:
                if host[0] == item_id:
                    self.hosts.remove(host)
                    self.redraw()
                    return True
        elif comp_type == "ROUTER":
            for router in self.routers:
                if router[0] == item_id:
                    self.routers.remove(router)
                    self.redraw()
                    return True
        return False

    def delete_link(self, item_id: int) -> bool:
        for link in self.links:
            if link[0] == item_id:
                self.links.remove(link)
                self.redraw()
                return True
        return False

    # def delete_interface(self, item_id: int) -> bool:
        # for interface in self.interfaces:
        # if interface[0] == item_id:
        # self.interfaces.remove(interface)
        # self.redraw()
        # return True
        # return False

    def re_align_coords(self, x: int, y: int, width: int, height: int) -> Tuple[int, int]:
        # Magic numbers are due to the ridge taking up some space
        # They have been tested thoroughly manually
        # TODO add a named variable serving as the maximum size on either side
        max_x = self.object_canvas.get_geometry()[0] - 3
        max_y = self.object_canvas.get_geometry()[1] - 3

        # Positions to check:
        #  1----------2----------3
        #  |                     |
        #  |          |          |
        #  |          |          |
        #  4       ---5---       6
        #  |          |          |
        #  |          |          |
        #  |                     |
        #  7----------8----------9

        coords: Tuple[int, int] = None
        # TODO group the conditions here instead of adding magic numbers
        left_corner: bool = x <= 1 and y <= 1

        # 1
        if (x <= 1 and y <= 1):
            coords = (2, 2)
        # 3
        elif (x + width > max_x and y <= 1):
            coords = (max_x - width, 2)
        # 2
        elif (x > 1 and y <= 1):
            coords = (x, 2)
        # 7
        elif (x <= 1 and y + height > max_y):
            coords = (2, max_y - height)
        # 9
        elif (x + width > max_x and y + height > max_y):
            coords = (max_x - width, max_y - height)
        # 8
        elif (x > 1 and y + height > max_y):
            coords = (x, max_y - height)
        # 4
        elif (x <= 1 and y > 1):
            coords = (2, y)
        # 6
        elif (x + width > max_x and y > 1):
            coords = (max_x - width, y)
        # 5
        else:
            coords = (x, y)

        return coords

    def show_menu(self) -> None:
        x: int = self.mouse_pos_x
        y: int = self.mouse_pos_y
        menu_type: Tuple[str, int] = self.intersects(x, y, 1, 1)
        if menu_type[0].upper() == "ROUTER":
            menu: Menu = self.object_canvas.router_config_menu
        elif menu_type[0].upper() == "HOST":
            menu: Menu = self.object_canvas.host_config_menu
        else:
            menu: Menu = self.object_canvas.network_config_menu
        self.menu_x = x
        self.menu_y = y
        self.object_canvas.show_menu(menu, x, y)

    def get_network_config_menu_frames(self) -> List[str]:
        return ["PLACEHOST", "PLACEROUTER"]

    def get_host_config_menu_frames(self) -> List[str]:
        return ["ADDINTERFACE", "DELETEINTERFACE", "SETAPPLICATION", "SEND", "CONNECT", "DISCONNECT"]

    def get_router_config_menu_frames(self) -> List[str]:
        return ["ADDINTERFACE", "DELETEINTERFACE", "CONNECT", "DISCONNECT"]

    def show_frame(self, frame_type: str, func: Callable) -> None:
        aligned_coords: Tuple[int, int] = self.re_align_coords(
            self.mouse_pos_x, self.mouse_pos_y, 350, 350)
        x: int = aligned_coords[0]
        y: int = aligned_coords[1]
        if frame_type == "PLACEHOST":
            self.object_canvas.setup_place_host_frame(x, y)
            self.bind_to_submit_button(func)
        elif frame_type == "PLACEROUTER":
            self.object_canvas.setup_place_router_frame(x, y)
            self.bind_to_submit_button(func)
        elif frame_type == "ADDINTERFACE":
            self.object_canvas.setup_add_interface_frame(x, y)
            self.bind_to_submit_button(func)
        elif frame_type == "DELETEINTERFACE":
            self.object_canvas.setup_delete_interface_frame(x, y)
            self.bind_to_submit_button(func)
        elif frame_type == "SETAPPLICATION":
            self.object_canvas.setup_set_application_frame(x, y)
            self.bind_to_submit_button(func)
        elif frame_type == "SEND":
            self.object_canvas.setup_start_sending_frame(x, y)
            self.bind_to_submit_button(func)
        elif frame_type == "CONNECT":
            self.object_canvas.setup_connect_to_node_frame(x, y)
            self.bind_to_submit_button(func)
        else:
            self.object_canvas.setup_disconnect_interface_frame(x, y)
            self.bind_to_submit_button(func)

    def hide_frame(self) -> None:
        self.object_canvas.clear_frame()

    def check_regex(self, title_label: str) -> bool:
        name_regex: str = "^.{1,15}$"
        ip_regex: str = "^((25[0-5]|(2[0-4]|1\d|[1-9]|)\d)(\.(?!$)|$)){4}$"
        digit_regex: str = "^\d{1,2}$"
        if title_label.upper() == "PLACE HOST":
            frst: bool = regex_matches(
                name_regex, self.object_canvas.entry_1.get())
            snd: bool = regex_matches(
                ip_regex, self.object_canvas.entry_2.get())
            thrd: bool = regex_matches(
                digit_regex, self.object_canvas.entry_3.get())
            return frst and snd and thrd
        elif title_label.upper() == "PLACE ROUTER":
            frst: bool = regex_matches(
                name_regex, self.object_canvas.entry_1.get())
            snd: bool = regex_matches(
                ip_regex, self.object_canvas.entry_2.get())
            thrd: bool = regex_matches(
                digit_regex, self.object_canvas.entry_3.get())
            frth: bool = regex_matches(
                digit_regex, self.object_canvas.entry_4.get())
            return frst and snd and thrd and frth
        elif title_label.upper() == "ADD INTERFACE":
            frst: bool = regex_matches(
                name_regex, self.object_canvas.entry_1.get())
            return frst
        elif title_label.upper() == "DELETE INTERFACE":
            frst: bool = regex_matches(
                name_regex, self.object_canvas.entry_1.get())
            return frst
        elif title_label.upper() == "SET APPLICATION":
            app_type_regex: str = "^CONST$|^AIMD$"
            frst: bool = regex_matches(
                name_regex, self.object_canvas.entry_1.get())
            snd: bool = regex_matches(
                digit_regex, self.object_canvas.entry_2.get())
            thrd: bool = regex_matches(
                digit_regex, self.object_canvas.entry_3.get())
            frth: bool = regex_matches(
                app_type_regex, self.object_canvas.entry_4.get())
            return frst and snd and thrd and frth
        elif title_label.upper() == "START SENDING":
            frst: bool = regex_matches(
                name_regex, self.object_canvas.entry_1.get())
            return frst
        elif title_label.upper() == "CONNECT TO NODE":
            frst: bool = regex_matches(
                name_regex, self.object_canvas.entry_1.get())
            snd: bool = regex_matches(
                name_regex, self.object_canvas.entry_2.get())
            thrd: bool = regex_matches(
                name_regex, self.object_canvas.entry_3.get())
            frth: bool = regex_matches(
                digit_regex, self.object_canvas.entry_4.get())
            ffth: bool = regex_matches(
                digit_regex, self.object_canvas.entry_5.get())
            return frst and snd and thrd and frth and ffth
        elif title_label.upper() == "DISCONNECT INTERFACE":
            frst: bool = regex_matches(
                name_regex, self.object_canvas.entry_1.get())
            return frst

    def submit_input(self) -> None:
        self.input_data = []
        title_label: str = self.object_canvas.title_label.cget("text")
        if self.check_regex(title_label):
            if title_label.upper() == "PLACE HOST":
                self.placing = True
                self.input_data.append("COMPONENT/HOST")
            elif title_label.upper() == "PLACE ROUTER":
                self.placing = True
                self.input_data.append("COMPONENT/ROUTER")
            for widget in self.object_canvas.config_frame.winfo_children():
                if widget.winfo_class() == "Entry" and widget["state"] == "normal":
                    self.input_data.append(widget.get())
            self.hide_frame()
        else:
            self.object_canvas.information_label.config(fg="red")

    def get_link_endpoints(self, x1: int, y1: int, x2: int, y2: int) -> Tuple[int, int, int, int]:
        # Positions to check:
        # 1            2            3
        #   -----------------------
        #   |                     |
        #   |                     |
        #   |                     |
        # 7 |                     | 8
        #   |                     |
        #   |                     |
        #   |                     |
        #   -----------------------
        # 4            5            6

        above: bool = y2 + self.node_height <= y1
        # 1
        above_left: bool = above and x2 < x1 + self.node_width // 4
        # 2
        above_middle: bool = above and (x2 + self.node_width >= x1 + self.node_width // 4 and x2 <= x1 + self.node_width - self.node_width // 4) # TODO
        # 3
        above_right: bool = above and x2 > x1 + self.node_width - self.node_width // 4

        below: bool = y2 >= y1 + self.node_height
        # 4
        below_left: bool = below and x2 + self.node_width < x1 + self.node_width // 4
        # 5
        below_middle: bool = below and (x2 + self.node_width >= x1 + self.node_width // 4 and x2 <= x1 + self.node_width - self.node_width // 4) # TODO
        # 6
        below_right: bool = below and x2 > x1 + self.node_width - self.node_width // 4

        # 7
        left: bool = y2 + self.node_height > y1 and y2 < y1 + self.node_height and x2 + self.node_width <= x1

        # 8 - unneccessary, since the "else" branch will always cover this case

        coords: Tuple[int, int, int, int] = None
        if above_middle:
            coords = (x1 + self.node_width // 2, y1, x2 + self.node_width // 2, y2 + self.node_height)
        elif above_left:
            coords = (x1 + self.node_width // 2, y1, x2 + self.node_width, y2 + self.node_height // 2)
        elif above_right:
            coords = (x1 + self.node_width // 2, y1, x2, y2 + self.node_height // 2)
        elif below_middle:
            coords = (x1 + self.node_width // 2, y1 + self.node_height, x2 + self.node_width // 2, y2)
        elif below_left:
            coords = (x1 + self.node_width // 2, y1 + self.node_height, x2 + self.node_width, y2 + self.node_height // 2)
        elif below_right:
            coords = (x1 + self.node_width // 2, y1 + self.node_height, x2, y2 + self.node_height // 2)
        elif left:
            coords = (x1, y1 + self.node_height // 2, x2 + self.node_width, y2 + self.node_height // 2)
        else:
            coords = (x1 + self.node_width, y1 + self.node_height // 2, x2, y2 + self.node_height // 2)
        return coords

    def get_node_coords(self, item_id: int) -> Tuple[int, int]:
        for host in self.hosts:
            if host[0] == item_id:
                return (host[1], host[2])
        for router in self.routers:
            if router[0] == item_id:
                return (host[1], host[2])
        return None
