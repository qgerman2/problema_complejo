import matplotlib
import matplotlib.pyplot as plt

# https://matplotlib.org/stable/users/explain/figure/backends.html
matplotlib.use("TkAgg")

x = [0, 1, 2, 3, 4]
y = [1, 2, 3, 4, 5]

# https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.plot.html
fig = plt.figure()
plt.plot(x, y, marker='x')
plt.show()
