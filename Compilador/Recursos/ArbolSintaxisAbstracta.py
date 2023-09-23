from Recursos import Nodo as nodo
from Analizador_Lexico import Separador as s

class ArbolSintaxisAbstracta:
    def __init__(self):
        self.raiz = []

    def __iter__(self):
        self.n = len(self.items)
        return self

    def __next__(self):
        if self.n > 0:
            self.n -= 1
            return self.items[self.n]
        else:
            raise StopIteration
        
"""crear_asa_linea:

Busca crear un arbol de sintaxis abstracta (ASA/AST) a partir de unos "tokens" que se le proporcionan
estos tokens se espera que correspondan unicamente a los tokens asociados a una linea en especifico, 
inicia creando un nodo "linea" que será la raiz del arbol y le agrega unos nodos hijos que corresponden
a los tokens de esa linea."""

def crear_asa_linea(tokens):
    raiz = nodo.Nodo("linea") # crea el nodo base
    for token in tokens: #por cada token le agrega un nodo hijo a la raiz
        raiz.agregar_hijo(nodo.Nodo(token))
    return raiz

"""crear_asa_programa:

usa el metodo crear_asa_linea para crear el arbol de sintaxis abstracta (ASA/AST) de todo el codigo, 
por tanto recibe un codigo general, que debe ser un arreglo de strings correspondientes a cada linea
del codigo, crea un nodo raiz denominado "programa" y le va agregando "hijos" que corresponden
a nodos "linea" que tienen asociados como hijos los tokens de esa linea"""

def crear_asa_programa(codigo):
    raiz = nodo.Nodo("programa")
    for elemento in codigo:
        tokens_linea = s.separador(elemento)
        raiz.agregar_hijo(crear_asa_linea(tokens_linea))
    return raiz

"""imprimir_asa

recibe como parametro un nodo raiz "nodo" a partir del cual empezar a imprimir los valores de si mismo, 
y sus nodos hijos, este proceso lo hace iterativamente para cada uno de sus hijos independientemente
de la profundidad, por tanto asi tenga más de 3 niveles de profundidad permitirá imprimir todo el arbol"""

def imprimir_asa(nodo, profundidad=0):
    print("  " * profundidad, nodo.valor) #imprime el valor del nodo raiz
    for hijo in nodo.hijos: # por cada uno de los hijos del nodo raiz se invoca a si mismo aumentando la profundidad en 1
        imprimir_asa(hijo, profundidad + 1)
    
