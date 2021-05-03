from tkinter import * 
from tkinter.ttk import *
from time import strftime
from datetime import datetime, timedelta
from multiprocessing.connection import Listener

root = Tk()
root.title('Workstation')
root.geometry('400x300')
root['background'] = 'lightblue'

now = datetime.min
stopped = False
total_steps = 0

address = ('localhost', 6000)
listener = Listener(address)
conn = listener.accept()

def time():
    global now
    global stopped
    if not stopped:
        now += timedelta(seconds=1)
        string = str(now)[10:]
        lbl.config(text = string)
    lbl.after(1000, time)

def notice():
    text = Label(root, text="Time for a break!",
                 background='lightblue', foreground='red', font=('calibri', 20, 'bold'))
    text.pack(pady=40)
    text.after(5000 , lambda: text.destroy())

def step(s):
        st = "Great, you just took " + s + " steps!"
        text = Label(root, text=st,
                 background='lightblue', foreground='green2', font=('calibri', 20, 'bold'))
        text.pack(pady=40)
        text.after(7000 , lambda: text.destroy())

def pipe():
    global stopped
    global now
    global total_steps
    msg = conn.recv()
    if msg != 'empty':
        if msg == 'stop':
            stopped = True
        elif msg == 'vibrate':
            notice()
        else:
            s = int(msg)
            now = datetime.min
            stopped = False
            step(msg)
            total_steps += s
            txt = 'Total steps: ' + str(total_steps)
            steps.config(text=txt)
    steps.after(100, pipe)
  
lbl = Label(root, font = ('calibri', 40, 'bold'),
            background = 'white',
            foreground = 'black')
steps = Label(root, text="Total steps: 0", background='white', foreground='Black', font=('calibri', 16, 'bold'))

lbl.pack(pady=20)
steps.pack(pady=20)
time()
pipe()
  
root.mainloop()