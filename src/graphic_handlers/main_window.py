"""
This module makes the GUI available for use when imported
"""
# Built-in modules
from tkinter import *
from tkinter import ttk

# Self-made modules
from src.graphic_handlers.widget_container import WidgetContainer


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
        A helper method serving as the main configuration point for the
        top-level window of the GUI\n
        This sets the following attributes of the main window:
        - title
        - icon visible when running the application
        - the initial dimensions of the main window
        - adds the contents of the main window
        """
        # Set the window title
        self.app.title("PPV Simulation")

        # Set the icon of the application
        icon: PhotoImage = PhotoImage(file="resources/packet.png")
        self.app.iconphoto(False, icon)

        # Set the dimensions of the main window
        screen_width: str = str(self.app.winfo_screenwidth())
        screen_height: str = str(self.app.winfo_screenheight())
        self.app.geometry(f"{screen_width}x{screen_height}")

        # Set the basic grid in the main window
        self.app.columnconfigure(0, weight=1)
        self.app.rowconfigure(0, weight=1)

        # Add the contents to the main window
        self.content: WidgetContainer = WidgetContainer(self.app)
