"""
This module makes the Simulation object available for use when imported
"""
from src.event_handlers.object_frame_handler import ObjectFrameHandler
from src.components.network import Network
from src.graphic_handlers.main_window import MainWindow
from src.utils.logger import Logger


class Simulation:
    """
    The connecting piece between the components and graphic handlers

    Data members:
    main_window (MainWindow): The main window of the GUI, containing everything
    network (Network): The main object of the components, containing everything
    logger (Logger): The logger object that writes the logs to a file
    """

    def __init__(self) -> None:
        self.logger: Logger = Logger("conf/logger_config.json")
        self.main_window: MainWindow = MainWindow()
        self.object_frame_handler: ObjectFrameHandler = ObjectFrameHandler(
            self.main_window.content.object_frame, self.logger)
        self.network: Network = Network()

    def start(self) -> None:
        """
        Starts the simulation, opening a new window
        """
        self.main_window.mainloop()
