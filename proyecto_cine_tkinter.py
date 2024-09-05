import tkinter as tk
import random
from tkinter import messagebox

# Inicializar el cine con 16 filas y 14 columnas
def inicializar_cine(filas, columnas):
    matriz = []
    for i in range(filas):
        fila = [str(j+1) for j in range(columnas)]  # Los asientos son numerados del 1 al 14
        matriz.append(fila)
    return matriz

# Función para ocupar asientos aleatoriamente
def ocupar_asientos_aleatoriamente(matriz, num_asientos_ocupados):
    filas = len(matriz)
    columnas = len(matriz[0])
    
    # Crear una lista de todos los asientos posibles
    asientos_disponibles = [(fila, col) for fila in range(filas) for col in range(columnas)]
    
    # Seleccionar al azar un número determinado de asientos
    asientos_ocupados = random.sample(asientos_disponibles, num_asientos_ocupados)
    
    # Marcar los asientos seleccionados como ocupados
    for fila, col in asientos_ocupados:
        matriz[fila][col] = "X"

# Función para reservar un asiento
def reservar_asiento(fila, col):
    if matriz[fila][col] == "X":
        messagebox.showerror("Error", "El asiento ya está ocupado.")
    else:
        matriz[fila][col] = "X"
        asientos[fila][col].config(text="X", state="disabled")
        messagebox.showinfo("Reserva", f"Asiento reservado en fila {fila + 1}, columna {col + 1}.")

# Función para inicializar la interfaz
def inicializar_interfaz(root, matriz):
    global asientos
    asientos = []
    for fila in range(len(matriz)):
        fila_botones = []
        for col in range(len(matriz[0])):
            if matriz[fila][col] == "X":
                boton = tk.Button(root, text="X", width=4, height=2, state="disabled")
            else:
                boton = tk.Button(root, text=matriz[fila][col], width=4, height=2, 
                                  command=lambda fila=fila, col=col: reservar_asiento(fila, col))
            boton.grid(row=fila, column=col)
            fila_botones.append(boton)
        asientos.append(fila_botones)

# Programa principal
def sistema_reserva_cine():
    global matriz
    filas = 16
    columnas = 14
    matriz = inicializar_cine(filas, columnas)

    # Ocupar asientos aleatoriamente
    ocupar_asientos_aleatoriamente(matriz, num_asientos_ocupados=30)

    # Crear ventana principal
    root = tk.Tk()
    root.title("Sistema de Reserva de Cine")

    # Inicializar la interfaz de asientos
    inicializar_interfaz(root, matriz)

    # Iniciar el loop de la interfaz
    root.mainloop()

# Ejecutar el sistema de reserva
sistema_reserva_cine()
