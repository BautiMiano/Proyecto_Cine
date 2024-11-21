from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import check_password_hash
import json
from datetime import datetime
import random
from flask import send_file
from fpdf import FPDF
import os
import re
import pytest

def es_nombre_valido(nombre):
    patron = r'^[a-zA-Z\s]+$'
    return bool(re.match(patron, nombre))

def es_correo_valido(mail):
    patron = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return bool(re.match(patron, mail))



# Test para la función es_nombre_valido
def test_es_nombre_valido():
    assert es_nombre_valido("Juan Perez") == True  # Nombre válido
    assert es_nombre_valido("Juan123") == False  # Nombre con números, no válido
    assert es_nombre_valido("Juan_Perez") == False  # Nombre con guión bajo, no válido
    assert es_nombre_valido("Juan Pérez") == True  # Nombre con espacio válido

# Test para la función es_correo_valido
def test_es_correo_valido():
    assert es_correo_valido("juan.perez@mail.com") == True  # Correo válido
    assert es_correo_valido("juan.perez.com") == False  # Correo sin @, no válido
    assert es_correo_valido("juan@perez") == False  # Correo sin dominio, no válido
    assert es_correo_valido("juan@perez.com") == True  # Correo válido

if __name__ == "__main__":
    # Solo ejecuta los tests si se corre este archivo directamente
    pytest.main()