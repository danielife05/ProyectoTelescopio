import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import math
import numpy as np

#OCUPA QUE LOS PUNTOS ENTRE LOS PISTONES Y LA BASE QUEDEN FIJOS DE MANERA QUE LOS
#PISTONES SE MUEVAN COMO UN LIMPIAPARABRISAS EN CONJUNTO(LOS 2 SE MUEVEN A LA VEZ)
#OCUPAN DELIMITAR EL ESPACIO EN DONDE ES POSIBLE TENER EL PUNTO
#PUEDEN USAR LA FUNCION DE VALOR ABSOLUTO PARA QUE DENTRO DE ESA ÁREA ESTÉN LOS PUNTOS POSIBLES

class AplicacionTelescopio:
    def __init__(self, raiz):
        self.raiz = raiz
        self.raiz.title("Telescopio James Webb")

        # Definir constantes (Longitudes del espejo y pistones)
        self.L = tk.DoubleVar(value=12.0)  # Largo del espejo
        self.B = tk.DoubleVar(value=8.0)  # Base del espejo (separación entre pistones)
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

        tk.Label(marco_entrada, text="F (Distancia del foco al extremo izquierdo del espejo principal):").grid(row=4, column=0, sticky=tk.W)
        tk.Entry(marco_entrada, textvariable=self.F).grid(row=4, column=1)

        # Entradas para las coordenadas de P
        tk.Label(marco_entrada, text="Px (Coordenada x de P):").grid(row=5, column=0, sticky=tk.W)
        tk.Entry(marco_entrada, textvariable=self.Px_var).grid(row=5, column=1)

        tk.Label(marco_entrada, text="Py (Coordenada y de P):").grid(row=6, column=0, sticky=tk.W)
        tk.Entry(marco_entrada, textvariable=self.Py_var).grid(row=6, column=1)

        # Botón para calcular y dibujar
        tk.Button(marco_entrada, text="Calcular y Dibujar", command=self.calcular_y_dibujar).grid(row=7, column=0, columnspan=2, pady=5)

        # Área de salida para mostrar las longitudes de los pistones y el ángulo
        self.etiqueta_salida = tk.Label(self.raiz, text="", font=('Arial', 12))
        self.etiqueta_salida.pack()

        # Área de dibujo
        self.figura = plt.Figure(figsize=(6, 6))
        self.ax = self.figura.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.figura, master=self.raiz)
        self.canvas.get_tk_widget().pack()

    def calcular_y_dibujar(self):
        # Obtener los parámetros de entrada
        L = self.L.get()
        B = self.B.get()
        D = self.D.get()
        d_max = self.d_max.get()
        F = self.F.get()
        Px = self.Px_var.get()
        Py = self.Py_var.get()

        # Validaciones iniciales
        if Py < 0:
            messagebox.showerror("Error", "Las coordenadas de P deben estar en los primeros dos cuadrantes (Px puede ser positivo o negativo, Py ≥ 0).")
            return

        if not (0 < L <= d_max and 0 < B <= d_max):
            messagebox.showerror("Error", "Las longitudes deben ser proporcionales para que el telescopio sea posible.")
            return

        # Definir las coordenadas de las bases de los pistones
        A = (-B / 2, 0)
        B_punto = (B / 2, 0)

        # Definir el objetivo para que el espejo siga la proyección del punto P y sea perpendicular
        def calcular_angulos(x1, x2, desplazamiento):
            espejo_izq_x, espejo_izq_y = A[0] + desplazamiento, A[1] + x1
            espejo_der_x, espejo_der_y = B_punto[0] + desplazamiento, B_punto[1] + x2

            # Centro del espejo
            espejo_centro_x = (espejo_izq_x + espejo_der_x) / 2
            espejo_centro_y = (espejo_izq_y + espejo_der_y) / 2

            # Vector del espejo
            vector_espejo_x = espejo_der_x - espejo_izq_x
            vector_espejo_y = espejo_der_y - espejo_izq_y

            # Vector del punto P proyectado sobre el espejo
            vector_punto_x = Px - espejo_centro_x
            vector_punto_y = Py - espejo_centro_y

            # Calcular el ángulo entre el espejo y la proyección
            producto_punto = vector_espejo_x * vector_punto_x + vector_espejo_y * vector_punto_y
            magnitud_espejo = math.sqrt(vector_espejo_x**2 + vector_espejo_y**2)
            magnitud_punto = math.sqrt(vector_punto_x**2 + vector_punto_y**2)

            if magnitud_espejo == 0 or magnitud_punto == 0:
                return 0

            cos_theta = producto_punto / (magnitud_espejo * magnitud_punto)
            angulo = math.degrees(math.acos(max(min(cos_theta, 1), -1)))

            return abs(angulo - 90)  # Queremos que el ángulo sea lo más cercano a 90° posible

        # Buscar la mejor combinación de x1 y x2 dentro de los límites permitidos
        mejor_x1, mejor_x2, mejor_desplazamiento = D, D, 0
        mejor_angulo = calcular_angulos(D, D, 0)

        for desplazamiento in np.linspace(-B / 2, B / 2, 50):
            for x1 in np.linspace(D, d_max, 50):
                for x2 in np.linspace(D, d_max, 50):
                    angulo_actual = calcular_angulos(x1, x2, desplazamiento)
                    if angulo_actual < mejor_angulo:
                        mejor_angulo = angulo_actual
                        mejor_x1, mejor_x2, mejor_desplazamiento = x1, x2, desplazamiento

        x1, x2, desplazamiento = mejor_x1, mejor_x2, mejor_desplazamiento

        # Verificar si se encontró una solución válida
        if mejor_angulo > 5:  # Si el ángulo no es suficientemente cercano a 90°
            messagebox.showwarning("Advertencia", "No se encontraron longitudes válidas para los pistones dentro de los límites establecidos. Se dibujará el telescopio en su máxima extensión posible.")
            x1 = x2 = d_max
            desplazamiento = 0

        # Calcular el ángulo del espejo considerando la extensión de los pistones
        mitad_espejo_x = (A[0] + B_punto[0]) / 2 + desplazamiento
        mitad_espejo_y = (x1 + x2) / 2
        vector_punto_x = Px - mitad_espejo_x
        vector_punto_y = Py - mitad_espejo_y
        angulo_proyeccion = math.degrees(math.atan2(vector_punto_y, vector_punto_x))
        angulo_espejo = angulo_proyeccion - 90  # Asegurar perpendicularidad

        # Mostrar las longitudes de los pistones y el ángulo
        texto_salida = (
            f"Ángulo del espejo respecto a la horizontal: {angulo_espejo:.2f}°\n"
            f"Longitud del pistón izquierdo (x1): {x1:.2f}\n"
            f"Longitud del pistón derecho (x2): {x2:.2f}\n"
            f"Ángulo de la proyección del punto sobre el espejo: {angulo_proyeccion:.2f}°"
        )
        self.etiqueta_salida.config(text=texto_salida)

        # Dibujar el sistema
        self.dibujar_sistema(x1, x2, Px, Py, L, B, angulo_espejo, mitad_espejo_x, mitad_espejo_y, desplazamiento)

    def dibujar_sistema(self, x1, x2, Px, Py, L, B, angulo_espejo, mitad_espejo_x, mitad_espejo_y, desplazamiento):
        self.ax.clear()

        # Coordenadas de las bases de los pistones
        A = (-B / 2 + desplazamiento, 0)
        B_punto = (B / 2 + desplazamiento, 0)

        # Coordenadas del espejo rotado
        A_prima = (A[0], A[1] + x1)
        B_prima = (B_punto[0], B_punto[1] + x2)

        # Coordenadas del espejo
        espejo_izq = A_prima
        espejo_der = B_prima

        # Dibujar los pistones
        self.ax.plot([A[0], A_prima[0]], [A[1], A_prima[1]], 'b-', linewidth=3, label='Pistón Izquierdo')
        self.ax.plot([B_punto[0], B_prima[0]], [B_punto[1], B_prima[1]], 'b-', linewidth=3, label='Pistón Derecho')

        # Dibujar el espejo
        self.ax.plot([espejo_izq[0], espejo_der[0]], [espejo_izq[1], espejo_der[1]], 'r-', linewidth=4, label='Espejo')

        # Dibujar el punto P
        self.ax.plot(Px, Py, 'go', label='Punto P')

        # Dibujar la proyección del punto sobre el espejo
        self.ax.plot([Px, mitad_espejo_x], [Py, mitad_espejo_y], 'g--', linewidth=1, label='Proyección del Punto')

        # Configuración del gráfico
        self.ax.set_xlabel('Eje X')
        self.ax.set_ylabel('Eje Y')
        self.ax.set_title('Orientación del Espejo Secundario')
        self.ax.legend()
        self.ax.grid(True)
        self.ax.axis('equal')
        # Centrar el telescopio en el origen
        max_rango = max(abs(B / 2 + desplazamiento), abs(x1), abs(x2), abs(Px), abs(Py)) + 1
        self.ax.set_xlim(-max_rango, max_rango)
        self.ax.set_ylim(0, max_rango)

        # Dibujar
        self.canvas.draw()

# Crear la ventana principal
raiz = tk.Tk()
aplicacion = AplicacionTelescopio(raiz)
raiz.mainloop()