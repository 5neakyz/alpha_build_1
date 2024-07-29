import time
import logging
from xmodem import XMODEM
from serial_port_manager import SerialPortManger
from listener import Listener

logger = logging.getLogger(__name__)

class Device(SerialPortManger):
    def __init__(self,parent,progress_bar_object=None):
        super().__init__(parent)
        logger.info(f'{self.serial_port_name}: Creating Device Object')
        self.progress_bar_object = progress_bar_object
        self.listener = Listener(self)
        self.listener.start_listening()

    def is_alive (self):
        if self.serial_connection:
            for _ in range(5):
                self.write_commands(["esc"])
                time.sleep(0.5)
                x = self.listener.get_buffer()
                if "Main Menu" in str(x):
                    logger.info(f'{self.serial_port_name}: is Alive')
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

    def write_commands(self,commands:list):
        if self.serial_connection:
            logger.info(f'{self.serial_port_name}: Sending Command(s): {commands}')
            for command in commands:
                if command =="esc":
                    command = (chr(27))     
                try:
                    self.serial_port.write(command.encode())
                except Exception:
                    logger.warning(f'{self.serial_port_name}: Failed Sending Commands')
                    return False
            return True
        return False
    
    #xmodem setup
    def getc(self,size, timeout=1):
        for _ in range (20):
            gbytes = self.serial_port.read(size)
            #print(f'GByte: {gbytes}')
            if gbytes:
                break
            time.sleep(0.1)
        return gbytes or None
    
    def putc(self,data, timeout=1):
        pbytes = self.serial_port.write(data)
        
        if len(data) > 1000:
            self.progress_bar_object.add_to_progress(1024)

        return  pbytes or None 
    
    def push(self,path):
        # basic check on path
        if not path:
            logger.warning(f'FAILED PATH {path}')
            return False 

        #check unit is responsive 
        if not self.is_alive():
            logger.warning("NOT ALIVE")
            return False
        
        # setup xmodem
        modem = XMODEM(self.getc, self.putc,'xmodem1k')#modes  xmodem , xmodem1k , xmodemcrc
        stream = open(path, 'rb')

        #open download menu of unit
        self.write_commands(["esc","6"])
        time.sleep(1)
        self.listener.pause_read()
        time.sleep(0.5)
        logger.info(f'{self.serial_port_name}: initiating Xmodem send')
        #send file
        status = modem.send(stream)
        logger.info(f'{self.serial_port_name}:Data Stream Status: {status}')

        if not status:
            logger.warning(f'{self.serial_port_name}: XMODEM FAILED. STATUS: {status}')
            return False
        
        self.listener.continue_read()
        # checks
        # logger.info(f'Begging checks:')
        if not self.install_checker():
            return False

        return True
    
    def install_checker(self):
        '''Ml30s on 3.17 need you to either wait 10 seconds or Ctrl X to confirm and install, 
        if you press esc it will cancel install'''
        logger.info(f"{self.serial_port_name}: Checking")
        for _ in range(120):
            time.sleep(0.5)
            lines = self.listener.get_buffer()

            if not lines: continue
            
            if "Ctrl X" in str(lines):
                self.write_commands(chr(24))
                logger.info("SENDING CTRL X")
                break

            if "install failed" in str(lines):
                logger.warning(f'INSTALL FAILED')
                return False
            
            if "Abort" in str(lines):
                logger.warning(f'INSTALL FAILED')
                return False
            
            if "Hello" in str(lines):
                #logger.info(f'Unit replied with Hello')
                break 
            
        return True