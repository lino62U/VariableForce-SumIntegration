# integracion.py
import numpy as np
from scipy.integrate import quad

def evaluar_fuerza(polinomio_str, x):
    try:
        polinomio_str = polinomio_str.replace("^", "**")
        return eval(polinomio_str)
    except Exception as e:
        raise ValueError(f"Error al evaluar la función: {e}")

def trabajo_sumatoria(fuerza, a, b, n):
    longitud_intervalo = (b - a) / n
    suma = 0
    for i in range(n):
        x_i = a + i * longitud_intervalo
        suma += fuerza(x_i) * longitud_intervalo
    return suma

def trabajo_integral(fuerza, a, b):
    integral, _ = quad(fuerza, a, b)
    return integral
