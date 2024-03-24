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
#my classes
from thread_runner import ThreadRunner
from pb_data import pb_data
from device import Device

class Multi_Stager_Gui():
    def __init__(self,root):
# - - - gui config - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
        self.root_window = root
        self.root_window.title("ML Multi Units")
        icon_path = self.resource_path("gui/assests/myicon.ico")
        self.root_window.iconbitmap(icon_path)
        #self.root_window.geometry("600x600")
        self.root_window.option_add("*tearOff", False) # This is always a good idea
        # Import the tcl file
        #self.root_window.tk.call('source', 'Forest-ttk-theme-master/forest-dark.tcl')
        style_path = self.resource_path('gui/assests/Forest-ttk-theme-master/forest-dark.tcl')
        self.root_window.tk.call('source', style_path)
        # Set the theme with the theme_use method
        ttk.Style().theme_use('forest-dark')
        #i think if a thread is running while closing the window the the object will remained connected
        self.root_window.protocol("WM_DELETE_WINDOW",self.close_window)
        # Make the app responsive
        self.root_window.columnconfigure(index=0, weight=1)
        self.root_window.columnconfigure(index=1, weight=1)
        self.root_window.columnconfigure(index=2, weight=1)
        self.root_window.rowconfigure(index=0, weight=1)
        self.root_window.rowconfigure(index=1, weight=1)
        self.root_window.rowconfigure(index=2, weight=1)

 # - - - vars - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        
        #returnes a lit of all com ports and infor
        self.comlist = serial.tools.list_ports.comports()
        #needed to just get com ports name(.device)
        self.COM_items = []
        for item in self.comlist:
            self.COM_items.append(item.device)
        self.COM_items.sort()
        self.selected_coms = []
        # for display purposes
        self.selected_coms_str = tk.StringVar(value=self.selected_coms)
        self.com_objects = []

        self.my_pb_object = pb_data()

        self.firmware_path= None
        self.personality_path = None
        self.firmware_path_str = tk.StringVar(value=self.firmware_path)
        self.personality_path_str = tk.StringVar(value=self.personality_path)

        self.hex_red = '#b40d1b'
        self.hex_green = '#217346'

        self.are_com_objects_usable = False


# - Menus - - - - - - - - - - - - - - - - - - - - - - - -
        menubar = tk.Menu(root)

        menu_settings = tk.Menu(menubar, tearoff=0)
        # menu_window =tk. Menu(menubar, tearoff=0)
        # menu_help = tk.Menu(menubar, tearoff=0)

        menubar.add_cascade(menu=menu_settings, label='Settings')
        # menubar.add_cascade(menu=menu_window, label='Window')
        # menubar.add_cascade(menu=menu_help, label='Help')

        #menubar.add_command(label="More?",command=self.toggle_unit_info_display)
        menubar.add_command(label="3: View Config",command = lambda: threading.Thread(target=self.get_unit_info("config")).start())
        menubar.add_command(label="4: Status Screen",command=lambda: threading.Thread(target=self.get_unit_info("status")).start())
        menubar.add_command(label="F: Prod TS",command=lambda: threading.Thread(target=self.get_unit_info("prodts")).start())

        menu_settings.add_command(label="Toggle Info",command=self.toggle_unit_info_display)
        #menu_settings.add_command(label="baudrate")
        menu_settings.add_command(label="Github",command=lambda: threading.Thread(target=self.open_github('https://github.com/5neakyz/Multi-ML-1.0')).start())


        self.root_window.config(menu=menubar)


#- - - -device selection - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        self.device_selection_frame = ttk.LabelFrame(self.root_window,text="Select Devices")
        self.device_selection_frame.grid(row=0, column=0, padx=(20, 10), pady=10, sticky="nsew")

        ##list box
        self.list_box_items = tk.Variable(value=self.COM_items)

        self.listbox = tk.Listbox(
            self.device_selection_frame,
            listvariable=self.list_box_items,
            font=('',14),
            height=6)

        self.listbox.pack(padx=10, pady=10,expand=True,fill="x")
        # alternate line colors
        try:
            for i in range(0,len(self.COM_items),2):
                self.listbox.itemconfigure(i, background='#242424')
        except Exception as e: print(e)

        #when list box item is clicked run fucntion items_selected
        self.listbox.bind('<<ListboxSelect>>', self.items_selected)

        #display selected devices
        self.selected_devices_frame= ttk.LabelFrame(self.device_selection_frame,text="Selected Devices")
        self.selected_devices_frame.pack(padx=10, pady=10,expand=True,fill="x")
        self.selected_devices_placeholder = ttk.Label(self.selected_devices_frame,textvariable=self.selected_coms_str,wraplength=250)
        self.selected_devices_placeholder.pack(padx=10, pady=10)

        # select devices buttons
        #we use the lambda function for threading so the app still works while the button is running
        self.connect_device_btn = ttk.Button(self.device_selection_frame, text="Connect",command=lambda: threading.Thread(target=self.connect_btn_press).start())
        self.connect_device_btn.pack(padx=10,pady=10,expand=True,anchor="s",side="left")

        self.disconnect_device_btn = ttk.Button(self.device_selection_frame, text="Disconnect",command=lambda: threading.Thread(target=self.disconnect_btn_press).start())
        self.disconnect_device_btn.pack(padx=10,pady=10,expand=True,anchor="s",side="left")

# - - - radio box - config type/ option - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        self.radio_option = tk.IntVar(value=1)
        #box for config options
        self.config_options_frame = ttk.LabelFrame(self.root_window,text="Config Options")
        self.config_options_frame.grid(row=0, column=1, padx=(20, 10), pady=10, sticky="nsew")
        #config options
        self.radio_1=ttk.Radiobutton(self.config_options_frame, text="Erase Config",variable=self.radio_option,value=1).pack(padx=5, pady=5,anchor="w")
        self.radio_2=ttk.Radiobutton(self.config_options_frame, text="Push Personality Only",variable=self.radio_option,value=2).pack(padx=5, pady=5,anchor="w")
        self.radio_3=ttk.Radiobutton(self.config_options_frame, text="Push Firmware Only",variable=self.radio_option,value=3).pack(padx=5, pady=5,anchor="w")
        self.radio_4=ttk.Radiobutton(self.config_options_frame, text="Push Both Firmware and Personality",value=4,variable=self.radio_option).pack(padx=5, pady=5,anchor="w")

# - - - file selection - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        self.select_files_frame = ttk.LabelFrame(self.root_window,text="Select Files")
        self.select_files_frame.grid(row=1, column=0,padx=(20, 10), pady=10, sticky="nsew")

        self.selected_firmwware_frame=ttk.LabelFrame(self.select_files_frame,text="Firmware Path")
        self.selected_firmwware_frame.pack(padx=10,pady=5,expand=True,fill="x")

        self.firmware_placeholder = ttk.Label(self.selected_firmwware_frame,textvariable=self.firmware_path_str,wraplength=250)
        self.firmware_placeholder.pack(padx=10,pady=5)

        self.selected_personality_frame=ttk.LabelFrame(self.select_files_frame,text="Personality Path")
        self.selected_personality_frame.pack(padx=10,pady=5,expand=True,fill="x")

        self.personality_placeholder = ttk.Label(self.selected_personality_frame,textvariable=self.personality_path_str,wraplength=250)
        self.personality_placeholder.pack(padx=10,pady=5)

        self.slct_firm_path_btn = ttk.Button(self.select_files_frame,text="Select Firmware",command=self.get_firmware_path)
        self.slct_firm_path_btn.pack(padx=10,pady=10,expand=True,anchor="s",side="left")

        self.slct_pers_path_btn = ttk.Button(self.select_files_frame,text="Select Personality",command=self.get_personality_path)
        self.slct_pers_path_btn.pack(padx=10,pady=10,expand=True,anchor="s",side="left")

# - - - Run Frame - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
        self.run_frame = ttk.LabelFrame(self.root_window,text="Run")
        self.run_frame.grid(row=1, column=1,padx=(20, 10), pady=10, sticky="nsew")


        self.results_frame = ttk.LabelFrame(self.run_frame,text="Results")
        self.results_frame.pack(padx=5,pady=5,expand=True,fill="x")

        self.results_placeholder = ttk.Label(self.results_frame,text="No results")
        self.results_placeholder.pack(padx=10, pady=10,expand=True,anchor="n")

        self.progress_bar = ttk.Progressbar(self.run_frame,orient='horizontal', length=250, mode='determinate')
        self.progress_bar.pack(padx=10, pady=10,expand=True)

        self.run_btn = ttk.Button(self.run_frame,text="Run",state="disabled",command=lambda: threading.Thread(target=self.run_btn_press).start())
        self.run_btn.pack(padx=10, pady=10,expand=True,anchor="sw",side="left")

# - - - Notebook (unit info)(work in progress) - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        '''this is dynamically generated see functions below
        '''
        self.notebook = ttk.Notebook(self.root_window,width=350)
        self.notebook.grid(row=0,column=2,columnspan=1,sticky="nsew", rowspan=3,padx=10,pady=10,)
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


# - Notebook (unit info) Functions - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
    def toggle_unit_info_display(self):
        if self.notebook.grid_info() == {}:
            self.root_window.columnconfigure(index=2, weight=1)
            self.notebook.grid(row=0,column=2,columnspan=1,sticky="nsew", rowspan=3,padx=10,pady=10,)
        else:
            self.root_window.columnconfigure(index=2, weight=0,minsize=0)
            self.notebook.grid_forget()

    def read_unit_info(self,device):
        if self.unit_info_option == "config":
            return device.read_config()
        if self.unit_info_option == "status":
            return device.read_status()
        if self.unit_info_option == "prodts":
            return device.prod_test_screen()
        return False

    def populate_unit_info(self,mode=None):
        self.clear_child_in_frame(self.notebook)
        self.unit_info_option = mode
        #spawns threadpool to check all units at once , costly startup time
        results = self.create_threadpool(self.read_unit_info,self.com_objects)
        for result in results: # populates display
            new_pad = ttk.Frame(self.notebook)
            self.notebook.add(new_pad,text=result[0])
            label = tk.Text(new_pad)
            label.pack(fill="both",expand=True)
            label.insert("end",result[1])

    def get_unit_info(self,mode="config"):
        if not self.com_objects or not self.are_com_objects_usable:
            self.clear_child_in_frame(self.notebook)
            return
        self.set_btns_disabled(self.connect_device_btn,self.disconnect_device_btn,self.run_btn)
        self.populate_unit_info(mode)
        self.set_btns_normal(self.connect_device_btn,self.disconnect_device_btn,self.run_btn)
# - BUTTON PRESSES - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

    # list box func, runs on item click
    # gets selected item and adds to two lists
    # one we use and one Tkinter uses to display
    def items_selected(self,event):
        #selected_indices = self.listbox.curselection()[0]#returns a list, you can select multiple
        try:
            selected_item = event.widget.get(self.listbox.curselection()[0])
            if selected_item in self.selected_coms:
                (self.selected_coms.remove(selected_item))
            else:
                (self.selected_coms.append(selected_item))
            self.selected_coms_str.set(self.selected_coms)
        except Exception as e: print(e)

    def connect_btn_press(self):
        self.set_btns_disabled(self.connect_device_btn,self.disconnect_device_btn,self.run_btn)
        self.selected_devices_frame.configure(text="Connecting")
        #check to see if any objects already exist,if no objects then temp list is skipped
        temp_obj_list = []#need a temp list as need .device attribute of the objects
        for ob in self.com_objects:
            temp_obj_list.append(ob.device)
        #creates the objects and adds them to com object list , skips dupes
        for device in self.selected_coms:
            if device not in temp_obj_list:
                self.com_objects.append(Device(device))
        #list comprehension is needed to remove objects of COMs that are no longer selected
        self.com_objects = [x for x in self.com_objects if x.device in self.selected_coms]

        '''using concurrent threading to check if we can connect to units being able to connect is being able to read the main menu
        it will fail if we cant even establish a serial connection this does mean that if, say a units voltage is too low it will count as fail
        but will not given reasons why '''

        results = self.create_threadpool(self.is_connection_live,self.com_objects)

        #display
        self.clear_child_in_frame(self.selected_devices_frame)#remove selected devices for results of connection
        # now we iterate through our results, to add to gui object[0] is com port, [1] is true or false
        self.display_results(self.selected_devices_frame,results)
        #re enable buttons and change label frame state
        if any(False in result for result in results) == True or len(results) == 0:
            self.set_btns_normal(self.connect_device_btn,self.disconnect_device_btn)
            self.are_com_objects_usable = False
        else:
            self.set_btns_normal(self.connect_device_btn,self.disconnect_device_btn,self.run_btn)
            self.are_com_objects_usable = True
        self.selected_devices_frame.configure(text="Selected Devices")

    def disconnect_btn_press(self):
        #empty selected coms and update tkinter string
        self.selected_coms.clear()
        self.com_objects.clear()
        self.selected_coms_str.set(self.selected_coms)
        self.clear_child_in_frame(self.selected_devices_frame)
        self.set_btns_disabled(self.run_btn)
        self.selected_devices_placeholder = ttk.Label(self.selected_devices_frame,textvariable=self.selected_coms_str,wraplength=250)
        self.selected_devices_placeholder.pack(padx=10, pady=10)

    def run_btn_press(self):
        #update gui
        self.clear_child_in_frame(self.results_frame)
        self.set_btns_disabled(self.connect_device_btn,self.disconnect_device_btn,self.run_btn)
        self.my_pb_object.progress = 0
        self.progress_bar["value"] = 0
        self.results_frame.config(text="Running...")
        #start
        my_thread = ThreadRunner(self.com_objects)
        my_thread.mode = self.radio_option.get()#radio button list values
        my_thread.personality_path = self.personality_path
        my_thread.firmware_path = self.firmware_path
        my_thread.my_pb_object = self.my_pb_object
        self.update_progress()
        results = my_thread.thread_run()
        #end
        print(results)
        self.progress_bar['value'] = self.my_pb_object.total
        self.display_results(self.results_frame,results)

        self.results_frame.config(text="Results")
        self.set_btns_normal(self.connect_device_btn,self.disconnect_device_btn,self.run_btn)
        #force update progress bar. it works poorly when just eraseing or just pushing personaility 
        self.progress_bar['maximum'] = 100
        self.progress_bar["value"] = 100

# - FUNCTIONS - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def create_threadpool(self,function,items):
        results = []
        with concurrent.futures.ThreadPoolExecutor() as executor:# parallelism 
            tasks = [executor.submit(function,item) for item in items]
            for x in concurrent.futures.as_completed(tasks):
                results.append(x.result())
        return results


    def resource_path(self,relative_path):
        """ Get absolute path to resource, works for dev and for PyInstaller """
        base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
        return os.path.join(base_path, relative_path)

    def set_btns_disabled(self,*buttons):
        for button in buttons:
            button.configure(state="disabled")

    def set_btns_normal(self,*buttons):
        for button in buttons:
            button.configure(state="normal")

    def toggle_btn_state(self,*buttons):
        for button in buttons:
            if str(button['state']) == 'normal':
                button.config(state=tk.DISABLED)
            else:
                button.config(state=tk.NORMAL)

    #destroys anything that is a child of the given frame
    def clear_child_in_frame(self,*frames):
        for frame in frames:
            for widgets in frame.winfo_children():
                widgets.destroy()

    def display_results(self,parent_label,results):
    # Result[0] (string) = COM PORT
    # Result[1] (bool)= outcome
        for result in (results):
            if result[1] == True:
                color = self.hex_green
            else:
                color = self.hex_red
            label = ttk.Label(parent_label,text=result[0],background=color)
            label.pack(padx=10, pady=10,expand=True,anchor="n",side="left")


    def is_connection_live(self,com_object):
        return com_object.device,com_object.is_alive()


    def get_personality_path(self):
        pPath = fd.askopenfilename()
        self.personality_path = pPath
        self.personality_path_str.set(pPath)

    def get_firmware_path(self):
        fPath = fd.askopenfilename()
        self.firmware_path = fPath
        self.firmware_path_str.set(fPath)


    def update_progress_loop(self):
        while self.my_pb_object.progress < (self.my_pb_object.total * 0.95):
            self.progress_bar['value'] = self.my_pb_object.progress
            time.sleep(0.1)
            

    def update_progress(self):
        if self.firmware_path == None and self.personality_path == None:
            return
        firm_size = 0
        pers_size = 0
        if self.firmware_path != None :
            firm_size = os.stat(self.firmware_path).st_size
        if self.personality_path != None :
            pers_size = os.stat(self.personality_path).st_size
        self.my_pb_object.total = (firm_size * len(self.com_objects)) + (pers_size * len(self.com_objects))
        self.progress_bar['maximum'] = self.my_pb_object.total

        threading.Thread(target=self.update_progress_loop).start()#thread will auto close on completion

    def open_github(self,url):
        webbrowser.open(url)

    def close_window(self):
        self.com_objects.clear()
        self.root_window.destroy()

if __name__ == '__main__':
    format = "%(asctime)s.%(msecs)04d: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO,
                        datefmt="%H:%M:%S")
    app = Multi_Stager_Gui(tk.Tk())