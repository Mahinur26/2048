import tkinter as tk

class Game(tk.Frame):
    def __init__(self):
        tk.Frame.__init__(self)
        self.grind()
        self.master.title("2048")
