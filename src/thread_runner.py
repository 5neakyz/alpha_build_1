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
    MODES -
    1 - Erase Config
    2 - Push Personality Only
    3 - Push Firmware Only - this also removes personality (ML safety reasons)
    4 - Push both Firmware and personality
    """
    def work_horse(self,obj):
        obj.pb_object = self.my_pb_object
        
        if self.tasks[0] > 0: # erase config
            logging.info(f"Erasing Config")
            if not self.erase_config(obj):
                return [obj.device,False]
            
        if self.tasks[2] > 0: # Push Firmware
            logging.info(f"Pushing Firmware")
            if not self.push_firmware(obj):
                return [obj.device,False]
            
        if self.tasks[1] > 0: # push personality
            logging.info(f"Pusing Personality")
            if not self.push_personality(obj):
                return [obj.device,False]
            
        if self.tasks[3] > 0: # Push BLE
            logging.info(f"Pushing BLE")
            if not self.push_BLE(obj):
                return [obj.device,False]
            
        return [obj.device,True]

    def erase_config(self,obj):
        if obj.erase_config() == True and obj.is_config() == False:
            return True
        else:
            return False

    def push_personality(self,obj):
        if self.personality_path == None:
            return False

        obj.erase_config()
        obj.personality_path =self.personality_path
        if obj.push(self.personality_path) and obj.is_config(): 
            return True

        return False
    
    def push_BLE(self,obj):
        if self.BLE_path == None:
            return False

        if not obj.push(self.BLE_path): 
            return False
        
        if not obj.install_checker():
            return False

        return True 

    def push_firmware(self,obj):
        if self.firmware_path == None:
            return False
        
        obj.erase_config()
        if obj.is_config():
            return False

        if not obj.push(self.firmware_path): 
            return False
        
        if not obj.install_checker():
            return False

        obj.write_commands(["esc"])
        
        starttime = time.time()
        for _ in range(20):# it takes like 10-14 seconds to install the firmware or 20 ish seconds for ml30s
            print(f"attempt {_} of 20 : total time waited {time.time()-starttime}")
            if obj.is_alive():
                return True
            time.sleep(0.5)
        else: return False


    def thread_run(self):
        results = []
        with concurrent.futures.ThreadPoolExecutor() as executor:# parallelism 
            tasks = [executor.submit(self.work_horse,device) for device in self.device_objects]
            for x in concurrent.futures.as_completed(tasks):
                results.append(x.result())
        return results

