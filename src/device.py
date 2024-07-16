import time
import logging

from serial_port_manager import SerialPortManger
from listener import Listener

class Device(SerialPortManger):
    def __init__(self,parent):
        super().__init__(parent)
        logging.info(f'{self.serial_port_name}: Creating Device Object')

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
            for i, command in enumerate(commands):
                if command =="esc":
                    command = (chr(27))     
                try:
                    self.serial_port.write(command.encode())
                except Exception:
                    logging.info(f'{self.serial_port_name}: Failed Sending Commands')
                    return False
            return True
        return False
