from Analizador_Lexico import Separador as s
from Recursos import Pila as pila
from Recursos import Nodo as nodo

"""validar_bloque:

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

"""validar__punto_y_coma:

recibe la raiz del arbol (ARBOL DE UNA LINEA) y verifica que su ultimo elemento sea un ;"""

#Validar un elemento 
def validar_punto_y_coma(raiz):
    if raiz.ultimo_hijo().valor[1][0] == ';':
        return True
    else: 
        return False

""" validar_estructura:

Recibe una lista de hijos de un nodo raiz, es decir, una lista de nodos cuyo valor se espera
sea de la forma de un token:
    [['CATEGORIA'],['valor']]
y tambien recibe una estructura (una lista de categorias de la fomra ['CATEGORIA','CATEGORIA',...,'CATEGORIA'])
la cual debe corresponder con la sucesión de categorias que tienen cada uno de los hijos. 
Podria decirse que es un metodo que análiza "gramaticas libres de contexto" pero solo en singular
no recibiría plurales de las categorias"""

def validar_estructura(estructura, hijos):
    es_valido = True
    if len(hijos) < len(estructura):
        return es_valido
    elif len(hijos) > len(estructura):
        return es_valido
    else:
        for i in range(len(estructura)-1):
            if estructura[i] != hijos[i].valor[0][0]:
                return not es_valido
            else:
                return es_valido
    
"""validar_tipo_de_dato_variable:

recibe un nodo que se espera sea un nodo del tipo [['PALABRA RESERVADA'],['x']] y comprueba que dentro de la lista
de palabras reservadas esta 'x' sea un tipo de dato nativo de C"""

def validar_tipo_de_dato_variable(nodo):
    es_valido = True
    if nodo.valor[1][0] != 'char' and  nodo.valor[1][0] != 'double' and nodo.valor[1][0] != 'float' and nodo.valor[1][0] != 'int' and nodo.valor[1][0] != 'long' and nodo.valor[1][0] != 'short':
        return not es_valido
    else:
        return es_valido

"""validar_declaracion_variable:

valida la DECLARACIÓN DE UNA VARIABLE, es decir, una linea en C del tipo:
    'PALABRA RESERVADA','IDENTIFICADOR','CARÁCTER PUNTUACIÓN'
para ello usa esa misma estructura (Que bien podriamos llamar gramatica libre de contexto), y los metodos
anteriormente definidos (validación del ;, validación del tipo de dato y validación de la estructura), si 
alguna de esas validaciones falla, entonces no comprueba lo demás y regresa que no es valido."""

def validar_declaracion_variable(raiz):
    es_valido = True
    estructura = ['PALABRA RESERVADA','IDENTIFICADOR','CARÁCTER PUNTUACIÓN']
    hijos = raiz.get_hijos() 

    if not validar_punto_y_coma(raiz):
        return not es_valido
    elif not validar_tipo_de_dato_variable(hijos[0]):
        return not es_valido
    elif not validar_estructura(estructura, hijos):
        return es_valido
    else:
        return es_valido
    
def validar_asignación(raiz):
    """
    puede ser de la forma: 
    TIPO IDENTIFICADOR = NUMERO/CADENA  ----    X
    IDENTIFICADOR = FUNCIÓN(PARAMETROS)
    IDENTIFICADOR = IDENTIFICADOR OPERADOR IDENTIFICADOR
    o una combinación de varios de estos 
    """
    es_valido = True
    estructuraA = ['IDENTIFICADOR','OPERADOR ASIGNACIÓN','NUMERO FLOTANTE']






    estructuraB = ['IDENTIFICADOR','OPERADOR ASIGNACIÓN','NUMERO ENTERO']
    estructuraC = ['IDENTIFICADOR','OPERADOR ASIGNACIÓN','LITERAL DE CADENA']
    estructuraD = ['IDENTIFICADOR','OPERADOR ASIGNACIÓN','IDENTIFICADOR','OPERADOR MATEMÁTICO','IDENTIFICADOR']

    hijos = raiz.get_hijos() 
    if not validar_punto_y_coma(raiz):
        return not es_valido
    
    else:
        return es_valido

"""


1. MODIFICACION DEL SEPARADOR O DEL LECTOR PARA NO PERMITIR DOS LINEAS EN UNA MISMA (EXCEPTO EN EL FOR)
2. Alterar la funcion de ; para que reciba la existencia de cualquier elemento 
3. atomica de operacion matematica "IDENTIFICADOR OPERADOR MATEMATICO IDENTIFICADOR"
4. atomica de parametros "TIPO IDENTIFICADOR" = declaracion variable
5. atomica de condicion "IDENTIFICADOR OPERADOR LOGICO IDENTIFICADOR"
6. atomica condicion 2 "IDENTIFICADOR OPERADOR COMPARACIÓN IDENTIFICADOR"
7. atomica incremental decremental ++ -- += -= =+ =-
8. Atomica de argumentos argumento + argumento" (Print, argumento como identificador, cadena)
9. atomica de argumentos 2 "Argumento, Argumento" (con tipos de argumento para funciones generales)

"""
