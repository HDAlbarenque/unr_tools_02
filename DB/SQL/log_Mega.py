from .db import session
from .models import Log_descargas


def log_Mega_ini(id_muni, id_tipo, inicio, descripcion):
    """
    Función para registrar en la base de datos de log diferentes eventos relacionados
    con la descarga de archivos

    Parameters:
        id_muni: Id de la municipalidad
        id_tipo: Id del tipo de descarga (1, 2 o 3)
        inicio: Fecha y hora de inicio de la descarga
        descripcion

    Return: Id del registro insertado si todo sale bien o None si algo sale mal
    """

    try:
        log = Log_descargas(
            id_muni=id_muni,
            id_tipo=id_tipo,
            inicio=inicio,
            fin="",
            descripcion=descripcion,
        )
        session.add(log)
        session.commit()
        return log.id

    except Exception as e:
        print(f"Error al registrar el log: {e}")


def log_Mega_fin(id_log, fecha_hora_fin):
    """
    Función para registrar en la base de datos de log la fecha y hora de fin de la descarga
    de un archivo

    Parameters:
        id_log: Id del registro de inicio de la descarga
        fecha_hora_fin: Fecha y hora de fin de la descarga

    Return: True si todo sale bien o False si algo sale mal
    """

    try:
        session.query(Log_descargas).filter(Log_descargas.id == id_log).update(
            {Log_descargas.fin: fecha_hora_fin}
        )
        session.commit()
        return True

    except Exception as e:
        print(f"Error al registrar el log: {e}")
        return False
