"""
This module makes ObjectFrame objects available for use when imported
"""
from tkinter import Button, PhotoImage, ttk, Scrollbar, Listbox, END
from idlelib.tooltip import Hovertip


class ObjectFrame:
    """
    The window containing a menu for interacting with objects, contained inside \
    the main window's WidgetContainer
    """

    def __init__(self, parent: ttk.Frame) -> None:
        self.object_frame: ttk.Frame = ttk.Frame(parent)
        self.arrow_button_image: PhotoImage = PhotoImage(
            file="resources/left_arrow.png")
        self.exit_button_image: PhotoImage = PhotoImage(
            file="resources/exit_icon.png")
        self.home_button_image: PhotoImage = PhotoImage(
            file="resources/home_icon.png")

        self.object_frame.grid(column=1, row=0, sticky="nsew")

        self.object_frame.columnconfigure((0, 1, 2), weight=1)

        # Buttons for navigation
        self.previous_menu_button: Button = Button(
            self.object_frame, bd=0, image=self.arrow_button_image, state="disabled")
        self.previous_menu_button.grid(column=0, row=0, sticky="nsew")
        Hovertip(self.previous_menu_button, "Return to the previous menu")

        self.main_menu_button: Button = Button(
            self.object_frame, bd=0, image=self.home_button_image)
        self.main_menu_button.grid(column=1, row=0, sticky="nsew")
        Hovertip(self.main_menu_button, "Go to the main menu")

        self.exit_button: Button = Button(
            self.object_frame, bd=0, image=self.exit_button_image)
        self.exit_button.grid(column=2, row=0, sticky="nsew")
        Hovertip(self.exit_button, "Exit the application")

        # Navigation helpers
        self.previous_menu = [""]
        self.curr_menu = "main_menu"

        # Main menu
        self.network_information_button = Button(
            self.object_frame, bd=0, text="Network Information")
        self.manipulation_button = Button(
            self.object_frame, bd=0, text="Component Manipulation")

        # Main menu/Component manipulation menu
        self.placement_button = Button(
            self.object_frame, bd=0, text="Component Placement")
        self.config_button = Button(
            self.object_frame, bd=0, text="Component Configuration")
        
        # Main menu/Network information menu
        self.hosts_button = Button(self.object_frame, bd=0, text="Hosts")
        self.routers_button = Button(self.object_frame, bd=0, text="Routers")
        self.connections_button = Button(
            self.object_frame, bd=0, text="Connections")
        self.interfaces_button = Button(
            self.object_frame, bd=0, text="Interfaces")
        self.applications_button = Button(
            self.object_frame, bd=0, text="Applications")

        # Main menu/Component manipulation menu/Component configuration menu
        

        # Main menu/Component manipulation menu/Component placement menu
        self.host_placement_button = Button(
            self.object_frame, bd=0, text="Place Host")
        self.router_placement_button = Button(
            self.object_frame, bd=0, text="Place Router")

        #self.main_menu()
        #self.manipulation_menu()
        #self.network_information_menu()

    # MAIN MENU
    def main_menu(self) -> None:
        self.clear_frame("main_menu", state="disabled")

        self.object_frame.rowconfigure((1, 2, 3, 4, 5), weight=1)

        self.network_information_button.grid(
            column=0, row=1, columnspan=3, sticky="nsew")
        self.manipulation_button.grid(
            column=0, row=2, columnspan=3, sticky="nsew")

    # MAIN MENU/NETWORK INFORMATION MENU
    def network_information_menu(self) -> None:
        self.clear_frame("network_information_menu")

        self.object_frame.rowconfigure((1, 2, 3, 4, 5), weight=1)

        self.hosts_button.grid(column=0, row=1, columnspan=3, sticky="nsew")
        self.routers_button.grid(column=0, row=2, columnspan=3, sticky="nsew")
        self.connections_button.grid(
            column=0, row=3, columnspan=3, sticky="nsew")
        self.interfaces_button.grid(
            column=0, row=4, columnspan=3, sticky="nsew")
        self.applications_button.grid(
            column=0, row=5, columnspan=3, sticky="nsew")

    # MAIN MENU/NETWORK INFORMATION MENU/HOSTS MENU
    def hosts_information_menu(self) -> None:
        # Lists every host with their corresponding data
        pass

    # MAIN MENU/NETWORK INFORMATION MENU/ROUTERS MENU
    def routers_information_menu(self) -> None:
        # Lists every router with their corresponding data
        pass

    # MAIN MENU/NETWORK INFORMATION MENU/INTERFACES MENU
    def interfaces_information_menu(self) -> None:
        # Lists every interface with their corresponding data
        pass

    # MAIN MENU/NETWORK INFORMATION MENU/CONNECTIONS MENU
    def connections_information_menu(self) -> None:
        # Lists every connection with their corresponding data
        pass

    # MAIN MENU/NETWORK INFORMATION MENU/APPLICATIONS MENU
    def applications_information_menu(self) -> None:
        # Lists every application with their corresponding data
        pass

    #------------------------------------------------------
    # MAIN MENU/COMPONENT MANIPULATION MENU
    def manipulation_menu(self) -> None:
        self.clear_frame("manipulation_menu")

        self.object_frame.rowconfigure((1, 2, 3, 4, 5), weight=1)
        self.placement_button.grid(
            column=0, row=1, columnspan=3, sticky="nsew")
        self.config_button.grid(
            column=0, row=2, columnspan=3, sticky="nsew")

    # MAIN MENU/COMPONENT MANIPULATION MENU/PLACEMENT MENU
    def placement_menu(self) -> None:
        self.clear_frame("placement_menu")

        self.object_frame.rowconfigure((1, 2, 3, 4, 5), weight=1)

        self.host_placement_button.grid(
            column=0, row=1, columnspan=3, sticky="nsew")
        self.router_placement_button.grid(
            column=0, row=2, columnspan=3, sticky="nsew")

    # MAIN MENU/COMPONENT MANIPULATION MENU/CONFIG MENU
    def config_menu(self) -> None:
        # List of hosts, routers, interfaces - scrollable -> opens up a menu on what to do with the item, and prompts whether you want to change or not
        pass

    def clear_frame(self, curr_menu, state="normal") -> None:
        if len(self.previous_menu) != 0:
            self.previous_menu_button.config(state="normal")
        self.previous_menu.append(self.curr_menu)
        self.curr_menu = curr_menu
        for widget in self.object_frame.winfo_children():
            if widget != self.previous_menu_button and \
               widget != self.exit_button and \
               widget != self.main_menu_button:
                widget.grid_forget()
        self.main_menu_button.config(state=state)

    def handle_previous_menu(self) -> None:
        pass