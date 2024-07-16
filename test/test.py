

import serial.tools.list_ports
import serial
from xmodem import XMODEM
import time
import os
import threading
import logging
import concurrent.futures




devices = ["COM1","COM2","COM3"]
label = ["lab1","lab2","lab3"]

for device in devices:
    print(label[devices.index(device)])

