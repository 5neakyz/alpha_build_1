import tkinter as tk
from tkinter import ttk 
import logging

from MyNewGui import Multi_Stager_Gui

if __name__ == "__main__":
    format = "%(asctime)s.%(msecs)04d: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO,
                        datefmt="%H:%M:%S")

    app = Multi_Stager_Gui(tk.Tk())
    