from flask import Flask, render_template, request, redirect, url_for, flash
from datetime import datetime
import random
from flask import send_file
from fpdf import FPDF
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Variables globales
peliculas_adultos = ["Venom El Ultimo Baile", "Terrifier 3 El Payaso Siniestro", "Sonrie 2"]
peliculas_todo_publico = ["Robot Salvaje", "La Leyenda Del Dragon"]
asientos_ocupados = 30                      
PRECIO_ENTRADA = 8000

# Inicializar asientos
def inicializar_asientos(filas, columnas):
    return [["O" for _ in range(columnas)] for _ in range(filas)]

def ocupar_asientos_aleatoriamente(matriz, num_asientos_ocupados): 
    filas = len(matriz)
    columnas = len(matriz[0])
    asientos_disponibles = [(fila, col) for fila in range(filas) for col in range(columnas)]
    asientos_ocupados = random.sample(asientos_disponibles, num_asientos_ocupados)
    for fila, col in asientos_ocupados:
        matriz[fila][col] = "X"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ingresar_datos', methods=['POST'])
def ingresar_datos():
    nombre = request.form['nombre']
    edad = request.form['edad']
    contraseña = request.form['contraseña']
    if not nombre or not edad or not contraseña:
        flash('Por favor, complete todos los campos.')
        return redirect(url_for('index'))
    
    return redirect(url_for('seleccionar_fecha', nombre=nombre, edad=edad))

@app.route('/crear_usuario', methods=['GET', 'POST'])
def crear_usuario():
    if request.method == 'POST':
        # Aquí debes procesar el formulario de creación de usuario
        nombre = request.form['nombre']
        edad = request.form['edad']
        contraseña = request.form['contraseña']
        mail = request.form['mail']
        
        # Aquí puedes guardar los datos del nuevo usuario en el archivo JSON
        # Llamar la función que tú o tu compañero usarán para guardar el usuario (por ejemplo)
        
        flash('¡Usuario creado exitosamente!')
        return redirect(url_for('index'))  # Redirigir al inicio después de crear el usuario

    return render_template('crear_usuario.html')  # Aquí debes renderizar el formulario para crear un usuario

@app.route('/seleccionar_fecha')
def seleccionar_fecha():
    nombre = request.args.get('nombre')
    edad = request.args.get('edad')
    return render_template('seleccionar_fecha.html', nombre=nombre, edad=edad)

@app.route('/confirmar_fecha', methods=['POST'])
def confirmar_fecha():
    fecha_str = request.form['fecha']
    nombre = request.form['nombre']
    edad = request.form['edad']
    fecha_seleccionada = datetime.strptime(fecha_str, "%Y-%m-%d").date()
    return redirect(url_for('seleccionar_horario', nombre=nombre, edad=edad, fecha=fecha_seleccionada))

@app.route('/seleccionar_horario')
def seleccionar_horario():
    nombre = request.args.get('nombre')
    edad = request.args.get('edad')
    fecha = request.args.get('fecha')
    return render_template('seleccionar_horario.html', nombre=nombre, edad=edad, fecha=fecha)

@app.route('/seleccionar_pelicula', methods=['POST'])
def seleccionar_pelicula():
    nombre = request.form['nombre']
    edad = int(request.form['edad'])
    fecha = request.form['fecha']
    
    if edad >= 18:
        peliculas = peliculas_adultos  # Películas para adultos
    else:
        peliculas = peliculas_todo_publico
    
    peliculas_con_imagenes = [
        {'nombre': 'Venom El Ultimo Baile', 'imagen': 'static/img/venom.jpg'},
        {'nombre': 'Terrifier 3 El Payaso Siniestro', 'imagen': 'static/img/terrifier-3.jpg'},
        {'nombre': 'Sonrie 2', 'imagen': 'static/img/sonrie2.jpg'},
        {'nombre': 'Robot Salvaje', 'imagen': 'static/img/robot-salvaje.jpg'},
        {'nombre': 'La Leyenda Del Dragon', 'imagen': 'static/img/la-leyenda-del-dragon.jpg'}
    ]
    peliculas_a_mostrar = [pelicula for pelicula in peliculas_con_imagenes if pelicula['nombre'] in peliculas]
    return render_template('seleccionar_pelicula.html', nombre=nombre, edad=edad, fecha=fecha, peliculas=peliculas_a_mostrar)

@app.route('/confirmar_pelicula', methods=['POST'])
def confirmar_pelicula():
    nombre = request.form['nombre']
    edad = request.form['edad']
    fecha = request.form['fecha']
    pelicula_seleccionada = request.form['pelicula']
    return redirect(url_for('seleccionar_asientos', nombre=nombre, edad=edad, fecha=fecha, pelicula=pelicula_seleccionada))

@app.route('/seleccionar_asientos', methods=['GET', 'POST'])
def seleccionar_asientos():
    nombre = request.args.get('nombre')
    edad = request.args.get('edad')
    fecha = request.args.get('fecha')
    pelicula = request.args.get('pelicula')

    # Inicializar asientos
    filas, columnas = 16, 14
    matriz = inicializar_asientos(filas, columnas)
    ocupar_asientos_aleatoriamente(matriz, asientos_ocupados)

    if request.method == 'POST':
        # Procesar asientos seleccionados
        asientos_seleccionados = request.form.getlist('asientos')  # Recibir lista de asientos seleccionados
        # Aquí podrías hacer algo con los asientos seleccionados, como validarlos o almacenarlos

        # Por ejemplo, si quieres guardarlos en la sesión o pasarlos a la siguiente etapa
        return redirect(url_for('realizar_pago', 
                                nombre=nombre, 
                                edad=edad, 
                                fecha=fecha, 
                                pelicula=pelicula, 
                                asientos_seleccionados=",".join(asientos_seleccionados)))

    return render_template('seleccionar_asientos.html', nombre=nombre, edad=edad, fecha=fecha, pelicula=pelicula, matriz=matriz)

@app.route('/realizar_pago', methods=['POST'])
def realizar_pago():
    # Recoger datos del formulario
    nombre = request.form['nombre']
    edad = request.form['edad']
    fecha = request.form['fecha']
    pelicula = request.form['pelicula']
    cantidad_entradas = int(request.form['cantidad_entradas'])

    # Obtener y procesar asientos seleccionados
    asientos_seleccionados = request.form.get('asientos_seleccionados', '')
    asientos_lista = asientos_seleccionados.split(',') if asientos_seleccionados else []

    # Validar cantidad de asientos seleccionados
    if len(asientos_lista) != cantidad_entradas:
        flash(f"Debes seleccionar exactamente {cantidad_entradas} asientos.")
        return redirect(
            url_for(
                'seleccionar_asientos',
                nombre=nombre,
                edad=edad,
                fecha=fecha,
                pelicula=pelicula,
                cantidad_entradas=cantidad_entradas
            )
        ) 

    # Calcular el total a pagar
    total = cantidad_entradas * PRECIO_ENTRADA

    # Renderizar la página de pago
    return render_template(
        'realizar_pago.html',
        nombre=nombre,
        edad=edad,
        fecha=fecha,
        pelicula=pelicula,
        cantidad_entradas=cantidad_entradas,
        total=total,
        asientos=asientos_lista
    )

@app.route('/confirmar_pago', methods=['POST'])
def confirmar_pago():
    # Verificar qué datos llegan
    print(request.form)  # Esto te ayudará a depurar el contenido del formulario
    
    try:
        nombre = request.form['nombre']
        edad = request.form['edad']
        pelicula = request.form['pelicula']
        fecha = request.form['fecha']
        cantidad_entradas = request.form['cantidad_entradas']
        total = request.form['total']
        metodo_pago = request.form['tipo_pago']
    except KeyError as e:
        flash(f"Error al procesar el formulario: {str(e)}")
        return redirect(url_for('realizar_pago'))  # Redirigir si hay un error

    # Redirigir a la página de impresión de entradas
    return redirect(url_for('imprimir_entrada', 
                            nombre=nombre, 
                            edad=edad, 
                            pelicula=pelicula, 
                            fecha=fecha, 
                            cantidad_entradas=cantidad_entradas, 
                            total=total))


@app.route('/imprimir_entrada')
def imprimir_entrada():
    # Obtener los parámetros de la URL
    nombre = request.args.get('nombre')
    edad = request.args.get('edad')
    pelicula = request.args.get('pelicula')
    fecha = request.args.get('fecha')
    cantidad_entradas = request.args.get('cantidad_entradas')
    total = request.args.get('total')

    # Asegúrate de que los valores estén disponibles
    if not all([nombre, edad, pelicula, fecha, cantidad_entradas, total]):
        return "Error: Datos incompletos", 400  # Puedes mostrar un mensaje de error si falta algún parámetro.

    # Renderizar la plantilla de impresión de entrada
    return render_template('imprimir_entrada.html',
                           nombre=nombre,
                           edad=edad,
                           pelicula=pelicula,
                           fecha=fecha,
                           cantidad_entradas=cantidad_entradas,
                           total=total)

def generate_pdf(nombre, edad, pelicula, fecha, cantidad_entradas, total):
    pdf = FPDF()
    pdf.add_page()

    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=f"Nombre: {nombre}", ln=True)
    pdf.cell(200, 10, txt=f"Edad: {edad}", ln=True)
    pdf.cell(200, 10, txt=f"Pelicula: {pelicula}", ln=True)
    pdf.cell(200, 10, txt=f"Fecha: {fecha}", ln=True)
    pdf.cell(200, 10, txt=f"Cantidad de Entradas: {cantidad_entradas}", ln=True)
    pdf.cell(200, 10, txt=f"Total: ${total}", ln=True)

    # Usar una ruta temporal válida para Windows
    output_dir = os.path.join(os.getcwd(), 'temp')  # Crear carpeta 'temp' en el directorio actual
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "entrada.pdf")

    pdf.output(output_path)

    return output_path

@app.route('/descargar_pdf', methods=['POST'])
def descargar_pdf():
    nombre = request.form['nombre']
    edad = request.form['edad']
    pelicula = request.form['pelicula']
    fecha = request.form['fecha']
    cantidad_entradas = request.form['cantidad_entradas']
    total = request.form['total']

    # Generación del PDF
    pdf_file = generate_pdf(nombre, edad, pelicula, fecha, cantidad_entradas, total)

    # Enviar el archivo PDF generado al usuario para que lo descargue
    return send_file(pdf_file, as_attachment=True, download_name="entrada.pdf")


if __name__ == '__main__':
    app.run(debug=True) 

#s