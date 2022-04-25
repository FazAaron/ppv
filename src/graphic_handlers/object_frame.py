"""
This module makes ObjectFrame objects available for use when imported
"""
from tkinter import END, SINGLE, Button, Listbox, PhotoImage, Text, ttk
from tkinter.messagebox import askyesno
from turtle import back

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
        s = ttk.Style()
        bg = s.lookup("TFrame", "background")
        self.information_box = Text(self.object_frame, background=bg)

        # Main menu/Component manipulation menu/Component configuration menu
        self.item_list = Listbox(
            self.object_frame, selectmode=SINGLE, bd=0, highlightthickness=0)
        self.delete_button = Button(
            self.object_frame, bd=0, text="Delete Component")
        self.set_application_button = Button(
            self.object_frame, bd=0, text="Set Application on Node")
        self.start_sending_button = Button(
            self.object_frame, bd=0, text="Start Sending from Node")
        self.add_interface_button = Button(
            self.object_frame, bd=0, text="Add Interface to Node")
        self.connect_button = Button(
            self.object_frame, bd=0, text="Connect to Node")
        self.disconnect_button = Button(
            self.object_frame, bd=0, text="Disconnect Interface")

        # Main menu/Component manipulation menu/Component placement menu
        self.host_placement_button = Button(
            self.object_frame, bd=0, text="Place Host")
        self.router_placement_button = Button(
            self.object_frame, bd=0, text="Place Router")

        # self.main_menu()
        # self.manipulation_menu()
        # self.network_information_menu()
        # self.config_menu()
        # self.disconnect_prompt()
        self.hosts_information_menu()

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
        self.clear_frame("hosts_information_menu")

        self.object_frame.rowconfigure(1, weight=1)
        self.information_box.grid(column=0, row=1, columnspan=3, sticky="nsew")
        for _ in range(1, 100):
            self.information_box.insert(END, "multiline\ntest")
            self.information_box.insert(END, "\n---\n")
        self.information_box.config(state="disabled")

        # Lists every host with their corresponding data

    # MAIN MENU/NETWORK INFORMATION MENU/ROUTERS MENU
    def routers_information_menu(self) -> None:
        self.clear_frame("routers_information_menu")

        self.object_frame.rowconfigure(1, weight=1)
        self.information_box.grid(column=0, row=1, columnspan=3, sticky="nsew")
        for _ in range(1, 100):
            self.information_box.insert(END, "multiline\ntest")
            self.information_box.insert(END, "\n---\n")
        self.information_box.config(state="disabled")

    # MAIN MENU/NETWORK INFORMATION MENU/INTERFACES MENU
    def interfaces_information_menu(self) -> None:
        self.clear_frame("interfaces_information_menu")

        self.object_frame.rowconfigure(1, weight=1)
        self.information_box.grid(column=0, row=1, columnspan=3, sticky="nsew")
        for _ in range(1, 100):
            self.information_box.insert(END, "multiline\ntest")
            self.information_box.insert(END, "\n---\n")
        self.information_box.config(state="disabled")

    # MAIN MENU/NETWORK INFORMATION MENU/CONNECTIONS MENU
    def connections_information_menu(self) -> None:
        self.clear_frame("connections_information_menu")

        self.object_frame.rowconfigure(1, weight=1)
        self.information_box.grid(column=0, row=1, columnspan=3, sticky="nsew")
        for _ in range(1, 100):
            self.information_box.insert(END, "multiline\ntest")
            self.information_box.insert(END, "\n---\n")
        self.information_box.config(state="disabled")

    # MAIN MENU/NETWORK INFORMATION MENU/APPLICATIONS MENU
    def applications_information_menu(self) -> None:
        self.clear_frame("applications_information_menu")

        self.object_frame.rowconfigure(1, weight=1)
        self.information_box.grid(column=0, row=1, columnspan=3, sticky="nsew")
        for _ in range(1, 100):
            self.information_box.insert(END, "multiline\ntest")
            self.information_box.insert(END, "\n---\n")
        self.information_box.config(state="disabled")

    # ------------------------------------------------------
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
        self.clear_frame("config_menu")

        self.object_frame.rowconfigure(
            (1, 2, 3, 4, 5, 6, 7, 8, 9, 10), weight=1)

        self.item_list.grid(column=0, row=1, columnspan=3,
                            rowspan=4, sticky="nsew")
        self.delete_button.grid(column=0, row=5, columnspan=3, sticky="nsew")
        self.set_application_button.grid(
            column=0, row=6, columnspan=3, sticky="nsew")
        self.start_sending_button.grid(
            column=0, row=7, columnspan=3, sticky="nsew")
        self.add_interface_button.grid(
            column=0, row=8, columnspan=3, sticky="nsew")
        self.connect_button.grid(column=0, row=9, columnspan=3, sticky="nsew")
        self.disconnect_button.grid(
            column=0, row=10, columnspan=3, sticky="nsew")

    def deletion_prompt(self) -> bool:
        answer: bool = askyesno(title="Delete component",
                                message="Are you sure you want to delete this component?")
        return answer

    def disconnect_prompt(self) -> bool:
        answer: bool = askyesno(title="Disconnect interface",
                                message="Are you sure you want to disconnect the interface?\nBoth sides of the connection will be disconnected.")
        return answer

    def exit_prompt(self) -> bool:
        answer: bool = askyesno(title="Exit application",
                                message="Are you sure you want to quit the application?")
        return answer

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
