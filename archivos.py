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

def guardar_restaurante(restaurante):
    datos = { 
        "nombre": restaurante ["nombre"],
        "capacidad": restaurante["capacidad"],
        "mesas_max": restaurante["mesas_max"],
        "menu": restaurante["menu"]
        }
    try: 
        with open(restaurante["ruta_json"], "w", encoding="utf-8")as archivo:
            json.dump(datos, archivo, ensure_ascii=False, indent=4)
        return True
    except OSError:
        print("No se pudo guardar el menú")
        return False
    