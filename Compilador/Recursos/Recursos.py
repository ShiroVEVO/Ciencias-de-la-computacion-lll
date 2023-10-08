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

""" leer_archivo:

Recibe por parametro una ruta absoluta "ruta_archivo" desde la raiz del proyecto es decir, 
Para rutas internas del Proyecto del compilador requiere que se especifique ese directorio
al principio de la ruta por ejemplo:
    Compilador/Analizado_Lexico/tokens.py
Si es en la carpeta general de compilador: 
    Compilador/archivo.c
luego de leerlo, omite las tabulaciones y espacios iniciales y finales. Luego comprueba, si
la linea tiene un ";" si lo tiene lo reemplaza con ";@" y posteriormente divide esa linea
a partir de los @, Esto permite que en casos donde hay varias lineas de codigo (cuya terminación
es ";") en una misma linea, las estandarice separandolas en varias lineas. 
Se introduce el @ debido a que el metodo .split() elimina el caracter mediante el cual el 
metodo "splitea" asi que si se hace .split(";") dividiría pero quitaría todos los ";" 
Luego comprueba que las lineas no sean vacias (Porque al splitear una linea que termina en ";" y no
tiene nada más allá de este generaría un arreglo con 2 posiciones la linea y un string vacio) y al final
las agrega al arreglo "codigo"
"""

def leer_archivo(ruta_archivo): 
    codigo = []
    with open(ruta_archivo, 'r') as archivo:
        for linea in archivo:
            linea = linea.strip(); # omite espacios iniciales y finales
            if ";" in linea and not "for" in linea:
                linea = linea.replace(";", ";@")
                lineas = linea.split("@")
                for linea in lineas:
                    if linea:
                        codigo.append(linea)
            else: 
                if linea:
                    codigo.append(linea)
    return codigo
