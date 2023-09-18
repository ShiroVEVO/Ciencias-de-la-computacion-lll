
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