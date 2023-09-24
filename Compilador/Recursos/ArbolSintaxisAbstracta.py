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

def crear_nodo_padre(raiz,inicio,final,valor):
    hijos = raiz.get_hijos()
    nodo_padre = nodo.Nodo(valor)
    nodos_a_mover = raiz.hijos[inicio:final + 1]
    for x in nodos_a_mover:
        nodo_padre.agregar_hijo(x)
    raiz.hijos[inicio:final + 1] = []
    raiz.hijos.insert(inicio, nodo_padre)
    return raiz
#
#
#--------------------------------------------MI AVANCE--------------------------------------------
"""
Crea un ASA a partir de una lista de tokens. Este me ayuda a validar una cadena completa, ya que el arbol 
queda así:
linea
   cadena
     [['IDENTIFICADO'], ['pedro']]
     [['IDENTIFICADO'], ['pascal']]
   [['OPERADOR MATEM�TICO'], [',']]
   [['IDENTIFICADOR'], ['a']]
Args: tokens (list): Lista de tokens, donde cada token es una lista de la forma [['TIPO'], ['VALOR']]
Returns: nodo.Nodo: El nodo raíz del ASA construido.
"""
def crear_asa_comentario(tokens):
    # Inicialización de variables
    primer_tipo_nodo_cadenas = True  # Indica si es el primer tipo de nodo de cadenas encontrado

    raiz = nodo.Nodo("linea")  # Crea el nodo raíz
    pila_nodos = [raiz]  # Utilizamos una pila para llevar un seguimiento de los nodos padres
    ultimo_nodo = raiz  # Inicializamos el último nodo abierto con el nodo raíz

    # Iteramos sobre los tokens
    for token in tokens:
        valor = token[1]
        # Caso: Cadena
        if valor == ['"']:
            if primer_tipo_nodo_cadenas:
                nuevo_nodo = nodo.Nodo("cadena")  # Creamos un nuevo nodo tipo "cadena"
                ultimo_nodo.agregar_hijo(nuevo_nodo)  # Agregamos el nuevo nodo como hijo del último nodo abierto
                pila_nodos.append(nuevo_nodo)  # Agregamos el nuevo nodo a la pila de nodos
                ultimo_nodo = nuevo_nodo  # Actualizamos el último nodo abierto
                primer_tipo_nodo_cadenas = False  # Desactivamos el indicador de primer tipo de nodo de cadenas
            else:
                pila_nodos.pop()  # Sacamos el último nodo padre de la pila
                ultimo_nodo = pila_nodos[-1] if pila_nodos else raiz  # Actualizamos el último nodo abierto
                primer_tipo_nodo_cadenas = True
        # Caso: Otro tipo de token
        else:
            ultimo_nodo.agregar_hijo(nodo.Nodo(token))  # Agregamos un nuevo hijo al último nodo abierto

    return raiz # Devolvemos el nuevo árbol construido

"""
Crea un nuevo árbol manteniendo la estructura de paréntesis del árbol original.
Este de aquí no sirve de nada, solo estaba tratando de hacer unas pruebas para lo que querias de
comparacion
Args: arbol (Nodo): El árbol original.
Returns: Nodo: El nuevo árbol generado.
"""
def crear_asa_parentesis_arbol(arbol):
    raiz = nodo.Nodo("linea") # Crea el nodo raíz del nuevo árbol
    pila_nodos = [raiz] # Utilizamos una pila para llevar un seguimiento de los nodos padres
    ultimo_nodo = raiz # Inicializamos el último nodo abierto con el nodo raíz del nuevo árbol

    # Función recursiva para procesar los nodos del árbol original
    def procesar_nodo(nodo_original):
        for hijo in nodo_original.get_hijos():
            nonlocal ultimo_nodo  # Indicamos que estamos usando la variable del ámbito externo

            # Caso: Paréntesis de apertura '('
            if hijo.valor[0][0] == 'SÍMBOLO ESPECIAL' and hijo.valor[1][0] == '(':
                nuevo_nodo = nodo.Nodo("()") # Creamos un nuevo nodo padre "()"
                ultimo_nodo.agregar_hijo(nuevo_nodo) # Agregamos el nuevo nodo como hijo del último nodo abierto
                pila_nodos.append(nuevo_nodo) # Agregamos el nuevo nodo a la pila de nodos
                ultimo_nodo = nuevo_nodo # Actualizamos el último nodo abierto
                procesar_nodo(hijo) # Llamada recursiva para procesar los hijos del nodo original

            # Caso: Paréntesis de cierre ')'
            elif hijo.valor[0][0] == 'SÍMBOLO ESPECIAL' and hijo.valor[1][0] == ')':
                pila_nodos.pop() # Sacamos el último nodo padre de la pila
                ultimo_nodo = pila_nodos[-1] if pila_nodos else raiz # Actualizamos el último nodo abierto

            # Caso: Otro tipo de token
            else:
                ultimo_nodo.agregar_hijo(hijo) # Agregamos un nuevo hijo al último nodo abierto

    procesar_nodo(arbol) # Iniciamos el procesamiento del árbol original

    return raiz # Devolvemos el nuevo árbol construido









