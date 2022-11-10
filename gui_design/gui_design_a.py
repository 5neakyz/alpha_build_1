import tkinter as tk
from tkinter import ttk


if __name__ == '__main__':
    root = tk.Tk()
    # MyApp(root)
    # root.mainloop()
    root.title("ML Multi Units")
    root.geometry("600x600")

    # Import the tcl file

    # Set the theme with the theme_use method
    selected_config_option = tk.IntVar(value=2)
    selected_config_option.set(2)
    
    config_options = ttk.LabelFrame(root,text="not in function")
    config_options.grid(row=2, column=2, padx=(20, 10), pady=10, sticky="nsew")

    radio_1 = ttk.Radiobutton(config_options, text="1",variable=selected_config_option,value=1)
    radio_1.grid(row=0, column=0, padx=5, pady=10, sticky="nsew")

    radio_2 = ttk.Radiobutton(config_options, text="2",variable=selected_config_option,value=2)
    radio_2.grid(row=1, column=0, padx=5, pady=10, sticky="nsew")

    radio_3 = ttk.Radiobutton(config_options, text="3",variable=selected_config_option,value=3)
    radio_3.grid(row=2, column=0, padx=5, pady=10, sticky="nsew")

    radio_4 = ttk.Radiobutton(config_options, text="4",variable=selected_config_option,value=4)
    radio_4.grid(row=3, column=0, padx=5, pady=10, sticky="nsew")

    # vars
    def rad (selected_config_option1):


        config_options1 = ttk.LabelFrame(root,text="in function")
        config_options1.grid(row=2, column=1, padx=(20, 10), pady=10, sticky="nsew")

        radio_11 = ttk.Radiobutton(config_options1, text="1",variable=selected_config_option1,value=1)
        radio_11.grid(row=0, column=0, padx=5, pady=10, sticky="nsew")

        radio_22 = ttk.Radiobutton(config_options1, text="2",variable=selected_config_option1,value=2)
        radio_22.grid(row=1, column=0, padx=5, pady=10, sticky="nsew")

        radio_33 = ttk.Radiobutton(config_options1, text="3",variable=selected_config_option1,value=3)
        radio_33.grid(row=2, column=0, padx=5, pady=10, sticky="nsew")

        radio_44 = ttk.Radiobutton(config_options1, text="4",variable=selected_config_option1,value=4)
        radio_44.grid(row=3, column=0, padx=5, pady=10, sticky="nsew")


    rad(selected_config_option)
    root.mainloop()