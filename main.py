
import tkinter as tk
import numpy as np

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from matplotlib import animation

import dynamics
from custom_widgets import EntryBox
from table import Table


def update_graphs():
    update_line()
    plot_potential()
    animate(0)
    update_animation()
    update_axis()
    fig.canvas.draw()
    potential_fig.canvas.draw()


def update_animation():
    xdata[:], ydata[:] = [], []
    anim_subplot.set_xlim(subplot.get_xlim())
    anim_subplot.set_ylim(subplot.get_ylim())


def update_line():
    global w_x, w_y, A_x, A_y, f
    line.set_ydata(A_y.value * np.sin(w_y.value * t + np.pi / 6 * f.value))
    line.set_xdata(A_x.value * np.sin(w_x.value * t))


def update_axis():
    subplot.set_aspect('equal', adjustable='datalim')
    subplot.relim()
    subplot.autoscale_view()


def set_up_canvas(figure, parent, column, row):
    c = FigureCanvasTkAgg(figure, master=parent)
    c.get_tk_widget().grid(column=column, row=row)
    c.draw()


def plot_potential():
    potential_subplot.cla()
    a = A_x.value if A_x.value > A_y.value else A_y.value
    x = np.arange(-a - .5, a + .5, 0.1)
    y = np.arange(-a - .5, a + .5, 0.1)
    x, y = np.meshgrid(x, y)
    z = dynamics.calc_potential_energy(A_x.value, w_x.value, x) + dynamics.calc_potential_energy(A_y.value, w_y.value, y)
    potential_subplot.plot_surface(x, y, z)
    #potential_subplot.pcolor(x,y,z)


def animate(i):
    x = A_x.value * np.sin(w_x.value * (0.01 * i))
    y = A_y.value * np.sin(w_y.value * (0.01 * i) + np.pi / 6 * f.value)
    point.set_data(x, y)
    return point,


def update_table(time):
    x = dynamics.calc_deviation(A_x.value, w_x.value, time, 0)
    y = dynamics.calc_deviation(A_y.value, w_y.value, time, f.value)
    v_x = dynamics.calc_osc_speed(time, w_x.value, A_x.value, 0)
    v_y = dynamics.calc_osc_speed(time, w_y.value, A_y.value, f.value)
    a_x = dynamics.calc_osc_acceleration_magnitude(time, w_x.value, A_x.value, 0)
    a_y = dynamics.calc_osc_acceleration_magnitude(time, w_y.value, A_y.value, f.value)
    e_k = dynamics.calc_kinetic_energy(1, (v_x ** 2 + v_y ** 2))
    e_p = dynamics.calc_potential_energy(1, w_x.value, x) + dynamics.calc_potential_energy(1, w_y.value, y)
    r = dynamics.calc_curvature(v_x,v_y,a_x,a_y)
    if r == -1:
        r = 'inf'
    list = [x,
            y,
            (v_x ** 2 + v_y ** 2) ** (1 / 2),
            (a_x ** 2 + a_y ** 2) ** (1 / 2),
            e_k,
            e_p,
            r]
    table.update(list)


def animate2(i):
    if i%10 == 0 :
        print(i)
    x = A_x.value * np.sin(w_x.value * (0.01 * i))
    y = A_y.value * np.sin(w_y.value * (0.01 * i) + np.pi / 6 * f.value)
    xdata.append(x)
    ydata.append(y)
    point2.set_data(x, y)
    anim_line.set_data(xdata, ydata)
    update_table(0.01*i)
    return point2,


def _quit():
    root.quit()
    root.destroy()


GRAPH_SIZE = 5
FONT_SIZE = 15

root = tk.Tk()
root.wm_title("Wykres drgan prostopadlych")
root.resizable(False, False)

main_frame = tk.Frame(master=root)
graphs_frame = tk.Frame(master=main_frame)
entry_frame = tk.Frame(master=main_frame)

A_y = EntryBox(entry_frame, "A\u2082:", 1, update_graphs)
A_x = EntryBox(entry_frame, "A\u2081:", 1, update_graphs)
w_y = EntryBox(entry_frame, "\u03C9\u2082:", 1, update_graphs)
w_x = EntryBox(entry_frame, "\u03C9\u2081:", 1, update_graphs)
f = EntryBox(entry_frame, "\u0394\u03C6 (*\u03C0/6):", 3, update_graphs)

t = np.arange(0, 100, 0.01)
x = A_x.value * np.sin(w_y.value * t)
y = A_y.value * np.sin(w_x.value * t + np.pi / 6 * f.value)

fig = Figure(figsize=(GRAPH_SIZE, GRAPH_SIZE), dpi=100)
subplot = fig.add_subplot(111)
line, = subplot.plot(x, y, 'g-')
point, = subplot.plot(0, 0, 'o')

fig.supxlabel("x [m]", fontsize=FONT_SIZE)
fig.supylabel("y [m]", fontsize=FONT_SIZE)
fig.suptitle(f'Wykres toru', fontsize=FONT_SIZE)

set_up_canvas(fig,graphs_frame, 1, 1)

potential_fig = Figure(figsize=(GRAPH_SIZE, GRAPH_SIZE), dpi=100)
potential_subplot = potential_fig.add_subplot(111, projection='3d')
#potential_subplot = potential_fig.add_subplot(111)

plot_potential()
potential_fig.suptitle(f'Wykres potencjału', fontsize=FONT_SIZE)
set_up_canvas(potential_fig, graphs_frame, 2, 1)

entry_frame.pack(side=tk.RIGHT)

table = Table(graphs_frame)
table.table_frame.grid(column=2, row=2)

main_frame.pack(fill=tk.BOTH, expand=True)
button = tk.Button(master=root, text="Zamknij", command=_quit)
button.pack(side=tk.BOTTOM)

anim = animation.FuncAnimation(fig, animate, interval=30)

anim_fig = Figure(figsize=(GRAPH_SIZE, GRAPH_SIZE), dpi=100)
anim_subplot = anim_fig.add_subplot(111)
anim_subplot.set_xlim([-1.2, 1.2])
anim_subplot.set_ylim([-1.2, 1.2])
anim_line, = anim_subplot.plot([], [], lw = 2)
xdata, ydata = [], []
point2, = anim_subplot.plot(0, 0, 'o')
set_up_canvas(anim_fig, graphs_frame, 1, 2)
anim2 = animation.FuncAnimation(anim_fig, animate2, interval=30)
anim_fig.supxlabel("x [m]", fontsize=FONT_SIZE)
anim_fig.supylabel("y [m]", fontsize=FONT_SIZE)
anim_fig.suptitle(f'Animacja', fontsize=FONT_SIZE)

fig.supxlabel("x [m]", fontsize=FONT_SIZE)
fig.supylabel("y [m]", fontsize=FONT_SIZE)
fig.suptitle(f'Wykres toru', fontsize=FONT_SIZE)
graphs_frame.pack(side=tk.LEFT)


tk.mainloop()

#Propozycja jak będziemy mieli za dużo czasu:
def Td():
    ax = plt.axes(projection='3d')

    t = np.arange(0,10,0.01)
    x = np.sin(2*t)
    y = np.sin(4*t)
    z = np.sin(6*t)

    ax.plot3D(x,y,z,'g-')
    plt.show()

#Td()

