import os
import subprocess



def ruta_imagen(nombre_plato):
    buscado= nombre_plato.lower().replace(" ","").replace("_", "")
    if not os.path.isdir("imagenes"):
        return None
    for archivo in os.listdir("imagenes"):
        nombre, extension = os.path.splitext(archivo)
        nombre = nombre.lower().replace(" ", "").replace("_", "")
        if nombre == buscado and extension.lower() in (".jpg", ".jpeg", ".png"):
            return os.path.join("imagenes", archivo)
    return None

def mostrar_imagen_plato(nombre_plato):
    ruta = ruta_imagen(nombre_plato)
    if ruta is None:
        return False
    try: 
        subprocess.run(["code", "-r", ruta], shell=True)
        return True
    except OSError:
        try:
            os.startfile(ruta)
            return True
        except OSError:
            return False