import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import math
import numpy as np


class AplicacionTelescopio:
    def __init__(self, raiz):
        self.raiz = raiz
        self.raiz.title("Telescopio James Webb")

        # Definir constantes (Longitudes del espejo y pistones)
        self.L = tk.DoubleVar(value=12.0)  # Largo del espejo
        self.B = tk.DoubleVar(value=14.0)  # Base del espejo (separación entre pistones)
        self.D = tk.DoubleVar(value=4.0)  # Longitud mínima de los pistones
        self.d_max = tk.DoubleVar(value=20.0)  # Longitud máxima de los pistones
        self.F = tk.DoubleVar(value=6.0)  # Distancia del foco al extremo izquierdo del espejo principal

        # Variables de entrada para las coordenadas de P
        self.Px_var = tk.DoubleVar(value=8.0)
        self.Py_var = tk.DoubleVar(value=12.0)

        self.crear_widgets()
        self.calcular_y_dibujar()

    def crear_widgets(self):
        # Marco de entrada
        marco_entrada = tk.Frame(self.raiz)
        marco_entrada.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)

        # Entradas para los parámetros del telescopio
        tk.Label(marco_entrada, text="L (Largo del espejo):").grid(row=0, column=0, sticky=tk.W)
        tk.Entry(marco_entrada, textvariable=self.L).grid(row=0, column=1)

        tk.Label(marco_entrada, text="B (Base del espejo):").grid(row=1, column=0, sticky=tk.W)
        tk.Entry(marco_entrada, textvariable=self.B).grid(row=1, column=1)

        tk.Label(marco_entrada, text="D (Longitud mínima de los pistones):").grid(row=2, column=0, sticky=tk.W)
        tk.Entry(marco_entrada, textvariable=self.D).grid(row=2, column=1)

        tk.Label(marco_entrada, text="d_max (Longitud máxima de los pistones):").grid(row=3, column=0, sticky=tk.W)
        tk.Entry(marco_entrada, textvariable=self.d_max).grid(row=3, column=1)

        tk.Label(marco_entrada, text="F (Distancia del foco al extremo izquierdo del espejo principal):").grid(row=4,
                                                                                                               column=0,
                                                                                                               sticky=tk.W)
        tk.Entry(marco_entrada, textvariable=self.F).grid(row=4, column=1)

        # Entradas para las coordenadas de P
        tk.Label(marco_entrada, text="Px (Coordenada x de P):").grid(row=5, column=0, sticky=tk.W)
        tk.Entry(marco_entrada, textvariable=self.Px_var).grid(row=5, column=1)

        tk.Label(marco_entrada, text="Py (Coordenada y de P):").grid(row=6, column=0, sticky=tk.W)
        tk.Entry(marco_entrada, textvariable=self.Py_var).grid(row=6, column=1)

        # Botón para calcular y dibujar
        tk.Button(marco_entrada, text="Calcular y Dibujar", command=self.calcular_y_dibujar).grid(row=7, column=0,
                                                                                                  columnspan=2, pady=5)

        # Área de salida para mostrar las longitudes de los pistones y el ángulo
        self.etiqueta_salida = tk.Label(self.raiz, text="", font=('Arial', 12))
        self.etiqueta_salida.pack()

        # Área de dibujo
        self.figura = plt.Figure(figsize=(8, 8))
        self.ax = self.figura.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.figura, master=self.raiz)
        self.canvas.get_tk_widget().pack()

    def calcular_y_dibujar(self):
        try:
            # Obtener los parámetros de entrada
            L = self.L.get()
            B = self.B.get()
            D = self.D.get()
            d_max = self.d_max.get()
            F = self.F.get()
            Px = self.Px_var.get()
            Py = self.Py_var.get()
        except tk.TclError:
            messagebox.showerror("Error", "Por favor, ingrese valores numéricos válidos.")
            return

        # Validaciones iniciales
        if Py < 0:
            messagebox.showerror("Error",
                                 "Las coordenadas de P deben estar en los primeros dos cuadrantes (Px puede ser positivo o negativo, Py ≥ 0).")
            return

        # PARCHE PARA CASO ESPECIAL (0,0)
        # Caso especial: Px = 0 y Py = 0
        if Px == 0 and Py == 0:
            messagebox.showwarning("Advertencia",
                                   "El punto P(0, 0) no genera una visualización válida. Se mostrará una posición de referencia.")
            Px = 1  # Establecer un valor mínimo para Px
            Py = 1  # Establecer un valor mínimo para Py

        # Validación de la relación 0 < L < B < d_max
        if not (0 < L < B < d_max):
            messagebox.showerror(
                "Error",
                "Los parámetros deben cumplir la relación: 0 < L < B < d_max.\n"
                "Por favor, ajusta los valores para que sean válidos."
            )
            return

        # Intentar encontrar la posición del espejo donde la proyección perpendicular cae en su punto medio
        encontrado = False
        for My in np.linspace(Py - L / 2, Py + L / 2, 500):
            N_x = -Px
            N_y = My - Py
            # Evitar división por cero
            if N_x == 0 and N_y == 0:
                continue

            # Dirección del espejo (normalizada)
            D_x = -N_y
            D_y = N_x
            norma = math.sqrt(D_x ** 2 + D_y ** 2)
            D_x /= norma
            D_y /= norma

            # Extremos del espejo
            espejo_izq_x = 0 + (-L / 2) * D_x
            espejo_izq_y = My + (-L / 2) * D_y
            espejo_der_x = 0 + (L / 2) * D_x
            espejo_der_y = My + (L / 2) * D_y

            # Longitudes de los pistones
            x1 = math.sqrt((espejo_izq_x - (-B / 2)) ** 2 + (espejo_izq_y - 0) ** 2)
            x2 = math.sqrt((espejo_der_x - (B / 2)) ** 2 + (espejo_der_y - 0) ** 2)

            # Validar que los pistones no se crucen
            if espejo_izq_y < 0 or espejo_der_y < 0:
                continue

            if D <= x1 <= d_max and D <= x2 <= d_max:
                encontrado = True
                break

        # Validar si P está directamente sobre el espejo
        # if encontrado and (-B / 2 <= Px <= B / 2) and (Py == My):
        #    messagebox.showwarning("Advertencia", "El punto P está directamente sobre el espejo. No se actualizará la gráfica.")
        #    return

        # Validar si los pistones se cruzan
        # if encontrado and espejo_izq_y > espejo_der_y:
        #    messagebox.showwarning("Advertencia", "Los pistones se cruzan. No se actualizará la gráfica.")
        #    return

        # Si no se encontró una solución válida, extender o contraer al máximo permitido
        if not encontrado:
            messagebox.showwarning(
                "Advertencia",
                "El punto está fuera del rango alcanzable. Se graficará el telescopio en su límite más cercano hacia la dirección del punto."
            )
            # Determinar las posiciones del pistón: uno en máxima elongación y otro en mínima
            x1 = d_max  # Pistón derecho en elongación máxima
            x2 = D  # Pistón izquierdo en elongación mínima

            # Dirección hacia el punto P
            theta = math.atan2(Py, Px)
            D_x = math.cos(theta)
            D_y = math.sin(theta)

            # Posición de los pistones en los límites máximos/mínimos
            espejo_izq_x = -B / 2 + x2 * D_x
            espejo_izq_y = max(0, x2 * D_y)  # Asegurarse de que y no sea negativo
            espejo_der_x = B / 2 + x1 * D_x
            espejo_der_y = max(0, x1 * D_y)  # Asegurarse de que y no sea negativo

            # Ajustar el espejo para que respete su longitud fija L
            espejo_centro_x = (espejo_izq_x + espejo_der_x) / 2
            espejo_centro_y = (espejo_izq_y + espejo_der_y) / 2

            espejo_izq_x = espejo_centro_x - (L / 2) * D_y
            espejo_izq_y = max(0, espejo_centro_y + (L / 2) * D_x)  # Asegurar que y no sea negativo
            espejo_der_x = espejo_centro_x + (L / 2) * D_y
            espejo_der_y = max(0, espejo_centro_y - (L / 2) * D_x)  # Asegurar que y no sea negativo

            # Ángulo del espejo respecto a la horizontal
            angulo_espejo = math.degrees(theta)

        # Ángulo del espejo respecto a la horizontal
        angulo_espejo = math.degrees(math.atan2(D_y, D_x))

        # Mostrar las longitudes de los pistones y el ángulo
        texto_salida = (
            f"Ángulo del espejo respecto a la horizontal: {angulo_espejo:.2f}°\n"
            f"Longitud del pistón izquierdo (x1): {x1:.2f}\n"
            f"Longitud del pistón derecho (x2): {x2:.2f}\n"
            f"Punto: {Px:.2f}, {Py:.2f}\n"
        )
        self.etiqueta_salida.config(text=texto_salida)

        # Dibujar el sistema
        self.dibujar_sistema(x1, x2, Px, Py, L, B, angulo_espejo, espejo_izq_x, espejo_izq_y, espejo_der_x,
                             espejo_der_y)

    def dibujar_sistema(self, x1, x2, Px, Py, L, B, angulo_espejo, espejo_izq_x, espejo_izq_y, espejo_der_x,
                        espejo_der_y):
        self.ax.clear()

        # Coordenadas de las bases de los pistones
        A = (-B / 2, 0)
        B_punto = (B / 2, 0)

        # Dibujar los pistones
        self.ax.plot([A[0], espejo_izq_x], [A[1], espejo_izq_y], 'b-', linewidth=3, label='Pistón Izquierdo')
        self.ax.plot([B_punto[0], espejo_der_x], [B_punto[1], espejo_der_y], 'b-', linewidth=3, label='Pistón Derecho')

        # Dibujar el espejo
        self.ax.plot([espejo_izq_x, espejo_der_x], [espejo_izq_y, espejo_der_y], 'r-', linewidth=4, label='Espejo')

        # Dibujar el punto P
        self.ax.plot(Px, Py, 'go', label='Punto P')

        # Dibujar la proyección perpendicular del punto P sobre el espejo (cae en el punto medio del espejo)
        mx = (espejo_izq_x + espejo_der_x) / 2
        my = (espejo_izq_y + espejo_der_y) / 2
        self.ax.plot([Px, mx], [Py, my], 'g--', linewidth=1, label='Proyección Perpendicular')

        # Configuración del gráfico
        self.ax.set_xlabel('Eje X')
        self.ax.set_ylabel('Eje Y')
        self.ax.set_title('Orientación del Espejo Secundario')
        self.ax.legend()
        self.ax.grid(True, which='both', linestyle='--', linewidth=0.5)
        self.ax.axis('equal')

        # Centrar el telescopio en el origen
        x_min = min(-B / 2, espejo_izq_x, Px) - 2  # Margen izquierdo
        x_max = max(B / 2, espejo_der_x, Px) + 2  # Margen derecho
        y_min = 0  # No permitir valores negativos en Y
        y_max = max(espejo_izq_y, espejo_der_y, Py) + 2  # Margen superior

        # Dibujar los ejes X=0 y Y=0
        self.ax.axhline(0, color='k', linewidth=1, label='Eje Y = 0', alpha=0.3)  # Eje X
        self.ax.axvline(0, color='k', linewidth=1, label='Eje X = 0', alpha =0.3)  # Eje Y

        self.ax.set_xlim(x_min, x_max)
        self.ax.set_ylim(y_min, y_max)

        # Dibujar
        self.canvas.draw()


# Crear la ventana principal
raiz = tk.Tk()
aplicacion = AplicacionTelescopio(raiz)
raiz.mainloop()