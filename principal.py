import archivos
import restaurante as rest
import grupos 
import pedidos
import imagenes

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
                lista_platos.append(plato)

                otro = input("Desea algo mas? (s/n): ").strip().lower()
                if otro != "s":
                    break

        pedidos.registrar_pedido(mesa, lista_platos)
        print(f"Pedido de la mesa {mesa['num_mesa']} anotado: {', '.join(lista_platos)}")

        otra = input("Atendemos otra mesa? (s/n): ").strip().lower()
        if otra != "s":
            return

       

    
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
        else: print("Pendiente")
        pausa()
        
if __name__ == "__main__":
    main()