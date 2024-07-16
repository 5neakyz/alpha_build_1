import tkinter as tk
import time
import threading
import logging

class NotebookHandler():
    def __init__(self,labels,devices):
        logging.info(f'Creating Notebook Handler')

        self.labels = labels
        self.devices = devices

        self.is_running = False
        self.needs_interrupt = False 

    def start_handler(self):
        self.is_running = True
        logging.info(f'Starting NB Handler')
        for device in self.devices:
            i = self.devices.index(device)
            label = self.labels[i]
            threading.Thread(target=self.handler, args=(label,device)).start()

    def interrupt(self):
        logging.info(f'Interrupting NB Handler')
        self.needs_interrupt = True

    def handler(self,label,device):
        logging.info(f'{device.serial_port_name}: NB Thread Started')
        while self.is_running and not self.needs_interrupt:
            serialPortBuffer = device.listener.get_buffer()
            # Update textbox in a kind of recursive function using Tkinter after() method
            label.delete('1.0',tk.END)
            label.insert(tk.INSERT, serialPortBuffer)
            # autoscroll to the bottom
            #label.see(tk.END)
            # Recursively call recursive_update_textbox using Tkinter after() method
            time.sleep(1)    