import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter import scrolledtext

import serial.tools.list_ports
import time
import os
import sys
import webbrowser
import threading
import logging
import concurrent.futures

#my classes
from ml_device import Device

#247F4C

class TungstenGui(tk.Tk):
    def __init__(self):
        super().__init__()
        # configure window
        self.title("5neakyz")
        self.geometry(f"{1460}x{760}")

        self.bind('<KeyPress>', self.onKeyPress)

        #style
        self.option_add("*tearOff", False) # This is always a good idea
        icon_path = self.resource_path("assests/myicon.ico")
        self.iconbitmap(icon_path)
        style_path = self.resource_path('assests/Forest-ttk-theme-master/forest-dark.tcl')
        self.tk.call('source', style_path)
        ttk.Style().theme_use('forest-dark')
        s = ttk.Style()
        s.configure('red.TFrame', background='red')#2B2B2B
        s.configure('green.TFrame',background="green")
        s.configure('blue.TFrame',background="blue")


        ##vars
        self.raw_comports = serial.tools.list_ports.comports() # comports on pc
        self.comports = self.get_comport_names() #comport names
        self.list_box_items = tk.Variable(self,value=self.comports)#comport names as string for listbox
        self.selected_comports = [] # user selection
        self.selected_comports_str = tk.StringVar(value=self.selected_comports) # string list
        self.devices = []
#frames / gui setup

# Menu Bar

        self.menu_bar = ttk.Frame()
        self.menu_bar.pack(fill="x",side="top")
        self.menu_bar_label = ttk.Label(self.menu_bar,background="#247F4C").pack(expand=True,fill="both")

# Footer Info Bar
        self.footer_bar = ttk.Frame()
        self.footer_bar.pack(fill="x",side="bottom")
        self.footer_bar_label = ttk.Label(self.footer_bar,background="#247F4C").pack(expand=True,fill="both")
# Side bar

        self.side_bar = ttk.Frame()
        self.side_bar.pack(fill="y",side="left")
        #create widgets
        self.side_bar_run_btn  = ttk.Button(self.side_bar,text="Run",command=lambda: threading.Thread(target=self.run_btn_press).start())
        self.side_bar_connect_btn = ttk.Button(self.side_bar,text="Connect")
        self.side_bar_disconnect_btn = ttk.Button(self.side_bar,text="Disconnect")
        self.side_bar_listbox = tk.Listbox(self.side_bar,listvariable=self.list_box_items,font=('',14),height=5,width=12)
        self.side_bar_selected_devices_frame= ttk.LabelFrame(self.side_bar,text="Selected Devices")
        self.side_bar_selected_devices_placeholder = ttk.Label(self.side_bar_selected_devices_frame,textvariable=self.selected_comports_str,wraplength=55)
        #functions on click listbox
        self.side_bar_listbox.bind('<<ListboxSelect>>', lambda event: self.items_selected(event))

        #create grid
        self.columnconfigure(1,weight=1)
        self.rowconfigure((1,2,3,4,5,6,7,8,9),weight=0)

        #place widgets
        self.side_bar_run_btn.grid(row=1,column=1,sticky="new",padx=20, pady=(20, 0))
        self.side_bar_connect_btn.grid(row=2,column=1,sticky="new",padx=20, pady=(20, 0))
        self.side_bar_disconnect_btn.grid(row=3,column=1,sticky="new",padx=20, pady=(20, 0))
        # list box
        self.side_bar_listbox.grid(row=4,column=1,sticky="nw",padx=20, pady=(20, 0))
        # alternate line colors
        try:
            for i in range(0,len(self.comports),2):
                self.side_bar_listbox.itemconfigure(i, background='#242424')
        except Exception as e: print(f'LIST BOX EXCEPTION{e}')

        self.side_bar_selected_devices_frame.grid(row=5,column=1,sticky="new",padx=20, pady=(20, 0))
        self.side_bar_selected_devices_placeholder.pack(padx=20,pady=20)

# Main

    # check buttons
        self.check_buttons = ttk.Frame()
        self.check_buttons.pack(fill="both")

        self.check_buttons.columnconfigure((1,2,3,4),weight=0)
        self.check_buttons.rowconfigure((1),weight=1)

        #check options values
        self.check_erase_config = tk.IntVar()
        self.check_push_pers = tk.IntVar()
        self.check_push_firm = tk.IntVar()
        self.check_push_BLE = tk.IntVar()

        self.check_1=ttk.Checkbutton(self.check_buttons, text="Erase Config",variable=self.check_erase_config).grid(row=1,column=1,padx=1,pady=1,sticky="w")
        self.check_2=ttk.Checkbutton(self.check_buttons, text="Push Personality",variable=self.check_push_pers).grid(row=1,column=2,padx=1,pady=1,sticky="w")
        self.check_3=ttk.Checkbutton(self.check_buttons, text="Push Firmware",variable=self.check_push_firm).grid(row=1,column=3,padx=1,pady=1,sticky="w")
        self.check_4=ttk.Checkbutton(self.check_buttons, text="Push BLE",variable=self.check_push_BLE).grid(row=1,column=4,padx=1,pady=1,sticky="w")

    # file selection 
        self.file_selection = ttk.Frame()
        self.file_selection.pack(fill="both")
        #create grid on frame
        self.file_selection.columnconfigure((1,2),weight=0)
        self.file_selection.rowconfigure((1,2,3),weight=0)        

        #vars
        self.firmware_path = None
        self.personality_path = None
        self.ble_path = None
        self.firmware_path_str = tk.StringVar(value=self.firmware_path)
        self.personality_path_str = tk.StringVar(value=self.personality_path)
        self.ble_path_str = tk.StringVar(value=self.ble_path)

        #create widgets
        self.select_firmware_btn  = ttk.Button(self.file_selection,text="Firmware",command=lambda: threading.Thread(target=self.get_path("firm")).start())
        self.select_personality_btn  = ttk.Button(self.file_selection,text="Personality",command=lambda: threading.Thread(target=self.get_path("pers")).start())
        self.select_ble_btn  = ttk.Button(self.file_selection,text="BLE",command=lambda: threading.Thread(target=self.get_path("ble")).start())
        self.firmware_label = ttk.Label(self.file_selection,textvariable=self.firmware_path_str)
        self.personality_label = ttk.Label(self.file_selection,textvariable=self.personality_path_str)
        self.ble_label = ttk.Label(self.file_selection,textvariable=self.ble_path_str)

        #place widgets
        self.select_firmware_btn.grid(row=1,column=1,padx=2,pady=2)
        self.select_personality_btn.grid(row=2,column=1,padx=2,pady=2)
        self.select_ble_btn.grid(row=3,column=1,padx=2,pady=2)
        self.firmware_label.grid(row=1,column=2,padx=2,pady=2,sticky="w")
        self.personality_label.grid(row=2,column=2,padx=2,pady=2,sticky="w")
        self.ble_label.grid(row=3,column=2,padx=2,pady=2,sticky="w")
    #display tabs
        self.tab_view = ttk.Notebook()
        self.tab_view.pack(fill="both",expand=True,padx=5,pady=5)

        self.new_pad = ttk.Frame(self.tab_view)

        self.tab_view.add(self.new_pad,text="Tab 1")




        self.mainloop()

    def run_btn_press(self):
        print(f'run')

    def connect_btn_press(self):
        #change frame text 
        self.side_bar_selected_devices_frame.configure(text="Connecting")
        #remove all in selected devices frame
        self.clear_child_in_frame(self.side_bar_selected_devices_frame)
        temp_devices_list = []
        for device in self.devices:
            temp_devices_list.append(device.device)

        for device in self.selected_comports():
            if device not in temp_devices_list:
                self.devices.append()
        #create threadpool for all devices threadpool(function , devices)
        results = self.create_threadpool(self.is_connection_live,self.co)
        #reset frame text
        self.side_bar_selected_devices_frame.configure(text="Selected Devices")

    def disconnect_btn_press(self):
        pass

    def create_threadpool(self,function,items):
        results = []
        with concurrent.futures.ThreadPoolExecutor() as executor:# parallelism 
            tasks = [executor.submit(function,item) for item in items]
            for x in concurrent.futures.as_completed(tasks):
                results.append(x.result())
        return results

    def clear_child_in_frame(self,*frames):
        for frame in frames:
            for widgets in frame.winfo_children():
                widgets.destroy()

    def get_path(self,type):
        path = fd.askopenfilename()
        head,tail = os.path.split(path)
        if type == "firm":
            self.firmware_path = tail
            self.firmware_path_str.set(tail)
        if type == "pers":
            self.personality_path = tail
            self.personality_path_str.set(tail)
        if type == "ble":
            self.ble_path = tail
            self.ble_path_str.set(tail)
        
    def items_selected(self,event):
        print(self.selected_comports)
        try:
            selected_item = event.widget.get(self.side_bar_listbox.curselection()[0])
            print(selected_item)
            if selected_item in self.selected_comports:
                (self.selected_comports.remove(selected_item))
            else:
                (self.selected_comports.append(selected_item))
            self.selected_comports_str.set(self.selected_comports)
        except Exception as e: print(e)

    def resource_path(self,relative_path):
        """ Get absolute path to resource, works for dev and for PyInstaller """
        base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
        return os.path.join(base_path, relative_path)
    
    def get_comport_names(self):
        comport_list = []
        for item in self.raw_comports:
            comport_list.append(item.device)
        return self.sort_comports(comport_list)
    
    def sort_comports(self,list):
        sorted_list = []
        for comport in list:
            comport = comport.replace("COM","")
            print(comport)
            try:
                sorted_list.append(int(comport))
            except:
                sorted_list.append(comport)

        sorted_list.sort()
        list = []
        
        for item in sorted_list:
            item =f"COM{item}"
            print(item)
            list.append(item)
        return list

    def onKeyPress(self,event):
        print(f'You pressed: {event.keysym}')

if __name__ == "__main__":
    TungstenGui()
