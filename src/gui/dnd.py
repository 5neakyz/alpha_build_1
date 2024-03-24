import customtkinter
import tkinter as tk
from tkinter import ttk


class Gui():
    def __init__(self,root):
# Menu Bar
        self.root_window = root
        self.root_window.title("ML Multi Units")
        self.root_window.geometry("600x600")
        #self.root_window.option_add("*tearOff", False) # This is always a good idea
        # Import the tcl file
        #self.root_window.tk.call('source', 'Forest-ttk-theme-master/forest-dark.tcl')
        # Set the theme with the theme_use method
        #i think if a thread is running while closing the window the the object will remained connected
        #self.root_window.protocol("WM_DELETE_WINDOW",self.close_window)
        # Make the app responsive

        menu_bar = tk.Menu(self)
        m1 = tk.Menu(menu_bar, tearoff=0)
        m1.add_command(label="Open File",command=self.open_file)
        m1.add_separator()
        m1.add_command(label="Save File",command=lambda : self.save_final(0))
        self.config(menu=menu_bar)

        menu_bar.add_cascade(label="File",menu=m1)
        m2 = tk.Menu(menu_bar, tearoff=0)
        m2.add_command(label="Light theme",command=lambda : self.theme_selection(0))
        m2.add_command(label="Dark theme",command=lambda : self.theme_selection(1))
        m2.add_separator()
        m2.add_command(label="System theme",command=lambda : self.theme_selection(2))
        self.config(menu=menu_bar)
        menu_bar.add_cascade(label="Setting",menu=m2)
        
        m3 = tk.Menu(menu_bar, tearoff=0)
        m3.add_command(label="help!",command=lambda : self.help_us())

        self.config(menu=menu_bar)
        menu_bar.add_cascade(label="Help",menu=m3)
        
        
        # configure grid layout (4x4)
        # self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=1)
        self.grid_rowconfigure((1, 2), weight=1)
        
        # Creating Side Bar Button here
        self.Left_Side_Bar_Button()
        
        # search Bar with Button 
        self.search_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.search_frame.grid(row=0, column=1, sticky="nw")
        self.search_frame.grid_rowconfigure(2, weight=1)
        self.search_bar_entry = customtkinter.CTkEntry(self.search_frame, placeholder_text="Search", width=200, corner_radius=0,fg_color="#fafafa", text_color="#000000")
        self.search_bar_entry.grid(row=0, column=0, sticky="nw", pady=15)
        self.bind('<Return>', self.update_row)


app = Gui(tk.Tk())
app.mainloop()