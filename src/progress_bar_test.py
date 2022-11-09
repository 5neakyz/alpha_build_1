import threading
import time
from tkinter import Button, Tk, HORIZONTAL
from tkinter.ttk import Progressbar
import os





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
    def func():
        for _ in range(5):
            print(_)
            if _ == 3:
                print("breaking")
                break
        else:
            print("else")
            return False
        print("outside")
        return True

    print(func())