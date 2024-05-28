from datetime import datetime
import os
from dotenv import load_dotenv

# from decouple import config
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base

load_dotenv()
DB_FILE = os.getenv("DB_FILE")
# DB_FILE = config("DB_FILE")

# Configurar conexiones entre SQLAlchemy y SQLite3 DB API
engine = create_engine(f"sqlite:///{DB_FILE}")

Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()
