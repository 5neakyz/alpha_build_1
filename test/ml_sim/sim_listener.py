import threading
import logging
import time

class Listener():
    def __init__(self,device):
        self.device = device
        self.is_running = False
        self.needs_interrupt = False 
        self.buffer_txt = ""
        self.download_temp_interrupt = False
        self.stop_threads = False
        self.log = logging.getLogger('Listener')
        self.log.info(f'{device.serial_port_name}: Creating Listener Object')

    def continue_read(self):
        self.log.info(f'{self.device.serial_port_name}: continuing Listener')
        self.download_temp_interrupt = False        

    def pause_read(self):
        self.log.info(f'{self.device.serial_port_name}: Pausing Listener')
        self.download_temp_interrupt = True  

    def get_buffer(self):
        return self.buffer_txt
    
    def interrupt(self):
        self.log.info(f'{self.device.serial_port_name}: Interrupting Listener')
        self.needs_interrupt = True
        self.stop_threads = True

    def start_listening(self):
        self.log.info(f'{self.device.serial_port_name}: Starting Listener')
        threading.Thread(target=self.listening).start()

    def listening(self):
        self.is_running = True
        self.log.info(f'{self.device.serial_port_name}: Thread Started, Listening')

        while self.is_running and not self.needs_interrupt:

            if self.download_temp_interrupt:# makes listener pauseable
                time.sleep(0.5)
                continue

            line = self.device.serial_port.readline()
            if line:
                self.log.info(f'{self.device.serial_port_name}: {line}')
                threading.Thread(target=self.device.receiver,args=(line,lambda: self.stop_threads)).start()
