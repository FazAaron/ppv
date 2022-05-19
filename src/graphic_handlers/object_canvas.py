"""
This module makes ObjectCanvas objects available for use when imported
"""
from tkinter import Button, Canvas, Entry, Label, Menu, ttk
from turtle import bgcolor
from typing import Callable, Tuple


class ObjectCanvas:
    """
    The canvas to 'draw' to, contained inside the main window's WidgetContainer

    Data members:
    canvas              (Canvas): The canvas to draw to
    network_config_menu (Menu): The Menu for configuring the Network
    host_config_menu    (Menu): The Menu to configure a Host
    router_config_menu  (Menu): The Menu to configure a Router
    config_menu         (ttk.Frame): The Frame to access certain features of \
                                     the Network
    submit_button       (Button): The Button to be used for submission inside \
                                  the config_menu
    cancel_button       (Button): The Button to be used for cancellation inside \
                                  the config_menu
    label_[1..5]        (Label): The Labels to be used inside the config_menu
    entry_[1..5]        (Entry): The Entries to be used inside the config_menu
    """

    def __init__(self, parent: ttk.Frame) -> None:
        self.canvas: Canvas = Canvas(
            parent, background="lightgrey", bd=1, highlightthickness=1, relief="ridge")

        # Pop-up menus
        self.network_config_menu: Menu = self.__setup_network_config_menu()
        self.host_config_menu: Menu = self.__setup_host_config_menu()
        self.router_config_menu: Menu = self.__setup_router_config_menu()

        # Frame that is opened after clicking an option in the pop-up menu
        self.config_frame: ttk.Frame = ttk.Frame(self.canvas, relief="ridge")

        # The Frame's inner Widgets - initial state
        font: Tuple[str, int] = ("JetBrainsMono NF", 8)
        self.submit_button: Button = Button(
            self.config_frame, text="Submit", font=font)
        self.cancel_button: Button = Button(
            self.config_frame, text="Cancel", font=font)

        self.title_label: Label = Label(
            self.config_frame, text="Title Label", font=font)
        self.information_label: Label = Label(
            self.config_frame, text="Information Label", font=font)

        self.label_1: Label = Label(
            self.config_frame, text="First Label", relief="ridge", font=font)
        self.entry_1: Entry = Entry(self.config_frame, state="disabled")

        self.label_2: Label = Label(
            self.config_frame, text="Second Label", relief="ridge", font=font)
        self.entry_2: Entry = Entry(self.config_frame, state="disabled")

        self.label_3: Label = Label(
            self.config_frame, text="Third Label", relief="ridge", font=font)
        self.entry_3: Entry = Entry(self.config_frame, state="disabled")

        self.label_4: Label = Label(
            self.config_frame, text="Fourth Label", relief="ridge", font=font)
        self.entry_4: Entry = Entry(self.config_frame, state="disabled")

        self.label_5: Label = Label(
            self.config_frame, text="Fifth Label", relief="ridge", font=font)
        self.entry_5: Entry = Entry(self.config_frame, state="disabled")

        # Set the position of this Frame inside the parent container
        self.canvas.grid(column=0, row=0, sticky="nsew")

    def get_geometry(self) -> Tuple[int, int]:
        return (self.canvas.winfo_width(), self.canvas.winfo_height())

    def bind(self, event_type: str, func: Callable) -> None:
        self.canvas.bind(event_type, func, add="+")

    def draw_component(self, x: int, y: int, width: int, height: int, component_type: str) -> int:
        item_id: int = -1
        if component_type.upper() == "ROUTER":
            item_id = self.canvas.create_rectangle(
                x, y, x + width, y + height, fill="lightblue")
        elif component_type.upper() == "HOST":
            item_id = self.canvas.create_rectangle(
                x, y, x + width, y + height, fill="grey")
        return item_id

    def draw_link(self, x1: int, y1: int, x2: int, y2: int) -> int:
        return self.canvas.create_line(x1, y1, x2, y2, fill="grey", width="2")

    def draw_interface(self, x: int, y: int, width: int, height: int) -> int:
        return self.canvas.create_rectangle(x, y, x + width, y + height, fill="white")

    def draw_string(self, x: int, y: int, text: str) -> None:
        self.canvas.create_text(x, y, text=text, anchor="e")

    def clear_canvas(self) -> None:
        self.canvas.delete("all")

    def after(self, time: int, func: Callable) -> None:
        self.canvas.after(time, func)

    def __setup_network_config_menu(self) -> Menu:
        network_config_menu = Menu(self.canvas, tearoff=0)
        network_config_menu.add_command(label="Place Host")
        network_config_menu.add_command(label="Place Router")
        network_config_menu.add_separator()
        network_config_menu.add_command(label="Close")
        return network_config_menu

    def __setup_host_config_menu(self) -> Menu:
        host_config_menu = Menu(self.canvas, tearoff=0)
        host_config_menu.add_command(label="Add Interface")
        host_config_menu.add_command(label="Delete Interface")
        host_config_menu.add_command(label="Set Application")
        host_config_menu.add_command(label="Start sending")
        host_config_menu.add_command(label="Connect to Node")
        host_config_menu.add_command(label="Disconnect Interface")
        host_config_menu.add_command(label="Delete Component")
        host_config_menu.add_separator()
        host_config_menu.add_command(label="Close")
        return host_config_menu

    def __setup_router_config_menu(self) -> Menu:
        router_config_menu = Menu(self.canvas, tearoff=0)
        router_config_menu.add_command(label="Add Interface")
        router_config_menu.add_command(label="Delete Interface")
        router_config_menu.add_command(label="Connect to Node")
        router_config_menu.add_command(label="Disconnect Interface")
        router_config_menu.add_command(label="Delete Component")
        router_config_menu.add_separator()
        router_config_menu.add_command(label="Close")
        return router_config_menu

    def show_menu(self, menu: Menu, x: int, y: int) -> None:
        try:
            menu.tk_popup(x, y)
        finally:
            menu.grab_release()

    def setup_place_host_frame(self, x: int, y: int) -> None:
        self.config_frame.place(x=x, y=y, width=350, height=350)

        self.title_label.config(text="Place Host")
        self.information_label.config(text=("Host Name:\nbetween 1 and 15 characters"
                                            "\nIP address:\n[0-255].[0-255].[0-255].[0-255]"
                                            "\nSend Rate:\n1-99"), fg="black")

        self.label_1.config(text="Host Name")
        self.entry_1.config(state="normal")

        self.label_2.config(text="IP Address")
        self.entry_2.config(state="normal")

        self.label_3.config(text="Send Rate")
        self.entry_3.config(state="normal")

        self.label_1.place(relx=0.0, rely=0.0, relwidth=0.5, relheight=0.1)
        self.entry_1.place(relx=0.5, rely=0.0, relwidth=0.5, relheight=0.1)

        self.label_2.place(relx=0.0, rely=0.1, relwidth=0.5, relheight=0.1)
        self.entry_2.place(relx=0.5, rely=0.1, relwidth=0.5, relheight=0.1)

        self.label_3.place(relx=0.0, rely=0.2, relwidth=0.5, relheight=0.1)
        self.entry_3.place(relx=0.5, rely=0.2, relwidth=0.5, relheight=0.1)

        self.information_label.place(
            relx=0.1, rely=0.4, relwidth=0.8, relheight=0.5)

        self.submit_button.place(
            relx=0.0, rely=0.9, relwidth=0.25, relheight=0.1)
        self.cancel_button.place(
            relx=0.75, rely=0.9, relwidth=0.25, relheight=0.1)
        self.title_label.place(relx=0.25, rely=0.9,
                               relwidth=0.5, relheight=0.1)

    def setup_place_router_frame(self, x: int, y: int) -> None:
        self.config_frame.place(x=x, y=y, width=350, height=350)

        self.title_label.config(text="Place Router")
        self.information_label.config(text=("Router Name:\nbetween 1 and 15 characters"
                                            "\nIP address:\n[0-255].[0-255].[0-255].[0-255]"
                                            "\nSend Rate: 1-99"
                                            "\nBuffer Size: 1-99"), fg="black")

        self.label_1.config(text="Router Name")
        self.entry_1.config(state="normal")

        self.label_2.config(text="IP Address")
        self.entry_2.config(state="normal")

        self.label_3.config(text="Send Rate")
        self.entry_3.config(state="normal")

        self.label_4.config(text="Buffer size")
        self.entry_4.config(state="normal")

        self.label_1.place(relx=0.0, rely=0.0, relwidth=0.5, relheight=0.1)
        self.entry_1.place(relx=0.5, rely=0.0, relwidth=0.5, relheight=0.1)

        self.label_2.place(relx=0.0, rely=0.1, relwidth=0.5, relheight=0.1)
        self.entry_2.place(relx=0.5, rely=0.1, relwidth=0.5, relheight=0.1)

        self.label_3.place(relx=0.0, rely=0.2, relwidth=0.5, relheight=0.1)
        self.entry_3.place(relx=0.5, rely=0.2, relwidth=0.5, relheight=0.1)

        self.label_4.place(relx=0.0, rely=0.3, relwidth=0.5, relheight=0.1)
        self.entry_4.place(relx=0.5, rely=0.3, relwidth=0.5, relheight=0.1)

        self.information_label.place(
            relx=0.1, rely=0.4, relwidth=0.8, relheight=0.5)

        self.submit_button.place(
            relx=0.0, rely=0.9, relwidth=0.25, relheight=0.1)
        self.cancel_button.place(
            relx=0.75, rely=0.9, relwidth=0.25, relheight=0.1)
        self.title_label.place(relx=0.25, rely=0.9,
                               relwidth=0.5, relheight=0.1)

    def setup_add_interface_frame(self, x: int, y: int) -> None:
        self.config_frame.place(x=x, y=y, width=350, height=350)

        self.title_label.config(text="Add Interface")
        self.information_label.config(text="Interface Name:\nbetween 1 and 15 characters",
                                      fg="black")

        self.label_1.config(text="Interface name")
        self.entry_1.config(state="normal")

        self.label_1.place(relx=0.0, rely=0.0, relwidth=0.5, relheight=0.1)
        self.entry_1.place(relx=0.5, rely=0.0, relwidth=0.5, relheight=0.1)

        self.information_label.place(
            relx=0.1, rely=0.4, relwidth=0.8, relheight=0.5)

        self.submit_button.place(
            relx=0.0, rely=0.9, relwidth=0.3, relheight=0.1)
        self.cancel_button.place(
            relx=0.7, rely=0.9, relwidth=0.3, relheight=0.1)
        self.title_label.place(relx=0.3, rely=0.9, relwidth=0.4, relheight=0.1)

    def setup_delete_interface_frame(self, x: int, y: int) -> None:
        self.config_frame.place(x=x, y=y, width=350, height=350)

        self.title_label.config(text="Delete Interface")
        self.information_label.config(text="Interface Name:\nbetween 1 and 15 characters",
                                      fg="black")

        self.label_1.config(text="Interface name")
        self.entry_1.config(state="normal")

        self.label_1.place(relx=0.0, rely=0.0, relwidth=0.5, relheight=0.1)
        self.entry_1.place(relx=0.5, rely=0.0, relwidth=0.5, relheight=0.1)

        self.information_label.place(
            relx=0.1, rely=0.4, relwidth=0.8, relheight=0.5)

        self.submit_button.place(
            relx=0.0, rely=0.9, relwidth=0.25, relheight=0.1)
        self.cancel_button.place(
            relx=0.75, rely=0.9, relwidth=0.25, relheight=0.1)
        self.title_label.place(relx=0.25, rely=0.9,
                               relwidth=0.5, relheight=0.1)

    def setup_set_application_frame(self, x: int, y: int) -> None:
        self.config_frame.place(x=x, y=y, width=350, height=350)

        self.title_label.config(text="Set Application")
        self.information_label.config(text=("Application Name:\nbetween 1 and 15 characters"
                                            "\nPacket Amount: 1-99"
                                            "\nSend Rate: 1-99"
                                            "\nApplication Type: CONST/AIMD"), fg="black")

        self.label_1.config(text="Application Name")
        self.entry_1.config(state="normal")

        self.label_2.config(text="Packet Amount")
        self.entry_2.config(state="normal")

        self.label_3.config(text="Send Rate")
        self.entry_3.config(state="normal")

        self.label_4.config(text="Application Type")
        self.entry_4.config(state="normal")

        self.label_1.place(relx=0.0, rely=0.0, relwidth=0.5, relheight=0.1)
        self.entry_1.place(relx=0.5, rely=0.0, relwidth=0.5, relheight=0.1)

        self.label_2.place(relx=0.0, rely=0.1, relwidth=0.5, relheight=0.1)
        self.entry_2.place(relx=0.5, rely=0.1, relwidth=0.5, relheight=0.1)

        self.label_3.place(relx=0.0, rely=0.2, relwidth=0.5, relheight=0.1)
        self.entry_3.place(relx=0.5, rely=0.2, relwidth=0.5, relheight=0.1)

        self.label_4.place(relx=0.0, rely=0.3, relwidth=0.5, relheight=0.1)
        self.entry_4.place(relx=0.5, rely=0.3, relwidth=0.5, relheight=0.1)

        self.information_label.place(
            relx=0.1, rely=0.4, relwidth=0.8, relheight=0.5)

        self.submit_button.place(
            relx=0.0, rely=0.9, relwidth=0.25, relheight=0.1)
        self.cancel_button.place(
            relx=0.75, rely=0.9, relwidth=0.25, relheight=0.1)
        self.title_label.place(relx=0.25, rely=0.9,
                               relwidth=0.5, relheight=0.1)

    def setup_start_sending_frame(self, x: int, y: int) -> None:
        self.config_frame.place(x=x, y=y, width=350, height=350)

        self.title_label.config(text="Start Sending")
        self.information_label.config(text=("Target Host IP or Name:\n"
                                            "[0-255].[0-255].[0-255].[0-255]\nOR\n"
                                            "between 1 and 15 characters"),
                                      fg="black")

        self.label_1.config(text="Target Host IP or Name")
        self.entry_1.config(state="normal")

        self.label_1.place(relx=0.0, rely=0.0, relwidth=0.6, relheight=0.1)
        self.entry_1.place(relx=0.6, rely=0.0, relwidth=0.4, relheight=0.1)

        self.information_label.place(
            relx=0.1, rely=0.4, relwidth=0.8, relheight=0.5)

        self.submit_button.place(
            relx=0.0, rely=0.9, relwidth=0.25, relheight=0.1)
        self.cancel_button.place(
            relx=0.75, rely=0.9, relwidth=0.25, relheight=0.1)
        self.title_label.place(relx=0.25, rely=0.9,
                               relwidth=0.5, relheight=0.1)

    def setup_connect_to_node_frame(self, x: int, y: int) -> None:
        self.config_frame.place(x=x, y=y, width=350, height=350)

        self.title_label.config(text="Connect to Node")
        self.information_label.config(text=("Target Node IP or Name:\n[0-255].[0-255].[0-255].[0-255]"
                                            "\nOR\nbetween 1 and 15 characters"
                                            "\nInterface Name:\nbetween 1 and 15 characters"
                                            "\nTarget Interface Name:\nbetween 1 and 15 characters"
                                            "\nSpeed of Link: 1-99"
                                            "\nMetrics of Link: 1-99"), fg="black")

        self.label_1.config(text="Target Node IP or Name")
        self.entry_1.config(state="normal")

        self.label_2.config(text="Interface Name")
        self.entry_2.config(state="normal")

        self.label_3.config(text="Target Interface Name")
        self.entry_3.config(state="normal")

        self.label_4.config(text="Speed of Link")
        self.entry_4.config(state="normal")

        self.label_5.config(text="Metrics of Link")
        self.entry_5.config(state="normal")

        self.label_1.place(relx=0.0, rely=0.0, relwidth=0.6, relheight=0.1)
        self.entry_1.place(relx=0.6, rely=0.0, relwidth=0.4, relheight=0.1)

        self.label_2.place(relx=0.0, rely=0.1, relwidth=0.6, relheight=0.1)
        self.entry_2.place(relx=0.6, rely=0.1, relwidth=0.4, relheight=0.1)

        self.label_3.place(relx=0.0, rely=0.2, relwidth=0.6, relheight=0.1)
        self.entry_3.place(relx=0.6, rely=0.2, relwidth=0.4, relheight=0.1)

        self.label_4.place(relx=0.0, rely=0.3, relwidth=0.6, relheight=0.1)
        self.entry_4.place(relx=0.6, rely=0.3, relwidth=0.4, relheight=0.1)

        self.label_5.place(relx=0.0, rely=0.4, relwidth=0.6, relheight=0.1)
        self.entry_5.place(relx=0.6, rely=0.4, relwidth=0.4, relheight=0.1)

        self.information_label.place(
            relx=0.1, rely=0.5, relwidth=0.8, relheight=0.4)

        self.submit_button.place(
            relx=0.0, rely=0.9, relwidth=0.25, relheight=0.1)
        self.cancel_button.place(
            relx=0.75, rely=0.9, relwidth=0.25, relheight=0.1)
        self.title_label.place(relx=0.25, rely=0.9,
                               relwidth=0.5, relheight=0.1)

    def setup_disconnect_interface_frame(self, x: int, y: int) -> None:
        self.config_frame.place(x=x, y=y, width=350, height=350)

        self.title_label.config(text="Disconnect Interface")
        self.information_label.config(text="Interface Name:\nbetween 1 and 15 characters",
                                      fg="black")

        self.label_1.config(text="Interface Name")
        self.entry_1.configure(state="normal")

        self.label_1.place(relx=0.0, rely=0.0, relwidth=0.5, relheight=0.1)
        self.entry_1.place(relx=0.5, rely=0.0, relwidth=0.5, relheight=0.1)

        self.information_label.place(
            relx=0.1, rely=0.4, relwidth=0.8, relheight=0.5)

        self.submit_button.place(
            relx=0.0, rely=0.9, relwidth=0.25, relheight=0.1)
        self.cancel_button.place(
            relx=0.75, rely=0.9, relwidth=0.25, relheight=0.1)
        self.title_label.place(relx=0.25, rely=0.9,
                               relwidth=0.5, relheight=0.1)

    def clear_frame(self) -> None:
        self.config_frame.place_forget()
        for widget in self.config_frame.winfo_children():
            if widget.winfo_class() == "Entry":
                widget.delete(0, "end")
                widget.configure(state="disabled")
            widget.place_forget()
