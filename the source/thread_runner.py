import concurrent.futures
from pickletools import read_uint1
import time
class ThreadRunner():
    def __init__(self,device_objects,personality_path=None,firmware_path=None,mode=-1):
        self.device_objects = device_objects
        self.personality_path = personality_path
        self.firmware_path = firmware_path
        self.mode = mode 

    """
    MODES -
    1 - Erase Config
    2 - Push Personality Only
    3 - Push Firmware Only - this also removes personality (ML safety reasons)
    4 - Push both Firmware and personality
    """
    def work_horse(self,obj):
        if obj.is_alive() == True:
            match self.mode:
                case 1:#erase Config
                        state1 = obj.erase_config()
                        state2 = obj.is_config()
                        if state1 == True and state2 == False: 
                            return [obj.device , True]
                        else:
                            return [obj.device,False]
                case 2:#push personality only
                    if self.personality_path == None:
                        return [obj.device,False]
                    else:
                        obj.erase_config()
                        obj.personality_path =self.personality_path
                        state1 = obj.push(1)
                        state2 = obj.is_config()
                        if state1 == True and state2 == True: 
                            return [obj.device , True]
                        else:
                            return [obj.device,False]

                case 3:#push firmware only
                    if self.firmware_path == None:
                        return [obj.device,False]
                    else:
                        obj.erase_config()
                        obj.firmware_path =self.firmware_path
                        state1 = obj.push(2)
                        time.sleep(20)# it takes like 10-14 seconds to install the firmware
                        for _ in range(5):
                            live = obj.is_alive()
                            if live == True:
                                break
                        state2 = obj.is_firmware()
                        if state1 == True and state2 == True: 
                            return [obj.device , True]
                        else:
                            return [obj.device,False]

                case 4:#push both personality and firmware
                    if self.personality_path == None or self.firmware_path == None:
                        return [obj.device,False]
                    else:
                        obj.erase_config()
                        obj.personality_path =self.personality_path
                        obj.firmware_path =self.firmware_path
                        state1 = obj.push(2)
                        time.sleep(20)# it takes like 10-14 seconds to install the firmware
                        for _ in range(5):
                            live = obj.is_alive()
                            if live == True:
                                break
                        state2 = obj.push(1)
                        state3 = obj.is_firmware()
                        state4 = obj.is_config()
                        if state1 == True and state2 == True and state3 == True and state4 == True:
                            return [obj.device , True]
                        else:
                            return [obj.device,False]
                case _:
                    return f"{obj.device} unsure how you got here but hey here we are, theres somehow no mode selected"

        else:
            return f"{obj.device} {False}cannot get read on menu, please debug using terra term"



        
        return f"{obj.device} completed {status}"

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

