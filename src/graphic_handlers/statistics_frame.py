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
    packets_sent_label     (Label): The Label to display Packets sent on
    packets_dropped_label  (Label): The Label to display Packets dropped on
    packets_received_label (Label): The Label to display Packets received on
    avg_sent_label         (Label): The Label to display average PPV sent on
    avg_dropped_label      (Label): The Label to display average PPV dropped on
    avg_received_label     (Label): The Label to display average PPV received on
    """

    def __init__(self, parent: ttk.Frame) -> None:
        self.statistics_frame: ttk.Frame = ttk.Frame(parent)

        # Setup the position of this Frame inside the parent container
        self.statistics_frame.grid(
            column=0, row=1, columnspan=2, sticky="nsew")

        # Setup the grid configuration for the Frame
        self.statistics_frame.rowconfigure((0, 1, 2), weight=1)
        self.statistics_frame.columnconfigure((0, 1), weight=1)

        # Setup the Labels
        self.packets_sent_label: Label = Label(
            self.statistics_frame, font=("JetBrainsMono NF", 10))
        self.packets_dropped_label: Label = Label(
            self.statistics_frame, font=("JetBrainsMono NF", 10))
        self.packets_received_label: Label = Label(
            self.statistics_frame, font=("JetBrainsMono NF", 10))

        self.avg_sent_label: Label = Label(
            self.statistics_frame, font=("JetBrainsMono NF", 10))
        self.avg_dropped_label: Label = Label(
            self.statistics_frame, font=("JetBrainsMono NF", 10))
        self.avg_received_label: Label = Label(
            self.statistics_frame, font=("JetBrainsMono NF", 10))

        # Set the grid cnfiguration for the Widgets
        self.packets_sent_label.grid(column=0, row=0, sticky="nsw")
        self.packets_dropped_label.grid(column=0, row=1, sticky="nsw")
        self.packets_received_label.grid(column=0, row=2, sticky="nsw")

        self.avg_sent_label.grid(column=1, row=0, sticky="nsw")
        self.avg_dropped_label.grid(column=1, row=1, sticky="nsw")
        self.avg_received_label.grid(column=1, row=2, sticky="nsw")

    def update_labels(self,
                      packets_sent: str,
                      packets_dropped: str,
                      packets_received: str,
                      avg_sent: str,
                      avg_dropped: str,
                      avg_received: str
                      ) -> None:
        """
        Update the Labels of the Frame

        Parameters:
        packets_sent     (str): The string to display in the packets_sent_label
        packets_dropped  (str): The string to display in the packets_dropped_label
        packets_received (str): The string to display in the packets_received_label
        avg_sent         (str): The string to display in the avg_sent_label
        avg_dropped      (str): The string to display in the avg_dropped_label
        avg_received     (str): The string to display in the avg_received_label
        """
        # Set the Labels to the given text
        self.packets_sent_label.config(text=packets_sent)
        self.packets_dropped_label.config(text=packets_dropped)
        self.packets_received_label.config(text=packets_received)
        self.avg_sent_label.config(text=avg_sent)
        self.avg_dropped_label.config(text=avg_dropped)
        self.avg_received_label.config(text=avg_received)
