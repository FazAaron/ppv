"""
This module makes ObjectFrameHandler objects available for use when imported
"""
# Built-in modules
from typing import Callable

# Self-made modules
from src.graphic_handlers.object_frame import ObjectFrame


class ObjectFrameHandler():
    """
    The class handling any access to the ObjectFrame class

    Data members:
    object_frame (ObjectFrame): The Frame itself to access
    """

    def __init__(self, object_frame: ObjectFrame) -> None:
        self.object_frame: ObjectFrame = object_frame
        start_display: str = ("Press right-click on the display or on a component\nto start working with the Network\n\n"
                              "Press left-click on a component to display its attributes here\n\n"
                              "Press left-click on a component and then drag to move it")

        # Display a starting text
        self.display_text(start_display)

    def display_text(self, to_display: str) -> None:
        """
        Displays text in the object_frame

        Parameters:
        to_display (str): The string to display
        """
        self.object_frame.display_text(to_display)

    def bind_to_exit(self, func: Callable) -> None:
        """
        Binds an event to the exit_button

        Parameters:
        func (Callable): The function to call on exit_button click
        """
        self.object_frame.exit_button.config(command=func)
