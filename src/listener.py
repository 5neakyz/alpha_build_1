import threading
import logging

class Listener():
    def __init__(self,device):
        logging.info(f'{device.serial_port_name}: Creating Listener Object')
        self.device = device
        self.is_running = False
        self.needs_interrupt = False 
        self.buffer_txt = ""

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
            lines = self.device.serial_port.readlines()
            if lines:
                self.buffer_txt = self.format(lines)
                #logging.info(f'{self.device.serial_port_name} : {self.format(lines)}')

    def format(self,byte_array_list):
        output = ""
        for line in byte_array_list:
            stripped = line.strip().replace(b'\t', b' ').replace(b'\r',b' ').replace(b'\x1b',b'').replace(b'\n',b'').replace(b'[2J',b'').replace(b':',b': ')
            if stripped:
                output += stripped.decode("utf-8") + '\n'
        return output