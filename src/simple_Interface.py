from tkinter import *
from tkinter import ttk 
from tkinter import filedialog as fd
from tkinter import font
import serial.tools.list_ports
import threading
from device import Device
from thread_runner import ThreadRunner
from pb_data import pb_data
import os
import pathlib
import time

class MyApp():
    def __init__(self, root):
        
        root.title("ML Multi Units")
        root.geometry("800x800")

# - Variables - - - - - - - - - - - - - - - - - - - - - -
        self.default_font = font.nametofont("TkDefaultFont")
        size = self.default_font.cget("size")
        self.default_font.configure(size=size+4)
        self.connected_devices = []
        self.comlist = serial.tools.list_ports.comports()
        for item in self.comlist:
            self.connected_devices.append(item.device)
        self.str_con_dev = StringVar(value=self.connected_devices)
        self.selected_devices =[]
        self.example_devices=["COM5"]
        self.SV_example_devices = StringVar(value=self.connected_devices)
        self.sltcd_devices_str = StringVar()
        self.var =IntVar(value=1)
        self.firmware_path= None
        self.firmware_path_str = StringVar(value=self.firmware_path)
        self.personality_path = None
        self.personality_path_str = StringVar(value=self.personality_path)
        self.device_objects = []
        self.hex_red = '#f5162c'
        self.hex_green = '#1df516'
        self.running_state_str = StringVar()

        #progress bar
        self.my_pb_object = pb_data()

        # self.device1_text = StringVar(value="")
        # self.device1_command = StringVar(value="")
        # self.device2_text = StringVar(value="THIS IT NOT YET IMPLEMENTED")
        # self.device2_command = StringVar(value="")
        # self.device3_text = StringVar(value="THIS IT NOT YET IMPLEMENTED")
        # self.device3_command = StringVar(value="")
        # self.device4_text = StringVar(value="THIS IT NOT YET IMPLEMENTED")
        # self.device4_command = StringVar(value="")
# - Menus - - - - - - - - - - - - - - - - - - - - - - - -
        menubar = Menu(root)

        menu_file = Menu(menubar, tearoff=0)
        menu_window = Menu(menubar, tearoff=0)
        menu_help = Menu(menubar, tearoff=0)

        menubar.add_cascade(menu=menu_file, label='File',font=self.default_font)
        menubar.add_cascade(menu=menu_window, label='Window',font=self.default_font)
        menubar.add_cascade(menu=menu_help, label='Help',font=self.default_font)

    # - File Menu - - - - - - - - - - - - - - - - - - - - - - -
        menu_file.add_separator()
    # - Window Menu - - - - - - - - - - - - - - - - - - - - - -
        menu_window.add_command(label="Zoom In", command=self.zoom_in, font=self.default_font)
        menu_window.add_command(label="Zoom Out", command=self.zoom_out, font=self.default_font)
        menu_window.add_separator()
    # - Help Menu - - - - - - - - - - - - - - - - - - - - - - -
        menu_help.add_command(label="Documentation",font=self.default_font,command=self.open_documentation)
        menu_help.add_separator()
        root.config(menu=menubar)

# - Notebook - - - - - - - - - - - - - - - - - - - - - - - - - - 
        my_notebook = ttk.Notebook(root)
        my_notebook.pack(pady=15)

        my_frame1 = Frame(my_notebook)
        # my_frame2 = Frame(my_notebook )
        # my_frame3 = Frame(my_notebook )
        # my_frame4 = Frame(my_notebook )
        # my_frame5 = Frame(my_notebook )

        my_frame1.pack(fill="both", expand=1,padx=10,pady=10)
        # my_frame2.pack(fill="both", expand=1,padx=10,pady=10)
        # my_frame3.pack(fill="both", expand=1,padx=10,pady=10)
        # my_frame4.pack(fill="both", expand=1,padx=10,pady=10)
        # my_frame5.pack(fill="both", expand=1,padx=10,pady=10)

        my_notebook.add(my_frame1,text="Main Menu")  
        # my_notebook.add(my_frame2,text="Device 1")
        # my_notebook.add(my_frame3,text="Device 2")
        # my_notebook.add(my_frame4,text="Device 3")
        # my_notebook.add(my_frame5,text="Device 4")
# - Notebook Main Menu - - - - - - - - - - - - - - - - - - - - - 
        lbox = Listbox(my_frame1,listvariable=self.str_con_dev, height=5)
        lbox.pack(padx=10, pady=10)
        #lbox.insert(END,*self.connected_devices)
        try:
            for i in range(0,len(self.example_devices),2):
                lbox.itemconfigure(i, background='#f0f0ff')
        except Exception as e: print(e)


        lbox.bind("<<ListboxSelect>>", self.selection)

        slcted_lbl = ttk.Label(my_frame1,text="Selected Devices: ").pack()
        slcted_d_lbl = ttk.Label(my_frame1,textvariable=self.sltcd_devices_str).pack()

        connect_btn = ttk.Button(my_frame1,text="Connect",command=lambda: threading.Thread(target=self.connect_to).start())
        connect_btn.pack()

        self.color_code_list = Frame(my_frame1)
        self.color_code_list.pack(padx=10, pady=10)
        

        radio_box = Frame(my_frame1)
        radio_box.pack(padx=10, pady=10)
        Radiobutton(radio_box, text="Erase Config", variable=self.var, value=1 ).grid(row=0,column=0)
        Radiobutton(radio_box, text="Push Personality Only", variable=self.var, value=2).grid(row=0,column=1)
        Radiobutton(radio_box, text="Push Firmware Only", variable=self.var, value=3).grid(row=0,column=2)
        Radiobutton(radio_box, text="Push Firmware and Personality", variable=self.var, value=4).grid(row=0,column=3)
        Radiobutton.configure

        firmware_btn = ttk.Button(my_frame1, text="Select Firmware", command=self.get_firmware).pack()
        firmware_lbl=ttk.Label(my_frame1,text="firmware path: ").pack()
        firmware_filepath_lbl = ttk.Label(my_frame1,textvariable=self.firmware_path_str).pack()

        Personality_btn = ttk.Button(my_frame1, text="Select Personality", command=self.get_personality).pack()
        Personality_lbl=ttk.Label(my_frame1,text="Personality path: ").pack()
        firmware_filepath_lbl = ttk.Label(my_frame1,textvariable=self.personality_path_str).pack()

        line_break = ttk.Label(my_frame1,text="").pack()

        line_break2 = ttk.Label(my_frame1,textvariable=self.running_state_str).pack()

        self.push_command_btn = ttk.Button(my_frame1,text="   RUN   ", state=DISABLED,command=lambda: threading.Thread(target=self.run).start())
        self.push_command_btn.pack()

        self.color_return_frame = Frame(my_frame1)
        self.color_return_frame.pack(padx=10, pady=10)

        self.disconnect_btn = ttk.Button(my_frame1,text="Disconnect",command=lambda: threading.Thread(target=self.disconnect).start())
        self.disconnect_btn.pack()

        self.progress_bar = ttk.Progressbar(my_frame1,orient=HORIZONTAL, length=500, mode='determinate')
        self.progress_bar.pack(padx=10, pady=10)
# - Notebook device1 - - - - - - - - - - - - - - - - - - - - -
        """
        not going to work on just yet, because this is going to take a while
        originally was using lits box, however there is some not so nice behavior(text formating is ugly) so i think i need to use label frame to be more "terminal like"
        """
#         device1_lbf = ttk.Labelframe(my_frame2,height=30).pack(fill = 'both')
#         device1_lb = ttk.Label(device1_lbf, textvariable=self.device1_text)
#         device1_lb.pack(fill='both',expand=False)
#         command_box1 = Frame(my_frame2)
#         command_box1.pack(padx=10, pady=10,fill='x')
#         device1_command_entry = ttk.Entry(command_box1,textvariable=self.device1_command,width=50)
#         device1_command_entry.pack(side="left")
#         device1_command_btn = ttk.Button(command_box1,text="Enter",command = lambda : self.button_press_test(1))#lambda to pass value to functions cannot otherwis
#         device1_command_btn.pack(side="right")
#         device1_help_lbl = ttk.Label(my_frame2,text="type 'esc' to send the Escape command. : Tip you can scroll in the text box").pack()
# # - Notebook device2 - - - - - - - - - - - - - - - - - - - - -
#         device2_lb = Listbox(my_frame3, listvariable=self.device2_text,height=25)
#         device2_lb.pack(fill='both',expand=False)
#         command_box2 = Frame(my_frame3)
#         command_box2.pack(padx=10, pady=10,fill='x')
#         device2_command_entry = ttk.Entry(command_box2,textvariable=self.device2_command,width=50)
#         device2_command_entry.pack(side="left")
#         device2_command_btn = ttk.Button(command_box2,text="Enter",command = lambda : self.button_press_test(2))
#         device2_command_btn.pack(side="right")
#         device2_help_lbl = ttk.Label(my_frame3,text="type 'esc' to send the Escape command. : Tip you can scroll in the text box").pack()
# # - Notebook device3 - - - - - - - - - - - - - - - - - - - - -
#         device3_lb = Listbox(my_frame4, listvariable=self.device3_text,height=25)
#         device3_lb.pack(fill='both',expand=False)
#         command_box3 = Frame(my_frame4)
#         command_box3.pack(padx=10, pady=10,fill='x')
#         device3_command_entry = ttk.Entry(command_box3,textvariable=self.device3_command,width=50)
#         device3_command_entry.pack(side="left")
#         device3_command_btn = ttk.Button(command_box3,text="Enter",command = lambda : self.button_press_test(3))
#         device3_command_btn.pack(side="right")
#         device3_help_lbl = ttk.Label(my_frame4,text="type 'esc' to send the Escape command. : Tip you can scroll in the text box").pack()
# # - Notebook device4 - - - - - - - - - - - - - - - - - - - - -
#         device4_lb = Listbox(my_frame5, listvariable=self.device4_text,height=25)
#         device4_lb.pack(fill='both',expand=False)
#         command_box4 = Frame(my_frame5)
#         command_box4.pack(padx=10, pady=10,fill='x')
#         device4_command_entry = ttk.Entry(command_box4,textvariable=self.device4_command,width=50)
#         device4_command_entry.pack(side="left")
#         device4_command_btn = ttk.Button(command_box4,text="Enter",command = lambda : self.button_press_test(4))
#         device4_command_btn.pack(side="right")
#         device4_help_lbl = ttk.Label(my_frame5,text="type 'esc' to send the Escape command. : Tip you can scroll in the text box").pack()
# - Functions - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    
    def update_progress_loop(self):
        #print("hello")
        while self.my_pb_object.progress < (self.my_pb_object.total * 0.95):
            self.progress_bar['value'] = self.my_pb_object.progress
            #print(f"value{self.my_pb_object.progress}")
            time.sleep(0.2)
            

    def update_progress(self):
        firm_size = 0
        pers_size = 0
        #print(self.firmware_path)
        if self.firmware_path != None :
            firm_size = os.stat(self.firmware_path).st_size
        if self.personality_path != None :
            pers_size = os.stat(self.personality_path).st_size
        self.my_pb_object.total = (firm_size * len(self.device_objects)) + (pers_size * len(self.device_objects))
        #print(self.my_pb_object.total)
        self.progress_bar['maximum'] = self.my_pb_object.total
        #print(f"device count{len(self.device_objects)}")
        #print("starting update loop")
        
        threading.Thread(target=self.update_progress_loop).start()

    def clear_frame(self,frame):
        for widgets in frame.winfo_children():
            widgets.destroy()

    def button_press_test(self,val):
        pass

    def open_documentation(self):
        x = pathlib.Path(__file__).parent.resolve()
        os.startfile(str(x)+"\docs.html")

    def get_personality(self):
        pPath = fd.askopenfilename()
        self.personality_path = pPath
        self.personality_path_str.set(pPath)

    def get_firmware(self):
        fPath = fd.askopenfilename()
        self.firmware_path = fPath
        self.firmware_path_str.set(fPath)
    # this function allows users to select the ports from the list box
    def selection(self,event):
        selection = event.widget.curselection()
        if selection:
            index = selection[0]
            data = event.widget.get(index)
            if data in self.selected_devices:
                (self.selected_devices.remove(data))
            else:
                (self.selected_devices.append(data))
        self.sltcd_devices_str.set(self.selected_devices)

    # accessiblilty - kinda trash tbh but kinda works(window does not resize and display all)
    def zoom_in(self):
        size = self.default_font.cget("size")
        self.default_font.configure(size=size+2)

    def zoom_out(self):
        size = self.default_font.cget("size")
        self.default_font.configure(size=max(size-2, 8))
    # connect button this is mainly for functionality of seeing if devices are alive before pushing commands,
    # also will be useful for terminal like displays for devices
    def connect_to(self):
        #reset screen
        temp_obj_list = []
        self.clear_frame(self.color_return_frame)
        self.push_command_btn.configure(state=DISABLED)
        #connect
        for ob in self.device_objects:
            temp_obj_list.append(ob.device)
        for device in self.selected_devices:
            if device not in temp_obj_list:#do not need duplicate objects, plus cant have duplicate as serial is already connected
                self.device_objects.append(Device(device))
        ##
        self.device_objects = [x for x in self.device_objects if x.device in self.selected_devices]
        #label s
        count = 0
        self.clear_frame(self.color_code_list)
        for i, object in enumerate(self.device_objects):
            color = self.hex_red
            x = object.is_alive()
            #print(f"{i} : {object.device} : is alive? : {x}")
            if x == True:
                color = self.hex_green
                count+=1
            myLabel = Label(self.color_code_list, text=object.device,bg=color)
            myLabel.grid(row=0, column=i)
        if count == len(self.device_objects) and len(self.device_objects) != 0:
            self.push_command_btn.configure(state=NORMAL)

    def disconnect(self):
        self.clear_frame(self.color_return_frame)
        self.clear_frame(self.color_code_list)
        self.device_objects = []
        for device in self.selected_devices:
            self.selected_devices.remove(device)
        self.sltcd_devices_str.set(self.selected_devices)
        self.push_command_btn.configure(state=DISABLED)


    def run(self):
        self.clear_frame(self.color_return_frame)
        self.my_pb_object.progress = 0
        self.progress_bar["value"] = 0
        self.running_state_str.set("RUNNING...")
        self.push_command_btn.configure(state=DISABLED)
        self.disconnect_btn.configure(state=DISABLED)
        my_thread = ThreadRunner(self.device_objects)
        my_thread.mode = self.var.get()#raido button list values
        my_thread.personality_path = self.personality_path
        my_thread.firmware_path = self.firmware_path
        my_thread.my_pb_object = self.my_pb_object
        #print("runing function next")
        self.update_progress()
        results = my_thread.thread_run()
        print(results)
        self.progress_bar['value'] = self.my_pb_object.total
        for i,result in enumerate(results):
            if result[1] == True:
                color = self.hex_green
            else:
                color = self.hex_red
            myLabel = Label(self.color_return_frame,text=result[0],bg=color)
            myLabel.grid(row=0,column=i)
        self.running_state_str.set("")
        self.push_command_btn.configure(state=NORMAL)
        self.disconnect_btn.configure(state=NORMAL)