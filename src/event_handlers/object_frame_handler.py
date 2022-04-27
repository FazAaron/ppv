"""
This module makes ObjectFrameHandler objects available for use when imported
"""
# Built-in modules - for type hints
from typing import Callable

# Self-made modules
from src.graphic_handlers.object_frame import ObjectFrame
from src.utils.logger import Logger


class ObjectFrameHandler():

    def __init__(self, object_frame: ObjectFrame, logger: Logger) -> None:
        self.object_frame: ObjectFrame = object_frame
        self.logger: Logger = logger

    def bind_to_exit(self, func=Callable) -> None:
        """
        Binds an event to the exit_button

        Parameters:
        func (Callable): The function to call on exit_button click
        """
        self.object_frame.exit_button.config(command=func)

    def display_text(self, to_display: str) -> None:
        """
        Displays text in the object_frame

        Parameters:
        to_display (str): The string to display
        """
        self.object_frame.display_text(to_display)
