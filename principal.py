import archivos
import restaurante as rest
import grupos 

#from PIL import Image

def mostrar_menu():
    print()
    print("=====RESTAURANTE CHIRRIPÓ=====")
    print('\n  ¡Abre sus puertas...!\n')
    azul = "\033[34m"
    blanco = "\033[97m"
    rojo = "\033[31m"
    reset = "\033[0m"

    print(azul + "   ████████████████████")
    print(blanco + "   ████████████████████")
    print(rojo + "   ████████████████████")
    print(rojo + "   ████████████████████")
    print(blanco + "   ████████████████████")
    print(azul + "   ████████████████████" + reset)
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


    
#         ---------Principal----------  
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
             print("\n¡Gracias por preferirnos!\n")
             print("     ¡PURA VIDA!\n")
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
        else: print("Pendiente")

if __name__ == "__main__":
    main()