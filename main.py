import sys
import numpy as np
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QGridLayout, QHBoxLayout
)
from PyQt5.QtGui import QPixmap
from integracion import evaluar_fuerza, trabajo_sumatoria, trabajo_integral
from graficos import MplCanvas, graficar_integral, graficar_sumatoria
from utilidades import redondear_discreto
import matplotlib.pyplot as plt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Área bajo la curva (Trabajo = Fuerza x Distancia)")
        self.setGeometry(100, 100, 1000, 800)

        # Estilo general
        self.setStyleSheet("background-color: #f0f0f0;")

        layout = QHBoxLayout()

        grid_layout = QGridLayout()

        self.polinomio_label = QLabel("Ingrese el polinomio de la fuerza (en función de x):")
        self.polinomio_label.setStyleSheet("font-weight: bold; color: #333;")
        self.polinomio_input = QLineEdit()
        self.polinomio_input.setPlaceholderText("Ejemplo: 2*x**3 - 3*x**2 + 4*x + 5")
        self.polinomio_input.setStyleSheet("padding: 5px; border: 1px solid #ccc;")

        self.a_label = QLabel("Ingrese la distancia inicial (a):")
        self.a_label.setStyleSheet("font-weight: bold; color: #333;")
        self.a_input = QLineEdit()
        self.a_input.setPlaceholderText("Ejemplo: 0 (metros)")
        self.a_input.setStyleSheet("padding: 5px; border: 1px solid #ccc;")

        self.b_label = QLabel("Ingrese la distancia final (b):")
        self.b_label.setStyleSheet("font-weight: bold; color: #333;")
        self.b_input = QLineEdit()
        self.b_input.setPlaceholderText("Ejemplo: 5 (metros)")
        self.b_input.setStyleSheet("padding: 5px; border: 1px solid #ccc;")

        self.n_label = QLabel("Número de intervalos para la sumatoria discreta (n):")
        self.n_label.setStyleSheet("font-weight: bold; color: #333;")
        self.n_input = QLineEdit()
        self.n_input.setPlaceholderText("Ejemplo: 100")
        self.n_input.setStyleSheet("padding: 5px; border: 1px solid #ccc;")

        self.calcular_button = QPushButton("Calcular")
        self.calcular_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50; 
                color: white; 
                padding: 10px; 
                border: none; 
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        self.calcular_button.clicked.connect(self.calcular_trabajo)

        self.resultado_label = QLabel("Resultado:")
        self.resultado_label.setStyleSheet("font-weight: bold; color: #333;")
        self.resultado_integral = QLabel("Trabajo por integral: ")
        self.resultado_sumatoria = QLabel("Trabajo por sumatoria: ")
        self.resultado_desviacion = QLabel("Desviación porcentual: ")

        # QLabel para las fórmulas en formato LaTeX
        self.formula_integral_label = QLabel()
        self.formula_sumatoria_label = QLabel()

        grid_layout.addWidget(self.polinomio_label, 0, 0, 1, 2)
        grid_layout.addWidget(self.polinomio_input, 1, 0, 1, 2)
        grid_layout.addWidget(self.a_label, 2, 0, 1, 2)
        grid_layout.addWidget(self.a_input, 3, 0, 1, 2)
        grid_layout.addWidget(self.b_label, 4, 0, 1, 2)
        grid_layout.addWidget(self.b_input, 5, 0, 1, 2)
        grid_layout.addWidget(self.n_label, 6, 0, 1, 2)
        grid_layout.addWidget(self.n_input, 7, 0, 1, 2)
        grid_layout.addWidget(self.calcular_button, 8, 0, 1, 2)
        grid_layout.addWidget(self.resultado_label, 9, 0, 1, 2)
        grid_layout.addWidget(self.resultado_integral, 10, 0, 1, 2)
        grid_layout.addWidget(self.resultado_sumatoria, 11, 0, 1, 2)
        grid_layout.addWidget(self.resultado_desviacion, 12, 0, 1, 2)
        grid_layout.addWidget(self.formula_integral_label, 13, 0, 1, 2)
        grid_layout.addWidget(self.formula_sumatoria_label, 14, 0, 1, 2)

        self.graph_layout = QVBoxLayout()
        self.canvas_integral = MplCanvas(self, width=5, height=4, dpi=100)
        self.canvas_sumatoria = MplCanvas(self, width=5, height=4, dpi=100)

        self.graph_layout.addWidget(QLabel("Área bajo la curva por integral:"))
        self.graph_layout.addWidget(self.canvas_integral)
        self.graph_layout.addWidget(QLabel("Área bajo la curva por sumatoria:"))
        self.graph_layout.addWidget(self.canvas_sumatoria)

        layout.addLayout(grid_layout)
        layout.addLayout(self.graph_layout)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def calcular_trabajo(self):
        try:
            polinomio_str = self.polinomio_input.text()
            a = float(self.a_input.text())
            b = float(self.b_input.text())
            n = int(self.n_input.text())

            # Definir la función de fuerza usando eval (con cuidado)
            def fuerza(x):
                return eval(polinomio_str)

            a_discreto, b_discreto = redondear_discreto(a, b)

            trabajo_discreto = trabajo_sumatoria(fuerza, a_discreto, b_discreto, n)
            trabajo_continuo = trabajo_integral(fuerza, a, b)

            desviacion = abs(trabajo_continuo - trabajo_discreto) / trabajo_continuo * 100

            self.resultado_integral.setText(f"Trabajo por integral: {trabajo_continuo:.5f}")
            self.resultado_sumatoria.setText(f"Trabajo por sumatoria: {trabajo_discreto:.5f}")
            self.resultado_desviacion.setText(f"Desviación porcentual: {desviacion:.2f}%")

            graficar_integral(self.canvas_integral, fuerza, a, b)
            graficar_sumatoria(self.canvas_sumatoria, fuerza, a_discreto, b_discreto, n)

            # Generar imágenes de las fórmulas con la función de fuerza proporcionada
            self.generar_formula_integral(polinomio_str, a, b)
            self.generar_formula_sumatoria(polinomio_str, a_discreto, b_discreto, n)

        except Exception as e:
            self.resultado_label.setText(f"Error: {str(e)}")

    def generar_formula_integral(self, polinomio_str, a, b):
        formula = r'$\int_{%s}^{%s} %s \, dx = \text{Trabajo por integral}$' % (a, b, polinomio_str.replace('**', '^'))
        plt.figure(figsize=(2, 1))
        plt.text(0.5, 0.5, formula, fontsize=12, ha='center', va='center')
        plt.axis('off')
        plt.savefig('formula_integral.png', bbox_inches='tight', pad_inches=0.1)
        plt.close()

        pixmap = QPixmap('formula_integral.png')
        self.formula_integral_label.setPixmap(pixmap)

    def generar_formula_sumatoria(self, polinomio_str, a_discreto, b_discreto, n):
        # La representación de la sumatoria
        formula = r'$\sum_{i=0}^{%s} F(x_i) \cdot \Delta x = \text{Trabajo por sumatoria}$' % n
        plt.figure(figsize=(2, 1))
        plt.text(0.5, 0.5, formula, fontsize=12, ha='center', va='center')
        plt.axis('off')
        plt.savefig('formula_sumatoria.png', bbox_inches='tight', pad_inches=0.1)
        plt.close()

        pixmap = QPixmap('formula_sumatoria.png')
        self.formula_sumatoria_label.setPixmap(pixmap)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())
