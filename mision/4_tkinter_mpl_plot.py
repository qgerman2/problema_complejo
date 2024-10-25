from tkinter import *
from tkinter import ttk

# https://matplotlib.org/stable/gallery/user_interfaces/embedding_in_tk_sgskip.html
from matplotlib.backend_bases import key_press_handler
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

import matplotlib.pyplot as plt

root = Tk()
root.title("titulo")

# Figura de matplotlib
x = [0, 1, 2, 3, 4]
y = [1, 2, 3, 4, 5]
fig = plt.figure()
plt.plot(x, y, marker='x')

frame = ttk.Frame(root, padding=20)
label = ttk.Label(frame, text="Hello World!")
# root.quit parece cerrar correctamente python (en vez de root.destroy)
button = ttk.Button(frame, text="Quit", command=root.quit)
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.draw()

frame.grid()
label.grid(row=0, column=0)
button.grid(row=0, column=1)
canvas.get_tk_widget().grid(row=0, column=2)

root.protocol("WM_DELETE_WINDOW", root.quit)
root.mainloop()
