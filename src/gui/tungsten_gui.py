import tkinter as tk
from tkinter import ttk

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

        #style
        self.option_add("*tearOff", False) # This is always a good idea
        icon_path = self.resource_path("assests/myicon.ico")
        self.iconbitmap(icon_path)
        style_path = self.resource_path('assests/Forest-ttk-theme-master/forest-dark.tcl')
        self.tk.call('source', style_path)
        ttk.Style().theme_use('forest-dark')
        s = ttk.Style()
        s.configure('2b.TFrame', background='#2B2B2B')

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
        self.config(style='2b.TFrame')
        self.create_widgets(parent)
        self.place_widgets(parent)

    def create_widgets(self,parent):
        #create widgets
        self.run_btn  = ttk.Button(self,text="Run")
        self.connect_btn = ttk.Button(self,text="Connect")
        self.disconnect_btn = ttk.Button(self,text="Disconnect")
        self.listbox = tk.Listbox(self,listvariable=parent.list_box_items,font=('',14),height=5)
        #functions on click listbox
        self.listbox.bind('<<ListboxSelect>>', self.items_selected)

    def place_widgets(self,parent):
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
        ttk.Label(self,background="#242424").pack(expand=True,fill="both")
        self.place(x=180,y=25,relwidth=1,relheight=1)

        self.radio_ml_options = RadioMLOption(self)

    def create_widgets(self,parent):
      pass  


class RadioMLOption(ttk.Frame):
    def __init__(self,parent):
        super().__init__(parent)
        ttk.Label(self,background="red").pack(expand=True,fill="both")
        self.place(x=0,y=0,relwidth=1,height=35)

if __name__ == "__main__":
    TungstenGui()
