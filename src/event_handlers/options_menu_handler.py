"""
This module makes OptionsMenuHandler objects available for use when imported
"""

from src.graphic_handlers.options_menu import OptionsMenu
from src.utils.logger import Logger


class OptionsMenuHandler:
    """
    The class handling any access to the OptionsMenu class

    Data members:
    options_menu (OptionsMenu): The Menu itself
    logger       (Logger): The logging object
    """

    def __init__(self, options_menu: OptionsMenu, logger: Logger) -> None:
        self.options_menu: OptionsMenu = options_menu
        self.logger: Logger = logger

    def show_menu(self, x: int, y: int) -> None:
        self.options_menu.pop_up(x, y)