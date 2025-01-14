import datetime, json, sys
from datetime import date, datetime
from pathlib import Path

from DB.Firebase.Firestore2lista import Firestore2lista

from DB.SQL.db import Base
from DB.SQL.models import Log_descargas
from DB.SQL.log_Mega import log_Mega_ini, log_Mega_fin
import mega_nz as MG
from mega.errors import RequestError


def crea_carpeta_destino(carpeta_padre="\\\\psei\\copia2\\Mega", Carpeta_hija=""):
    ruta_unc = Path(f"{carpeta_padre}\\{Carpeta_hija}")

    try:
        ruta_unc.mkdir(parents=True, exist_ok=False)
    except FileExistsError:
        # print("La carpeta padre ya existe")
        return ruta_unc
    except Exception as e:
        print(f"Error al crear la carpeta: {e}")
        return None
    else:
        # print("La carpeta se ha creado correctamente")
        return ruta_unc


# Procesa la municipalidad
# ========================
def dwnld_muni(file_log, string_fecha, ruta_unc, muni):
    print(
        f"{datetime.now().strftime('%H:%M:%S')} - {muni['muni_nro']} - {muni['muni_nombre']}"
    )

    # Grabo en el archivo de log la fecha y hora de inicio de la muni
    log_id = log_Mega_ini(
        id_muni=muni["muni_nro"],
        id_tipo=1,
        inicio=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        descripcion=muni["muni_nombre"],
    )
    file_log.write(f"   {muni['muni_nro']} - {muni['muni_nombre']}\n")
    file_log.write(f"   - Inicio: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

    # Iniciar sesión en MEGA NZ y obtener contenido de la cuenta
    mega = MG.Mega_nz(muni["Usuario"], muni["Password"])
    if not mega:
        print("### Error al iniciar sesión")
        exit()

    # Trae el contenido de la cuenta de MEGA
    mega.get_account_content(debug_files=False, debug_file=muni["muni_nro"])

    # Carpeta dentro de la cuenta de MEGA
    in_folder = muni["Mega_Carpeta"]

    if produccion:
        # Busca el archivo con la fecha correspondiente, en la carpeta especificada
        dwnld_RAR(file_log, string_fecha, ruta_unc, mega, in_folder)

    # Grabo en el archivo de log la fecha y hora de fin de la muni
    if not log_Mega_fin(
        id_log=log_id, fecha_hora_fin=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ):
        print("### Error al registrar la fecha de fin de la descarga")


# Descarga del archivo RAR de la fecha correspondiente
# ====================================================
def dwnld_RAR(file_log, string_fecha, ruta_unc, mega, in_folder):
    fila_archivo = mega.Account_content.locate_file_in_folder(
        mega, file_pattern=string_fecha, in_folder=in_folder
    )
    if fila_archivo:
        try:
            url = mega.get_url(mega.object_list[fila_archivo]["data4url"])
            dwn = mega.dwnld_url(
                url,
                folder_dest=ruta_unc.as_posix(),
                file_dest=mega.object_list[fila_archivo]["nombre"],
                sobre_escribir=False,
            )
            # Grabo en el archivo de log la fecha y hora de fin de la muni
            file_log.write(
                f"   - Fin   : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
            )
        except RequestError as e:
            print(f"Error al obtener la URL: {e}")
            file_log.write(f"Error al obtener la URL: {e}\n")
        except Exception as e:
            print(f"Se produjo un error inesperado: {e}")
    else:
        file_log.write(f"   - No se encuentra el archivo de la fecha actual\n")
        print((f"         - No se encuentra el archivo de la fecha actual\n"))


if __name__ == "__main__":
    print(f"Inicio proceso: {datetime.now().strftime('%H:%M:%S')}")

    datos_UNIRE = Firestore2lista()

    # Abro archivo de log para agregarle registros
    file_log = open("scratch/log.txt", "a")
    # Grabo en el archivo de log la fecha y hora de inicio del proceso
    file_log.write(
        f"### Inicio proceso: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
    )

    # Determina el día de la semana y, si es domingo, termina el proceso
    nro_dia_semana = date.today().weekday()
    if nro_dia_semana == 6:  # domingo
        sys.exit()

    # Determinar el string de fecha para buscar en el nombre de archivo
    string_fecha = datetime.now().strftime("%Y%m%d")
    # string_fecha = "20240514"

    # Crea carpeta de destino para las descargas, si no puede termina el programa
    ruta_unc = crea_carpeta_destino(Carpeta_hija=f"{string_fecha}")
    if not ruta_unc:
        sys.exit()

    produccion = False
    produccion = True

    for muni in datos_UNIRE:
        # Determinar si tiene usurio y contraseña para descargar archivos desde nube
        if muni["Usuario"] and muni["Password"]:
            # if muni["muni_nro"] == "035":
            #     continue

            dwnld_muni(file_log, string_fecha, ruta_unc, muni)

    # Grabo en el archivo de log la fecha y hora de fin del proceso
    file_log.write(
        f"### Fin de proceso: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
    )
    # Cierro el archivo de log
    file_log.close()

    print(f"Hora de finalización: {datetime.now().strftime('%H:%M:%S')}")
