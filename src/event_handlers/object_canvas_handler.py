"""
This module makes ObjectCanvasHandler objects available for use when imported
"""
# Built-in modules
from typing import Callable

# Self-made modules
from src.components.network import Network
from src.graphic_handlers.object_canvas import ObjectCanvas
from src.utils.logger import Logger


class ObjectCanvasHandler:
    """
    The class handling any access to the ObjectCanvas class, and also handling \
    specific actions using the methods binded to them by the MainHandler class

    Data members:
    object_canvas (ObjectCanvas): The Frame itself to access
    """

    def __init__(self, object_canvas: ObjectCanvas) -> None:
        self.object_canvas: ObjectCanvas = object_canvas

    def bind(self, event: str, func: Callable) -> None:
        self.object_canvas.bind(event, func)

    def is_placing(self) -> None:
        return self.object_canvas.placing[1]

    def draw(self, comp_type: str, x1: int, y1: int, x2: int = 0, y2: int = 0) -> None:
        self.object_canvas.clear_canvas()
        if comp_type.upper() == "COMPONENT/ROUTER":
            self.object_canvas.draw_component(x1, y1, "ROUTER")
        elif comp_type.upper() == "COMPONENT/HOST":
            self.object_canvas.draw_component(x1, y1, "HOST")
        elif comp_type.upper() == "LINK":
            self.object_canvas.draw_link(x1, y1, x2, y2)
        elif comp_type.upper() == "INTERFACE":
            self.object_canvas.draw_interface(x1, y1)
