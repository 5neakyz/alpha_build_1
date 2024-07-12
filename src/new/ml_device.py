
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
            self.serial_port = serial.Serial(port = self.serial_port_name, baudrate=self.serial_port_baud, timeout=0.05)
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
            self.listener = Listener(self)
            self.listener.start_listening()

    def is_alive (self):
        if self.serial_connection == True:
            for _ in range(1):
                self.write_commands(["esc"])
                time.sleep(0.5)
                x = self.listener.get_buffer()
                if "Main Menu" in str(x):
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
    def __init__(self,device):
        logging.info(f'creating Listener')
        self.device = device
        self.is_running = False
        self.needs_interrupt = False 
        self.buffer_txt = ""

    def get_buffer(self):
        return self.buffer_txt
    
    def interrupt(self):
        logging.info(f'Interrupting Listener')
        self.needs_interrupt = True

    def start_listening(self):
        logging.info(f'Starting Listener')
        threading.Thread(target=self.listening).start()

    def listening(self):
        self.is_running = True
        logging.info(f'Thread Started, Listening: {self.device.serial_port_name}')

        while self.is_running and not self.needs_interrupt:
            # line = self.device.serial_port.readline()
            # if line:
            #     logging.info(f'{self.device.serial_port_name} : {line}')

            lines = self.device.serial_port.readlines()
            if lines:
                self.buffer_txt = lines
                logging.info(f'{self.device.serial_port_name} : {self.format(lines)}')

    def format(self,byte_array_list):
        output = ""
        for line in byte_array_list:
            stripped = line.strip().replace(b'\t', b' ').replace(b'\r',b' ').replace(b'\x1b',b'').replace(b'\n',b'').replace(b'[2J',b'')
            if stripped:
                output += stripped.decode("utf-8") + '\n'
        return output
    
if __name__ == '__main__':

    #self.button.clicked.connect(self.copy_text)

    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO,
                        datefmt="%H:%M:%S")
    print(f'setup unit')
    sg14 = Device("COM19")
    time.sleep(1)
    print(f'ALIVE?: {sg14.is_alive()}')
    time.sleep(1)
    sg14.write_commands(['esc','4'])
    time.sleep(10)
    sg14.listener.interrupt()


