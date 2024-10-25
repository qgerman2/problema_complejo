from tkinter import *
from tkinter import ttk
import time
import asyncio
from async_tkinter_loop import async_handler, async_mainloop

root = Tk()
root.title("titulo")

frame = ttk.Frame(root, padding=20)
label = ttk.Label(frame, text="Hello World!")
button = ttk.Button(frame, text="Quit", command=root.destroy)

frame.grid()
label.grid(row=0, column=0)
button.grid(row=0, column=1)

async def printear():
    while True:
        print("hola", time.time_ns())
        await asyncio.sleep(1)

root.after(0, async_handler(printear))
async_mainloop(root)
