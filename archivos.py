import json

from restaurante import crear_restaurante

def cargar_restaurante(ruta_archivo):
    with open (ruta_archivo,"r", encoding="utf-8") as archivo:
        datos= json.load(archivo)

    restaurante= crear_restaurante(
        datos["nombre"],
        datos["capacidad"],
        datos["mesas_max"],
        datos["menu"]
    )

    return restaurante