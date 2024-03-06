from icecream import ic
from mega import Mega
import json


email = "municipalidad035@gmail.com"
password = "Unire035/*-789"

mega = Mega()

# login
mega_cnx = mega.login(email, password)


class account_content:

    def __init__(self, mega_cnx):
        self.mega_cnx = mega_cnx

    def get_account_content(self):
        # get account files
        files = self.mega_cnx.get_files()
        # Grabo la lista de archivos construida en archivo JSON
        # with open("scratch/lista_files.json", "w") as f:
        #     json.dump(files, f, indent=4)

        object_list = []
        for file in files:
            id_file = files[file]["h"]

            id_parent = files[file]["p"]
            id_parent = (
                id_parent if id_parent else None
            )  # Si no tiene padre, le pongo None

            tipo = files[file]["t"]
            nombre = files[file]["a"]["n"]
            data_get_link = (id_file, files[file])

            object_list.append(
                {
                    "id_file": id_file,
                    "id_parent": id_parent,
                    "tipo": tipo,
                    "nombre": nombre,
                    "ruta": None,
                    "data_get_link": data_get_link,
                }
            )

        return object_list

    # Función para buscar el padre de un item (todo con la lista)
    def find_ruta(self, lista, id_parent):
        if id_parent:
            for fila in lista:
                if fila["id_file"] == id_parent:
                    # Si la fila no tiene padre, retorno el valor encontrado
                    if not fila["id_parent"]:
                        return f'\{fila["nombre"]}'
                    # Si la fila tiene padre, busco el padre del padre
                    else:
                        ruta_padre = self.find_ruta(lista, fila["id_parent"])
                        return ruta_padre + f'\{fila["nombre"]}'
            # Si no encuentra Padre, retorna None
            return ""
        else:
            return ""

    # Función para agregar a cada elemento de la lista el nombre del padre encontrado
    def agregar_ruta(self, lista):
        for indice, fila in enumerate(lista):
            padre = self.find_ruta(lista, fila["id_parent"])
            fila["ruta"] = padre
        return lista


ic()

oContenido = account_content(mega_cnx=mega_cnx)
lista_arch = oContenido.get_account_content()
lista_con_ruta = oContenido.agregar_ruta(lista_arch)

# Grabo la lista de archivos construida en archivo de texto
with open("scratch/lista_files.csv", "w") as f:
    for file in lista_arch:
        f.write(
            f"{file['tipo']};{file['nombre']};{file['id_file']};{file['id_parent']};{file['ruta']}\n"
        )
        pass
print(lista_arch[5]["nombre"])
