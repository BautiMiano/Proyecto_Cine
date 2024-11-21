# Sistema de Reservación de Entradas para Cine 🎥

Esta es una aplicación web desarrollada en **Python** usando **Flask** para gestionar la reservación de entradas al cine. Los usuarios pueden registrarse, iniciar sesión, elegir películas según su edad, seleccionar asientos y descargar sus entradas en formato PDF.

---

## Características ✨

### Gestión de Usuarios:
- Registro de usuarios con validación de:
  - Nombre (solo letras y espacios).
  - Correo electrónico.
  - Contraseña única.
- Inicio de sesión con validación de credenciales.
- Almacenamiento de datos en un archivo JSON.

### Funciones de Reservación:
- Selección de fecha y horario para las películas.
- Visualización de películas clasificadas según la edad del usuario:
  - Mayores de 18 años: Todas las películas.
  - Menores de 18 años: Solo películas de público general.
- Selección de asientos con visualización de disponibilidad.

### Generación de Entradas:
- Cálculo del precio total según el número de entradas seleccionadas.
- Generación de entradas en formato PDF con detalles de la compra.
- Descarga directa del archivo PDF.

---

## Tecnologías Utilizadas 🛠️

- **Backend**: Python (Flask)
- **Frontend**: HTML, CSS, JavaScript
- **Base de Datos**: Almacenamiento en JSON
- **Generación de PDFs**: Biblioteca `fpdf`
- **Seguridad**: Validación de contraseñas y manejo de sesiones.

---

## Instalación y Configuración ⚙️

### Requisitos Previos:
1. **Python**: Asegúrate de tener instalado Python 3.8 o superior.
2. Instala las bibliotecas necesarias ejecutando:
   ```bash
   pip install Flask werkzeug fpdf

## Pasos de Instalación:

### Clona este repositorio:

git clone <https://github.com/BautiMiano/Proyecto_Cine.git>
cd <Proyecto_Cine>

### Instala las dependencias:

pip install -r requirements.txt

### Ejecuta la aplicación:

python app.py


### Abre tu navegador y ve a:

http://127.0.0.1:5000

## Uso de la Aplicación 🚀

### 1. Registro de Usuario:

Ve a la sección "Crear Usuario".
Completa los datos requeridos:
    Nombre, Edad, Contraseña y Correo Electrónico.

### 2. Iniciar Sesión:

Inicia sesión con tu correo y contraseña registrados.

### 3. Reservar Entradas:

Selecciona:
    Fecha y horario.
    Película (según la edad del usuario).
    Asientos disponibles.
    Confirma el pago.

### 4. Descargar Entradas:

Genera y descarga el archivo PDF con los detalles de tu compra.

## Estructura del Proyecto 📁

.
├── app.py                # Archivo principal de la aplicación
├── templates/            # Archivos HTML para las vistas
│   ├── index.html        # Página de inicio
│   ├── crear_usuario.html # Registro de usuarios
│   ├── iniciar_sesion.html # Inicio de sesión
│   ├── seleccionar_fecha.html # Selección de fechas
│   ├── seleccionar_horario.html # Selección de horarios
│   ├── seleccionar_pelicula.html # Elección de películas
│   ├── seleccionar_asientos.html # Selección de asientos
│   ├── realizar_pago.html # Pago de las entradas
│   └── imprimir_entrada.html # Confirmación y descarga de PDF
├── static/               # Recursos estáticos (imágenes, CSS, JS)
│   ├── img/              # Imágenes de las películas
│   ├── css/              # Archivos CSS
│   └── js/               # Archivos JavaScript
├── usuarios.json         # Archivo para almacenamiento de usuarios
├── temp/                 # Carpeta para archivos temporales (PDFs)
└── README.md             # Documentación del proyecto
└── requirements.txt      # Dependencias del proyecto


