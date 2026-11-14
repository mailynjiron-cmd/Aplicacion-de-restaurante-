import archivos
import restaurante as rest
import grupos 
import pedidos
import imagenes
import cobros

#         ---------Cargar restaurante----------  
def mostrar_menu():
    print()
    print("=======RESTAURANTE CHIRRIPÓ=======")
    print()    
    azul = "\033[34m"
    blanco = "\033[97m"
    rojo = "\033[31m"
    reset = "\033[0m"

    print(azul + "     ████████████████████")
    print(blanco + "     ████████████████████")
    print(rojo + "     ████████████████████")
    print(rojo + "     ████████████████████")
    print(blanco + "     ████████████████████")
    print(azul + "     ████████████████████" + reset)
    print()
    print("==================================")
    print("1. Abrir el restaurante")
    print("2. Recibir grupos que llegan")
    print("3. Tomar el pedido de una mesa")
    print("4. Cobrar mesa")
    print("5. Añadir un plato a la carta")
    print("6. Consultar estado")
    print("7. Cerrar el restaurante")
    print("==================================")


def pedir_numero(mensaje, minimo, maximo):
    while True:
        texto = input(mensaje)
        try:
            numero = int(texto)
        except ValueError:
            print("Escribe un solo número, por favor.")
            continue
        if minimo <= numero <= maximo:
            return numero
        print(f"Elige un numero del {minimo} al {maximo}.")


def elegir_archivo(carpeta):
    lista = archivos.listar_archivos(carpeta)
    if not lista:
        print(f'Ahora mismo no hay nada pendiente aqui"{carpeta}".')
        return None
    for i, nombre in enumerate(lista, start=1):
        print(f" {i}.{nombre} ")
    eleccion = pedir_numero("¿Cuál atendemos?: ", 1, len(lista))
    return carpeta + "/" + lista[eleccion -1]

def opcion_cargar_restaurante():
    restaurante = archivos.cargar_restaurante("restaurantes/chirripo.json")
    if restaurante is not None:
        print(f'"{restaurante["nombre"]}" Abre sus puertas...')
    return restaurante

#         ---------Grupos----------  

def opciones_cargar_grupo(restaurante):
    print("Grupos esperando en la entrada:")
    ruta = elegir_archivo("mesas")
    if ruta is None:
        return
    resultados = grupos.cargar_grupos(restaurante, ruta)
    if resultados is None:
        print("No se pudo leer la lista de grupos.")
        return
    for clientes, num in resultados:
        if num is None:
            print(f" Lo sentimos, no hay sitio para un grupo de {clientes}.")
        else:
            print(f"Grupo de {clientes} sentado en la mesa {num}.")
    print(f"Personas en el restaurante: {restaurante['ocupacion']} de {restaurante['capacidad']}")

#         ---------Tomar pedido----------  

def mostrar_carta(restaurante):
    print()
    print("Menu:")
    for plato, precio in restaurante["menu"].items():
        print(f"   - {plato}: {precio} € ") 


def elegir_mesa(mesas):
    for mesa in mesas:
         print(f"  Mesa {mesa['num_mesa']} ({mesa['clientes']} personas)")

    numeros =[mesa["num_mesa"] for mesa in mesas]
    while True:
        num = pedir_numero("¿Que mesa atendemos?: ", min(numeros), max(numeros))
        for mesa in mesas:
            if mesa["num_mesa"] == num:
                return mesa
        print("Esa mesa no esta en la lista.")

def opcion_tomar_pedido(restaurante):
    while True:
        mesas = pedidos.mesas_sin_pedido(restaurante)
        if not mesas:
            print("No hay mesas esperando para pedir.") 
            return
        print("Mesas que todavia no han pedido:")
        mesa=elegir_mesa(mesas)
        mostrar_carta(restaurante)  


        lista_platos = []
        for i in range(mesa["clientes"]):
            print()
            print(f"---Cliente {i+1}---")

            while True:
                plato = pedidos.buscar_plato(restaurante, input("¿Que desea tomar?: "))
                while plato is None:
                    print("Lo sentimos, ese plato no esta en el menu.")
                    plato= pedidos.buscar_plato(restaurante, input("¿Que desea tomar?: "))
                    
                ver = input(f"¿Desea ver como es el {plato}? (s/n): ").strip().lower()
                if ver == "s":
                    if not imagenes.mostrar_imagen_plato(plato):
                        print("No tenemos foto de este plato todavia")
                cantidad = pedir_numero(f"Cuantos {plato}?: ", 1, 10)
                for _ in range(cantidad):
                    lista_platos.append(plato)

                otro = input("Desea algo mas? (s/n): ").strip().lower()
                if otro != "s":
                    break

        pedidos.registrar_pedido(mesa, lista_platos)
        print()
        print(f"Pedido de la mesa {mesa['num_mesa']} anotado: {', '.join(lista_platos)}")

        otra = input("Atendemos otra mesa? (s/n): ").strip().lower()
        if otra != "s":
            return

#         ---------Cobros----------  
def opcion_cobrar_mesa(restaurante):
    mesas = cobros.mesas_servidas(restaurante)
    if not mesas:
        print("No hay mesas listas para cobrar.")

    print()
    print("=====Mesas listas para cobrar=====")
    mesa = elegir_mesa(mesas)

#         ---------Cuenta----------
    print()
    print(f"Cuenta de la mesa {mesa['num_mesa']}:")
    for plato in sorted(set(mesa["pedidos"])):
        cantidad = mesa["pedidos"].count(plato)
        precio = restaurante["menu"][plato]
        print(f" {cantidad} x {plato} ({precio} € ) = {cantidad * precio} €")

#         ---------Propina----------
    porcentaje = 0
    if preguntar_si_no("¿Desea dejar propina? (s/n): "):
        porcentaje = pedir_numero("¿Que porcentaje? (por ejemplo 5, 10 o 15): ", 1, 100)

#         ---------Total----------
    subtotal, propina, total = cobros.cobrar_y_liberar(restaurante, mesa, porcentaje)
    print(f"\nSubtotal: {subtotal} €")
    if propina >0:
        print(f"Propina ({porcentaje}%): {propina} €")
    print(f"Total a pagar: {total} €")
    
#         ---------Dividir cuenta----------
    if mesa["clientes"] > 1 and preguntar_si_no("Desean dividir la cuenta? (s/n): "):
        personas = pedir_numero(f"¿Entre cuantas personas? (2-{mesa['clientes']}) ", 2, mesa['clientes'])
        por_persona = round(total/personas, 2)
        print("Cada persona paga: {por_persona} €")
   
    print()
    print(f"Mesa {mesa['num_mesa']} liberada. ¡Gracias por su visita! ¡PURA VIDA!")
    print()
    print(f"Ganacias de la noche: {restaurante['ganancias']} €")

def preguntar_si_no(mensaje):
    while True:
        respuesta= input(mensaje).strip().lower()
        if respuesta in ("s", "si"):
            return True
        if respuesta in ("n", "no"):
            return False
        print("Responde solo con 's' (si) o 'n' (no), por favor.")

def pedir_precio(mensaje):
    while True:
        texto = input(mensaje).replace(",", ".")
        try: 
            precio= float(texto)
        except ValueError: 
            print("Escribe un precio valido, por ejemplo 12 o 0,70")
            continue
        if precio > 0:
            if precio .is_integer():
                return int precio
            return round(precio, 2)
        print("El precio tiene que ser mayor que 0.")

def opcion_ampliar_menu(restaurante):
    nombre = input("Nombre del plato: ").strip()
    if nombre == "": 
        print("El nombre no puede estar vacio.")
        return
    existente = pedidos.buscar_plato(restaurante, nombre)
    if existente is not none:
        print(f"{existente} ya esta en a carta({restaurante['menu'][existente]} €).")
        if not preguntar_si_no("Quieres cambiar su precio? (s/n):"):
            return
        nombre = existente

    precio = pedir_precio("Precio: ")
    rest.anadir_plato(restaurante, nombre, precio)

    if archivos.guardar_restaurante(restaurante):
        print(f"{nombre} guardado en la carta a {precio} €.")
        
    
#         ---------Principal----------  
def pausa():
    input("\nPulsa Enter para volver al menú...")

def main():
    restaurante = None 

    while True:
        mostrar_menu()
        opcion = input("Elige una opción: ").strip()

        if opcion =="1":
            nuevo = opcion_cargar_restaurante()
            if nuevo is not None:
                restaurante = nuevo
        elif opcion == "7":
             print("\n¡Restaurante cerrado! ¡Gracias por tu trabajo!\n")
             print("¡PURA VIDA!\n")
             azul = "\033[34m"
             blanco = "\033[97m"
             rojo = "\033[31m"
             reset = "\033[0m"
             
             print(azul + "████████████████████")
             print(blanco + "████████████████████")
             print(rojo + "████████████████████")
             print(rojo + "████████████████████")
             print(blanco + "████████████████████")
             print(azul + "████████████████████" + reset)
             break
        elif opcion not in ["2", "3", "4", "5", "6"]:
            print("Esta opción no exite")
        elif restaurante is None: 
            print("El restaurante aun esta cerrado. Ábrelo con la opción 1.")
        elif opcion == "2":
            opciones_cargar_grupo(restaurante)
        elif opcion == "3":
            opcion_tomar_pedido(restaurante)
        elif opcion == "4":
            opcion_cobrar_mesa(restaurante)
        elif opcion == "5":
            opcion_ampliar_menu(restaurante)
        else: print("Pendiente")
        pausa()
        
if __name__ == "__main__":
    main()