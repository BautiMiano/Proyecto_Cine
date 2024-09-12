import tkinter as tk
from tkinter import simpledialog, messagebox
from PIL import Image, ImageTk
import random
from datetime import datetime, timedelta

# Función para inicializar el cine
def inicializar_cine(filas, columnas):
    matriz = []
    for i in range(filas):
        fila = [str(j+1) for j in range(columnas)]
        matriz.append(fila)
    return matriz

# Función para ocupar asientos aleatoriamente
def ocupar_asientos_aleatoriamente(matriz, num_asientos_ocupados):
    filas = len(matriz)
    columnas = len(matriz[0])
    asientos_disponibles = [(fila, col) for fila in range(filas) for col in range(columnas)]
    asientos_ocupados = random.sample(asientos_disponibles, num_asientos_ocupados)
    for fila, col in asientos_ocupados:
        matriz[fila][col] = "X"

# Función para ingresar datos del usuario


def ingresar_datos():
    global nombre, edad
    nombre = simpledialog.askstring("Nombre", "Ingrese su nombre:")
    edad = simpledialog.askinteger("Edad", "Ingrese su edad:", minvalue=0, maxvalue=120)
    if nombre and edad is not None:
        mostrar_peliculas()
    else:
        messagebox.showwarning("Entrada Inválida", "Por favor, ingrese todos los datos correctamente.")
    return nombre, edad

# Función para mostrar las películas disponibles como botones
def mostrar_peliculas():
    peliculas = ["Deadpool & Wolverine", "La Trampa", "Kill Masacre En El Tren"] if edad >= 18 else ["Intensamente 2", "Mi Villano Favorito 4"]

    ventana_peliculas = tk.Toplevel(root)
    ventana_peliculas.title("Seleccionar Película")

    tk.Label(ventana_peliculas, text="Seleccione una película:", font=('Helvetica', 16, 'bold')).pack(pady=10)

    for pelicula in peliculas:
        boton_pelicula = tk.Button(ventana_peliculas, text=pelicula, width=20, height=2, command=lambda p=pelicula: seleccionar_pelicula(p), bg='red', fg='white')
        boton_pelicula.pack(pady=5)

# Función para manejar la selección de película
def seleccionar_pelicula(pelicula):
    global pelicula_seleccionada
    pelicula_seleccionada = pelicula
    mostrar_fecha_y_horarios()

# Función para mostrar opciones de fecha y horarios
def mostrar_fecha_y_horarios():
    ventana_fecha_horarios = tk.Toplevel(root)
    ventana_fecha_horarios.title("Seleccionar Fecha y Horario")

    tk.Label(ventana_fecha_horarios, text="Seleccione una fecha:", font=('Helvetica', 16, 'bold')).pack(pady=10)

    fecha_opciones = ["Hoy", "Mañana"]
    for fecha in fecha_opciones:
        boton_fecha = tk.Button(ventana_fecha_horarios, text=fecha, width=20, height=2, command=lambda f=fecha: seleccionar_fecha(f), bg='red', fg='white')
        boton_fecha.pack(pady=5)

# Función para manejar la selección de fecha
def seleccionar_fecha(fecha):
    global fecha_seleccionada
    fecha_seleccionada = datetime.now() if fecha == "Hoy" else datetime.now() + timedelta(days=1)
    mostrar_horarios()

# Función para mostrar los horarios disponibles como botones
def mostrar_horarios():
    ventana_horarios = tk.Toplevel(root)
    ventana_horarios.title("Seleccionar Horario")

    tk.Label(ventana_horarios, text=f"Selecciona un horario para la película '{pelicula_seleccionada}'", font=('Helvetica', 16, 'bold')).pack(pady=10)

    franjas_horarias = {
        "Mediodía": [f"{random.randint(12, 13)}:{random.choice(['00', '15', '30', '45'])}"],
        "Tarde": [f"{random.randint(15, 17)}:{random.choice(['00', '15', '30', '45'])}"],
        "Noche": [f"{random.randint(19, 21)}:{random.choice(['00', '15', '30', '45'])}"]
    }

    for franja, horas in franjas_horarias.items():
        tk.Label(ventana_horarios, text=franja, font=('Helvetica', 14, 'bold')).pack(pady=5)
        for hora in horas:
            boton_hora = tk.Button(ventana_horarios, text=hora, width=10, height=2, command=lambda h=hora: seleccionar_horario(h), bg='red', fg='white')
            boton_hora.pack(pady=5)

# Función para manejar la selección de horario
def seleccionar_horario(hora):
    global horario_seleccionado
    horario_seleccionado = hora
    mostrar_asientos()

# Función para mostrar la grilla de asientos
def mostrar_asientos():
    filas = 16
    columnas = 14
    global matriz
    matriz = inicializar_cine(filas, columnas)
    ocupar_asientos_aleatoriamente(matriz, num_asientos_ocupados=30)

    ventana_asientos = tk.Toplevel(root)
    ventana_asientos.title("Seleccionar Asiento")

    pantalla_label = tk.Label(ventana_asientos, text="Pantalla", font=('Helvetica', 16, 'bold'), bg='gray', fg='white', width=50)
    pantalla_label.grid(row=0, column=0, columnspan=columnas, pady=10)

    for i in range(filas):
        for j in range(columnas):
            estado_asiento = "X" if matriz[i][j] == "X" else str(j+1)
            color = 'red' if estado_asiento == "X" else 'lightblue'
            boton_asiento = tk.Button(ventana_asientos, text=f"{estado_asiento}", width=3, height=2, bg=color,
                                     command=lambda fila=i, col=j: seleccionar_asiento(fila, col))
            boton_asiento.grid(row=i+1, column=j, padx=2, pady=2)

# Función para seleccionar el asiento
def seleccionar_asiento(fila, col):
    if matriz[fila][col] == "X":
        messagebox.showerror("Error", "El asiento ya está ocupado.")
    else:
        matriz[fila][col] = "X"
        fecha_formateada = fecha_seleccionada.strftime("%d/%m/%Y")
        messagebox.showinfo("Reserva Confirmada", f"{nombre}: Has reservado para ver '{pelicula_seleccionada}' en la fila {fila + 1}, asiento {col + 1} el día {fecha_formateada} a las {horario_seleccionado}. Lo esperamos en el cine.")

# Crear la ventana principal
root = tk.Tk()
root.title("Proyecto Cine")
root.geometry("400x500") 

# Cargar y mostrar la imagen del logo
try:
    logo_imagen = Image.open("C:/Users/Fede/UADE/Progra1/proyecto_cine/img/logo2.png")
    logo_imagen = logo_imagen.resize((250, 250), Image.Resampling.LANCZOS) 
    logo_imagen_tk = ImageTk.PhotoImage(logo_imagen)
    
    logo_label = tk.Label(root, image=logo_imagen_tk)
    logo_label.pack(pady=10)
except Exception as e:
    print(f"No se pudo cargar la imagen del logo: {e}")


titulo_label = tk.Label(root, text="Proyecto Cine", font=('Helvetica', 24, 'bold'), fg='red')
titulo_label.pack(pady=20)

tk.Button(root, text="Comenzar Reserva", command=ingresar_datos, font=('Helvetica', 12, 'bold'), bg='red', fg='white').pack(pady=20)


#DICCIONARIO
# ingresar_datos= {
#             "nombre":nombre,
#             "edad":edad 
#     }
root.mainloop()