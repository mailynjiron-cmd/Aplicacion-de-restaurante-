from archivos import cargar_restaurante
from grupos import cargar_grupos

restaurante = cargar_restaurante("restaurante.json")
restaurante = cargar_grupos(restaurante, "grupos.json")

print(restaurante)