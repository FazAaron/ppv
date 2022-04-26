"""
This module makes ObjectFrame objects available for use when imported
"""
from pickle import FALSE
from tkinter import (END, SINGLE, Button, Entry, Label, Listbox, PhotoImage,
                     Radiobutton, Text, ttk, Tk)
from tkinter.messagebox import askyesno
from unittest import case

from idlelib.tooltip import Hovertip


class ObjectFrame:
    """
    The window containing a menu for interacting with objects, contained inside \
    the main window's WidgetContainer
    """

    def __init__(self, parent: ttk.Frame, root: Tk) -> None:
        self.root = root
        self.object_frame: ttk.Frame = ttk.Frame(parent)
        self.parent: ttk.Frame = parent
        self.arrow_button_image: PhotoImage = PhotoImage(
            file="resources/left_arrow.png")
        self.exit_button_image: PhotoImage = PhotoImage(
            file="resources/exit_icon.png")
        self.home_button_image: PhotoImage = PhotoImage(
            file="resources/home_icon.png")

        self.object_frame.grid(column=1, row=0, sticky="nsew")

        self.object_frame.columnconfigure((0, 1, 2), weight=1)

        # Main menu
        self.network_information_button: Button = Button(
            self.object_frame, text="Network Information", relief="ridge")
        self.manipulation_button: Button = Button(
            self.object_frame, text="Component Manipulation", relief="ridge")

        # Main menu/Component manipulation menu
        self.placement_button: Button = Button(
            self.object_frame, text="Component Placement", relief="ridge")
        self.config_button: Button = Button(
            self.object_frame, text="Component Configuration", relief="ridge")

        # Main menu/Network information menu
        self.hosts_button: Button = Button(
            self.object_frame, text="Hosts", relief="ridge")
        self.routers_button: Button = Button(
            self.object_frame, text="Routers", relief="ridge")
        self.information_box: Text = Text(
            self.object_frame, bd=0, highlightthickness=0)

        # Main menu/Component manipulation menu/Component configuration menu
        self.item_list: Listbox = Listbox(
            self.object_frame, selectmode=SINGLE, bd=0, highlightthickness=0)
        self.delete_component_button: Button = Button(
            self.object_frame, text="Delete Component", relief="ridge")
        self.set_application_button: Button = Button(
            self.object_frame, text="Set Application on Node", relief="ridge")
        self.start_sending_button: Button = Button(
            self.object_frame, text="Start Sending from Node", relief="ridge")
        self.add_interface_button: Button = Button(
            self.object_frame, text="Add Interface to Node", relief="ridge")
        self.delete_interface_button: Button = Button(
            self.object_frame, text="Delete Interface from Node", relief="ridge")
        self.connect_button: Button = Button(
            self.object_frame, text="Connect to Node", relief="ridge")
        self.disconnect_button: Button = Button(
            self.object_frame, text="Disconnect Interface on Node", relief="ridge")

        # Main menu/Component manipulation menu/component configuration menu/set application menu
        self.app_name_label: Label = Label(
            self.object_frame, text="Application name", relief="ridge")
        self.app_name_entry: Entry = Entry(self.object_frame)

        self.amount_label: Label = Label(
            self.object_frame, text="Packet amount to send", relief="ridge")
        self.amount_entry: Entry = Entry(self.object_frame)

        self.send_rate_label: Label = Label(
            self.object_frame, text="Send rate", relief="ridge")
        self.send_rate_entry: Entry = Entry(self.object_frame)

        self.app_type_label: Label = Label(
            self.object_frame, text="Application type", relief="ridge")
        self.app_type_radio_1: Radiobutton = Radiobutton(
            self.object_frame, text="CONST")
        self.app_type_radio_2: Radiobutton = Radiobutton(
            self.object_frame, text="AIMD")

        # MAIN MENU/COMPONENT MANIPULATION MENU/CONFIG MENU/START SENDING BUTTON
        self.name_or_ip_label: Label = Label(
            self.object_frame, text="Target Host name or IP", relief="ridge")
        self.name_or_ip_entry: Entry = Entry(self.object_frame)

        # MAIN MENU/COMPONENT MANIPULATION MENU/CONFIG MENU/ADD INTERFACE BUTTON
        self.add_interface_name_label: Label = Label(
            self.object_frame, text="Interface name", relief="ridge")
        self.add_interface_name_entry: Entry = Entry(self.object_frame)

        # MAIN MENU/COMPONENT MANIPULATION MENU/CONFIG MENU/DELETE INTERFACE BUTTON
        self.delete_interface_name_label: Label = Label(
            self.object_frame, text="Interface name", relief="ridge")
        self.delete_interface_name_entry: Entry = Entry(self.object_frame)

        # MAIN MENU/COMPONENT MANIPULATION MENU/CONFIG MENU/CONNECT TO NODE BUTTON
        self.connect_name_or_ip_label: Label = Label(
            self.object_frame, text="Target Node name or IP", relief="ridge")
        self.connect_name_or_ip_entry: Entry = Entry(self.object_frame)

        self.self_interface_label: Label = Label(
            self.object_frame, text="Interface on the Node", relief="ridge")
        self.self_interface_entry: Entry = Entry(self.object_frame)

        self.other_interface_label: Label = Label(
            self.object_frame, text="Interface on the other Node", relief="ridge")
        self.other_interface_entry: Entry = Entry(self.object_frame)

        self.speed_label: Label = Label(
            self.object_frame, text="Link speed", relief="ridge")
        self.speed_entry: Entry = Entry(self.object_frame)

        self.metrics_label: Label = Label(
            self.object_frame, text="Link metrics", relief="ridge")
        self.metrics_entry: Entry = Entry(self.object_frame)

        # MAIN MENU/COMPONENT MANIPULATION MENU/CONFIG MENU/DISCONNECT INTERFACE BUTTON
        self.disconnect_interface_name_label: Label = Label(
            self.object_frame, text="Interface name", relief="ridge")
        self.disconnect_interface_name_entry: Entry = Entry(self.object_frame)

        # Main menu/Component manipulation menu/Component placement menu
        self.host_placement_button: Button = Button(
            self.object_frame, text="Place Host", relief="ridge")
        self.router_placement_button: Button = Button(
            self.object_frame, text="Place Router", relief="ridge")

        # Main menu/Component manipulation menu/Component placement menu/Host and Router placement button
        self.menu_information_label = Label(self.object_frame)

        self.name_label = Label(
            self.object_frame, relief="ridge")
        self.name_entry = Entry(self.object_frame)
        self.ip_label = Label(
            self.object_frame, text="IP address", relief="ridge")
        self.ip_entry = Entry(self.object_frame)

        self.buffer_size_label = Label(
            self.object_frame, text="Buffer size", relief="ridge")
        self.buffer_size_entry = Entry(self.object_frame)

        # Generic submit / cancel buttons
        self.submit: Button = Button(
            self.object_frame, text="Submit", bg="royalblue")
        self.cancel: Button = Button(
            self.object_frame, text="Cancel", bg="royalblue")

        # Buttons for navigation
        self.previous_menu_button: Button = Button(
            self.object_frame, image=self.arrow_button_image, state="disabled")
        self.previous_menu_button.grid(column=0, row=0, sticky="nsew")
        Hovertip(self.previous_menu_button, "Return to the previous menu")

        self.main_menu_button: Button = Button(
            self.object_frame, image=self.home_button_image)
        self.main_menu_button.grid(column=1, row=0, sticky="nsew")
        Hovertip(self.main_menu_button, "Go to the main menu")

        self.exit_button: Button = Button(
            self.object_frame, image=self.exit_button_image)
        self.exit_button.grid(column=2, row=0, sticky="nsew")
        Hovertip(self.exit_button, "Exit the application")

        # Navigation helpers
        self.previous_menu = []
        self.curr_menu = "main_menu"

        self.main_menu(False)

    # _______________________________________________________________
    # _______________________________________________________________
    # MAIN MENU
    def main_menu(self, save_as_previous=True) -> None:
        self.__clear_frame("main_menu", save_as_previous, state="disabled")

        self.menu_information_label.config(
            text="Main menu", font=("Arial", 14))
        self.menu_information_label.grid(
            column=0, row=1, columnspan=3, sticky="nsew")

        self.object_frame.rowconfigure(1, weight=1)
        self.object_frame.rowconfigure((2, 3, 4, 5, 6), weight=2)

        self.network_information_button.grid(
            column=0, row=2, columnspan=3, sticky="nsew")
        self.manipulation_button.grid(
            column=0, row=3, columnspan=3, sticky="nsew")

    # _______________________________________________________________
    # _______________________________________________________________
    # MAIN MENU/NETWORK INFORMATION MENU
    def network_information_menu(self, save_as_previous=True) -> None:
        self.__clear_frame("network_information_menu", save_as_previous)

        self.menu_information_label.config(
            text="Network information", font=("Arial", 14))
        self.menu_information_label.grid(
            column=0, row=1, columnspan=3, sticky="nsew")

        self.object_frame.rowconfigure(1, weight=1)
        self.object_frame.rowconfigure((2, 3, 4, 5, 6), weight=2)

        self.hosts_button.grid(column=0, row=2, columnspan=3, sticky="nsew")
        self.routers_button.grid(column=0, row=3, columnspan=3, sticky="nsew")

    # MAIN MENU/NETWORK INFORMATION MENU/HOSTS MENU
    def hosts_information_menu(self, save_as_previous=True) -> None:
        self.__clear_frame("hosts_information_menu", save_as_previous)

        self.object_frame.rowconfigure(1, weight=1)
        self.object_frame.rowconfigure(2, weight=5)

        self.menu_information_label.config(
            text="Host information in the Network", font=("Arial", 18))
        self.menu_information_label.grid(
            column=0, row=1, columnspan=3, sticky="nsew")

        self.information_box.grid(column=0, row=2, columnspan=3, sticky="nsew")
        # for _ in range(1, 100):
        #self.information_box.insert(END, "multiline\ntest")
        #self.information_box.insert(END, "\n---\n")
        # self.information_box.config(state="disabled")

    # MAIN MENU/NETWORK INFORMATION MENU/ROUTERS MENU
    def routers_information_menu(self, save_as_previous=True) -> None:
        self.__clear_frame("routers_information_menu", save_as_previous)

        self.object_frame.rowconfigure(1, weight=1)
        self.object_frame.rowconfigure(2, weight=5)

        self.menu_information_label.config(
            text="Router information in the Network", font=("Arial", 18))
        self.menu_information_label.grid(
            column=0, row=1, columnspan=3, sticky="nsew")

        self.object_frame.rowconfigure(1, weight=1)
        self.information_box.grid(column=0, row=2, columnspan=3, sticky="nsew")
        # for _ in range(1, 100):
        #self.information_box.insert(END, "multiline\ntest")
        #self.information_box.insert(END, "\n---\n")
        # self.information_box.config(state="disabled")
    # _______________________________________________________________
    # _______________________________________________________________
    # MAIN MENU/COMPONENT MANIPULATION MENU

    def manipulation_menu(self, save_as_previous=True) -> None:
        self.__clear_frame("manipulation_menu", save_as_previous)

        self.menu_information_label.config(
            text="Manipulate Network components", font=("Arial", 18))
        self.menu_information_label.grid(
            column=0, row=1, columnspan=3, sticky="nsew")

        self.object_frame.rowconfigure(1, weight=1)
        self.object_frame.rowconfigure((2, 3, 4, 5, 6), weight=2)

        self.placement_button.grid(
            column=0, row=2, columnspan=3, sticky="nsew")
        self.config_button.grid(
            column=0, row=3, columnspan=3, sticky="nsew")

    # _______________________________________________________________
    # _______________________________________________________________
    # MAIN MENU/COMPONENT MANIPULATION MENU/PLACEMENT MENU
    def placement_menu(self, save_as_previous=True) -> None:
        self.__clear_frame("placement_menu", save_as_previous)

        self.object_frame.rowconfigure(1, weight=1)
        self.object_frame.rowconfigure((2, 3, 4, 5, 6), weight=2)

        self.menu_information_label.config(
            text="Place Network components", font=("Arial", 18))
        self.menu_information_label.grid(
            column=0, row=1, columnspan=3, sticky="nsew")

        self.host_placement_button.grid(
            column=0, row=2, columnspan=3, sticky="nsew")
        self.router_placement_button.grid(
            column=0, row=3, columnspan=3, sticky="nsew")

    def host_placement_menu(self, save_as_previous=True) -> None:
        self.__clear_frame("host_placement_menu", save_as_previous)

        self.object_frame.rowconfigure((1, 2, 3, 4, 5), weight=1)

        self.menu_information_label.config(
            text="Add a Host to the Network", font=("Arial", 18))
        self.menu_information_label.grid(
            column=0, row=1, columnspan=3, sticky="nsew")

        self.name_label.config(text="Host name")
        self.name_label.grid(column=0, row=2, sticky="nsew")
        self.name_entry.grid(column=1, row=2, columnspan=2, sticky="nsew")

        self.ip_label.grid(column=0, row=3, sticky="nsew")
        self.ip_entry.grid(column=1, row=3, columnspan=2, sticky="nsew")

        self.send_rate_label.grid(column=0, row=4, sticky="nsew")
        self.send_rate_entry.grid(column=1, row=4, columnspan=2, sticky="nsew")

        self.submit.grid(column=0, row=5, columnspan=2, sticky="sw")
        self.cancel.grid(column=2, row=5, sticky="se")

    def router_placement_menu(self, save_as_previous=True) -> None:
        self.__clear_frame("router_placement_menu", save_as_previous)

        self.object_frame.rowconfigure((1, 2, 3, 4, 5, 6), weight=1)

        self.menu_information_label.config(
            text="Add a Router to the Network", font=("Arial", 18))
        self.menu_information_label.grid(
            column=0, row=1, columnspan=3, sticky="nsew")

        self.name_label.config(text="Router name")
        self.name_label.grid(column=0, row=2, sticky="nsew")
        self.name_entry.grid(column=1, row=2, columnspan=2, sticky="nsew")

        self.ip_label.grid(column=0, row=3, sticky="nsew")
        self.ip_entry.grid(column=1, row=3, columnspan=2, sticky="nsew")

        self.send_rate_label.grid(column=0, row=4, sticky="nsew")
        self.send_rate_entry.grid(column=1, row=4, columnspan=2, sticky="nsew")

        self.buffer_size_label.grid(column=0, row=5, sticky="nsew")
        self.buffer_size_entry.grid(
            column=1, row=5, columnspan=2, sticky="nsew")

        self.submit.grid(column=0, row=6, columnspan=2, sticky="sw")
        self.cancel.grid(column=2, row=6, sticky="se")

    # _______________________________________________________________
    # _______________________________________________________________
    # MAIN MENU/COMPONENT MANIPULATION MENU/CONFIG MENU
    def config_menu(self, save_as_previous=True) -> None:
        self.__clear_frame("config_menu", save_as_previous)

        self.object_frame.rowconfigure(
            (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11), weight=1)

        self.menu_information_label.config(
            text="Configure Network components", font=("Arial", 18))
        self.menu_information_label.grid(
            column=0, row=1, columnspan=3, sticky="nsew")

        self.item_list.grid(column=0, row=2, columnspan=3,
                            rowspan=4, sticky="nsew")
        self.delete_component_button.grid(
            column=0, row=6, columnspan=3, sticky="nsew")
        self.set_application_button.grid(
            column=0, row=7, columnspan=3, sticky="nsew")
        self.start_sending_button.grid(
            column=0, row=8, columnspan=3, sticky="nsew")
        self.add_interface_button.grid(
            column=0, row=9, columnspan=3, sticky="nsew")
        self.delete_interface_button.grid(
            column=0, row=10, columnspan=3, sticky="nsew")
        self.connect_button.grid(column=0, row=10, columnspan=3, sticky="nsew")
        self.disconnect_button.grid(
            column=0, row=11, columnspan=3, sticky="nsew")

    # MAIN MENU/COMPONENT MANIPULATION MENU/CONFIG MENU/SET APPLICATION BUTTON
    def set_application_menu(self, save_as_previous=True) -> None:
        self.__clear_frame("set_application_menu", save_as_previous)

        self.object_frame.rowconfigure((1, 2, 3, 4, 5, 6, 7, 8), weight=1)

        self.menu_information_label.config(
            text="Set the Application on the Host", font=("Arial", 18))
        self.menu_information_label.grid(
            column=0, row=1, columnspan=3, sticky="nsew")

        self.app_name_label.grid(column=0, row=2, sticky="nsew")
        self.app_name_entry.grid(column=1, row=2, columnspan=2, sticky="nsew")

        self.amount_label.grid(column=0, row=3, sticky="nsew")
        self.amount_entry.grid(column=1, row=3, columnspan=2, sticky="nsew")

        self.send_rate_label.grid(column=0, row=4, sticky="nsew")
        self.send_rate_entry.grid(column=1, row=4, columnspan=2, sticky="nsew")

        self.app_type_label.grid(column=0, row=5, columnspan=3, sticky="nsew")
        self.app_type_radio_1.grid(
            column=0, row=6, columnspan=3, sticky="nsew")
        self.app_type_radio_2.grid(
            column=0, row=7, columnspan=3, sticky="nsew")

        self.submit.grid(column=0, row=8, columnspan=2, sticky="sw")
        self.cancel.grid(column=2, row=8, sticky="se")

    # MAIN MENU/COMPONENT MANIPULATION MENU/CONFIG MENU/START SENDING BUTTON
    def start_sending_menu(self, save_as_previous=True) -> None:
        self.__clear_frame("start_sending_menu", save_as_previous)
        self.object_frame.rowconfigure((1, 2), weight=1)
        self.object_frame.rowconfigure(3, weight=40)

        self.menu_information_label.config(
            text="Start sending to an other Host", font=("Arial", 18))
        self.menu_information_label.grid(
            column=0, row=1, columnspan=3, sticky="nsew")

        self.name_or_ip_label.grid(column=0, row=2, sticky="nsew")
        self.name_or_ip_entry.grid(
            column=1, row=2, columnspan=2, sticky="nsew")

        self.submit.grid(column=0, row=3, columnspan=2, sticky="sw")
        self.cancel.grid(column=2, row=3, sticky="se")

    # MAIN MENU/COMPONENT MANIPULATION MENU/CONFIG MENU/ADD INTERFACE BUTTON
    def add_interface_menu(self, save_as_previous=True) -> None:
        self.__clear_frame("add_interface_menu", save_as_previous)
        
        self.object_frame.rowconfigure((1, 2), weight=1)
        self.object_frame.rowconfigure(3, weight=40)

        self.menu_information_label.config(
            text="Add an Interface to the Node", font=("Arial", 18))
        self.menu_information_label.grid(
            column=0, row=1, columnspan=3, sticky="nsew")

        self.add_interface_name_label.grid(column=0, row=2, sticky="nsew")
        self.add_interface_name_entry.grid(
            column=1, row=2, columnspan=2, sticky="nsew")

        self.submit.grid(column=0, row=3, columnspan=2, sticky="sw")
        self.cancel.grid(column=2, row=3, sticky="se")

    # MAIN MENU/COMPONENT MANIPULATION MENU/CONFIG MENU/DELETE INTERFACE BUTTON
    def delete_interface_menu(self, save_as_previous=True) -> None:
        self.__clear_frame("delete_interface_menu", save_as_previous)
        self.object_frame.rowconfigure((1, 2), weight=1)
        self.object_frame.rowconfigure(3, weight=40)

        self.menu_information_label.config(
            text="Delete an Interface from the Node", font=("Arial", 18))
        self.menu_information_label.grid(
            column=0, row=1, columnspan=3, sticky="nsew")

        self.delete_interface_name_label.grid(column=0, row=2, sticky="nsew")
        self.delete_interface_name_entry.grid(
            column=1, row=2, columnspan=2, sticky="nsew")

        self.submit.grid(column=0, row=3, columnspan=2, sticky="sw")
        self.cancel.grid(column=2, row=3, sticky="se")

    # MAIN MENU/COMPONENT MANIPULATION MENU/CONFIG MENU/CONNECT TO NODE BUTTON
    def connect_menu(self, save_as_previous=True) -> None:
        self.__clear_frame("connect_menu", save_as_previous)
        self.object_frame.rowconfigure(1, weight=1)
        self.object_frame.rowconfigure((2, 3, 4, 5, 6, 7), weight=1)

        self.menu_information_label.config(
            text="Connect to an other Node", font=("Arial", 18))
        self.menu_information_label.grid(
            column=0, row=1, columnspan=3, sticky="nsew")

        self.connect_name_or_ip_label.grid(column=0, row=2, sticky="nsew")
        self.connect_name_or_ip_entry.grid(
            column=1, row=2, columnspan=2, sticky="nsew")

        self.self_interface_label.grid(column=0, row=3, sticky="nsew")
        self.self_interface_entry.grid(
            column=1, row=3, columnspan=2, sticky="nsew")

        self.other_interface_label.grid(column=0, row=4, sticky="nsew")
        self.other_interface_entry.grid(
            column=1, row=4, columnspan=2, sticky="nsew")

        self.speed_label.grid(column=0, row=5, sticky="nsew")
        self.speed_entry.grid(column=1, row=5, columnspan=2, sticky="nsew")

        self.metrics_label.grid(column=0, row=6, sticky="nsew")
        self.metrics_entry.grid(column=1, row=6, columnspan=2, sticky="nsew")

        self.submit.grid(column=0, row=7, columnspan=2, sticky="sw")
        self.cancel.grid(column=2, row=7, sticky="se")

    # MAIN MENU/COMPONENT MANIPULATION MENU/CONFIG MENU/DISCONNECT INTERFACE BUTTON
    def disconnect_interface_menu(self, save_as_previous=True) -> None:
        self.__clear_frame("disconnect_interface_menu", save_as_previous)

        self.object_frame.rowconfigure((1, 2), weight=1)
        self.object_frame.rowconfigure(3, weight=40)

        self.menu_information_label.config(
            text="Disconnect an Interface", font=("Arial", 18))
        self.menu_information_label.grid(
            column=0, row=1, columnspan=3, sticky="nsew")

        self.disconnect_interface_name_label.grid(
            column=0, row=2, sticky="nsew")
        self.disconnect_interface_name_entry.grid(
            column=1, row=2, columnspan=2, sticky="nsew")

        self.submit.grid(column=0, row=3, columnspan=2, sticky="sw")
        self.cancel.grid(column=2, row=3, sticky="se")

    # _______________________________________________________________
    # _______________________________________________________________

    # _______________________________________________________________
    # _______________________________________________________________
    # MAIN MENU/COMPONENT MANIPULATION MENU/CONFIG MENU/DELETE BUTTON
    def disconnect_prompt(self) -> bool:
        answer: bool = askyesno(title="Disconnect interface",
                                message="Are you sure you want to disconnect the interface?\nBoth sides of the connection will be disconnected.")
        return answer

    # MAIN MENU/COMPONENT MANIPULATION MENU/CONFIG MENU/DELETE COMPONENT AND INTERFACE BUTTON
    def deletion_prompt(self) -> bool:
        answer: bool = askyesno(title="Delete item",
                                message="Are you sure you want to delete this item?")
        return answer

    def exit_prompt(self) -> bool:
        answer: bool = askyesno(title="Exit application",
                                message="Are you sure you want to quit the application?")
        return answer
    # _______________________________________________________________
    # _______________________________________________________________

    def __clear_frame(self, curr_menu, save_as_previous, state="normal") -> None:
        if save_as_previous:
            self.previous_menu.append(self.curr_menu)
        self.curr_menu = curr_menu
        if len(self.previous_menu) != 0:
            self.previous_menu_button.config(state="normal")
        for widget in self.object_frame.winfo_children():
            if widget != self.previous_menu_button and \
               widget != self.exit_button and \
               widget != self.main_menu_button:
                widget.grid_forget()
        self.main_menu_button.config(state=state)

    def return_to_previous(self) -> None:
        previous_item = self.previous_menu.pop()
        if (len(self.previous_menu) == 0):
            self.previous_menu_button.config(state="disabled")
        if previous_item == "main_menu":
            self.main_menu(False)
        elif previous_item == "network_information_menu":
            self.network_information_menu(False)
        elif previous_item == "hosts_information_menu":
            self.hosts_information_menu(False)
        elif previous_item == "routers_information_menu":
            self.routers_information_menu(False)
        elif previous_item == "manipulation_menu":
            self.manipulation_menu(False)
        elif previous_item == "placement_menu":
            self.placement_menu(False)
        elif previous_item == "host_placement_menu":
            self.host_placement_menu(False)
        elif previous_item == "router_placement_menu":
            self.router_placement_menu(False)
        elif previous_item == "config_menu":
            self.config_menu(False)
        elif previous_item == "set_application_menu":
            self.set_application_menu(False)
        elif previous_item == "start_sending_menu":
            self.start_sending_menu(False)
        elif previous_item == "add_interface_menu":
            self.add_interface_menu(False)
        elif previous_item == "delete_interface_menu":
            self.delete_interface_menu(False)
        elif previous_item == "connect_menu":
            self.connect_menu(False)
        elif previous_item == "disconnect_interface_menu":
            self.disconnect_interface_menu(False)
        else:
            self.main_menu(False)

    def return_to_main_menu(self) -> None:
        self.previous_menu = []
        self.previous_menu_button.config(state="disabled")
        self.main_menu(False)

    def exit(self) -> None:
        if self.exit_prompt():
            self.root.destroy()