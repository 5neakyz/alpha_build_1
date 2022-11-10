import tkinter as tk
from tkinter import ttk 

class MyApp:
    def __init__(self,root):
        self.root_window = root
        # Import the tcl file
        self.root_window.call('source', 'C:/Users/sneak/Multi-ML-1.0/gui_design/Forest-ttk-theme-master/forest-dark.tcl')

        # Set the theme with the theme_use method
        ttk.Style().theme_use('forest-dark')

        self.who_goes_first = tk.StringVar(None, "B")
        #create who goes first variable
        #self.who_goes_first = tk.StringVar()
        self.who_goes_first.set("B")
        #black radio button
        self._who_goes_first_radiobutton = ttk.Radiobutton(
            self.root_window,
            text = 'Black',
            variable = self.who_goes_first,
            value = 'B')    
        self._who_goes_first_radiobutton.grid(row=0, column=1)

        #white radio button
        self._who_goes_first_radiobutton = ttk.Radiobutton(
            self.root_window,
            text = 'White',
            variable = self.who_goes_first,
            value = 'W')    
        self._who_goes_first_radiobutton.grid(row=1, column=1)

    def start(self) -> None:
        self.root_window.mainloop()

if __name__ == '__main__':

    root = tk.Tk()
    game = MyApp(root)
    game.start()
    # MyApp(root)
    # root.mainloop()
