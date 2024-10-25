import asyncio
from sqlite3 import connect
from tkinter import *
from tkinter import ttk
from async_tkinter_loop import async_handler, async_mainloop
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backend_bases import key_press_handler
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from mavsdk import System
from mavsdk.action import ActionError
from mavsdk import mission_raw
from mavsdk.mission import (MissionItem, MissionPlan)

# Conexión a dron
mavsdk_server_ip = 'localhost'
mavsdk_server_port = 50051
drone_address = "udp://:14540"

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
label_conectado = ttk.Label(frame, text="desconectado")
button = ttk.Button(frame, text="Quit", command=root.destroy)
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.draw()
label_x = ttk.Label(frame, text="??")
label_y = ttk.Label(frame, text="?")
label_z = ttk.Label(frame, text="A?")


frame.grid()
label.grid(row=0, column=0)
label_conectado.grid(row=1, column=0)
button.grid(row=0, column=1)
canvas.get_tk_widget().grid(row=0, column=2)
label_x.grid(row=3, column=0, columnspan=2)
label_y.grid(row=4, column=0, columnspan=2)
label_z.grid(row=5, column=0, columnspan=2)


# Conexion con dron
evento_desconectar = asyncio.Event()
mavsdk = System(mavsdk_server_address=mavsdk_server_ip,
                port=mavsdk_server_port)
listeners = []


async def loop_conexion():
    print("Conectando")
    await mavsdk.connect(system_address=drone_address)
    print("Conectado")
    # event listeners
    listeners.append(asyncio.create_task(loop_estado()))
    await evento_desconectar.wait()
    print("se completo uno")
    for task in listeners:
        print("cancelando un task")
        task.cancel()
    print("fin")
    return

root.after(0, async_handler(loop_conexion))


async def loop_estado():
    try:
        async for connection_state in mavsdk.core.connection_state():
            label_conectado.config(
                text="conectado" if connection_state.is_connected else "desconectado")
    except Exception as e:
        return


async def loop_posicion():
    try:
        async for position in mavsdk.telemetry.position():
            label_x.config(text=f"lat: {position.latitude_deg} deg")
            label_y.config(text=f"lat: {position.longitude_deg} deg")
            label_z.config(text=f"alt: {position.relative_altitude_m} m")
    except Exception as e:
        return


def test():
    print("test")
    evento_desconectar.set()
    root.destroy()


root.protocol("WM_DELETE_WINDOW", test)
async_mainloop(root)
