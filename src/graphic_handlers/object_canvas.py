"""
This module makes ObjectCanvas objects available for use when imported
"""
from tkinter import Canvas, PhotoImage, ttk
from typing import List, Tuple


class ObjectCanvas:
    """
    The canvas to 'draw' to, contained inside the main window's WidgetContainer
    """

    def __init__(self, parent: ttk.Frame) -> None:
        self.canvas: Canvas = Canvas(
            parent, background="lightgrey", bd=1, highlightthickness=1, relief="ridge")
        self.canvas.grid(column=0, row=0, sticky="nsew")
        self.placing: bool = False  # Might not be needed here
        self.router_img: PhotoImage = PhotoImage(file="resources/router.png")
        self.host_img: PhotoImage = PhotoImage(file="resources/host.png")
        self.components: List[Tuple(int, int)] = []

    def bind(self, event_type: str, func) -> None:
        self.canvas.bind(event_type, func)

    def intersects(self, x, y, width, height) -> bool:
        pass

    def draw_component(self, x: int, y: int, component_type: str) -> None:
        if component_type == "ROUTER":
            self.canvas.create_image((x, y), image=self.router_img)
            self.components.append((x, y))
        elif component_type == "HOST":
            self.canvas.create_image((x, y), image=self.host_img)
            self.components.append((x, y))

    def draw_link(self, x1: int, y1: int, x2: int, y2: int) -> None:
        self.canvas.create_line(x1, y1, x2, y2, fill="grey", width="3")

    def draw_interface(self, x: int, y: int) -> None:
        self.canvas.create_rectangle(x, y, x + 5, y + 10, fill="white")

    def delete_component(self, x: int, y: int) -> None:
        pass

    def delete_link(self, x: int, y: int) -> None:
        pass

    def delete_interface(self, x: int, y: int) -> None:
        pass
