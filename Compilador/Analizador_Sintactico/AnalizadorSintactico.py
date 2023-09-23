from Analizador_Lexico import Separador as s
from Recursos import Pila as pila
from Recursos import Nodo as nodo

"""
validar_bloque:

Recibe todo un bloque de codigo como parametro "codigo", un numero de linea "num_linea" donde 
empezar a validar, se espera que esa linea sea la linea donde se encontraba validando antes de 
ser invocado el metodo, Es decir aquella linea donde se abrió el (,{,[ o /* y una "cadena" que
corresponde al caracter de cierre que se espera. 
Si lo encuentra regresa la pila de codigo que se encontraba dentro del bloque (Si todo es en una
sola linea regresa esa linea), sino lo encuentra en todo lo que falta de codigo regresa una pila 
vacia."""

def validar_bloque(codigo, num_linea, cadena):
    es_valido = False #Parametro de validación
    pi = pila.Pila() #Pila para guardar las lineas involucradas entre apertura y cierre
    i = num_linea  
    while not es_valido and i < len(codigo): # mientras no se haya validado y no supere el maximo de codigo
        pi.apilar(codigo[i]) #se apila la linea
        tokens_linea = s.separador(codigo[i]) #se separa en tokens la linea, Puede ser que el comentario o x
                                            #termine y un salvaje le meta otra linea de codigo luego de eso...
        for elemento in tokens_linea:   #Al dividir en tokens valida si en esa linea esta el cierre que necesita o no
            if str(elemento[1][0]) == cadena:
                es_valido = True        #Si lo esta cambia a que si es valido
        i += 1   
    if not es_valido:   #si al llegar al final del codigo no es valido, vacia la pila y devuelve eso
        pi.vaciar
        return pi
    else:               #si lo encontro y es valido, devuelve la pila con las lineas involucradas
        return pi
    
"""
crear_asa_linea:

Busca crear un arbol de sintaxis abstracta (ASA/AST) a partir de unos "tokens" que se le proporcionan
estos tokens se espera que correspondan unicamente a los tokens asociados a una linea en especifico, 
inicia creando un nodo "linea" que será la raiz del arbol y le agrega unos nodos hijos que corresponden
a los tokens de esa linea.
"""
def crear_asa_linea(tokens):
    raiz = nodo.Nodo("linea") # crea el nodo base
    for token in tokens: #por cada token le agrega un nodo hijo a la raiz
        raiz.agregar_hijo(nodo.Nodo(token))
    return raiz

"""
crear_asa_programa:

usa el metodo crear_asa_linea para crear el arbol de sintaxis abstracta (ASA/AST) de todo el codigo, 
por tanto recibe un codigo general, que debe ser un arreglo de strings correspondientes a cada linea
del codigo, crea un nodo raiz denominado "programa" y le va agregando "hijos" que corresponden
a nodos "linea" que tienen asociados como hijos los tokens de esa linea
"""
def crear_asa_programa(codigo):
    raiz = nodo.Nodo("programa")
    for elemento in codigo:
        tokens_linea = s.separador(elemento)
        raiz.agregar_hijo(crear_asa_linea(tokens_linea))
    return raiz

"""
imprimir_asa

recibe como parametro un nodo raiz "nodo" a partir del cual empezar a imprimir los valores de si mismo, 
y sus nodos hijos, este proceso lo hace iterativamente para cada uno de sus hijos independientemente
de la profundidad, por tanto asi tenga más de 3 niveles de profundidad permitirá imprimir todo el arbol
"""
def imprimir_asa(nodo, profundidad=0):
    print("  " * profundidad, nodo.valor) #imprime el valor del nodo raiz
    for hijo in nodo.hijos: # por cada uno de los hijos del nodo raiz se invoca a si mismo aumentando la profundidad en 1
        imprimir_asa(hijo, profundidad + 1)