# Archivo: config.py

import os
from dotenv import load_dotenv

# Carga las variables del archivo .env
load_dotenv()

class Config:
    # Obtiene la URL de la base de datos desde el archivo .env
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False