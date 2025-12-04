from sqlalchemy import create_engine, MetaData
from dotenv import load_dotenv
import os

# Cargar variables de entorno
load_dotenv()

# Construir URI desde variables de entorno
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')

DB_URI = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

# Crear el engine
engine = create_engine(DB_URI, echo=True)

# Crear objeto de metadata
metadata_obj = MetaData()

# Función para obtener conexión
def get_connection():
    return engine.connect()