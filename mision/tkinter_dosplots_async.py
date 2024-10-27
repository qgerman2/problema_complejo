from tkinter import *
from tkinter import ttk
import time
import math
import asyncio
from async_tkinter_loop import async_handler, async_mainloop

from matplotlib.backend_bases import key_press_handler
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

import matplotlib.pyplot as plt

root = Tk()
root.title("titulo")

# Multiples figuras en matplotlib
# https://matplotlib.org/stable/gallery/subplots_axes_and_figures/multiple_figs_demo.html

x = [0, 1, 2, 3, 4]
y = [1, 2, 3, 4, 5]
fig = plt.figure(1)
plt.plot(x, y, marker='x')

fig2 = plt.figure(2)
plt.plot(x, y, marker='o')

frame = ttk.Frame(root, padding=20)
label = ttk.Label(frame, text="Hello World!")
button = ttk.Button(frame, text="Quit", command=root.destroy)
canvas = FigureCanvasTkAgg(fig, master=root)
canvas2 = FigureCanvasTkAgg(fig2, master=root)

frame.grid()
label.grid(row=0, column=0)
button.grid(row=0, column=1)
canvas.get_tk_widget().grid(row=0, column=2)
canvas2.get_tk_widget().grid(row=0, column=3)

# mundo asincronico


async def inicio():
    # correr dos funciones en paralelo
    asyncio.create_task(printear())
    asyncio.create_task(printear2())


async def printear():
    while True:
        t = time.time()
        x = [0, 0.01, 0.02, 0.03, 0.04]
        y = [math.sin(t), math.sin(t+0.01), math.sin(t+0.02),
             math.sin(t+0.03), math.sin(t+0.04)]
        plt.figure(1)
        plt.clf()
        plt.plot(x, y, marker='x')
        plt.ylim(-1, 1)
        canvas.draw()
        await asyncio.sleep(0.01)


async def printear2():
    while True:
        t = time.time()
        x = [0, 0.01, 0.02, 0.03, 0.04]
        y = [math.cos(t), math.cos(t+0.01), math.cos(t+0.02),
             math.cos(t+0.03), math.cos(t+0.04)]
        plt.figure(2)
        # plt.clf()
        plt.ylim(-1, 1)
        plt.xlim(0, 0.04)
        plt.plot(x, y, marker='o', color='r')
        canvas2.draw()
        await asyncio.sleep(0.01)


root.after(0, async_handler(inicio))

async_mainloop(root)
