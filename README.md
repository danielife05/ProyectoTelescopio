# Proyecto: Simulación de Orientación del Espejo Secundario del Telescopio James Webb

## Descripción
Este proyecto desarrolla un modelo matemático y visual basado en el sistema de orientación del espejo secundario del telescopio James Webb, empleando pistones lineales para ajustar con precisión su posición e inclinación. La implementación incluye un enfoque simplificado que permite determinar las longitudes de los pistones necesarias para enfocar el telescopio hacia un punto de interés específico en el espacio.

El sistema consta de un espejo secundario rectangular de largo \(L\) y dos pistones en sus extremos, ajustados a una base fija en el espejo principal de separación \(B\). La extensión de cada pistón \(x_i\) debe respetar los límites físicos establecidos: \(D \leq x_i \leq d_{max}\). La orientación se calcula asegurando que el espejo sea perpendicular a la dirección hacia el punto objetivo \(P(x, y)\).

---

## Objetivos
### General:
- Simular y validar un modelo matemático que permita la orientación precisa de un espejo secundario hacia un punto en el espacio.

### Específicos:
- Determinar las longitudes de los pistones (\(x_1\), \(x_2\)) necesarias para orientar el espejo hacia \(P(x, y)\).
- Realizar validaciones físicas y geométricas de los parámetros ingresados para garantizar la operatividad del sistema.
- Implementar una interfaz gráfica interactiva que permita visualizar los resultados y realizar simulaciones en diferentes configuraciones.

---

## Parámetros de Entrada
- **L**: Largo del espejo (en unidades).
- **B**: Separación entre los pistones (en unidades).
- **D**: Longitud mínima de los pistones (en unidades).
- **d_max**: Longitud máxima de los pistones (en unidades).
- **F**: Distancia del foco al extremo izquierdo del espejo principal (en unidades).
- **P(x, y)**: Coordenadas del punto objetivo en el espacio.

## Parámetros de Salida
- **x1**: Longitud del pistón izquierdo.
- **x2**: Longitud del pistón derecho.
- **\(\theta\)**: Ángulo de inclinación del espejo respecto a la horizontal.

---

