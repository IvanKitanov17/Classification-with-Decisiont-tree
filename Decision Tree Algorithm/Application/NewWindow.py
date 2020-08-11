from tkinter import *


class TextBoxWindow:
    def __init__(self, master):
        self.master = master

        self.scrollbar = Scrollbar(self.master)
        self.scrollbar.pack(side=RIGHT, fill=Y)

        self.textbox = Text(self.master, width="700", height="300")
        self.textbox.config(state="normal")
        self.textbox.pack()

        self.textbox.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.textbox.yview)
