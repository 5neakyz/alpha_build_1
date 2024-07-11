
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
        self.listener = Listen()
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


class Listen():
    def __init__(self):
        logging.info(f'creating Listener')
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
        logging.info(f'Thread Started, Listening: {device.serial_port_name}')

        while self.is_running and not self.needs_interrupt:
            line = device.serial_port.readline()
            logging.info(f'{device.serial_port_name} : {line}')
            #print(f'{device.serial_port_name} : {line}')

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

if __name__ == '__main__':

    #self.button.clicked.connect(self.copy_text)

    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO,
                        datefmt="%H:%M:%S")
    print(f'setup unit')
    sg14 = Device("COM4")
    #ml30 = Device("COM13")
    # listener = Listener(sg14,ml30)
    # t = threading.Thread(target=listener.start_listening)
    # t.start()
    time.sleep(1)
    # print(f'sending command')
    # sg14.write_commands(["esc","4"])
    # ml30.write_commands(["esc","4"])
    time.sleep(15)
    # listener.interrupt()


