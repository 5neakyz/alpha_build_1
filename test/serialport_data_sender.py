from serial import Serial
import time
import serial.tools.list_ports
import tkinter as tk
from tkinter import ttk
import threading
# serialPort = serial.Serial(
#     port="COM3", baudrate=115200, bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE
# )

# data = [b'\x1b[2J\x1b[2J\r\t\t\tView Config\r\r\n', b'\r\n', b'\n', b'sz 0x2f8\r\n', b'CF', b'G sz: 760=759\r\n', b'CONFIG\r\n', b'\r\n', b'PersonalityVer      ML12_CT_Microl_DAFCF_040619\r\n', b'\r\n', b'HostIP \t\t\t172.17.168.157\r\n', b'HostPort    5432\r\n', b'APN         microlise.lte1.gdsp\r\n', b'InetPassword\t\ta\r\n', b'InetUser\t\ta\r\n', b'AccessTech \t\t4\r\n', b'CAN1Mode \t\tJ1939\r\n', b'DistanceSource \t\t2\r\n', b'ShockWakeupThreshold \t200\r\n', b'ShockWakeupDuration \t1\r\n', b'WakeUp \t\t\t28800\r\n', b'PowerRetain \t\t900\r\n', b'WakeupMask \t\t4\r\n', b'TimedRep \t\t1800\r\n', b'Distance \t\t1609\r\n', b'CoastingD \t\t20 10 1.0\r\n', b'CruiseControl \t\t1 0\r\n', b'ExcessiveRPM \t\t3200 3 1.0\r\n', b'ExcessiveIdle \t\t1 120 1.0\r\n', b'ExcessiveSpeedD \t96 10 1.0\r\n', b'HarshAcceleration \t22 10 2.0\r\n', b'HarshBrake \t\t-12.87 0 11.87\r\n', b'HarshCorneringG \t8 0.4 0.3\r\n', b'LogLevel \t\t4\r\n', b'IgnitionOn \t\t5 5\r\n', b'IgnitionOff \t\t5 5\r\n', b'MovingAfterStopped \t1 60 1.0\r\n', b'OverDriving \t\t95 10 1\r\n', b'resetTimerOnDist \t1\r\n', b'StartUpTimeFix \t\t1\r\n', b'ShortPowRetain \t\t180\r\n', b'Stopped \t\t1 60 1.0\r\n']


# for _ in range(100):
#     print(_)
#     time.sleep(1)
#     for item in data:
#         serialPort.write(item)


class Controller(object):
    def __init__(self,msg,port):
        super().__init__()
        self.stop_event = threading.Event()
        self.serialport = port
        self.output = msg
        self.interval = 1 

    def send_constantly(self):
        while not self.stop_event.is_set():
            print(f'looping {self.stop_event.is_set()}')
            for item in self.output:
                #print(item)
                self.serialport.write(item)
                #port2.write(item)

            self.stop_event.wait(self.interval)   

    def start(self):
        print("starting Thread")
        self.stop_event.clear()
        self.thread = threading.Thread(target = self.send_constantly)
        self.thread.start()


    def stop(self):
        print("stopping thread")
        self.stop_event.set()
        print(self.stop_event.is_set())

class SimpleSimulator(tk.Tk):
    def __init__(self):
        super().__init__()
        # configure window
        self.title("Simple Simulator")
        self.geometry(f"{200}x{200}")
        self.running_state = False

        self.serialPort1 = serial.Serial(
        port="COM3", baudrate=115200, bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE)
        # self.serialPort2 = serial.Serial(
        # port="COM5", baudrate=115200, bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE)
        # self.serialPort3 = serial.Serial(
        # port="COM7", baudrate=115200, bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE)

        self.output = [b'\x1b[2J\x1b[2J\r\t\t\tView Config\r\r\n',
                    b'\r\n',
                    b'\n',
                    b'sz 0x2f8\r\n',
                    b'CF',
                    b'G sz: 760=759\r\n',
                    b'CONFIG\r\n',
                    b'\r\n',
                    b'PersonalityVer      ML12_CT_Microl_DAFCF_040619\r\n',
                    b'\r\n',
                    b'HostIP \t\t\t172.17.168.157\r\n',
                    b'HostPort    5432\r\n',
                    b'APN         microlise.lte1.gdsp\r\n',
                    b'InetPassword\t\ta\r\n',
                    b'InetUser\t\ta\r\n',
                    b'AccessTech \t\t4\r\n',
                    b'CAN1Mode \t\tJ1939\r\n',
                    b'DistanceSource \t\t2\r\n',
                    b'ShockWakeupThreshold \t200\r\n',
                    b'ShockWakeupDuration \t1\r\n',
                    b'WakeUp \t\t\t28800\r\n',
                    b'PowerRetain \t\t900\r\n',
                    b'WakeupMask \t\t4\r\n',
                    b'TimedRep \t\t1800\r\n',
                    b'Distance \t\t1609\r\n',
                    b'CoastingD \t\t20 10 1.0\r\n',
                    b'CruiseControl \t\t1 0\r\n',
                    b'ExcessiveRPM \t\t3200 3 1.0\r\n',
                    b'ExcessiveIdle \t\t1 120 1.0\r\n',
                    b'ExcessiveSpeedD \t96 10 1.0\r\n',
                    b'HarshAcceleration \t22 10 2.0\r\n',
                    b'HarshBrake \t\t-12.87 0 11.87\r\n',
                    b'HarshCorneringG \t8 0.4 0.3\r\n',
                    b'LogLevel \t\t4\r\n',
                    b'IgnitionOn \t\t5 5\r\n',
                    b'IgnitionOff \t\t5 5\r\n',
                    b'MovingAfterStopped \t1 60 1.0\r\n',
                    b'OverDriving \t\t95 10 1\r\n',
                    b'resetTimerOnDist \t1\r\n',
                    b'StartUpTimeFix \t\t1\r\n',
                    b'ShortPowRetain \t\t180\r\n',
                    b'Stopped \t\t1 60 1.0\r\n']
        
        self.control = Controller(self.output,self.serialPort1)

        self.run_btn = ttk.Button(self, text="Run",command = lambda: threading.Thread(target=self.run).start())
        self.run_btn.grid(row=1, column=0, padx=20, pady=10)

        self.mainloop()

    def run(self):
        if self.running_state == False:
            self.running_state = True
            self.run_btn.configure(text="Running")
            self.control.start()
        else: 
            self.running_state = False
            self.run_btn.configure(text="Stopped")
            self.control.stop()
            


SimpleSimulator()