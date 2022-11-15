import re
import serial
from xmodem import XMODEM
import time
import serial.tools.list_ports

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
            print("SERIAL IN USE")#probably
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
        for _ in range(10):
            self.write_commands(["esc"])
            x = self.ser.readlines()
            if "Main Menu" in str(x):
                return True
            time.sleep(0.5)
        else:
            return False

    def is_config(self):
        for _ in range(5):
            live = self.is_alive()
            if live == True:
                self.write_commands(["esc", "3"])
                x = self.ser.readlines()
                if "No Config" in str(x):
                    return False
                else:
                    return True
        return False

    def is_firmware (self):
        vers = None
        for _ in range(5):
            live = self.is_alive()
            if live == True:
                break
        else:
            return False
        try:
            list_of_matches = re.findall("\d\.\d\d\.\d", self.firmware_path)
            vers = list_of_matches[0]
        except Exception as e: print(e)
        #print(vers)
        self.write_commands(["esc", "4"])
        x = self.ser.readlines()
        if vers == None:
            return False
        else:
            if str(vers) in str(x):
                return False
            else:
                return True

    def erase_config(self):
        for _ in range(5):
            live = self.is_alive()
            if live == True:
                self.write_commands(["esc","9","h","y"])
                time.sleep(0.5)
                return True
            return False
        # self.write_commands(["esc","3"])
        # data = self.ser.readlines()
        # time.sleep(0.5)
        # if "No Config" in str(data):
        #     self.write_commands(["esc"])
        #     return True
        # else:
        #     return False
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
        def getc(size, timeout=1):
            return self.ser.read(size) or None
        def putc(data, timeout=1):
            self.pb_object.add_to_progress(128)
            #print(f"{self.pb_object.progress}/{self.pb_object.total}")
            return self.ser.write(data)  # note that this ignores the timeout
        modem = XMODEM(getc, putc)#modes = xmodem , xmodem1k , xmodemcrc
        stream = open(path, 'rb')

        self.write_commands(["esc","6"])

        for _ in range(4):#can only read first 4 lines of download screen, have to push on the 5th
            self.ser.readline()
        status = modem.send(stream)
        #print(status)
        return status
