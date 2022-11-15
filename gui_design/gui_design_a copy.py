import logging
import threading
import time
import concurrent.futures
def thread_function(name):
    logging.info("Thread %s: starting", name)
    time.sleep(1)
    logging.info("Thread %s: finishing", name)
    #return True

if __name__ == "__main__":
    format = "%(asctime)s.%(msecs)04d: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO,
                        datefmt="%H:%M:%S")

    # names = ["1","2","3"]
    # results = [["1",True],["2",False],["3",False]]
    # print(any(False in result for result in results))

    # timenow = time.time()
    # for _ in range(10):
    #     print(f"attempt {_} of 10 : total time waited {time.time() - timenow}")
    #     time.sleep(0.2)


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


    test = threading.Thread(target=thread_function,args="a")
    logging.info(f"is thread alive 1 {test.is_alive()}")
    test.start()
    logging.info(f"is thread alive 2 {test.is_alive()}")
    time.sleep(0.5)
    logging.info(f"is thread alive 3 {test.is_alive()}")
    time.sleep(3)
    logging.info(f"is thread alive 4 {test.is_alive()}")
