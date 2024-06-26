

import serial.tools.list_ports
import serial
from xmodem import XMODEM
import time
import os
import threading
import logging
import concurrent.futures

def worker():
    print("Thread execution starts")
    time.sleep(2)  # This simulates a time-consuming task
    print("Thread execution ends")

class test():
    def __init__(self):
        self.interrupt = False
        self.count = 0 
        
    def start(self):
        print("STARTING")
        while not self.interrupt:
            time.sleep(0.5)
            print("a")
            self.count += 1
            if self.count > 10:
                break

    def stop(self):
        print("STOPPPING")
        self.interrupt = True


print("one: Create Class")
#x = test()
print("two: start loop")
t = threading.Thread(target=worker())
t.start()
print("three: wait")
print("four")
#x.stop()


# def worker():
#     print("Thread execution starts")
#     time.sleep(2)  # This simulates a time-consuming task
#     print("Thread execution ends")

# create a thread by specifying the target function
t = threading.Thread(target=worker)

# start the thread
t.start()

print("###########Main thread execution ends")

