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

"""
Recibe por parametro una ruta absoluta "ruta_archivo" desde la raiz del proyecto es decir, 
Para rutas internas del Proyecto del compilador requiere que se especifique ese directorio
al principio de la ruta por ejemplo:
    Compilador/Analizado_Lexico/tokens.py
Si es en la carpeta general de compilador: 
    Compilador/archivo.c
luego de leerlo, omite las tabulaciones y espacios iniciales asi como todas las lineas que
sean de separación y las va introduciendo en un arreglo "codigo" el cual devolverá una vez
termine de leer el archivo.
"""
def leer_archivo(ruta_archivo): 
    codigo = []
    with open(ruta_archivo, 'r') as archivo:
        for linea in archivo:
            linea = linea.strip();
            if linea:
                codigo.append(linea)
    return codigo
