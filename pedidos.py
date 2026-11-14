def mesas_sin_pedido(restaurante):
    resultado = []
    for mesa in restaurante["mesas"]:
        if len(mesa["pedidos"]) == 0:
            resultado.append(mesa)
    return resultado

def buscar_plato(restaurante, texto):
    texto= texto.strip().lower()
    for plato in restaurante["menu"]:
        if plato.lower() == texto:
            return plato
    return None

def registrar_pedido(mesa, lista_platos):
    mesa["pedidos"]= lista_platos