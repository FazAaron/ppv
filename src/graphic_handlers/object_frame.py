"""
This module makes ObjectFrame objects available for use when imported
"""
from tkinter import ttk


class ObjectFrame:
    """
    The window containing a menu for interacting with objects, contained inside \
    the main window's WidgetContainer
    """

    def __init__(self, parent: ttk.Frame) -> None:
        self.object_frame: ttk.Frame = ttk.Frame(parent, relief="ridge")
        self.object_frame.grid(column=1, row=0, sticky="nsew")
