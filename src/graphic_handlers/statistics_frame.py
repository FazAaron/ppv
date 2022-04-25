"""
This module makes StatisticsFrame objects available for use when imported
"""
from re import S
from tkinter import Label, ttk


class StatisticsFrame:
    """
    The window containing a statistics regarding the run, contained inside \
    the main window's WidgetContainer

    Data members:
    statistics_frame       (ttk.Frame): The Frame itself
    packets_sent_label     (Label): The Label to display packets sent on
    packets_dropped_label  (Label): The Label to display Packets dropped on
    packets_received_label (Label): The Label to display Packets received on
    """

    def __init__(self, parent: ttk.Frame) -> None:
        self.statistics_frame: ttk.Frame = ttk.Frame(parent)
        self.statistics_frame.grid(
            column=0, row=1, columnspan=2, sticky="nsew")
        self.statistics_frame.rowconfigure(0, weight=1)
        self.statistics_frame.rowconfigure(1, weight=1)
        self.statistics_frame.rowconfigure(2, weight=1)

        # Setup the Labels
        self.packets_sent_label: Label = Label(
            self.statistics_frame, text="Packets sent: 0")
        self.packets_dropped_label: Label = Label(
            self.statistics_frame, text="Packets dropped: 0")
        self.packets_received_label: Label = Label(
            self.statistics_frame, text="Packets received: 0")

        # Set the grid position and options
        self.packets_sent_label.grid(column=0, row=0, sticky="nsw")
        self.packets_dropped_label.grid(column=0, row=1, sticky="nsw")
        self.packets_received_label.grid(column=0, row=2, sticky="nsw")

    def update_labels(self, packets_sent: int, packets_dropped: int) -> None:
        self.packets_sent_label.config(
            text=f"Packets sent: {packets_sent}")
        self.packets_dropped_label.config(
            text=f"Packets dropped: {packets_dropped}")
        self.packets_received_label.config(
            text=f"Packets received: {packets_sent - packets_dropped}")
