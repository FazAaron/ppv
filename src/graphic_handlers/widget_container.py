"""
This module makes WidgetContainer objects available for use when imported
"""
# Built-in modules
from tkinter import Tk
from tkinter import ttk

# Self-made modules
from src.graphic_handlers.object_canvas import ObjectCanvas
from src.graphic_handlers.object_frame import ObjectFrame
from src.graphic_handlers.statistics_frame import StatisticsFrame


class WidgetContainer:
    """
    The main container inside the main window containing every other item
    """

    def __init__(self, parent: Tk) -> None:
        self.content: ttk.Frame = ttk.Frame(parent)
        self.canvas: ObjectCanvas = ObjectCanvas(self.content)
        self.object_frame: ObjectFrame = ObjectFrame(self.content)
        self.statistics_frame: StatisticsFrame = StatisticsFrame(self.content)

        self.content.grid(column=0, row=0, sticky="nsew")
        self.content.columnconfigure(0, weight=3)
        self.content.columnconfigure(1, weight=1)
        self.content.rowconfigure(0, weight=5)
        self.content.rowconfigure(1, weight=1)
