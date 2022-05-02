"""
This module makes ObjectCanvas objects available for use when imported
"""
from tkinter import Canvas, PhotoImage, ttk
from typing import List, Tuple


class ObjectCanvas:
    """
    The canvas to 'draw' to, contained inside the main window's WidgetContainer

    Data members:
    canvas     (Canvas): The canvas to draw to
    placing    (Tuple[str, bool]): Whether the user is placing at the moment or not
    router_img (PhotoImage): The image of the Router
    host_img   (PhotoImage): The image of the Host
    components (List[Tuple[int, int]]): The coordinates of the components
    """

    def __init__(self, parent: ttk.Frame) -> None:
        self.canvas: Canvas = Canvas(
            parent, background="lightgrey", bd=1, highlightthickness=1, relief="ridge")
        self.placing: Tuple[str, bool] = "", False
        self.router_img: PhotoImage = PhotoImage(file="resources/router.png")
        self.host_img: PhotoImage = PhotoImage(file="resources/host.png")
        self.hosts: List[Tuple[int, int, int]] = []
        self.routers: List[Tuple[int, int, int]] = []
        self.interfaces: List[Tuple[int, int, int]] = []
        self.links: List[Tuple[int, int, int, int, int]] = []

        # Set the position of this Frame inside the parent container
        self.canvas.grid(column=0, row=0, sticky="nsew")

    def bind(self, event_type: str, func) -> None:
        self.canvas.bind(event_type, func, add="+")

    def intersects(self, x, y, width, height) -> bool:
        pass

    def link_intersects(self, x, y, width, height) -> bool:
        pass

    def draw_component(self, x: int, y: int, component_type: str) -> None:
        if component_type.upper() == "ROUTER":
            item_id: int = self.canvas.create_image((x, y), image=self.router_img)
            self.routers.append((item_id, x, y))
        elif component_type.upper() == "HOST":
            item_id: int = self.canvas.create_image((x, y), image=self.host_img)
            self.hosts.append((item_id, x, y))

    def draw_link(self, x1: int, y1: int, x2: int, y2: int) -> None:
        self.canvas.create_line(x1, y1, x2, y2, fill="grey", width="3")

    def draw_interface(self, x: int, y: int) -> None:
        self.canvas.create_rectangle(x, y, x + 10, y + 10, fill="white")

    def draw_string(self, x: int, y: int) -> None:
        self.canvas.create_text(x, y, text="Asd")

    def delete_component(self, x: int, y: int) -> None:
        pass

    def delete_link(self, x: int, y: int) -> None:
        pass

    def delete_interface(self, x: int, y: int) -> None:
        pass

    def __redraw(self) -> None:
        for _, x, y in self.hosts:
            pass
        for _, x, y in self.routers:
            self.canvas.create_image((x, y), image=self.router_img)
        for _, x, y in self.interfaces:
            pass
        for _, x1, y1, x2, y2 in self.links:
            pass

    def clear_canvas(self) -> None:
        self.canvas.delete("all")
        self.__redraw()

    def show_menu(self, type: str) -> None:
        pass

    def show_frame(self) -> None:
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
