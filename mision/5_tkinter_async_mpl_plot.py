from tkinter import *
from tkinter import ttk
import time
import asyncio
from async_tkinter_loop import async_handler, async_mainloop

from matplotlib.backend_bases import key_press_handler
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

import matplotlib.pyplot as plt

root = Tk()
root.title("titulo")

x = [0, 1, 2, 3, 4]
y = [1, 2, 3, 4, 5]
fig = plt.figure()
plt.plot(x, y, marker='x')

frame = ttk.Frame(root, padding=20)
label = ttk.Label(frame, text="Hello World!")
# root.destroy funciona bien con tkinter async
button = ttk.Button(frame, text="Quit", command=root.destroy)
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.draw()

frame.grid()
label.grid(row=0, column=0)
button.grid(row=0, column=1)
canvas.get_tk_widget().grid(row=0, column=2)


async def printear():
    while True:
        print("hola", time.time_ns())
        await asyncio.sleep(1)

root.after(0, async_handler(printear))

async_mainloop(root)
