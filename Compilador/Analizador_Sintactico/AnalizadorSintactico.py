from Analizador_Lexico import Separador as s
from Recursos import Pila as pila
from Recursos import Nodo as nodo
from Recursos import ArbolSintaxisAbstracta as asa

"""
1. (HECHO) SALVO EL...(Como manejamos el !??)
2. (HECHO) atomica incremental decremental ++ -- 
3. Declaración funcion 
4. Asignación 
5. Llamada función
6. Sentencia If
7. While

"""
#---------------------- INICIO ATOMICAS -----------------
"""validar_bloque:

Recibe todo un bloque de codigo como parametro "codigo", un numero de linea "num_linea" donde 
empezar a validar, se espera que esa linea sea la linea donde se encontraba validando antes de 
ser invocado el metodo, Es decir aquella linea donde se abrió el (,{,[ o /* y una "cadena" que
corresponde al caracter de cierre que se espera. 
Si lo encuentra regresa la pila de codigo que se encontraba dentro del bloque (Si todo es en una
sola linea regresa esa linea), sino lo encuentra en todo lo que falta de codigo regresa una pila 
vacia."""
def validar_bloque(codigo, num_linea, cadena):
    es_valido = False  # Parametro de validación
    pi = pila.Pila()  # Pila para guardar las lineas involucradas entre apertura y cierre
    i = num_linea
    while not es_valido and i < len(codigo):  # mientras no se haya validado y no supere el maximo de codigo
        pi.apilar(codigo[i])  # se apila la linea
        tokens_linea = s.separador(codigo[i])  # se separa en tokens la linea, Puede ser que el comentario o x
        # termine y un salvaje le meta otra linea de codigo luego de eso...
        for elemento in tokens_linea:  # Al dividir en tokens valida si en esa linea esta el cierre que necesita o no
            if str(elemento[1][0]) == cadena:
                es_valido = True  # Si lo esta cambia a que si es valido
        i += 1
    if not es_valido:  # si al llegar al final del codigo no es valido, vacia la pila y devuelve eso
        pi.vaciar
        return pi
    else:  # si lo encontro y es valido, devuelve la pila con las lineas involucradas
        return pi

"""validar_caracter:

Recibe:
    1. un arbol de una UNICA LINEA denominado como "raiz", 
    2. un caracter como "caracter"
y Busca en el arbol de la linea si alguno de los hijos es el caracter buscado, Si lo encuentra
devuelve un True si no lo encuentra devuelve un False."""
def validar_caracter(raiz, caracter):
    existe = False
    hijos = raiz.get_hijos()
    for hijo in hijos:
        if hijo.valor[1][0] == caracter:
            existe = True
    return existe

def validar_token(raiz, token):
    existe = False
    hijos = raiz.get_hijos()
    for hijo in hijos:
        if hijo.valor[0][0] == token:
            existe = True
    return existe

"""validar_estructura:

Recibe una lista de hijos de un nodo raiz, es decir, una lista de nodos cuyo valor se espera
sea de la forma de un token:
    [['CATEGORIA'],['valor']]
y tambien recibe una estructura (una MULTILISTA de categorias), para todas las posibles opciones 
de una gramatica particular, los hijos se van a validar a ver si corresponden a alguna de las 
posibilidades de la gramatica alojadas en la multilista "estructuras".

Por ejemplo si queremos validar la estructura de una operación matematica
tenemos las posibilidades:

IDENTIFICADOR OPERADOR MATEMATICO IDENTIFICADOR
IDENTIFICADOR OPERADOR MATEMATICO NUMERO ENTERO
IDENTIFICADOR OPERADOR MATEMATICO NUMERO FLOTANTE
NUMERO ENTERO OPERADOR MATEMATICO IDENTIFICADOR
NUMERO ENTERO OPERADOR MATEMATICO NUMERO ENTERO
NUMERO ENTERO OPERADOR MATEMATICO NUMERO FLOTANTE   -- SE ELIMINA EN EL VALIDADOR ESPECIFICO por la incompatibilidad de tipos
NUMERO FLOTANTE OPERADOR MATEMATICO NUMERO FLOTANTE
NUMERO FLOTANTE OPERADOR MATEMATICO IDENTIFICADOR
NUMERO FLOTANTE OPERADOR MATEMATICO NUMERO ENTERO -- SE ELIMINA EN EL VALIDADOR ESPECIFICO por la incompatibilidad de tipos

asi pues pasariamos una lista de 3 espacios, en la lista del primer espacio habrán 3 posibilidades, en la lista del
segundo espacio habrá 1 posibilidad, y en la lista del tercer espacio habran 3 posibilidades. lo que nos evita definir
las 7 gramaticas posibles y evaluar cada una con un metodo simple de estructura como lista, en su lugar solo manejamos 
una multilista y excluimos esas 2 posibilidades erroneas en el validador especifico de las operaciones matematicas"""
def validar_estructura(estructura, hijos):
    es_valido = True
    if len(hijos) != len(estructura):
        return not es_valido
    else:
        for i in range(len(estructura)):
            for j in range(len(estructura[i])):
                if estructura[i][j] != hijos[i].valor[0][0]:
                    es_valido = False
                else:
                    es_valido = True
                    break
            if not es_valido:
                break
    return es_valido

"""validar_operacion_matematica: (ACTUALIZADO A NODO PAPA)

Recibe un arbol raiz (Se espera que sea el arbol de una linea), un indice (Numero del hijo donde
inicia la operación matematica) y un rango (donde termina la operación matematica) tomando esos 
hijos valida las posibles combinaciones para una  operación matematica es decir, que tenga un 
operador matematico en la mitad y que a ambos lados de ellos tenga Identificador, Numero Entero, 
Numero flotante u otra operación matematica (a +-*/% b) Excluyendo las combinaciones donde se 
intentan operar Numeros flotantes con Numeros enteros. al encontrarla crea un nodo papa de 
"Operación matematica" y los nodos hijos de raiz que se involucran con esta operación pasan a 
ser hijos del nodo papa.
"""
def validar_operacion_matematica(raiz, inicial, final):
    hijos = raiz.hijos[inicial:final + 1]
    valor_papa = [['OPERACIÓN MATEMATICA'],['']]
    estructura = [['IDENTIFICADOR', 'NUMERO ENTERO', 'NUMERO FLOTANTE','OPERACIÓN MATEMATICA'],
                  ['OPERADOR MATEMÁTICO'],
                  ['IDENTIFICADOR', 'NUMERO FLOTANTE', 'NUMERO ENTERO','OPERACIÓN MATEMATICA']]
    if validar_estructura(estructura, hijos):
        if ((hijos[0].valor[0][0] == 'NUMERO FLOTANTE' and hijos[2].valor[0][0] == 'NUMERO ENTERO') or (
                hijos[0].valor[0][0] == 'NUMERO ENTERO' and hijos[2].valor[0][0] == 'NUMERO FLOTANTE')):
            return None
        else:
           return asa.crear_nodo_padre(raiz,inicial,final,valor_papa) 
    else:
        return None

"""validar_declaracion_variable_parametros: (ACTUALIZADO A NODO PAPA)

Recibe unos "hijos" (lista de nodos cuyo valor son tokens) y valida que estos tengan la estructura
PALABRA RESERVADA - IDENTIFICADOR, Si cumple con ello luego evalua si la palabra reservada
es un tipo de dato, si no lo es, regresa un False, si lo es Regresa un True"""
def validar_declaracion_variable_parametros(raiz,inicial,final):
    hijos = raiz.hijos[inicial:final + 1]
    es_valido = True
    valor_papa = [['DECLARACIÓN VARIABLE/PARAMETROS'],['']]
    estructura = [['PALABRA RESERVADA'], ['IDENTIFICADOR']]
    if validar_estructura(estructura, hijos):
        if hijos[0].valor[1][0] != 'char' and hijos[0].valor[1][0] != 'double' and hijos[0].valor[1][0] != 'float' and \
                hijos[0].valor[1][0] != 'int' and hijos[0].valor[1][0] != 'long' and hijos[0].valor[1][0] != 'short':
            return None
        else:
            return asa.crear_nodo_padre(raiz,inicial,final,valor_papa)
    else:
        return None

"""validar_comparacion: (ACTUALIZADO A NODO PAPA)
Recibe unos "hijos" (lista de nodos cuyo valor son tokens) y valida que estos tengan
la estructura de un atomico de comparación basico, es decir que tengan un operador
de comparación en la mitad, y a ambos lados de este tengan un identificador (sea de
variable o de función, un numero entero, un numero flotante o una cadena)."""
def validar_comparacion(raiz, inicial, final):
    hijos = raiz.hijos[inicial:final + 1]
    valor_papa = [['COMPARACIÓN'],['']]
    estructura = [['IDENTIFICADOR', 'NUMERO ENTERO', 'NUMERO FLOTANTE', 'LITERAL DE CADENA','COMPARACIÓN'],
                  ['OPERADOR COMPARACIÓN'],
                  ['IDENTIFICADOR', 'NUMERO FLOTANTE', 'NUMERO ENTERO', 'LITERAL DE CADENA','COMPARACIÓN']]
    if validar_estructura(estructura, hijos):
        return asa.crear_nodo_padre(raiz,inicial,final,valor_papa)
    else:
        return None

def validar_condicion(raiz, inicial,final):
    hijos = raiz.hijos[inicial:final + 1]
    estructura = [['IDENTIFICADOR','COMPARACIÓN'], ['OPERADOR LÓGICO'], ['IDENTIFICADOR','COMPARACIÓN']]
    estructuraB = [['OPERADOR LÓGICO'],['IDENTIFICADOR','COMPARACIÓN','OPERADOR LÓGICO']] #DEFINIRLO CON IF SEGUN LA LONGITUD DIFERENCIA ENTRE INICIAL Y FINAL
    valor_papa = [['CONDICIÓN'],['']]
    if (final+1 - inicial) == 3:
        if validar_estructura(estructura, hijos) and hijos[1].valor[1][0] != '!':
            return asa.crear_nodo_padre(raiz,inicial,final,valor_papa)
        else:
            asa.imprimir_asa(raiz)
            return None
    elif(final+1 - inicial) == 2:
            if validar_estructura(estructuraB, hijos) and hijos[0].valor[1][0] == '!':
                return asa.crear_nodo_padre(raiz,inicial,final,valor_papa)
            else:
                asa.imprimir_asa(raiz)
                return None

def validar_incremental_decremental(raiz,inicial,final):
    hijos = raiz.hijos[inicial:final + 1]
    estructura = [['IDENTIFICADOR','OPERACIÓN MATEMATICA','CARÁCTER INC-DEC'], ['IDENTIFICADOR','OPERACIÓN MATEMATICA','CARÁCTER INC-DEC']]
    valor_papa = [['INCREMENTAL DECREMENTAL'],['']]
    if validar_estructura(estructura, hijos):
        return asa.crear_nodo_padre(raiz,inicial,final,valor_papa) 
    else:
        return None

"""validar_argumentos normales:
Recibe unos "hijos" (lista de nodos cuyo valor son tokens) y valida que estos tengan
la estructura de un atomico de argumento basico, es decir que tengan un cáracter de 
puntuación específico (,) en la mitad, y a ambos lados de este tengan un identificador (sea de
variable o de función, un numero entero, un numero flotante o una cadena).
"""
def validar_argumentos(hijos):
    es_valido = True
    estructura = [['IDENTIFICADOR', 'NUMERO ENTERO', 'NUMERO FLOTANTE'], ['CARÁCTER PUNTUACIÓN']]
    print(hijos[0].valor)
    if validar_estructura(estructura, hijos) or hijos[0].valor == "cadena":
        if len(hijos) == 1:
            return es_valido
        elif not hijos[1].valor[1][0] == ",":
            return not es_valido
        else:
            return es_valido
    else:
        return not es_valido

"""validar_argumentos de printf, donde solo se pueden identificadores y cadenas"""
def validar_argumentos_printf(hijos):
    es_valido = True
    estructura = [['IDENTIFICADOR'], ['OPERADOR MATEMÁTICO']]
    if validar_estructura(estructura, hijos) or hijos[0].valor == "cadena":
        if len(hijos) == 1:
            return es_valido
        elif not hijos[1].valor[1][0] == "+":
            return not es_valido
        else:
            return es_valido
    else:
        return not es_valido

#------------------- FIN ATOMICAS ------------------------

#---------------- INICIO COMPUESTAS ----------------------

def validar_asignacion(raiz):
    es_valido = True
    i = 0
    hijos = raiz.get_hijos()
    estructura = [['IDENTIFICADOR','DECLARACIÓN VARIABLE/PARAMETROS'],
                  ['OPERADOR ASIGNACIÓN'],
                  ['IDENTIFICADOR','OPERACIÓN MATEMATICA','NUMERO ENTERO', 'NUMERO FLOTANTE','CADENA'],
                  ['CARÁCTER PUNTUACIÓN']]

    while i < len(hijos):
        if hijos[i].valor[0][0] == 'OPERADOR MATEMÁTICO':
            raiz = validar_operacion_matematica(raiz, i - 1, i + 1)
            if raiz is None:
                return not es_valido
            else:
                hijos = raiz.get_hijos()
                i = 0 
                asa.imprimir_asa(raiz)
        else:
            i += 1
    if hijos[0].valor[0][0] == 'PALABRA RESERVADA':
        return es_valido
    elif hijos[0].valor[0][0] == 'IDENTIFICADOR':
        return es_valido
    else:
        return not es_valido
    """
    posibilidades: 
    Declaracion = Operacion matematica/NumeroEntero/Identificador/NumeroFlotante
    Identificador = Operacion matematica/NumeroEntero/Identificador/NumeroFlotante/cadenas
    """


