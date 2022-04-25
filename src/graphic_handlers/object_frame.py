"""
This module makes ObjectFrame objects available for use when imported
"""
from tkinter import Button, Label, PhotoImage, ttk
from idlelib.tooltip import Hovertip


class ObjectFrame:
    """
    The window containing a menu for interacting with objects, contained inside \
    the main window's WidgetContainer
    """

    def __init__(self, parent: ttk.Frame) -> None:
        self.object_frame: ttk.Frame = ttk.Frame(parent)
        self.object_frame.grid(column=1, row=0, sticky="nsew")
        self.object_frame.columnconfigure((0, 1), weight=1)
        self.object_frame.rowconfigure((1, 2, 3), weight=1)
        self.arrow_button_image: PhotoImage = PhotoImage(file="resources/left_arrow.png")
        self.exit_button_image: PhotoImage = PhotoImage(file="resources/exit_icon.png")

        self.main_menu_button: Button = Button(
            self.object_frame, bd=0, image=self.arrow_button_image)
        self.main_menu_button.grid(column=0, row=0, sticky="nsew")
        self.exit_button: Button = Button(self.object_frame, bd=0, image=self.exit_button_image)
        self.exit_button.grid(column=1, row=0, sticky="nsew")
        Hovertip(self.main_menu_button, "Return to the Main Menu")
        Hovertip(self.exit_button, "Exit the application")
        self.main_menu()

    def main_menu(self) -> None:
        for widget in self.object_frame.winfo_children():
            if widget != self.main_menu_button and widget != self.exit_button:
                widget.grid_forget()
        self.main_menu_button.config(state="disabled")
        Button(self.object_frame, bd=0, text="Network Information Menu").grid(column=0, row=1, columnspan=2, sticky="nsew")
        Button(self.object_frame, bd=0, text="Placement Menu").grid(column=0, row=2, columnspan=2, sticky="nsew")
        Button(self.object_frame, bd=0, text="Component Configuration Menu").grid(column=0, row=3, columnspan=2, sticky="nsew")

    def routers_menu(self) -> None:
        pass

    def hosts_menu(self) -> None:
        pass

    def host_menu(self) -> None:
        pass

    def router_menu(self) -> None:
        pass

    def connections_menu(self) -> None:
        pass

    def applications_menu(self) -> None:
        pass

    def application_menu(self) -> None:
        pass
