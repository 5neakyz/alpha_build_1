import serial.tools.list_ports
import serial
from xmodem import XMODEM
import time
import os
import threading
import logging
import concurrent.futures

class Device():
    def __init__(self,device,personality_path=None,firmware_path=None,pb_object=None):# device is string like "COM6"
        self.device=device
        self.personality_path = personality_path
        self.firmware_path = firmware_path
        self.safe_serial = True
        self.pb_object = pb_object
        try:
            self.ser = serial.Serial(device, 115200, timeout=0.050)
        except Exception:
            logging.info("SERIAL IN USE")#probably
            self.safe_serial=False

    ## makes it easier to send commands for other functions
    def write_commands(self,commands):
        for i, command in enumerate(commands):
            if command =="esc":
                command = (chr(27))
            try:
                self.ser.write(command.encode())
            except Exception as e: print(e)

            if commands[i] != commands[-1]:# if last command in commands do not load menu so i can view it else where
                self.ser.readlines()# waits for the menu to load, needed other wise commands get sent too fast for the ML

    def is_alive (self):
        if self.safe_serial==False:
            return False
        for _ in range(3):#attempts 3 times
            self.write_commands(["esc"])
            x = self.ser.readlines()
            if "Main Menu" in str(x):
                return True
            time.sleep(0.5)
        else:
            return False


    def erase_config(self):
        for _ in range(5):
            live = self.is_alive()
            if live == True:
                self.write_commands(["esc","9","h","y"])
                time.sleep(0.5)
                return True
            return False

    def read_config(self):
        out = ""
        for _ in range(5):
            if self.is_alive(): break
        else: return False

        self.write_commands(["esc", "3"])
        for _ in range(50):
            lines = self.ser.readlines()
            if not lines:continue

            print(f"LINES :\n{lines}")
            for line in lines:
                y = line.strip().replace(b'\t\t', b'  ').replace(b'\t',b' ')
                #out +=(y.decode('utf-8')+ ' \n') 
                print(y)
            return [self.device,"out"]
            
        return [self.device,"No READ"]

    def read_config_lines(self):
            out = ""
            for _ in range(5):
                if self.is_alive(): break
            else: return False

            self.write_commands(["esc", "3"])

            lines = self.ser.readlines

    
    """
    MODES should probs change this
    1 - Push Personality
    2 - Push Firmware
    """
    def push(self,mode=-1):
        if mode == 1:# MODE 1 push personality
            if self.personality_path == None:
                return False
            else:
                path = self.personality_path
        elif mode == 2:# MODE 2 push Firmware
            if self.firmware_path == None:
                return False
            else:
                path = self.firmware_path
        else:
            return False

        for _ in range(5):
            live = self.is_alive()
            if live == True:
                break
        else:
            return False

        #xmodem setup
        #getc - shove cake down down their throat - dont ask just do
        def getc(size, timeout=1):
            gbytes = self.ser.read(size)
            if self.loop == 0:
                gbytes = b'C'
            else:
                gbytes = b'\x06'
            logging.info(f"GByte : {gbytes}")
            self.loop +=1
            return gbytes or None

        def putc(data, timeout=1):
            pbytes = self.ser.write(data)
            logging.info(f'PByte: {pbytes}')
            return pbytes or None

        self.loop = 0
        modem = XMODEM(getc, putc)#modes = xmodem , xmodem1k , xmodemcrc
        stream = open(path, 'rb')

        self.write_commands(["esc","6"])

        for _ in range(4):#can only read first 4 lines of download screen, have to push on the 5th
            self.ser.readline()
        status = modem.send(stream,retry = 30)
        #print(status)
        return status



if __name__ == '__main__':
    format = "%(asctime)s.%(msecs)04d: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO,
                        datefmt="%H:%M:%S")

    myunit = Device("COM9")
    myunit.firmware_path="J:/gitcode/Multi-ML-1.0/firmware/ml30/ML30_V_3.88.0_c741.bin"
    #myunit.firmware_path="J:/gitcode/Multi-ML-1.0/firmware/ml30/ML30_V_3.84.0_b981.bin"
    myunit.personality_path="J:/gitcode/Multi-ML-1.0/firmware/ml30/ML30_CT_Microl_DAFCF_040619.txt"
    logging.info(f"DEVICE STATUS IsAlive: {myunit.is_alive()}")
    # logging.info(f"Clear CONFIG : {myunit.erase_config()}")
    logging.info(f"CONFIG : {myunit.read_config()[1]}")
    # logging.info(f"push firm : {myunit.push(2)}")
    # logging.info(f"push pers : {myunit.push(1)}")
    #logging.info(f"CONFIG : {myunit.read_config()}")