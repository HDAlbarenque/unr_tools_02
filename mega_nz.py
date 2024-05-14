import datetime

import os, json
import uuid
from mega import Mega
from icecream import ic


class Mega_nz:

    object_list = []  # Lista de archivos y carpetas

    def __init__(self, email, password):
        """
        Inicializa una nueva instancia de la clase 'Mega_NZ`.

        Args:
            email (str): The email address used for authentication.
            password (str): The password used for authentication.

        Initializes the following instance variables:
            - email (str): The email address used for authentication.
            - password (str): The password used for authentication.
            - object_list (list): An empty list to store files and folders.
            - mega (Mega): An instance of the `Mega` class.
            - mega_cnx (Mega): An instance of the `Mega` class after successful login.
                If login fails, it is set to `None`.

        Prints an error message if login fails.
        """
        self.email = email
        self.password = password
        self.object_list = []  # Lista de archivos y carpetas
        self.mega = Mega()
        try:
            self.mega_cnx = self.mega.login(email, password)
        except Exception as e:
            self.mega_cnx = None
            print(f"Error al iniciar sesión: {e}")

    # Función que descarga un archivo desde la URL obtenida con get_link()
    def dwnld_url(self, url, folder_dest, file_dest=None, sobre_escribir=False):
        """
        Descarga un archivo de la URL dada y lo guarda al destino de la carpeta especificado.

        Parameters:
            url (str): The URL of the file to be downloaded.
            folder_dest (str): The destination folder where the downloaded file will be saved.

        Returns:
            Resultado de la descarga
        """
        if (
            os.path.isfile(folder_dest + "/" + file_dest) and not sobre_escribir
        ):  # Si el archivo ya existe, no lo descargo
            return None
        else:  # Aquí se produjo el error
            return self.mega_cnx.download_url(
                url, dest_path=folder_dest, dest_filename=file_dest
            )

    # Función que devuelve la URL de descarga
    def get_url(self, data4url):
        """
        Obtiene la URL desde los datos de un archivo de archivo determinado.

        Parameters:
            file_data4url (str): The file data to get the link for.

        Returns:
            str: The URL link for the given file data.
        """
        return self.mega_cnx.get_link(data4url)

    def download_filename(self, file_name, dest_path):
        """
        Descarga un archivo de la cuenta Mega, a partir de su nombre, y lo guarda en la ruta de destino especificada.

        Parameters:
            file_name (str): The name of the file to download.
            dest_path (str): The path where the downloaded file will be saved.

        Returns:
            str or None: The result of the download if successful, or None if the file was not found.
        """
        file = self.mega_cnx.find(file_name)
        if file:
            dwn = self.mega_cnx.download(file, dest_path)
            return dwn
        else:
            return None

    def get_account_content(self, debug_files=False, debug_file="lista_files"):
        """
        Recupera el contenido de la cuenta Mega.

        Args:
            debug_files (bool, optional): Whether to generate debug files. Defaults to False.
            debug_file (str, optional): The name of the debug file. Defaults to "lista_files".

        Returns:
            list: A list containing the content of the user's Mega account.
        """
        oContenido = self.Account_content(mega_cnx=self.mega_cnx)
        self.object_list = oContenido.object_list

        # Genero archivos de debug si se indica en parámetro debug_files = True.
        if debug_files:
            self.genera_debug_files(debug_file)

        return self.object_list

    def genera_debug_files(self, debug_file):
        """
        Genera archivos de depuración en formatos CSV y JSON basados en la lista de objetos.

        Args:
            debug_file (str): The name of the debug file to be generated.

        Returns:
            None
        """
        # Grabo la lista de archivos construida en archivo de texto
        with open(f"scratch/{debug_file}.csv", "w") as f:
            for objeto in self.object_list:
                f.write(
                    f"{objeto['tipo']};{objeto['nombre']};{objeto['id_file']};{objeto['id_parent']};{objeto['ruta']}\n"
                )
        # Grabo la lista de archivos construida en archivo JSON
        with open(f"scratch/{debug_file}.json", "w") as f:
            json.dump(self.object_list, f, indent=4)

    class Account_content:

        object_list = []

        def __init__(self, mega_cnx):
            self.object_list = []
            self.mega_cnx = mega_cnx
            self.get_account_content()
            self.agregar_ruta()

        # Carga el contenido de la cuenta en la lista object_list
        def get_account_content(self):
            """
            Recupera el contenido de la cuenta Mega.

            This function retrieves the files and folders in the user's Mega account
            and stores the information in the `object_list` attribute of the class.

            Returns:
                None
            """
            # get account files
            files = self.mega_cnx.get_files()
            # Grabo la lista de archivos construida en archivo JSON
            with open("scratch/content.json", "w") as f:
                json.dump(files, f, indent=4)

            for file in files:
                id_file = files[file]["h"]

                id_parent = files[file]["p"]
                id_parent = (
                    id_parent if id_parent else None
                )  # Si no tiene padre, le pongo None

                tipo = files[file]["t"]
                nombre = files[file]["a"]["n"]
                data4url = (id_file, files[file])

                self.object_list.append(
                    {
                        "id_file": id_file,
                        "id_parent": id_parent,
                        "tipo": tipo,
                        "nombre": nombre,
                        "ruta": None,
                        "data4url": data4url,
                    }
                )

            # return self.object_list

        # Función para buscar el padre de un item (todo con la lista)
        def find_ruta(self, lista, id_parent):
            """
            Encuentre la ruta de un archivo en una lista dada basada en su ID de padre.

            Parameters:
                lista (list): The list of dictionaries containing file information.
                id_parent (str): The ID of the parent file.

            Returns:
                str: The path of the file found, including its name.
                    If the parent file is not found, returns an empty string.
            """
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
        def agregar_ruta(self):
            """
            Agrega un campo "RUTA" a cada elemento en el Object_List, que contiene el nombre de la
            carpeta principal que se encuentra en función del campo "ID_PARENT".

            Parameters:
                self (object): The object instance.

            Returns:
                None
            """
            for indice, fila in enumerate(self.object_list):
                padre = self.find_ruta(self.object_list, fila["id_parent"])
                fila["ruta"] = padre

        # Función que devuelve en que posición de la lista está un archivo con una ruta determinada
        def locate_file_in_folder(self, file_pattern, in_folder):
            """
            Localiza un archivo en una carpeta basado en un patrón de archivo y la ruta de la carpeta.

            Args:
                file_pattern (str): The pattern to match against the file name.
                in_folder (str): The path of the folder to search in.

            Returns:
                int or None: The index of the file in the object list if found,
                            None otherwise.
            """
            # Busca primero el archivo en la carpeta determinada
            for indice, fila in enumerate(self.object_list):
                if fila["ruta"] == in_folder and (
                    fila["nombre"].find(file_pattern) > -1
                ):
                    return indice

            # Si no encuentra archivo en carpeta, intenta localizarlo en cualquier carpeta
            for indice, fila in enumerate(self.object_list):
                if fila["nombre"].find(file_pattern) > -1:
                    return indice

            # Si no encuentra archivo en la carpeta determinada, ni en cualquier otra carpeta...
            return None


if __name__ == "__main__":
    print(f"Inicio proceso: {datetime.datetime.now().strftime('%H:%M:%S')}")

    email = "municipalidad234@gmail.com"
    password = "234/*-789"

    mega = Mega_nz(email, password)
    if not mega:
        print("### Error al iniciar sesión")
        exit()

    mega.get_account_content(debug_files=True)

    string_fecha = datetime.datetime.now().strftime("%Y%m%d")
    in_folder = r"\Cloud Drive\MEGAsync"
    row_number = mega.Account_content.locate_file_in_folder(
        mega, file_pattern=string_fecha, in_folder=in_folder
    )
    link = mega.get_url(data4url=mega.object_list[row_number]["data4url"])
    dwn = mega.dwnld_url(
        link,
        folder_dest="/borrar",
        file_dest=mega.object_list[row_number]["nombre"],
        sobre_escribir=False,
    )

    # lista_objetos = mega.object_list

    print(f"Hora de finalización: {datetime.datetime.now().strftime('%H:%M:%S')}")
