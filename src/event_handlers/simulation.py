"""
This module makes the Simulation object available for use when imported
"""
# Built-in modules
from tkinter.messagebox import askyesno

# Self-made modules
from src.components.network import Network
from src.event_handlers.object_canvas_handler import ObjectCanvasHandler
from src.event_handlers.object_frame_handler import ObjectFrameHandler
from src.event_handlers.options_menu_handler import OptionsMenuHandler
from src.event_handlers.statistics_frame_handler import StatisticsFrameHandler
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
        self.__setup_object_frame_handler()
        self.__setup_options_menu_handler()
        self.__setup_statistics_frame_handler()
        self.__setup_object_canvas_handler()
        self.network: Network = Network()

    def start(self) -> None:
        """
        Starts the simulation, opening a new window
        """
        self.main_window.mainloop()

    # Private methods
    def __exit_prompt(self) -> bool:
        """
        Opens a pop-up prompt asking a yes/no question for the user, whether \
        they want to exit or not

        Returns:
        bool: Whether the user wants to exit or not
        """
        answer: bool = askyesno(title="Exit application",
                                message="Are you sure you want to quit the application?")
        if answer:
            self.main_window.exit()

    def __setup_object_frame_handler(self) -> None:
        """
        Sets up the ObjectFrameHandler object
        """
        self.object_frame_handler: ObjectFrameHandler = ObjectFrameHandler(
            self.main_window.content.object_frame, self.logger)

        # Bind to the exit button
        self.object_frame_handler.bind_to_exit(self.__exit_prompt)

    def __setup_options_menu_handler(self) -> None:
        self.options_menu_handler: OptionsMenuHandler = OptionsMenuHandler(
            self.main_window.content.options_menu, self.logger)

    def __setup_statistics_frame_handler(self) -> None:
        """
        Sets up the StatisticsFrameHandler object
        """
        self.statistics_frame_handler: StatisticsFrameHandler = StatisticsFrameHandler(
            self.main_window.content.statistics_frame, self.logger)

    def __setup_object_canvas_handler(self) -> None:
        """
        Sets up the StatisticsFrameHandler object
        """
        self.object_canvas_handler: ObjectCanvasHandler = ObjectCanvasHandler(
            self.main_window.content.object_canvas, self.logger)

        # Bind to left click
        self.object_canvas_handler.bind("<Button-1>", self.__asd)
        #self.object_canvas_handler.bind("<Button-1>", self.__asd_2)

        # Bind to left click + drag
        #self.object_canvas_handler.bind("<B1-Motion>", self.__test)

        # Bind to right click
        self.object_canvas_handler.bind("<Button-3>", self.__right_click_event)

        # Bind to motion
        #self.object_canvas_handler.bind("<Motion>", self.__asd)
        
    def __asd(self, event) -> None:
        if event.x_root > 0:
            self.object_canvas_handler.object_canvas.canvas.delete("all")
            self.object_canvas_handler.draw("INTERFACE", event.x_root, event.y_root)
            self.object_canvas_handler.object_canvas.draw_string(event.x_root + 5, event.y_root + 25)

    def __right_click_event(self, event) -> None:
        self.options_menu_handler.show_menu(event.x_root, event.y_root)
