from db import *
from models import Log_descargas, Log_tipos


# Función que, si la tabla 'log_tipos' está vacía, le inserta tres registros de diferentes estados
def insertar_log_tipos():
    if not session.query(Log_tipos).first():
        # session.add(Log_tipos("Alimento"))
        x = session.add_all(
            [Log_tipos("Información"), Log_tipos("Advertencia"), Log_tipos("Error")]
        )
        session.commit()


if __name__ == "__main__":
    Base.metadata.create_all(engine)
    insertar_log_tipos()
    print("Base de datos creada con exito!\n")
