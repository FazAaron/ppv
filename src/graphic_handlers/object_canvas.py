"""
This module makes ObjectCanvas objects available for use when imported
"""
from tkinter import Canvas
from tkinter import ttk


class ObjectCanvas:

    def __init__(self, parent: ttk.Frame) -> None:
        self.canvas: Canvas = Canvas(
            parent, background="lightgrey", bd=0, highlightthickness=0)
        self.canvas.grid(column=0, row=0, sticky="nsew")

    def __motion_handler(event: str):
        pass

    def __left_click_handler(event: str):
        pass

    def __right_click_handler(event: str):
        pass
