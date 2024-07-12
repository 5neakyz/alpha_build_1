
import serial.tools.list_ports
import serial
from xmodem import XMODEM
import time
import os
import threading
import logging
import concurrent.futures

class SerialPortManger():
    def __init__(self,comport_name):
        self.serial_connection = False
        self.serial_port = None
        self.serial_port_name = comport_name
        self.serial_port_baud = 115200

        try:
            self.serial_port = serial.Serial(port = self.serial_port_name, baudrate=self.serial_port_baud, timeout=2)
            self.serial_connection = True
            logging.info(f'Connection Established: {self.serial_port_name}')
        except Exception:
            logging.info("SERIAL IN USE")#probably
            self.serial_connection=False


    def disconnect(self):
        self.serial_port.close()

class Device(SerialPortManger):
    def __init__(self,parent):
        super().__init__(parent)

        #only creates listener if there is connection
        if self.serial_connection:
            logging.info(f'1')
            self.listener = Listen(self)
            self.listener.start_listening()

    def is_alive (self):
        if self.serial_connection == True:
            return True
        return False

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


class Listener():
    def __init__(self,*devices):
        super().__init__()
        self.devices = devices
        self.is_running = False
        self.needs_interrupt = False 

    def interrupt(self):
        logging.info(f'Interrupting Listener')
        self.needs_interrupt = True

    def listening(self,device):
        logging.info(f'Listening')
        self.is_running = True
        logging.info(f'Thread Started, Listening: {device.serial_port_name}')

        while self.is_running and not self.needs_interrupt:
            line = device.serial_port.readline()
            logging.info(f'{device.serial_port_name} : {line}')
            #print(f'{device.serial_port_name} : {line}')
    
    def start_listening(self):
        logging.info(f'Starting Listener')
        results = []
        with concurrent.futures.ThreadPoolExecutor() as executor:# parallelism 
            tasks = [executor.submit(self.listening,device) for device in self.devices]
            for x in concurrent.futures.as_completed(tasks):
                results.append(x.result())
        return results
    
    def format_readlines(self,lines):
        output = ''

        for line in lines:
            text = line.strip().replace(b'\t', b'').replace(b'\n',b'').replace(b'\r',b'').replace(b'\x1b',b'').replace(b'\xfe',b'')
            try:
                output +=(text.decode('utf-8')+ ' \n')
            except Exception as e: print(e,text)

        return output