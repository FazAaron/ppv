"""
This module makes ObjectCanvas objects available for use when imported
"""
from tkinter import Canvas, ttk, Menu
from typing import Callable, Tuple


class ObjectCanvas:
    """
    The canvas to 'draw' to, contained inside the main window's WidgetContainer

    Data members:
    canvas              (Canvas): The canvas to draw to
    network_config_menu (Menu): The Menu for configuring the Network
    host_config_menu    (Menu): The Menu to configure a Host
    router_config_menu  (Menu): The Menu to configure a Router
    config_menu         (ttk.Frame): The Frame to access certain features of \
                                     the Network
    """

    def __init__(self, parent: ttk.Frame) -> None:
        self.canvas: Canvas = Canvas(
            parent, background="lightgrey", bd=1, highlightthickness=1, relief="ridge")
        self.network_config_menu: Menu = None
        self.host_config_menu: Menu = None
        self.router_config_menu: Menu = None
        self.config_menu: ttk.Frame = None

        # Set the position of this Frame inside the parent container
        self.canvas.grid(column=0, row=0, sticky="nsew")

    def get_geometry(self) -> Tuple[int, int]:
        return (self.canvas.winfo_width(), self.canvas.winfo_height())

    def bind(self, event_type: str, func: Callable) -> None:
        self.canvas.bind(event_type, func, add="+")

    def draw_component(self, x: int, y: int, component_type: str) -> int:
        item_id: int = -1
        if component_type.upper() == "ROUTER":
            item_id = self.canvas.create_rectangle(x, y, x + 32, y + 32, fill="lightblue")
        elif component_type.upper() == "HOST":
            item_id = self.canvas.create_rectangle(x, y, x + 32, y + 32, fill="grey")
        return item_id

    def draw_link(self, x1: int, y1: int, x2: int, y2: int) -> int:
        return self.canvas.create_line(x1, y1, x2, y2, fill="grey", width="3")

    def draw_interface(self, x: int, y: int) -> int:
        return self.canvas.create_rectangle(x, y, x + 10, y + 10, fill="white")

    def draw_string(self, x: int, y: int) -> None:
        self.canvas.create_text(x, y, text="Asd")

    def clear_canvas(self) -> None:
        self.canvas.delete("all")

    def setup_network_config_menu(self) -> Menu:
        if self.network_config_menu is None:
            self.network_config_menu = Menu(self.canvas, tearoff=0)
            self.network_config_menu.add_command(label="Place Host")
            self.network_config_menu.add_command(label="Place Router")
        return self.network_config_menu

    def setup_host_config_menu(self) -> Menu:
        if self.host_config_menu is None:
            self.host_config_menu = Menu(self.canvas, tearoff=0)
            self.host_config_menu.add_command(label="Delete Component")
            self.host_config_menu.add_command(label="Add Interface")
            self.host_config_menu.add_command(label="Delete Interface")
            self.host_config_menu.add_command(label="Set Application")
            self.host_config_menu.add_command(label="Start sending")
            self.host_config_menu.add_command(label="Connect to Node")
            self.host_config_menu.add_command(label="Disconnect Interface")
        return self.host_config_menu

    def setup_router_config_menu(self) -> Menu:
        if self.router_config_menu is None:
            self.router_config_menu = Menu(self.canvas, tearoff=0)
            self.router_config_menu.add_command(label="Delete Component")
            self.router_config_menu.add_command(label="Add Interface")
            self.router_config_menu.add_command(label="Delete Interface")
            self.router_config_menu.add_command(label="Connect to Node")
            self.router_config_menu.add_command(label="Disconnect Interface")
        return self.router_config_menu

    def setup_place_host_frame(self) -> None:
        pass

    def setup_place_router_frame(self) -> None:
        pass

    def setup_add_interface_frame(self) -> None:
        pass

    def setup_delete_interface_frame(self) -> None:
        pass

    def setup_set_application_frame(self) -> None:
        pass

    def setup_set_application_frame(self) -> None:
        pass

    def setup_start_sending_frame(self) -> None:
        pass

    def setup_connect_to_node_frame(self) -> None:
        pass

    def setup_disconnect_interface_frame(self) -> None:
        pass

# """
# This module makes OptionsMenu objects available for use when imported
# """
#from tkinter import Button, Entry, Label, Menu, ttk


# class OptionsMenu:

    # def __init__(self, parent: ttk.Frame) -> None:
        #self.parent = parent
        #self.options_menu: Menu = Menu(parent, tearoff=0)
        #self.options_menu.add_command(label="1", command=self.show_canvas_options)
        # self.options_menu.add_command(label="1")
        # self.options_menu.add_command(label="1")
        # self.options_menu.add_command(label="1")
        # self.options_menu.add_command(label="1")
        # self.options_menu.add_command(label="1")
        # To remove menu items self.options_menu.delete(1, 5)

    # def pop_up(self, x: int, y: int) -> None:
        #self.x = x
        #self.y = y
        #self.options_menu.tk_popup(x, y)

    # def show_frame(self) -> None:
        #test = ttk.Frame(self.parent, relief="ridge")
        #self.entry_1 = Entry(test)
        #button = Button(test, text="asd", command=self.stuff)
        #label_1 = Label(test, text="asd")
        #test.place(x=self.x, y=self.y, width=250, height=250)
        #button.place(x=2, y=0, width=250, height=100)
        #label_1.place(x=2, y=100, width=100, height=150)
        #self.entry_1.place(x=50, y=100, width=150, height=150)

    # def show_host_options(self) -> None:
        #self.options_menu.delete(0, self.options_menu.index("end"))

    # def show_router_options(self) -> None:
        #self.options_menu.delete(0, self.options_menu.index("end"))

    # def show_canvas_options(self) -> None:
        #self.options_menu.delete(0, self.options_menu.index("end"))

    # def test_stuff(self) -> None:
        #test = ttk.Frame(self.parent, relief="ridge")
        #self.entry_1 = Entry(test)
        #button = Button(test, text="asd", command=self.stuff)
        #label_1 = Label(test, text="asd")
        #test.place(x=self.x, y=self.y, width=250, height=250)
        #button.place(x=0, y=0)
        #label_1.place(x=0, y=button.winfo_y() + button.winfo_height())
        #self.entry_1.place(x=0, y=label_1.winfo_height())

    # def stuff(self) -> None:
        # print(self.entry_1.get())
