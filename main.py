from src.event_handlers.simulation import Simulation
from src.utils.logger import Logger

if __name__ == "__main__":
    simulation: Simulation = Simulation()
    simulation.start()