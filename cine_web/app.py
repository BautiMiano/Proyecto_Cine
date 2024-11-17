from flask import Flask, render_template, request, redirect, url_for, flash
from datetime import datetime
import random
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

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
    if not nombre or not edad:
        flash('Por favor, complete todos los campos.')
        return redirect(url_for('index'))
    
    return redirect(url_for('seleccionar_fecha', nombre=nombre, edad=edad))

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
    peliculas = peliculas_adultos + peliculas_todo_publico if edad >= 18 else peliculas_todo_publico
    return render_template('seleccionar_pelicula.html', nombre=nombre, edad=edad, fecha=fecha, peliculas=peliculas)

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

from flask import request, flash, redirect, url_for, render_template

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
    # Recoger datos enviados por el formulario de pago
    nombre = request.form['nombre']
    edad = request.form['edad']
    pelicula = request.form['pelicula']
    fecha = request.form['fecha']
    cantidad_entradas = request.form['cantidad_entradas']
    total = request.form['total']
    metodo_pago = request.form['tipo_pago']  # Recoger el método de pago

    # Aquí puedes añadir lógica de procesamiento del pago, como integrar un sistema de pago
    # Por ahora, asumimos que el pago es exitoso

    flash('¡Pago realizado con éxito!')

    # Redirigir a la página para imprimir la entrada o confirmación
    return redirect(
        url_for(
            'imprimir_entrada',
            nombre=nombre,
            edad=edad,
            pelicula=pelicula,
            fecha=fecha,
            cantidad_entradas=cantidad_entradas,
            total=total
        )
    )

@app.route('/imprimir_entrada', methods=['GET', 'POST'])
def imprimir_entrada():
    # Si la solicitud es GET, tomamos los parámetros de la URL
    if request.method == 'GET':
        nombre = request.args.get('nombre')
        edad = request.args.get('edad')
        pelicula = request.args.get('pelicula')
        fecha = request.args.get('fecha')
        cantidad_entradas = request.args.get('cantidad_entradas')
        total = request.args.get('total')
    # Si la solicitud es POST, tomamos los datos del formulario
    else:
        nombre = request.form['nombre']
        edad = request.form['edad']
        pelicula = request.form['pelicula']
        fecha = request.form['fecha']
        cantidad_entradas = request.form['cantidad_entradas']
        total = request.form['total']

        # Lógica para generar el PDF si es necesario
        if nombre and edad and pelicula and fecha and cantidad_entradas and total:
            # Crear el PDF, si quieres guardar la entrada como PDF
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            pdf.cell(200, 10, txt="Entrada de Cine", ln=True, align='C')
            pdf.ln(10)
            pdf.cell(200, 10, txt=f"Nombre: {nombre}", ln=True)
            pdf.cell(200, 10, txt=f"Edad: {edad}", ln=True)
            pdf.cell(200, 10, txt=f"Película: {pelicula}", ln=True)
            pdf.cell(200, 10, txt=f"Fecha: {fecha}", ln=True)
            pdf.cell(200, 10, txt=f"Cantidad de Entradas: {cantidad_entradas}", ln=True)
            pdf.cell(200, 10, txt=f"Total: ${total}", ln=True)

            # Guardar el archivo PDF
            pdf_output = f"{nombre}_entrada.pdf"
            pdf.output(pdf_output)

            # Puedes retornar el archivo PDF como descarga o mostrar un mensaje
            flash('¡Tu entrada ha sido descargada exitosamente!', 'success')
            return redirect(url_for('imprimir_entrada', nombre=nombre, edad=edad, pelicula=pelicula, fecha=fecha, cantidad_entradas=cantidad_entradas, total=total))

    # Renderizar la página de impresión
    return render_template(
        'imprimir_entrada.html',
        nombre=nombre,
        edad=edad,
        pelicula=pelicula,
        fecha=fecha,
        cantidad_entradas=cantidad_entradas,
        total=total
    )
if __name__ == '__main__':
    app.run(debug=True)
