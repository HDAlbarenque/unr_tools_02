from db import Base

from sqlalchemy import Column, Integer, String, Float


class Log_tipos(Base):
    __tablename__ = "log_tipos"

    id = Column(Integer, primary_key=True)
    descripcion = Column(String, nullable=False)

    def __init__(self, descripcion):
        self.descripcion = descripcion

    def __repr__(self):
        return f"{self.id} - {self.descripcion}"

    def __str__(self):
        return self.descripcion


class Log_descargas(Base):
    __tablename__ = "log_descargas"

    id = Column(Integer, primary_key=True)
    id_tipo = Column(Integer, nullable=False)
    id_muni = Column(Integer, nullable=False)
    inicio = Column(String, nullable=False)
    fin = Column(String, nullable=False)
    descripcion = Column(Integer, nullable=False)

    def __init__(self, id_muni, id_tipo, inicio, fin, descripcion):
        self.id_muni = id_muni
        self.id_tipo = id_tipo
        self.inicio = inicio
        self.fin = fin
        self.descripcion = descripcion

    def __repr__(self):
        return f"{self.id} - {self.id_muni} - {self.id_tipo} - {self.inicio} - {self.fin} - {self.descripcion}"

    def __str__(self):
        return self.descripcion
