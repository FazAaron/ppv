"""
This module makes StatisticsFrame objects available for use when imported
"""
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

        # Setup the position of this Frame inside the parent container
        self.statistics_frame.grid(
            column=0, row=1, columnspan=2, sticky="nsew")

        # Setup the grid configuration for the Frame
        self.statistics_frame.rowconfigure(0, weight=1)
        self.statistics_frame.rowconfigure(1, weight=1)
        self.statistics_frame.rowconfigure(2, weight=1)

        # Setup the Labels
        self.packets_sent_label: Label = Label(
            self.statistics_frame)
        self.packets_dropped_label: Label = Label(
            self.statistics_frame)
        self.packets_received_label: Label = Label(
            self.statistics_frame)

        # Set the grid cnfiguration for the Widgets
        self.packets_sent_label.grid(column=0, row=0, sticky="nsw")
        self.packets_dropped_label.grid(column=0, row=1, sticky="nsw")
        self.packets_received_label.grid(column=0, row=2, sticky="nsw")

    def update_labels(self, packets_sent: int, packets_dropped: int) -> None:
        """
        Update the Labels of the Frame

        Parameters:
        packets_sent    (int): The value to display in the packets_sent_label
        packets_dropped (int): The value to display in the packets_dropped_label
        """
        self.packets_sent_label.config(
            text=f"Packets sent: {packets_sent}")
        self.packets_dropped_label.config(
            text=f"Packets dropped: {packets_dropped}")
        self.packets_received_label.config(
            text=f"Packets received: {packets_sent - packets_dropped}")
