# utilidades.py
import math

def redondear_discreto(a, b):
    a_discreto = math.floor(a)
    b_discreto = math.ceil(b)
    return a_discreto, b_discreto

