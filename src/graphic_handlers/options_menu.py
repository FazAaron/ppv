"""
This module makes OptionsMenu objects available for use when imported
"""
from tkinter import Button, Entry, Label, Menu, ttk
from turtle import setundobuffer

class OptionsMenu:

    def __init__(self, parent: ttk.Frame) -> None:
        self.parent = parent
        self.options_menu: Menu = Menu(parent, tearoff=0)
        self.options_menu.add_command(label="1", command=self.test_stuff)
        self.options_menu.add_command(label="1")
        self.options_menu.add_command(label="1")
        self.options_menu.add_command(label="1")
        self.options_menu.add_command(label="1")
        self.options_menu.add_command(label="1")
        # To remove menu items self.options_menu.delete(1, 5)

    def pop_up(self, x: int, y: int) -> None:
        self.x = x
        self.y = y
        self.options_menu.tk_popup(x, y)

    def test_stuff(self) -> None:
        test = ttk.Frame(self.parent, relief="ridge")
        self.entry_1 = Entry(test)
        button = Button(test, text="asd", command=self.stuff)
        label_1 = Label(test, text="asd")
        test.place(x=self.x, y=self.y, width=250, height=250)
        button.place(x=2, y=2)
        label_1.place(x=10, y=10)
        self.entry_1.place(x=50, y=10)

    def stuff(self) -> None:
        print(self.entry_1.get())