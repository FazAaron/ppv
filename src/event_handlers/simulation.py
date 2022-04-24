from src.graphic_handlers.main_window import MainWindow

class Simulation:
    def __init__(self) -> None:
        self.main_window = MainWindow()

    def start(self):
        self.main_window.app.mainloop()