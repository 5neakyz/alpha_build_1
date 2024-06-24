
import serial.tools.list_ports
import serial
from xmodem import XMODEM
import time
import os
import threading
import logging
import concurrent.futures

"""
basic (trash) simulator of an ML unit for testing purposes

COM 0 COM
virtual com connections between
home pc
COM3 - COM4

Sim - COM3 
Tera Term - COM4 

"""

class ML_Sim():
    def __init__(self):
        self.serial_connection = False
        self.is_running = False
        self.serial_port = None
        self.serial_port_name = "COM3"
        self.serial_port_baud = 115200

        try:
            self.serial_port = serial.Serial(port = self.serial_port_name, baudrate=self.serial_port_baud, timeout=2)
        except Exception:
            logging.info("SERIAL IN USE")#probably
            self.serial_connection=False

        logging.info(f'Connection Established: {self.serial_port_name}')

    def disconnect(self):
        self.serial_port.close()

    def output(self):
            self.serial_port.write(b'\x1b\Hello\r\r\n')


class Listener():
    def __init__(self,parent):
        super().__init__(parent)
        self.is_running = False
        self.needs_interrupt = False 

    def interrupt(self,parent):
        logging.info(f'Interrupting Listener')
        self.needs_interrupt = True

    def listening(self,parent):
        self.is_running = True
        logging.info(f'Thread Started, Listening: {parent.serial_port_name}')

        while self.is_running and not self.needs_interrupt:
            time.sleep(0.05)
            lines = self.ser.readlines()
            if not lines: continue
            print(lines)

    def start_listening(self,parent):
        thread = threading.Thread(target=self.listening)
        thread.start()

if __name__ == '__main__':

    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO,
                        datefmt="%H:%M:%S")
    
    x = ML_Sim()
    x.output()
