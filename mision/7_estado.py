import os

# asyncio
import asyncio

# tkinter
from tkinter import *
from tkinter import ttk
from tracemalloc import stop
from async_tkinter_loop import async_handler, async_mainloop

# matplotlib
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backend_bases import key_press_handler
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# mavsdk
from mavsdk import System
from mavsdk.action import ActionError
from mavsdk import mission_raw
from mavsdk.mission import (MissionItem, MissionPlan)

# Figura de matplotlib
x = [0, 1, 2, 3, 4]
y = [1, 2, 3, 4, 5]
fig = plt.figure()
plt.plot(x, y, marker='x')

# Ventana de tkinter
root = Tk()
root.title("titulo")

frame = ttk.Frame(root, padding=20)
label = ttk.Label(frame, text="Hello World!")
button = ttk.Button(frame, text="Quit", command=lambda: os._exit(0))
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.draw()

frame.grid()
label.grid(row=0, column=0)
button.grid(row=0, column=1)
canvas.get_tk_widget().grid(row=0, column=2)

# Conexion con dron y descargar mision
address = "tcp://:5762"


async def conexion():
    drone = System()
    await drone.connect(address)
    async for connection_state in drone.core.connection_state():
        texto = f"estado: {"conectado" if connection_state.is_connected else "desconectado"}"
        label.config(text=texto)

root.after(0, async_handler(conexion))


root.protocol("WM_DELETE_WINDOW", lambda: os._exit(0))
async_mainloop(root)
