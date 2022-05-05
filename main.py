"""
This module makes the Simulation object available for use when imported\n
This is the main entry point of the program
"""
from src.components.network import Network
from src.event_handlers.main_handler import MainHandler
from src.graphic_handlers.main_window import MainWindow


class Simulation:
    """
    The Simulation itself, containing the main components of the program

    Data members:
    main_window  (MainWindow): The main window of the GUI, containing everything
    network      (Network): The main object of the components, containing everything
    main_handler (MainHandler): The main event handling object, connecting \
                                event handlers together
    """

    def __init__(self) -> None:
        self.network: Network = Network()
        self.main_window: MainWindow = MainWindow()
        self.main_handler: MainHandler = MainHandler(
            self.main_window, self.network)

    def start(self) -> None:
        """
        Starts the simulation, opening a new window
        """
        self.main_window.mainloop()


if __name__ == "__main__":
    simulation: Simulation = Simulation()
    simulation.start()
