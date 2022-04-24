"""
This module makes ObjectCanvas objects available for use when imported
"""
from tkinter import Canvas, PhotoImage
from tkinter import ttk


class ObjectCanvas:
    """
    The canvas to 'draw' to, contained inside the main window's WidgetContainer
    """

    def __init__(self, parent: ttk.Frame) -> None:
        self.canvas: Canvas = Canvas(
            parent, background="lightgrey", bd=0, highlightthickness=0)
        self.canvas.grid(column=0, row=0, sticky="nsew")
        self.placing: bool = False
        self.router_img: PhotoImage = PhotoImage(file="resources/router.png")
        self.host_img: PhotoImage = PhotoImage(file="resources/host.png")

    def bind(self, event_type: str, func) -> None:
        self.canvas.bind(event_type, func)

    def draw_img(self, x: int, y: int, component_type: str) -> None:
        if component_type == "ROUTER":
            self.canvas.create_image((x, y), image=self.router_img)
        elif component_type == "HOST":
            self.canvas.create_image((x, y), image=self.host_img)
