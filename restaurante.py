def crear_restaurante(nombre, capacidad, mesas_max, menu):
    restaurante={
        "nombre": nombre,
        "capacidad": capacidad,
        "mesas_max": mesas_max,
        "menu": menu,
        "mesas": [],
        "ocupacion": 0,
        "ganacias": 0,
        "siguiente_mesa": 1
    }

    return restaurante