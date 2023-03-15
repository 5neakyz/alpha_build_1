
import serial.tools.list_ports
import serial
from xmodem import XMODEM
import time
import os
import threading
import logging
import concurrent.futures

def threader(func,params):
    results = []
    with concurrent.futures.ThreadPoolExecutor() as executor:# parallelism 
        tasks = [executor.submit(func,device) for device in params]
        for x in concurrent.futures.as_completed(tasks):
            results.append(x.result())
    return results

def sleeper(item):
    logging.info(f"ITEM {item} : START")
    time.sleep(0.5)
    logging.info(f"ITEM {item} : END")



if __name__ == '__main__':
    format = "%(asctime)s.%(msecs)04d: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO,
                        datefmt="%H:%M:%S")

    # mylist = [1,2,3,4]
    # threader(sleeper,mylist)

    import webbrowser

    url = "https://www.google.com/"

    webbrowser.open(url, new=0, autoraise=True)