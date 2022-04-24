"""
This module makes the Simulation object available for use when imported
"""
from src.components.network import Network
from src.graphic_handlers.main_window import MainWindow


class Simulation:
    """
    The connecting piece between the components and graphic handlers

    Data members:
    main_window (MainWindow): The main window of the GUI, containing everything
    network (Network): The main object of the components, containing everything
    """

    def __init__(self) -> None:
        self.main_window: MainWindow = MainWindow()
        self.network: Network = Network()

    def start(self):
        """
        Starts the simulation, opening a new window
        """
        self.main_window.app.mainloop()
