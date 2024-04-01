import serial.tools.list_ports
import serial
from xmodem import XMODEM
import time
import os
import threading
import logging
import concurrent.futures

class SerialPortManger():
    def __init__(self,comport_name):# device is string like "COM6"
        self.serial_connection = False
        self.is_running = False
        self.serial_port = None
        self.serial_port_name = comport_name
        self.serial_port_baud = 115200
        # Create a byte array to store incoming data
        self.serial_port_buffer = bytearray()

        try:
            self.serial_port = serial.Serial(self.serial_port_name, self.serial_port_baud, timeout=0.050)
        except Exception:
            logging.info("SERIAL IN USE")#probably
            self.serial_connection=False

    def disconnect(self):
        self.serial_port.close()

class Device(SerialPortManger):
    def __init__(self,parent):
        super().__init__(parent)

    def write_commands(self,commands):
        for i, command in enumerate(commands):
            if command =="esc":
                command = (chr(27))
            
            try:
                self.serial_port.write(command.encode())
            except Exception as e: print(e)

            if commands[i] != commands[-1]:# if last command in commands do not load menu so i can view it else where
                self.serial_port.readlines()# waits for the menu to load, needed other wise commands get sent too fast for the ML

    def ml_read(self):
        for _ in range(100):
            lines = self.serial_port.readline()
            print(lines)

class DeviceHandler():
    def __init__(self,*devices):
        super().__init__()
        self.devices = devices
        self.is_running = False
        self.needs_interrupt = False 
 
    def continuous_read(self,device):
        '''
        '''
        self.is_running = True
        logging.info(f'Thread Started for: {device.serial_port_name}')

        while self.is_running and not self.needs_interrupt:
            print(device.readline())


    def begin_continuous_read(self):
        results = []
        with concurrent.futures.ThreadPoolExecutor() as executor:# parallelism 
            tasks = [executor.submit(self.continuous_read,device) for device in self.devices]
            for x in concurrent.futures.as_completed(tasks):
                results.append(x.result())
        return results

    def interrupt(self):
        print("interrupting")
        self.needs_interrupt = True


if __name__ == '__main__':

    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO,
                        datefmt="%H:%M:%S")
    
    unit = Device("COM5")
    
    thread_handler = DeviceHandler(unit)
    #print(thread_handler.begin_continuous_read())
    threading.Thread(target=thread_handler.begin).start()

    time.sleep(3)
    thread_handler.interrupt()





