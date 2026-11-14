import json
import archivos

#         ---------Sentar grupos----------  

def hay_sitio(restaurante, clientes):

    cabe_gente = restaurante["ocupacion"] + clientes <= restaurante["capacidad"]
    cabe_mesa = len(restaurante["mesas"]) < restaurante["mesas_max"]
    return cabe_gente and cabe_mesa

def sentar_grupo(restaurante, clientes): 

    if not hay_sitio(restaurante, clientes):
        return None

    num = restaurante["siguiente_mesa"]
    mesa = {"num_mesa": num, "clientes": clientes, "pedidos": []}

    restaurante["mesas"].append(mesa)
    restaurante["ocupacion"] += clientes
    restaurante["siguiente_mesa"] +=1
    return num


def cargar_grupos(restaurante, ruta_archivo):

    datos = archivos.leer_json(ruta_archivo)
    if datos is None or not isinstance(datos, list):
        return None

    resultados = []
    for grupo in datos:
        if isinstance(grupo, dict) and isinstance(grupo.get("clientes"), int) and grupo["clientes"] > 0:
            num = sentar_grupo(restaurante, grupo["clientes"])
            resultados.append((grupo["clientes"], num))
    return resultados 



    