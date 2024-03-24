import tkinter as tk

def onKeyPress(event):
    text.insert('end', 'You pressed %s\n' % (event.keysym, ))

root = tk.Tk()
root.geometry('300x200')
text = tk.Text(root, background='black', foreground='white', font=('Comic Sans MS', 12))
text.pack()
root.bind('<KeyPress>', onKeyPress)
root.mainloop()
