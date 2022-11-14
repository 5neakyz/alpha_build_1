import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd

import serial.tools.list_ports
import time
import os
import threading

#my classes
from thread_runner import ThreadRunner
from pb_data import pb_data
from device import Device

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
        self.selected_coms_str = tk.StringVar(value=self.selected_coms)
        self.com_objects = []

        self.firmware_path= None
        self.personality_path = None
        self.firmware_path_str = tk.StringVar(value=self.firmware_path)
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

        #when list box item is clicked run fucntion items_selected
        self.listbox.bind('<<ListboxSelect>>', self.items_selected)

        #display selected devices
        self.selected_devices_frame= ttk.LabelFrame(self.device_selection_frame,text="Selected Devices")
        self.selected_devices_frame.pack(padx=10, pady=10,expand=True)
        self.selected_devices_placeholder = ttk.Label(self.selected_devices_frame,textvariable=self.selected_coms_str,wraplength=250)
        self.selected_devices_placeholder.pack(padx=10, pady=10)

        # select devices buttons
        #we use the lambda function for threading so the app still works while the button is running
        self.connect_device_btn = ttk.Button(self.device_selection_frame, text="Connect",command=lambda: threading.Thread(target=self.connect_btn_press).start())
        self.connect_device_btn.pack(padx=10,pady=10,expand=True,anchor="s",side="left")

        self.disconnect_device_btn = ttk.Button(self.device_selection_frame, text="Disconnect",command=lambda: threading.Thread(target=self.disconnect_btn_press).start())
        self.disconnect_device_btn.pack(padx=10,pady=10,expand=True,anchor="s",side="left")

        #radio box - config type/ option
        self.var = tk.IntVar(value=1)
        #box for config options
        self.config_options_frame = ttk.LabelFrame(self.root_window,text="Config Options")
        self.config_options_frame.grid(row=0, column=1, padx=(20, 10), pady=10, sticky="nsew")
        #config options
        self.radio_1=ttk.Radiobutton(self.config_options_frame, text="Erase Config",variable=self.var,value=1).pack(padx=5, pady=5,anchor="w")
        self.radio_2=ttk.Radiobutton(self.config_options_frame, text="Push Personality Only",variable=self.var,value=2).pack(padx=5, pady=5,anchor="w")
        self.radio_3=ttk.Radiobutton(self.config_options_frame, text="Push Firmware Only",variable=self.var,value=3).pack(padx=5, pady=5,anchor="w")
        self.radio_4=ttk.Radiobutton(self.config_options_frame, text="Push Both Firmware and Personality",value=4,variable=self.var).pack(padx=5, pady=5,anchor="w")

        #file selection

        self.select_files_frame = ttk.LabelFrame(self.root_window,text="Select Files")
        self.select_files_frame.grid(row=1, column=0,padx=(20, 10), pady=10, sticky="nsew")

        self.selected_firmwware_frame=ttk.LabelFrame(self.select_files_frame,text="Firmware Path")
        self.selected_firmwware_frame.pack(padx=10,pady=5,expand=True)

        self.firmware_placeholder = ttk.Label(self.selected_firmwware_frame,textvariable=self.firmware_path_str,wraplength=250)
        self.firmware_placeholder.pack(padx=10,pady=5)

        self.selected_personality_frame=ttk.LabelFrame(self.select_files_frame,text="Personality Path")
        self.selected_personality_frame.pack(padx=10,pady=5,expand=True)

        self.personality_placeholder = ttk.Label(self.selected_personality_frame,textvariable=self.personality_path_str,wraplength=250)
        self.personality_placeholder.pack(padx=10,pady=5)

        self.slct_firm_path_btn = ttk.Button(self.select_files_frame,text="Select Firmware",command=self.get_firmware_path)
        self.slct_firm_path_btn.pack(padx=10,pady=10,expand=True,anchor="s",side="left")

        self.slct_pers_path_btn = ttk.Button(self.select_files_frame,text="Select Personality",command=self.get_personality_path)
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

    #destroys anything that is a child of the given frame
    def clear_frame(self,frame):
        for widgets in frame.winfo_children():
            widgets.destroy()


    # list box func, runs on item click
    # gets selected item and adds to two lists
    # one we use and one Tkinter uses to display
    def items_selected(self,event):
        selected_indices = self.listbox.curselection()[0]#returns a list, you can select multiple
        selected_item = event.widget.get(self.listbox.curselection()[0])
        if selected_item in self.selected_coms:
            (self.selected_coms.remove(selected_item))
        else:
            (self.selected_coms.append(selected_item))
        self.selected_coms_str.set(self.selected_coms)


    def connect_btn_press(self):
        #check to see if any objects already exist
        #if no objects then temp list is skipped
        #need a temp list as need .device attribute of the objects
        self.selected_devices_frame.configure(text="Connecting")
        temp_obj_list = []
        for ob in self.com_objects:
            temp_obj_list.append(ob.device)
        #creates the objects and adds them to com object list , skips dupes
        for device in self.selected_coms:
            if device not in temp_obj_list:#do not need duplicate objects, plus cant have duplicate as serial is already connected
                self.com_objects.append(Device(device))
        #list comprehension is needed to remove objects of COMs that are no longer selected
        self.com_objects = [x for x in self.com_objects if x.device in self.selected_coms]

        self.clear_frame(self.selected_devices_frame)
        for i, object in enumerate(self.com_objects):
            color = self.hex_red
            alive = object.is_alive()
            if alive == True:
                color = self.hex_green
            my_connection_label = ttk.Label(self.selected_devices_frame,text=object.device,background=color)
            my_connection_label.pack(ipadx=5, ipady=5,padx=5, pady=5,side="left",expand=True)

        self.selected_devices_frame.configure(text="Selected Devices")

    def disconnect_btn_press(self):
        #empty selected coms and update tkinter string
        self.selected_coms.clear()
        self.selected_coms_str.set(self.selected_coms)
        self.clear_frame(self.selected_devices_frame)
        self.selected_devices_placeholder = ttk.Label(self.selected_devices_frame,textvariable=self.selected_coms_str,wraplength=250)
        self.selected_devices_placeholder.pack(padx=10, pady=10)

    def get_personality_path(self):
        pPath = fd.askopenfilename()
        self.personality_path = pPath
        self.personality_path_str.set(pPath)

    def get_firmware_path(self):
        fPath = fd.askopenfilename()
        self.firmware_path = fPath
        self.firmware_path_str.set(fPath)

if __name__ == '__main__':
    game = MyApp(tk.Tk())