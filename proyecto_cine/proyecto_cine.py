import random

# Función para imprimir la disposición de los asientos
def imprimir_matriz(matriz):
    cont = 1
    print("Disponibilidad de asientos (X = Ocupado):")
    for fila in matriz:
        print(fila, cont)
        cont += 1

# Función para validar entradas numéricas
def input_numero(mensaje, minimo, maximo):
    while True:
        try:
            numero = int(input(mensaje))
            if minimo <= numero <= maximo:
                return numero
            else:
                print(f"Por favor, ingrese un número entre {minimo} y {maximo}.")
        except ValueError:
            print("Entrada inválida, ingrese un número.")

# Función para seleccionar la película según la edad
def seleccionar_pelicula(edad):
    if edad >= 18:
        peliculas = ["Alien", "El Secreto de Sus Ojos", "Rápido y Furioso"]
    else:
        peliculas = ["Intensamente", "Gaturro"]

    print("Películas disponibles:")
    for idx, pelicula in enumerate(peliculas, start=1):
        print(f"{idx}. {pelicula}")

    seleccion = input_numero("Seleccione el número de la película: ", 1, len(peliculas))
    return peliculas[seleccion - 1], seleccion

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

# Función para seleccionar el asiento y marcarlo como ocupado
def seleccionar_asiento(matriz):
    imprimir_matriz(matriz)
    sel_fil = input_numero("Seleccione la fila de su asiento (1-16): ", 1, len(matriz))
    
    # Verificar que el asiento no esté ocupado
    while True:
        sel_col = input_numero(f"Seleccione el asiento en la fila {sel_fil} (1-14): ", 1, len(matriz[0]))
        if matriz[sel_fil - 1][sel_col - 1] != "X":
            matriz[sel_fil - 1][sel_col - 1] = "X"  # Marcar asiento como ocupado
            break
        else:
            print("El asiento ya está ocupado. Por favor, seleccione otro.")
    
    return sel_fil, sel_col

# Programa principal
def sistema_reserva_cine():
    nombre = input("Ingrese su nombre: ")
    edad = input_numero("Ingrese su edad: ", 0, 120)

    filas = 16
    columnas = 14
    matriz = inicializar_cine(filas, columnas)

    # Ocupar asientos aleatoriamente (puedes cambiar el número de asientos ocupados)
    ocupar_asientos_aleatoriamente(matriz, num_asientos_ocupados=30)

    # Selección de película
    pelicula, sala = seleccionar_pelicula(edad)

    # Selección de asiento
    sel_fil, sel_col = seleccionar_asiento(matriz)

    # Confirmación de reserva
    print(f"Felicidades, {nombre}! Ya reservaste tu entrada para '{pelicula}' en la sala {sala}.")
    print(f"Tu asiento está en la fila {sel_fil}, asiento {sel_col}.")

# Ejecutar el sistema de reserva
sistema_reserva_cine()
