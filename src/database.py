# database.py
from flask_sqlalchemy import SQLAlchemy
import os

# Instancia de SQLAlchemy vacía por ahora.
db = SQLAlchemy()

# Ruta para la carpeta 'data' (relativa al directorio de este fichero)
DATA_DIR = "instance"
DB_FILE_NAME = "cocina.db"
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), DATA_DIR, DB_FILE_NAME)
