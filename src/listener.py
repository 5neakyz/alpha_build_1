import threading
import logging
import time
class Listener():
    def __init__(self,device):
        logging.info(f'{device.serial_port_name}: Creating Listener Object')
        self.device = device
        self.is_running = False
        self.needs_interrupt = False 
        self.buffer_txt = ""
        self.download_temp_interrupt = False

    def continue_read(self):
        logging.info(f'{self.device.serial_port_name}: continuing Listener')
        self.download_temp_interrupt = False        

    def pause_read(self):
        logging.info(f'{self.device.serial_port_name}: Pausing Listener')
        self.download_temp_interrupt = True  

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
            if self.download_temp_interrupt:
                time.sleep(0.5)
                continue
            '''
            ReadLines Version
            '''
            # lines = self.device.serial_port.readlines()
            # if lines:
            #     self.buffer_txt = self.rls_format(lines)
            #     logging.info(f'{self.device.serial_port_name} : {self.format(lines)}')
            '''
            ReadLine Version
            '''
            line = self.device.serial_port.readline()
            # logging.info(f'{self.device.serial_port_name}: {line}')
            if line:
                if b'\x1b' in line:
                    self.buffer_txt = ""
                    split = line.split(b'\x1b')
                    line = split[-1]
            stripped = line.replace(b'\r',b' ').replace(b'\x1b',b'').replace(b'[2J',b'').replace(b':',b': ')
            if stripped:
                self.buffer_txt += stripped.decode("utf-8")

    def rls_format(self,byte_array_list):
        output = ""
        for line in byte_array_list:
            if b'\x1b' in line:
                output = ""
                split = line.split(b'\x1b')
                line = split[-1]
            #stripped = line.strip().replace(b'\t', b' ').replace(b'\r',b' ').replace(b'\x1b',b'').replace(b'\n',b'').replace(b'[2J',b'').replace(b':',b': ')
            stripped = line.replace(b'\r',b' ').replace(b'\x1b',b'').replace(b'[2J',b'').replace(b':',b': ')
            if stripped:
                output += stripped.decode("utf-8")
        return output