import json

def cargar_grupos(restaurante, ruta_archivo):

    archivo = open(ruta_archivo, "r", encoding="utf-8")
    grupos = json.load(archivo)
    archivo.close()

    for grupo in grupos:

        clientes = grupo["clientes"]

        num_mesas = len(restaurante["mesas"]) + 1

        if (restaurante["ocupacion"]+ clientes <= restaurante["capacidad"]
            and len(restaurante["mesas"]) < restaurante["mesas_max"]):

            nueva_mesa = {
                "num_mesa": num_mesas,
                "clientes": clientes,
                "atendida": False
            }

            restaurante["mesas"].append(nueva_mesa)
            restaurante["ocupacion"] += clientes

            print("Grupo sentado en la mesa:", num_mesas)

        else:
            print("No hay espacio para un grupo de:", clientes, "clientes.")
    return restaurante        