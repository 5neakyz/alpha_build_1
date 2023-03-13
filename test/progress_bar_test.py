import threading
import time
from tkinter import Button, Tk, HORIZONTAL
from tkinter.ttk import Progressbar
import os



import dataclasses

@dataclasses.dataclass
class pb_data():
    """
    Data structure to hold the progress bar data.
    """
    progress: int = 0
    total: int = 0

    def add_to_progress(self, value):
        self.progress += value
        return self.progress

class MonApp(Tk):
    def __init__(self):
        super().__init__()

        self.btn = Button(self, text='Traitement', command=self.traitement)
        self.btn.grid(row=0, column=0)
        self.progress = Progressbar(self, orient=HORIZONTAL, length=100, mode='determinate')

    def traitement(self):
        def real_traitement():
            self.progress.grid(row=1,column=0)
            self.progress['value'] = 0 
            self.progress['maximum'] = 500
            for _ in range (5):
                self.progress['value'] +=20
                time.sleep(1)
            self.progress.grid_forget()

            self.btn['state']='normal'

        self.btn['state']='disabled'
        threading.Thread(target=real_traitement).start()





if __name__ == '__main__':
    # app = MonApp()
    # app.mainloop()
    # file_name = "J:/gitcode/Multi-ML-1.0/firmware/ml30/ML30_V_3.88.0_c741.bin"
    # file_stats = os.stat(file_name).st_size
    # print(file_stats)

    PB = pb_data()
    print(PB.total)