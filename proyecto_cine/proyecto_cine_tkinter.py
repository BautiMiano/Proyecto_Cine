import tkinter as tk
from tkinter import simpledialog, messagebox
from PIL import Image, ImageTk
import random
from tkcalendar import Calendar 
from datetime import datetime
import qrcode
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# Función para inicializar el cine
def inicializar_cine(filas, columnas):
    matriz = []
    matriz = [[str(j+1) for j in range(columnas)] for _ in range(filas)]
    return matriz

# Función para ocupar asientos aleatoriamente
def ocupar_asientos_aleatoriamente(matriz, num_asientos_ocupados):
    filas = len(matriz)
    columnas = len(matriz[0])
    asientos_disponibles = [(fila, col) for fila in range(filas) for col in range(columnas)]
    asientos_ocupados = random.sample(asientos_disponibles, num_asientos_ocupados)
    for fila, col in asientos_ocupados:
        matriz[fila][col] = "X"

# Función para sugerir películas según el nombre parcial
def sugerir_pelicula(parte_nombre, lista_peliculas):
    sugerencias = []
    parte_nombre = parte_nombre.lower()
    for pelicula in lista_peliculas:
        if parte_nombre in pelicula.lower():
            sugerencias.append(pelicula)
    return sugerencias

# Función para mostrar fecha y horarios
def mostrar_fecha_y_horarios():
    global root, fecha_seleccionada
    ventana_fecha = tk.Toplevel(root)
    ventana_fecha.title("Seleccionar Fecha")

    tk.Label(ventana_fecha, text="Seleccione una fecha:", font=('Helvetica', 16, 'bold')).pack(pady=10)

    cal = Calendar(ventana_fecha, selectmode='day', date_pattern='mm/dd/yy')
    cal.pack(pady=10)  

    tk.Button(ventana_fecha, text="Confirmar", command=lambda: seleccionar_fecha(cal.get_date(), ventana_fecha), bg='red', fg='white').pack(pady=10)

# Función para ingresar datos del usuario
def ingresar_datos():
    global nombre, edad, root
    nombre = simpledialog.askstring("Nombre", "Ingrese su nombre:")
    if not nombre:
        return
    edad = simpledialog.askinteger("Edad", "Ingrese su edad:", minvalue=0, maxvalue=120)
    if edad is None:
        return
    mostrar_fecha_y_horarios()

def seleccionar_fecha(fecha_str, ventana):
    global fecha_seleccionada
    # Convierte la fecha seleccionada del calendario a un objeto datetime
    fecha_seleccionada = datetime.strptime(fecha_str, "%m/%d/%y")
    ventana.destroy()  # Cierra la ventana actual
    mostrar_horarios()

def mostrar_horarios():
    global root, pelicula_seleccionada, horario_seleccionado
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
            boton_hora = tk.Button(ventana_horarios, text=hora,
                                   command=lambda h=hora: seleccionar_horario(h, ventana_horarios),
                                   width=10, height=2, bg='red', fg='white')
            boton_hora.pack(pady=5)

def seleccionar_horario(hora, ventana):
    global horario_seleccionado
    horario_seleccionado = hora
    ventana.destroy()  # Cierra la ventana actual
    mostrar_fecha_y_horarios()
    mostrar_peliculas()

# Función para mostrar las películas disponibles como botones
def mostrar_peliculas():
    global root, edad, pelicula_seleccionada, fecha_seleccionada, horario_seleccionado, cantidad_entradas, matriz, buscar_entry

    # Definir todas las películas disponibles
    peliculas_adultos = ["Deadpool & Wolverine", "La Trampa", "Kill Masacre En El Tren"]
    peliculas_todo_publico = ["Intensamente 2", "Mi Villano Favorito 4"]
    peliculas = peliculas_adultos + peliculas_todo_publico if edad >= 18 else peliculas_todo_publico

    ventana_peliculas = tk.Toplevel(root)
    ventana_peliculas.title("Seleccionar Película")

    tk.Label(ventana_peliculas, text="Cartelera de Películas:", font=('Helvetica', 16, 'bold')).pack(pady=10)

    # Mostrar todas las películas como botones
    for pelicula in peliculas:
        boton_pelicula = tk.Button(ventana_peliculas, text=pelicula, width=20, height=2,
                                   command=lambda p=pelicula: seleccionar_pelicula(p, ventana_peliculas),
                                   bg='red', fg='white')
        boton_pelicula.pack(pady=5)

    # Campo de entrada para buscar película
    tk.Label(ventana_peliculas, text="Buscar película por nombre:", font=('Helvetica', 12)).pack(pady=10)
    buscar_entry = tk.Entry(ventana_peliculas, width=30)
    buscar_entry.pack(pady=5)

    # Botón para buscar la película
    tk.Button(ventana_peliculas, text="Buscar",
              command=lambda: buscar_pelicula(buscar_entry.get(), peliculas, ventana_peliculas),
              bg='lightgreen', fg='black').pack(pady=10)

# Función para buscar película
def buscar_pelicula(parte_nombre, peliculas, ventana):
    if parte_nombre:
        sugerencias = sugerir_pelicula(parte_nombre, peliculas)
        if sugerencias:
            mostrar_peliculas_sugeridas(sugerencias, ventana)
        else:
            messagebox.showinfo("Sin coincidencias", "No se encontraron películas que coincidan.")
    else:
        messagebox.showwarning("Entrada Inválida", "Por favor, ingrese parte del nombre de la película.")

def mostrar_peliculas_sugeridas(peliculas, ventana_anterior):
    global root, pelicula_seleccionada
    ventana_sugerencias = tk.Toplevel(root)
    ventana_sugerencias.title("Sugerencias de Películas")

    tk.Label(ventana_sugerencias, text="Sugerencias:", font=('Helvetica', 16, 'bold')).pack(pady=10)

    for pelicula in peliculas:
        boton_pelicula = tk.Button(ventana_sugerencias, text=pelicula, width=20, height=2,
                                   command=lambda p=pelicula: seleccionar_pelicula(p, ventana_anterior),
                                   bg='red', fg='white')
        boton_pelicula.pack(pady=5)

def seleccionar_pelicula(pelicula, ventana):
    global pelicula_seleccionada, cantidad_entradas, cantidad_entradas_inicial
    pelicula_seleccionada = pelicula
    cantidad_entradas_inicial = cantidad_entradas 
    ventana.destroy()  # Cierra la ventana actual
    elegir_cant_entradas()

# Función para elegir la cantidad de entradas
def elegir_cant_entradas():
    ventana_entradas = tk.Toplevel(root)
    ventana_entradas.title("Seleccionar Cantidad de Entradas")

    tk.Label(ventana_entradas, text="Seleccione la cantidad de entradas:", font=('Helvetica', 16, 'bold')).pack(pady=10)

    cantidad_entry = tk.Entry(ventana_entradas, width=5)
    cantidad_entry.pack(pady=5)

    tk.Button(ventana_entradas, text="Confirmar", command=lambda: confirmar_cantidad(cantidad_entry.get(), ventana_entradas), bg='red', fg='white').pack(pady=10)

def confirmar_cantidad(cantidad, ventana):
    try:
        cantidad = int(cantidad)
        if cantidad > 0:
            global cantidad_entradas, cantidad_entradas_inicial
            cantidad_entradas = cantidad
            cantidad_entradas_inicial = cantidad
            ventana.destroy()  # Cierra la ventana actual
            mostrar_asientos()
        else:
            messagebox.showwarning("Entrada Inválida", "Por favor, ingrese una cantidad válida de entradas.")
    except ValueError:
        messagebox.showwarning("Entrada Inválida", "Por favor, ingrese un número válido.")
    except IndexError:
        messagebox.showerror("Error", "Ocurrió un error al procesar la cantidad de entradas. Por favor, intente nuevamente.")

def mostrar_asientos():
    global root, matriz, asientos_seleccionados
    filas = 16
    columnas = 14
    matriz = inicializar_cine(filas, columnas)
    ocupar_asientos_aleatoriamente(matriz, num_asientos_ocupados=30)

    ventana_asientos = tk.Toplevel(root)
    ventana_asientos.title("Seleccionar Asiento")

    pantalla_label = tk.Label(ventana_asientos, text="Pantalla", font=('Helvetica', 16, 'bold'), bg='gray', fg='white', width=50)
    pantalla_label.grid(row=0, column=0, columnspan=columnas, pady=10)

    asientos_seleccionados = []

    for i in range(filas):
        for j in range(columnas):
            estado_asiento = "X" if matriz[i][j] == "X" else str(j+1)
            color = 'red' if estado_asiento == "X" else 'lightblue'
            boton_asiento = tk.Button(ventana_asientos, text=f"{estado_asiento}", width=3, height=2, bg=color,
                                      command=lambda fila=i, col=j: seleccionar_asiento(fila, col, ventana_asientos))
            boton_asiento.grid(row=i+1, column=j, padx=2, pady=2)

def seleccionar_asiento(fila, col, ventana_asientos):
    global matriz, cantidad_entradas, asientos_seleccionados
    if matriz[fila][col] != "X":
        if len(asientos_seleccionados) < cantidad_entradas:
            matriz[fila][col] = "S"  # Marcar asiento seleccionado temporalmente
            asientos_seleccionados.append((fila, col))
            actualizar_asientos(ventana_asientos)
        else:
            messagebox.showwarning("Límite Alcanzado", f"Solo puede seleccionar {cantidad_entradas} asientos.")
    else:
        
        messagebox.showwarning("Asiento Ocupado", "El asiento seleccionado ya está ocupado.")

def actualizar_asientos(ventana_asientos):
    global matriz, asientos_seleccionados
    for widget in ventana_asientos.winfo_children():
        widget.destroy()

    pantalla_label = tk.Label(ventana_asientos, text="Pantalla", font=('Helvetica', 16, 'bold'), bg='gray', fg='white', width=50)
    pantalla_label.grid(row=0, column=0, columnspan=14, pady=10)

    for i in range(16):
        for j in range(14):
            estado_asiento = "X" if matriz[i][j] == "X" else ("S" if (i, j) in asientos_seleccionados else str(j+1))
            color = 'red' if estado_asiento == "X" else ('yellow' if estado_asiento == "S" else 'lightblue')
            boton_asiento = tk.Button(ventana_asientos, text=f"{estado_asiento}", width=3, height=2, bg=color,
                                      command=lambda fila=i, col=j: seleccionar_asiento(fila, col, ventana_asientos))
            boton_asiento.grid(row=i+1, column=j, padx=2, pady=2)

    if len(asientos_seleccionados) == cantidad_entradas:
        confirmar_asientos(ventana_asientos)

# Define el precio de una entrada
PRECIO_ENTRADA = 8000 

def mostrar_precio_total():
    global root, cantidad_entradas_inicial
    if cantidad_entradas_inicial is None:
        messagebox.showerror("Error", "La cantidad de entradas no está definida.")
        return
    precio_total = cantidad_entradas_inicial * PRECIO_ENTRADA

    ventana_precio = tk.Toplevel(root)
    ventana_precio.title("Precio Total")

    tk.Label(ventana_precio, text=f"El precio total de {cantidad_entradas_inicial} entradas es: ${precio_total}", font=('Helvetica', 16, 'bold')).pack(pady=10)
    tk.Button(ventana_precio, text="Proceder al Pago", command=lambda: proceder_al_pago(ventana_precio), bg='lightgreen', fg='black').pack(pady=10)

def proceder_al_pago(ventana_precio):
    ventana_precio.destroy()  # Cierra la ventana de precio total
    realizar_pago()  # Llama a la función para realizar el pago

# Llama a la función mostrar_precio_total después de confirmar los asientos
def confirmar_asientos(ventana_asientos):
    global matriz, asientos_seleccionados, cantidad_entradas, cantidad_entradas_inicial
    for fila, col in asientos_seleccionados:
        matriz[fila][col] = "X"  # Confirmar asientos seleccionados
    cantidad_entradas -= len(asientos_seleccionados)
    asientos_seleccionados = []
    if cantidad_entradas <= 0:
        ventana_asientos.destroy()  # Cierra la ventana de asientos
        messagebox.showinfo("Reserva Completa", "Ha reservado todos los asientos.")
        mostrar_precio_total()  # Llama a la función para mostrar el precio total
    else:
        messagebox.showinfo("Asientos Reservados", f"Ha reservado los asientos. Quedan {cantidad_entradas} asientos por reservar.")
        actualizar_asientos(ventana_asientos)

# Función para realizar el pago de las entradas
def realizar_pago():
    global root, cantidad_entradas
    ventana_pago = tk.Toplevel(root)
    ventana_pago.title("Realizar Pago")

    tk.Label(ventana_pago, text="Seleccione el método de pago:", font=('Helvetica', 16, 'bold')).pack(pady=10)

    metodos_pago = ["Tarjeta de Crédito", "Tarjeta de Débito", "Mercado Pago"]
    for metodo in metodos_pago:
        tk.Button(ventana_pago, text=metodo, width=20, height=2,
                  command=lambda m=metodo: abrir_detalles_pago(m, ventana_pago),
                  bg='lightblue', fg='black').pack(pady=5)

def abrir_detalles_pago(metodo, ventana):
    # Cierra la ventana de selección de método de pago
    ventana.destroy()
    
    if metodo == "Mercado Pago":
        generar_qr_pago()
    else:
        # Ventana para ingresar detalles del pago
        ventana_detalles = tk.Toplevel(root)
        ventana_detalles.title(f"Detalles de Pago con {metodo}")

        tk.Label(ventana_detalles, text=f"Ingrese los detalles para {metodo}:", font=('Helvetica', 16, 'bold')).pack(pady=10)

        tk.Label(ventana_detalles, text="Número de tarjeta:").pack(pady=5)
        numero_tarjeta = tk.Entry(ventana_detalles, width=30)
        numero_tarjeta.pack(pady=5)

        tk.Label(ventana_detalles, text="Fecha de expiración (MM/AA):").pack(pady=5)
        fecha_expiracion = tk.Entry(ventana_detalles, width=10)
        fecha_expiracion.pack(pady=5)

        tk.Label(ventana_detalles, text="Código de seguridad:").pack(pady=5)
        codigo_seguridad = tk.Entry(ventana_detalles, show='*', width=10)
        codigo_seguridad.pack(pady=5)

        tk.Button(ventana_detalles, text="Confirmar Pago", command=lambda: confirmar_pago(metodo, numero_tarjeta.get(), fecha_expiracion.get(), codigo_seguridad.get(), ventana_detalles)).pack(pady=10)

def generar_qr_pago():
    # Simular la URL de pago
    url_pago = "link.mercadopago.com.ar/proyectocine"
    
    # Generar el código QR
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(url_pago)
    qr.make(fit=True)

    img = qr.make_image(fill='black', back_color='white')
    img.save("qr_pago.png")

    # Crear ventana para mostrar el QR
    ventana_qr = tk.Toplevel(root)
    ventana_qr.title("Pago con Mercado Pago")
    
    tk.Label(ventana_qr, text="Escanee el código QR para realizar el pago:", font=('Helvetica', 16, 'bold')).pack(pady=10)
    
    # Mostrar la imagen QR
    img = Image.open("qr_pago.png")
    img.thumbnail((200, 200))  # Ajustar el tamaño
    img_tk = ImageTk.PhotoImage(img)
    label_img = tk.Label(ventana_qr, image=img_tk)
    label_img.image = img_tk  # Keep a reference to avoid garbage collection
    label_img.pack(pady=10)

    # Botón para confirmar el pago
    tk.Button(ventana_qr, text="Confirmar Pago", command=lambda: confirmar_pago_qr(ventana_qr), bg='lightgreen', fg='black').pack(pady=10)

    ventana_qr.mainloop()  # Mantiene la ventana abierta

def confirmar_pago_qr(ventana):
    global fecha_seleccionada
    messagebox.showinfo("Pago Realizado", "El pago con Mercado Pago ha sido realizado con éxito.")
    ventana.destroy()  # Cierra la ventana de QR
    imprimir_entrada()  # Llama a la función para imprimir la entrada
def confirmar_pago(metodo, numero_tarjeta, fecha_expiracion, codigo_seguridad, ventana):
    global fecha_seleccionada
    # Simulación de validación
    if not numero_tarjeta or not fecha_expiracion or not codigo_seguridad:
        messagebox.showwarning("Error", "Por favor, complete todos los campos.")
        return
    messagebox.showinfo("Pago Realizado", f"El pago con {metodo} ha sido realizado con éxito.\n\nDetalles de la transacción:\nNúmero de tarjeta: {numero_tarjeta}\nFecha de expiración: {fecha_expiracion}")
    imprimir_entrada()  # Llama a la función para imprimir la entrada
    ventana.destroy()  # Cierra la ventana de detalles de pago

def imprimir_entrada():
    global nombre, edad, pelicula_seleccionada, fecha_seleccionada, horario_seleccionado, cantidad_entradas_inicial
    try:
        nombre_archivo = f"entrada_{nombre}_{pelicula_seleccionada}.pdf"
        
        c = canvas.Canvas(nombre_archivo, pagesize=letter)
        c.setFont("Helvetica", 12)
        
        # Título
        c.drawString(100, 750, "Entrada de Cine")
        
        # Datos del usuario
        c.drawString(100, 730, f"Nombre: {nombre}")
        c.drawString(100, 710, f"Edad: {edad}")
        
        # Detalles de la película
        c.drawString(100, 690, f"Película: {pelicula_seleccionada}")
        c.drawString(100, 670, f"Fecha: {fecha_seleccionada.strftime('%d/%m/%Y') if fecha_seleccionada else 'Fecha no seleccionada'}")
        c.drawString(100, 650, f"Horario: {horario_seleccionado}")
        
        # Cantidad de entradas
        c.drawString(100, 630, f"Cantidad de Entradas: {cantidad_entradas_inicial}")
        
        # Instrucciones adicionales
        c.drawString(100, 600, "¡Disfruta de la película!")
        
        c.save()
        messagebox.showinfo("Impresión Exitosa", f"Entrada impresa: {nombre_archivo}")
    except Exception as e:
        messagebox.showerror("Error de Impresión", f"Ocurrió un error al imprimir la entrada: {e}")

def mostrar_entrada(nombre, edad, pelicula, fecha, horario, asientos):
    entrada_texto = f"--- Entrada de Cine ---\n"
    entrada_texto += f"Nombre: {nombre}\n"
    entrada_texto += f"Edad: {edad}\n"
    entrada_texto += f"Película: {pelicula}\n"
    entrada_texto += f"Fecha: {fecha.strftime('%d/%m/%Y')}\n"
    entrada_texto += f"Horario: {horario}\n"
    entrada_texto += f"Asientos seleccionados: {', '.join(asientos)}\n"
    
    # Crear una nueva ventana para mostrar la entrada
    ventana_entrada = tk.Toplevel()
    ventana_entrada.title("Entrada de Cine")
    label = tk.Label(ventana_entrada, text=entrada_texto, padx=10, pady=10)
    label.pack()
    
    # Botón para cerrar la ventana
    btn_cerrar = tk.Button(ventana_entrada, text="Cerrar", command=ventana_entrada.destroy)
    btn_cerrar.pack(pady=10)
    
# Función para mostrar la ventana de ayuda con preguntas frecuentes
def mostrar_ayuda():
    global root
    ventana_ayuda = tk.Toplevel(root)
    ventana_ayuda.title("Preguntas Frecuentes")
   
    # Etiquetas con preguntas frecuentes
    tk.Label(ventana_ayuda, text="Medios de Pago", font=('Helvetica', 14, 'bold')).pack(pady=5)
    tk.Label(ventana_ayuda, text="Aceptamos tarjetas de crédito, débito y efectivo.").pack(pady=5)

    tk.Label(ventana_ayuda, text="¿Cómo Reservar?", font=('Helvetica', 14, 'bold')).pack(pady=5)
    tk.Label(ventana_ayuda, text="Seleccione una película, fecha, horario y asiento disponible.").pack(pady=5)

    tk.Label(ventana_ayuda, text="Descuentos", font=('Helvetica', 14, 'bold')).pack(pady=5)
    tk.Label(ventana_ayuda, text="Contamos con descuentos para estudiantes y jubilados.").pack(pady=5)

    # Entrada para mensaje de contacto
    tk.Label(ventana_ayuda, text="Escriba su consulta:", font=('Helvetica', 12)).pack(pady=5)
    consulta_entry = tk.Entry(ventana_ayuda, width=50)
    consulta_entry.pack(pady=10)

    # Botón para enviar el mensaje
    tk.Button(ventana_ayuda, text="Enviar", command=lambda: enviar_consulta(consulta_entry), bg='lightgreen', fg='black').pack(pady=10)

def enviar_consulta(consulta_entry):
    mensaje = consulta_entry.get()
    if mensaje:
        messagebox.showinfo("Consulta Enviada", "Su consulta ha sido enviada.")
    else:
        messagebox.showwarning("Consulta Vacía", "Por favor, escriba su consulta antes de enviarla.")

global nombre, edad, pelicula_seleccionada, fecha_seleccionada, horario_seleccionado, cantidad_entradas, matriz, logo_imagen_tk, cantidad_entradas_inicial, asientos_seleccionados, buscar_entry
nombre, edad, pelicula_seleccionada, fecha_seleccionada, horario_seleccionado, cantidad_entradas, matriz, logo_imagen_tk, cantidad_entradas_inicial, asientos_seleccionados, buscar_entry = None, None, None, None, None, None, None, None, None, [], None

def main():
    global root, logo_imagen_tk
    root = tk.Tk()
    root.title("Proyecto Cine")
    
    try:
        logo_imagen = Image.open("c:/Users/Fede/UADE/Progra1/proyecto_cine/img/logo2.png")
        logo_imagen = logo_imagen.resize((250, 250), Image.LANCZOS)
        logo_imagen_tk = ImageTk.PhotoImage(logo_imagen)
    except FileNotFoundError:
        logo_imagen_tk = None
        messagebox.showerror("Error", "No se pudo cargar la imagen del logo. Asegúrese de que el archivo 'img/logo2.png' existe.")
    except Exception as e:
        logo_imagen_tk = None
        messagebox.showerror("Error", f"Ocurrió un error al cargar la imagen del logo: {e}")
        print(f"No se pudo cargar la imagen del logo: {e}")

    if logo_imagen_tk:
        logo_label = tk.Label(root, image=logo_imagen_tk)
        logo_label.pack(pady=20)
    else:
        tk.Label(root, text="Proyecto Cine", font=('Helvetica', 16, 'bold')).pack(pady=20)

    tk.Button(root, text="Ingresar Datos", command=ingresar_datos, bg='lightblue', fg='black').pack(pady=10)
    tk.Button(root, text="Ayuda", command=mostrar_ayuda, bg='lightgreen', fg='black').pack(pady=10)

    root.mainloop()

# Ejecutar la función principal
if __name__ == "__main__":
    main()
    