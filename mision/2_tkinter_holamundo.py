from tkinter import *
from tkinter import ttk
import time

# https://docs.python.org/3/library/tkinter.html#tkinter.Tk
root = Tk()
root.title("titulo")

# Contenido de la ventana
# https://tkdocs.com/tutorial/widgets.html#frame
frame = ttk.Frame(root, padding=20)
label = ttk.Label(frame, text="Hello World!")
button = ttk.Button(frame, text="Quit", command=root.destroy)

# Disposición de elementos
# https://tkdocs.com/tutorial/grid.html
frame.grid()
label.grid(row=0, column=0)
button.grid(row=0, column=1)

# Preparar una funcion que va a correr de fondo
# https://tkdocs.com/tutorial/eventloop.html
def printear():
    print("hola ", time.time_ns())
    root.after(1000, printear)
root.after(0, printear)

# Iniciar event loop
root.mainloop()
