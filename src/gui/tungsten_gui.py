import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd

import serial.tools.list_ports
import time
import os
import sys
import webbrowser
import threading
import logging
import concurrent.futures


class TungstenGui(tk.Tk):
    def __init__(self):
        super().__init__()
        # configure window
        self.title("5neakyz")
        self.geometry(f"{1200}x{600}")

        self.bind('<KeyPress>', self.onKeyPress)

        #style
        self.option_add("*tearOff", False) # This is always a good idea
        icon_path = self.resource_path("assests/myicon.ico")
        self.iconbitmap(icon_path)
        style_path = self.resource_path('assests/Forest-ttk-theme-master/forest-dark.tcl')
        self.tk.call('source', style_path)
        ttk.Style().theme_use('forest-dark')
        s = ttk.Style()
        s.configure('2b.TFrame', background='red')#2B2B2B

        ##vars
        self.raw_comports = serial.tools.list_ports.comports()
        self.comports = self.get_comport_names()
        self.list_box_items = tk.Variable(self,value=self.comports)
        self.selected_comports = []
        self.selected_comports_str = tk.StringVar(value=self.selected_comports)

        #frames / gui setup
        self.menu_bar = MenuBar(self)
        self.menu_bar = Sidebar(self)
        self.main_area = MainArea(self)


        self.mainloop()

    def resource_path(self,relative_path):
        """ Get absolute path to resource, works for dev and for PyInstaller """
        base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
        return os.path.join(base_path, relative_path)
    
    def get_comport_names(self):
        comport_list = []
        for item in self.raw_comports:
            comport_list.append(item.device)
        comport_list.sort()
        return comport_list
    
    def onKeyPress(self,event):
        print(f'You pressed: {event.keysym}')

class MenuBar(ttk.Frame):
    def __init__(self,parent):
        super().__init__(parent)
        ttk.Label(self,background="#247F4C").pack(expand=True,fill="both")
        self.place(x=0,y=0,relwidth=1,height=25)

    def donothing():
        pass

class Sidebar(ttk.Frame):
    def __init__(self,parent):
        super().__init__(parent)
        # create sidebar frame with widgets
        #ttk.Label(self,background="#2B2B2B").pack(expand=True,fill="both")
        self.place(x=0,y=25,width=180,relheight=1)
        #self.config(style='2b.TFrame')

        #create widgets
        self.run_btn  = ttk.Button(self,text="Run",command=lambda: threading.Thread(target=self.run_btn_press(parent)).start())
        self.connect_btn = ttk.Button(self,text="Connect")
        self.disconnect_btn = ttk.Button(self,text="Disconnect")
        self.listbox = tk.Listbox(self,listvariable=parent.list_box_items,font=('',14),height=5)
        #functions on click listbox
        self.listbox.bind('<<ListboxSelect>>', self.items_selected)

        #create grid
        self.columnconfigure(1,weight=1)
        self.rowconfigure((1,2,3,4,5,6,7,8,9),weight=0)

        #place widgets
        # place buttons
        self.run_btn.grid(row=1,column=1,sticky="new",padx=20, pady=(20, 0))
        self.connect_btn.grid(row=2,column=1,sticky="new",padx=20, pady=(20, 0))
        self.disconnect_btn.grid(row=3,column=1,sticky="new",padx=20, pady=(20, 0))
        # list box
        self.listbox.grid(row=4,column=1,sticky="new",padx=20, pady=(20, 0))
        # alternate line colors
        try:
            for i in range(0,len(parent.comports),2):
                self.listbox.itemconfigure(i, background='#242424')
        except Exception as e: print(f'LIST BOX EXCEPTION{e}')

    def run_btn_press(self,parent):
        print(parent.main_area.radio_ml_options.radio_option.get())


    def items_selected(self,event):
        try:
            selected_item = event.widget.get(self.listbox.curselection()[0])
            print(selected_item)
        #     if selected_item in parent.selected_comports:
        #         (parent.selected_comports.remove(selected_item))
        #     else:
        #         (parent.selected_comports.append(selected_item))
        #     parent.selected_comports_str.set(parent.selected_comports)
        except Exception as e: print(e)
        # print(parent.selected_comports)

class MainArea(ttk.Frame):
    def __init__(self,parent):
        super().__init__(parent)
        #ttk.Label(self,background="#242424").pack(expand=True,fill="both")
        self.place(x=180,y=25,relwidth=1,relheight=1)

        self.radio_ml_options = RadioMLOption(self)
        self.file_path_selction = FilePathSelection(self)
        self.device_display = DeviceDisplay(self)
        self.info_bar = InfoBar(self)

    def create_widgets(self,parent):
      pass  

class RadioMLOption(ttk.Frame):
    def __init__(self,parent):
        super().__init__(parent)
        #ttk.Label(self,background="red").pack(expand=True,fill="both")
        #self.place(x=0,y=0,relwidth=1,height=35)
        self.pack(side="top",anchor="nw",fill="x")
        #self.config(style='2b.TFrame')

        self.columnconfigure((1,2,3,4),weight=0)
        self.rowconfigure((1),weight=1)

        self.radio_option = tk.IntVar(value=1)

        self.radio_1=ttk.Radiobutton(self, text="Erase Config",variable=self.radio_option,value=1).grid(row=1,column=1,padx=1,pady=1,sticky="w")
        self.radio_2=ttk.Radiobutton(self, text="Push Personality Only",variable=self.radio_option,value=2).grid(row=1,column=2,padx=1,pady=1,sticky="w")
        self.radio_3=ttk.Radiobutton(self, text="Push Firmware Only",variable=self.radio_option,value=3).grid(row=1,column=3,padx=1,pady=1,sticky="w")
        self.radio_4=ttk.Radiobutton(self, text="Push Both Firmware and Personality",value=4,variable=self.radio_option).grid(row=1,column=4,padx=1,pady=1,sticky="w")

    def get_radio_selection(self):
        return self.radio_option.get()

class FilePathSelection(ttk.Frame):
    def __init__(self,parent):
        super().__init__(parent)
        #ttk.Label(self,background="red").pack(expand=True,fill="both")
        #self.place(x=0,y=35,relwidth=1,height=70)
        self.pack(side="top",anchor="nw",fill="x")
        #self.config(style='2b.TFrame')

        #create grid on frame
        self.columnconfigure((1,2),weight=0)
        self.rowconfigure((1,2),weight=0)        

        #vars
        self.firmware_path = None
        self.personality_path = None
        self.firmware_path_str = tk.StringVar(value=self.firmware_path)
        self.personality_path_str = tk.StringVar(value=self.personality_path)

        #create widgets
        self.select_firmware_btn  = ttk.Button(self,text="Firmware",command=lambda: threading.Thread(target=self.get_firmware_path).start())
        self.select_personality_btn  = ttk.Button(self,text="Personality",command=lambda: threading.Thread(target=self.get_personality_path).start())
        self.firmware_label = ttk.Label(self,textvariable=self.firmware_path_str)
        self.personality_label = ttk.Label(self,textvariable=self.personality_path_str)

        #place widgets
        self.select_firmware_btn.grid(row=1,column=1,padx=2,pady=2)
        self.select_personality_btn.grid(row=2,column=1,padx=2,pady=2)
        self.firmware_label.grid(row=1,column=2,padx=2,pady=2)
        self.personality_label.grid(row=2,column=2,padx=2,pady=2)


    def get_personality_path(self):
        pPath = fd.askopenfilename()
        self.personality_path = pPath
        self.personality_path_str.set(pPath)

    def get_firmware_path(self):
        fPath = fd.askopenfilename()
        self.firmware_path = fPath
        self.firmware_path_str.set(fPath)

class DeviceDisplay(ttk.Frame):
    def __init__(self,parent):
        super().__init__(parent)
        self.pack(side="top",anchor="nw",expand=True,fill="both")
        self.config(style='2b.TFrame')

class InfoBar(ttk.Frame):
    def __init__(self,parent):
        super().__init__(parent)
        self.pack(side="top",anchor="nw",expand=True,fill="x")
        #self.config(style='2b.TFrame')

if __name__ == "__main__":
    TungstenGui()
