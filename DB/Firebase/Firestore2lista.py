import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore


# Función para recuperar la lista de URLs desde Firestore
def Firestore2lista():
    if not firebase_admin._apps:
        cred = credentials.Certificate("DB/Firebase/fb_unire.json")
        firebase_admin.initialize_app(cred)

    db = firestore.client()

    # Traer el campo 'URLs', del documento ' municipalidades', de la colección 'UNIRE'
    muni_filas = (
        db.collection("Datos_Munis")
        .document("Mega_metadatos")
        .get()
        .get("Datos_Backup")
    )

    if muni_filas:
        return muni_filas


if __name__ == "__main__":
    lista = Firestore2lista()
    pass
