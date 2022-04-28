"""
This module makes ObjectFrame objects available for use when imported
"""
from tkinter import Button, Label, PhotoImage, ttk
from idlelib.tooltip import Hovertip


class ObjectFrame:
    """
    The window containing the exit button and acting as a display for Network
    components

    Data members:
    parent             (ttk.Frame): The parent window containing this and other \
                                    Widgets
    object_frame       (ttk.Frame): The Frame itself
    exit_button        (Button): Exit button
    exit_button_image  (PhotoImage): The image of the exit_button
    display_text_label (Label): The field to display the data on
    """

    def __init__(self, parent: ttk.Frame) -> None:
        self.object_frame: ttk.Frame = ttk.Frame(parent)
        self.parent: ttk.Frame = parent
        self.exit_button_image: PhotoImage = PhotoImage(
            file="resources/exit_icon.png")

        # Set the position of this Frame inside the parent container
        self.object_frame.grid(column=1, row=0, sticky="nsew")

        # Setup the grid configuration for the Frame
        self.object_frame.columnconfigure(0, weight=10)
        self.object_frame.columnconfigure(1, weight=1)
        self.object_frame.rowconfigure(0, weight=1)
        self.object_frame.rowconfigure(1, weight=50)

        # Setup the Widgets
        self.exit_button: Button = Button(
            self.object_frame, image=self.exit_button_image)
        Hovertip(self.exit_button, "Exit the application")
        self.display_text_label: Label = Label(
            self.object_frame, text="", width=7)

        # Set the grid configuration for the Widgets
        self.exit_button.grid(column=1, row=0, sticky="nsew")
        self.display_text_label.grid(
            column=0, row=1, columnspan=2, sticky="new", ipadx=0, padx=0)
        start_display: str = ("Press right-click on the display to start working with the Network\n\n"
                              "Press left-click on a component to display it's attributes here\n\n"
                              "Press left-click on a component and then drag to move it")

        # Display a starting text
        self.display_text(start_display)

    def display_text(self, to_display: str) -> None:
        """
        Changes the currently shown text in the display_text_label

        Parameters:
        to_display (str): The string to display
        """
        self.display_text_label.config(text=to_display)
