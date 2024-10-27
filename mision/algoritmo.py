# matplotlib
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backend_bases import key_press_handler
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# shapely
import shapely
import shapely.plotting
import shapely.ops

# trayectoria y obstaculo

x = [-367818907,
     -367845591,
     -367839231,
     -367824796,
     -367813797,
     -367844731,
     -367876351,
     -367912782,
     -367927216,
     -367954709,
     -367968456,
     -367984263,
     -367969143,
     -367944400,
     -367987012,
     -368035808,
     -368079790,
     -368094909,
     -368105904,
     -368129267,
     -368156753,
     -368156753]

y = [-730684814,
     -730720854,
     -730753899,
     -730826855,
     -730916977,
     -730968475,
     -731001949,
     -731001949,
     -730965042,
     -730953884,
     -730969334,
     -731032848,
     -731064606,
     -731227684,
     -731252575,
     -731275749,
     -731233692,
     -731167603,
     -731083488,
     -731083488,
     -731131554,
     -731204510]

obst_x = -367990000
obst_y = -730969334

fig = plt.figure()
plt.plot(x, y, marker='.')
plt.plot(obst_x, obst_y, marker='o', color='red')
# inicio en verde
plt.plot(x[0], y[0], marker='x', color='green')


# area a evitar
# https://shapely.readthedocs.io/en/stable/reference/shapely.Point.html
# https://shapely.readthedocs.io/en/stable/reference/shapely.plotting.plot_polygon.html#shapely.plotting.plot_polygon
contorno = shapely.boundary(shapely.Point(obst_x, obst_y).buffer(100000))
shapely.plotting.plot_line(contorno)


# iterar sobre segmentos de linea

entrada = False
salida = False

# encontrar primera y ultima interseccion
for i in range(0, len(x)-1):
    segmento = shapely.LineString([(x[i], y[i]), (x[i+1], y[i+1])])
    interseccion = shapely.intersection(contorno, segmento)
    if not interseccion.is_empty:
        if entrada == False:
            entrada = interseccion
        else:
            salida = interseccion

if entrada != False:
    shapely.plotting.plot_points(entrada)

if salida != False:
    shapely.plotting.plot_points(salida)

# shapely es muy challa
# sale mejor hacerlo con ecuaciones

plt.show()
