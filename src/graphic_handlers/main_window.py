"""
This module makes the GUI available for use when imported
"""
# Built-in modules
from tkinter import *
from tkinter import ttk
from turtle import bgcolor

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

        # self.app.resizable(0, 0)

        # Add the contents of the main window
        self.__setup_containers()

    def __setup_containers(self):
        """
        A helper method setting up the main container window and it's contents
        """
        content_style = ttk.Style()
        content_style.configure("Black.TFrame", background="black")
        content: ttk.Frame = ttk.Frame(self.app, style="Black.TFrame")

        content.grid(column=0, row=0)
        content.columnconfigure(0, weight=1)
        content.rowconfigure(0, weight=1)
        pass

    def __setup_object_canvas(self):
        pass

    def __setup_object_frame(self):
        pass

    def __setup_statistics_frame(self):
        pass
