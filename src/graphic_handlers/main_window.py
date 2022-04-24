"""
This module makes the GUI available for use when imported
"""
# Built-in modules
from tkinter import *
from tkinter import ttk

# Self-made modules
from src.graphic_handlers.object_canvas import ObjectCanvas
from src.graphic_handlers.object_frame import ObjectFrame
from src.graphic_handlers.statistics_frame import StatisticsFrame


class MainWindow:
    """
    The top-level window of the GUI, containing every single GUI element

    Data members:
    app (Tk): The top-level containing window of the GUI
    """

    def __init__(self) -> None:
        self.app: Tk = Tk()
        self.__config_main_window()

    def __config_main_window(self) -> None:
        """
        A helper method serving as a main configuration point for the top-level \
        window of the GUI\n
        This sets the following attributes of the main window:
        - title
        - icon visible when running the application
        - the initial dimensions of the main window
        """
        self.app.title("PPV Simulation")

        icon: PhotoImage = PhotoImage(file="resources/packet.png")
        self.app.iconphoto(False, icon)

        screen_width: str = str(self.app.winfo_screenwidth())
        screen_height: str = str(self.app.winfo_screenheight())
        self.app.geometry(f"{screen_width}x{screen_height}")
