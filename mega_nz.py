import datetime

import os
import uuid
from mega import Mega


class Mega_nz:

    lista_contenido = []  # Lista de archivos y carpetas
    lista_contenido_cargada = False

    def __init__(self, email, password):
        self.email = email
        self.password = password
        self.mega = Mega()
        try:
            self.mega_cnx = self.mega.login(email, password)
        except Exception as e:
            self.mega_cnx = None
            print(f"Error al iniciar sesión: {e}")

    # Login a cuenta de Mega
    # def mega_login(self):
    #     try:
    #         self.mega_cnx = self.mega.login(self.email, self.password)
    #         return self.mega_cnx
    #     except Exception as e:
    #         return None

    # Función para descargar archivos de Mega, pasando como parámetros el objeto de conexión, el nombre del archivo
    # a descargar, y la ruta donde se guardará el archivo descargado.
    def download_file_name(self, file_name, dest_path):
        file = self.mega_cnx.find(file_name)
        if file:
            dwn = self.mega_cnx.download(file, dest_path)
            return dwn
        else:
            return None


if __name__ == "__main__":
    print(f"Inicio proceso: {datetime.datetime.now().strftime('%H:%M:%S')}")

    email = "municipalidad035@gmail.com"
    password = "Unire035/*-789"

    archivo = "Borrar2.txt"
    carpeta_dest = "/borrar"

    mega = Mega_nz(email, password)
    if not mega:
        print("### Error al iniciar sesión")
        exit()
    else:
        download = mega.download_file_name(archivo, carpeta_dest)
        if download:
            print(f"Archivo descargado: {archivo}")
        else:
            print(f"Error al descargar el archivo: {archivo}")

    print(f"Hora de finalización: {datetime.datetime.now().strftime('%H:%M:%S')}")
