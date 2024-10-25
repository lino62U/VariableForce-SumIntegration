# graficos.py
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

class MplCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = plt.Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super().__init__(fig)

def graficar_integral(canvas, fuerza, a, b):
    x = np.linspace(a, b, 100)
    y = fuerza(x)
    canvas.axes.clear()
    canvas.axes.plot(x, y, label='Fuerza (N)')
    canvas.axes.fill_between(x, y, alpha=0.5, label='Área bajo la curva')
    canvas.axes.set_title('Área bajo la curva por integral')
    canvas.axes.set_xlabel('Distancia (m)')
    canvas.axes.set_ylabel('Fuerza (N)')
    canvas.axes.legend()
    canvas.draw()

def graficar_sumatoria(canvas, fuerza, a, b, n):
    x = np.linspace(a, b, n + 1)
    y = fuerza(x)
    canvas.axes.clear()
    canvas.axes.plot(x, y, label='Fuerza (N)', color='blue')
    
    # Graficar los rectángulos
    for i in range(n):
        canvas.axes.bar(x[i], y[i], width=(x[i+1]-x[i]), alpha=0.5, align='edge', edgecolor='black', label='Sumatoria' if i == 0 else "")
    
    canvas.axes.set_title('Área bajo la curva por sumatoria')
    canvas.axes.set_xlabel('Distancia (m)')
    canvas.axes.set_ylabel('Fuerza (N)')
    canvas.axes.legend()
    canvas.draw()
