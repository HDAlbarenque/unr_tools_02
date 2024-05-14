import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base

load_dotenv()
DB_FILE = os.getenv("DB_FILE")

# Configurar conexiones entre SQLAlchemy y SQLite3 DB API
engine = create_engine(f"sqlite:///{DB_FILE}")

Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()


# Función para registrar en el log el inicio de descarga de una municipalidad
def log_inicial(
    id_muni,
    inicio,
    fin,
    descripcion,
    id_tipo=1,
):
    pass
