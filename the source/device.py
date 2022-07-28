from asyncore import write
from dataclasses import dataclass
import re
from select import select
from tkinter import X
import serial
from xmodem import XMODEM
import time
import serial.tools.list_ports


class Device():
    def __init__(self,device,personality_path=None,firmware_path=None):# device is string like "COM6"
        self.device=device
        self.personality_path = personality_path
        self.firmware_path = firmware_path
        self.safe_serial = True
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
            #self.ser.write(chr(27).encode())
            time.sleep(0.1)
            x = self.ser.readlines()
            if "Main Menu" in str(x):
                return True
            time.sleep(0.1)
        else:
            return False

    def is_config(self):
        self.write_commands(["esc", "3"])
        x = self.ser.readlines()
        if "No Config" in str(x):
            return False
        else:
            return True

    def is_firmware (self):
        vers = None
        try:
            list_of_matches = re.findall("\d\.\d\d\.\d", self.firmware_path)
            vers = list_of_matches[0]
        except Exception as e: print(e)
        self.write_commands(["esc", "3"])
        x = self.ser.readlines()
        if vers == None:
            return False
        else:
            if str(vers) in str(x):
                return False
            else:
                return True

    def erase_config(self):
        self.write_commands(["esc","9","h","y"])
        time.sleep(0.5)
        self.write_commands(["esc","3"])
        data = self.ser.readlines()
        if "No Config" in str(data):
            self.write_commands(["esc"])
            return True
        else:
            return False
    """
    MODES
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

        #xmodem setup
        def getc(size, timeout=1):
            return self.ser.read(size) or None
        def putc(data, timeout=1):
            return self.ser.write(data)  # note that this ignores the timeout
        modem = XMODEM(getc, putc)#modes = xmodem , xmodem1k , xmodemcrc
        stream = open(path, 'rb')

        self.write_commands(["esc","6"])

        for _ in range(4):#can only read first 4 lines of download screen, have to push on the 5th
            self.ser.readline()
        status = modem.send(stream)
        #print(status)
        return status

# testing purposes
if __name__ == "__main__":
    import concurrent.futures
    # one = Device("COM6")
    # print(one.is_alive())
    # print(one.erase_config())
    # one.personality_path = "S:/Production/CONFIGURATION FILES/ML12 Firmware/ML12_CT_Microl_DAFCF_040619.txt"
    #"S:/Production/CONFIGURATION FILES/ML12 Firmware/ML12_V_3.88.3_e001.bin"
    # print(one.push())
    selected_devices= ["COM6","COM7"]
    my_objects = []
    for device in selected_devices:
        my_objects.append(Device(device))
    # for i, object in enumerate(my_objects):
    #     x = object.is_alive()
    #     print(x)

    def living(obj):
        if obj.is_alive() == True:
            obj.erase_config()
            obj.firmware_path = "S:/Production/CONFIGURATION FILES/ML12 Firmware/ML12_V_3.88.3_e001.bin"
            obj.personality_path = "S:/Production/CONFIGURATION FILES/ML12 Firmware/ML12_CT_Microl_DAFCF_040619.txt"
            stat = obj.push(1)
            return f"{obj.device} completed {stat} "


    """
    Pyserial objects are not pickable so cannot use ProccessPoolExecuter
    based on the very limited testing i have done, it seems to be about the same give or take a couple 100ths of a second
    either way its about the same as doing only 1 device on terra term(no slagging of terra term, its actually very good), 
    """
    def mp_run(my_objects):                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         
        with concurrent.futures.ThreadPoolExecutor() as executor:# parallelism 
            tasks = [executor.submit(living,device) for device in my_objects]
            for x in concurrent.futures.as_completed(tasks):
                print(x.result())
    s = time.perf_counter()
    mp_run(my_objects)
    elapsed = time.perf_counter() - s
    print(f"{__file__} executed in {elapsed:0.2f} seconds.")