def buscar_elemento(lista, campo, valor):
    for elemento in lista:
        if elemento[campo] == valor:
            return True
    return False

def contar_elemento(lista, campo):
    contador = {}

    for elemento in lista:
        if elemento:
            dato = str(elemento[campo])
            if dato in contador:
                contador[dato] += 1
            else:
                contador[dato] = 1

    return contador

def leer_archivo(ruta_archivo):
    codigo = []
    with open(ruta_archivo, 'r') as archivo:
        for linea in archivo:
            linea = linea.strip();
            if linea:
                codigo.append(linea)
    return codigo
