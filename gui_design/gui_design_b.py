import tkinter as tk
from tkinter import ttk


class MyApp():
    def __init__(self,root):
        self.root_window = root
        self.root_window.title("ML Multi Units")
        self.root_window.geometry("600x600")
        self.root_window.option_add("*tearOff", False) # This is always a good idea
        # Import the tcl file
        self.root_window.tk.call('source', 'C:/Users/sneak/Multi-ML-1.0/gui_design/Forest-ttk-theme-master/forest-dark.tcl')
        # Set the theme with the theme_use method
        ttk.Style().theme_use('forest-dark')


 
        #radio box - config type/ option
        self.var = tk.IntVar(value=1)

        #box for config options
        self.config_options = ttk.LabelFrame(self.root_window,text="Config Options")
        self.config_options.grid(row=0, column=0, padx=(20, 10), pady=10, sticky="nsew")
        #config options
        self.radio_1=ttk.Radiobutton(self.config_options, text="Erase Config",variable=self.var,value=1).grid(row=0, column=0, padx=5, pady=10, sticky="nsew")
        self.radio_2=ttk.Radiobutton(self.config_options, text="Push Personality Only",variable=self.var,value=2).grid(row=1, column=0, padx=5, pady=10, sticky="nsew")
        self.radio_3=ttk.Radiobutton(self.config_options, text="Push Firmware Only",variable=self.var,value=3).grid(row=2, column=0, padx=5, pady=10, sticky="nsew")
        self.radio_4=ttk.Radiobutton(self.config_options, text="Push Both Firmware and Personality",value=4,variable=self.var).grid(row=3, column=0, padx=5, pady=10, sticky="nsew")

        self.select_files = ttk.LabelFrame(self.root_window,text="Config Options")
        self.select_files.grid(row=1, column=0,padx=(20, 10), pady=10, sticky="nsew")

        self.slct_firm_path_btn = ttk.Button(self.select_files,text="Select Firmware")
        self.slct_firm_path_btn.grid(row=0, column=0,padx=(20, 10), pady=10, sticky="nsew")

        self.slct_pers_path_btn = ttk.Button(self.select_files,text="Select Personality")
        self.slct_pers_path_btn.grid(row=3, column=0,padx=(20, 10), pady=10, sticky="nsew")

        # var = tk.IntVar(None,value=2)
        print("help")
    def start_mainloop(self) -> None:
        self.root_window.mainloop()

if __name__ == '__main__':

    root = tk.Tk()
    game = MyApp(root)
    game.start_mainloop()