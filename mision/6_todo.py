# asyncio
import asyncio

# tkinter
from tkinter import *
from tkinter import ttk
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
button = ttk.Button(frame, text="Quit", command=root.destroy)
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.draw()

frame.grid()
label.grid(row=0, column=0)
button.grid(row=0, column=1)
canvas.get_tk_widget().grid(row=0, column=2)

# Conexion con dron y descargar mision
async def conexion():
    drone = System(mavsdk_server_address='localhost', port=50051)
    await drone.connect(system_address="udp://:14540")
    mision = await drone.mission_raw.download_mission()
    for item in mision:
        print(item)

root.after(0, async_handler(conexion))
async_mainloop(root)
