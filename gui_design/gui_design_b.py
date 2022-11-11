import tkinter as tk
from tkinter import ttk


class MyApp():
    def __init__(self,root):
        self.root_window = root
        self.root_window.title("ML Multi Units")
        #self.root_window.geometry("600x600")
        self.root_window.option_add("*tearOff", False) # This is always a good idea
        # Import the tcl file
        self.root_window.tk.call('source', 'C:/Users/bknox/Multi-ML-1.0/gui_design/Forest-ttk-theme-master/forest-dark.tcl')
        # Set the theme with the theme_use method
        ttk.Style().theme_use('forest-dark')
        # Make the app responsive
        root.columnconfigure(index=0, weight=1)
        root.columnconfigure(index=1, weight=1)
        root.columnconfigure(index=2, weight=1)
        root.rowconfigure(index=0, weight=1)
        root.rowconfigure(index=1, weight=1)
        root.rowconfigure(index=2, weight=1)

 
        #device selection
        self.device_selection_frame = ttk.LabelFrame(self.root_window,text="Select Devices")
        self.device_selection_frame.grid(row=0, column=0, padx=(20, 10), pady=10, sticky="nsew")

        ##list box
        langs = ('Java', 'C#', 'C', 'C++', 'Python','Go', 'JavaScript', 'PHP', 'Swift')
        self.COM_items = []
        self.list_box_items = tk.Variable(value=langs)

        listbox = tk.Listbox(
            self.device_selection_frame,
            listvariable=self.list_box_items,
            height=6,
            selectmode=tk.EXTENDED)

        listbox.grid(row=0, column=0,columnspan=2, padx=(20, 10), pady=10, sticky="nsew")

        def items_selected(event):
            # get selected indices
            selected_indices = listbox.curselection()
            # get selected items
            selected_langs = ",".join([listbox.get(i) for i in selected_indices])
            msg = f'You selected: {selected_langs}'
            print(msg)

        listbox.bind('<<ListboxSelect>>', items_selected)
        #display selected devices
        self.seleted_coms_lbl = ttk.Label(self.device_selection_frame,text="Selected Devices: ")
        self.seleted_coms_lbl.grid(row=1, column=0,columnspan=3)
        #self.seleted_coms_lbl = ttk.Label(self.device_selection_frame,textvariable=self.sltcd_devices_str).pack()

        # select devices buttons
        self.connect_device_btn = ttk.Button(self.device_selection_frame, text="Connect")
        self.connect_device_btn.grid(row=3, column=0, padx=(20,10),pady=10, sticky="nsew")

        self.disconnect_device_btn = ttk.Button(self.device_selection_frame, text="Disconnect")
        self.disconnect_device_btn.grid(row=3, column=1, padx=(20,10),pady=10, sticky="nsew")

        #radio box - config type/ option
        self.var = tk.IntVar(value=1)
        #box for config options
        self.config_options_frame = ttk.LabelFrame(self.root_window,text="Config Options")
        self.config_options_frame.grid(row=0, column=1, padx=(20, 10), pady=10, sticky="nsew")
        #config options
        self.radio_1=ttk.Radiobutton(self.config_options_frame, text="Erase Config",variable=self.var,value=1).grid(row=0, column=0, padx=5, pady=10, sticky="nsew")
        self.radio_2=ttk.Radiobutton(self.config_options_frame, text="Push Personality Only",variable=self.var,value=2).grid(row=1, column=0, padx=5, pady=10, sticky="nsew")
        self.radio_3=ttk.Radiobutton(self.config_options_frame, text="Push Firmware Only",variable=self.var,value=3).grid(row=2, column=0, padx=5, pady=10, sticky="nsew")
        self.radio_4=ttk.Radiobutton(self.config_options_frame, text="Push Both Firmware and Personality",value=4,variable=self.var).grid(row=3, column=0, padx=5, pady=10, sticky="nsew")

        #file selection
        self.select_files_frame = ttk.LabelFrame(self.root_window,text="Select Files")
        self.select_files_frame.grid(row=1, column=0,padx=(20, 10), pady=10, sticky="nsew")

        self.slct_firm_path_btn = ttk.Button(self.select_files_frame,text="Select Firmware")
        self.slct_firm_path_btn.grid(row=0, column=0,padx=(20, 10), pady=10, sticky="nsew")

        self.slct_pers_path_btn = ttk.Button(self.select_files_frame,text="Select Personality")
        self.slct_pers_path_btn.grid(row=3, column=0,padx=(20, 10), pady=10, sticky="nsew")


        #sizegrip
        sizegrip = ttk.Sizegrip(self.root_window)
        sizegrip.grid(row=100, column=100, padx=(0, 5), pady=(0, 5))

        # Center the window, and set minsize
        self.root_window.update()
        self.root_window.minsize(self.root_window.winfo_width(), self.root_window.winfo_height())
        x_cordinate = int((self.root_window.winfo_screenwidth()/2) - (self.root_window.winfo_width()/2))
        y_cordinate = int((self.root_window.winfo_screenheight()/2) - (self.root_window.winfo_height()/2))
        self.root_window.geometry("+{}+{}".format(x_cordinate, y_cordinate))
        
        self.root_window.mainloop()

if __name__ == '__main__':
    game = MyApp(tk.Tk())