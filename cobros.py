
def mesas_servidas(restaurante):
    resultado = []
    for mesa in restaurante["mesas"]:
        if len(mesa["pedidos"]) > 0:
            resultado.append(mesa)
    return resultado

def calcular_cuenta(restaurante, mesa): 
    total=0
    for plato in mesa["pedidos"]:
        total += restaurante["menu"][plato]
    return total

def cobrar_y_liberar(restaurante, mesa, porcentaje_propina =0): 
    subtotal = calcular_cuenta(restaurante, mesa)
    propina = round(subtotal* porcentaje_propina /100, 2)
    total = subtotal + propina

    restaurante["ganancias"] += total
    restaurante["ocupacion"] -= mesa["clientes"]
    restaurante["mesas"].remove(mesa)
    return subtotal, propina, total