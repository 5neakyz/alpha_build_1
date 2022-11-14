import logging
import threading
import time
import concurrent.futures
def thread_function(name):
    logging.info("Thread %s: starting", name)
    time.sleep(2)
    logging.info("Thread %s: finishing", name)
    return True

if __name__ == "__main__":
    format = "%(asctime)s.%(msecs)04d: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO,
                        datefmt="%H:%M:%S")

    names = ["1","2","3"]
    results = []
    with concurrent.futures.ThreadPoolExecutor() as executor:# parallelism 
        tasks = [executor.submit(thread_function,device) for device in names]
        for x in concurrent.futures.as_completed(tasks):
            results.append(x.result())
    print(results)



    # threads = list()
    # for index in range(3):
    #     logging.info("Main    : create and start thread %d.", index)
    #     x = threading.Thread(target=thread_function, args=(index,))
    #     threads.append(x)
    #     x.start()

    # for index, thread in enumerate(threads):
    #     logging.info("Main    : before joining thread %d.", index)
    #     thread.join()
    #     logging.info("Main    : thread %d done", index)
