"""
This module makes StatisticsFrame objects available for use when imported
"""
from tkinter import ttk


class StatisticsFrame:

    def __init__(self, parent: ttk.Frame) -> None:
        self.statistics_frame: ttk.Frame = ttk.Frame(parent, relief="ridge")
        self.statistics_frame.grid(
            column=0, row=1, columnspan=2, sticky="nsew")
