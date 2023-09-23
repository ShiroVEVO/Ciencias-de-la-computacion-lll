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

def crear_asa(tokens):
    raiz = nodo.Nodo("linea")
    nodo_actual = raiz
    pi = pila.Pila()
    pi.apilar(raiz);
    for token in tokens: 
        nodo_actual.agregar_hijo(nodo.Nodo(token))
        """
        if token[1][0] == "{":
            nuevo_nodo = nodo.Nodo(token)
            nodo_actual.agregar_hijo(nuevo_nodo)
       
            pila.apilar(nuevo_nodo)
            nodo_actual = nuevo_nodo
        elif token == "}":
            pila.desapilar()
            nodo_actual = pila[-1]
        else:
            nodo_actual.agregar_hijo(nodo(token))"""
    return raiz

def imprimir_asa(nodo, profundidad=0):
    print("  " * profundidad, " ", nodo.valor)
    for hijo in nodo.hijos:
        imprimir_asa(hijo, profundidad + 1)