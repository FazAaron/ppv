"""
This module makes MainHandler objects available for use when imported
"""
from src.components.network import Network
from src.graphic_handlers.main_window import MainWindow
from src.utils.logger import Logger


class MainHandler:

    def __init__(self, main_window: MainWindow, network: Network) -> None:
        self.main_window: MainWindow = main_window
        self.network: Network = network
        self.logger = Logger("conf/logger_config.json")
