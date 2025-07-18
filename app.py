# Archivo: app.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from config import Config

# Inicializa la aplicación Flask
app = Flask(__name__)

# Configura la base de datos directamente
app.config['SQLALCHEMY_DATABASE_URI'] = Config.SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = Config.SQLALCHEMY_TRACK_MODIFICATIONS

# Inicializa la instancia de SQLAlchemy
db = SQLAlchemy(app)

# Inicializa la instancia de Bcrypt
bcrypt = Bcrypt(app)

# Importa el archivo de rutas para que los endpoints sean registrados
from routes import * # <--- Agrega esta línea