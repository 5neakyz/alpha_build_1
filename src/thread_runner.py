import concurrent.futures
import time
import logging
class ThreadRunner():
    def __init__(self,device_objects,my_pb_object=None,personality_path=None,firmware_path=None,BLE_path=None,tasks=[0,0,0,0],):
        self.device_objects = device_objects
        self.personality_path = personality_path
        self.firmware_path = firmware_path
        self.BLE_path = BLE_path
        self.tasks = tasks
        self.my_pb_object = my_pb_object
    """
    """
    def work_horse(self,device):
        device.pb_object = self.my_pb_object
        
        if self.tasks[0] > 0: # erase config
            logging.info(f"Erasing Config")
            if not device.erase_config():
                return [device.device,False]
            
        if self.tasks[2] > 0: # Push Firmware
            logging.info(f"Pushing Firmware")
            if not device.push(self.firmware_path):
                return [device.device,False]
            
        if self.tasks[1] > 0: # push personality
            logging.info(f"Pushing Personality")
            if not device.push(self.personality_path):
                return [device.device,False]
            
        if self.tasks[3] > 0: # Push BLE
            logging.info(f"Pushing BLE")
            if not device.push(self.BLE_path):
                return [device.device,False]
            
        return [device.device,True]
 
    def thread_run(self):
        results = []
        with concurrent.futures.ThreadPoolExecutor() as executor:# parallelism 
            tasks = [executor.submit(self.work_horse,device) for device in self.device_objects]
            for x in concurrent.futures.as_completed(tasks):
                results.append(x.result())
        return results

