
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

class SerialPortManger():
    def __init__(self,comport_name):
        self.serial_connection = False
        self.serial_port = None
        self.serial_port_name = comport_name
        self.serial_port_baud = 115200

        try:
            self.serial_port = serial.Serial(port = self.serial_port_name, baudrate=self.serial_port_baud, timeout=0.05)
            self.serial_connection = True
            logging.info(f'{self.serial_port_name}: Connection Established')
        except Exception:
            logging.info("CANNOT CONNECT")
            self.serial_connection=False

    def disconnect(self):
        logging.info(f'{self.serial_port_name}: Disconnected')
        self.serial_port.close()

class Device(SerialPortManger):
    def __init__(self,parent):
        super().__init__(parent)
        logging.info(f'{self.serial_port_name}: Creating Device Object')
        #only creates listener if there is connection
        if self.serial_connection:
            self.listener = Listener(self)
            self.listener.start_listening()

    def is_alive (self):
        if self.serial_connection:
            for _ in range(1):
                self.write_commands(["esc"])
                time.sleep(0.5)
                x = self.listener.get_buffer()
                if "Main Menu" in str(x):
                    logging.info(f'{self.serial_port_name}: is Alive')
                    return True
        return False

    def erase_config(self):
        if self.serial_connection:
            for _ in range(5):
                if self.is_alive():
                    break
            else: return False
            self.write_commands(["esc","9","h","y"])
            time.sleep(0.5)
            return True
        return False

    def write_commands(self,commands):
        if self.serial_connection:
            logging.info(f'{self.serial_port_name}: Sending Command(s): {commands}')
            for command in (commands):
                if command =="esc":
                    command = (chr(27))
                command = "command"+command   
                try:
                    self.serial_port.write(command.encode())
                except Exception:
                    logging.info(f'{self.serial_port_name}: Failed Sending Commands')
                    return False
            return True
        return False

class Listener():
    def __init__(self,device):
        logging.info(f'{device.serial_port_name}: Creating Listener Object')
        self.device = device
        self.is_running = False
        self.needs_interrupt = False 
        self.buffer_txt = ""
        self.mainmenu = [b'[2J\r\t\t\tMain Menu\r\r\n',
                    b'\r\n',
                    b'\n',
                    b'1 - one \r\n',
                    b'2 - two\r\n',
                    b'3 - three\r\n',
                    b'4 - four\r\n',
                    b'5 - five\r\n',
                    b'6 - six\r\n',
                    b'7 - seven\r\n',
                    b'8 - eight\r\n',
                    b'9 - nine\r\n',
                    b'\n'
                    b'Enter >']
        self.status = [b'\x1b[2'
                        b'J\r\t\t\tStatus Screen\r\n'
                        b'\r\n'
                        b'MTU4 Time\t:30/03/24,14:41:13 \tUptime: 01:25:12\r\n'
                        b'IMEI\t\t:\tTelit 864: 10.01.020\r\n'
                        b'Ver\t\t:3.90.2\tcrc 0x96c0 size:545436\r\n'
                        b'Sig Q\t\t:255 = 0 Percent \r\n'
                        b'GPRS\t\t:Trying\r\n'
                        b'IP\t\t:\r\n'
                        b'IMSI\t\t:\r\n'
                        b'ICCID\t\t:\r\n'
                        b'SRVR\t\t:172.17.144.97\t\tNot Connected \t5432\r\n'
                        b'Power Retain\t:7200\tSleep: 43200=0\tRe-try: 6 \r\n'
                        b'VIN\t\t:                 \tDriverId :Unknown\r\n'
                        b'VRN\t\t:               \r\n'
                        b'\r\n'
                        b'GPSVer\t\t:HW:00040007\tSW:7.03 (45969)\r\n'
                        b'Latitude\t: 53.03206253\tPower\t\t:On (24.81v)\r\n'
                        b'Longitude\t: -1.46555280\tIgnition\t:On\r\n'
                        b"GPSFix\t\t:TRUE FC 25  \tCh1 'Camera'\t:Low\t(DPD)\r\n"
                        b"Num Sats\t:8\t\tCh2 'Unknown'\t:High\t(DPU)\r\n"
                        b"Speed\t\t:  0.275948\tCh3 'Unknown'\t:High\t(DPU)\r\n"
                        b"Course\t\t:  0.000000\tCh4 'PTO'\t:High\t(DPU)\r\n"
                        b'Distance\t:0000010301\tShut Down\t:7200s\r\n'
                        b'GPS Antenna\t:0\t\tBatt Capacity\t:unknown (3.78v)\r\n'
                        b'GPS err (fHacc)\t:6.30\t\tCharge State\t:Fault\r\n'
                        b'GPS AvCNO\t:22.00\t\tBT name\t\t:MTU4-728670\r\n'
                        b'GPS err (HDOP)\t:0.96\r\n'
                        b'Commissioning field: \r\n'
                        b'\r\n']
        
    def get_buffer(self):
        return self.buffer_txt
    
    def interrupt(self):
        logging.info(f'{self.device.serial_port_name}: Interrupting Listener')
        self.needs_interrupt = True

    def start_listening(self):
        logging.info(f'{self.device.serial_port_name}: Starting Listener')
        threading.Thread(target=self.listening).start()

    def listening(self):
        self.is_running = True
        logging.info(f'{self.device.serial_port_name}: Thread Started, Listening')

        while self.is_running and not self.needs_interrupt:
            lines = self.device.serial_port.readline()
            if lines:
                self.buffer_txt = lines
                logging.info(f'{self.device.serial_port_name} : {lines}')
                if b"\x1b" in (lines):
                    for line in self.mainmenu:
                        try:
                            self.device.serial_port.write(line)
                        except Exception:
                            logging.info(f'{self.device.serial_port_name}: Failed Sending Commands')
                if b"command4" in (lines):
                    for _ in range (10):
                        if self.needs_interrupt:
                            break
                        for line in self.status:
                            try:
                                self.device.serial_port.write(line)
                            except Exception:
                                logging.info(f'{self.device.serial_port_name}: Failed Sending Commands')
                            time.sleep(1)
    
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
    
    port = "COM4"
    logging.info(f'Starting ML simulator on: {port}')
    unit = Device(port)

    time.sleep(30)
    unit.listener.interrupt()
    unit.disconnect()
