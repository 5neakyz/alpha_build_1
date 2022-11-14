import tkinter as tk
from tkinter import ttk


class MyApp():
    def __init__(self,root):
        self.root_window = root
        self.root_window.title("ML Multi Units")
        #self.root_window.geometry("600x600")
        self.root_window.option_add("*tearOff", False) # This is always a good idea
        # Import the tcl file
        self.root_window.tk.call('source', 'gui_design/Forest-ttk-theme-master/forest-dark.tcl')
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
        langs = ('COM1','COM2','COM3','COM4','COM5','COM6','COM7','COM8',)
        self.COM_items = []
        self.list_box_items = tk.Variable(value=langs)

        listbox = tk.Listbox(
            self.device_selection_frame,
            listvariable=self.list_box_items,
            height=6,
            font=('',12),
            selectmode=tk.EXTENDED)

        listbox.pack(padx=10, pady=10,expand=True)

        def items_selected(event):
            # get selected indices
            selected_indices = listbox.curselection()
            # get selected items
            selected_langs = ",".join([listbox.get(i) for i in selected_indices])
            msg = f'You selected: {selected_langs}'
            print(msg)

        listbox.bind('<<ListboxSelect>>', items_selected)
        #display selected devices
        self.selected_devices_frame = ttk.LabelFrame(self.device_selection_frame,text="Selected Devices")
        self.selected_devices_frame.pack(padx=10, pady=10,expand=True)

        self.slct_d_placeholder_lbl = ttk.Label(self.selected_devices_frame,text="Nothing Selected")
        self.slct_d_placeholder_lbl.pack(anchor="w",padx=5, pady=5,)

        # self.selected_devices_lbl = ttk.Label(self.selected_devices_frame,text="COM1")
        # self.selected_devices_lbl.pack(padx=5, pady=10,expand=True,side="left")
        # self.selected_devices_lbl = ttk.Label(self.selected_devices_frame,text="COM2")
        # self.selected_devices_lbl.pack(padx=5, pady=10,expand=True,side="left")
        # self.selected_devices_lbl = ttk.Label(self.selected_devices_frame,text="COM3")
        # self.selected_devices_lbl.pack(padx=5, pady=10,expand=True,side="left")
        # self.selected_devices_lbl = ttk.Label(self.selected_devices_frame,text="COM4")
        # self.selected_devices_lbl.pack(padx=5, pady=10,expand=True,side="left")

        # select devices buttons
        self.connect_device_btn = ttk.Button(self.device_selection_frame, text="Connect")
        self.connect_device_btn.pack(padx=10, pady=10,side="left",expand=True)

        self.disconnect_device_btn = ttk.Button(self.device_selection_frame, text="Disconnect")
        self.disconnect_device_btn.pack(padx=10, pady=10,side="left",expand=True)

        #radio box - config type/ option
        self.var = tk.IntVar(value=1)
        #box for config options
        self.config_options_frame = ttk.LabelFrame(self.root_window,text="Config Options")
        self.config_options_frame.grid(row=0, column=1, padx=(20, 10), pady=10, sticky="nsew")
        #config options
        self.radio_1=ttk.Radiobutton(self.config_options_frame, text="Erase Config",variable=self.var,value=1).pack(padx=20, pady=15,anchor="nw",side="top")
        self.radio_2=ttk.Radiobutton(self.config_options_frame, text="Push Personality Only",variable=self.var,value=2).pack(padx=20, pady=15,anchor="nw",side="top")
        self.radio_3=ttk.Radiobutton(self.config_options_frame, text="Push Firmware Only",variable=self.var,value=3).pack(padx=20, pady=15,anchor="nw",side="top")
        self.radio_4=ttk.Radiobutton(self.config_options_frame, text="Push Both Firmware and Personality",value=4,variable=self.var).pack(padx=20, pady=15,anchor="nw",side="top")

        #file selection
        self.selected_firmware_path = tk.StringVar(value="C:/Users/sneak/Multi-ML-1.0/gui_design/Forest-ttk-theme-master/forest-dark.tcl")


        self.select_files_frame = ttk.LabelFrame(self.root_window,text="Select Files")
        self.select_files_frame.grid(row=1, column=0,padx=(20, 10), pady=10, sticky="nsew")

        self.firmware_frame_box = ttk.LabelFrame(self.select_files_frame,text="Firmware Path")
        self.firmware_frame_box.pack(padx=10, pady=10,expand=True)

        self.selected_firmware_lbl = ttk.Label(self.firmware_frame_box,textvariable=self.selected_firmware_path,wraplength=300)
        self.selected_firmware_lbl.pack(padx=10, pady=10,expand=True)

        self.personality_frame_box = ttk.LabelFrame(self.select_files_frame,text="Personality Path")
        self.personality_frame_box.pack(padx=10, pady=10,expand=True)

        self.slct_firm_path_btn = ttk.Button(self.select_files_frame,text="Select Firmware")
        self.slct_firm_path_btn.pack(padx=10, pady=10,expand=True,side="left")

        self.selected_personality_lbl = ttk.Label(self.personality_frame_box,textvariable=self.selected_firmware_path,wraplength=300)
        self.selected_personality_lbl.pack(padx=10, pady=10,expand=True)

        self.slct_pers_path_btn = ttk.Button(self.select_files_frame,text="Select Personality")
        self.slct_pers_path_btn.pack(padx=10, pady=10,expand=True,side="left")

        # RUN
        self.run_frame = ttk.LabelFrame(self.root_window,text="Run")
        self.run_frame.grid(row=1,column=1,padx=(20, 10), pady=10, sticky="nsew")


        self.progress_bar = ttk.Progressbar(self.run_frame,orient='horizontal', length=200, mode='determinate')
        self.progress_bar.pack(padx=10, pady=10,expand=True)

        self.returned_results_frame = ttk.LabelFrame(self.run_frame,text="Returned Results")
        self.returned_results_frame.pack(padx=10, pady=10,expand=True)

        self.slct_d_placeholder_lbl = ttk.Label(self.returned_results_frame,text="Nothing Selected")
        self.slct_d_placeholder_lbl.pack(anchor="w",padx=5, pady=5,)

        self.run_btn=ttk.Button(self.run_frame,text ="Run",)
        self.run_btn.pack(padx=10, pady=10,anchor="sw",expand=True)

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