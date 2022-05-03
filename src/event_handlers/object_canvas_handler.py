"""
This module makes ObjectCanvasHandler objects available for use when imported
"""
# Built-in modules
from typing import Callable, Tuple, List

# Self-made modules
from src.graphic_handlers.object_canvas import ObjectCanvas


class ObjectCanvasHandler:
    """
    The class handling any access to the ObjectCanvas class, and also handling \
    specific actions using the methods binded to them by the MainHandler class

    Data members:
    object_canvas (ObjectCanvas): The Frame itself to access
    """

    def __init__(self, object_canvas: ObjectCanvas) -> None:
        self.object_canvas: ObjectCanvas = object_canvas
        self.placing: Tuple[str, bool] = "", False
        self.hosts: List[Tuple[int, int, int]] = []
        self.routers: List[Tuple[int, int, int]] = []
        self.interfaces: List[Tuple[int, int, int]] = []
        self.links: List[Tuple[int, int, int, int, int]] = []

    def bind(self, event: str, func: Callable) -> None:
        self.object_canvas.bind(event, func)

    def is_placing(self) -> None:
        return self.object_canvas.placing[1]

    def draw(self, comp_type: str, x1: int, y1: int, x2: int = 0, y2: int = 0) -> int:
        item_id: int = -1
        aligned_coords: Tuple[int, int] = (x1, y1)

        if comp_type.upper() == "COMPONENT/ROUTER" or comp_type.upper() == "COMPONENT/HOST":
            aligned_coords = self.re_align_coords(x1, y1, 32, 32)
            if aligned_coords is None or self.intersects(aligned_coords[0], aligned_coords[1], 32, 32)[1] is not None:
                return item_id
        elif comp_type.upper() == "INTERFACE":
            aligned_coords = self.re_align_coords(x1, y1, 10, 10)
            if aligned_coords is None or self.intersects(aligned_coords[0], aligned_coords[1], 10, 10)[1] is not None:
                return item_id

        if comp_type.upper() == "COMPONENT/ROUTER":
            item_id = self.object_canvas.draw_component(
                aligned_coords[0], aligned_coords[1], "ROUTER")
            self.routers.append(
                (item_id, aligned_coords[0], aligned_coords[1]))
        elif comp_type.upper() == "COMPONENT/HOST":
            item_id = self.object_canvas.draw_component(
                aligned_coords[0], aligned_coords[1], "HOST")
            self.hosts.append((item_id, aligned_coords[0], aligned_coords[1]))
        elif comp_type.upper() == "LINK":
            item_id = self.object_canvas.draw_link(x1, y1, x2, y2)
            self.links.append((item_id, x1, y1, x2, y2))
        elif comp_type.upper() == "INTERFACE":
            item_id = self.object_canvas.draw_interface(
                aligned_coords[0], aligned_coords[1])
            self.interfaces.append(
                (item_id, aligned_coords[0], aligned_coords[1]))

        return item_id

    def redraw(self) -> None:
        self.object_canvas.clear_canvas()
        for _, x, y in self.hosts:
            self.object_canvas.draw_component(x, y, "HOST")
        for _, x, y in self.routers:
            self.object_canvas.draw_component(x, y, "ROUTER")
        for _, x, y in self.interfaces:
            self.object_canvas.draw_interface(x, y)
        for _, x1, y1, x2, y2 in self.links:
            self.object_canvas.draw_link(x1, y1, x2, y2)

    def intersects(self, x, y, width, height) -> Tuple[str, int]:
        for host in self.hosts:
            if (host[1] <= x + width and host[2] <= y + height and host[1] + 32 >= x and host[2] + 32 >= y):
                return ("host", host[0])
        for router in self.routers:
            if (router[1] <= x + width and router[2] <= y + height and router[1] + 32 >= x and router[2] + 32 >= y):
                return ("router", router[0])
        for interface in self.interfaces:
            if (interface[1] <= x + width and interface[2] <= y + height and interface[1] + 10 >= x and interface[2] + 10 >= y):
                return ("interface", interface[0])
        return ("", None)

    def delete_component(self, item_id: int) -> bool:
        for host in self.hosts:
            if host[0] == item_id:
                self.hosts.remove(host)
                self.redraw()
                return True
        for router in self.hosts:
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

    def delete_interface(self, item_id: int) -> bool:
        for interface in self.interfaces:
            if interface[0] == item_id:
                self.interfaces.remove(interface)
                self.redraw()
                return True
        return False

    def re_align_coords(self, x: int, y: int, width: int, height: int) -> Tuple[int, int]:
        # Magic numbers are due to the ridge taking up some space
        # They have been tested thoroughly manually
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

        # 1
        if (x <= 1 and y <= 1):
            #self.canvas.create_rectangle(2, 2, width + 2, height + 2)
            coords = (2, 2)
        # 3
        elif (x + width > max_x and y <= 1):
            # self.canvas.create_rectangle(max_x - width, 2, max_x, height + 2)
            coords = (max_x - width, 2)
        # 2
        elif (x > 1 and y <= 1):
            # self.canvas.create_rectangle(x, 2, x + width, height + 2)
            coords = (x, 2)
        # 7
        elif (x <= 1 and y + height > max_y):
            # self.canvas.create_rectangle(2, max_y - height, width + 2, max_y)
            coords = (2, max_y - height)
        # 9
        elif (x + width > max_x and y + height > max_y):
            #self.canvas.create_rectangle(max_x - width, max_y - height, max_x, max_y)
            coords = (max_x - width, max_y - height)
        # 8
        elif (x > 1 and y + height > max_y):
            # self.canvas.create_rectangle(x, max_y - height, x + width, max_y)
            coords = (x, max_y - height)
        # 4
        elif (x <= 1 and y > 1):
            # self.canvas.create_rectangle(2, y, width + 2, y + height)
            coords = (2, y)
        # 6
        elif (x + width > max_x and y > 1):
            # self.canvas.create_rectangle(max_x - width, y, max_x, y + height)
            coords = (max_x - width, y)
        # 5
        else:
            #self.canvas.create_rectangle(x, y, x + width, y + height)
            coords = (x, y)

        return coords

    def show_menu(self, x: int, y: int) -> None:
        menu_type = self.intersects(x, y, 1, 1)
        if menu_type[0] == "router":
            self.object_canvas.setup_router_config_menu().tk_popup(x, y)
        elif menu_type[0] == "host":
            self.object_canvas.setup_host_config_menu().tk_popup(x, y)
        else:
            self.object_canvas.setup_network_config_menu().tk_popup(x, y)
            