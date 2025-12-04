from sqlalchemy import create_engine, MetaData
from dotenv import load_dotenv
import os


load_dotenv()


DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')

DB_URI = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'


engine = create_engine(DB_URI, echo=True)


metadata_obj = MetaData()


def get_connection():
    return engine.connect()