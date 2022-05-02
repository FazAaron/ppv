"""
This module makes MainHandler objects available for use when imported
"""
# Built-in modules
from tkinter import messagebox

# Self-made modules
from src.components.network import Network
from src.event_handlers.object_canvas_handler import ObjectCanvasHandler
from src.event_handlers.object_frame_handler import ObjectFrameHandler
from src.event_handlers.statistics_frame_handler import StatisticsFrameHandler
from src.graphic_handlers.main_window import MainWindow
from src.graphic_handlers.widget_container import WidgetContainer
from src.utils.logger import Logger


class MainHandler:
    """
    This class is used to connect together the handlers for every graphical \
    component, providing them with bindings to different events, creating \
    a user-interactive graphical interface

    Data members:
    main_window              (MainWindow): The main window of the GUI, containing everything
    network                  (Network): The main object of the components, containing everything
    object_canvas_handler    (ObjectCanvasHandler): The object canvas handling object
    object_frame_handler     (ObjectFrameHandler): The object frame handling object
    statistics_frame_handler (StatisticsFrameHandler): The statistics frame handling object
    logger                   (Logger): The logger object, logging neccessary actions
    """

    def __init__(self, main_window: MainWindow, network: Network) -> None:
        self.main_window: MainWindow = main_window
        self.network: Network = network

        content: WidgetContainer = self.main_window.content
        self.object_canvas_handler: ObjectCanvasHandler = ObjectCanvasHandler(
            content.object_canvas)
        self.object_frame_handler: ObjectFrameHandler = ObjectFrameHandler(
            content.object_frame)
        self.statistics_frame_handler: StatisticsFrameHandler = StatisticsFrameHandler(
            content.statistics_frame)

        self.logger = Logger("conf/logger_config.json")

        # Setup the bindings to the Handlers
        self.__bind_to_object_frame_handler()

    # Bindings to Handlers
    ## ObjectFrameHandler specific bindings
    def __bind_to_object_frame_handler(self) -> None:
        self.object_frame_handler.bind_to_exit(self.__exit_prompt)

    ## ObjectCanvasHandler specific bindings

    ## Bindings on more than one Handler

    # Private methods
    def __exit_prompt(self) -> None:
        """
        Opens a pop-up prompt asking a yes/no question for the user, whether \
        they want to exit or not
        """
        answer: bool = messagebox.askyesno(title="Exit application",
                                           message="Are you sure you want to quit the application?")
        if answer:
            self.main_window.exit()
