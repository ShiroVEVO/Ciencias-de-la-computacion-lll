from Analizador_Lexico import Separador as s
from Recursos import Pila as pila
from Recursos import Nodo as nodo

"""
cariño!!!, creo que me equivoqué, no siempre se necesitarán los arboles como parametro, en ocasiones podemos pasar solo algunos
hijos, es decir partecitas especificas del arbol, Mira el metodo de validar_operación_matematica y piensa lo siguiente, Si te paso
la linea

int a = b + c;

el arbol llamado "raiz" seria tooooda la linea, pero las partes más atómicas como la operación matematica no necesitan toda la linea
sino solo unos hijos de esta...
        ///(Los hijos son una lista de nodos cuyo valor es de la forma [['CATEGORIA_TOKEN'],[VALOR_LEXEMA]])////
que vendrian siendo el "b+c". Ahora bien, el otro lado del igual el "int a" se debe validar con el atomico
de "declaración" que sigue la gramatica [TIPO, IDENTIFICADOR].
Y la linea en su conjunto se validará con el "validar linea asignación, quien será el que invoque los metodos para validar tanto
el "int a" como el "b + c".
En conclusión en ocasiones los metodos más pequeñitos, que validan las cosas más atomicas pueden simplemente recibir una lista con
los hijos necesarios. solo las validaciones más generales recibiran la linea entera. 


1. (HECHO) MODIFICACION DEL SEPARADOR O DEL LECTOR PARA NO PERMITIR DOS LINEAS EN UNA MISMA (EXCEPTO EN EL FOR)
2. (HECHO) Alterar la funcion de ; para que reciba la existencia de cualquier elemento 
3. (HECHO) atomica de operacion matematica "IDENTIFICADOR OPERADOR MATEMATICO IDENTIFICADOR"
4. (HECHO) atomica de (parametros/Declaracion Variable) "TIPO IDENTIFICADOR"
5. (HECHO, DISCUTIBLE)atomica comparacion "IDENTIFICADOR/NUMEROS/CADENAS... OPERADOR COMPARACIÓN (lo mismo de antes del operador)
    para la 5. no hay que quitar el ++ -- de operadores de comparación?? Ya cree otra cateogia, pero solo con esos dos
6. (Chale...)atomica de condicion "comparacion/identificador OPERADOR LOGICO comparacion/identificador" (Como manejamos el !??)
7. atomica incremental decremental ++ -- += -= =+ =-
8. (HECHO, aunque lo mismo de comparación) Atomica de argumentos "argumento + " (Print, argumento como identificador, cadena)
9. (HECHO, aunque lo mismo de comparación) Atomica de argumentos 2 "Argumento ," (con tipos de argumento para funciones generales)
"""

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


"""validar_operacion_matematica:

Recibe unos "hijos" (lista de nodos cuyo valor son tokens) y valida las posibles combinaciones para una 
operación matematica es decir, que tenga un operador matematico en la mitad y que a ambos lados de ellos
tenga Identificador, Numero Entero o Numero flotante, Excluyendo las combinaciones donde se intentan operar
Numeros flotantes con Numeros enteros."""


def validar_operacion_matematica(hijos):
    es_valido = True
    estructura = [['IDENTIFICADOR', 'NUMERO ENTERO', 'NUMERO FLOTANTE'], ['OPERADOR MATEMÁTICO'],
                  ['IDENTIFICADOR', 'NUMERO FLOTANTE', 'NUMERO ENTERO']]
    if validar_estructura(estructura, hijos):
        if ((hijos[0].valor[0][0] == 'NUMERO FLOTANTE' and hijos[2].valor[0][0] == 'NUMERO ENTERO') or (
                hijos[0].valor[0][0] == 'NUMERO ENTERO' and hijos[2].valor[0][0] == 'NUMERO FLOTANTE')):
            return not es_valido
        else:
            return es_valido
    else:
        return not es_valido


"""validar_declaracion_variable_parametros:

Recibe unos "hijos" (lista de nodos cuyo valor son tokens) y valida que estos tengan la estructura
PALABRA RESERVADA - IDENTIFICADOR, Si cumple con ello luego evalua si la palabra reservada
es un tipo de dato, si no lo es, regresa un False, si lo es Regresa un True"""


def validar_declaracion_variable_parametros(hijos):
    es_valido = True
    estructura = [['PALABRA RESERVADA'], ['IDENTIFICADOR']]
    if validar_estructura(estructura, hijos):
        print("Aja!")
        if hijos[0].valor[1][0] != 'char' and hijos[0].valor[1][0] != 'double' and hijos[0].valor[1][0] != 'float' and \
                hijos[0].valor[1][0] != 'int' and hijos[0].valor[1][0] != 'long' and hijos[0].valor[1][0] != 'short':
            return not es_valido
        else:
            return es_valido
    else:
        print("Aiñ!")
        return not es_valido


"""validar_comparacion:
Recibe unos "hijos" (lista de nodos cuyo valor son tokens) y valida que estos tengan
la estructura de un atomico de comparación basico, es decir que tengan un operador
de comparación en la mitad, y a ambos lados de este tengan un identificador (sea de
variable o de función, un numero entero, un numero flotante o una cadena).

POR AHORA, excluye los operadores de comparación ++ y -- porqué creo que no se usan
en ninguna comparación =-= pero no estoy seguro, lo hablamos luego, besos en las nalgas JAJAJAJAJA"""


def validar_comparacion(hijos):
    es_valido = True
    estructura = [['IDENTIFICADOR', 'NUMERO ENTERO', 'NUMERO FLOTANTE', 'LITERAL DE CADENA'],
                  ['OPERADOR COMPARACIÓN'],
                  ['IDENTIFICADOR', 'NUMERO FLOTANTE', 'NUMERO ENTERO', 'LITERAL DE CADENA']]
    if validar_estructura(estructura, hijos):
        return es_valido
    else:
        return not es_valido


def validar_condicion(raiz):  # comparacion/identificador OPERADOR LOGICO comparacion/identificador
    es_valido = True
    estructura = [['IDENTIFICADOR'], ['OPERADOR LÓGICO'], ['IDENTIFICADOR']]
    """
        Me acabo de dar cuenta de la utilidad de los nodos intermedios JAJAJAJA
        Si empaquetamos los atomicos que ya validamos bajo una nueva etiqueta, es decir un nuevo nodo, que se
        convierta en un intermediario podemos usarlo aquí para validar con la estructura

        Se me ocurre crear un metodo en nodo.py... que "empaquete" unos nodos bajo un nuevo alias, como si fuese un nuevo "token"
        y que se convierta en un nodo papa entre la raiz y los hijos el cual podemos usar y llamamos ese metodo 
        en cada uno de los metodos que ya hice que son SI son atomicos para asi comparar facilmente... algo como:

        ESTOOOO
        linea <- NODO RAIZ
            [['IDENTIFICADOR'],['a']] <- NODOS HIJOS de aqui para abajo...
            [['OPERADOR COMPARACIÓN'],['>=']]
            [['IDENTIFICADOR'],['b']]
            [['OPERADOR LOGICO'], [&&]]
            [['IDENTIFICADOR'],['a']]
            [['OPERADOR COMPARACIÓN'],['!=']]
            [['IDENTIFICADOR'],['b']]
        
        PASA A ESTOOO!

        linea <- NODO RAIZ, Ahora le dire abuelo
            [['COMPARACIÓN'],['']] <- Nodo PAPA creado por el metodo
                [['IDENTIFICADOR'],['a']] <- Nodos Hijos del papa
                [['OPERADOR COMPARACIÓN'],['>=']]
                [['IDENTIFICADOR'],['b']]
            [['OPERADOR LOGICO'], [&&]] <- Nodo sin papa JAJAJA
            [['COMPARACIÓN'],['']] <- Papa 2
                [['IDENTIFICADOR'],['a']] <- Nodos Hijos del papa 2
                [['OPERADOR COMPARACIÓN'],['!=']]
                [['IDENTIFICADOR'],['b']]

        Lo expliqué lo mejor que pude... porque ya son las 8:46 y me vas a dar nalgadas de las malas...
        Hablamos mañana :3 sorry por dejarte las alteraciones más hardcore :((
    """
    return None


# --------------------------------------------------- HASTA AQUÍ LLEGA EL CODIGO UTIL-------------

""" 
validar_tipo_de_dato_variable:

recibe un nodo que se espera sea un nodo del tipo [['PALABRA RESERVADA'],['x']] y comprueba que dentro de la lista
de palabras reservadas esta 'x' sea un tipo de dato nativo de C

def validar_tipo_de_dato_variable(nodo):
    es_valido = True
    if nodo.valor[1][0] != 'char' and  nodo.valor[1][0] != 'double' and nodo.valor[1][0] != 'float' and nodo.valor[1][0] != 'int' and nodo.valor[1][0] != 'long' and nodo.valor[1][0] != 'short':
        return not es_valido
    else:
        return es_valido

    
"""

# ----------------------------AQUÍ EMPIEZA MI CODIGO------------------------------
"""validar_argumentos normales:
Recibe unos "hijos" (lista de nodos cuyo valor son tokens) y valida que estos tengan
la estructura de un atomico de argumento basico, es decir que tengan un cáracter de 
puntuación específico (,) en la mitad, y a ambos lados de este tengan un identificador (sea de
variable o de función, un numero entero, un numero flotante o una cadena).
"""


def validar_argumentos(hijos):
    es_valido = True
    estructura = [['IDENTIFICADOR', 'NUMERO ENTERO', 'NUMERO FLOTANTE'], ['CARÁCTER PUNTUACIÓN']]
    print()
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
