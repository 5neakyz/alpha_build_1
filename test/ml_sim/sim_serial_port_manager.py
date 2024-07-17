import serial.tools.list_ports
import serial
import logging

class SerialPortManger():
    def __init__(self,comport_name):
        self.serial_connection = False
        self.serial_port = None
        self.serial_port_name = comport_name
        self.serial_port_baud = 115200
        self.log = logging.getLogger('SerialPortManger')

        try:
            self.serial_port = serial.Serial(port = self.serial_port_name, baudrate=self.serial_port_baud, timeout=0.1)
            self.serial_connection = True
            logging.info(f'{self.serial_port_name}: Connection Established')
        except Exception:
            logging.info("CANNOT CONNECT")
            self.serial_connection=False

    def disconnect(self):
        logging.info(f'{self.serial_port_name}: Disconnected')
        self.serial_port.close()
        self.serial_connection = False