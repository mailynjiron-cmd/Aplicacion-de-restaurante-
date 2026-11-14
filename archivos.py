import json
import os

from restaurante import crear_restaurante

def listar_archivos(carpeta):
    if not os.path.isdir(carpeta):
        return[]
    archivos =[]
    for nombre in os.listdir(carpeta):
        if nombre.endswith(".json"):
            archivos.append(nombre)
    return sorted(archivos)


def leer_json(ruta_archivo):
    try:
        with open(ruta_archivo, "r", encoding="utf-8") as archivo:
            return json.load(archivo)
    except FileNotFoundError:
        print("No se encuentra el archivo:", ruta_archivo)
    except json.JSONDecodeError:
        print("El archivo no tiene un JSON valicación", ruta_archivo)
    return None


def cargar_restaurante(ruta_archivo):
    datos= leer_json(ruta_archivo)
    if datos is None:
        return None

    try:
        restaurante= crear_restaurante(
            datos["nombre"],
            datos["capacidad"],
            datos["mesas_max"],
            datos["menu"]
    )

    except (KeyError, TypeError):
        print("Al JSON del restaurante le faltan campos(nombre, capacidad, meas_max, menu).")
        return None 

    restaurante["ruta_json"] = ruta_archivo #me ayuda a saber donde guarde el menu 
    return restaurante