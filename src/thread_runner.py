import concurrent.futures
import time
class ThreadRunner():
    def __init__(self,device_objects,my_pb_object=None,personality_path=None,firmware_path=None,mode=-1,):
        self.device_objects = device_objects
        self.personality_path = personality_path
        self.firmware_path = firmware_path
        self.mode = mode 
        self.my_pb_object = my_pb_object
    """
    MODES -
    1 - Erase Config
    2 - Push Personality Only
    3 - Push Firmware Only - this also removes personality (ML safety reasons)
    4 - Push both Firmware and personality
    """
    def work_horse(self,obj):
        if obj.is_alive() == True:
            obj.pb_object = self.my_pb_object
            match self.mode:
                case 1:#erase Config
                    return self.erase_config(obj)
                case 2:#push personality only
                    return self.push_personality(obj)
                case 3:#push firmware only
                    return self.push_firmware(obj)
                case 4:#push both personality and firmware
                    return self.push_both(obj)
                case _:
                    return f"{obj.device} unsure how you got here but hey here we are, theres somehow no mode selected"

        else:
            return [obj.device,False]



    def erase_config(self,obj):
        if obj.erase_config() == True and obj.is_config() == False:#we dont want a config 
            return [obj.device , True]
        else:
            return [obj.device,False]

    def push_personality(self,obj):
        if self.personality_path == None:
            return [obj.device,False]
        else:
            obj.erase_config()
            obj.personality_path =self.personality_path
            if obj.push(1) and obj.is_config(): 
                return [obj.device , True]
            else:
                return [obj.device,False]

    def push_firmware(self,obj):
        if self.firmware_path == None:
            return [obj.device,False]
        else:
            obj.firmware_path =self.firmware_path
            if obj.erase_config() and obj.is_config() == False and obj.push(2): 
                starttime = time.time()
                for _ in range(20):# it takes like 10-14 seconds to install the firmware
                    print(f"attempt {_} of 20 : total time waited {time.time()-starttime}")
                    live = obj.is_alive()
                    if live == True:
                        break
                    time.sleep(0.5)
                else: return [obj.device,False]
                #not checking firmware for now as this is dependent on file names being all similar when i regex split to get vers
                #if obj.is_firmware():
                #    return [obj.device , True]
                #return [obj.device,False]
                return [obj.device , True]
            else:
                return [obj.device,False]

    def push_both(self,obj):
        if self.personality_path == None or self.firmware_path == None:
            return [obj.device,False]
        else:
            obj.personality_path =self.personality_path
            obj.firmware_path =self.firmware_path
            if obj.erase_config() and obj.is_config() == False and obj.push(2): 
                starttime = time.time()
                for _ in range(20):
                    live = obj.is_alive()
                    print(f"attempt {_} of 20 : total time waited {time.time()-starttime}")
                    if live == True:
                        break
                    time.sleep(0.5)
                else: return [obj.device,False]
                if obj.push(1) and obj.is_config(): 
                    return [obj.device , True]
                else:
                    return [obj.device,False]
            else:
                return [obj.device,False]

    """
    Pyserial objects are not pickable so cannot use ProccessPoolExecuter
    based on the very limited testing i have done, it seems to be about the same as ThreadPoolExecutor give or take a couple 100ths of a second
    either way its about the same as doing only 1 device on terra term(not slagging off terra term, it does a lot of stuff and a lot better than my mess of a application), 
    """
    def thread_run(self):
        results = []
        with concurrent.futures.ThreadPoolExecutor() as executor:# parallelism 
            tasks = [executor.submit(self.work_horse,device) for device in self.device_objects]
            for x in concurrent.futures.as_completed(tasks):
                results.append(x.result())
        return results

