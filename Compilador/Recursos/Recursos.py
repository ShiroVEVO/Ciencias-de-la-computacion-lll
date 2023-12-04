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

def formatear_archivo(lineas):
    codigo_procesado = []
    pila_corchetes = []

    for linea in lineas:
        linea = linea.replace(';', '').replace('"', '')
        if any(tipo in linea for tipo in ['int', 'float', 'char', 'long', 'short']):
            if '=' not in linea:
                continue
            else:
                codigo_procesado.append(linea)
        if '{' in linea:
            pila_corchetes.append('{')

        if pila_corchetes:
            codigo_procesado.append(linea)

            if '}' in linea:
                pila_corchetes.pop()

    return codigo_procesado

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

def leerArchivo(nombre):
    lineas = []
    FormatLines = ([])

    try:
        file = open(nombre, 'r')
        while True:
            linea = str(file.readline())
            if linea:

                linea = linea.replace('\n', '')
                FormatLines.append(linea)
                linea = linea.replace('\t', '')
                # if linea != '' and linea != '\n':
                lineas.append(linea)
            else:
                break
        file.close()
        return lineas
    except FileNotFoundError:
        print("Error con el archivo")