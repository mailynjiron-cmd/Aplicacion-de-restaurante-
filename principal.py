
import archivos
import restaurante as rest

from PIL import Image

def mostrar_menu():
    print()
    print("=====GESTION DE RESTAURANTE=====")
    print("1. Cargar restaurante")
    print("2. Cargar nuevas peticiones de grupos")
    print("3. Tomar pedido")
    print("4. Cobrar y liberar una mesa")
    print("5. Ampliar el menu")
    print("6. Consultar estado")
    print("7. Salir")
    print("==================================")


def pedir_numero(mensaje, minimo, maximo):
    while True:
        texto = input(mensaje)
        try:
            numero = int(texto)
        except ValueError:
            print("Eso no es un numero entero.")
            continue
        if minimo <= numero <= maximo:
            return numero
        print(f"Debe de estar entre {minimo} y {maximo}.")


def elergir_archivo(carpeta):
    lista = archivos.listar_archivos(carpeta)
    if not lista:
        print(f'No hay archivos .json en la carpeta"{carpeta}".')
        return None
    for i, nombre in enumerate(lista, start=1):
        print(f" {i}.{nombre} ")
    eleccion = pedir_numero("Elige un archivo: ", 1, len(lista))
    return carpeta + "/" + lista[eleccion -1]

def opcion_cargar_restaurante():
    restaurante = archivos.cargar_restaurante("restaurantes/chirripo.json")
    if restaurante is not None:
        print(f'"{restaurante["nombre"]}" cargando...')
    return restaurante


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
        #elif opcion == "7":
           # if restaurante is not None:
           # archivos.guardar_restaurante(restaurante)
          #  print("¡Gracias por preferirnos! PURA VIDA", "")

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
            print("Opción no valida")
        elif restaurante is None: 
            print("Primero tienes que cargar el restaurante(opción 1).")
        else: print("Pendiente")

if __name__ == "__main__":
    main()