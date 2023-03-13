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
        for _ in range(3):#attempts 3 times
            self.write_commands(["esc"])
            x = self.ser.readlines()
            if "Main Menu" in str(x):
                return True
            time.sleep(0.5)
        else:
            return False

    def is_config(self):
        for _ in range(5):
            if self.is_alive():
                break
        else: return False

        self.write_commands(["esc", "3"])

        if "No Config" in str(self.ser.readlines()):
            return False
        else:
            return True
        

    def is_firmware (self):
        vers = None
        for _ in range(5):
            if self.is_alive():
                break
        else: return False

        try:
            list_of_matches = re.findall("\d\.\d\d\.\d", self.firmware_path)
            vers = list_of_matches[0]
        except Exception as e: print(e)
        #print(vers)
        self.write_commands(["esc", "4"])
        x = self.ser.readlines()
        if vers is None:
            return False
        else:
            if str(vers) in str(x):
                return False
            else:
                return True

    def erase_config(self):
        for _ in range(5):
            if self.is_alive():
                break
        else: return False

        self.write_commands(["esc","9","h","y"])
        time.sleep(0.5)
        return True
    

    #xmodem setup
    def getc(self,size, timeout=1):
        gbytes = self.ser.read(size)
        print(f"G_Bytes: {gbytes}")
        return gbytes or None
    
    def putc(self,data, timeout=1):
        pbytes = self.ser.write(data)
        self.pb_object.add_to_progress(1028)
        time.sleep(0.1) # have to wait otherwise it reads nothing
        print(f"P_Bytes: {data}")
        return  pbytes or None 
    """
    MODES should probs change this
    1 - Push Personality
    2 - Push Firmware
    """
    def push(self,mode=-1):
        if mode == 1:# MODE 1 push personality
            if self.personality_path is None: return False
            else: path = self.personality_path
        elif mode == 2:# MODE 2 push Firmware
            if self.firmware_path is None: return False
            else: path = self.firmware_path
        else: return False

        for _ in range(5):
            if self.is_alive():
                break
        else: return False
        
        
        modem = XMODEM(self.getc, self.putc,'xmodem1k')#modes  xmodem , xmodem1k , xmodemcrc
        stream = open(path, 'rb')

        self.write_commands(["esc","6"])

        for _ in range(4):#can only read first 4 lines of download screen, have to push on the 5th
            self.ser.readline()
        status = modem.send(stream)
        #print(status)
        return status

    def read_config(self):
        out = ""
        for _ in range(5):
            if self.is_alive(): break
        else: return False

        self.write_commands(["esc", "3"])
        for _ in range(50):
            lines = self.ser.readlines()
            if not lines:continue

            for line in lines:
                y = line.strip().replace(b'\t\t', b'  ').replace(b'\t',b' ')
                out +=(y.decode('utf-8')+ ' \n')
            return [self.device,out]
            
        return [self.device,"No READ"]

    def read_status(self):
        out = ""
        for _ in range(5):
            if self.is_alive(): break
        else: return False

        self.write_commands(["esc", "4"])
        for _ in range(50):
            lines = self.ser.readlines()

            if not lines: continue

            for line in lines:
                y = line.strip().replace(b'\t\t', b'  ').replace(b'\t',b' ')
                out +=(y.decode('utf-8')+ ' \n')
            return [self.device,out]
                
        return [self.device,"No READ"]