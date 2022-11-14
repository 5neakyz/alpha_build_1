import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd

import serial.tools.list_ports

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

 # - - - vars - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        
        #returnes a lit of all com ports and infor
        self.comlist = serial.tools.list_ports.comports()
        #needed to just get com ports name(.device)
        self.COM_items = []
        for item in self.comlist:
            self.COM_items.append(item.device)

        self.selected_coms = []


        self.firmware_path= None
        self.firmware_path_str = tk.StringVar(value=self.firmware_path)
        self.personality_path = None
        self.personality_path_str = tk.StringVar(value=self.personality_path)

        self.hex_red = '#f5162c'
        self.hex_green = '#1df516'

        #device selection
        self.device_selection_frame = ttk.LabelFrame(self.root_window,text="Select Devices")
        self.device_selection_frame.grid(row=0, column=0, padx=(20, 10), pady=10, sticky="nsew")

        ##list box
        self.list_box_items = tk.Variable(value=self.COM_items)

        self.listbox = tk.Listbox(
            self.device_selection_frame,
            listvariable=self.list_box_items,
            height=6)

        self.listbox.pack(padx=10, pady=10,expand=True)
        # alternate line colors
        try:
            for i in range(0,len(self.COM_items),2):
                self.listbox.itemconfigure(i, background='#242424')
        except Exception as e: print(e)

        def items_selected(event):
            # get selected indices
            selected_indices = self.listbox.curselection()
            # get selected items
            selected_langs = ",".join([self.listbox.get(i) for i in selected_indices])
            msg = f'You selected: {selected_langs}'
            print(msg)

        self.listbox.bind('<<ListboxSelect>>', items_selected)

        #display selected devices
        self.selected_devices_frame= ttk.LabelFrame(self.device_selection_frame,text="Selected Devices")
        self.selected_devices_frame.pack(padx=10, pady=10,expand=True)
        self.selected_devices_placeholder = ttk.Label(self.selected_devices_frame,text="Nothing Selected",wraplength=300)
        self.selected_devices_placeholder.pack(padx=10, pady=10)

        # select devices buttons
        self.connect_device_btn = ttk.Button(self.device_selection_frame, text="Connect")
        self.connect_device_btn.pack(padx=10,pady=10,expand=True,anchor="s",side="left")

        self.disconnect_device_btn = ttk.Button(self.device_selection_frame, text="Disconnect")
        self.disconnect_device_btn.pack(padx=10,pady=10,expand=True,anchor="s",side="left")

        #radio box - config type/ option
        self.var = tk.IntVar(value=1)
        #box for config options
        self.config_options_frame = ttk.LabelFrame(self.root_window,text="Config Options")
        self.config_options_frame.grid(row=0, column=1, padx=(20, 10), pady=10, sticky="nsew")
        #config options
        self.radio_1=ttk.Radiobutton(self.config_options_frame, text="Erase Config",variable=self.var,value=1).pack(padx=5, pady=5,anchor="w",expand=True)
        self.radio_2=ttk.Radiobutton(self.config_options_frame, text="Push Personality Only",variable=self.var,value=2).pack(padx=5, pady=5,anchor="w",expand=True)
        self.radio_3=ttk.Radiobutton(self.config_options_frame, text="Push Firmware Only",variable=self.var,value=3).pack(padx=5, pady=5,anchor="w",expand=True)
        self.radio_4=ttk.Radiobutton(self.config_options_frame, text="Push Both Firmware and Personality",value=4,variable=self.var).pack(padx=5, pady=5,anchor="w",expand=True)

        #file selection

        self.select_files_frame = ttk.LabelFrame(self.root_window,text="Select Files")
        self.select_files_frame.grid(row=1, column=0,padx=(20, 10), pady=10, sticky="nsew")

        self.selected_firmwware_frame=ttk.LabelFrame(self.select_files_frame,text="Firmware Path")
        self.selected_firmwware_frame.pack(padx=10,pady=5,expand=True)

        self.firmware_placeholder = ttk.Label(self.selected_firmwware_frame,text="C:/Users/bknox/Multi-ML-1.0/gui_design/Forest-ttk-theme-master/forest-dark.tcl",wraplength=300)
        self.firmware_placeholder.pack(padx=10,pady=5)

        self.selected_personality_frame=ttk.LabelFrame(self.select_files_frame,text="Personality Path")
        self.selected_personality_frame.pack(padx=10,pady=5,expand=True)

        self.personality_placeholder = ttk.Label(self.selected_personality_frame,text="C:/Users/bknox/Multi-ML-1.0/gui_design/Forest-ttk-theme-master/forest-dark.tcl",wraplength=300)
        self.personality_placeholder.pack(padx=10,pady=5)

        self.slct_firm_path_btn = ttk.Button(self.select_files_frame,text="Select Firmware")
        self.slct_firm_path_btn.pack(padx=10,pady=10,expand=True,anchor="s",side="left")

        self.slct_pers_path_btn = ttk.Button(self.select_files_frame,text="Select Personality")
        self.slct_pers_path_btn.pack(padx=10,pady=10,expand=True,anchor="s",side="left")

        # run 
        self.run_frame = ttk.LabelFrame(self.root_window,text="Run")
        self.run_frame.grid(row=1, column=1,padx=(20, 10), pady=10, sticky="nsew")


        self.results_frame = ttk.LabelFrame(self.run_frame,text="Results")
        self.results_frame.pack(padx=5,pady=5,expand=True)

        self.results_placeholder = ttk.Label(self.results_frame,text="No results")
        self.results_placeholder.pack(padx=10, pady=10,expand=True,anchor="n")

        self.progress_bar = ttk.Progressbar(self.run_frame,orient='horizontal', length=250, mode='determinate')
        self.progress_bar.pack(padx=10, pady=10,expand=True)

        self.run_btn = ttk.Button(self.run_frame,text="Run")
        self.run_btn.pack(padx=10, pady=10,expand=True,anchor="sw",side="left")



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