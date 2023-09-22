from Analizador_Lexico import separador as s
from Recursos import pila as pila

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
    es_valido = False
    pi = pila.Pila()
    i = num_linea
    while not es_valido and i < len(codigo):
        pi.apilar(codigo[i])
        tokens_linea = s.separador(codigo[i])
        for elemento in tokens_linea:
            if str(elemento[1][0]) == cadena:
                es_valido = True
        i += 1
    if not es_valido:
        pi.vaciar
        return pi
    else:
        return pi
